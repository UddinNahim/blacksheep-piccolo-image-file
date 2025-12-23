from __future__  import annotations

from enum import StrEnum
from datetime import datetime, timezone
import secrets

from piccolo.table import Table
from piccolo.columns import Varchar, UUID, Timestamptz
from piccolo.columns.defaults.uuid import UUID4
from piccolo.columns.defaults.timestamptz import TimestamptzNow
from asyncpg.exceptions import UniqueViolationError


CERT_PREFIX = "FAAC"


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def generate_certificate_id(prefix: str = CERT_PREFIX) -> str:
    """
    No DB dependency:
    FAAC-YYYYMMDDHHMMSSffffff-XYZ
    - timestamp includes microseconds (ffffff)
    - XYZ is random 000-999
    """
    ts = utcnow().strftime("%Y%m%d%H%M%S%f")  # year month day hour minute second microsecond
    rand3 = f"{secrets.randbelow(1000):03d}"
    return f"{prefix}-{ts}-{rand3}"


class CertificateStatus(StrEnum):
    PENDING = "pending"
    COMPLETED = "completed"


class Certificate(Table):
    id = UUID(primary_key=True, default=UUID4())

    # App-generated ID (no sequences/triggers)
    certificate_id = Varchar(length=64, unique=True, default=generate_certificate_id)

    name = Varchar(length=100)
    course_details = Varchar(length=250)
    registration_number = Varchar(length=50)
    batch = Varchar(length=20)

    completion_date = Timestamptz(null=True)
    issue_date = Timestamptz(default=TimestamptzNow())

    status = Varchar(length=20, choices=CertificateStatus, default=CertificateStatus.PENDING)
    image = Varchar(length=255, null=True)

    created_at = Timestamptz(default=TimestamptzNow())
    updated_at = Timestamptz(auto_update=utcnow)

    @classmethod
    async def create_with_safe_id(cls, **data) -> "Certificate":
        """
        Optional helper:
        retries if a rare collision happens (unique constraint).
        """
        for _ in range(5):
            obj = cls(**data)
            # certificate_id default will be applied automatically, but setting explicitly is ok:
            obj.certificate_id = generate_certificate_id()
            try:
                await obj.save()
                return obj
            except UniqueViolationError:
                continue
        raise RuntimeError("Could not generate a unique certificate_id after several retries.")