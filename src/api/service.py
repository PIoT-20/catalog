import json
import cherrypy
from bson import json_util
from models.service_model import ServiceModel


@cherrypy.expose
@cherrypy.tools.json_out()
class ServiceApi(object):
    def GET(self):
        cherrypy.response.status = 200
        return json.loads(json_util.dumps(ServiceModel.get_services()))

    def POST(self):
        try:
            data = cherrypy.request.body.read()
            sensor_dict = json_util.loads(data)
            sensor: ServiceModel = ServiceModel.from_dict(sensor_dict)
        except TypeError or ValueError or KeyError as e:
            cherrypy.response.status = 422
            return json.dumps({"error": str(e)})

        new_service = sensor.create_service()
        cherrypy.response.status = 201
        return json.loads(json_util.dumps(new_service))

    def PUT(self):
        try:
            data = cherrypy.request.body.read()
            sensor_dict = json_util.loads(data)
            sensor: ServiceModel = ServiceModel.from_dict(sensor_dict)
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
