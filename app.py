from flask import Flask
from flask_smorest import Api
from flask_cors import CORS

from src.controllers.v1.store_controller import blp as StoreBlueprint
from src.controllers.v1.register_controller import blp as RegisterBlueprint

app = Flask(__name__)

app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "Self Checkout REST API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

api = Api(app)

api.register_blueprint(StoreBlueprint)
api.register_blueprint(RegisterBlueprint)

if __name__ == "__main__":
    app.run(host='0.0.0.0')