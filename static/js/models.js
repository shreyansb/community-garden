////
//// Model
////

cg.models.Idea = Backbone.Model.extend({
    
    urlRoot: '/ideas',

    owned_by_current_user: function() {
        console.log("Idea::owned_by_current_user");
        return (this.get('owner_id') === cg.userId);
    }

});
