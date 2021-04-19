from flask.globals import request
from flask_restx import Namespace, fields, reqparse
from werkzeug.datastructures import FileStorage
import enum
authorization = reqparse.RequestParser()
authorization.add_argument("Authorization", location="headers", required=True)

upload_parser = reqparse.RequestParser()
upload_parser.add_argument("file_attachment", location="files", type=FileStorage, required=True)

class EnumLanguage(enum.Enum):
    English = 'en'
    Russian = 'ru'

class UsersDto:
    api = Namespace("users", description="comment related operations")
    users = api.inherit(
        "users",
        {
            "email": fields.String(
                required=True,
                description="user email address",
                example="admin@cargill.com",
            ),
            "name": fields.String(
                required=True, description="user username", example="First lastname"
            ),
            "password_hash": fields.String(
                required=False, description="user password", example="abc123"
            ),
            "photo_url": fields.String(required=False, description="photo url")
        }
    )
    login = api.inherit(
        "users",
        {
            "email": fields.String(
                required=True,
                description="user email address",
                example="admin@cargill.com"
            ),
            "password": fields.String(
                required=True,
                description="user password",
                example="admin123"
            )
        }
    )

class AnalyticsDto:
    api = Namespace("analytics", description="API for Analytics", ordered=True)
    analytics_post = api.model(
        "analytics",
        {
            "event_name": fields.String(
                required=True,
                description="Name of the event for which data is recorded",
                example="USER_LOGIN",
            ),
            "user_data": fields.Raw(
                required=False,
                description="A json object stored as string to pass all the related information",
                example={"data": "something"}
            ),
            "device_info": fields.Raw(
                required=False,
                description="A json object to store the device info",
                example={"device": "mobile", "browser": "Chrome 80"},
            ),
            "network_info": fields.Raw(
                required=False,
                description="A json object to store the network info",
                example={"network": "3G"},
            )
        },
    )

class WorkflowsDto:
    api = Namespace("workflows", description="API for workflows", ordered=True)
    workflows = api.model(
        "workflows",
        {
            "en": fields.Raw(
                required=True,
                description="English language details",
                example={
                    "name": "Test workflow",
                    "description": "Some help text about workflow",
                    "description_image": ""
                },
            ),
            "ru": fields.Raw(
                required=True,
                description='Language',
                example={
                    "name": "Рабочий процесс тестирования",
                    "description": "Некоторая справка о рабочем процессе",
                    "description_image": ""
                },
            )
        },
    )

class UserWorkflowsDto:
    api = Namespace("user_workflows", description="API for workflows", ordered=True)
    user_workflows = api.model(
        "user_workflows",
        {
            "user_id": fields.Integer(
                required=True,
                description="User Id to whom workflow has to be assigned",
                example=2
            ),
            "workflow_id": fields.Integer(
                required=True,
                description="Workflow Id",
                example=3
            ),
            "times": fields.Integer(
                required=False,
                description="No. of times we has to complete workflow",
                example=1
            ),
            "completed": fields.Integer(
                required=False,
                description="No of workflows completed",
                example=0
            )
        },
    )

class UserResponsesDto:
    api = Namespace("user_responses", description="data filled by the user")
    user_responses = api.inherit(
        "user_responses",
        {
            "user_id": fields.Integer(
                required=False,
                description="User Id who has submitted the response",
                example=2
            ),
            "user_workflow_id": fields.Integer(
                required=True,
                description="User Id who has submitted the response",
                example=2
            ),
            "workflow_details_id": fields.Integer(
                required=True,
                description="User Id who has submitted the response",
                example=2
            ),
            "response": fields.Raw(
                required=True,
                description="{'<question_id>:'<response>'}",
                example={
                    "<question_id>": "<response>"
                }
            ),
            "response_status": fields.String(
                required=False,
                description="user response status",
                example="REVIEW"
            )
        }
    )

class QuestionsDto:
    api = Namespace("questions", description="Questions for the workflows")
    questions = api.inherit(
        "questions",
        {
            "workflow_details_id": fields.Integer(
                required=True,
                description="workflow detail Id in which question is getting attached",
                example=2
            ),
            "name": fields.String(
                required=True,
                description="Question title",
                example="Chicken video recording"
                ),
            "description": fields.String(
                required=False,
                description="Question description",
                example="Instructions to answer question"
                ),
            "help_text": fields.String(
                required=False,
                description="Help text for question",
                example="Metrics or other information for answering question"
                ),
            "is_required": fields.Boolean(
                required=False,
                description="Defines if the question is required to answer",
                example=False
                ),
            "question_type": fields.String(
                required=True,
                description="Defines question type",
                enum=['text','video', 'number']
                ),
            "default_value": fields.String(
                required=False,
                description="",
                example=""
                ),
            "question_serial_num": fields.Integer(
                required=True,
                description="Order in which question is placed in the form",
                example="1"
                ),
        }
    )

class EnumQuestions(enum.Enum):
    Video = 'video'
    Text = 'text'
    Number = 'number'

class FilesDto:
    api = Namespace("files", description="APIs for handling files")
    files = api.inherit("files", {})