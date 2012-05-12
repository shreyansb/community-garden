import requests
import uuid

from queries import init_db_conn, USER_COLLECTION, IDEA_COLLECTION

db = init_db_conn()

db[USER_COLLECTION].remove()
db[IDEA_COLLECTION].remove()

user_id = uuid.uuid4()
idea_id = uuid.uuid4()

url = 'http://localhost:9001/idea'
doc = {
        'id':idea_id,
        'user_id': user_id,
        'user_email': 'ashaegupta@gmail.com',
        'short_desc': 'Rooftop gardens',
        'long_desc': 'you get to go pet little furry things without picking up their poop',
        'use_cases': 'pet lovas who don\'t have time for pets',
        'tags': '["sillywilly","another item"]'
}

r = requests.post(url, data=doc)

db[USER_COLLECTION].count()
db[USER_COLLECTION].find_one()

db[IDEA_COLLECTION].count()
db[IDEA_COLLECTION].find_one()

doc = {
        'idea_id':idea_id,
        'user_id': user_id,
        'short_desc': 'Rooftop gardens and pools',
        'tags':'["green", "fresh air"]'
}

r = requests.post(url, data=doc)
spec = {'_id': idea_id}
idea_dict = db[IDEA_COLLECTION].find_one(spec)

from models import Idea
idea = Idea(**idea_dict)
print idea.to_python()
