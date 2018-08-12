package models

import (
	"github.com/changkun/spritzer/db"
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

// IsNodeExist check if url is exist
func IsNodeExist(url string) bool {
	var nodes []Node
	database := db.GetMongo()
	defer db.Close()

	if err := database.C(db.Node).Find(bson.M{
		"url": url,
	}).All(&nodes); err != nil {
		return false
	}
	if len(nodes) > 0 {
		return true
	}
	return false
}
