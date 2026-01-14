from blacksheep import FromJSON, Request, Response, auth, ok, created, no_content, not_found
from src.common.constants import MAX_LIMIT
from src.common.response import ErrorResponse, PaginatedResponse
from certificate.schema import (
    CertificateCreateSchema,
    CertificateListResponseSchema,
    CertificateResponseSchema,
    CertificateUpdateSchema,
)
from certificate.tables import Certificate

# Helper for consistent 404 formatting
def certificate_not_found(certificate_id: str):
    return not_found(ErrorResponse(
        code=404,
        message="certificate_id not found",
        error_code="not_found",
        details={"certificate_id": certificate_id},
    ))


async def create_certificate(data: FromJSON[CertificateCreateSchema]) -> Response:
    new_cert = await Certificate.create_with_safe_id(**data.value.model_dump())
    # BlackSheep automatically handles Pydantic models if you use created()
    return created(CertificateResponseSchema(**new_cert.to_dict()))


async def get_certificates(
    certificate_id: str | None = None, 
    limit: int = 15, 
    offset: int = 0
) -> Response:
    if certificate_id:
        certificate = await Certificate.objects().where(
            Certificate.certificate_id == certificate_id,
            Certificate.is_active.eq(True),
        ).first()

        if not certificate:
            return certificate_not_found(certificate_id)

        return ok(CertificateResponseSchema(**certificate.to_dict()))

    # Pagination logic
    total_items = await Certificate.count().where(Certificate.is_active.eq(True))
    certificates = (
        await Certificate.objects()
        .where(Certificate.is_active.eq(True))
        .offset(offset * limit)
        .order_by(Certificate.created_at, ascending=False)
        .limit(min(limit, MAX_LIMIT))
    )
    
    response = PaginatedResponse(
        limit=limit,
        offset=offset,
        total_items=total_items,
        data=CertificateListResponseSchema(
            root=[CertificateResponseSchema(**cert.to_dict()) for cert in certificates]
        ),
    )
    return ok(response)


@auth("authenticated")
@require_certificate_write()
async def delete_certificate(certificate_id: str) -> Response:
    # Check existence before "soft delete"
    exists = await Certificate.objects().where(
        Certificate.certificate_id == certificate_id,
        Certificate.is_active.eq(True),
    ).exists()

    if not exists:
        return certificate_not_found(certificate_id)

    await Certificate.update(is_active=False).where(
        Certificate.certificate_id == certificate_id
    ).run()

    return no_content()


@auth("authenticated")
@require_certificate_write()
async def update_certificate(
    certificate_id: str,
    data: FromJSON[CertificateUpdateSchema],
) -> Response:
    exist = await Certificate.objects().where(
        Certificate.certificate_id == certificate_id,
        Certificate.is_active.eq(True),
    ).first()

    if not exist:
        return certificate_not_found(certificate_id)

    await (
        Certificate.update(**data.value.model_dump(exclude_unset=True))
        .where(Certificate.certificate_id == certificate_id)
        .run()
    )
    
    await exist.refresh()
    return ok(CertificateResponseSchema(**exist.to_dict()))