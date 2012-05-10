import pymongo
import bson

from model.queries import Link, User, Idea


##
##  Database name, database collections and collection indexes
##
DB_NAME = 'community_garden'
USER_COLLECTION = 'users'
indexes_users = [
    [('user_id', pymongo.ASCENDING)],
    [('user_email', pymongo.ASCENDING)]
]
IDEA_COLLECTION = 'ideas'
indexes_ideas = [
    [('owner_id', pymongo.ASCENDING)],
    [('owner_email', pymongo.ASCENDING)],
    [('idea_id', pymongo.ASCENDING)]
]


##
##  Methods to instantiate a database
##
def init_db_conn(**kwargs):
    dbc = pymongo.Connection(**kwargs)
    db_conn = dbc[DB_NAME]
    apply_all_indexes(db_conn, indexes_users, USER_COLLECTION)
    apply_all_indexes(db_conn, indexes_ideas, IDEA_COLLECTION)
    return db_conn

def end_request(db_conn):
    """Here as a visual reminder that this funciton must be called at the end
    of a request to return the socket back to pymongo's built-in thread pooling.
    """
    return db_conn.end_request()


def apply_all_indexes(db, indexes, collection):
    """Takes a list of indexes and applies them to a collection.

    Intended for use after functions that create/update/delete entire
    documents.
    """
    for index in indexes:
        db[collection].ensure_index(index)
    return True


##
##  Methods to save, load and update a user
##
def load_user(db, user_id=None):
    """Loads a user document from MongoDB.
    """
    query_dict = dict()
    if user_id:
        query_dict['user_id']
    else:
        raise ValueError('User_id required')

    user_dict = db[USER_COLLECTION].find_one(query_dict)

    if user_dict is None:
        return None
    else:
        u = User(**user_dict)
        return u

def save_user(db, user):
    """Saves a user document from MongoDB.
    """
    user_doc = user.to_python()
    uid = db[USER_COLLECTION].insert(user_doc)
    user._id = uid
    
    return uid


##
##  Methods to save, load and update an idea
##
def load_idea(db, idea_id=None):
    """Loads an idea document from MongoDB.
    """
    query_dict = dict()
    if idea_id:
        query_dict['idea_id']
    else:
        raise ValueError('Idea id required')

    idea_dict = db[IDEA_COLLECTION].find_one(query_dict)

    if idea_dict is None:
        return None
    else:
        i = Idea(**idea_dict)
        return i

def save_idea(db, idea):
    """Saves a user document from MongoDB.
    """
    idea_doc = idea.to_python()
    uid = db[IDEA_COLLECTION].insert(idea_doc)
    idea._id = uid
    
    return uid