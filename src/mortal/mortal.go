package main

import (
	"github.com/changkun/mortal/api"
	"github.com/gin-gonic/gin"
)

func main() {
	router := gin.Default()
	v1 := router.Group("/api/v1")
	{
		v1.POST("/collect", api.Recv)
	}
	println("start on: http://0.0.0.0:12346")
	router.Run(":12346")
}
