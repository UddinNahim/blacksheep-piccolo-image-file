import datetime
from piccolo.table import Table
from piccolo.columns import Varchar, Boolean, Timestamptz, Text ,Integer

class Certificate(Table):
    """
    Represents a digital certificate issued to a student or participant.
    """
    # The full name of the recipient
    name = Varchar(length=100)
    
    # A unique identifier for the certificate (useful for verification)
    reg_num = Varchar(length=50, unique=True, index=True)
    batch = Integer()
    
    # The date the certificate was officially issued
    # We use a callable (datetime.now) so it generates when the record is created
    issue_date = Timestamptz(default=datetime.datetime.now)
    
    # Stores the file path or URL to the certificate image/PDF
    image = Varchar(length=255, null=True)
    
    # Status: True for Active/Valid, False for Revoked/Invalid
    status = Boolean(default=True)

    # Optional: Add a description or metadata
    details = Text(null=True)