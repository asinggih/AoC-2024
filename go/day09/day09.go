package main

import (
	"fmt"
	"io"
	"log"
	"os"
	"strconv"
)

func readFileAsString(name string) string {

	filePath := fmt.Sprintf("%s.txt", name)

	file, err := os.Open(filePath)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	// Read the entire file into a string
	content, _ := io.ReadAll(file)

	return string(content)
}

func appendBlock(id int, size string, inflated []int) []int {
	limit, _ := strconv.Atoi(size)
	for i := 0; i < limit; i++ {
		inflated = append(inflated, id)
	}
	return inflated
}

func inflate(compressed string) []int {
	var inflated []int
	id := 0
	for idx, size := range compressed {
		if idx%2 == 0 {
			// file block
			// append id * size in the inflated slice
			inflated = appendBlock(id, string(size), inflated)
			id++
		} else {
			// free block
			// append -1 * slice in the inflated slice
			inflated = appendBlock(-1, string(size), inflated)
		}
	}
	//fmt.Println(inflated)
	return inflated
}

func pop(slice []int) (int, []int) {
	lastElement := slice[len(slice)-1]
	slice = slice[:len(slice)-1]
	return lastElement, slice
}

func compactor(inflatedList []int) []int {
	compactedSlice := make([]int, len(inflatedList))
	copy(compactedSlice, inflatedList)
	cutoffIdx := -1
	for idx, id := range compactedSlice {

		// stop condition
		if len(inflatedList) == idx {
			//compactedSlice[idx] = -9999
			cutoffIdx = idx
			break
		}

		if id == -1 {
			lastElement := -1
			for lastElement == -1 {
				poppedElement, poppedList := pop(inflatedList)
				inflatedList = poppedList
				if poppedElement != -1 {
					compactedSlice[idx] = poppedElement
				}
				lastElement = poppedElement
			}
		}
	}
	// Remove the unused trailing items
	compactedSlice = compactedSlice[0:cutoffIdx]

	//fmt.Println("Compacted:")
	//fmt.Println(compactedSlice)

	return compactedSlice
}

func checksum(compactedSlice []int) int {
	cs := 0
	for idx, id := range compactedSlice {
		cs += idx * id
	}
	return cs
}

func solvePart1(compressed string) int {
	//fmt.Println(compressed)
	inflatedSlice := inflate(compressed)
	compactedSlice := compactor(inflatedSlice)
	cs := checksum(compactedSlice)
	return cs
}

/*
	00...111...2...333.44.5555.6666.777.888899
	0099.111...2...333.44.5555.6666.777.8888..
	0099.1117772...333.44.5555.6666.....8888..
	0099.111777244.333....5555.6666.....8888..
	00992111777.44.333....5555.6666.....8888..
*/

type FreeSpace struct {
	size     int
	location int
}

func generateLookup(inflatedSlice []int) map[int]int {
	lookupTable := make(map[int]int)
	for _, item := range inflatedSlice {
		if item != -1 {
			if _, exists := lookupTable[item]; !exists {
				lookupTable[item] = 1
			} else {
				lookupTable[item]++
			}
		}
	}
	return lookupTable
}

func solvePart2(compressed string) int {
	//fmt.Println(compressed)
	inflatedSlice := inflate(compressed)
	fmt.Println(inflatedSlice)
	lookupTable := generateLookup(inflatedSlice)
	fmt.Println(lookupTable)

	compactedSlice := []int{0}
	cs := checksum(compactedSlice)
	return cs
}

func main() {

	sampleText := readFileAsString("day09/sample_input")
	text := readFileAsString("day09/input")

	fmt.Println("Part 1")
	part1Sample := solvePart1(sampleText)
	fmt.Println(part1Sample) // 1928
	part1 := solvePart1(text)
	fmt.Println(part1) // 6435922584968

	fmt.Println()

	fmt.Println("Part 2")
	part2Sample := solvePart2(sampleText)
	fmt.Println(part2Sample) // 48
	//part2 := solvePart2(text)
	//fmt.Println(part2) // 107069718

}
