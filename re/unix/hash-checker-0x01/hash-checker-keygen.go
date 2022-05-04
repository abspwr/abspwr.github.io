package main

import (
	"fmt"
	"os"
	"strconv"
)

func isNum(input string) bool {
	_, err := strconv.Atoi(input)
	return err == nil
}

func main() {

	if len(os.Args) != 2 || len(os.Args[1]) != 6 || !isNum(os.Args[1]) {
		fmt.Println("Usage: ", os.Args[0], "xxxx")
		return
	}

	input := os.Args[1]

	//input := "231337"

	n := len(input)
	init := [6]uint64{1, 0, 0, 0, 0, 0}

	// initialize the rest of the magic values, these are always the same for init array
	// init := [6]uint64{0x1, 0x83, 0x4309, 0x224d9b, 0x118db651, 0x228a4e1d}
	for i := 1; i < n; i++ {
		init[i] = (init[i-1] * 0x83) % 0x3b9aca09
	}
	//fmt.Printf("init array: %x\n", init)

	hash := uint64(input[0])
	for j := 1; j < n; j++ {
		// hash = hash + (uint64(input[j])%0x3b9aca09)*init[j]%0x3b9aca09 // ghidra decompiler
		// remove unecessary mod and parentheses - simplify
		hash = hash + uint64(input[j])*init[j]%0x3b9aca09
	}
	//fmt.Printf("hash: %x\n", hash)

	if hash == 0x3c0431a5 {
		fmt.Println("Key is valid!")
	} else {
		fmt.Println("Wrong key!")
	}
}
