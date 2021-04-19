from app.main import flask_bcrypt, logger
from app.main.config import key
import jwt

def password(password):
    return (
        flask_bcrypt.generate_password_hash(password).decode("utf-8")
    )

def check_password(password_hash, password):
    return flask_bcrypt.check_password_hash(password_hash, password)

def decode_token(request):
    try:
        token = request.headers.get("Authorization").split(" ")[1]
        payload = jwt.decode(token, key, algorithms=["HS256"])
        return payload, 200
    except Exception as e:
        logger.error(str(e))
        return {"status": "Invalid token"}, 401
