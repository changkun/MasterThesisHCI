package api

import "github.com/changkun/gink/models"

// PingOutput .
type PingOutput struct {
	Message string `json:"message"`
	Version string `json:"version"`
}

// NodesOutput .
type NodesOutput struct {
	Message string        `json:"message"`
	Nodes   []models.Node `json:"nodes"`
}

// SaveNodeInput .
type SaveNodeInput struct {
	models.Node
}

// SaveNodeOutput .
type SaveNodeOutput struct {
	Message string `json:"message"`
}

// SaveActionPathInput .
type SaveActionPathInput struct {
	models.SupervisedActionPath
}

// SaveActionPathOutput .
type SaveActionPathOutput struct {
	Message string `json:"message"`
}
