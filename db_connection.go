package main

import (
	redis "github.com/alphazero/Go-Redis"
	"log"
)

var (
	redisSpec  = redis.DefaultSpec()
	redisConn  redis.Client
	redisError interface{}
)

func setupRedisConnection() {
	redisConn, redisError = redis.NewSynchClientWithSpec(redisSpec)
	if redisError != nil {
		log.Fatal("couldn't connect to redis: ", redisError)
	}
}
