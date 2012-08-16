package main

import (
    "code.google.com/p/go.net/websocket"
    "crypto/sha256"
    "encoding/base64"
    "log"
    "math/rand"
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

    // receive a message and respond to it in a goroutine
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
    /* Respond to an incoming message.
    Right now, simulates work by sleeping for a few seconds
    */
    log.Printf("%v is processing a message", wsConn.id)
    time.Sleep(time.Duration(rand.Int31n(5000)) * time.Millisecond)
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
