package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"io/ioutil"
	"strconv"
	"strings"
	"unicode/utf8"
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
	CommonNode  bool    `json:"common_node"`
}
type Link struct {
	Source int `json:"source"`
	Target int `json:"target"`
	// SourceURL   string  `json:"source_url"`
	// TargetURL   string  `json:"target_url"`
	StaySeconds float64 `json:"stay_seconds"`
}

// Change node property: length to the point

var users []int
var taskid = 9
var similarity = 0.98

func init() {
	t := flag.Int("tid", 1, "task id")
	u := flag.String("users", "1", "totoal users")
	s := flag.Float64("sim", 0.98, "similarity")
	flag.Parse()
	if *t > 9 || *t < 1 {
		panic("wrong task id")
	}
	if *u == "" {
		panic("wrong users")
	}
	if *s > 1 || *s < 0 {
		panic("wrong similarity")
	}
	taskid = *t
	us := strings.Split(*u, ",")
	for _, v := range us {
		uid, _ := strconv.Atoi(v)
		users = append(users, uid)
	}
	similarity = *s
	// fmt.Printf("params: %d, %d, %f\n", taskid, totalusers, similarity)
}

func main() {
	target := Target{}
	index := 0

	nodes := map[string]*struct {
		index  int
		label  string
		group  int
		stay   float64
		common bool
	}{}
	for _, userid := range users {

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
			if v, ok := nodes[obj.PreviousURL]; !ok { // 新节点
				label++ // 记录节点的标签序号
				// labelChanged = true
				index++ // 记录全局唯一的序号
				nodes[obj.PreviousURL] = &struct {
					index  int
					label  string
					group  int
					stay   float64
					common bool
				}{
					index:  index,
					label:  fmt.Sprintf("%d", label),
					group:  userid, // 按用户分组
					stay:   obj.StaySeconds,
					common: false, // 首次添加的节点不是公共节点
				}
				var maxFuzzy float64
				for url := range nodes {
					ratio := ComputeFuzzyRatio(obj.PreviousURL, url)
					if ratio > maxFuzzy {
						maxFuzzy = ratio
					}
				}
				if maxFuzzy > similarity {
					nodes[obj.PreviousURL].common = true
				}
			} else { // 发现原有的节点
				// 将停留时间增加到原有节点上，如果当前的 stream id
				v.stay = v.stay + obj.StaySeconds
				// v.label += fmt.Sprintf(",%d", label)
				if userid != v.group {
					v.common = true
				}
			}
			if v, ok := nodes[obj.CurrentURL]; !ok { // new node
				label++
				// labelChanged = true
				index++
				nodes[obj.CurrentURL] = &struct {
					index  int
					label  string
					group  int
					stay   float64
					common bool
				}{
					index:  index,
					label:  fmt.Sprintf("%d", label),
					group:  userid,
					stay:   obj.StaySeconds,
					common: false,
				}
				var maxFuzzy float64
				for url := range nodes {
					ratio := ComputeFuzzyRatio(obj.PreviousURL, url)
					if ratio > maxFuzzy {
						maxFuzzy = ratio
					}
				}
				if maxFuzzy > similarity {
					nodes[obj.CurrentURL].common = true
				}
			} else { // old node
				v.stay += obj.StaySeconds
				// v.label += fmt.Sprintf(",%d", label)
				if userid != v.group {
					v.common = true
				}
			}

			// compute link
			link := Link{
				Source:      nodes[obj.PreviousURL].index,
				Target:      nodes[obj.CurrentURL].index,
				StaySeconds: obj.StaySeconds,
			}
			target.Links = append(target.Links, link)
		}

	}

	for k := range nodes {
		node := Node{
			Index:       nodes[k].index,
			URL:         k,
			Group:       nodes[k].group,
			Label:       nodes[k].label,
			StaySeconds: nodes[k].stay,
			CommonNode:  nodes[k].common,
		}
		target.Nodes = append(target.Nodes, node)
	}

	b, err := json.Marshal(target)
	if err != nil {
		panic(err)
	}

	commonNodes := 0
	for _, v := range nodes {
		if v.common {
			commonNodes++
		}
	}

	// intersection ratio  = common node / total nodes
	fmt.Printf("task %d total %d users, intersection ratio: %.4f\n", taskid, len(users), float64(commonNodes)/float64(len(nodes)))

	ioutil.WriteFile(fmt.Sprintf("js/clickstream-task-%d-all.js", taskid), []byte("var graph = "+string(b)), 0777)
}

// task 9 intersection ratio: 0.2475

// ComputeFuzzyRatio ...
func ComputeFuzzyRatio(a, b string) float64 {
	d := ComputeDistance(a, b)
	return float64(d) / float64(max(len(a), len(b)))
}

// ComputeDistance computes the levenshtein distance between the two
// strings passed as an argument. The return value is the levenshtein distance
//
// Works on runes (Unicode code points) but does not normalize
// the input strings. See https://blog.golang.org/normalization
// and the golang.org/x/text/unicode/norm pacage.
func ComputeDistance(a, b string) int {
	if len(a) == 0 {
		return utf8.RuneCountInString(b)
	}

	if len(b) == 0 {
		return utf8.RuneCountInString(a)
	}

	if a == b {
		return 0
	}

	// We need to convert to []rune if the strings are non-ascii.
	// This could be avoided by using utf8.RuneCountInString
	// and then doing some juggling with rune indices.
	// The primary challenge is keeping track of the previous rune.
	// With a range loop, its not that easy. And with a for-loop
	// we need to keep track of the inter-rune width using utf8.DecodeRuneInString
	s1 := []rune(a)
	s2 := []rune(b)

	// swap to save some memory O(min(a,b)) instead of O(a)
	if len(s1) > len(s2) {
		s1, s2 = s2, s1
	}
	lenS1 := len(s1)
	lenS2 := len(s2)

	// init the row
	x := make([]int, lenS1+1)
	for i := 0; i <= lenS1; i++ {
		x[i] = i
	}

	// fill in the rest
	for i := 1; i <= lenS2; i++ {
		prev := i
		var current int

		for j := 1; j <= lenS1; j++ {

			if s2[i-1] == s1[j-1] {
				current = x[j-1] // match
			} else {
				current = min(min(x[j-1]+1, prev+1), x[j]+1)
			}
			x[j-1] = prev
			prev = current
		}
		x[lenS1] = prev
	}
	return x[lenS1]
}

func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}
func max(a, b int) int {
	if a > b {
		return a
	}
	return b
}
