# app/api/patient/patientroutes.py

import json
import os

import httpx
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.storage import delete_patient_files, upload_patient_file
from app.models.patientmodel.demographicmodel import Demographic
from app.models.patientmodel.diagnosisnotesmodel import DiagnosisNotes
from app.models.patientmodel.doctorassessmentmodel import DoctorAssessment
from app.models.patientmodel.hospitaloperationsmodel import HospitalOperations
from app.models.patientmodel.imagingdatamodel import ImagingData
from app.models.patientmodel.labresultsmodel import LabResults
from app.models.patientmodel.lifestyledatamodel import LifestyleData
from app.models.patientmodel.medicalhistorymodel import MedicalHistory
from app.models.patientmodel.medicationsmodel import Medications
from app.models.patientmodel.nursenotesmodel import NurseNote
from app.models.patientmodel.remotemonitoringmodel import RemoteMonitoring
from app.models.patientmodel.vitalsignsmodel import VitalSigns
from app.schemas.patientschema.demographicschema import DemographicCreate
from app.schemas.patientschema.diagnosisnotesschema import DiagnosisNotesSchema
from app.schemas.patientschema.hospitaloperationsschema import HospitalOperationsSchema
from app.schemas.patientschema.imagingdataschema import ImagingDataSchema
from app.schemas.patientschema.labresultschema import LabResultsSchema
from app.schemas.patientschema.lifestyledataschema import LifestyleDataSchema
from app.schemas.patientschema.medicalhistoryschema import MedicalHistorySchema
from app.schemas.patientschema.medicationschema import MedicationsSchema
from app.schemas.patientschema.remotemonitoringschema import RemoteMonitoringSchema
from app.schemas.patientschema.vitalsignschema import VitalSignsSchema

patientrouter = APIRouter(prefix="/patients", tags=["Patients"])

ALLOWED_SPACE_HOST = os.getenv("SPACE_BUCKET", "") + "." + os.getenv("SPACE_REGION", "") + ".digitaloceanspaces.com"

@patientrouter.post("/extract-text")
async def extract_text_from_file(file: UploadFile = File(...)):
    ext = (file.filename or "").split(".")[-1].lower()
    contents = await file.read()
    text = ""
    error = ""
    try:
        if ext in ("jpg", "jpeg", "png", "bmp", "tiff", "tif", "webp"):
            import io
            import easyocr
            import numpy as np
            from PIL import Image
            img = Image.open(io.BytesIO(contents)).convert("RGB")
            reader = easyocr.Reader(["en"], gpu=False, verbose=False)
            results = reader.readtext(np.array(img), detail=0)
            text = "\n".join(results)
        elif ext == "pdf":
            import io
            import pdfplumber
            with pdfplumber.open(io.BytesIO(contents)) as pdf:
                pages = [page.extract_text() or "" for page in pdf.pages]
                text = "\n\n".join(p for p in pages if p.strip())
        elif ext == "dcm":
            import io
            import pydicom
            ds = pydicom.dcmread(io.BytesIO(contents), stop_before_pixels=True)
            lines = []
            for tag in ds:
                if tag.keyword and tag.value:
                    val = str(tag.value)
                    if len(val) < 200:
                        lines.append(f"{tag.keyword}: {val}")
            text = "\n".join(lines)
        else:
            return {"text": "", "filename": file.filename, "error": f"Unsupported file type: {ext}"}
    except Exception:
        text = ""
    return {"text": text.strip(), "filename": file.filename}


@patientrouter.get("/file-proxy")
async def file_proxy(url: str):
    if ALLOWED_SPACE_HOST not in url:
        raise HTTPException(status_code=403, detail="URL not allowed.")

    ext = url.split("?")[0].split(".")[-1].lower()
    mime_map = {
        "zip": "application/zip",
        "rar": "application/x-rar-compressed",
        "dcm": "application/dicom",
        "pdf": "application/pdf",
        "jpg": "image/jpeg", "jpeg": "image/jpeg",
        "png": "image/png",
    }
    content_type = mime_map.get(ext, "application/octet-stream")
    filename = url.split("/")[-1].split("?")[0]

    async def stream():
        async with httpx.AsyncClient(timeout=120) as client:
            async with client.stream("GET", url) as resp:
                if resp.status_code != 200:
                    return
                async for chunk in resp.aiter_bytes(chunk_size=65536):
                    yield chunk

    return StreamingResponse(
        stream(),
        media_type=content_type,
        headers={"Content-Disposition": f'inline; filename="{filename}"'},
    )


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def parse_form_json(field_name: str, payload: str, schema_class):
    try:
        data = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid JSON payload for {field_name}",
        ) from exc

    try:
        return schema_class(**data)
    except ValidationError as exc:
        raise HTTPException(
            status_code=422,
            detail={
                "field": field_name,
                "errors": exc.errors(),
            },
        ) from exc

