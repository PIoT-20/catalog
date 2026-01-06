import json

import cherrypy
from bson import json_util

from models.user_model import UserModel


@cherrypy.expose()
@cherrypy.tools.json_out()
class UserApi(object):
    def GET(self):
        cherrypy.response.status = 200
        return json_util.dumps(UserModel.get_users())

    def POST(self):
        try:
            data = cherrypy.request.body.read()
            sensor_dict = json_util.loads(data)
            sensor: UserModel = UserModel.from_dict(sensor_dict)
        except TypeError or ValueError or KeyError as e:
            cherrypy.response.status = 422
            return json.dumps({"error": str(e)})

        new_user = sensor.create_user()
        cherrypy.response.status = 201
        return json_util.dumps(new_user)

    def PUT(self):
        try:
            data = cherrypy.request.body.read()
            sensor_dict = json_util.loads(data)
            sensor: UserModel = UserModel.from_dict(sensor_dict)
        except TypeError or ValueError or KeyError as e:
            cherrypy.response.status = 422
            return json.dumps({"error": str(e)})

        updated_user = sensor.update_user()
        if updated_user is not None:
            cherrypy.response.status = 201
            return json_util.dumps(updated_user)
        else:
            cherrypy.response.status = 400
            return json.dumps({"error": "sensor Id not found"})

    def DELETE(self, user_id: str):

        if UserModel.delete_user(user_id):
            cherrypy.response.status = 204
            return None
        else:
            cherrypy.response.status = 400
            return json_util.dumps({"error": "sensor Id not found"})
