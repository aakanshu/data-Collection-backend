from flask import request
from flask_restx import Resource
from app.main.services.user_responses_service import (
    list_all,
    list_id,
    add_row,
    update_row,
    delete_row
)
from ..utils.dto import UserResponsesDto
api = UserResponsesDto.api
_user_responses_post = UserResponsesDto.user_responses

@api.route("")
class UserResponses(Resource):
    @api.response(500, "Internal Server Error")
    def get(self):
        """ List all the user_responses """
        return list_all()

    @api.expect(_user_responses_post)
    @api.response(201, "New record created successfully.")
    def post(self):
        """ Create a new user_responses """
        return add_row(request.json, request)

@api.route("/<int:id>")
@api.param("id", "UserResponses type identifier")
class UserResponsesList(Resource):
    def get(self, id):
        """ Get details of an existing user_responses """
        return list_id(id)
    
    @api.expect(_user_responses_post)
    def put(self, id):
        """ Update an existing user_responses """
        return update_row(id, request.json, request)

    def delete(self, id):
        """ Delete an existing user_responses """
        return delete_row(id, request)
