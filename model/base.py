__author__ = "Suyash Soni"
__email__ = "suyash.soni248@gmail.com"

from uuid import uuid4
from mysql_connector import db
from settings import config
from sqlalchemy.orm import class_mapper
from sqlalchemy.orm import ColumnProperty

def generate_uuid():
    """
    :return: Random UUID4 String.
    """
    return str(uuid4())


class BaseModel(db.Model):
    """
    `BaseModel` for providing common-fields for audit & trail, to child models.
    """
    __abstract__ = True

    id = db.Column("id", db.String(75), primary_key=True, default=generate_uuid)
    created_date = db.Column(db.DateTime, default=db.func.now())
    updated_date = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    # Soft-delete, 0 means that record is NOT deleted, any UTC timestamp value(>0) means
    # record is deleted at that UTC time.
    is_deleted = db.Column(db.Integer, default=0)

    def to_dict(self, *args, **kwargs):
        raise NotImplementedError("All the models must implement to_dict")

    @classmethod
    def field_names(cls):
        return [prop.key for prop in class_mapper(cls).iterate_properties if isinstance(prop, ColumnProperty)]

    @classmethod
    def column_names(cls):
        return cls.__table__.columns.keys()

    @staticmethod
    def create_index(tablename, *cols, **kwargs):
        """
        Used for to create index, index name will be in following format -

            - col1{SEPARATOR}col2{SEPARATOR}...{SEPARATOR}colN

        :param tablename: Target table.
        :param cols: column names which will be part of the index.

        :return: Name of the index.
        """
        return ''.join([tablename] + ['{sep}' + col for col in cols]).format(
            sep=config['FIELDS_SEPARATOR']
        )