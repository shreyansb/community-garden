package main

import (
	"encoding/json"
	"fmt"
	"labix.org/v2/mgo/bson"
	"log"
)

type User struct {
	Id        int
	FirstName string
	LastName  string
	Email     string
}

type getUserParams struct {
	Id int
}

///
/// User handlers
///

func getUserHandler(wsConn *wsConnection, message *wsMessage) wsResponse {
	var getUserParams getUserParams
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
	response := wsResponse{RESPONSE_TYPE_SUCCESS, message.getId(), user.Id}
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
	firstName, _ := redisConn.Hget(keyString, "firstName")
	lastName, _ := redisConn.Hget(keyString, "lastName")
	email, _ := redisConn.Hget(keyString, "email")
	user := User{id, string(firstName), string(lastName), string(email)}

	mongoUser := User{}
	c := mongoClient.DB("cg").C("users")
	err := c.Find(bson.M{"id": id}).One(&mongoUser)
	if err != nil {
		log.Printf("couldn't find user: ", err)
	} else {
		log.Printf("mongo user: %v", mongoUser)
	}

	return user, nil
}

func createUser(user User) error {
	keyString := fmt.Sprintf("user:%d", user.Id)
	redisConn.Hset(keyString, "firstName", []byte(user.FirstName))
	redisConn.Hset(keyString, "lastName", []byte(user.LastName))
	redisConn.Hset(keyString, "email", []byte(user.Email))

	c := mongoClient.DB("cg").C("users")
	err := c.Insert(&user)
	if err != nil {
		log.Printf("couldn't save user to db: ", err)
	}
	return nil
}
