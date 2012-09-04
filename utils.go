package main

import (
	"crypto/rand"
	"fmt"
	"io"
)

func randomId() string {
	/* generate a 16 byte random string,
	   using the output of /dev/urandom 
	*/
	buf := make([]byte, 16)
	io.ReadFull(rand.Reader, buf)
	return fmt.Sprintf("%x", buf)
}
