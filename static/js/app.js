var cg = cg || {};

cg.socket = new WebSocket("ws://" + window.ws_host + "/ws");
cg.socket.connections = {};
cg.socket.failedIncomingMessages = {};

cg.socket.onopen = function () {
    console.log("connection opened");
};

cg.socket.onmessage = function (event_) {
    console.log("received message: " + event_.data);
    var incoming = JSON.parse(event_.data);
    if (incoming.Id && incoming.Message) {
        cg.socket.connections[incoming.Id](incoming.Message);
    } else {
        var d = new Date();
        cg.socket.failedIncomingMessages[d.toISOString()] = incoming;
    }
};

cg.socket.onclose = function () {
    console.log("connection closed");
}

cg.send_message = function(message, callback) {
    var message_id = cg.random_id();
    cg.socket.connections[message_id] = callback;
    outgoing = {
        'Id': message_id,
        'Message': message
    }
    console.log(outgoing);
    cg.socket.send(JSON.stringify(outgoing));
}

cg.random_id = function() {
    var S4 = function() {
        return (((1+Math.random())*0x10000)|0).toString(16).substring(1);
    };
    return (S4()+S4()+S4()+S4());
}

cg.hello_callback = function(message) {
    console.log("hello_callback: " + message);
}
