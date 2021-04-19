import enum
from app.main import db
from app.main.helpers.authentication import password, check_password
import datetime

class RefQuestions(enum.Enum):
    video = 'Video Question'
    text = 'Text Question'
    number = 'Number Question'

class Questions(db.Model):
    __tablename__ = "questions"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    workflow_details_id = db.Column(db.Integer, db.ForeignKey("workflow_details.id"))
    name = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text)
    help_text = db.Column(db.Text)
    is_required = db.Column(db.BOOLEAN, nullable=False, default=False)
    question_type = db.Column(db.Enum(RefQuestions), nullable=False)
    default_value = db.Column(db.Text)
    question_serial_num = db.Column(db.Integer, nullable=False)
    created = db.Column(
        db.DateTime, nullable=False, default=datetime.datetime.now()
    )
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    last_modified = db.Column(
        db.DateTime, db.ForeignKey("users.id"),
        nullable=False,
        default=datetime.datetime.now(),
        onupdate=datetime.datetime.now()
    )
    last_modified_by = db.Column(db.Integer)
    active = db.Column(db.Boolean, default=True, nullable=False)

    def __repr__(self):
        return "<Questions: {}".format(self.id)

    def add_record(data, user_id):
        return Questions(
            workflow_details_id = data.get("workflow_details_id"),
            name = data.get("name"),
            description = data.get("description", ""),
            help_text = data.get("help_text", ""),
            is_required = data.get("is_required", False),
            question_type = data.get("question_type", "text"),
            default_value = data.get("default_value"),
            question_serial_num = data.get("question_serial_num"),
            created = datetime.datetime.now(),
            last_modified = datetime.datetime.now(),
            created_by = user_id,
            last_modified_by = user_id
        )
    
    def update_record(row, data, user_id):
        row.workflow_details_id = data.get("workflow_details_id", row.workflow_details_id)
        row.name = data.get("name", row.name)
        row.description = data.get("description", row.description)
        row.help_text = data.get("help_text", row.help_text)
        row.is_required = data.get("is_required", row.is_required)
        row.question_type = data.get("question_type", row.question_type)
        row.default_value = data.get("default_value", row.default_value)
        row.question_serial_num = data.get("question_serial_num", row.question_serial_num)
        row.last_modified = datetime.datetime.now()
        row.active = data.get("active", row.active)
        row.last_modified_by = user_id

