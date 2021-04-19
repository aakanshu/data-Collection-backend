from flask import request
from flask_restx import Resource
from ..services.user_workflows_service import (
    list_all,
    list_id,
    add_row,
    update_row,
    delete_row
)
from ..utils.dto import UserWorkflowsDto
api = UserWorkflowsDto.api
_user_workflows_post = UserWorkflowsDto.user_workflows

@api.route("/")
class UserWorkflows(Resource):
    @api.doc(
        params={
            "language": {
                "description": "Name of the event",
                "in": "query",
                "type": "string",
                "example": "en",
            }
        }
    )
    @api.response(500, "Internal Server Error")
    def get(self):
        """ List all the user_workflows """
        language = request.args.get("language", "en")
        if language not in ["en", "ru"]:
            language = "en"
        return list_all(language)

    @api.expect(_user_workflows_post)
    @api.response(201, "New record created successfully.")
    def post(self):
        """ Create a new user_workflows """
        data = request.json
        if 'user_id' not in data or 'workflow_id' not in data:
            return {"status": "Input Validation failed"}, 412
        return add_row(request.json, request)

@api.route("/<int:id>")
@api.param("id", "UserWorkflows type identifier")
class UserWorkflowsList(Resource):
    @api.doc(
        params={
            "language": {
                "description": "Name of the event",
                "in": "query",
                "type": "string",
                "example": "en",
            }
        }
    )
    def get(self, id):
        """ Get details of an existing user_workflows """
        language = request.args.get("language", "en")
        if language not in ["en", "ru"]:
            language = "en"
        return list_id(id, language)
    
    @api.expect(_user_workflows_post)
    def put(self, id):
        """ Update an existing user_workflows """
        return update_row(id, request.json, request)

    def delete(self, id):
        """ Delete an existing user_workflows """
        return delete_row(id, request)
