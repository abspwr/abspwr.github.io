// abspwr
package main

import (
	"fmt"
	"math"
)

func sumDigs(n uint64) uint64 {
	if n == 0 {
		return 0
	} else {
		return n%10 + sumDigs(n/10)
	}
}

func printDigs(n uint64) {
	if n == 0 {
		fmt.Println()
	} else {
		printDigs(n / 10)
		fmt.Print(n % 10)
	}
}

func main() {
	n := 6
	t := uint64(0x32) // 50
	max := uint64(math.Pow10(n))
	i := uint64(0)

	for i = 1; i < max; i++ {
		if sumDigs(i) == t {
			printDigs(i)
		}
	}
}
