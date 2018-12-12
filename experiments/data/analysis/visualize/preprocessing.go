package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
)

type ClickObject struct {
	UserID      int     `json:"user_id"`
	PreviousURL string  `json:"previous_url"`
	CurrentURL  string  `json:"current_url"`
	StaySeconds float64 `json:"stay_seconds"`
}

type TaskClickstream struct {
	TaskID      int           `json:"task_id"`
	Clickstream []ClickObject `json:"clickstream"`
}

type Target struct {
	Nodes []Node `json:"nodes"`
	Links []Link `json:"links"`
}

type Node struct {
	Index       string  `json:"index"`
	URL         string  `json:"url"`
	Group       int     `json:"group"`
	StaySeconds float64 `json:"stay_seconds"`
}
type Link struct {
	Source string `json:"source"`
	Target string `json:"target"`
	// SourceURL   string  `json:"source_url"`
	// TargetURL   string  `json:"target_url"`
	StaySeconds float64 `json:"stay_seconds"`
}

func main() {
	target := Target{}
	index := 0

	for i := 1; i < 2; i++ {
		raw, err := ioutil.ReadFile(fmt.Sprintf("../dataset/%d.json", i))
		if err != nil {
			panic(err)
		}

		var t []TaskClickstream
		err = json.Unmarshal(raw, &t)
		if err != nil {
			panic(err)
		}

		nodes := map[string]struct {
			index int
			stay  float64
		}{}
		for _, obj := range t[0].Clickstream {
			if v, ok := nodes[obj.PreviousURL]; !ok {
				index++
				nodes[obj.PreviousURL] = struct {
					index int
					stay  float64
				}{
					index: index,
					stay:  obj.StaySeconds,
				}
			} else {
				v.stay = nodes[obj.PreviousURL].stay + obj.StaySeconds
			}
			if v, ok := nodes[obj.CurrentURL]; !ok {
				index++
				nodes[obj.CurrentURL] = struct {
					index int
					stay  float64
				}{
					index: index,
					stay:  obj.StaySeconds,
				}
			} else {
				v.stay += obj.StaySeconds
			}

			link := Link{
				Source: fmt.Sprintf("%d", nodes[obj.PreviousURL].index),
				Target: fmt.Sprintf("%d", nodes[obj.CurrentURL].index),
				// SourceURL:   obj.PreviousURL,
				// TargetURL:   obj.CurrentURL,
				StaySeconds: obj.StaySeconds,
			}
			target.Links = append(target.Links, link)
		}

		for k := range nodes {
			node := Node{
				Index:       fmt.Sprintf("%d", nodes[k].index),
				URL:         k,
				Group:       i,
				StaySeconds: nodes[k].stay,
			}
			target.Nodes = append(target.Nodes, node)
		}
	}

	b, err := json.Marshal(target)
	if err != nil {
		panic(err)
	}

	ioutil.WriteFile("clickstream.json", b, 0777)
}
