require(["connection"]);

var cg = cg || {};

////

cg.hello_callback = function(message) {
    cg.log.to_el("hello_callback: " + message);
};
