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