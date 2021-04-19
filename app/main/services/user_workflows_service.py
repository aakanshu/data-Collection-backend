from app.main.helpers.authentication import decode_token
from app.main import db
from app.main.models.workflows import UserWorkflows
from app.main.services.workflows_service import _parse_workflow
from ..helpers.parser import (
    _save_changes,
    _error_handler,
    _parse_object,
)
from sqlalchemy.exc import IntegrityError

def list_all(language):
    try:
        response = {"data": []}
        rows = UserWorkflows.query.filter_by(active=True).all()
        for row in rows:
            response["data"].append(_parse_user_workflows(row, language))
        return response, 200
    except Exception as e:
        return _error_handler("GET", "/user_workflows", e, 500)

def add_row(data, request):
    try:
        payload, status = decode_token(request)
        if status != 200:
            return {"status": "User not found."}, 404
        user_id = payload.get("sub")
        record = UserWorkflows.add_record(data, user_id)
        _save_changes(record)
        return {"id": record.id, "status": "success"}, 201
    except IntegrityError as e:
        return _error_handler("POST", "/user_workflows", e, 500)

def list_id(id, language):
    try:
        response = {"data": []}
        row = UserWorkflows.query.filter_by(id=id, active=True).first()
        if not row:
            return response, 404
        response["data"].append(_parse_user_workflows(row, language))
        return response, 200
    except Exception as e:
        return _error_handler("GET", "/user_workflows/"+str(id), e, 500)

def update_row(id, data, request):
    try:
        row = UserWorkflows.query.filter_by(id=id, active=True).first()
        if not row:
            return {"status": "No object found!"}, 404
        payload, status = decode_token(request)
        if status != 200:
            return {"status": "User not found."}, 404
        user_id = payload.get("sub")
        UserWorkflows.update_record(row, data, user_id)
        db.session.commit()
        return {"status": "Record update successfully"}, 200
    except Exception as e:
        return _error_handler("PUT", "/user_workflows/"+str(id), e, 500)

def delete_row(id, request):
    return update_row(id, {"active": False}, request)

def _parse_user_workflows(user_workflow, language):
    data = _parse_object(user_workflow)
    workflow = _parse_workflow(user_workflow.workflows)
    for item in workflow["workflow_details"]:
        if item["language"] == language:
            data["workflow_details"] = item
            break;
    return data
