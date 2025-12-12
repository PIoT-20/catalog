import cherrypy


@cherrypy.expose
class ServiceApi(object):
    def GET(self):
        return "Hello World!"
    def POST(self):
        return "Hello World!"
    def PUT(self):
        return "Hello World!"
    def DELETE(self):
        return "Hello World!"
