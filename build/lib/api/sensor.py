from json.decoder import JSONDecoder

import cherrypy

from src.models.sensor_model import SensorModel


@cherrypy.expose
@cherrypy.tools.json_out()
@cherrypy.tools.json_in()
class SensorApi(object):
    def GET(self):
        return "Hello World!"
    @cherrypy.tools.json_in()
    def POST(self):
        data = cherrypy.request.json
        sensor: SensorModel = JSONDecoder().decode(data)
        sensor.createSensor()
        return "sensor created"
    def PUT(self):
        return "Hello World!"
    def DELETE(self):
        return "Hello World!"
