package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"sort"
)

type node struct {
	key  string
	cost float64
}

// Graph {
// 	"a": {"b": 10, "c": 20},
// 	"b": {"a": 50},
// 	"c": {"b": 10, "a": 25},
// }
// Graph is a rappresentation of how the points in our graph are connected
// between each other
type Graph map[string]map[string]float64

// Path finds the shortest path between start and target, also returning the
// total cost of the found path.
func (g Graph) Path(start, target string) (path []string, cost float64, err error) {
	if len(g) == 0 {
		err = fmt.Errorf("cannot find path in empty map")
		return
	}

	// ensure start and target are part of the graph
	if _, ok := g[start]; !ok {
		err = fmt.Errorf("cannot find start %v in graph", start)
		return
	}
	if _, ok := g[target]; !ok {
		err = fmt.Errorf("cannot find target %v in graph", target)
		return
	}

	explored := make(map[string]bool)   // set of nodes we already explored
	frontier := NewQueue()              // queue of the nodes to explore
	previous := make(map[string]string) // previously visited node

	// add starting point to the frontier as it'll be the first node visited
	frontier.Set(start, 0)

	// run until we visited every node in the frontier
	for !frontier.IsEmpty() {
		// get the node in the frontier with the lowest cost (or priority)
		aKey, aPriority := frontier.Next()
		n := node{aKey, aPriority}

		// when the node with the lowest cost in the frontier is target, we can
		// compute the cost and path and exit the loop
		if n.key == target {
			cost = n.cost

			nKey := n.key
			for nKey != start {
				path = append(path, nKey)
				nKey = previous[nKey]
			}

			break
		}

		// add the current node to the explored set
		explored[n.key] = true

		// loop all the neighboring nodes
		for nKey, nCost := range g[n.key] {
			// skip alreadt-explored nodes
			if explored[nKey] {
				continue
			}

			// if the node is not yet in the frontier add it with the cost
			if _, ok := frontier.Get(nKey); !ok {
				previous[nKey] = n.key
				frontier.Set(nKey, n.cost+nCost)
				continue
			}

			frontierCost, _ := frontier.Get(nKey)
			nodeCost := n.cost + nCost

			// only update the cost of this node in the frontier when
			// it's below what's currently set
			if nodeCost < frontierCost {
				previous[nKey] = n.key
				frontier.Set(nKey, nodeCost)
			}
		}
	}

	// add the origin at the end of the path
	path = append(path, start)

	// reverse the path because it was popilated
	// in reverse, form target to start
	for i, j := 0, len(path)-1; i < j; i, j = i+1, j-1 {
		path[i], path[j] = path[j], path[i]
	}

	return
}

// Queue is a basic priority queue implementation, where the node with the
// lowest priority is kept as first element in the queue
type Queue struct {
	keys  []string
	nodes map[string]float64
}

// Len is part of sort.Interface
func (q *Queue) Len() int {
	return len(q.keys)
}

// Swap is part of sort.Interface
func (q *Queue) Swap(i, j int) {
	q.keys[i], q.keys[j] = q.keys[j], q.keys[i]
}

// Less is part of sort.Interface
func (q *Queue) Less(i, j int) bool {
	a := q.keys[i]
	b := q.keys[j]

	return q.nodes[a] < q.nodes[b]
}

// Set updates or inserts a new key in the priority queue
func (q *Queue) Set(key string, priority float64) {
	// inserts a new key if we don't have it already
	if _, ok := q.nodes[key]; !ok {
		q.keys = append(q.keys, key)
	}

	// set the priority for the key
	q.nodes[key] = priority

	// sort the keys array
	sort.Sort(q)
}

// Next removes the first element from the queue and retuns it's key and priority
func (q *Queue) Next() (key string, priority float64) {
	// shift the key form the queue
	key, keys := q.keys[0], q.keys[1:]
	q.keys = keys

	priority = q.nodes[key]

	delete(q.nodes, key)

	return key, priority
}

// IsEmpty returns true when the queue is empty
func (q *Queue) IsEmpty() bool {
	return len(q.keys) == 0
}

// Get returns the priority of a passed key
func (q *Queue) Get(key string) (priority float64, ok bool) {
	priority, ok = q.nodes[key]
	return
}

// NewQueue creates a new empty priority queue
func NewQueue() *Queue {
	var q Queue
	q.nodes = make(map[string]float64)
	return &q
}

// ClickObject ...
type ClickObject struct {
	UserID      int     `json:"user_id"`
	PreviousURL string  `json:"previous_url"`
	CurrentURL  string  `json:"current_url"`
	StaySeconds float64 `json:"stay_seconds"`
}

