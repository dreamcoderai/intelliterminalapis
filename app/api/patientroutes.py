# app/api/patient/patientroutes.py

import json

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.storage import upload_patient_file
from app.models.patientmodel.demographicmodel import Demographic
from app.models.patientmodel.diagnosisnotesmodel import DiagnosisNotes
from app.models.patientmodel.hospitaloperationsmodel import HospitalOperations
from app.models.patientmodel.imagingdatamodel import ImagingData
from app.models.patientmodel.labresultsmodel import LabResults
from app.models.patientmodel.lifestyledatamodel import LifestyleData
from app.models.patientmodel.medicalhistorymodel import MedicalHistory
from app.models.patientmodel.medicationsmodel import Medications
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
            contact_details=demographic_data.contact_details,
            emergency_contact=demographic_data.emergency_contact,
            insurance_details=demographic_data.insurance_details,
        )

        db.add(patient)
        db.flush()

        patient_id = patient.id

        imaging_data = ImagingDataSchema(
            xray=upload_patient_file(xray, patient_id, "xray") if xray else None,
            ct_scan=upload_patient_file(ctScan, patient_id, "ct-scan") if ctScan else None,
            mri=upload_patient_file(mri, patient_id, "mri") if mri else None,
            ultrasound=upload_patient_file(ultrasound, patient_id, "ultrasound")
            if ultrasound
            else None,
            dicom_images=upload_patient_file(
                dicomImages, patient_id, "dicom-images"
            )
            if dicomImages
            else None,
            radiology_reports=upload_patient_file(
                radiologyReports, patient_id, "radiology-reports"
            )
            if radiologyReports
            else None,
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
        raise HTTPException(
            status_code=500,
            detail="Failed to save complete patient record",
        ) from exc

    return {
        "message": "Complete patient record saved successfully",
        "patient_id": patient_id,
        "imaging_data": imaging_data.dict(),
    }
