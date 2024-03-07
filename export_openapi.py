import json

import yaml

from api_main import create_app


app = create_app()

openapi_schema = app.openapi()

with open("openapi.json", "w") as f:
    json.dump(openapi_schema, f)

with open("openapi.yaml", "w") as f:
    yaml.dump(openapi_schema, f, sort_keys=False)

