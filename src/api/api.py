import cherrypy

from .device import DeviceApi
from .service import ServiceApi
from .user import UserApi
import json

conf = {
    '/': {

        'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
        'tools.sessions.on': False,
        'tools.response_headers.on': True,
        'tools.response_headers.headers': [('Content-Type', 'text/plain'),('Accept', 'application/json'), ('Content-Type', 'application/json')],
    }
}



@cherrypy.expose
class Api():
    def __init__(self):
        self.device = DeviceApi()
        self.user = UserApi()
        self.service = ServiceApi()
    def GET(self):
        return "GET REQUEST"
    def POST(self):
        return "POST REQUEST"
    def PUT(self):
        return "PUT REQUEST"
    def DELETE(self):
        return "DELETE REQUEST"

    def startApi(self):
        cherrypy.config.update({
            "server.socket_host": "0.0.0.0",
            "server.socket_port": 8080,
        })

        cherrypy.tree.mount(self.device, '/device', conf)
        cherrypy.tree.mount(self.user, '/user', conf)
        cherrypy.tree.mount(self.service, '/service', conf)
        cherrypy.quickstart(self, '/', conf)
