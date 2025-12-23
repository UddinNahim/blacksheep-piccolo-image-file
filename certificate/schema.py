from pydantic import BaseModel,Field
from typing import Optional

class CertificateCreate(BaseModel):
    name: str
    reg_num: str
    batch: int
    image: Optional[str] = None
    status: bool = True


class CertificateCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    reg_num: str = Field(..., min_length=5)
    batch: int = Field(..., gt=2000) # Must be greater than 2000
    status: bool = True

from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional
from enum import Enum

# Mirror the Enum for Pydantic validation
class CertificateStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"

# --- BASE SCHEMA ---
class CertificateBase(BaseModel):
    name: str = Field(..., max_length=100)
    course_details: str = Field(..., max_length=250)
    registration_number: str = Field(..., max_length=50)
    batch: str = Field(..., max_length=20)
    status: str
    completion_date: Optional[datetime] = None

# --- POST SCHEMA (Input) ---
# Used when creating a certificate. Notice we DON'T ask for 'id' 
# or 'certificate_id' because the server generates those.
class CertificateCreate(CertificateBase):
    pass

# --- GET SCHEMA (Output) ---
# Used when sending data back to the user. Includes all DB fields.
class CertificateRead(CertificateBase):
    id: str 
    certificate_id: str
    status: CertificateStatus
    issue_date: datetime
    created_at: datetime
    updated_at: datetime
    image: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class CertificateVerifyResponse(BaseModel):
    name: str
    course_details:str
    registration_number:str
    batch:str
    issue_date: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)