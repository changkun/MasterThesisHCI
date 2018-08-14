package models

import (
	"github.com/changkun/gink/db"
	"github.com/sirupsen/logrus"
	"gopkg.in/mgo.v2/bson"
)

// SupervisedActionPath .
type SupervisedActionPath struct {
	Path              []string `json:"path"        bson:"path"`
	ManualDescription string   `json:"manual_desc" bson:"manual_desc"`
}

// Save .
func (s *SupervisedActionPath) Save() error {
	logrus.Info("insert: ", s.ManualDescription)

	database := db.GetMongo()
	defer db.Close()

	if _, err := database.C(db.Supervised).Upsert(
		bson.M{
			"path": s.Path,
		}, s,
	); err != nil {
		logrus.Error("upsert err: ", err)
		return err
	}
	return nil
}

// IsActionPathRecorded .
func IsActionPathRecorded(nodes []Node) bool {
	database := db.GetMongo()
	defer db.Close()

	path := []string{}
	for _, node := range nodes {
		path = append(path, node.URL)
	}

	var existPath SupervisedActionPath
	if err := database.C(db.Supervised).Find(bson.M{
		"path": path,
	}).One(&existPath); err != nil {
		logrus.Error("find exist path in db failed: ", err)
		return false
	}
	if len(existPath.ManualDescription) < 10 {
		logrus.Error("description too short, need re-describe.")
		return false
	}
	return true
}
