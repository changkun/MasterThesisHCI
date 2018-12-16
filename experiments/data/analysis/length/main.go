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

func main() {
	total := 21
	lengthMat := [21][9]int{}
	durationMat := [21][9]float64{}
	for i := 1; i <= total; i++ {
		raw, err := ioutil.ReadFile(fmt.Sprintf("../dataset/%d.json", i))
		if err != nil {
			panic(err)
		}

		var ts []TaskClickstream
		err = json.Unmarshal(raw, &ts)
		if err != nil {
			panic(err)
		}

		for j, t := range ts {
			lengthMat[i-1][j] = len(t.Clickstream)

			totalStay := 0.0
			for p := range t.Clickstream {
				totalStay += t.Clickstream[p].StaySeconds
			}
			durationMat[i-1][j] = totalStay
		}
	}

	fmt.Println(lengthMat)

	fmt.Printf("%.6v", durationMat)
}
