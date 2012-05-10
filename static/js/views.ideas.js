// The view for a single idea, always editable
cg.views.IdeaView = Backbone.View.extend({

    el: "#content",

    template: _.template($('#idea-template').html()),

    events: {
        'click #save'       : 'save',
    },

    initialize: function() {
        // re-render the view when the model changes
        this.model.bind('change', this.render, this); 
        this.render();
    },

    render: function() {
        console.log("IdeaView::render");
        // we pass the model in here because we want to call functions
        // on it, like item.owned_by_current_user();
        this.$el.html(
            this.template({item:this.model}));
        return this;
    },

    save: function() {
        console.log("IdeaView::save");
        // TODO: validation
        console.log(this.model);
        this.model.save();
    }

});
