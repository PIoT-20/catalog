import json
from datetime import datetime

import cherrypy
from bson import json_util

from models.service_model import ServiceModel


@cherrypy.expose
@cherrypy.tools.json_out()
class ServiceApi(object):
    def GET(self, service_type=None):
        cherrypy.response.status = 200
        try:
            if service_type:
                services = ServiceModel.get_service_by_type(service_type)
                if services:
                    return json.loads(json_util.dumps(services[0]))
                else:
                    cherrypy.response.status = 404
                    return json.dumps({"error": "service type not found"})
            else:
                return json.loads(json_util.dumps(ServiceModel.get_services()))
        except Exception as e:
            print(f"Error getting services: {e}")
            cherrypy.response.status = 500
            return json.dumps({"error": "Internal Server Error"})

    def POST(self):
        try:
            data = cherrypy.request.body.read()
            service_dict = json_util.loads(data)
            service_dict["last_updated"] = datetime.now().timestamp()
            sensor: ServiceModel = ServiceModel.from_dict(service_dict)
        except TypeError or ValueError or KeyError as e:
            cherrypy.response.status = 422
            return json.dumps({"error": str(e)})

        existing_services = ServiceModel.get_service_by_type(sensor.service_type)
        if existing_services:
            sensor._id = existing_services[0]["_id"]
            updated_service = sensor.update_service()
            cherrypy.response.status = 200
            return json.loads(json_util.dumps(updated_service))

        new_service = sensor.create_service()
        cherrypy.response.status = 201
        return json.loads(json_util.dumps(new_service))

    def PUT(self):
        try:
            data = cherrypy.request.body.read()
            service_dict = json_util.loads(data)
            service_dict["last_updated"] = datetime.now().timestamp()
            sensor: ServiceModel = ServiceModel.from_dict(service_dict)
        except TypeError or ValueError or KeyError as e:
            cherrypy.response.status = 422
            return json.dumps({"error": str(e)})

        updated_service = sensor.update_service()
        if updated_service is not None:
            cherrypy.response.status = 201
            return json.loads(json_util.dumps(updated_service))
        else:
            cherrypy.response.status = 400
            return json.dumps({"error": "sensor Id not found"})

    def DELETE(self, sensor_id: str):
        if ServiceModel.delete_service(sensor_id):
            cherrypy.response.status = 204
            return None
        else:
            cherrypy.response.status = 400
            return json_util.dumps({"error": "sensor Id not found"})
