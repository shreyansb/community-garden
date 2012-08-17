package main

import (
    "code.google.com/p/go.net/websocket"
    "log"
    "math/rand"
    "time"
)

type wsConnection struct {
	ws *websocket.Conn
	wsChan chan string
    id string
}

type wsMessage struct {
    Id string
    Message string
}

func wsHandler(ws *websocket.Conn) {
    // create a wsConnection instance
    wsConn := &wsConnection{
        ws: ws,
        wsChan: make(chan string),
        id: randomId(),
    }

    // receive a message and respond to it in a goroutine
    for {
        var message wsMessage
        err := websocket.JSON.Receive(wsConn.ws, &message)
        if err != nil {
            log.Printf("handleMessages Receive error: %v", err)
            break
        }
        go respondToMessage(wsConn, message)
    }
}

func respondToMessage(wsConn *wsConnection, message wsMessage) {
    /* Respond to an incoming message.
    Right now, simulates work by sleeping for a few seconds
    */
    log.Printf("%v is processing a message", wsConn.id)
    time.Sleep(time.Duration(rand.Int31n(5000)) * time.Millisecond)
    log.Printf("%v responded: %s", wsConn.id, message)
    bad_message := "haha"
    err := websocket.JSON.Send(wsConn.ws, bad_message)
    if err != nil {
        log.Printf("handleMessages Send error: %v", err)
        return
    }
}
