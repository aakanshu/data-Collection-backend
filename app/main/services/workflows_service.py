from app.main.helpers.authentication import decode_token
from app.main import db
from app.main.models.workflows import Workflows, WorkflowDetails
from ..helpers.parser import (
    _save_changes,
    _error_handler,
    _parse_object,
    _parse_list
)
from sqlalchemy.exc import IntegrityError
AUDIT_ATTR = [
    "active",
    "created", 
    "created_by", 
    "last_modified", 
    "last_modified_by"
]

def list_all():
    try:
        response = {"data": []}
        rows = Workflows.query.filter_by(active=True).all()
        for row in rows:
            response["data"].append(_parse_workflow(row))
        return response, 200
    except Exception as e:
        return _error_handler("GET", "/workflows", e, 500)

def add_row(data, request):
    try:
        payload, status = decode_token(request)
        if status != 200:
            return {"status": "User not found."}, 404
        user_id = payload.get("sub")
        record = Workflows.add_record(user_id)
        _save_changes(record)
        for details in _generate_details(data):
            row = WorkflowDetails.add_record(details, record.id, user_id)
            _save_changes(row)
        return {"id": record.id, "status": "success"}, 201
    except IntegrityError as e:
        return _error_handler("POST", "/workflows", e, 500)

def list_id(id):
    try:
        row = Workflows.query.filter_by(id=id, active=True).first()
        if not row:
            return {"data": []}, 404
        return {"data": _parse_workflow(row)}, 200
    except Exception as e:
        return _error_handler("GET", "/workflows/"+str(id), e, 500)

def update_row(id, data, request):
    try:
        row = Workflows.query.filter_by(id=id, active=True).first()
        if not row:
            return {"status": "No object found!"}, 404
        payload, status = decode_token(request)
        if status != 200:
            return {"status": "User not found."}, 404
        user_id = payload.get("sub")
        parsed_data = {}
        for lang_data in _generate_details(data):
            parsed_data[lang_data['language']] = lang_data
        for workflow_detail in row.workflow_details:
            language_name = workflow_detail.language.name
            if language_name in data.keys():
                WorkflowDetails.update_record(workflow_detail, parsed_data[language_name], user_id)
        db.session.commit()
        return {"status": "Record update successfully"}, 200
    except Exception as e:
        return _error_handler("GET", "/workflows/"+str(id), e, 500)

def delete_row(id, request):
    row = Workflows.query.filter_by(id=id, active=True).first()
    if not row:
        return {"status": "No object found!"}, 404
    payload, status = decode_token(request)
    if status != 200:
        return {"status": "User not found."}, 404
    user_id = payload.get("sub")
    for details in row.workflow_details:
        details.last_modified_by = user_id
        details.active = False
    row.active = False
    row.last_modified_by = user_id
    db.session.commit()
    return {"status": "Workflow Deleted successfully"}, 200

def _generate_details(obj):
    data = []
    for language in obj:
        detail_obj = obj[language]
        detail_obj["language"] = language
        if "name" in detail_obj:
            data.append(detail_obj)
    return data

def _parse_workflow(workflow):
    workflow_details = _parse_list(workflow.workflow_details)
    for index in range(len(workflow_details)):
        workflow_details[index]['language'] = workflow_details[index]['language'].name
    data = _parse_object(workflow)
    data["workflow_details"] = workflow_details
    return data
