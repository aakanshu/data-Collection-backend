from flask import request
from flask_restx import Resource
from ..services.users_service import (
    list_all,
    list_id,
    add_row,
    update_row,
    delete_row,
    user_login,
    # user_logout
)
from ..utils.dto import UsersDto, authorization
api = UsersDto.api
_users_post = UsersDto.users
_users_login = UsersDto.login

@api.route("")
class Users(Resource):
    @api.response(500, "Internal Server Error")
    def get(self):
        """ List all the users """
        return list_all()

    @api.expect(_users_post)
    @api.response(201, "New record created successfully.")
    def post(self):
        """ Create a new users """
        return add_row(request.json, request)

@api.route("/<int:id>")
@api.param("id", "Users type identifier")
class UsersList(Resource):
    def get(self, id):
        """ Get details of an existing users """
        return list_id(id)
    
    @api.expect(_users_post)
    def put(self, id):
        """ Update an existing users """
        return update_row(id, request.json, request)

    def delete(self, id):
        """ Delete an existing users """
        return delete_row(id)

@api.route("/login")
class UsersLogin(Resource):
    @api.expect(_users_login)
    def post(self):
        """ API for user login """
        return user_login(request.json)

# @api.route("/logout")
# class UsersLogout(Resource):
#     @api.expect(authorization)
#     def get(self):
#         """ Logout API to invalidate token """
#         return user_logout(request)
