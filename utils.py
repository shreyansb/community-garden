import datetime
import simplejson

ISO_8601_format = "%Y-%m-%dT%H:%M:%SZ"

def json_encode(data):
    def datetime_encoder(value):
        if isinstance(value, datetime.datetime):
            return datetime.datetime.strftime(value, ISO_8601_format)
    return simplejson.dumps(data, default=datetime_encoder)