// TaskClickstream ...
type TaskClickstream struct {
	TaskID      int           `json:"task_id"`
	Clickstream []ClickObject `json:"clickstream"`
}

// userid: 1~21, taskid: 1~9
func readClickstream(userid, taskid int) TaskClickstream {
	raw, err := ioutil.ReadFile(fmt.Sprintf("../dataset/%d.json", userid))
	if err != nil {
		panic(err)
	}

	var t []TaskClickstream
	err = json.Unmarshal(raw, &t)
	if err != nil {
		panic("parse clickstream failed" + err.Error())
	}
	return t[taskid-1]
}

func buildGraph(userid, taskid int) (Graph, string, string, int, float64) {
	clickstream := readClickstream(userid, taskid)
	start := clickstream.Clickstream[0].PreviousURL
	end := clickstream.Clickstream[len(clickstream.Clickstream)-1].CurrentURL

	graph := map[string]map[string]float64{}

	totalDuration := 0.0
	for _, page := range clickstream.Clickstream {
		totalDuration += page.StaySeconds
		if _, ok := graph[page.PreviousURL]; ok {
			if _, ok := graph[page.PreviousURL][page.CurrentURL]; ok {
				graph[page.PreviousURL][page.CurrentURL] += page.StaySeconds
			} else {
				graph[page.PreviousURL][page.CurrentURL] = page.StaySeconds
			}
		} else {
			graph[page.PreviousURL] = map[string]float64{page.CurrentURL: page.StaySeconds}
		}
	}
	graph[clickstream.Clickstream[len(clickstream.Clickstream)-1].CurrentURL] = map[string]float64{}

	return Graph(graph), start, end, len(graph), totalDuration
}

func main() {
	for taskid := 1; taskid < 10; taskid++ {
		for userid := 1; userid < 22; userid++ {
			graph, start, end, nnodes, tduration := buildGraph(userid, taskid)
			path, cost, err := graph.Path(start, end)
			if err != nil {
				panic(err)
			}
			efficiency := 0.5*float64(len(path))/float64(nnodes) + 0.5*cost/tduration
			fmt.Printf("(%d, %d) task efficiency: %.4f\n", userid, taskid, efficiency)
		}
	}
}

// (1, 1) task efficiency: 0.3914
// (2, 1) task efficiency: 0.3493
// (3, 1) task efficiency: 0.3773
// (4, 1) task efficiency: 0.8519
// (5, 1) task efficiency: 0.6763
// (6, 1) task efficiency: 0.4058
// (7, 1) task efficiency: 0.1710
// (8, 1) task efficiency: 0.9092
// (9, 1) task efficiency: 0.2801
// (10, 1) task efficiency: 0.9185
// (11, 1) task efficiency: 0.6170
// (12, 1) task efficiency: 0.2540
// (13, 1) task efficiency: 0.2862
// (14, 1) task efficiency: 0.4749
// (15, 1) task efficiency: 0.2866
// (16, 1) task efficiency: 0.3820
// (17, 1) task efficiency: 0.7425
// (18, 1) task efficiency: 0.7876
// (19, 1) task efficiency: 0.4303
// (20, 1) task efficiency: 0.3187
// (21, 1) task efficiency: 0.3369

// (1, 2) task efficiency: 0.8349
// (2, 2) task efficiency: 0.2230
// (3, 2) task efficiency: 0.3828
// (4, 2) task efficiency: 0.0132
// (5, 2) task efficiency: 1.0000
// (6, 2) task efficiency: 0.6904
// (7, 2) task efficiency: 0.3889
// (8, 2) task efficiency: 0.4515
// (9, 2) task efficiency: 0.0622
// (10, 2) task efficiency: 0.9085
// (11, 2) task efficiency: 0.4798
// (12, 2) task efficiency: 0.4503
// (13, 2) task efficiency: 0.3142
// (14, 2) task efficiency: 0.3633
// (15, 2) task efficiency: 0.5425
// (16, 2) task efficiency: 0.6696
// (17, 2) task efficiency: 0.3004
// (18, 2) task efficiency: 0.6121
// (19, 2) task efficiency: 0.1888
// (20, 2) task efficiency: 0.6652
// (21, 2) task efficiency: 0.7462

// (1, 3) task efficiency: 0.1734
// (2, 3) task efficiency: 0.1203
// (3, 3) task efficiency: 0.2194
// (4, 3) task efficiency: 0.9356
// (5, 3) task efficiency: 0.1768
// (6, 3) task efficiency: 0.8488
// (7, 3) task efficiency: 0.1416
// (8, 3) task efficiency: 0.3546
// (9, 3) task efficiency: 0.5126
// (10, 3) task efficiency: 0.5782
// (11, 3) task efficiency: 0.4606
// (12, 3) task efficiency: 0.2221
// (13, 3) task efficiency: 0.4412
// (14, 3) task efficiency: 0.4239
// (15, 3) task efficiency: 0.3245
// (16, 3) task efficiency: 0.2078
// (17, 3) task efficiency: 0.4946
// (18, 3) task efficiency: 0.9163
// (19, 3) task efficiency: 0.5342
// (20, 3) task efficiency: 0.2073
// (21, 3) task efficiency: 0.6191

