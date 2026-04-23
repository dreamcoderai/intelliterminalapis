# app/api/patient/patientroutes.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import SessionLocal

from app.models.patientmodel.demographicmodel import Demographic
from app.models.patientmodel.medicalhistorymodel import MedicalHistory
from app.models.patientmodel.vitalsignsmodel import VitalSigns
from app.models.patientmodel.labresultsmodel import LabResults
from app.models.patientmodel.medicationsmodel import Medications
from app.models.patientmodel.diagnosisnotesmodel import DiagnosisNotes
from app.models.patientmodel.lifestyledatamodel import LifestyleData
from app.models.patientmodel.remotemonitoringmodel import RemoteMonitoring
from app.models.patientmodel.hospitaloperationsmodel import HospitalOperations

from app.schemas.patientschema.demographicschema import DemographicCreate
from app.schemas.patientschema.medicalhistoryschema import MedicalHistorySchema
from app.schemas.patientschema.vitalsignschema import VitalSignsSchema
from app.schemas.patientschema.labresultschema import LabResultsSchema
from app.schemas.patientschema.medicationschema import MedicationsSchema
from app.schemas.patientschema.diagnosisnotesschema import DiagnosisNotesSchema
from app.schemas.patientschema.lifestyledataschema import LifestyleDataSchema
from app.schemas.patientschema.remotemonitoringschema import RemoteMonitoringSchema
from app.schemas.patientschema.hospitaloperationsschema import HospitalOperationsSchema

patientrouter = APIRouter(prefix="/patients", tags=["Patients"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@patientrouter.post("/create-complete")
def create_complete_patient(
    demographic: DemographicCreate,
    medical_history: MedicalHistorySchema,
    vital_signs: VitalSignsSchema,
    lab_results: LabResultsSchema,
    medications: MedicationsSchema,
    diagnosis_notes: DiagnosisNotesSchema,
    lifestyle_data: LifestyleDataSchema,
    remote_monitoring: RemoteMonitoringSchema,
    hospital_operations: HospitalOperationsSchema,
    db: Session = Depends(get_db),
):
    # 1. Demographic
    patient = Demographic(
        full_name=demographic.full_name,
        dob=demographic.dob,
        age=demographic.age,
        gender=demographic.gender,
        blood_group=demographic.blood_group,
        height=demographic.height,
        weight=demographic.weight,
        bmi=demographic.bmi,
        contact_details=demographic.contact_details,
        emergency_contact=demographic.emergency_contact,
        insurance_details=demographic.insurance_details,
    )

    db.add(patient)
    db.commit()
    db.refresh(patient)

    patient_id = patient.id

    # 2 to 10 linked records
    db.add(MedicalHistory(patient_id=patient_id, **medical_history.dict()))
    db.add(VitalSigns(patient_id=patient_id, **vital_signs.dict()))
    db.add(LabResults(patient_id=patient_id, **lab_results.dict()))
    db.add(Medications(patient_id=patient_id, **medications.dict()))
    db.add(DiagnosisNotes(patient_id=patient_id, **diagnosis_notes.dict()))
    db.add(LifestyleData(patient_id=patient_id, **lifestyle_data.dict()))
    db.add(RemoteMonitoring(patient_id=patient_id, **remote_monitoring.dict()))
    db.add(HospitalOperations(patient_id=patient_id, **hospital_operations.dict()))

    db.commit()

    return {
        "message": "Complete patient record saved successfully",
        "patient_id": patient_id,
    }



