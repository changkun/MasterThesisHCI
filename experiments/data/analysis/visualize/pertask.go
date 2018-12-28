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
	Index       int     `json:"id"`
	URL         string  `json:"url"`
	Label       string  `json:"label"`
	Group       int     `json:"group"`
	StaySeconds float64 `json:"stay_seconds"`
}
type Link struct {
	Source int `json:"source"`
	Target int `json:"target"`
	// SourceURL   string  `json:"source_url"`
	// TargetURL   string  `json:"target_url"`
	StaySeconds float64 `json:"stay_seconds"`
}

// Change node property: length to the point

const taskid = 1

func main() {
	target := Target{}
	index := 0

	nodes := map[string]*struct {
		index int
		label string
		group int
		stay  float64
	}{}
	for userid := 1; userid < 22; userid++ {

		raw, err := ioutil.ReadFile(fmt.Sprintf("../dataset/%d.json", userid))
		if err != nil {
			panic(err)
		}

		var t []TaskClickstream
		err = json.Unmarshal(raw, &t)
		if err != nil {
			panic(err)
		}

		label := 0
		for _, obj := range t[taskid-1].Clickstream {
			labelChanged := false

			if v, ok := nodes[obj.PreviousURL]; !ok { // new node
				label++
				labelChanged = true
				index++
				nodes[obj.PreviousURL] = &struct {
					index int
					label string
					group int
					stay  float64
				}{
					index: index,
					label: fmt.Sprintf("%d", label),
					group: userid,
					stay:  obj.StaySeconds,
				}
			} else { // old node
				v.stay = nodes[obj.PreviousURL].stay + obj.StaySeconds
			}
			if v, ok := nodes[obj.CurrentURL]; !ok { // new node
				label++
				labelChanged = true
				index++
				nodes[obj.CurrentURL] = &struct {
					index int
					label string
					group int
					stay  float64
				}{
					index: index,
					label: fmt.Sprintf("%d", label),
					group: userid,
					stay:  obj.StaySeconds,
				}
			} else { // old node
				v.stay += obj.StaySeconds
			}

			// compute link
			link := Link{
				Source:      nodes[obj.PreviousURL].index,
				Target:      nodes[obj.CurrentURL].index,
				StaySeconds: obj.StaySeconds,
			}
			target.Links = append(target.Links, link)

			if !labelChanged {
				label++
			}
		}

	}

	for k := range nodes {
		node := Node{
			Index:       nodes[k].index,
			URL:         k,
			Group:       nodes[k].group,
			Label:       nodes[k].label,
			StaySeconds: nodes[k].stay,
		}
		target.Nodes = append(target.Nodes, node)
	}

	b, err := json.Marshal(target)
	if err != nil {
		panic(err)
	}

	ioutil.WriteFile(fmt.Sprintf("js/clickstream-task-%d-all.js", taskid), []byte("var graph = "+string(b)), 0777)
}
