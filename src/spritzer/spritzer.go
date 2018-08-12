package main

import (
	"bytes"
	"io/ioutil"
	"net/http"
	"path/filepath"
	"regexp"
	"strings"

	"github.com/PuerkitoBio/goquery"
	"github.com/changkun/spritzer/models"

	log "github.com/sirupsen/logrus"
)

const (
	starting = "http://www.medien.ifi.lmu.de"
)

func crawler(url string, value string) (map[string]string, error) {
	// if url is recorded in dabase, fast return
	if models.IsNodeExist(url) {
		return map[string]string{}, nil
	}

	// Save if should stop, also stop on file
	ext := filepath.Ext(filepath.Base(strings.TrimPrefix(strings.Split(url, "?")[0], starting)))
	if !strings.Contains(url, starting) || len(ext) > 1 {
		node := models.Node{
			URL:   url,
			Value: value,
			IsEnd: true,
		}
		node.Save()
		return map[string]string{}, nil
	}
	log.Info("extension: ", ext)

	// Reading the page
	response, err := http.Get(url)
	if err != nil {
		log.Errorf("get failed, url: %s", url)
		return map[string]string{}, err
	}
	// Read source code
	sourceCode, err := ioutil.ReadAll(response.Body)
	if err != nil {
		log.Errorf("read source code error: %s", err.Error())
		return map[string]string{}, err
	}
	response.Body.Close()

	responseBody := ioutil.NopCloser(bytes.NewBuffer(sourceCode))
	doc, err := goquery.NewDocumentFromReader(responseBody)
	if err != nil {
		log.Errorf("new document fail, url: %s", url)
		return map[string]string{}, err
	}

	// Get all possible metas
	metas := []string{}
	doc.Find("meta[name=description]").Each(func(i int, s *goquery.Selection) {
		if content, ok := s.Attr("content"); ok {
			metas = append(metas, content)
		}
	})

	keywords := []string{}
	doc.Find("meta[name=keywords]").Each(func(i int, s *goquery.Selection) {
		if content, ok := s.Attr("content"); ok {
			keywords = append(keywords, content)
		}
	})

	// Get all possible links
	next := []models.ChildPointer{}
	ret := map[string]string{}
	doc.Find("a").Each(func(i int, s *goquery.Selection) {
		href, ok := s.Attr("href")
		if !ok {
			return
		}
		var link string
		// ./index.html
		// /index.html
		// index.html
		// #index
		// http://xxxx
		if strings.HasPrefix(href, "http") {
			link = href
		} else if strings.HasPrefix(href, "#") || strings.HasPrefix(href, ".") {
			link = starting + "/" + href
		} else if strings.HasPrefix(href, "/") {
			link = starting + href
		} else {
			link = starting + "/" + href
		}
		next = append(next, models.ChildPointer{
			URL:   link,
			Value: s.Text(),
		})
		ret[link] = s.Text()
	})
	// Maybe get others
	re1 := regexp.MustCompile(`<.*?>`)
	re2 := regexp.MustCompile(` +`)
	re3 := regexp.MustCompile(`<!--.*-->`)
	filtered := re1.ReplaceAllString(string(sourceCode), ` `)
	filtered = re2.ReplaceAllString(filtered, ` `)
	filtered = re3.ReplaceAllString(filtered, ` `)
	strings.Replace(filtered, "\\n", " ", -1)
	strings.Replace(filtered, "\\t", " ", -1)
	node := models.Node{
		URL:        url,
		Value:      value,
		Meta:       metas,
		Keywords:   keywords,
		SourceCode: filtered,
		IsEnd:      false,
		Next:       next,
	}
	node.Save()
	return ret, nil
}

func spider(tasks map[string]string) {
	nextTasks := map[string]string{}
	for url, value := range tasks {
		result, err := crawler(url, value)
		if err != nil {
			continue
		}
		for u, v := range result {
			nextTasks[u] = v
		}
	}
	if len(nextTasks) > 0 {
		spider(nextTasks)
	}
}

func main() {
	spider(map[string]string{
		starting: "entry page",
	})
}
