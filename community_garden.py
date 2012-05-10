import os
import re
import tornado
import tornado.httpserver
import tornado.autoreload
import tornado.escape
import tornado.httpclient
import tornado.ioloop
import tornado.web
import simplejson as json
import logging
import uuid

from queries import (init_db_conn,
                     create_or_update_user,
                     get_user,
                     create_or_update_idea,
                     get_idea)
from models import (User,
                    Idea)

class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db
    
    def get_current_user(self):
        # First see if user_id exists
        user_id = self.get_argument('user_id', None)
        user_email = self.get_argument('user_email', None)
        
        user = get_user(self.db, user_id)
        
        # Add user if it doesn't exist
        if not user:
            user = self.add_new_user(user_id, user_email)
        return user
        
    def add_new_user(self, user_id, user_email):
        u = User()
        u.id = user_id
        u.email = user_email
        
        try:
            u.validate()
            print 'Validation passed\n'
        except Exception, e:
            logging.error('Item validation failed')
            logging.error(e)
            return self.render_error(500)
        
        user = create_or_update_user(self.db, u)
        return user

class MainHandler(BaseHandler):
    def get(self):
        return None
        
    def post(self):
        return None

class IdeaHandler(BaseHandler):
    """Get a specific idea by id
    """
    def get(self):
        return None
    """Post a new idea to the database or update an existing idea
    """
    def post(self):
        logging.info("Posting an idea")
        
        idea_id = self.get_argument('idea_id', None)
        
        if not idea_id:
            logging.error('Item validation failed')
            logging.error(e)
            return self.render_error(500)
            
        idea = get_idea(self.db, idea_id)
        
        if not idea:
            response = self.create_idea(idea_id)
        else:
            response = self.update_idea(idea)

        self.write(response)
        self.finish()
    
    def update_idea(self, idea_doc):
        logging.info("Updating an idea")
        # If the user_id is the same as the owner_id, allow to update more things
        
    
    
    def create_idea(self, idea_id):
        logging.info("Creating an idea")
        
        user = self.get_current_user()
        
        i = Idea()
        i.id = idea_id
        i.owner_id = user.id
        i.short_desc = self.get_argument('short_desc', None)
        i.long_desc = self.get_argument('long_desc', None)
        i.use_cases = self.get_argument('use_cases', None)
        i.tags_list = self.get_arguments('tags', None)
        
        try:
            i.validate()
            print 'Validation passed\n'
        except Exception, e:
            logging.error('Item validation failed')
            logging.error(e)
            return self.render_error(500)
        
        response = create_or_update_idea(self.db, i)
        print "response", response.to_python()
        return response
        
    
settings = {
    'debug': True, # enables automatic reruning of this file when edited
    'static_path': os.path.join(os.path.dirname(__file__), "static")
}

# Instantiate database connection
db_conn = init_db_conn()

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/idea", IdeaHandler)
    ],  
     **settings) 
application.db = db_conn


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(9001)
    tornado.ioloop.IOLoop.instance().start()
