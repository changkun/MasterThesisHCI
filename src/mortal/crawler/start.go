package crawler

import (
	"fmt"

	"github.com/changkun/mortal/utils"
)

// Explore ...
func Explore(URL string) error {
	domain, err := utils.GetDomain(URL)
	if err != nil {
		return err
	}
	fmt.Println(domain)
	return nil
}
