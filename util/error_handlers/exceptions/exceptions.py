__author__ = "Suyash Soni"
__email__ = "suyash.soni248@gmail.com"

import itertools
from settings import config
from util.constants.error_codes import ErrorCode

class Error(object):
    """
    Every time error needs to thrown, instance of this class must be used to represent an error.
    """
    def __init__(self, error_constant, *fields, message=None):
        self.error_constant = error_constant or ErrorCode.NON_STANDARD_ERROR
        self.fields = tuple(fields)
        self.message = message

    @property
    def to_dict(self):
        self.fields = tuple(itertools.chain(*map(lambda field: field.split(config['FIELDS_SEPARATOR'])[1::] if config['FIELDS_SEPARATOR'] in field else field.split(config['FIELDS_SEPARATOR']), self.fields)))
        err_dict = dict(error_constant = self.error_constant)
        if self.fields: err_dict['fields'] = self.fields
        if self.message: err_dict['message'] = self.message
        return err_dict

class BaseException(Exception):
    """
    Base class for custom exceptions.
    Subclasses should provide `status_code`, `message` and `errors` properties.
    """
    status_code = 500
    message = 'A server error occurred.'
    errors = []

    def __init__(self, message=None, status_code=500, errors=()):
        self.status_code = status_code
        self.errors = errors
        if message: self.message = message

    def __str__(self):
        return "Error({}): {}".format(self.status_code, self.message)

class DatabaseException(BaseException):
    message = 'Error occurred while performing DB operation.'
    def __init__(self, message=None, status_code=400, errors=()):
        super(DatabaseException, self).__init__(message=message, status_code=400, errors=errors)

class SqlAlchemyException(DatabaseException):
    message = 'Error occurred while performing an operation on RDBMS.'
    def __init__(self, message=None, status_code=400, errors=()):
        # from thirdparty import db
        # db.session.rollback()
        message = message or self.message
        super(SqlAlchemyException, self).__init__(message=message, status_code=status_code, errors=errors)

class NotFound(BaseException):
    message = 'Resource not found.'
    def __init__(self, message=None, errors=()):
        message = message or self.message
        super(NotFound, self).__init__(message=message, status_code=404, errors=errors)

class BadRequest(BaseException):
    message = 'Bad request.'
    def __init__(self, message=None, errors=()):
        message = message or self.message
        super(BadRequest, self).__init__(message=message, status_code=400, errors=errors)

class NotAuthenticated(BaseException):
    message = 'Authentication required.'
    def __init__(self, message=None, errors=()):
        message = message or self.message
        super(NotAuthenticated, self).__init__(message=message, status_code=401, errors=errors)

class Unauthrorized(BaseException):
    message = 'You are not authorized to perform this action.'
    def __init__(self, message=None, errors=()):
        message = message or self.message
        super(Unauthrorized, self).__init__(message=message, status_code=403, errors=errors)

class ExceptionBuilder(object):
    def __init__(self, exc_cls=BaseException):
        self._exc_cls = exc_cls
        self._errors = []
        self._message = ''
        self._code = None

    def error(self, error_constant, *fields, message=None):
        self._errors.append(Error(error_constant, *fields, message=message).to_dict)
        return self

    def message(self, msg):
        self._message = msg
        return self

    def status_code(self, code):
        self._code = code
        return self

    def throw(self):
        if self._code:
            raise self._exc_cls(errors=self._errors, message=self._message, status_code=self._code)
        else:
            raise self._exc_cls(errors=self._errors, message=self._message)


