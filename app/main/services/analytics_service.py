from app.main.helpers.authentication import decode_token
from app.main.models.analytics import Analytics
from ..helpers.parser import (
    _save_changes,
    _error_handler,
    _parse_list
)
from sqlalchemy.exc import IntegrityError
AUDIT_ATTR = ['active', 'created']

def list_all(search):
    try:
        rows = Analytics.get_events(search)
        return {"data":  _parse_list(rows, AUDIT_ATTR, [])}, 200
    except Exception as e:
        return _error_handler("GET", "/analytics", e, 500)

def add_row(data, request):
    try:
        payload, status = decode_token(request)
        if status != 200:
            return {"status": "User not found."}, 404
        user_id = payload.get("sub")
        record = Analytics.add_record(data, user_id)
        _save_changes(record)
        return {"id": record.id, "status": "success"}, 201
    except IntegrityError as e:
        return _error_handler("POST", "/analytics", e, 500)
