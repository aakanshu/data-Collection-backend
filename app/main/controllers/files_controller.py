from app.main import logger
from flask import request
from flask_restx import Resource
from ..services.storage_service import (
    upload_file
)
from ..utils.dto import FilesDto, upload_parser
api = FilesDto.api
_files_post = FilesDto.files

@api.route("/upload")
class Users(Resource):
    @api.expect(upload_parser)
    @api.response(201, "New record created successfully.")
    def post(self):
        """ Create a new users """
        logger.info("upload api called")
        logger.info(request.files)
        logger.info(request.files["file_attachment"])
        uploaded_file = request.files["file_attachment"]
        logger.info(upload_file)
        return upload_file(file=uploaded_file)
