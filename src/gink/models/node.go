package models

import (
	"errors"
	"math/rand"

	"github.com/changkun/gink/db"
	"github.com/sirupsen/logrus"
	"gopkg.in/mgo.v2/bson"
)

// Node represents the state of Action Path
type Node struct {
	URL               string         `json:"url"         bson:"url"`
	Value             string         `json:"value"       bson:"value"`
	Meta              []string       `json:"meta"        bson:"meta"`
	Keywords          []string       `json:"keywords"    bson:"keywords"`
	ManualDescription string         `json:"manual_desc" bson:"manual_desc"`
	SourceCode        string         `json:"source_code" bson:"source_code"`
	IsEnd             bool           `json:"is_end"      bson:"is_end"`
	Next              []ChildPointer `json:"next"        bson:"next"`
}

// ChildPointer represents the next state of Action Path
type ChildPointer struct {
	URL   string `json:"url" bson:"url"`
	Value string `json:"value" bson:"value"`
}

// var
var (
	ErrNoNodes = errors.New("no nodes")
)

// Save to database
func (n *Node) Save() error {
	logrus.Info("insert: ", n.URL)
	database := db.GetMongo()
	defer db.Close()

	if _, err := database.C(db.Node).Upsert(
		bson.M{
			"url": n.URL,
		}, n,
	); err != nil {
		logrus.Error("upsert err: ", err)
		return err
	}
	return nil
}

// FindActionPath .
func FindActionPath(minLength int, entry string) ([]Node, error) {
	database := db.GetMongo()
	defer db.Close()

	var nodes []Node

	// 1. append first node
	var validNodes []Node
	var node Node
	if err := database.C(db.Node).Find(bson.M{
		"url": entry,
		// "manual_desc": "",
	}).All(&validNodes); err != nil {
		logrus.Errorf("fail to find node from database, error: %s", err.Error())
		return nil, err
	}
	if len(validNodes) == 0 {
		return nil, ErrNoNodes
	}

RETRY:
	node = validNodes[rand.Intn(len(validNodes))]
	nodes = []Node{}
	nodes = append(nodes, node)

	logrus.Info("starting at: ", node.URL)
	logrus.Info("next length: ", len(node.Next))

	// 2. append child nodes
	for i := 1; ; i++ {
		logrus.Info("done: ", i)
		if len(node.Next) == 0 {
			// TODO: check minLength
			if len(nodes) < minLength {
				goto RETRY
			}
			break
		}

		var nextNode Node
		skip := rand.Intn(len(node.Next) / 2)

	NEXT:
		for index, next := range node.Next {
			if index < skip {
				continue NEXT
			}
			// do not use the node if it is a loop
			for _, exist := range nodes {
				if next.URL == exist.URL || next.URL == entry {
					continue NEXT
				}
			}

			if err := database.C(db.Node).Find(bson.M{
				"url": next.URL,
			}).One(&nextNode); err != nil {
				logrus.Errorf("fail to find nextNode from database, error: %s", err.Error())
				continue NEXT
			}

			if len(nextNode.ManualDescription) > 0 {
				continue NEXT
			}

			logrus.Info("next at: ", nextNode.URL)
			nodes = append(nodes, nextNode)
			break NEXT
		}
		node = nextNode
	}
	logrus.Info("length: ", len(nodes))
	if len(nodes) == 0 {
		return nil, ErrNoNodes
	}
	return nodes, nil
}
