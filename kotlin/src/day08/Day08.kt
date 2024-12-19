package day08

import readInput
import kotlin.math.abs

private fun <T> getAllPairs(list: List<T>): List<Pair<T, T>> {
    val pairs = mutableListOf<Pair<T, T>>()
    for (i in list.indices) {
        for (j in i + 1 until list.size) {
            pairs.add(list[i] to list[j])
        }
    }
    return pairs
}

fun part1(matrix: List<String>) : Int {

    val antiNodes = mutableSetOf<Pair<Int,Int>>()

    val lookupTable = mutableMapOf<Char, MutableList<Pair<Int,Int>>>()

    val rowMax = matrix[0].length
    val colMax = matrix.size

    matrix.forEachIndexed { row, rows ->
        rows.forEachIndexed { col, _ ->
            val node = matrix[row][col]
            if (node != '.') {
                val listOfPairs = lookupTable.getOrPut(node) {
                    mutableListOf()
                }
                listOfPairs.add(Pair(row, col))
            }
        }
    }

    for ((_, listOfPairs) in lookupTable) {
        val uniquePairs = getAllPairs(listOfPairs)

        uniquePairs.forEach { nodes ->
            val firstAntiNodeLoc = getAntiNodeLoc(nodes.first, nodes.second, rowMax, colMax)
            firstAntiNodeLoc?.let { antiNodes.add(it) }

            val secondAntiNodeLoc = getAntiNodeLoc(nodes.second, nodes.first, rowMax, colMax)
            secondAntiNodeLoc?.let { antiNodes.add(it) }
        }

    }
    return antiNodes.size
}

private fun getAntiNodeLoc(
    nodeA: Pair<Int, Int>,
    nodeB: Pair<Int, Int>,
    rowMax: Int,
    colMax: Int
) : Pair<Int, Int>? {

    val diffs = Pair(
        abs(nodeA.first-nodeB.first),
        abs(nodeA.second-nodeB.second)
    )

    val anchorRow = nodeA.first
    val rowB = nodeB.first

    val antiNodeAnchorRow = if (anchorRow <= rowB) {
        anchorRow - diffs.first
    } else {
        anchorRow + diffs.first
    }

    val anchorCol = nodeA.second
    val colB = nodeB.second

    val antiNodeAnchorCol = if (anchorCol <= colB) {
        anchorCol - diffs.second
    } else {
        anchorCol + diffs.second
    }

    // antiNode location within bounds
    if (antiNodeAnchorCol in 0 until colMax &&
        antiNodeAnchorRow in 0 until rowMax
    ) {
        return Pair(antiNodeAnchorRow, antiNodeAnchorCol)
    }

    return null

}



fun part2(matrix: List<String>) : Int {

    val antiNodes = mutableSetOf<Pair<Int,Int>>()

    val lookupTable = mutableMapOf<Char, MutableList<Pair<Int,Int>>>()

    val antennaeLoc = mutableSetOf<Pair<Int,Int>>()

    val rowMax = matrix[0].length
    val colMax = matrix.size

    matrix.forEachIndexed { row, rows ->
        rows.forEachIndexed { col, _ ->
            val node = matrix[row][col]
            if (node != '.') {
                val listOfPairs = lookupTable.getOrPut(node) {
                    mutableListOf()
                }
                val nodeLoc = Pair(row, col)
                listOfPairs.add(nodeLoc)
                antennaeLoc.add(nodeLoc)
            }
        }
    }

    for ((_, listOfPairs) in lookupTable) {
        val uniquePairs = getAllPairs(listOfPairs)

        uniquePairs.forEach { nodes ->
            var firstNodeA = nodes.first
            var secondNodeA = nodes.second
            while (true) {
                getAntiNodeLoc(firstNodeA, secondNodeA, rowMax, colMax)?.let {
                    antiNodes.add(it)
                    secondNodeA = firstNodeA
                    firstNodeA = it
                } ?: break
            }


            var firstNodeB = nodes.second
            var secondNodeB = nodes.first
            while (true) {
                getAntiNodeLoc(firstNodeB, secondNodeB, rowMax, colMax)?.let {
                    antiNodes.add(it)
                    secondNodeB = firstNodeB
                    firstNodeB = it
                } ?: break
            }

        }

    }
    return (antiNodes + antennaeLoc).size
}

fun main() {

    val testInput = readInput("day08/sample_input")
    val input = readInput("day08/input")

    check(part1(testInput).also { println("Part 1 sample input : ${it}") } == 14)
    println(part1(input))
    check(part1(input).also { println("Part 1 input : ${it}") } == 320)
    println()

    check(part2(testInput).also { println("Part 2 sample input : ${it}") } == 34)
    println(part1(input))
    check(part2(input).also { println("Part 2 input : ${it}") } == 1157)
    println()


    println(part2(testInput))
    println(part2(input))


}
