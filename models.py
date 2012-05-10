import dictshield
from dictshield.document import diff_id_field
from dictshield.document import Document, EmbeddedDocument
from dictshield.fields.mongo import ObjectIdField
from dictshield.fields import (StringField, URLField, EmailField,
                                DateTimeField, UUIDField, IntField)

from dictshield.fields.compound import ListField, EmbeddedDocumentField
import datetime

from bson.objectid import ObjectId

class Link(EmbeddedDocument):
    title = StringField(required=True)
    url = URLField(required=True)

class User(Document):
    email = EmailField(required=True)

class Idea(Document):
    owner_id = UUIDField()
    short_desc = StringField(required=True)
    long_desc = StringField(required=True)
    use_cases = StringField(required=True)
    links = ListField(EmbeddedDocumentField(Link))
    likes_count = IntField(default=0)
    likes_list = ListField(StringField())
    tags_list = ListField(StringField())
    created_date = DateTimeField(required=True, default=datetime.datetime.now)
    updated_date = DateTimeField(default=datetime.datetime.now)