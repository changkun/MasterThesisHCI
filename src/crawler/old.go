package old

func crawl(URL string, link chan string, finish chan bool) {
	resp, err := http.Get(URL)
	defer func() {
		finish <- true
	}()

	if err != nil {
		log.Info("ERROR: Failed to crawl \"" + URL + "\"")
		return
	}
	defer resp.Body.Close()
	sourceCode, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return
	}
	sourceCode = string(SrouceCode)

	doc, err := goquery.NewDocumentFromReader(resp.Body)
	if err != nil {
		log.Debug("URL: %s fail. Error: %s", URL, err.Error())
		return
	}

	doc.Find("a").Each(func(i int, s *goquery.Selection) {
		href, ok := s.Attr("href")
		if ok {
			_, err := url.ParseRequestURI(href)
			if err != nil {
				char := href[0]
				if char == '/' {
					link <- URL + href
				} else {
					link <- URL + "/" + href
				}
			}
		}
	})
	doc.Find("input").Each(func(i int, s *goquery.Selection) {
		href, ok := s.Attr("href")
		if ok {
			_, err := url.ParseRequestURI(href)
			if err != nil {
				char := href[0]
				if char == '/' {
					link <- URL + href
				} else {
					link <- URL + "/" + href
				}
			}
		}
	})
	doc.Find("textarea").Each(func(i int, s *goquery.Selection) {
		href, ok := s.Attr("href")
		if ok {
			_, err := url.ParseRequestURI(href)
			if err != nil {
				char := href[0]
				if char == '/' {
					link <- URL + href
				} else {
					link <- URL + "/" + href
				}
			}
		}
	})
	doc.Find("div").Each(func(i int, s *goquery.Selection) {
		href, ok := s.Attr("href")
		if ok {
			_, err := url.ParseRequestURI(href)
			if err != nil {
				char := href[0]
				if char == '/' {
					link <- URL + href
				} else {
					link <- URL + "/" + href
				}
			}
		}
	})

}

func seed(urls map[string]bool) {
	foundUrls := make(map[string]bool)
	chURL := make(chan string)
	chFinished := make(chan bool)

	defer func() {
		close(chURL)
		close(chFinished)
	}()

	dos := 0
	for url, do := range urls {
		if do {
			dos++
			go crawl(url, chURL, chFinished)
		}
	}

	// Subscribe to both channels
	for c := 0; c < dos; {
		select {
		case url := <-chURL:
			log.Info("url: ", url)
			foundUrls[url] = true
		case <-chFinished:
			c++
		}
	}

	log.Info("Found", len(foundUrls), "unique urls:")
	if depth < settings.MaxDepth {
		depth++
		for url := range foundUrls {

			var node models.Node
			uuid, _ := uuid.NewRandom()

			if !strings.Contains(url, settings.Region) {
				node = models.Node{
					Label:       uuid.String(),
					Type:        "link",
					Value:       url,
					Description: "",
					SrouceCode:
					IsEnd:       true,
					Next:        "",
				}
				// insert into database
				db.GetInstance().Mongo.C(db.Node).Upsert(bson.M{}, node)
				foundUrls[url] = false
				continue
			}

			node = models.Node{
				Label:       uuid.String(),
				Type:        "link",
				Value:       url,
				Description: "",
				IsEnd:       false,
				Next:        "",
			}

			// insert into database
			db.GetInstance().Mongo.C(db.Node).Upsert(bson.M{}, node)
		}
		seed(foundUrls)
	}
}
