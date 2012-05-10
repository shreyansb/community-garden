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
                     save_user,
                     load_user,
                     save_idea,
                     load_idea)

class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    def get_current_user(self):
        user_id = self.get_argument("user_id")
        if not user_id:
            # create a user
            return None
        return self.db.get()

class MainHandler(BaseHandler):
    def get(self):
        
    def post(self):


class IdeaHandler(BaseHandler):
    """Get a specific idea by id
    """
    def get(self):

    """Post a new idea to the database or update an existing idea
    """
    def post(self):
        idea_id = self.get_argument('idea_id', None)
        
        if not idea_id:
            return None
            
        idea_doc = load_idea(idea_id)
        
        if not idea_doc:
            self.create_idea(idea_id)
        else:
            self.update_idea(idea_doc)
    
    def update_idea(self, idea_doc):
        # If the user_id is the same as the owner_id, allow to update more things
        user_id = self.get_argument('user_id', None)
        tags = self.get_argument('tags', None)
        short_desc = self.get_argument('short_desc', None)
        long_desc = self.get_argument('long_desc', None)
        use_cases = self.get_argument('use_cases', None)    
    
    def create_idea(self):
        i = Idea()
        i.owner_id = self.get_argument('owner_id', None)
        i.owner_email = self.get_argument('owner_email', None)
        i.short_desc = self.get_argument('short_desc', None)
        i.long_desc = self.get_argument('long_desc', None)
        i.use_cases = self.get_argument('use_cases', None)
        i.tags = self.get_argument('tags', None)
        
        try:
            i.validate()
            print 'Validation passed\n'
        except Exception, e:
            logging.error('Item validation failed')
            logging.error(e)
            return self.render_error(500)
        
        save_idea(self.db_conn, i)
        return self.finish()
        
    
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


# self.db