@patientrouter.get("/by-email")
def get_patient_by_email(email: str, db: Session = Depends(get_db)):
    patient = db.query(Demographic).filter(Demographic.email == email).first()
    if not patient:
        raise HTTPException(status_code=404, detail="No patient record found for this account")
    return {"id": patient.id, "full_name": patient.full_name}


@patientrouter.get("/get-all")
def get_all_patients( 
    db: Session = Depends(get_db) ): 
    patients = db.query(Demographic).order_by(Demographic.id.desc() ).all() 
    return { "success": True, "data": patients }


@patientrouter.get("/{patient_id}")
def get_complete_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Demographic).filter(Demographic.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    def to_dict(row):
        if row is None:
            return {}
        return {c.name: getattr(row, c.name) for c in row.__table__.columns}

    return {
        "demographic":         to_dict(patient),
        "medical_history":     to_dict(db.query(MedicalHistory).filter(MedicalHistory.patient_id == patient_id).first()),
        "vital_signs":         to_dict(db.query(VitalSigns).filter(VitalSigns.patient_id == patient_id).first()),
        "lab_results":         to_dict(db.query(LabResults).filter(LabResults.patient_id == patient_id).first()),
        "medications":         to_dict(db.query(Medications).filter(Medications.patient_id == patient_id).first()),
        "diagnosis_notes":     to_dict(db.query(DiagnosisNotes).filter(DiagnosisNotes.patient_id == patient_id).first()),
        "imaging_data":        to_dict(db.query(ImagingData).filter(ImagingData.patient_id == patient_id).first()),
        "lifestyle_data":      to_dict(db.query(LifestyleData).filter(LifestyleData.patient_id == patient_id).first()),
        "remote_monitoring":   to_dict(db.query(RemoteMonitoring).filter(RemoteMonitoring.patient_id == patient_id).first()),
        "hospital_operations": to_dict(db.query(HospitalOperations).filter(HospitalOperations.patient_id == patient_id).first()),
    }


@patientrouter.put("/{patient_id}")
def update_complete_patient(
    patient_id: int,
    demographic: str = Form(...),
    medical_history: str = Form(...),
    vital_signs: str = Form(...),
    lab_results: str = Form(...),
    medications: str = Form(...),
    diagnosis_notes: str = Form(...),
    lifestyle_data: str = Form(...),
    remote_monitoring: str = Form(...),
    hospital_operations: str = Form(...),
    xray: UploadFile | None = File(None),
    ctScan: UploadFile | None = File(None),
    mri: UploadFile | None = File(None),
    ultrasound: UploadFile | None = File(None),
    dicomImages: UploadFile | None = File(None),
    radiologyReports: UploadFile | None = File(None),
    voiceNote: UploadFile | None = File(None),
    extractedTexts: str = Form(""),
    db: Session = Depends(get_db),
):
    patient = db.query(Demographic).filter(Demographic.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    demographic_data      = parse_form_json("demographic",        demographic,        DemographicCreate)
    medical_history_data  = parse_form_json("medical_history",    medical_history,    MedicalHistorySchema)
    vital_signs_data      = parse_form_json("vital_signs",        vital_signs,        VitalSignsSchema)
    lab_results_data      = parse_form_json("lab_results",        lab_results,        LabResultsSchema)
    medications_data      = parse_form_json("medications",        medications,        MedicationsSchema)
    diagnosis_notes_data  = parse_form_json("diagnosis_notes",    diagnosis_notes,    DiagnosisNotesSchema)
    lifestyle_data_parsed = parse_form_json("lifestyle_data",     lifestyle_data,     LifestyleDataSchema)
    remote_monitoring_data   = parse_form_json("remote_monitoring",   remote_monitoring,   RemoteMonitoringSchema)
    hospital_operations_data = parse_form_json("hospital_operations", hospital_operations, HospitalOperationsSchema)

    def upsert(model, data_dict):
        record = db.query(model).filter(model.patient_id == patient_id).first()
        if record:
            for k, v in data_dict.items():
                setattr(record, k, v)
        else:
            db.add(model(patient_id=patient_id, **data_dict))

    def safe_upload_or_keep(file, existing_url, category):
        if file and hasattr(file, "filename") and file.filename:
            try:
                new_url = upload_patient_file(file, patient_id, category)
                if existing_url:
                    delete_patient_files([existing_url])
                return new_url
            except Exception as e:
                print(f"Upload error for {category}: {e}")
        return existing_url

    try:
        for k, v in demographic_data.dict().items():
            setattr(patient, k, v)

        upsert(MedicalHistory,     medical_history_data.dict())
        upsert(VitalSigns,         vital_signs_data.dict())
        upsert(LabResults,         lab_results_data.dict())
        upsert(Medications,        medications_data.dict())
        upsert(DiagnosisNotes,     diagnosis_notes_data.dict())
        upsert(LifestyleData,      lifestyle_data_parsed.dict())
        upsert(RemoteMonitoring,   remote_monitoring_data.dict())
        upsert(HospitalOperations, hospital_operations_data.dict())

        imaging = db.query(ImagingData).filter(ImagingData.patient_id == patient_id).first()
        if imaging:
            imaging.xray              = safe_upload_or_keep(xray,             imaging.xray,              "xray")
            imaging.ct_scan           = safe_upload_or_keep(ctScan,           imaging.ct_scan,           "ct-scan")
            imaging.mri               = safe_upload_or_keep(mri,              imaging.mri,               "mri")
            imaging.ultrasound        = safe_upload_or_keep(ultrasound,       imaging.ultrasound,        "ultrasound")
            imaging.dicom_images      = safe_upload_or_keep(dicomImages,      imaging.dicom_images,      "dicom-images")
            imaging.radiology_reports = safe_upload_or_keep(radiologyReports, imaging.radiology_reports, "radiology-reports")
            imaging.voice_url         = safe_upload_or_keep(voiceNote,        imaging.voice_url,         "voice")
            if extractedTexts:
                imaging.extracted_texts = extractedTexts
        else:
            db.add(ImagingData(
                patient_id=patient_id,
                xray=safe_upload_or_keep(xray, None, "xray"),
                ct_scan=safe_upload_or_keep(ctScan, None, "ct-scan"),
                mri=safe_upload_or_keep(mri, None, "mri"),
                ultrasound=safe_upload_or_keep(ultrasound, None, "ultrasound"),
                dicom_images=safe_upload_or_keep(dicomImages, None, "dicom-images"),
                radiology_reports=safe_upload_or_keep(radiologyReports, None, "radiology-reports"),
                voice_url=safe_upload_or_keep(voiceNote, None, "voice"),
                extracted_texts=extractedTexts or None,
            ))

        db.commit()
        db.refresh(patient)
    except HTTPException:
        db.rollback()
        raise
    except Exception as exc:
        db.rollback()
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to update patient record: {str(exc)}") from exc

    return {"message": "Patient record updated successfully", "patient_id": patient_id}


@patientrouter.post("/create-complete")
def create_complete_patient(
    demographic: str = Form(...),
    medical_history: str = Form(...),
    vital_signs: str = Form(...),
    lab_results: str = Form(...),
    medications: str = Form(...),
    diagnosis_notes: str = Form(...),
    lifestyle_data: str = Form(...),
    remote_monitoring: str = Form(...),
    hospital_operations: str = Form(...),
    xray: UploadFile | None = File(None),
    ctScan: UploadFile | None = File(None),
    mri: UploadFile | None = File(None),
    ultrasound: UploadFile | None = File(None),
    dicomImages: UploadFile | None = File(None),
    radiologyReports: UploadFile | None = File(None),
    voiceNote: UploadFile | None = File(None),
    extractedTexts: str = Form(""),
    db: Session = Depends(get_db),
):
    demographic_data = parse_form_json("demographic", demographic, DemographicCreate)
    medical_history_data = parse_form_json(
        "medical_history", medical_history, MedicalHistorySchema
    )
    vital_signs_data = parse_form_json("vital_signs", vital_signs, VitalSignsSchema)
    lab_results_data = parse_form_json("lab_results", lab_results, LabResultsSchema)
    medications_data = parse_form_json("medications", medications, MedicationsSchema)
    diagnosis_notes_data = parse_form_json(
        "diagnosis_notes", diagnosis_notes, DiagnosisNotesSchema
    )
    lifestyle_data_parsed = parse_form_json(
        "lifestyle_data", lifestyle_data, LifestyleDataSchema
    )
    remote_monitoring_data = parse_form_json(
        "remote_monitoring", remote_monitoring, RemoteMonitoringSchema
    )
    hospital_operations_data = parse_form_json(
        "hospital_operations", hospital_operations, HospitalOperationsSchema
    )

    try:
        patient = Demographic(
            full_name=demographic_data.full_name,
            dob=demographic_data.dob,
            age=demographic_data.age,
            gender=demographic_data.gender,
            blood_group=demographic_data.blood_group,
            height=demographic_data.height,
            weight=demographic_data.weight,
            bmi=demographic_data.bmi,
            phone=demographic_data.phone,
            email=demographic_data.email,
            address=demographic_data.address,
            emergency_contact=demographic_data.emergency_contact,
            insurance_details=demographic_data.insurance_details,
        )

        db.add(patient)
        db.flush()

        patient_id = patient.id

        # Safely handle file uploads - check if file exists and has content
        def safe_upload(file, patient_id, category):
            if file and hasattr(file, 'filename') and file.filename:
                try:
                    return upload_patient_file(file, patient_id, category)
                except Exception as e:
                    print(f"Upload error for {category}: {e}")
                    return None
            return None

        imaging_data = ImagingDataSchema(
            xray=safe_upload(xray, patient_id, "xray"),
            ct_scan=safe_upload(ctScan, patient_id, "ct-scan"),
            mri=safe_upload(mri, patient_id, "mri"),
            ultrasound=safe_upload(ultrasound, patient_id, "ultrasound"),
            dicom_images=safe_upload(dicomImages, patient_id, "dicom-images"),
            radiology_reports=safe_upload(radiologyReports, patient_id, "radiology-reports"),
            voice_url=safe_upload(voiceNote, patient_id, "voice"),
            extracted_texts=extractedTexts or None,
        )

        db.add(MedicalHistory(patient_id=patient_id, **medical_history_data.dict()))
        db.add(VitalSigns(patient_id=patient_id, **vital_signs_data.dict()))
        db.add(LabResults(patient_id=patient_id, **lab_results_data.dict()))
        db.add(Medications(patient_id=patient_id, **medications_data.dict()))
        db.add(DiagnosisNotes(patient_id=patient_id, **diagnosis_notes_data.dict()))
        db.add(LifestyleData(patient_id=patient_id, **lifestyle_data_parsed.dict()))
        db.add(
            RemoteMonitoring(
                patient_id=patient_id,
                **remote_monitoring_data.dict(),
            )
        )
        db.add(
            HospitalOperations(
                patient_id=patient_id,
                **hospital_operations_data.dict(),
            )
        )
        db.add(ImagingData(patient_id=patient_id, **imaging_data.dict()))

        db.commit()
        db.refresh(patient)
    except HTTPException:
        db.rollback()
        raise
    except Exception as exc:
        db.rollback()
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save complete patient record: {str(exc)}",
        ) from exc

    return {
        "message": "Complete patient record saved successfully",
        "patient_id": patient_id,
        "imaging_data": imaging_data.dict(),
    }


@patientrouter.delete("/{patient_id}")
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Demographic).filter(Demographic.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Collect imaging file URLs before deleting DB records
    imaging = db.query(ImagingData).filter(ImagingData.patient_id == patient_id).first()
    if imaging:
        delete_patient_files([
            imaging.xray,
            imaging.ct_scan,
            imaging.mri,
            imaging.ultrasound,
            imaging.dicom_images,
            imaging.radiology_reports,
            imaging.voice_url,
        ])

    for model in [
        NurseNote, DoctorAssessment,
        MedicalHistory, VitalSigns, LabResults, Medications,
        DiagnosisNotes, LifestyleData, RemoteMonitoring,
        HospitalOperations, ImagingData,
    ]:
        db.query(model).filter(model.patient_id == patient_id).delete()

    db.delete(patient)
    db.commit()
    return {"success": True, "message": "Patient deleted successfully"}
