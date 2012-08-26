var cg = cg || {};

// a mapping of messages sent to the server, and 
// their associated callbacks
cg.connections = {};

// incoming messages from the server that don't have 
// :Id or :Message. We don't know how to deal with these
// might be useful for debugging
cg.failedIncomingMessages = {};

// a flag for whether the client is trying to reconnect
// after a broken connection. this prevents and infinite 
// loop of retry loops
cg.retryingConnection = false;

// called when a websocket connection is established
// aka 'readyState === 1'
cg.onopen = function () {
    console.log("connection opened");
};

// called when we receive an incoming message from the server
cg.onmessage = function (event_) {
    console.log("received message: " + event_.data);
    var incoming = JSON.parse(event_.data);
    if (incoming.Id && incoming.Message) {
        cg.connections[incoming.Id](incoming.Message);
    } else {
        var d = new Date();
        cg.failedIncomingMessages[d.toISOString()] = incoming;
    }
};

// called when the connection breaks. we only kick off a
// reconnect loop if we're not already in such a loop
cg.onclose = function () {
    console.log("connection closed");
    if (!cg.retryingConnection) {
        cg.retryConnection(0);
    }
};

// called when there's a connection error. 
cg.onerror = function() {
    console.log("connection error");
};

// create a websocket connection and set it up with
// event handlers
cg.connect = function() {
    cg.socket = new WebSocket("ws://" + window.ws_host + "/ws");
    cg.socket.onopen = cg.onopen;
    cg.socket.onclose = cg.onclose;
    cg.socket.onmessage = cg.onmessage;
    cg.socket.onerror = cg.onerror;
};

// called when a connection breaks. tries to reconnect,
// waits half a second, then calls a function that checks
// the state of the connection, and retries connection if 
// the connection did not succeed
cg.retryConnection = function(retryAttempt) {
    cg.retryingConnection = true;
    cg.connect();
    setTimeout(function() { 
        cg.checkConnection(retryAttempt); 
    }, 500);
}

// check the connection, and if it's still closed, retry,
// using an exponential backoff.
// Limited to 7 attempts.
cg.checkConnection = function(retryAttempt) {
    var retryAttempt = (typeof(retryAttempt) === "undefined") ? 0 : retryAttempt;
    var retryTime = Math.pow(2, retryAttempt) * 1000;
    if (cg.socket.readyState === 1) {
        console.log("reconnected");
        cg.retryingConnection = false;
    } else if (cg.socket.readyState === undefined || cg.socket.readyState > 1) {
        if (retryAttempt > 7) {
            console.log("done retrying. come back later");
        } else {
            console.log("nothing yet, will retry in " + retryTime + " ms");
            retryAttempt++;
            setTimeout(function() { 
                cg.retryConnection(retryAttempt); 
            }, retryTime);
        }
    }
};

// send a message, mark the connection id and callback function
// and send the message as a JSON string
cg.send_message = function(message, callback) {
    var message_id = cg.random_id();
    cg.connections[message_id] = callback;
    outgoing = {
        'Id': message_id,
        'Message': message
    }
    console.log(outgoing);
    cg.socket.send(JSON.stringify(outgoing));
};

cg.random_id = function() {
    var S4 = function() {
        return (((1+Math.random())*0x10000)|0).toString(16).substring(1);
    };
    return (S4()+S4()+S4()+S4());
};

cg.hello_callback = function(message) {
    console.log("hello_callback: " + message);
};

// start the first connection
cg.connect();
