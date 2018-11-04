package db

import (
	"fmt"

	"github.com/changkun/mortal/utils"
)

// IsDomainExist ...
func IsDomainExist(URL string) bool {
	domain, err := utils.GetDomain(URL)
	fmt.Println(domain, err)
	return false
}
