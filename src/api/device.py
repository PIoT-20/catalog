import json

import cherrypy
from bson import json_util

from src.models.device_model import DeviceModel


@cherrypy.expose()
@cherrypy.tools.json_out()
class DeviceApi(object):
    def GET(self, **params):
        cherrypy.response.status = 200
        client_id = params.get("client_id")
        device_id = params.get("device_id")

        if client_id is not None and device_id is not None:
            return json.loads(
                json_util.dumps(
                    DeviceModel.get_devices_by_client_and_device_id(
                        client_id, device_id
                    )
                )
            )
        elif client_id is not None and device_id is None:
            print("hit here")
            return json.loads(
                json_util.dumps(DeviceModel.get_devices_by_client_id(client_id))
            )
        elif client_id is None and device_id is not None:
            device = DeviceModel.get_devices_by_device_id(device_id)
            if not device:
                cherrypy.response.status = 404
                return json.dumps({"error": f"Device with id {device_id} not found"})
            else:
                return json.loads(json_util.dumps(device))
        else:
            return json.loads(json_util.dumps(DeviceModel.get_devices()))

    def POST(self):
        try:
            data = cherrypy.request.body.read()
            device_dict = json_util.loads(data)
            device: DeviceModel = DeviceModel.from_dict(device_dict)

        except TypeError or ValueError or KeyError as e:
            cherrypy.response.status = 422
            return json.dumps({"error": str(e)})

        new_device = device.create_device()
        cherrypy.response.status = 201
        return json.loads(json_util.dumps(new_device))

    def PUT(self):
        try:
            data = cherrypy.request.body.read()
            device_dict = json_util.loads(data)
            device: DeviceModel = DeviceModel.from_dict(device_dict)
        except TypeError or ValueError or KeyError as e:
            cherrypy.response.status = 422
            return json.dumps({"error": str(e)})

        updated_device = device.update_device()
        if updated_device is not None:
            cherrypy.response.status = 200
            return json.loads(json_util.dumps(updated_device))
        else:
            cherrypy.response.status = 400
            return {"error": "device Id not found"}

    def DELETE(self, device_id: str):
        if DeviceModel.delete_device(device_id):
            cherrypy.response.status = 204
            return None
        else:
            cherrypy.response.status = 422
            return {"error": "Cannot delete device"}

    def OPTIONS(self, *args, **kwargs):
        cherrypy.response.status = 200
        return ""
