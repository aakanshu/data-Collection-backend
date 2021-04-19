from app.main import db, logger
AUDIT_ATTR = ["active", "created", "created_by", "last_modified", "last_modified_by"]

def _parse_object(obj, audit_attr=AUDIT_ATTR, date_attr=[]):
    data = {k: v for k, v in obj.__dict__.items() if not k.startswith("_")}
    [data.pop(key) for key in audit_attr]
    for key in date_attr:
        if data[key] != None: data[key] = data[key].isoformat()
    return data


def _parse_list(arr, audit_attr=AUDIT_ATTR, date_attr=[]):
    data = []
    for obj in arr:
        if obj.active == True:
            data.append(_parse_object(obj, audit_attr, date_attr))
    return data


def _raw_parse_list(arr, audit_attr, date_attr):
    data = []
    for obj in arr:
        data.append(_parse_object(obj, audit_attr, date_attr))
    return data


def _save_changes(data):
    db.session.add(data)
    db.session.commit()


def _field_present(data, fields):
    input_list = data.keys()
    return all(item in input_list for item in fields)


def _diff_list(list_a, list_b):
    return list(set(list_a) - set(list_b))


def _get_elements(arr, key):
    data = []
    for item in arr:
        data.append(item[key])
    return data

def _error_handler(method, path, e, error_code):
    db.session.rollback()
    logger.error("Exception occurred in " + method + " " + path + "API, error: " + str(e))
    if error_code == 500:
       return {"status": "Internal server error."}, error_code 
    else:
        return {"status": "Error occurred while updating record."}, error_code