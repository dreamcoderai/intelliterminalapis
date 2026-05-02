# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# -----------------------------------
# Database Imports
# -----------------------------------
from app.core.database import engine, Base

# -----------------------------------
# Import Models (VERY IMPORTANT)
# Without importing models,
# Base.metadata.create_all() will
# not create tables
# -----------------------------------
from app.models.usersmodel.usermodel import User
from app.models.patientmodel.doctorassessmentmodel import DoctorAssessment  # noqa: F401
from app.models.patientmodel.nursenotesmodel import NurseNote  # noqa: F401
from app.models.ipdmodel.admissionmodel import IPDAdmission  # noqa: F401
from app.models.ipdmodel.bedallocationmodel import BedAllocation  # noqa: F401
from app.models.ipdmodel.admissiontransfermodel import AdmissionTransfer  # noqa: F401
from app.models.ipdmodel.admissionschememodel import AdmissionScheme  # noqa: F401
from app.models.ipdmodel.pmjaydetailsmodel import PmjayDetails  # noqa: F401
from app.models.ipdmodel.cghsdetailsmodel import CghsDetails  # noqa: F401
from app.models.ipdmodel.esicdetailsmodel import EsicDetails  # noqa: F401
from app.models.ipdmodel.abdmdetailsmodel import AbdmDetails  # noqa: F401
from app.models.ipdmodel.referraldetailsmodel import ReferralDetails  # noqa: F401

# -----------------------------------
# Import Routers
# -----------------------------------
from app.api.routes import router as router
from app.api.userroutes import userrouter as userrouter
from app.api.dashboardroutes import dashboardrouter as dashboardrouter
from app.api.patientroutes import patientrouter as patientrouter
from app.api.assessmentroutes import assessmentrouter as assessmentrouter
from app.api.nursenotesroutes import nursenotesrouter as nursenotesrouter
from app.api.ipdroutes import router as ipdrouter


# -----------------------------------
# Create Database Tables Automatically
# -----------------------------------
Base.metadata.create_all(bind=engine)


# -----------------------------------
# FastAPI App Initialization
# -----------------------------------
app = FastAPI(
    title="PulseTerminal API",
    version="1.0.0",
    description="Enterprise Healthcare Intelligence Platform API"
)


# -----------------------------------
# CORS Middleware
# -----------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------------
# Include Routers
# -----------------------------------

# Authentication APIs
app.include_router(router)

# User Management APIs
app.include_router(userrouter)
app.include_router(dashboardrouter)
app.include_router(patientrouter)
app.include_router(assessmentrouter)
app.include_router(nursenotesrouter)
app.include_router(ipdrouter)


# -----------------------------------
# Root Health Check API
# -----------------------------------
@app.get("/")
def health_check():
    return {
        "message": "PulseTerminal API Running"
    }


# -----------------------------------
# Optional Debug Route
# -----------------------------------
@app.get("/health")
def health():
    return {
        "status": "healthy",
        "database": "connected",
        "service": "PulseTerminal Backend"
    }