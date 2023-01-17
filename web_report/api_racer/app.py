from flasgger import Swagger
from flask import Flask
from flask_restful import Api

from .api_views import DetailDriverApi, ReportApi, ReportApiAsc

app = Flask(__name__)
api = Api(app)
Swagger(app)
api.add_resource(ReportApi, '/api/v1/report/')
api.add_resource(ReportApiAsc, '/api/v1/drivers/')
api.add_resource(DetailDriverApi, '/api/v1/drivers/driver_id=<code>')
