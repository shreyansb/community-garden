// The view for the homepage, which is a list of ideas
// and a search bar at the top
cg.views.HomepageView = Backbone.View.extend({

    el: "#content",

    ulEl: "#idea_list_ul",

    template: _.template($('#homepage-template').html()),

    events: {
        'click #new_idea'           : 'loadIdeaById'
    },

    initialize: function(options) {
        console.log("HomepageView::initialize");
        _.bindAll(this, 'render', 
                        'renderEach', 
                        'notifyParent',
                        'loadIdeaById');
    },

    render: function(ideas) {
        console.log("HomepageView::render");
        //// the code below is what you use when you are actually
        //// using fetch, not dummy data
        //// it uses a deferred, and when the loading is done, it
        //// calls renderEach on each model in the collection
        var fetching = cg.ideas.fetch();
        this.$el.html(
                this.template());
        this.$(this.ulEl).empty();
        var _this = this;
        fetching.then(function() {
            cg.ideas.each(_this.renderEach);
        });
        cg.app.navigate("");
        //cg.ideas.each(this.renderEach);
        return this;
    },

    renderEach: function(idea) {
        console.log("HomepageView::renderEach");
        // `idea` is a model in the collection
        // for each model, create a IdeaListItemView
        var item = new cg.views.IdeaListItemView({model:idea});
        // listen for the child firing off the 'click' event
        // if caught, call notifyParent
        item.on('clickIdea', this.notifyParent);
        // render the subview and append it to this view
        var item_html = item.render().el;
        this.$(this.ulEl).append(item_html);
    },

    notifyParent: function(child_model) {
        console.log("HomepageView::notifyParent");
        // now this view also triggers an event for its parent (the router)
        // to handle. pass the attribute received along
        this.trigger('clickIdea', child_model);
    },

    loadIdeaById: function() {
        console.log("HomepageView::loadIdeaById");
        this.trigger('clickNew');
    },

    backToHome: function() {
        console.log("HomepageView::backToHome");
        this.trigger('backToHome');
    }
});

// Each of these is an item in the list
cg.views.IdeaListItemView = Backbone.View.extend({
    
    tagName: 'li',

    template: _.template($('#idea-list-item-template').html()),

    events: {
        'click'         : 'goToIdea'
    },

    initialize: function() {
        _.bindAll(this, 'render', 'goToIdea');
    },

    render: function() {
        console.log("IdeaListItemView::render");
        var item_html = this.template(this.model.toJSON());
        this.$el.html(item_html);
        return this;
    },

    goToIdea: function() {
        console.log("IdeaListItemView::goToIdea");
        // trigger an event that the parent of this view will be listening for
        // pass this model along
        this.trigger('clickIdea', this.model);
    }

});
