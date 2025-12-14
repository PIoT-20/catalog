

import cherrypy

from src.models.sensor_model import SensorModel

@cherrypy.expose
@cherrypy.tools.json_out()
@cherrypy.tools.json_in()
class SensorApi(object):
    
    def GET(self):
        cherrypy.response.status = 200
        return SensorModel.getSensors()
    
    def POST(self):
        data = cherrypy.request.json
        sensor: SensorModel = SensorModel.from_dict(data)
        
        try:
            newSensor = sensor.createSensor()
            cherrypy.response.status = 201
            return newSensor
        except:
            cherrypy.response.status = 422
            return {"error": "Cannot create sensor"}
    def PUT(self):
        data = cherrypy.request.json
        
        sensor: SensorModel = SensorModel.from_dict(data)
        try:
            cherrypy.response.status = 200
            return sensor.updateSensor()
        except:
            cherrypy.response.status = 422
            return {"error": "Cannot update sensor"}
        
    def DELETE(self, id: str):
        if SensorModel.deleteSensor(id):
            cherrypy.response.status = 204
            return 
        else:
            cherrypy.response.status = 422
            return {"error": "Cannot delete sensor"}
