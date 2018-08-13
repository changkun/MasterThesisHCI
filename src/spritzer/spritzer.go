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
	"github.com/changkun/spritzer/settings"

	log "github.com/sirupsen/logrus"
)

const ()

func crawler(url string, value string) (map[string]string, error) {
	// if url is recorded in dabase, fast return
	if models.IsNodeExist(url) {
		return map[string]string{}, nil
	}

	// Save if should stop, also stop on file
	ext := filepath.Ext(filepath.Base(strings.TrimPrefix(strings.Split(url, "?")[0], settings.Starting)))
	if !strings.Contains(url, settings.Starting) || len(ext) > 1 {
		node := models.Node{
			URL:   url,
			Value: value,
			IsEnd: true,
		}
		node.Save()
		return map[string]string{}, nil
	}

	// Reading the page
	response, err := http.Get(url)
	if err != nil {
		log.Errorf("get failed, url: %s", url)
		return map[string]string{}, err
	}
	if response.StatusCode != http.StatusOK {
		log.Errorf("bad url: %s, status code: %d", url, response.StatusCode)
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
		if strings.HasPrefix(href, "http") { // http://xxxx/xxx
			link = href
		} else if strings.HasPrefix(href, "#") || strings.HasPrefix(href, ".") { // #index  ./index.html
			if strings.HasSuffix(url, "/") {
				link = url + href
			} else {
				link = url + "/" + href
			}
		} else if strings.HasPrefix(href, "/") { // /index.html
			if strings.HasSuffix(settings.Starting, "/") {
				link = settings.Starting + href[1:]
			} else {
				link = settings.Starting + href
			}
		} else { // index.html
			if strings.HasSuffix(url, "/") {
				link = url + href
			} else {
				link = url + "/" + href
			}
		}
		next = append(next, models.ChildPointer{
			URL:   link,
			Value: s.Text(),
		})
		log.Infof("link %s, text %s", link, s.Text())
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
		settings.Starting: "entry page",
	})
}
