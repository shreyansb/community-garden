package main

import (
	"code.google.com/p/go.net/websocket"
	"fmt"
	"log"
)

const (
	// Types of incoming messages
	MESSAGE_TYPE_GET         = 1
	MESSAGE_TYPE_POST        = 2
	MESSAGE_TYPE_PUT         = 3
	MESSAGE_TYPE_DELETE      = 4
	MESSAGE_TYPE_SUBSCRIBE   = 11
	MESSAGE_TYPE_UNSUBSCRIBE = 12
	// Response codees, mapping to HTTP codes
	RESPONSE_TYPE_SUCCESS   = 200
	RESPONSE_TYPE_NOT_FOUND = 404
	RESPONSE_TYPE_ERROR     = 500
)

var (
	messageTypes = map[int]string{
		MESSAGE_TYPE_GET:         "get",
		MESSAGE_TYPE_POST:        "post",
		MESSAGE_TYPE_PUT:         "put",
		MESSAGE_TYPE_DELETE:      "delete",
		MESSAGE_TYPE_SUBSCRIBE:   "subscribe",
		MESSAGE_TYPE_UNSUBSCRIBE: "unsubscribe",
	}
	routes = map[string]func(*wsConnection, *wsMessage) wsResponse{
		"get:user": getUserHandler,
	}
)

type wsConnection struct {
	ws     *websocket.Conn
	wsChan chan string
	id     string
}

// incoming websocket message
type wsMessage struct {
	MessageType int
	Id          string
	Resource    string
	Params      string
}

// outgoing websocket message
type wsResponse struct {
	ResponseType int
	Id           string
	Response     string
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

func parseAndProcessMessage(wsConn *wsConnection, message *wsMessage) wsResponse {
	/*
	 */
	messageTypeString := messageTypes[message.getMessageType()]
	resource := message.getResource()
	route := fmt.Sprintf("%s:%s", messageTypeString, resource)
	return routes[route](wsConn, message)
}

///
/// methods that operate on a *wsMessage
///

func (message *wsMessage) getId() string {
	return (*message).Id
}
func (message *wsMessage) getMessageType() int {
	return (*message).MessageType
}
func (message *wsMessage) getResource() string {
	return (*message).Resource
}
func (message *wsMessage) getParams() string {
	return (*message).Params
}
