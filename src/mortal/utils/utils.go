package utils

import (
	"fmt"
	"net/url"
)

// GetDomain ...
func GetDomain(URL string) (domain string, err error) {
	u, err := url.Parse(URL)
	if err != nil {
		return "", fmt.Errorf("ERROR DOMAIN: %v", err)
	}
	return u.Host, nil
}
