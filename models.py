from dictshield.document import (Document, 
                                 EmbeddedDocument)
from dictshield.fields import (StringField, 
                               URLField, 
                               DateTimeField, 
                               UUIDField, 
                               IntField)
from dictshield.fields.compound import (ListField,
                                        EmbeddedDocumentField)
import datetime

class Link(EmbeddedDocument):
    title = StringField(required=True)
    url = URLField(required=True)

class User(Document):
    pass

class Idea(Document):
    _public_fields = ['owner_id', 'short_desc', 'long_desc', 'use_cases',
                      'links', 'likes_count', 'likes_list', 'tags_list', 
                      'created_date', 'updated_date']
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
