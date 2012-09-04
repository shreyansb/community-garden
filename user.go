package main

import (
	"log"
)

type User struct {
	Id   int
	Name string
}

func getUserHandler(wsConn *wsConnection, message *wsMessage) wsResponse {
	response := wsResponse{RESPONSE_TYPE_SUCCESS, message.getId(), "User: Shreyans Bhansali"}
	params := message.getParams()
	log.Printf("params as a string: %s", params)
	return response
}
