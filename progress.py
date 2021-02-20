import copy
import time

seenListsOfLists = []


def createBoard(puzzleType):
    if puzzleType == "1":
        # returnBoard = [[1, 6, 7], [5, 0, 3], [4, 8, 2]]
        # returnBoard = [[7, 1, 2], [4, 8, 5], [6, 3, 0]]
        # returnBoard = [[0, 7, 2], [4, 6, 1], [3, 5, 8]]  # depth 24
        # returnBoard = [[1, 8, 2], [0, 4, 3], [7, 6, 5]]
        returnBoard = [[8, 6, 7], [2, 5, 4], [3, 0, 1]]
        return returnBoard

    else:
        print("Enter your puzzle, use a zero to represent the blank.")
        s1 = input("Enter the first row, use space or tabs between numbers. Press Enter when finished.")
        s2 = input("Enter the second row, use space or tabs between numbers. Press Enter when finished.")
        s3 = input("Enter the third row, use space or tabs between numbers. Press Enter when finished.")


def findValueInBoard(puzzle, value):
    row = 0
    col = 0
    for i in range(len(puzzle.board)):
        for j in range(len(puzzle.board[i])):
            if puzzle.board[i][j] == value:
                row = i
                col = j
                arr = [row, col]
                return arr


def misplacedTileCalculator(node):
    start = 1
    misplacedCount = 0
    for i in range(len(node.board)):
        for j in range(len(node.board[i])):
            if node.board[i][j] != start:
                misplacedCount += 1
            start += 1
    return misplacedCount - 1


def possibleExpansions(puzzle, searchType):
    possibleNodes = []
    flag_goUp, flag_goLeft, flag_goRight, flag_goDown = 1, 1, 1, 1
    zeroLoc = findValueInBoard(puzzle, 0)
    if zeroLoc[0] == 0:
        flag_goUp = 0
    if zeroLoc[0] == 2:
        flag_goDown = 0
    if zeroLoc[1] == 0:
        flag_goLeft = 0
    if zeroLoc[1] == 2:
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
            goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
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


def generalSearch(state, searchType):
    nodesQueue = []
    global iterations
    iterations = 0
    nodesQueue.append(state)
    seenListsOfLists.append(state.board)
    while (len(nodesQueue) != 0):
        iterations += 1
        node = nodesQueue.pop(0)
        if (node.board == [[1, 2, 3], [4, 5, 6], [7, 8, 0]]):
            print("\nDepth of found node\n")
            print(node.depth)
            print("\nTotal expanded nodes\n")
            print(iterations)
            print("\n")
            return node
        # queuing function
        if searchType == "1":
            nodesQueue.extend(possibleExpansions(node, searchType))
        elif searchType == "2":
            nodesQueue.extend(possibleExpansions(node, searchType))
            nodesQueue.sort(key=lambda x: x.cost + x.depth, reverse=False)
        elif searchType == "3":
            nodesQueue.extend(possibleExpansions(node, searchType))
            nodesQueue.sort(key=lambda x: (x.depth + x.cost, x.depth))


def main():
    print("Welcome to Bertie Woosters 8-puzzle solver.")
    puzzleType = input("Type “1” to use a default puzzle, or “2” to enter own puzzle.\n")
    boardd = createBoard(puzzleType)
    test = node(boardd, 0, 0)
    print(test.board)
    searchType = input("Enter choice of algorithm. 1 for Uniform Cost,\
    2 for Misplaced Tile, 3 for Manhattan Distance")
    start_time = time.time()
    generalSearch(test, searchType)
    print("--- %s seconds ---" % (time.time() - start_time))


main()

