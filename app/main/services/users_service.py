from app.main import db
from app.main.models.users import Users
from app.main.helpers.parser import (
    _save_changes,
    _error_handler,
    _parse_object,
    _parse_list
)
from app.main.helpers.authentication import decode_token
from sqlalchemy.exc import IntegrityError

def list_all():
    try:
        rows = Users.query.filter_by(active=True).all()
        return {"data":  _parse_list(rows,["active"],[])}, 200
    except Exception as e:
        return _error_handler("GET", "/users", e, 500)

def add_row(data, request):
    try:
        record = Users.add_record(data)
        _save_changes(record)
        return {"id": record.id, "status": "success"}, 201
    except IntegrityError as e:
        return _error_handler("POST", "/users", e, 500)

def list_id(id):
    try:
        row = Users.query.filter_by(id=id, active=True).first()
        if not row:
            return {"data": []}, 404
        return {"data":  _parse_object(row,["active"],[])}, 200
    except Exception as e:
        return _error_handler("GET", "/users/"+str(id), e, 500)

def update_row(id, data, request):
    try:
        row = Users.query.filter_by(id=id, active=True).first()
        if not row:
            return {"status": "No object found!"}, 404
        # payload, status = decode_token(request)
        # if status != 200:
        #     return {"status": "User not found."}, 404
        # user_id = payload.get("sub")
        Users.update_record(row, data)
        db.session.commit()
        return {"status": "Record update successfully"}, 200
    except Exception as e:
        return _error_handler("GET", "/users/"+str(id), e, 500)

def delete_row(id):
    return update_row(id, {"active": False})

def user_login(data):
    try:
        row = (
            Users.query
            .filter_by(email=data.get("email"), active=True).first()
        )      
        if not row:
            return {"status": "Invalid credentials!"}, 401
        return Users.generate_token(row, data.get("password"))
    except Exception as e:
        return _error_handler("POST", "/users/login", e, 500)

# def user_logout(request):
#     try:
#         token = request.headers.get("Authorization").split(" ")[1]
#         row = AccessToken.query.filter_by(id=token).first()
#         db.session.delete(row)
#         db.session.commit()
#         return {"status": "User Logged out successfully"}, 200
#     except Exception as e:
#         return _error_handler("GET", "/users/logout", e, 500)