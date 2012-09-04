package main

import (
	"code.google.com/p/go.net/websocket"
	"log"
)

type wsConnection struct {
	ws     *websocket.Conn
	wsChan chan string
	id     string
}

// incoming websocket message
type wsMessage struct {
    MessageType int
    Message string
	Id      string
}

// outgoing websocket message
type wsResponse struct {
    ResponseType int
    Response string
    Id string
}

func wsHandler(ws *websocket.Conn) {
	// create a wsConnection instance
	wsConn := &wsConnection{
		ws:     ws,
		wsChan: make(chan string),
		id:     randomId(),
	}

	// receive a message and respond to it in a goroutine
	for {
		var message wsMessage
		err := websocket.JSON.Receive(wsConn.ws, &message)
		if err != nil {
			log.Printf("handleMessages Receive error: %v", err)
			break
		}
		go respondToMessage(wsConn, &message)
	}
}

func respondToMessage(wsConn *wsConnection, message *wsMessage) {
	/* Respond to an incoming message.
	   Right now, simulates work by sleeping for a few seconds
	*/
    log.Printf("%v received: %v", wsConn.id, *message)
    response := parseAndProcessMessage(wsConn, message)
	log.Printf("%v responded: %v", wsConn.id, response)
	err := websocket.JSON.Send(wsConn.ws, response)
	if err != nil {
		log.Printf("handleMessages Send error: %v", err)
		return
	}
}

func parseAndProcessMessage(wsConn *wsConnection, message *wsMessage) (wsResponse) {
    response_json := "response json"
    response := wsResponse{82, response_json, message.getId()}
    return response
}

///
/// methods that operate on a *wsMessage
///

func (message *wsMessage) getId() (string) {
    return (*message).Id
}

