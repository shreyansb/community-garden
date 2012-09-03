package main

import (
	"code.google.com/p/go.net/websocket"
	"flag"
	"html/template"
	"log"
	"net/http"
	"os"
	"runtime"
	"strings"
)

var (
	port           = flag.String("port", ":8080", "port")
	homeTemplate   = template.Must(template.ParseFiles("templates/home.html"))
	staticFilePath = "/static/"
	handlers       = map[string]func(http.ResponseWriter, *http.Request){
		"/":        homeHandler,
		"/static/": staticHandler,
	}
)

///
/// main
///

func main() {
	// set up a map of routes to handler functions
	// set up all handlers
	for route, handler := range handlers {
		http.HandleFunc(route, handler)
	}
	http.Handle("/ws", websocket.Handler(wsHandler))

	// start the server after getting either a user-entered or default :port
	flag.Parse()
	log.Printf("ListenAndServe: starting on localhost%s", *port)
	if err := http.ListenAndServe(*port, nil); err != nil {
		log.Fatal("ListenAndServe: ", err)
	}
}

///
/// handlers
///

func homeHandler(response http.ResponseWriter, request *http.Request) {
	// pass the `Host` so the app knows which websocket to connect to
	homeTemplate.Execute(response, request.Host)
}

func staticHandler(response http.ResponseWriter, request *http.Request) {
	cwd, err := os.Getwd()
	if err != nil {
		log.Fatal("staticHandler: ", err)
		panic(err)
	}
	filePath := cwd + staticFilePath + strings.SplitN(request.RequestURI, "/", 3)[2]
	http.ServeFile(response, request, filePath)
}
