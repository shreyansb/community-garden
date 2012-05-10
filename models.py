import dictshield
from dictshield.document import diff_id_field
from dictshield.document import Document
from dictshield.fields.mongo import ObjectIdField
from dictshield.fields import (StringField, URLField, EmailField,
ListField, DateTimeField, UUIDField, ObjectIDField, IntField, EmbeddedDocumentField)

from bson.objectid import ObjectId

class Link(EmbeddedDocument):
    title = StringField(required=True)
    url = URLField(required=True)

class User(EmbeddedDocument):
    user_email = EmailField(required=True)
    ideas_owned = ListField(EmbeddedDocument(Idea))
    ideas_liked = ListField(EmbeddedDocument(Idea))
    ideas_contributed_to = ListField(EmbeddedDocument(Idea))
    ideas_touched = ListField(EmbeddedDocument(Idea))
    user_id = UUIDField()

class Idea(Document):
    owner = EmbeddedDocumentField(User)
    short_desc = StringField(required=True)
    long_desc = StringField(required=True)
    use_cases = StringField(required=True)
    links = ListField(EmbeddedDocumentField(Link))
    likes_count = IntField(default=0)
    likes_list = ListField(StringField())
    tags = ListField(StringField())
    created_date = DateTimeField(required=True, default=datetime.datetime.now)
    updated_date = DateTimeField(default=datetime.datetime.now)
    idea_id = UUIDField()