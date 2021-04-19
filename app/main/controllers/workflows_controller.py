from app.main.services.questions_service import list_workflow_questions
from flask import request
from flask_restx import Resource
from ..services.workflows_service import (
    list_all,
    list_id,
    add_row,
    update_row,
    delete_row
)
from ..utils.dto import WorkflowsDto
api = WorkflowsDto.api
_workflows_post = WorkflowsDto.workflows

@api.route("")
class Workflows(Resource):
    @api.response(500, "Internal Server Error")
    def get(self):
        """ List all the workflows """
        return list_all()

    @api.expect(_workflows_post)
    @api.response(201, "New record created successfully.")
    def post(self):
        """ Create a new workflows """
        return add_row(request.json, request)

@api.route("/<int:id>")
@api.param("id", "Workflows type identifier")
class WorkflowsList(Resource):
    def get(self, id):
        """ Get details of an existing workflows """
        return list_id(id)
    
    @api.expect(_workflows_post)
    def put(self, id):
        """ Update an existing workflows """
        return update_row(id, request.json, request)

    def delete(self, id):
        """ Delete an existing workflows """
        return delete_row(id, request)

@api.route("/<int:workflow_details_id>/questions")
@api.param("workflow_details_id", "workflow details type identifier")
class WorkflowQuestions(Resource):
    def get(self, workflow_details_id):
        return list_workflow_questions(workflow_details_id)