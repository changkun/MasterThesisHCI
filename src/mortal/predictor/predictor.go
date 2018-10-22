package predictor

import (
	"math/rand"
	"sort"
)

// Jump ...
type Jump struct {
	URL         string `json:"url"`
	Description string `json:"description"`
	Confidence  int    `json:"confidence"` // 0 to 100
}

// CalculateNext ...
func CalculateNext() *[]Jump {
	j := []Jump{
		Jump{
			URL:         "https://google.com",
			Description: "Search engine",
			Confidence:  rand.Intn(100),
		},
		Jump{
			URL:         "https://github.com",
			Description: "Github",
			Confidence:  rand.Intn(100),
		},
		Jump{
			URL:         "https://medium.com",
			Description: "Ideas and stories",
			Confidence:  rand.Intn(100),
		},
		Jump{
			URL:         "https://news.ycombinator.com/news",
			Description: "Venture capital and hacker news",
			Confidence:  rand.Intn(100),
		},
		Jump{
			URL:         "https://youtube.com",
			Description: "Videos",
			Confidence:  rand.Intn(100),
		},
	}
	sort.Slice(j, func(i, k int) bool {
		return j[i].Confidence > j[k].Confidence
	})
	length := rand.Intn(len(j))
	r := j[0:length]
	return &r
}

// CalculateDestination ...
func CalculateDestination() *[]Jump {
	j := []Jump{
		Jump{
			URL:         "https://google.com",
			Description: "Search engine",
			Confidence:  rand.Intn(100),
		},
		Jump{
			URL:         "https://github.com",
			Description: "Github",
			Confidence:  rand.Intn(100),
		},
		Jump{
			URL:         "https://medium.com",
			Description: "Ideas and stories",
			Confidence:  rand.Intn(100),
		},
		Jump{
			URL:         "https://news.ycombinator.com/news",
			Description: "Venture capital and hacker news",
			Confidence:  rand.Intn(100),
		},
		Jump{
			URL:         "https://youtube.com",
			Description: "Videos",
			Confidence:  rand.Intn(100),
		},
	}
	sort.Slice(j, func(i, k int) bool {
		return j[i].Confidence > j[k].Confidence
	})
	length := rand.Intn(len(j))
	r := j[0:length]
	return &r
}

// CalculateProductivity ...
func CalculateProductivity() int {
	return rand.Intn(100)
}
