__author__ = "Suyash Soni"
__email__ = "suyash.soni248@gmail.com"

class SingletonMeta(type):
    """
    Metaclass to implement **Single design pattern**.

    Usage: Can be used in following ways while defining a class -

        * `class SomeClass(BaseClass, metaclass=Singleton):`
        * `class SomeClass(metaclass=Singleton):`
    """

    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]