// (1, 4) task efficiency: 0.2953
// (2, 4) task efficiency: 0.5413
// (3, 4) task efficiency: 0.9510
// (4, 4) task efficiency: 0.2619
// (5, 4) task efficiency: 0.2941
// (6, 4) task efficiency: 0.3307
// (7, 4) task efficiency: 0.3463
// (8, 4) task efficiency: 0.9096
// (9, 4) task efficiency: 0.1507
// (10, 4) task efficiency: 0.7907
// (11, 4) task efficiency: 0.9997
// (12, 4) task efficiency: 0.3174
// (13, 4) task efficiency: 0.5925
// (14, 4) task efficiency: 0.5136
// (15, 4) task efficiency: 0.2327
// (16, 4) task efficiency: 0.2347
// (17, 4) task efficiency: 0.5096
// (18, 4) task efficiency: 0.2514
// (19, 4) task efficiency: 1.0000
// (20, 4) task efficiency: 0.2853
// (21, 4) task efficiency: 0.7516

// (1, 5) task efficiency: 0.3652
// (2, 5) task efficiency: 0.3363
// (3, 5) task efficiency: 0.3523
// (4, 5) task efficiency: 0.2424
// (5, 5) task efficiency: 0.4139
// (6, 5) task efficiency: 0.6835
// (7, 5) task efficiency: 0.3185
// (8, 5) task efficiency: 0.1097
// (9, 5) task efficiency: 0.4041
// (10, 5) task efficiency: 0.5268
// (11, 5) task efficiency: 0.3488
// (12, 5) task efficiency: 0.2557
// (13, 5) task efficiency: 0.3559
// (14, 5) task efficiency: 0.6098
// (15, 5) task efficiency: 0.1987
// (16, 5) task efficiency: 0.2221
// (17, 5) task efficiency: 0.2195
// (18, 5) task efficiency: 1.0000
// (19, 5) task efficiency: 0.6691
// (20, 5) task efficiency: 0.6462
// (21, 5) task efficiency: 0.5547

// (1, 6) task efficiency: 0.7073
// (2, 6) task efficiency: 0.1909
// (3, 6) task efficiency: 0.1459
// (4, 6) task efficiency: 0.6350
// (5, 6) task efficiency: 0.1838
// (6, 6) task efficiency: 0.3035
// (7, 6) task efficiency: 0.3787
// (8, 6) task efficiency: 0.6171
// (9, 6) task efficiency: 0.1580
// (10, 6) task efficiency: 0.7795
// (11, 6) task efficiency: 0.2315
// (12, 6) task efficiency: 0.2100
// (13, 6) task efficiency: 0.5147
// (14, 6) task efficiency: 0.3792
// (15, 6) task efficiency: 0.1608
// (16, 6) task efficiency: 0.2549
// (17, 6) task efficiency: 0.7292
// (18, 6) task efficiency: 0.1442
// (19, 6) task efficiency: 0.3953
// (20, 6) task efficiency: 0.1147
// (21, 6) task efficiency: 0.3175

// (1, 7) task efficiency: 0.3013
// (2, 7) task efficiency: 0.2000
// (3, 7) task efficiency: 0.5178
// (4, 7) task efficiency: 0.1307
// (5, 7) task efficiency: 0.1653
// (6, 7) task efficiency: 0.4376
// (7, 7) task efficiency: 0.2169
// (8, 7) task efficiency: 0.3828
// (9, 7) task efficiency: 0.2030
// (10, 7) task efficiency: 0.4011
// (11, 7) task efficiency: 0.3725
// (12, 7) task efficiency: 0.3249
// (13, 7) task efficiency: 0.3730
// (14, 7) task efficiency: 0.1011
// (15, 7) task efficiency: 0.1386
// (16, 7) task efficiency: 0.2753
// (17, 7) task efficiency: 0.6073
// (18, 7) task efficiency: 0.3904
// (19, 7) task efficiency: 0.4746
// (20, 7) task efficiency: 0.3896
// (21, 7) task efficiency: 0.0625

