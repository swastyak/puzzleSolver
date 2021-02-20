import copy
import time
import numpy
import sys

seenListsOfLists = []
outputArray = []


def createBoard(puzzleType):
    if puzzleType == "1":  # Runs algorithm with preset puzzle
        returnBoard = [[0, 7, 2], [4, 6, 1], [3, 5, 8]]  # depth 24
        return returnBoard

    else:
        s1 = input("Please enter the number of rows\n")
        s1 = int(s1)  # Runs algorithm for user input state
        appendString = ""
        for i in range(s1):
            tempString = input("Enter the number " + str(i + 1) +
                               " row. Use space between numbers. Press Enter when finished. Use zero for blank.\n")
            appendString += tempString + ' '
        finalList = list(appendString.split(" "))
        finalList.pop()
        for i in range(len(finalList)):
            finalList[i] = int(finalList[i])
        return numpy.reshape(finalList, (s1, s1)).tolist()


def findValueInBoard(puzzle, value):
    # Double for loop to find coordinates of value in the given puzzle
    for i in range(len(puzzle.board)):
        for j in range(len(puzzle.board[i])):
            if puzzle.board[i][j] == value:
                return [i, j]


def misplacedTileCalculator(node):
    start = 1
    misplacedCount = 0
    # Double for loop, at every index will see if the value matches what it should be
    for i in range(len(node.board)):
        for j in range(len(node.board[i])):
            if node.board[i][j] != start:
                misplacedCount += 1
            start += 1
    return misplacedCount - 1  # Won't count the blank tile


def possibleExpansions(puzzle, searchType, goalFinale):
    possibleNodes = []
    flag_goUp, flag_goLeft, flag_goRight, flag_goDown = 1, 1, 1, 1
    zeroLoc = findValueInBoard(puzzle, 0)
    if zeroLoc[0] == 0:
        flag_goUp = 0
    if zeroLoc[0] == len(puzzle.board) - 1:
        flag_goDown = 0
    if zeroLoc[1] == 0:
        flag_goLeft = 0
    if zeroLoc[1] == len(puzzle.board) - 1:
        flag_goRight = 0

    if flag_goUp == 1:
        temp1 = copy.deepcopy(puzzle.board)
        x = zeroLoc[0] - 1
        y = zeroLoc[1]
        swap1 = puzzle.board[x][y]
        temp1[x][y] = 0
        temp1[x+1][y] = swap1
        if temp1 not in seenListsOfLists:
            temp11 = node(temp1, puzzle.depth+1, 0)
            possibleNodes.append(temp11)
            seenListsOfLists.append(temp1)
    if flag_goDown == 1:
        temp2 = copy.deepcopy(puzzle.board)
        x = zeroLoc[0] + 1
        y = zeroLoc[1]
        swap1 = puzzle.board[x][y]
        temp2[x][y] = 0
        temp2[x-1][y] = swap1
        if temp2 not in seenListsOfLists:
            temp22 = node(temp2, puzzle.depth+1, 0)
            possibleNodes.append(temp22)
            seenListsOfLists.append(temp2)
    if flag_goLeft == 1:
        temp3 = copy.deepcopy(puzzle.board)
        x = zeroLoc[0]
        y = zeroLoc[1] - 1
        swap3 = puzzle.board[x][y]
        temp3[x][y] = 0
        temp3[x][y+1] = swap3
        if temp3 not in seenListsOfLists:
            temp33 = node(temp3, puzzle.depth+1, 0)
            possibleNodes.append(temp33)
            seenListsOfLists.append(temp3)
    if flag_goRight == 1:
        temp4 = copy.deepcopy(puzzle.board)
        x = zeroLoc[0]
        y = zeroLoc[1] + 1
        swap4 = puzzle.board[x][y]
        temp4[x][y] = 0
        temp4[x][y-1] = swap4
        if temp4 not in seenListsOfLists:
            temp44 = node(temp4, puzzle.depth+1, 0)
            possibleNodes.append(temp44)
            seenListsOfLists.append(temp4)
    if (searchType == "2"):
        for i in range(len(possibleNodes)):
            possibleNodes[i].cost = misplacedTileCalculator(possibleNodes[i])
    if (searchType == "3"):
        for i in range(len(possibleNodes)):
            goal = goalFinale
            goaB = node(goal, 0, 0)
            possibleNodes[i].cost = manhattanCalculator(possibleNodes[i], goaB)
    return possibleNodes


