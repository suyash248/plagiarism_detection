__author__ = "Suyash Soni"
__email__ = "suyash.soni248@gmail.com"

class Injectable(object):
    """
    Injects a class in another class.

    Usage::
        * service_obj = Injectable('my_package.my_services.MyService', "arg1", "some_arg", kw1="val1").inject
        * service_obj = Injectable(MyService, "arg1", "some_arg", kw1="val1").inject
    """
    def __init__(self, injectable_class, *args, **kwargs):
        self.injectable_class = injectable_class
        self.args = args
        self.kwargs = kwargs

    @property
    def inject(self):
        return inject(self.injectable_class, *self.args, **self.kwargs)

def inject(injectable_class, *args, **kwargs):

    """
    :param injectable_class: Either fully qualified name of **injectable_class**. i.e. `my_module.some_pkg.SomeService`
                                or type of class
    :param args: Arguments required to instantiate **injectable_class**, as defined under `__init__` of **injectable_class**.
    :param kwargs: Keyword args required to instantiate **injectable_class**, as defined under `__init__` of **injectable_class**.
    :return: An instance of **injectable_class**

    Injects the **injectable_class** inside a another class.

    Usage::
        * service_obj = inject('my_package.my_services.MyService', "arg1", "some_arg", kw1="val1")
        * service_obj = inject(MyService, "arg1", "some_arg", kw1="val1")

    """
    if type(injectable_class) == str:
        from util.commons import load_class
        injectable_class = load_class(injectable_class)
    return getattr(injectable_class, 'instance')(*args, **kwargs)
