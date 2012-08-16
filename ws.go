package main

import (
	"code.google.com/p/go.net/websocket"
    "crypto/sha256"
    "encoding/base64"
    "log"
    "time"
)

type wsConnection struct {
	ws *websocket.Conn
	wsChan chan string
    id string
}

func wsHandler(ws *websocket.Conn) {
    // create a wsConnection instance
    wsConn := &wsConnection{
        ws: ws,
        wsChan: make(chan string),
        id: randomId(),
    }
    // handle incoming messages from the websocket
    handleMessages(wsConn)
}

func handleMessages(wsConn *wsConnection) {
    for {
        var message string
        err := websocket.Message.Receive(wsConn.ws, &message)
        if err != nil {
            log.Printf("handleMessages Receive error: %v", err)
            break
        }
        go respondToMessage(wsConn, message)
    }
}

func respondToMessage(wsConn *wsConnection, message string) {
    log.Printf("%v is processing a message", wsConn.id)
    time.Sleep(10000 * time.Millisecond)
    log.Printf("%v responded: %s", wsConn.id, message)
    err := websocket.Message.Send(wsConn.ws, message)
    if err != nil {
        log.Printf("handleMessages Send error: %v", err)
        return
    }
}

func randomId() string {
    /* generates a random id based on the sha256 of the current time
    there's probably a better way to generate ids
    */
    hasher := sha256.New()
    hasher.Write([]byte((time.Now()).String()))
    return string(base64.URLEncoding.EncodeToString(hasher.Sum(nil)))
}
