import copy
import time
import numpy

# seenPuzzles will check for duplicates, and improve runtime significantly
# outputArray hold string outputs for all nodes visited in order from algorithm
# outputArray will be outputted to file at end of code, to prevent clutter on terminal
seenPuzzles = []
outputArray = []


def createBoard(puzzleType):
    if puzzleType == "1":
        # Run standard board, given depth 24.
        returnBoard = [[1, 6, 7], [5, 0, 3], [4, 8, 2]]
        return returnBoard

    else:
        # Accept nxn board of any type from the user.
        s1 = input("Please enter the number of rows\n")
        s1 = int(s1)
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
    # Uses double for loop, checks if element in passed in node is where it should be
    # Compares this using variable "start" which has the correct first element ->
    # -> in every board, and increments accordingly
    # misplacedCount = counter for how many are in wrong position
    start = 1
    misplacedCount = 0
    for i in range(len(node.board)):
        for j in range(len(node.board[i])):
            if node.board[i][j] != start:
                misplacedCount += 1
            start += 1
    return misplacedCount - 1  # Won't count the blank tile


def manhattanCalculator(node, goalNode):
    # Function used to calculate heuristic using Manhattan distance
    # Generally, Manhattan is the sum of how far a tile is from it's goal ->
    # -> state in the x and y direction. Direction doesn't matter ->
    # -> use absolute value when finding the difference in both x and y dir.
    # Find what value is at the [i][j] tile, and then find that in our "goal state"
    # Then computes distance. Can be optimized
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


def possibleExpansions(puzzle, searchType, goalFinale):
    # General expansion function, will check if blank tile is on any edge
    # If it is, don't expand towards the direction of the edge it's near; this is purpose of flags
    # If flag is true for direction, make a new puzzle, do the swap in that direction
    # Then, make sure it's not a duplicate node, and if it's not, add it to possibleNodes queue to return
    # If misplaced tiles or Manhattan distance, put proper cost at end of each node in possibleNodes queue
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
        if temp1 not in seenPuzzles:
            temp11 = node(temp1, puzzle.depth+1, 0)
            possibleNodes.append(temp11)
            seenPuzzles.append(temp1)
    if flag_goDown == 1:
        temp2 = copy.deepcopy(puzzle.board)
        x = zeroLoc[0] + 1
        y = zeroLoc[1]
        swap1 = puzzle.board[x][y]
        temp2[x][y] = 0
        temp2[x-1][y] = swap1
        if temp2 not in seenPuzzles:
            temp22 = node(temp2, puzzle.depth+1, 0)
            possibleNodes.append(temp22)
            seenPuzzles.append(temp2)
    if flag_goLeft == 1:
        temp3 = copy.deepcopy(puzzle.board)
        x = zeroLoc[0]
        y = zeroLoc[1] - 1
        swap3 = puzzle.board[x][y]
        temp3[x][y] = 0
        temp3[x][y+1] = swap3
        if temp3 not in seenPuzzles:
            temp33 = node(temp3, puzzle.depth+1, 0)
            possibleNodes.append(temp33)
            seenPuzzles.append(temp3)
    if flag_goRight == 1:
        temp4 = copy.deepcopy(puzzle.board)
        x = zeroLoc[0]
        y = zeroLoc[1] + 1
        swap4 = puzzle.board[x][y]
        temp4[x][y] = 0
        temp4[x][y-1] = swap4
        if temp4 not in seenPuzzles:
            temp44 = node(temp4, puzzle.depth+1, 0)
            possibleNodes.append(temp44)
            seenPuzzles.append(temp4)
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
    # Node class used for holding important variables necessary for ->
    # -> a given puzzle state, and helps deal with diff. search algos.
    # self.board = arrangement of tiles for this node
    # self.depth = depth of this arrangement's node from the top
    # self.cost = to be updated based on heuristic, standard (UCS) = 0
    def __init__(self, board, depth, cost):
        self.board = board
        self.depth = depth
        self.cost = cost


def generalSearch(state, searchType, goalFinale):
    # Frontier will be the queue of nodes; top will have next node to visit
    # Iterations variable will be used to print how many nodes were expanded
    # maxQueueSize will determine how much space is needed to run algo.
    # Search type 1 = UCS, 2 = Misplaced tile, 3 = Manhattan
    # While loop condition: repeat cases until node is found or no solution.
    # Inside while loop: node to expand will always be on top; top depends on queueing function for later iterations
    # Inside while loop: lambda function used to sort frontier based on node's depth + cost
    frontier = []
    global iterations
    iterations = 0
    global maxQueueSize
    maxQueueSize = 0
    frontier.append(state)
    seenPuzzles.append(state.board)
    while (len(frontier) != 0):
        iterations += 1
        if (len(frontier) > maxQueueSize):
            maxQueueSize = len(frontier)
        node = frontier.pop(0)
        outputArray.append("The best node to expand with a g(n) = " + str(node.depth) +
                           " and h(n) = " + str(node.cost) + " is..." + str(node.board))
        if (node.board == goalFinale):
            print("Found the goal state!!\nTo solve this problem the search algorithm expanded a total of " +
                  str(iterations) + " nodes.")
            print("The maximum number of nodes in the queue at anytime was " +
                  str(maxQueueSize) + " nodes.")
            print("The depth of the goal node was " + str(node.depth) + ".")
            return node
        # Following equivalent to pseudocode in class:
        # nodes = QUEUEING-FUNCTION(nodes, EXPAND(node, problem.OPERATORS))
        if searchType == "1":
            frontier.extend(possibleExpansions(node, searchType, goalFinale))
        elif searchType == "2":
            frontier.extend(possibleExpansions(node, searchType, goalFinale))
            frontier.sort(key=lambda x: (x.depth + x.cost, x.depth))
        elif searchType == "3":
            frontier.extend(possibleExpansions(node, searchType, goalFinale))
            frontier.sort(key=lambda x: (x.depth + x.cost, x.depth))


def main():
    # Main function, mostly used to initiate program
    # Also outputs to file order in which nodes were visited (for tracing)
    # Also creates "goalFinale," which is the desired solution state ->
    # -> for nxn user input puzzle
    print("Welcome to Swastyak's 8-puzzle solver.")
    puzzleType = input("Type “1” to use a default puzzle, or “2” to enter own puzzle.\n")
    boardd = createBoard(puzzleType)
    test = node(boardd, 0, 0)
    cnt = 1
    goalFinale = copy.deepcopy(test.board)
    for i in range(len(goalFinale)):
        for j in range(len(goalFinale[i])):
            goalFinale[i][j] = cnt
            cnt += 1
    goalFinale[-1][-1] = 0
    print("This was the input board. " + str(test.board))
    print("This is the goal board. " + str(goalFinale))
    searchType = input(
        "Enter choice of algorithm. 1 for Uniform Cost, 2 for Misplaced Tile, 3 for Manhattan Distance\n")
    print("Starting with beginning state of: " + str(test.board) + "\nTimer will be turned on now.")
    start_time = time.time()
    dn = generalSearch(test, searchType, goalFinale)
    print("Total runtime was " + str(time.time() - start_time) + " seconds.")
    print("Finished with goal state of: " + str(dn.board))
    print("Outputting order in which nodes were visited to output.txt...")
    with open('output.txt', 'w') as f:
        for i in range(len(outputArray)):
            if i == 0:
                print(
                    outputArray[i] + " Please ignore h(n) for first case, all nodes are initialized with 0. \
                    \nThe node never hits the while loop, it is the special first case.", file=f)
            else:
                print(outputArray[i], file=f)


main()
