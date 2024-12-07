package day04

import readInput


val TARGET_CHARS = setOf(
    listOf('X', 'M', 'A', 'S'),
    listOf('S', 'A', 'M', 'X'),
)

fun horizontalSearchCount(searchScope: List<Char>): Int {
    val charCollections = searchScope.windowed(4)
    return charCollections.count { it in TARGET_CHARS }
}

fun transpose(matrix: List<List<Char>>): List<List<Char>> {
    return matrix[0].indices.map { col ->
        matrix.map { row -> row[col] }
    }
}

private fun handleDiagonalRightCount(
    charList:List<List<Char>>,
    xLen: Int,
    yLen: Int
) : Int {
    var diagonalCountRight = 0
    for (i in 0..xLen) {
        for (j in 0..yLen) {
            runCatching {
                val currentCharList = listOf(
                    charList[i][j],
                    charList[i + 1][j + 1],
                    charList[i + 2][j + 2],
                    charList[i + 3][j + 3],
                )
                if (currentCharList in TARGET_CHARS) {
                    diagonalCountRight += 1
                }
            }
        }
    }
    return diagonalCountRight
}

private fun handleDiagonalLeftCount(
    charList:List<List<Char>>,
    xLen: Int,
    yLen: Int
) : Int {
    var diagonalCountLeft = 0
    for (i in 0..xLen) {
        for (j in yLen downTo 3) {
            runCatching {
                val currentCharList = listOf(
                    charList[i][j],
                    charList[i + 1][j - 1],
                    charList[i + 2][j - 2],
                    charList[i + 3][j - 3],
                )

                if (currentCharList in TARGET_CHARS) {
                    diagonalCountLeft += 1
                }
            }
        }
    }
    return diagonalCountLeft
}

/*
       [M, M, M, S, X, X, M, A, S, M]
       [M, S, A, M, X, M, S, M, S, A]
       [A, M, X, S, X, M, A, A, M, M]
       [M, S, A, M, A, S, M, S, M, X]
       [X, M, A, S, A, M, X, A, M, M]
       [X, X, A, M, M, X, X, A, M, A]
       [S, M, S, M, S, A, S, X, S, S]
       [S, A, X, A, M, A, S, A, A, A]
       [M, A, M, M, M, X, M, M, M, M]
       [M, X, M, X, A, X, M, A, S, X]
    */
fun part1(input: List<String>): Int {

    val charList = input.map { it.toList() }

    var horizontalCount = 0
    for (chars in charList) {
        horizontalCount += horizontalSearchCount(chars)
    }

    var verticalCount = 0
    val transposedCharlist = transpose(charList)
    for (chars in transposedCharlist) {
        verticalCount += horizontalSearchCount(chars)
    }

    val xLen = charList[0].size
    val yLen = charList.size

    val diagonalCountRight = handleDiagonalRightCount(charList, xLen, yLen)
    val diagonalCountLeft = handleDiagonalLeftCount(charList, xLen, yLen)

    return horizontalCount + verticalCount + diagonalCountLeft + diagonalCountRight
}

val TARGET_CHARS_2ND = setOf(
    listOf('M', 'A', 'S'),
    listOf('S', 'A', 'M'),
)

fun part2(input: List<String>): Int {

    val charList = input.map { it.toList() }

    val xLen = charList[0].size
    val yLen = charList.size

    var count = 0
    for (i in 0..xLen) {
        for (j in 0..yLen) {
            runCatching {
                val diagRight = listOf(
                    charList[i][j],
                    charList[i+1][j+1],
                    charList[i+2][j+2]
                )
                val diagLeft = listOf(
                    charList[i+2][j],
                    charList[i+1][j+1],
                    charList[i][j+2]
                )
                if (diagRight in TARGET_CHARS_2ND && diagLeft in TARGET_CHARS_2ND) {
                    count += 1
                }
            }
        }
    }

    return count
}

fun main() {

    val testInput = readInput("day04/sample_input")
    val input = readInput("day04/input")

    check(part1(testInput).also { println("Part 1 sample input : ${it}") } == 18)
    check(part1(input).also { println("Part 1 input : ${it}") } == 2514)
    println()
    check(part2(testInput).also { println("Part 2 sample input : ${it}") } == 9)
    check(part2(input).also { println("Part 2 input : ${it}") } == 1888)


}