class node:
    def __init__(self, boardd, depthh, cost):
        self.board = boardd
        self.depth = depthh
        self.cost = cost


def manhattanCalculator(node, goalNode):
    sum = 0
    fake = 0
    for i in range(len(node.board)):
        for j in range(len(node.board[i])):
            if node.board[i][j] != 0:
                fake = node.board[i][j]
                coord = findValueInBoard(goalNode, fake)
                xpos = coord[0]
                ypos = coord[1]
                sum += abs(xpos - i) + abs(ypos - j)
    return sum


def generalSearch(state, searchType, goalFinale):
    # The following are declarations of variables used in the general search algorithm
    frontier = []  # Queue of nodes; top of frontier will have next node to visit
    global iterations
    iterations = 0  # Used to show how many nodes were expanded
    global maxQueueSize
    maxQueueSize = 0  # Used to determine how much space is needed to run algorithm
    frontier.append(state)
    seenListsOfLists.append(state.board)
    while (len(frontier) != 0):  # Will go until node found or no solution
        iterations += 1
        if (len(frontier) > maxQueueSize):
            maxQueueSize = len(frontier)
        # Node to expand will always be on top; top depends on queueing function for later iterations
        node = frontier.pop(0)
        # print("The best node to expand with a g(n) = " +
        #       str(node.depth) + " and h(n) = " + str(node.cost) + " is...")
        # print(node.board)
        # with open('output.txt', 'a') as f:
        #     print("The best node to expand with a g(n)=" + str(node.depth) +
        #           " and h(n)=" + str(node.cost) + " is ...", file=f)
        #     print(node.board, file=f)
        outputArray.append("The best node to expand with a g(n) = " + str(node.depth) +
                           " and h(n) = " + str(node.cost) + " is..." + str(node.board))
        if (node.board == goalFinale):
            print("This is the goal state!!\nTo solve this problem the search algorithm expanded a total of " +
                  str(iterations) + " nodes.")
            print("The maximum number of nodes in the queue at anytime was " +
                  str(maxQueueSize) + " nodes.")
            print("The depth of the goal node was " + str(node.depth) + ".")
            return node
        # queuing function, 1 for UFC, 2 for Misplaced tiles, 3 for Manhattan distance
        if searchType == "1":
            frontier.extend(possibleExpansions(node, searchType, goalFinale))
            # No special case to consider, sort frontier just based on expansion order
        elif searchType == "2":
            frontier.extend(possibleExpansions(node, searchType, goalFinale))
            # frontier.sort(key=lambda x: x.cost + x.depth, reverse=False)
            frontier.sort(key=lambda x: (x.depth + x.cost, x.depth))
            # what this lambda fxn allows us to do is sort all of the nodes
        elif searchType == "3":
            frontier.extend(possibleExpansions(node, searchType, goalFinale))
            frontier.sort(key=lambda x: (x.depth + x.cost, x.depth))


def main():
    print("Welcome to Bertie Woosters 8-puzzle solver.")
    puzzleType = input("Type “1” to use a default puzzle, or “2” to enter own puzzle.\n")
    boardd = createBoard(puzzleType)
    test = node(boardd, 0, 0)
    # print(len(test.board[0]))
    print("This is the goal board.")
    cnt = 1
    goalFinale = copy.deepcopy(test.board)
    for i in range(len(goalFinale)):
        for j in range(len(goalFinale[i])):
            goalFinale[i][j] = cnt
            cnt += 1
    goalFinale[-1][-1] = 0
    print(goalFinale)
    print("This was the input board.")
    print(test.board)
    searchType = input(
        "Enter choice of algorithm. 1 for Uniform Cost, 2 for Misplaced Tile, 3 for Manhattan Distance")
    print("Starting with beginning state of: " + str(test.board))
    start_time = time.time()
    dn = generalSearch(test, searchType, goalFinale)
    print("Total runtime was " + str(time.time() - start_time) + " seconds.")
    print("Finished with goal state of: " + str(dn.board))
    with open('output.txt', 'w') as f:
        for i in range(len(outputArray)):
            print(outputArray[i], file=f)


main()

