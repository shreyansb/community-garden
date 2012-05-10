import pymongo
import bson

from models import Link, User, Idea

import logging


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
def get_user(db, user_id):
    """Loads a user document from MongoDB.
    """
    spec = {"_id":user_id}
    
    user_dict = db[USER_COLLECTION].find_one(spec)

    if user_dict:
        user = User(**user_dict)
        return user
    else:
        return None

def create_or_update_user(db, user):
    """Saves a user document from MongoDB.
    """
    user_doc = user.to_python()
    # remove Nones
    spec = {"_id":user.id}
    db[USER_COLLECTION].insert(spec, document= {'$set':user_doc}, upsert=True, safe=True)
    return user

##
##  Methods to save, load and update an idea
##
def get_idea(db, idea_id):
    """Loads an idea document from MongoDB.
"""
    spec = {"_id":idea_id}
    
    idea_dict = db[IDEA_COLLECTION].find_one(spec)
    
    logging.info("Getting idea from the database", "*"*100)

    if idea_dict:
        idea = Idea(**idea_dict)
        logging.info("Idea_dict:", "*"*100)
        logging.info("Idea_dict:", idea.to_python())
        return idea
    else:
        return None


def create_or_update_idea(db, idea):
    """Saves a user document from MongoDB.
    """
    idea_doc = idea.to_python()
    idea_add_to_set_keys = ['tags_list', 'likes_list']
    
    set_doc = {}
    add_to_set_doc = {} 
    
    for key, value in idea_doc.iteritems():
        if key in idea_add_to_set_keys:
            if value:
                add_to_set_doc[key] = value
        else:
            if value:
                set_doc[key] = value
    
    spec = {"_id":idea.id}
    db[IDEA_COLLECTION].update(spec, document={'$set':set_doc, '$addToSet':add_to_set_doc}, upsert=True, safe=True)
    return idea