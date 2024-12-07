package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"slices"
	"strconv"
	"strings"
)

func readInput(name string) (map[int]map[int]bool, [][]int) {

	filePath := fmt.Sprintf("%s.txt", name)

	file, err := os.Open(filePath)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	lookupTable := make(map[int]map[int]bool)

	var allUpdates [][]int

	scanner := bufio.NewScanner(file)
	isLookupTable := true

	for scanner.Scan() {
		input := scanner.Text()

		if input == "" {
			isLookupTable = false
			continue
		}

		if isLookupTable { // handling the lookup list
			parts := strings.Split(input, "|")
			key, _ := strconv.Atoi(parts[0])
			value, _ := strconv.Atoi(parts[1])

			if _, exists := lookupTable[key]; !exists {
				lookupTable[key] = make(map[int]bool)
				lookupTable[key][value] = true
			} else {
				lookupTable[key][value] = true
			}
		} else { // handling the updates list now
			parts := strings.Split(input, ",")
			var updatesList []int
			for _, value := range parts {
				intVal, _ := strconv.Atoi(value)
				updatesList = append(updatesList, intVal)
			}
			allUpdates = append(allUpdates, updatesList)

		}

	}

	return lookupTable, allUpdates
}

func anySetContentHasBeenSeen(set map[int]bool, seen map[int]bool) bool {
	for futureNumber := range set {
		if seen[futureNumber] {
			return true
		}
	}
	return false
}

type P1Wrapper struct {
	validMidPointSum int
	invalidList      [][]int
}

func solvePart1(lookupTable map[int]map[int]bool, allUpdates [][]int) P1Wrapper {

	seen := make(map[int]bool)

	var validUpdatesList [][]int
	var invalidUpdatesList [][]int

	for _, updatesList := range allUpdates {
		areValidUpdates := true
		for _, patch := range updatesList {

			setOfNums := lookupTable[patch]
			if anySetContentHasBeenSeen(setOfNums, seen) {
				areValidUpdates = false
				break
			}
			// add patch number to the seen cache
			seen[patch] = true
		}

		if areValidUpdates {
			validUpdatesList = append(validUpdatesList, updatesList)
		} else {
			invalidUpdatesList = append(invalidUpdatesList, updatesList)
		}

		// clear the seen cache
		seen = make(map[int]bool)
	}

	total := 0
	for _, updates := range validUpdatesList {
		midPointIdx := len(updates) / 2
		midPointValue := updates[midPointIdx]
		total += midPointValue
	}

	return P1Wrapper{
		validMidPointSum: total,
		invalidList:      invalidUpdatesList,
	}

}

func sort2(numList []int, lookupTable map[int]map[int]bool) {
	slices.SortFunc(numList, func(num1, num2 int) int {
		futureNums := lookupTable[num1]
		if _, exists := futureNums[num2]; !exists {
			return -1
		}
		if _, exists := lookupTable[num2]; !exists {
			return 1
		}
		return 0
	})
}

func solvePart2(lookupTable map[int]map[int]bool, allInvalidUpdates [][]int) int {

	total := 0
	for _, invalidUpdates := range allInvalidUpdates {

		sort2(invalidUpdates, lookupTable)

		midPointIdx := len(invalidUpdates) / 2
		midPointValue := invalidUpdates[midPointIdx]
		total += midPointValue
	}

	return total
}

func main() {

	sampleLookupTable, sampleAllUpdates := readInput("sample_input")
	lookupTable, allUpdates := readInput("input")

	fmt.Println("Part 1")
	part1Sample := solvePart1(sampleLookupTable, sampleAllUpdates)
	fmt.Println(part1Sample.validMidPointSum)
	part1 := solvePart1(lookupTable, allUpdates)
	fmt.Println(part1.validMidPointSum)

	fmt.Println()

	fmt.Println("Part 2")
	part2Sample := solvePart2(lookupTable, part1Sample.invalidList)
	fmt.Println(part2Sample)
	part2 := solvePart2(lookupTable, part1.invalidList)
	fmt.Println(part2)

}
