package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

const targetNum = 9

type Location struct {
	row int
	col int
}

func readInput(name string) ([][]int, [][]int) {

	filePath := fmt.Sprintf("%s.txt", name)

	file, err := os.Open(filePath)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	var matrix [][]int
	var startLoc [][]int
	//var visited [][]bool

	scanner := bufio.NewScanner(file)

	count := 0
	for scanner.Scan() {
		input := scanner.Text()
		parts := strings.Split(input, "")

		var row []int
		var boolRow []bool
		for idx, c := range parts {
			num, _ := strconv.Atoi(c)

			row = append(row, num)

			// also record the start location
			if num == 0 {
				loc := []int{count, idx}
				startLoc = append(startLoc, loc)
			}

			boolRow = append(boolRow, false)

		}
		matrix = append(matrix, row)
		//visited = append(visited, boolRow)
		count += 1
	}

	return matrix, startLoc
}

func isWithinBounds(row int, col int, maxRow int, maxCol int) bool {
	if row >= 0 && row < maxRow &&
		col >= 0 && col < maxCol {
		return true
	}
	return false
}

func isValid(
	row int, col int,
	maxRow int, maxCol int,
	prevNode int, currentNode int,
	visited map[string]bool,
) bool {

	isInsideBox := isWithinBounds(row, col, maxRow, maxCol)
	isGraduallyInc := prevNode+1 == currentNode

	targetLoc := strconv.Itoa(row) + strconv.Itoa(col)
	hasBeenVisited := visited[targetLoc]

	return isInsideBox && isGraduallyInc && !hasBeenVisited
}

var visited = make(map[string]bool)
var globalCount = 0

func runDFS(matrix [][]int, rowStart int, colStart int, path [][]int) bool {

	rowMax := len(matrix[0])
	colMax := len(matrix)

	targetLoc := strconv.Itoa(rowStart) + strconv.Itoa(colStart)
	visited[targetLoc] = true
	path = append(path, []int{rowStart, colStart})

	currentNum := matrix[rowStart][colStart]

	// base case
	if currentNum == targetNum {
		globalCount += 1
		//return true
	}

	up := []int{-1, 0}
	down := []int{1, 0}
	left := []int{0, -1}
	right := []int{0, 1}
	searchScope := [][]int{up, down, left, right}

	// Search around the current loc
	for _, loc := range searchScope {
		offsetRow := loc[0]
		offsetCol := loc[1]

		newRow := rowStart + offsetRow
		newCol := colStart + offsetCol

		//fmt.Println("newRow is")
		//fmt.Println(newRow)
		//fmt.Println("newCol is")
		//fmt.Println(newCol)

		prevNode := matrix[rowStart][colStart]
		// isWithinBounds(row, col, maxRow, maxCol)
		var currentNode *int
		//currentNode = nil
		if isWithinBounds(newRow, newCol, rowMax, colMax) {
			value := matrix[newRow][newCol]
			currentNode = &value
		} else {
			//println("here B")
			continue
		}

		if isValid(
			newRow, newCol,
			rowMax, colMax,
			prevNode, *currentNode,
			visited,
		) {
			if runDFS(matrix, newRow, newCol, path) {
				return true
			}
		}
	}
	//println
	// Backtrack
	path = path[:len(path)-1]
	delete(visited, targetLoc)

	return false
}

// func runDFS(matrix [][]int, rowStart int, colStart int, path [][]int) bool {
func solvePart1(matrix [][]int, startLoc [][]int) {

	//for _, startPoint := range startLoc {
	//	r := startPoint[0]
	//	c := startPoint[0]
	//
	//	runDFS(matrix, r, c, [][]int{})
	//}

	//visited := make(map[string]bool)
	r := startLoc[0][0]
	c := startLoc[0][1]
	//fmt.Println("start loc is")
	//fmt.Println(r)
	//fmt.Println(c)
	//fmt.Println()
	runDFS(matrix, r, c, [][]int{})

	fmt.Println(globalCount)
	//fmt.Println()
	//fmt.Println(startLoc)
	fmt.Println("visited")
	fmt.Println(visited)

	//var out []int
	//for idx := range visited {
	//	fmt.Println(idx)
	//	combo := strings.Split(idx, "")
	//	//fmt.Printf("a:%s b:%s", combo[0], combo[1])
	//	a, _ := strconv.Atoi(combo[0])
	//	b, _ := strconv.Atoi(combo[1])
	//	out = append(out, matrix[a][b])
	//}
	//
	//fmt.Println(out)

}

func main() {

	matrix, startLoc := readInput("sample_input")
	//lookupTable, allUpdates := readInput("input")
	//fmt.Println(matrix)
	//fmt.Println()
	//fmt.Println(startLoc)

	fmt.Println("Part 1")
	fmt.Println("startloc")
	fmt.Println(startLoc)
	solvePart1(matrix, startLoc)
	//fmt.Println(part1Sample.validMidPointSum)
	//part1 := solvePart1(lookupTable, allUpdates)
	//fmt.Println(part1.validMidPointSum)

	fmt.Println()

	//fmt.Println("Part 2")
	//part2Sample := solvePart2(lookupTable, part1Sample.invalidList)
	//fmt.Println(part2Sample)
	//part2 := solvePart2(lookupTable, part1.invalidList)
	//fmt.Println(part2)

}
