import enum
from app.main import db
from app.main.helpers.authentication import password, check_password
import datetime

class RefLanguage(enum.Enum):
    en = 'English'
    ru = 'Russian'

class Workflows(db.Model):
    __tablename__ = "workflows"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
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
    workflow_details = db.relationship("WorkflowDetails")
    
    def __repr__(self):
        return "<Workflows: {}".format(self.id)

    def add_record(user_id):
        return Workflows(
            created = datetime.datetime.now(),
            last_modified = datetime.datetime.now(),
            created_by = user_id,
            last_modified_by = user_id
        )

class WorkflowDetails(db.Model):
    __tablename__ = "workflow_details"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    workflow_id = db.Column(db.Integer, db.ForeignKey("workflows.id"))
    name = db.Column(db.String(300), nullable=False)
    description = db.Column(db.Text)
    description_image = db.Column(db.String(300))
    language = db.Column(db.Enum(RefLanguage))
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
        return "<WorkflowDetails: {}".format(self.id)

    def add_record(data, workflow_id, user_id):
        return WorkflowDetails(
            workflow_id = workflow_id,
            name = data.get("name"),
            description = data.get("description", ""),
            description_image = data.get("description_image", ""),
            language = data.get("language", "en"),
            created = datetime.datetime.now(),
            last_modified = datetime.datetime.now(),
            created_by = user_id,
            last_modified_by = user_id
        )
    
    def update_record(row, data, user_id):
        row.name = data.get("name", row.name)
        row.description = data.get("description", row.description)
        row.description_image = data.get("description_image", row.description_image)
        row.last_modified = datetime.datetime.now()
        row.active = data.get("active", row.active)
        row.last_modified_by = user_id

class UserWorkflows(db.Model):
    __tablename__ = "user_workflows"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    workflow_id = db.Column(db.Integer, db.ForeignKey("workflows.id"))
    times = db.Column(db.Integer, nullable=False, default=1)
    completed = db.Column(db.Integer, nullable=False, default=0)
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
    workflows = db.relationship("Workflows")

    def __repr__(self):
        return "<UserWorkflows: {}".format(self.id)

    def add_record(data, user_id):
        return UserWorkflows(
            user_id = data.get("user_id"),
            workflow_id = data.get("workflow_id"),
            times = data.get("times", 1),
            completed = data.get("completed", 0),
            created = datetime.datetime.now(),
            last_modified = datetime.datetime.now(),
            created_by = user_id,
            last_modified_by = user_id
        )

    def update_record(row, data, user_id):
        row.times = data.get("times", row.times)
        row.completed = data.get("completed", row.completed)
        row.last_modified = datetime.datetime.now()
        row.active = data.get("active", row.active)
        row.last_modified_by = user_id