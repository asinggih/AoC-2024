package main

import (
	"fmt"
	"io"
	"log"
	"os"
	"regexp"
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

func solvePart1(longText string) int {
	re := regexp.MustCompile(`mul\((\d{1,3}),(\d{1,3})\)`)

	matches := re.FindAllStringSubmatch(longText, -1) // -1 means find maximum number of matches

	total := 0
	for _, combo := range matches {
		firstNum, _ := strconv.Atoi(combo[1])
		secondNum, _ := strconv.Atoi(combo[2])

		total += firstNum * secondNum
	}

	return total
}

func solvePart2(longText string) int {
	re := regexp.MustCompile(`(do\(\)|don't\(\))|mul\((\d{1,3}),(\d{1,3})\)`)

	matches := re.FindAllStringSubmatch(longText, -1) // -1 means find maximum number of matches

	total := 0
	doMultiply := true
	for _, combo := range matches {
		// [[mul(2,4)  2 4] [don't() don't()  ] [mul(5,5)  5 5] [mul(11,8)  11 8] [do() do()  ] [mul(8,5)  8 5]]
		action := combo[1]
		firstNum := combo[2]
		secondNum := combo[3]

		if firstNum != "" && secondNum != "" && doMultiply {
			a, _ := strconv.Atoi(firstNum)
			b, _ := strconv.Atoi(secondNum)
			total += a * b
		}

		if action == "don't()" {
			doMultiply = false
		} else if action == "do()" {
			doMultiply = true
		}

	}

	return total
}

func main() {

	sampleText := readFileAsString("sample_input")
	text := readFileAsString("input")

	fmt.Println("Part 1")
	part1Sample := solvePart1(sampleText)
	fmt.Println(part1Sample) // 161
	part1 := solvePart1(text)
	fmt.Println(part1) // 189600467

	fmt.Println()

	fmt.Println("Part 2")
	part2Sample := solvePart2(sampleText)
	fmt.Println(part2Sample) // 48
	part2 := solvePart2(text)
	fmt.Println(part2) // 107069718

}
