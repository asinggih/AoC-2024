package day02

import readInput
import kotlin.math.abs

enum class Trend {
    UP,
    DOWN,
    STEADY
}

val MIN_THRESHOLD = 1
val MAX_THRESHOLD = 3

fun isWithinLimit(numA: Int, numB:Int): Boolean {
    val diff = abs(numA-numB)
    return diff in MIN_THRESHOLD..MAX_THRESHOLD
}

fun getState(numA: Int, numB:Int): Trend {
    return when {
        numB > numA -> Trend.UP
        numA > numB -> Trend.DOWN
        else        -> Trend.STEADY
    }
}

fun getProblematicIndex(levels: List<Int>) : Int? {
    var currentTrend: Trend? = null
    for (idx in 0 until levels.size-1) {
        val firstNum = levels[idx]
        val secondNum = levels[idx+1]

        val state = getState(firstNum, secondNum)

        // TREND CHECK
        if (state == Trend.STEADY) {
            return idx
        }

        val validTrend = currentTrend?.let { it == state }
            ?: run {
                currentTrend = state
                true
            }

        if (!validTrend) {
            return idx
        }

        // WITHIN LIMIT CHECK
        if(!isWithinLimit(firstNum, secondNum)) {
            return idx
        }
    }
    return null
}

fun areValidLevels(levels: List<Int>) : Boolean {
    var currentTrend: Trend? = null
    for (idx in 0 until levels.size-1) {
        val firstNum = levels[idx]
        val secondNum = levels[idx+1]

        val state = getState(firstNum, secondNum)

        // TREND CHECK
        if (state == Trend.STEADY) {
            return false
        }

        val validTrend = currentTrend?.let { it == state }
            ?: run {
                currentTrend = state
                true
            }

        if (!validTrend) {
            return false
        }

        // WITHIN LIMIT CHECK
        if(!isWithinLimit(firstNum, secondNum)) {
            return false
        }
    }
    return true
}

fun part1(input: List<String>): Int {
    // key is true(safe) and false(unsafe)
    // value is the count of how many times it occured
    val result = mutableMapOf<Boolean, Int>(
        true to 0,
        false to 0
    )

    input.forEach { report ->
        val levels = report.split(" ").map { it.toInt() }
        val areValidLevels = areValidLevels(levels)
        result[areValidLevels] = result.getOrDefault(areValidLevels, 0) + 1
    }

    return result.getOrDefault(true, 0)
}

fun part2(input: List<String>): Int {
    // key is true(safe) and false(unsafe)
    // value is the count of how many times it occured
    val result = mutableMapOf(
        true to 0,
        false to 0
    )

    input.forEach { report ->
        val levels = report.split(" ").map { it.toInt() }.toMutableList()
        val problematicIdx = getProblematicIndex(levels)

        val areValidLevels =  problematicIdx?.let {

            // Not proud with this approach tbh :(
            // Search around the problematic index to see if it can work
            val newListA = levels.filterIndexed{ index, _ -> index != problematicIdx }
            val newListB = levels.filterIndexed{ index, _ -> index != problematicIdx - 1}
            val newListC = levels.filterIndexed{ index, _ -> index != problematicIdx + 1 }

            val bruteForced = setOf(
                areValidLevels(newListA),
                areValidLevels(newListB),
                areValidLevels(newListC)
            )

            true in bruteForced

        } ?: areValidLevels(levels)

        result[areValidLevels] = result.getOrDefault(areValidLevels, 0) + 1
    }

    return result.getOrDefault(true, 0)
}

fun main() {
    // test if implementation meets criteria from the description, like:
    val testInput = readInput("day02/sample_input")
    val input = readInput("day02/input")

    check(part1(testInput).also { println("Part 1 sample input : ${it}") } == 2)
    check(part1(input).also { println("Part 1 input : ${it}") } == 321)
    println()
    check(part2(testInput).also { println("Part 2 sample input : ${it}") } == 4)
    check(part2(input).also { println("Part 2 sample input : ${it}") } == 386)

}