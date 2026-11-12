# catalog

The catalog is the service registry and configuration store for the PIoT-20 system. It stores **users**, **devices** and **services** in MongoDB. Every other component uses it to find each other and to read device configuration.

It is a CherryPy REST API on port `8080`.

## Configuration

| Env var | Description |
|---|---|
| `MONGO_DB` | MongoDB connection URI (required). Data goes in the `catalog` database. |

## Running

```sh
pip install .
MONGO_DB="mongodb+srv://..." python -m src.api
```

With Docker:

```sh
docker build -t catalog .
docker run -p 8080:8080 -e MONGO_DB="..." catalog
```

In the full stack, start it with `docker compose up catalog` from the [devops](https://github.com/PIoT-20/devops) repo. It is exposed on host port `8085`.

## API

All responses are JSON. MongoDB ids are serialized as Extended JSON (`{"_id": {"$oid": "..."}}`). CORS is open.

### Services: `/service`

| Method | Description |
|---|---|
| `GET /service` | List all registered services |
| `GET /service?service_type=<type>` | Get the most recent service of that type (404 if there is none) |
| `POST /service` | Register a service. If one of the same `service_type` already exists, it is updated (200). Otherwise a new one is created (201). |
| `PUT /service` | Update a service by `_id` |
| `DELETE /service/<id>` | Remove a service |

```json
{ "service_type": "QIS", "address": "http://qis:8080", "description": "Quality Index Service" }
```

`service_type` is unique. Types used in the system:

| Type | Service |
|---|---|
| `history-tracking` | history tracking adaptor |
| `QIS` | quality index service |
| `agent_TWANoise`, `agent_WBGT`, `agent_NVIRVentilation` | sensor agents |

### Devices: `/device`

| Method | Description |
|---|---|
| `GET /device` | List all devices |
| `GET /device?device_id=<id>` | Get one device (404 if not found) |
| `GET /device?client_id=<user_id>` | List one user's devices |
| `POST /device` | Create a device (201) |
| `PUT /device` | Update a device by `_id` |
| `DELETE /device/<id>` | Delete a device |

```json
{
  "user_id": "<user id>",
  "device_type": "TWANoise",
  "location": "<map point id>",
  "description": "Desk noise sensor",
  "sensors": [{ "type": "noise", "model": "...", "unit": "dB" }],
  "connection_info": { "protocol": "EMULATOR", "emulator_type": "LIVE", "frequency_seconds": 30 }
}
```

- `device_type` must match an agent type (`TWANoise`, `WBGT`, `NVIRVentilation`).
- `connection_info` is free-form, but it must include `protocol`. The fields the gateway understands are listed in the [device-gateway README](https://github.com/PIoT-20/device-gateway).

### Users: `/user`

| Method | Description |
|---|---|
| `GET /user` | List all users |
| `POST /user` | Create a user |
| `PUT /user` | Update a user by `_id` |
| `DELETE /user/<id>` | Delete a user |

```json
{ "name": "...", "email": "...", "svg_map": "<svg floor plan>", "points": [{ "path_id": "...", "level": 0 }] }
```

`svg_map` is the floor plan the dashboard displays. `points` are locations on that map, and devices refer to them through `location`.

## Project structure

```
src/
  api/      CherryPy resources (device, user, service) and server setup
  models/   Model classes with their MongoDB queries
  db/       MongoDB connection
```
