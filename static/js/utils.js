var cg = cg || {};
cg.log = cg.log || {};
cg.format = cg.format || {};

cg.random_id = function() {
    var S4 = function() {
        return (((1+Math.random())*0x10000)|0).toString(16).substring(1);
    };
    return (S4()+S4()+S4()+S4());
};

///
/// logging
///

cg.log.to_el = function(message) {
    var el = document.getElementById(cg.connection_el_id);
    var log_el = document.createElement("div");
    log_el.innerHTML = message;
    el.appendChild(log_el);
};

///
/// format
///

cg.format.to_string = function(message) {
    for (var i = 0; i < message.length; i++) {
        message[i] = message[i].toString();
    }
    return message;
};

