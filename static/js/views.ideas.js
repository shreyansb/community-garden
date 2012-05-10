// The view for a single idea, always editable
cg.views.IdeaView = Backbone.View.extend({

    el: "#content",

    template: _.template($('#idea-template').html()),

    events: {
        'click .save'       : 'save',
    },

    initialize: function() {
        // re-render the view when the model changes
        this.model.bind('change', this.render, this); 
        this.render();
    },

    render: function() {
        this.$el.html(
            this.template({item:this.model}));
                //this.model.toJSON()))
        return this;
    },

    save: function() {
        // TODO: validation
        this.model.save()
    }

});
