package api

import (
	"fmt"
	"net/http"

	"github.com/changkun/mortal/crawler"
	"github.com/changkun/mortal/db"
	"github.com/changkun/mortal/predictor"
	"github.com/gin-gonic/gin"
)

// CollectRequest defines the request of progressive clickstream collection
type CollectRequest struct {
	UserID      string  `json:"user_id" bson:"user_id"`
	PreviousURL string  `json:"previous_url" bson:"previous_url"`
	CurrentURL  string  `json:"current_url" bson:"current_url"`
	StaySeconds float64 `json:"stay_seconds,string" bson:"stay_seconds"`
	Time        string  `json:"time" bson:"time"`
}

// CollectResponse defines the response of progressive clickstream prediction
// - Message is a general message that indicates a human readable status of the message
// - Next returns all next possible urls that could be the next action of user
// - Destination returns all possible destination urls that the user may terminate the accessing
// - Productivity returns the current productivity of the user at the moment
type CollectResponse struct {
	Message      string            `json:"message"`
	Next         *[]predictor.Jump `json:"next"`
	Destinations *[]predictor.Jump `json:"destination"`
	Productivity int               `json:"productivity"` // 0 to 100
}

// Save ...
func (c *CollectRequest) Save() {
	// if domain not exit in database, explore the website
	if db.IsDomainExist(c.CurrentURL) {
		crawler.Explore(c.CurrentURL)
	}

	database := db.GetMongo()
	defer db.Close()

	if err := database.C(db.Raw).Insert(c); err != nil {
		fmt.Println("insert err: ", err)
		return
	}
	// save url embedding
	// TODO:
	fmt.Println("current click: ", c)
}

// Recv handles the request and response of a collect event
// request contains the urls of clickstream
// response returns prediction of subsequent user actions
func Recv(c *gin.Context) {
	input := CollectRequest{}
	if err := c.ShouldBindJSON(&input); err != nil {
		c.JSON(http.StatusOK, &CollectResponse{
			Message: fmt.Sprintf("ERROR: %v", err),
		})
		return
	}
	input.Save()
	response := &CollectResponse{
		Message:      "OK",
		Next:         predictor.CalculateNext(),
		Destinations: predictor.CalculateDestination(),
		Productivity: predictor.CalculateProductivity(),
	}
	c.JSON(http.StatusOK, response)
}
