__author__ = "Suyash Soni"
__email__ = "suyash.soni248@gmail.com"

from flask_restful import Resource
from util.injector import Injectable, inject

class BaseController(Resource):
    """
    Every controller must extend this class.
    """

    # Child controllers must override this property with default service for a specific module.
    __service_class__ = inject('service.base.BaseService')

    @property
    def service(self):
        """
        Returns an instance of service class(as defined under `__service_class__`. i.e. default service) to be used
        inside a controller. Usage inside controller's action methods::
            service_obj = self.service
        """
        if self.__service_class__ is None:
            raise NotImplementedError("Controller {} must override '__service_class__' property".format(self.__class__.__name__))
        return self.__service_class__.inject if isinstance(self.__service_class__, (Injectable)) else self.__service_class__