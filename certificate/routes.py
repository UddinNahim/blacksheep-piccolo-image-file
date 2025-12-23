from blacksheep import  FromForm, Request, not_found, route,get ,json ,post ,FromJSON , delete ,status_code
import app 
from certificate.tables import Certificate
from  certificate.schema import CertificateCreate,CertificateVerifyResponse
import uuid ,os


JPG_FOLDER = "certificate/jpg"

@post("/certificate_entry")
async def certificate_entry(request: Request, data: FromForm[CertificateCreate]):
    cert_data = data.value # Pydantic validated form fields

    # 1. Handle the File
    files = await request.files()
    if not files:
        return json({"error": "Missing .jpg file"}, status=400)
    
    image_file = files[0]
    
    # Secure filename generation
    filename = f"{uuid.uuid4().hex}.jpg"
    file_path = os.path.join(JPG_FOLDER, filename)

    # 2. Check existence BEFORE saving the file (Efficiency)
    exists = await Certificate.exists().where(
        Certificate.reg_num == cert_data.reg_num
    )
    if exists:
        return json({"error": f"Certificate {cert_data.reg_num} already exists"}, status=400)

    # 3. Save the file to the jpg folder
    with open(file_path, mode="wb") as f:
        f.write(image_file.data)

    # 4. Save to Database
    try:
        new_cert = Certificate(
            name=cert_data.name,
            reg_num=cert_data.reg_num,
            batch=cert_data.batch,
            image=filename, # Use the new filename we just created
            status=cert_data.status
        )
        await new_cert.save()
        
        return json({
            "success": True, 
            "message": "Certificate created successfully",
            "image_url": f"/jpg/{filename}"
        }, status=201)
        
    except Exception as e:
        # Cleanup: Delete the file if the database save fails
        if os.path.exists(file_path):
            os.remove(file_path)
        return json({"error": f"Database error: {str(e)}"}, status=500)
    


@get("/verify/{reg_num}")
async def verify_certificate(reg_num: str):
    cert = await Certificate.objects().get(
        Certificate.reg_num == reg_num
    )
    
    if not cert:
        return json({"valid": False, "message": "Certificate not found"}, status=404)
        
    return json({
        "valid": cert.status,
        "recipient": cert.name,
        "issued_on": cert.issue_date.isoformat(),
        "image_url": cert.image
    })

@get("/certificate/all")
async def certificate_all():
    all_cert = await Certificate.select().run()
    return json(all_cert)

@delete("/certificate-delete/{id}")
async def certificate_delete(id: int):
    # 1. Fetch the certificate first to find the image filename
    cert = await Certificate.objects().get(Certificate.id == id)

    if not cert:
        return json({"error": "Certificate not found"}, status=404)

    # 2. Delete the physical file from the jpg folder
    if cert.image:
        file_path = os.path.join("jpg", cert.image)
        if os.path.exists(file_path):
            os.remove(file_path)

    # 3. Delete the record from the database
    # In Piccolo, .remove() is the easiest way to delete a fetched object
    await cert.remove()

    return json({
        "success": True, 
        "message": f"Certificate {id} and its image were deleted"
    })
from certificate.schema import CertificateCreate,CertificateRead
    
@post("/certificates2")
async def create_cert(data:CertificateCreate):
    existing = await Certificate.objects().get(
        (Certificate.registration_number == data.registration_number) &
        (Certificate.batch == data.batch)
    )
    if existing:
        return {"error":"certificate already exists"}

    new_cert = await Certificate.create_with_safe_id(**data.model_dump())
    return new_cert.to_dict()

@get("/certificates2")
async def get_all_certificate():
    return await Certificate.select()





@get("/certificates2/{certificate_id}")
async def verification_certificate(certificate_id: str) :
    # Use .objects() to get a Piccolo object
    verify = await Certificate.objects().where(
        Certificate.certificate_id == certificate_id
    ).first()

    if not verify:
        # Note: In BlackSheep controllers, use self.not_found() 
        # or raise the exception directly
        return not_found({"error": "Certificate not found or invalid."})
    
    response_data  = CertificateVerifyResponse.model_validate(verify)
    return response_data.model_dump()