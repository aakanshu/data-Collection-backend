from .. import db
import datetime

class Analytics(db.Model):
    """ Analytics Model for storing the events """
    __tablename__ = "analytics"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    event_name = db.Column(db.String(255), nullable=False)
    user_data = db.Column(db.JSON, nullable=False)
    device_info = db.Column(db.JSON, nullable=False)
    network_info = db.Column(db.JSON, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
    active = db.Column(db.Boolean, default=True, nullable=False)

    def __repr__(self):
        return "<Record : {}".format(self.id)

    def get_events(search):
        if search == "":
            return Analytics.query.filter_by(active=True).all()
        return (
            Analytics.query.filter(Analytics.event_name.ilike(search))
            .filter_by(active=True)
            .all()
        )

    def add_record(data, user_id):
        return Analytics(
            user_id = user_id,
            event_name = data.get("event_name", "DEFAULT"),
            user_data = data.get("user_data"),
            device_info = data.get("device_info"),
            network_info = data.get("network_info"),
            created = datetime.datetime.now(),
            active=True
        )
