from blacksheep import Request, FromFiles, post
from blacksheep.server.responses import created, bad_request, json
from pydantic import ValidationError

# Assuming these are your local project imports
from certificate.r2_client import upload_certificate_image
from certificate.schema import CertificateCreate, CertificateRead 
from certificate.tables import Certificate, generate_certificate_id 

@post("/create-certificate")
async def create_certificate(request: Request, files: FromFiles):
    """
    Creates a certificate by validating form data and uploading an image.
    """
    # 1. Extract and Validate Form Data
    # Since you are sending images, the data is coming in as multipart/form-data
    form_data = await request.form()
    
    try:
        # Convert the MultiDict to a regular dict for Pydantic
        # Note: form_data.items() handles the conversion properly
        payload = CertificateCreate(**{k: v for k, v in form_data.items()})
    except ValidationError as e:
        # 'unprocessable_entity' doesn't exist in BlackSheep, use json(..., status=422)
        return json(e.errors(), status=422)

    # 2. Handle Image Upload
    image_key = None
    
    # files.value is a list of FormFile objects
    if files.value and len(files.value) > 0:
        image = files.value[0]
        content = await image.read()
        
        # Validate format and size (5MB limit)
        allowed_types = ("image/jpeg", "image/png", "image/jpg")
        if image.content_type not in allowed_types:
            return bad_request("Invalid format. Only JPG/PNG allowed.")
            
        if len(content) > 5 * 1024 * 1024:
            return bad_request("File too large. Max 5MB.")
        
        # Upload to R2 and get the key/path
        image_key = upload_certificate_image(content, image.content_type)

    # 3. Save to Database
    # Using await as per your generate_certificate_id call
    cert_id = await generate_certificate_id()
    
    cert = Certificate(
        certificate_id=cert_id,
        image_key=image_key,
        **payload.model_dump()
    )
    
    await cert.save()

    # 4. Return success response (201 Created)
    # We create the read schema and dump it to a dict for the response
    response_data = CertificateRead(
        **cert.to_dict(), 
        image_url=image_key
    ).model_dump()

    return created(response_data)