from flask_restx import Api, Resource
from flask import Blueprint
from app.main.controllers.users_controller import api as users_ns
from app.main.controllers.analytics_controller import api as analytics_ns
from app.main.controllers.workflows_controller import api as workflows_ns
from app.main.controllers.user_workflows_controller import api as user_workflows_ns
from app.main.controllers.user_responses_controller import api as user_responses_ns
from app.main.controllers.questions_controller import api as questions_ns
from app.main.controllers.files_controller import api as files_ns

blueprint = Blueprint("api", __name__)
authorizations = {"Bearer": {"type": "apiKey", "in": "header", "name": "Authorization"}}

api = Api(
    blueprint,
    authorizations=authorizations,
    title="App Name",
    version="1.0",
    description="APIs",
    doc="/swagger-ui.html",
    security="Bearer"
)

api.add_namespace(users_ns, path="/users")
api.add_namespace(analytics_ns, path="/analytics")
api.add_namespace(workflows_ns, path="/workflows")
api.add_namespace(user_workflows_ns, path="/user_workflows")
api.add_namespace(user_responses_ns, path="/user_responses")
api.add_namespace(questions_ns, path="/questions")
api.add_namespace(files_ns, path="/files")

@api.route("/validateToken")
class ValidateToken(Resource):
    def get(self):
        return {"status": "Is valid"}
@api.route("/health")
class HealthEndpoint(Resource):
    def get(self):
        return {"status": "Service is running"}
