import os
import tornado
import tornado.httpserver
import tornado.autoreload
import tornado.escape
import tornado.httpclient
import tornado.ioloop
import tornado.web
import logging

from uuid import UUID, uuid4

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
        
        if user_id:
            user_id_UUID = UUID(user_id)
        else:
            user_id_UUID = uuid4()
        
        user = get_user(self.db, user_id_UUID)
        
        # Add user if it doesn't exist
        if not user:
            user = self.add_new_user(user_id)
        return user
        
    def add_new_user(self, user_id):
        u = User()
        u.id = user_id
        
        try:
            u.validate()
            print 'Validation passed\n'
        except Exception:
            raise tornado.web.HTTPError(400)
        
        user = create_or_update_user(self.db, u)
        return user
    
    def get_current_idea_if_exists(self, idea_id=None):
        
        idea_id_UUID = UUID(idea_id)
        
        # if there is no idea_id, return error
        if not idea_id:
            raise tornado.web.HTTPError(400)
            
        return get_idea(self.db, idea_id_UUID)
    
    def validate_and_write_idea(self, idea):
        try:
            idea.validate()
            print 'Validation passed\n'
        except Exception, e:
            raise tornado.web.HTTPError(400)

        response = create_or_update_idea(self.db, idea)
        return response
    

class MainHandler(BaseHandler):
    def get(self):
        return self.render('index.html')
        
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
        #import pdb; pdb.set_trace()
        print "Posting an idea", "*"*100
        
        idea_id = self.get_argument('idea_id', None)
        idea = self.get_current_idea_if_exists(idea_id)
        
        # If the idea does not already exists, create it, otherwise, update it
        if not idea:
            response = self.create_idea(idea_id)
        else:
            response = self.update_idea(idea)

        self.write(response)
        self.finish()
    
    def update_idea(self, idea):
        print "Updating an idea", "*"*100
        
        user = self.get_current_user()
        
        i = Idea()
        i.id = idea.id
        
        if user.id == idea.owner_id:
            i.short_desc = self.get_argument('short_desc', None)
            i.long_desc = self.get_argument('long_desc', None)
            i.use_cases = self.get_argument('use_cases', None)
        i.tags_list = self.get_argument('tags', None)
        # i.links = self.get_argument('links', None)
        return self.validate_and_write_idea(i)
    
    def create_idea(self, idea_id):
        
        user = self.get_current_user()
        
        i = Idea()
        i.id = idea_id
        i.owner_id = user.id
        i.short_desc = self.get_argument('short_desc', None)
        i.long_desc = self.get_argument('long_desc', None)
        i.use_cases = self.get_argument('use_cases', None)
        i.tags_list = self.get_arguments('tags', None)
        
        return self.validate_and_write_idea(i)
    
class LikeHandler(BaseHandler):

    def post(self):
        """Given an idea_id and a user_id, increase the 
        like count on the idea, if the user hasn't already
        liked it
        """
        user = self.get_current_user()
        idea = self.get_current_idea_if_exists()
        
        if not idea:
            raise tornado.web.HTTPError(400)
        
        if user.id not in idea.likes_list:
            idea.likes_list.append(user.id)
            idea.likes_count =+ 1
            self.validate_and_write_idea(idea)
            
        return idea.likes_count 

settings = {
    'debug': True, # enables automatic reruning of this file when edited
    'static_path': os.path.join(os.path.dirname(__file__), "static")
}

# Instantiate database connection
db_conn = init_db_conn()

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/idea", IdeaHandler),
    (r"/like", LikeHandler)
    ],  
     **settings) 
application.db = db_conn


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(9001)
    tornado.ioloop.IOLoop.instance().start()
