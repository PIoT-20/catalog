import json

import cherrypy

from src.models.sensor_model import SensorModel
from bson import json_util

@cherrypy.expose()
@cherrypy.tools.json_out()
# @cherrypy.tools.json_in()
class SensorApi(object):

    def GET(self):
        cherrypy.response.status = 200
        return json_util.dumps(SensorModel.get_sensors())
    
    def POST(self):
        try:
            data = cherrypy.request.body.read()
            sensor_dict = json_util.loads(data)
            sensor: SensorModel = SensorModel.from_dict(sensor_dict)
        except TypeError or ValueError or KeyError as e:
            cherrypy.response.status = 422
            return json.dumps({"error": str(e)})

        new_sensor = sensor.create_sensor()
        cherrypy.response.status = 201
        return json_util.dumps(new_sensor)

    def PUT(self):
        try:
            data = cherrypy.request.body.read()
            sensor_dict = json_util.loads(data)
            sensor: SensorModel = SensorModel.from_dict(sensor_dict)
        except TypeError or ValueError or KeyError as e:
            cherrypy.response.status = 422
            return json.dumps({"error": str(e)})

        updated_sensor = sensor.update_sensor()
        if updated_sensor is not None:
            cherrypy.response.status = 201
            return json_util.dumps(updated_sensor)
        else:
            cherrypy.response.status = 400
            return json.dumps({"error": "sensor Id not found"})
        
    def DELETE(self, sensor_id: str):

        if SensorModel.delete_sensor(sensor_id):
            cherrypy.response.status = 204
            return None
        else:
            cherrypy.response.status = 400
            return json_util.dumps({"error": "sensor Id not found"})