// (1, 8) task efficiency: 0.1555
// (2, 8) task efficiency: 0.2789
// (3, 8) task efficiency: 0.3354
// (4, 8) task efficiency: 0.2108
// (5, 8) task efficiency: 0.2085
// (6, 8) task efficiency: 0.2549
// (7, 8) task efficiency: 0.3026
// (8, 8) task efficiency: 0.2620
// (9, 8) task efficiency: 0.3736
// (10, 8) task efficiency: 0.3871
// (11, 8) task efficiency: 0.3466
// (12, 8) task efficiency: 0.4583
// (13, 8) task efficiency: 0.3280
// (14, 8) task efficiency: 0.6635
// (15, 8) task efficiency: 0.2576
// (16, 8) task efficiency: 0.4002
// (17, 8) task efficiency: 0.4422
// (18, 8) task efficiency: 0.3788
// (19, 8) task efficiency: 0.3520
// (20, 8) task efficiency: 0.2477
// (21, 8) task efficiency: 0.4585

// (1, 9) task efficiency: 0.0236
// (2, 9) task efficiency: 0.1092
// (3, 9) task efficiency: 0.1486
// (4, 9) task efficiency: 0.4437
// (5, 9) task efficiency: 0.3438
// (6, 9) task efficiency: 0.1480
// (7, 9) task efficiency: 0.1248
// (8, 9) task efficiency: 0.0227
// (9, 9) task efficiency: 0.2147
// (10, 9) task efficiency: 0.3176
// (11, 9) task efficiency: 0.9038
// (12, 9) task efficiency: 0.2513
// (13, 9) task efficiency: 0.1573
// (14, 9) task efficiency: 0.3289
// (15, 9) task efficiency: 0.2490
// (16, 9) task efficiency: 0.9433
// (17, 9) task efficiency: 0.2136
// (18, 9) task efficiency: 0.2986
// (19, 9) task efficiency: 0.5817
// (20, 9) task efficiency: 0.0901
// (21, 9) task efficiency: 0.3451

// [0.3914, 0.8349, 0.1734, 0.2953, 0.3652, 0.7073, 0.3013, 0.1555, 0.0236],
// [0.3493, 0.2230, 0.1203, 0.5413, 0.3363, 0.1909, 0.2000, 0.2789, 0.1092],
// [0.3773, 0.3828, 0.2194, 0.9510, 0.3523, 0.1459, 0.5178, 0.3354, 0.1486],
// [0.8519, 0.0132, 0.9356, 0.2619, 0.2424, 0.6350, 0.1307, 0.2108, 0.4437],
// [0.6763, 1.0000, 0.1768, 0.2941, 0.4139, 0.1838, 0.1653, 0.2085, 0.3438],
// [0.4058, 0.6904, 0.8488, 0.3307, 0.6835, 0.3035, 0.4376, 0.2549, 0.1480],
// [0.1710, 0.3889, 0.1416, 0.3463, 0.3185, 0.3787, 0.2169, 0.3026, 0.1248],
// [0.9092, 0.4515, 0.3546, 0.9096, 0.1097, 0.6171, 0.3828, 0.2620, 0.0227],
// [0.2801, 0.0622, 0.5126, 0.1507, 0.4041, 0.1580, 0.2030, 0.3736, 0.2147],
// [0.9185, 0.9085, 0.5782, 0.7907, 0.5268, 0.7795, 0.4011, 0.3871, 0.3176],
// [0.6170, 0.4798, 0.4606, 0.9997, 0.3488, 0.2315, 0.3725, 0.3466, 0.9038],
// [0.2540, 0.4503, 0.2221, 0.3174, 0.2557, 0.2100, 0.3249, 0.4583, 0.2513],
// [0.2862, 0.3142, 0.4412, 0.5925, 0.3559, 0.5147, 0.3730, 0.3280, 0.1573],
// [0.4749, 0.3633, 0.4239, 0.5136, 0.6098, 0.3792, 0.1011, 0.6635, 0.3289],
// [0.2866, 0.5425, 0.3245, 0.2327, 0.1987, 0.1608, 0.1386, 0.2576, 0.2490],
// [0.3820, 0.6696, 0.2078, 0.2347, 0.2221, 0.2549, 0.2753, 0.4002, 0.9433],
// [0.7425, 0.3004, 0.4946, 0.5096, 0.2195, 0.7292, 0.6073, 0.4422, 0.2136],
// [0.7876, 0.6121, 0.9163, 0.2514, 1.0000, 0.1442, 0.3904, 0.3788, 0.2986],
// [0.4303, 0.1888, 0.5342, 1.0000, 0.6691, 0.3953, 0.4746, 0.3520, 0.5817],
// [0.3187, 0.6652, 0.2073, 0.2853, 0.6462, 0.1147, 0.3896, 0.2477, 0.0901],
// [0.3369, 0.7462, 0.6191, 0.7516, 0.5547, 0.3175, 0.0625, 0.4585, 0.3451],
