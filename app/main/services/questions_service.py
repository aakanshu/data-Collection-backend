from app.main import db
from app.main.models.questions import Questions
from app.main.helpers.authentication import decode_token
from ..helpers.parser import (
    _save_changes,
    _error_handler,
    _parse_object,
)
from sqlalchemy.exc import IntegrityError

def list_workflow_questions(workflow_detail_id:int):
    try:
        response = {"data": []}
        rows = (
            Questions.query
            .filter_by(workflow_details_id=workflow_detail_id, active=True)
            .order_by(Questions.question_serial_num)
            .all()
        )
        for row in rows:
            response["data"].append(_parse_question(row))
        return response, 200
    except Exception as e:
        _error_handler("GET", "/workflow_details/"+str(workflow_detail_id)+"/questions", e, 500)

def list_all():
    try:
        response = {"data": []}
        rows = Questions.query.filter_by(active=True).all()
        for row in rows:
            response["data"].append(_parse_question(row))
        return response, 200
    except Exception as e:
        return _error_handler("GET", "/questions", e, 500)

def add_row(data, request):
    try:
        payload, status = decode_token(request)
        if status != 200:
            return {"status": "User not found."}, 404
        user_id = payload.get("sub")
        record = Questions.add_record(data, user_id)
        _save_changes(record)
        return {"id": record.id, "status": "success"}, 201
    except IntegrityError as e:
        return _error_handler("POST", "/questions", e, 500)

def list_id(id):
    try:
        row = Questions.query.filter_by(id=id, active=True).first()
        if not row:
            return {"data": []}, 404
        return {"data":  _parse_question(row)}, 200
    except Exception as e:
        return _error_handler("GET", "/questions/"+str(id), e, 500)

def update_row(id, data, request):
    try:
        row = Questions.query.filter_by(id=id, active=True).first()
        if not row:
            return {"status": "No object found!"}, 404
        payload, status = decode_token(request)
        if status != 200:
            return {"status": "User not found."}, 404
        user_id = payload.get("sub")
        Questions.update_record(row, data, user_id)
        db.session.commit()
        return {"status": "Record update successfully"}, 200
    except Exception as e:
        return _error_handler("GET", "/questions/"+str(id), e, 500)

def delete_row(id, request):
    return update_row(id, {"active": False}, request)

def _parse_question(question):
    data = _parse_object(question)
    data["question_type"] = data["question_type"].name
    return data