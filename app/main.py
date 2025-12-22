from blacksheep import Application
from app.routes import *
from certificate.routes import *

from blacksheep.server.openapi.v3 import OpenAPIHandler
from openapidocs.v3 import Info


app  = Application()



app.serve_files("jpg",root_path="certificate/jpg",discovery=True)

docs = OpenAPIHandler(info=Info(title="LMS Certificate System", version="1.0"))
docs.bind_app(app)
