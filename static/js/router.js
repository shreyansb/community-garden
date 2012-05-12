////
//// Router
////

cg.controllers.IdeaRouter = Backbone.Router.extend({

    routes: {
        "new"               : "newIdea",
        ":idea_id"          : "loadIdeaById",
        ""                  : "homepage"
    },

    initialize: function() {
        console.log("IdeaRouter::initializing");

        cg.userId = cg.utils.getOrSetUserId();

        _.bindAll(this, 'homepage',
                        'newIdea',
                        'renderIdea',
                        'loadIdeaFromModel', 
                        'loadIdeaById');

        var dummy_data = [  {'short_desc':'one', 
                                'long_desc':'airbnb for moms', 
                                'id':1,
                                'owner_id': '624f6593-1d1c-b266-4713-01414d12bca3'
                            }, 
                            {'short_desc':'two', 
                                'long_desc':'airbnb for your mom', 
                                'id':2,
                                'tags': 'airbnb, mom',
                                'owner_id': 'asdfasfasfd'
                            }]

        cg.ideas = new cg.collections.IdeaList(dummy_data);
        cg.views.homepage = new cg.views.HomepageView();
        // listen for the homepage view firing off a `click` event
        // and call a function to render the idea view
        cg.views.homepage.on('clickIdea', this.renderIdea, this);
        cg.views.homepage.on('clickNew', this.newIdea, this);
        ////use this when not using dummy data
        //cg.ideas = new cg.collections.IdeaList();
    },

    homepage: function() {
        console.log("IdeaRouter::homepage");
        // set the content of this view's el
        // by calling render on the view
        cg.views.homepage.render();
        //$(this.el).html(cg.views.homepage.render().el);
    },

    newIdea: function() {
        console.log("IdeaRouter::newIdea");
        var idea = new cg.models.Idea({owner_id:cg.userId});
        cg.views.newIdea = new cg.views.IdeaView({model:idea});
        cg.views.newIdea.on("clickBackToHome", this.homepage);
    },
    
    loadIdeaById: function(idea_id) {
        console.log("IdeaRouter::loadIdeaById");
        var idea = cg.ideas.get(idea_id);
        if (!idea)
            idea = new cg.models.Idea(idea_id);
        cg.views.newIdea = new cg.views.IdeaView({model:idea});
        cg.views.newIdea.on("clickBackToHome", this.homepage);
    },

    loadIdeaFromModel: function(idea) {
        console.log("IdeaRouter::loadIdeaFromModel");
        cg.views.newIdea = new cg.views.IdeaView({model:idea});
        cg.views.newIdea.on("clickBackToHome", this.homepage);
    },

    renderIdea: function(child_model) {
        console.log("IdeaRouter::renderIdea");
        //this.navigate(child_model.attributes.id.toString());
        this.loadIdeaFromModel(child_model);
    }

});
