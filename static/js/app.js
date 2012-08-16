var cg = cg || {};

cg.socket = new WebSocket("ws://" + window.ws_host + "/ws");

cg.socket.onopen = function () {
    console.log("connection opened");
};
cg.socket.onmessage = function (event_) {
    console.log("message: ");
    console.log(event_.data);
};
cg.socket.onclose = function () {
    console.log("connection closed");
}
