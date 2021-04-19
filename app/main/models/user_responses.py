from app.main import db
import datetime

class UserResponses(db.Model):
    __tablename__ = "user_responses"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user_workflow_id = db.Column(db.Integer, db.ForeignKey("user_workflows.id"), nullable=False)
    workflow_details_id = db.Column(db.Integer, db.ForeignKey("workflow_details.id"), nullable=False)
    response = db.Column(db.JSON, nullable=False)
    response_status = db.Column(db.String(30), nullable=False, default="REVIEW")
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
        return "<UserResponses: {}".format(self.id)

    def add_record(data, user_id):
        return UserResponses(
            user_id=data.get("user_id", user_id),
            user_workflow_id=data.get("user_workflow_id"),
            workflow_details_id=data.get("workflow_details_id"),
            response=data.get("response"),
            response_status=data.get("response_status","REVIEW"),
            created=datetime.datetime.now(),
            created_by=user_id,
            last_modified=datetime.datetime.now(),
            last_modified_by=user_id
        )
    
    def update_record(row, data, user_id):
        row.user_id = data.get("user_id", row.user_id)
        row.user_workflow_id = data.get("user_workflow_id", row.user_workflow_id)
        row.workflow_details_id = data.get("workflow_details_id", row.workflow_details_id)
        row.response = data.get("response", row.response)
        row.response_status = data.get("response_status", row.response_status)
        row.last_modified = datetime.datetime.now()
        row.last_modified_by = user_id
        row.active = data.get("active", row.active)
        