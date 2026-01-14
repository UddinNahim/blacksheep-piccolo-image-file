from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field, RootModel, computed_field


class CertificateStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"


class BaseCertificateSchema(BaseModel):
    name: str = Field(..., max_length=100)
    course_details: str = Field(..., max_length=250)
    registration_number: str = Field(..., max_length=50)
    batch: str = Field(..., max_length=20)
    completion_date: datetime | None = None
    status: CertificateStatus = CertificateStatus.PENDING
    image: str | None = None


class CertificateCreateSchema(BaseCertificateSchema):
    pass


class CertificateResponseSchema(BaseCertificateSchema):
    id: UUID
    certificate_id: str
    issue_date: datetime
    created_at: datetime
    updated_at: datetime


class CertificateVerifyResponseSchema(BaseCertificateSchema):
    certificate_id: str | None
    issue_date: datetime | None = None


class CertificateUpdateSchema(BaseModel):
    name: str | None = None
    course_details: str | None = None
    registration_number: str | None = None
    batch: str | None = None
    completion_date: datetime | None = None
    status: CertificateStatus | None = None
    image: str | None = None


class CertificateListResponseSchema(RootModel):
    root: list[CertificateResponseSchema]

    @computed_field
    @property
    def total_count(self) -> int:
        return len(self.root)
