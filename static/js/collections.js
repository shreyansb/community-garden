////
//// Collection
////

// initially backed by localstorage, eventually will talk to the server
cg.collections.IdeaList = Backbone.Collection.extend({
    
    url: '/idea',

    model: cg.models.Idea

});

//
// global collection of Ideas
// This will store 1 model if you land on an idea page
// and all the ideas that the user sees on the homepage
cg.Ideas = new cg.collections.IdeaList;
