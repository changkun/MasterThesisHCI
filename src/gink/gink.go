package main

import (
	"net/http"
	"sync"

	"github.com/changkun/gink/api"
	"github.com/sirupsen/logrus"

	"github.com/gin-gonic/gin"
)

func main() {
	router := gin.Default()

	router.StaticFS("/tool", http.Dir("templates"))
	v1 := router.Group("/api/v1")
	{
		v1.GET("/ping", api.Pong)
		v1.GET("/path", api.PathFetcher)
		v1.POST("/node", api.SaveNode)
		v1.POST("/path", api.SaveActionPath)
	}

	var wg sync.WaitGroup

	wg.Add(1)
	go func() {
		defer wg.Done()
		if err := router.Run("0.0.0.0:12346"); err != nil {
			logrus.Error(err)
		}
	}()

	logrus.Info("Gink Labeling Tool is on: http://0.0.0.0:12346/tool")
	wg.Wait()
}
