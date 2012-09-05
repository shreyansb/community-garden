package main

import (
	"encoding/json"
	"fmt"
	"log"
)

type User struct {
	Id   int
	Name string
}

type getUserParamsStruct struct {
	Id int
}

///
/// User handlers
///

func getUserHandler(wsConn *wsConnection, message *wsMessage) wsResponse {
	var getUserParams getUserParamsStruct
	paramBytes := message.getParamBytes()
	err := json.Unmarshal(paramBytes, &getUserParams)
	if err != nil {
		log.Printf("error decoding json: ", err)
	}
	user, err := getUserById(getUserParams.Id)
	if err != nil {
		return errorResponse(wsConn, message, "User not found")
	}
	return successResponse(wsConn, message, user)
}

func postUserHandler(wsConn *wsConnection, message *wsMessage) wsResponse {
	var user User
	paramBytes := message.getParamBytes()
	err := json.Unmarshal(paramBytes, &user)
	if err != nil {
		log.Printf("error decoding json: ", err)
	}
	if err := createUser(user); err != nil {
		log.Printf("error creating user: ", err)
	}
	log.Printf("posted User: %v", user)
	response := wsResponse{RESPONSE_TYPE_SUCCESS, message.getId(), "Posted"}
	return response
}

func subscribeUserHandler(wsConn *wsConnection, message *wsMessage) wsResponse {
	response := wsResponse{RESPONSE_TYPE_SUCCESS, message.getId(), "Subscribed"}
	return response
}

///
/// methods to access the datastore
///

func getUserById(id int) (User, error) {
	keyString := fmt.Sprintf("user:%d", id)
	userValue, err := redisConn.Hget(keyString, "name")
	log.Printf("redisResult: %v, %v", userValue, err)
	user := User{id, string(userValue)}
	return user, nil
}

func createUser(user User) error {
	keyString := fmt.Sprintf("user:%d", user.Id)
	redisConn.Hset(keyString, "name", []byte(user.Name))
	return nil
}
