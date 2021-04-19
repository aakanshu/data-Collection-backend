from flask import request
from flask_restx import Resource
from ..services.questions_service import (
    list_all,
    list_id,
    add_row,
    update_row,
    delete_row
)
from ..utils.dto import QuestionsDto
api = QuestionsDto.api
_questions_post = QuestionsDto.questions

@api.route("")
class Questions(Resource):
    @api.response(500, "Internal Server Error")
    def get(self):
        """ List all the questions """
        return list_all()

    @api.expect(_questions_post)
    @api.response(201, "New record created successfully.")
    def post(self):
        """ Create a new questions """
        return add_row(request.json, request)

@api.route("/<int:id>")
@api.param("id", "Questions type identifier")
class QuestionsList(Resource):
    def get(self, id):
        """ Get details of an existing questions """
        return list_id(id)
    
    @api.expect(_questions_post)
    def put(self, id):
        """ Update an existing questions """
        return update_row(id, request.json, request)

    def delete(self, id):
        """ Delete an existing questions """
        return delete_row(id)
