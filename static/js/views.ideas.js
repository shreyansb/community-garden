// The view for a single idea, always editable
cg.views.IdeaView = Backbone.View.extend({

    el: "#content",

    template: _.template($('#idea-template').html()),

    events: {
        'click #save'                   : 'save',
        'click #back_to_home_button'    : 'backToHome',
        'blur #item_short_desc'         : 'updateModel',
        'blur #item_long_desc'          : 'updateModel',
        'blur #item_use_cases'          : 'updateModel',
        'blur #item_tags'               : 'updateModel'
    },

    initialize: function() {
        console.log("IdeaView::initialize");
        // re-render the view when the model changes
        this.model.bind('change', this.render, this); 
        this.render();
    },

    render: function() {
        console.log("IdeaView::render");
        this.setHash();
        // we pass the model in here because we want to call functions
        // on it, like item.owned_by_current_user();
        this.$el.html(
            this.template({item:this.model}));
        return this;
    },

    save: function() {
        console.log("IdeaView::save");
        console.log(this.model);
        this.model.save();
    },

    backToHome: function() {
        console.log("IdeaView::backToHome");
        this.trigger('clickBackToHome')
    },

    setHash: function() {
        console.log("IdeaView::setHash");
        var current_id = this.model.get('id');
        if (current_id)
            current_id = current_id.toString();
        else
            current_id = 'new'
        cg.app.navigate('/' + current_id);
    },

    updateModel: function(event) {
        console.log("IdeaView::updateModel");
        var updatedEl = event.target.id;
        var updatedVal = $('#' + updatedEl).val();
        this.model.set(updatedEl, updatedVal);
    }

});
