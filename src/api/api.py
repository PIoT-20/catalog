import json

import cherrypy

from .device import DeviceApi
from .service import ServiceApi
from .user import UserApi



def cors():
    cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
    cherrypy.response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    cherrypy.response.headers["Access-Control-Allow-Headers"] = "*"

cherrypy.tools.cors = cherrypy.Tool('before_handler', cors)

conf = {
    '/': {
        'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
        'tools.sessions.on': False,
        'tools.response_headers.on': True,
        'tools.cors.on': True,
        'tools.response_headers.headers': [('Content-Type', 'text/plain'),('Accept', '*/*'), ('Content-Type', 'application/json')],

    }
}

@cherrypy.expose
class Api:
    def __init__(self):
        self.device = DeviceApi()
        self.user = UserApi()
        self.service = ServiceApi()


    @cherrypy.tools.json_out()
    def GET(self):
        return {"status": "ok"}

    def startApi(self):
        cherrypy.config.update({
            "server.socket_host": "0.0.0.0",
            "server.socket_port": 8080,
        })

        cherrypy.tree.mount(self.device, '/device', conf)
        cherrypy.tree.mount(self.user, '/user', conf)
        cherrypy.tree.mount(self.service, '/service', conf)
        cherrypy.tree.mount(self, '/', conf)
        cherrypy.engine.start()
        cherrypy.engine.block()
