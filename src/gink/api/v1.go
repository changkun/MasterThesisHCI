package api

import (
	"net/http"

	"github.com/changkun/gink/models"
	"github.com/changkun/gink/settings"
	"github.com/gin-gonic/gin"
)

// Pong .
func Pong(c *gin.Context) {
	c.JSON(http.StatusOK, &PingOutput{
		Message: "pong",
		Version: settings.Version,
	})
}

// consts
const (
	minLength = 3
	maxTry    = 10
	entry     = "http://www.medien.ifi.lmu.de"
)

// PathFetcher .
func PathFetcher(c *gin.Context) {

	var (
		nodes    []models.Node
		err      error
		recorded bool
	)
	recorded = false
	for i := 0; i < maxTry; i++ {
		nodes, err = models.FindActionPath(minLength, entry)
		if err != nil {
			continue
		}
		if recorded = models.IsActionPathRecorded(nodes); recorded {
			continue
		}
		break
	}

	if recorded {
		c.JSON(http.StatusBadRequest, &NodesOutput{
			Message: "Fail to get action path",
			Nodes:   nil,
		})
		return
	}

	c.JSON(http.StatusOK, &NodesOutput{
		Message: "Featch action path success",
		Nodes:   nodes,
	})

}

// SaveNode .
func SaveNode(c *gin.Context) {
	input := SaveNodeInput{}
	if err := c.ShouldBindJSON(&input); err != nil {
		c.JSON(http.StatusBadRequest, &SaveNodeOutput{
			Message: "wrong structure err: " + err.Error(),
		})
		return
	}
	if err := input.Save(); err != nil {
		c.JSON(http.StatusBadRequest, &SaveNodeOutput{
			Message: "database err: " + err.Error(),
		})
		return
	}
	c.JSON(http.StatusOK, &SaveNodeOutput{
		Message: "Saved.",
	})
}

// SaveActionPath .
func SaveActionPath(c *gin.Context) {
	input := SaveActionPathInput{}
	if err := c.ShouldBindJSON(&input); err != nil {
		c.JSON(http.StatusBadRequest, &SaveActionPathOutput{
			Message: "wrong structure err: " + err.Error(),
		})
		return
	}
	if err := input.Save(); err != nil {
		c.JSON(http.StatusBadRequest, &SaveActionPathOutput{
			Message: "database err: " + err.Error(),
		})
		return
	}
	c.JSON(http.StatusOK, &SaveActionPathOutput{
		Message: "Saved.",
	})
}
