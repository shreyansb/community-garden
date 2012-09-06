package main

import (
	redis "github.com/alphazero/Go-Redis"
	mongo "labix.org/v2/mgo"
	"log"
)

const (
	MONGO_CLIENT_URL = "localhost"
)

var (
	/// redis
	redisSpec  = redis.DefaultSpec()
	redisConn  redis.Client
	redisError redis.Error
	/// mongo
	mongoClient *mongo.Session
	mongoError  error
)

func setupRedisConnection() {
	log.Printf("connecting to redis...")
	redisConn, redisError = redis.NewSynchClientWithSpec(redisSpec)
	if redisError != nil {
		log.Fatal("couldn't connect to redis: ", redisError)
	}
	log.Printf("connected to redis.")
}

func setupMongoConnection() {
	log.Printf("connecting to mongo...")
	mongoClient, mongoError = mongo.Dial(MONGO_CLIENT_URL)
	if mongoError != nil {
		log.Fatal("couldn't connect to mongo: ", mongoError)
	}
	log.Printf("connected to mongo.")
}

func setupDBConnections() {
	go setupRedisConnection()
	go setupMongoConnection()
}

func closeDBConnections() {
	mongoClient.Close()
	log.Printf("closed mongo connection.")
}
