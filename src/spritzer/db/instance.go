package db

import (
	"errors"
	"sync"
	"time"

	"github.com/changkun/spritzer/settings"
	mgo "gopkg.in/mgo.v2"
)

// mongo collections
const (
	Node = "node"
)

// Instance : the database for cloudlab service
type Instance struct {
	Mongo *mgo.Database
}

var (
	once       sync.Once
	dbInstance *Instance
)

// GetMongo returns mongodb database
func GetMongo() *mgo.Database {
	initMongo()
	return instance().Mongo
}

// Close all database connection
// currently no need for this action since
// connection is a singleton in init phase
func Close() {
	if instance().Mongo != nil {
		instance().Mongo.Session.Close()
	}
	dbInstance.Mongo = nil
}

// GetInstance return a singleton database instance
func instance() *Instance {
	once.Do(func() {
		dbInstance = &Instance{}
	})
	return dbInstance
}

func initMongo() {
	err := instance().connectMongoWith(settings.MongoURL)
	if err != nil {
		panic(err)
	}
}

func (db *Instance) parseMongo(url string) *mgo.DialInfo {
	dialInfo, err := mgo.ParseURL(url)
	if err != nil || dialInfo.Database != "spritzer" {
		return nil
	}
	// must connected to database within a second
	dialInfo.Timeout = time.Second
	return dialInfo
}

func (db *Instance) connectMongoWith(url string) error {
	if db.Mongo == nil {
		dialInfo := db.parseMongo(url)
		if dialInfo == nil {
			return errors.New("Parse MongoDB URL error")
		}
		session, err := mgo.DialWithInfo(dialInfo)
		if err != nil {
			return err
		}
		db.Mongo = session.DB(dialInfo.Database)
	}
	return nil
}
