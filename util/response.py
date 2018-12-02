__author__ = "Suyash Soni"
__email__ = "suyash.soni248@gmail.com"

import time
from flask_restful import fields, marshal
from flask import request
from util.error_handlers.exceptions import BaseException, Error
from util.constants.error_codes import ErrorCode
from flask import Response as FlaskResponse
from pymysql import MySQLError
from sqlalchemy.exc import SQLAlchemyError
from util.logger import Logger

class Response(object):
    def __init__(self, success=True, data=None, errors=(), message="", status_code=200, headers=None, mimetype=None):
        self.success = success
        self.data = data
        self.errors = errors
        self.message = message

        # These fields won't be marshaled and hence won't be part of `data` in underlying response.
        self.status_code = status_code
        self.headers = headers
        self.mimetype = mimetype

def response_builder(response):
    """
    Marshals & transforms `Response` object to the response format supported by Flask-Restful, and return it.

    :param response: instance of `Response` class as returned by controller's action method.

    :return: `response data`, `status code`, `response headers`
    """
    # Actual response structure in the form of JSON.
    marshal_fields = {
        "success": fields.Boolean,
        "message": fields.String,
        "data": fields.Raw,
        "errors": fields.Raw
    }

    if response.data and not isinstance(response.data, (list, set, dict, str, tuple, int, float, bool)):
        return FlaskResponse(response.data, mimetype=response.mimetype)

    marshaled_res = marshal(response, marshal_fields)
    headers = dict(response.headers) if response.headers else None
    return marshaled_res, response.status_code, headers


def intercept(profiler=True):
    """
     Request-Response interceptor which handles response format.

    :param profiler: Logs the the time taken by the underlying request.
    """
    def _intercept_decorator(func):
        def wrapper(controller, *args, **kwargs):
            try:

                start = time.time()
                response_obj = func(controller, *args, **kwargs)
                end = time.time()
                if profiler:
                    api_name = "{}: {}".format(func.__name__.upper(), request.url_rule)
                    Logger.info("{} took {} sec(s)".format(api_name, end-start))

            except BaseException as be:
                # Custom exceptions are handled here.
                import traceback
                print(traceback.format_exc())
                if not isinstance(be.errors, (list, tuple)):
                    be.errors = [be.errors]
                response_obj = Response(success=False, status_code=be.status_code, message=be.message,
                                        errors=be.errors)
            except (MySQLError, SQLAlchemyError) as dbe:
                # Default exceptions thrown by SQLAlchemy are handled here.
                import traceback
                print(traceback.format_exc())

                message = 'Database error occurred.'
                response_obj = Response(success=False, status_code=500, message=message,
                                        errors=[Error(ErrorCode.DB_ERROR, 'database_error', message=str(dbe)).to_dict])
            except Exception as e:
                # Any uncaught exception will be handled here.
                import traceback
                print (traceback.format_exc())
                response_obj = Response(success=False, status_code=500,
                                        errors=[Error(ErrorCode.NON_STANDARD_ERROR, message=str(e)).to_dict])

            return response_builder(response_obj)
        return wrapper

    return _intercept_decorator