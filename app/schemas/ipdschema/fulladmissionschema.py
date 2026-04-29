from pydantic import BaseModel, root_validator
from typing import Optional, Any
from .admissionschema import IPDAdmissionBase
from .bedallocationschema import BedAllocationBase
from .admissiontransferschema import AdmissionTransferBase
from .pmjaydetailsschema import PmjayDetailsCreate
from .cghsdetailsschema import CghsDetailsCreate
from .esicdetailsschema import EsicDetailsCreate
from .abdmdetailsschema import AbdmDetailsCreate
from .referraldetailsschema import ReferralDetailsCreate


class InsurancePayload(BaseModel):
    active_scheme: Optional[str] = None
    pmjay: Optional[PmjayDetailsCreate] = None
    cghs: Optional[CghsDetailsCreate] = None
    esic: Optional[EsicDetailsCreate] = None
    abdm: Optional[AbdmDetailsCreate] = None
    referral: Optional[ReferralDetailsCreate] = None

    @root_validator(pre=True)
    def validate_active_scheme(cls, values):
        active_scheme = values.get("active_scheme")
        if not active_scheme:
            return values

        # Check that active scheme data is present
        scheme_data = values.get(active_scheme)
        if scheme_data is None:
            raise ValueError(f"Data for active scheme '{active_scheme}' is missing")

        # Ensure other schemes are not filled
        schemes = ["pmjay", "cghs", "esic", "abdm", "referral"]
        for scheme in schemes:
            if scheme != active_scheme and values.get(scheme) is not None:
                raise ValueError(f"Multiple schemes are filled but active_scheme is '{active_scheme}'")

        return values


class IPDFullAdmissionCreate(BaseModel):
    """
    Accepts the payload exactly as the frontend sends it:
      { basic: { patient_id, ... }, pmjay: {}, cghs: {}, ... }
    patient_id lives inside basic; we don't require it at the top level.
    """
    basic: IPDAdmissionBase
    pmjay: Optional[PmjayDetailsCreate] = None
    cghs: Optional[CghsDetailsCreate] = None
    esic: Optional[EsicDetailsCreate] = None
    abdm: Optional[AbdmDetailsCreate] = None
    referral: Optional[ReferralDetailsCreate] = None


class InsuranceResponse(BaseModel):
    active_scheme: Optional[str] = None
    details: Any = None


class IPDFullAdmissionResponse(BaseModel):
    message: str
    admission_id: int
    bed: Any = None
    transfer: Any = None
    insurance: Optional[InsuranceResponse] = None
