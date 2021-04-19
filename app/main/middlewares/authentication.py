from werkzeug.wrappers import Request, Response
from app.main.config import key
import jwt
import time
import logging
logging.basicConfig(level=logging.INFO, format=f"%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger()
SKIP_VALIDATION = ['/swagger-ui.html',  '/swagger.json', '/swaggerui/favicon-32x32.png',
    '/swaggerui/swagger-ui-standalone-preset.js', '/swaggerui/swagger-ui-bundle.js',
    '/swaggerui/droid-sans.css', '/swaggerui/swagger-ui.css',
    '/swaggerui/swagger-ui-standalone-preset.js', '/swaggerui/favicon-16x16.png',
    '/health', '/users/login']

class TokenValidation():
    '''
    Simple WSGI middleware to validate token
    '''

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        request = Request(environ, shallow=True)
        if request.path in SKIP_VALIDATION:
            return self.app(environ, start_response)
        logger.info("Middleware called for API path " + str(request.path))
        if request.headers.get("Authorization"):
            token = request.headers.get("Authorization").split(" ")[-1]
            try:
                payload = jwt.decode(token, key, algorithms=["HS256"])
                if payload['exp'] > int(time.time()):
                    return self.app(environ, start_response)
            except Exception as e:
                res = Response(u'Authorization failed', mimetype= 'text/plain', status=401)
                return res(environ, start_response)
        else:
            res = Response(u'Authorization failed', mimetype= 'text/plain', status=401)
            return res(environ, start_response)
