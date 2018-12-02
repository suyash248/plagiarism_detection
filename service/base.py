__author__ = "Suyash Soni"
__email__ = "suyash.soni248@gmail.com"

from util.singleton import SingletonMeta


class BaseService(object, metaclass=SingletonMeta):
    """
    Every service must extend this class. child classes will be **Singleton** by default.

    If child service overrides `__init__`, it should be made sure that parent's `__init__` method is called.
    example::

        Inside child service ->
        def __init__(self, arg1, arg2, kw1=12, kw2=23):
            super(ChildService, self).__init__(arg1, arg2, kw1=kw1, kw2=kw2)
            self.arg1 = arg1
            self.arg2 = arg2
            self.kw1 = kw1
            self.kw2 = kw2

    Child service classes can be used inside controllers as follows::
        * self.service - returns instance of default service as defined under **__service_class__** inside controller.
        * other_service_obj = self.inject("arg1", kw1="kw1val", service_class='my_package.my_services.OtherService')
    """
    def __init__(self, *args, **kwargs):
        from mysql_connector import db
        self.db = db

    @classmethod
    def instance(cls, *args, **kwargs):
        """
        Factory method to instantiate underlying concrete service class(`cls`).
        """
        return cls(*args, **kwargs)
