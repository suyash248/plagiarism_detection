__author__ = "Suyash Soni"
__email__ = "suyash.soni248@gmail.com"

import json
from model.base import BaseModel
from mysql_connector import db

class Document(BaseModel):
    __tablename__ = 'documents'

    content = db.Column('content', db.Text(), nullable=False)
    title = db.Column('title', db.String(200), nullable=False)
    description = db.Column('description', db.Text(), nullable=True)
    author = db.Column('author', db.String(200), nullable=True)

    # Table metadata can be specified as follows -
    __table_args__ = (
        db.UniqueConstraint('title', 'is_deleted'),
        db.Index(BaseModel.create_index(__tablename__, 'title', 'is_deleted'), 'title', 'is_deleted'),
    )

    def __str__(self):
        return self.title

    def __repr__(self):
        return json.dumps(self.to_dict())

    def to_dict(self, *args, **kwargs):
        return {
            'id': self.id,
            'author': self.author,
            'title': self.title,
            'description': self.description,
            'content': self.content
        }