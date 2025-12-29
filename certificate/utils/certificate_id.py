# src/utils/certificate_id.py

from certificate.tables import Certificate


async def generate_certificate_id() -> str:
    PREFIX = "FAAC"

    # Get the latest certificate
    last_cert = (
        await Certificate
        .select(Certificate.certificate_id)
        .order_by(Certificate.id, ascending=False)
        .first()
        .run()
    )

    if not last_cert:
        return f"{PREFIX}001"

    last_id = last_cert["certificate_id"]
    number = int(last_id.replace(PREFIX, ""))
    next_number = number + 1

    return f"{PREFIX}{next_number:03d}"
