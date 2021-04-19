from app.main import db
from app.main.helpers.authentication import password, check_password
import datetime
from app.main.config import key
import jwt

class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(100))
    photo_url = db.Column(db.String(255))
    # created = db.Column(
    #     db.DateTime, nullable=False, default=datetime.datetime.now()
    # )
    # created_by = db.Column(db.Integer, nullable=False)
    # last_modified = db.Column(
    #     db.DateTime,
    #     nullable=False,
    #     default=datetime.datetime.now(),
    #     onupdate=datetime.datetime.now()
    # )
    # last_modified_by = db.Column(db.Integer)
    active = db.Column(db.Boolean, default=True, nullable=False)

    def __repr__(self):
        return "<Users: {}".format(self.id)

    def add_record(data):
        return Users(
            name = data.get("name", ''),
            email = data.get("email"),
            password_hash = password(data.get("password")),
            photo_url = data.get("photo_url", ''),
            # created_by = user_id,
            # last_modified_by = user_id
        )

    def update_record(row, data):
        row.name = data.get("name", row.name)
        row.email = data.get("email", row.email)
        if data.get("password", False):
            row.password_hash = password(data.get("password"))
        row.photo_url = data.get("photo_url", row.photo_url)
        row.active = data.get("active", row.active)
        # row.last_modified_by = user_id

    def generate_token(user, password):
        is_matched = check_password(user.password_hash, password)
        if not is_matched:
            return {"status": "Invalid Credentials!"}, 401
        payload={
            'exp': datetime.datetime.now() + datetime.timedelta(days=30),
            'iat': datetime.datetime.now(), 'sub': user.id }
        # row = AccessToken.add_row(user.id)
        # db.session.add(row)
        # db.session.commit()
        return {"token": str(jwt.encode(payload, key, algorithm="HS256")), "status": "Login successfully"}, 200

        