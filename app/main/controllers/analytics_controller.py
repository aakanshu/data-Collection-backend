from flask import request
from flask_restx import Resource

from app.main.services.analytics_service import (
    list_all,
    add_row,
)
from app.main.utils.dto import AnalyticsDto

api = AnalyticsDto.api
_analytics_post = AnalyticsDto.analytics_post


@api.route("")
class AnalyticsList(Resource):
    @api.doc(
        params={
            "event_name": {
                "description": "Name of the event",
                "in": "query",
                "type": "string",
                "example": "USER_LOGIN",
            }
        }
    )
    @api.response(200, "Records fetched successfully.")
    def get(self):
        """ List all the events """
        search_query = request.args.get("event_name", "")
        return list_all(search_query)

    @api.doc("Record New event")
    @api.response(201, "Event recorded successfully.")
    @api.expect(_analytics_post)
    def post(self):
        """ Add new Event """
        return add_row(request.json, request)
