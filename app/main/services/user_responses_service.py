from app.main import db
from app.main.models.user_responses import UserResponses
from app.main.helpers.authentication import decode_token
from ..helpers.parser import (
    _save_changes,
    _error_handler,
    _parse_object,
    _parse_list
)
from sqlalchemy.exc import IntegrityError

def list_all():
    try:
        rows = UserResponses.query.filter_by(active=True).all()
        return {"data":  _parse_list(rows)}, 200
    except Exception as e:
        return _error_handler("GET", "/user_responses", e, 500)

def add_row(data, request):
    try:
        payload, status = decode_token(request)
        if status != 200:
            return {"status": "User not found."}, 404
        user_id = payload.get("sub")
        record = UserResponses.add_record(data, user_id)
        _save_changes(record)
        return {"id": record.id, "status": "success"}, 201
    except IntegrityError as e:
        return _error_handler("POST", "/user_responses", e, 500)

def list_id(id):
    try:
        row = UserResponses.query.filter_by(id=id, active=True).first()
        if not row:
            return {"data": []}, 404
        return {"data":  _parse_object(row)}, 200
    except Exception as e:
        return _error_handler("GET", "/user_responses/"+str(id), e, 500)

def update_row(id, data, request):
    try:
        row = UserResponses.query.filter_by(id=id, active=True).first()
        if not row:
            return {"status": "No object found!"}, 404
        payload, status = decode_token(request)
        if status != 200:
            return {"status": "User not found."}, 404
        user_id = payload.get("sub")
        UserResponses.update_record(row, data, user_id)
        db.session.commit()
        return {"status": "Record update successfully"}, 200
    except Exception as e:
        return _error_handler("GET", "/user_responses/"+str(id), e, 500)

def delete_row(id, request):
    return update_row(id, {"active": False}, request)
