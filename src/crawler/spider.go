package main

import (
	"fmt"
	"net/http"
	"strings"

	"golang.org/x/net/html"
)

func getHref(t html.Token) (ok bool, href string) {
	for _, a := range t.Attr {
		if a.Key == "href" {
			href = a.Val
			ok = true
		}
	}
	return
}

func crawl(url string, ch chan string, chFinished chan bool) {
	fmt.Println(url)
	resp, err := http.Get(url)

	defer func() {
		chFinished <- true
	}()

	if err != nil {
		fmt.Println("ERROR: Failed to crawl \"" + url + "\"")
		return
	}
	defer resp.Body.Close()

	z := html.NewTokenizer(resp.Body)

	for {
		tt := z.Next()

		switch {
		case tt == html.ErrorToken:
			return
		case tt == html.StartTagToken:
			t := z.Token()
			isAnchor := t.Data == "a"
			if !isAnchor {
				continue
			}
			ok, url := getHref(t)
			if !ok {
				continue
			}
			hasProto := strings.Index(url, "http") == 0
			if hasProto {
				// fmt.Println("Found URL: ", url)
				ch <- url
			}
		}
	}
}

func seed(urls map[string]bool) {
	foundUrls := make(map[string]bool)
	chUrls := make(chan string)
	chFinished := make(chan bool)
	defer func() {
		close(chUrls)
		close(chFinished)
	}()

	dos := 0
	for url, do := range urls {
		if do {
			dos++
			go crawl(url, chUrls, chFinished)
		}
	}

	// Subscribe to both channels
	for c := 0; c < dos; {
		select {
		case url := <-chUrls:
			foundUrls[url] = true
		case <-chFinished:
			c++
		}
	}

	fmt.Println("Found", len(foundUrls), "unique urls:")
	if depth < max {
		fmt.Println("depth: ", depth, ", max: ", max)
		depth++
		for url := range foundUrls {
			if !strings.Contains(url, region) && strings.Contains(url, "http") {
				fmt.Println(" - ", url, " | end.")
				foundUrls[url] = false
				continue
			}
			fmt.Println(" - " + url)
		}
		seed(foundUrls)
	}
}

const (
	region = "medien.ifi"
	max    = 10
)

var depth = 0
var starting = "http://www.medien.ifi.lmu.de"

func main() {
	seed(map[string]bool{starting: true})
}
