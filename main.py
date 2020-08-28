import input
import random
import itertools
def getAllAdj(maze, ih, iw):
    res = []
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            # Not diag of maze
            if i != j and i + j != 0:
                ii = i + ih
                jj = j + iw
                if validCell(ii, jj, len(maze)):
                    res.append(list((ii, jj)))
    return res

def validCell(i, j, shape):
    return 0 <= i and i < shape and 0 <= j and j < shape

def Resolution(KB, alpha):
    clauses = KB.copy()
    if '-' in alpha:
        not_alpha = [alpha.replace('-', '')]
    else:
        not_alpha = ['-' + alpha]
    clauses.append(not_alpha)
    new = []
    while True:
        # Tổ hợp chập 2
        for pair_clauses in itertools.combinations(clauses, 2):
            if isComplementaryClause(list(pair_clauses[0] + pair_clauses[1])):
                resolvents = Resolve(pair_clauses)
                if len(resolvents) == 0:
                    return True
                #resolvents = sorted(resolvents, key=lambda x:x[-1])
                if not(isComplementaryClause(resolvents)) and(resolvents not in clauses) and(resolvents not in new):
                    new.append(resolvents)

        if len(new) == 0:
            return False

        clauses = clauses + new
        new.clear()

def Resolve(pair_clauses):
    clauses_1 = pair_clauses[0].copy()
    clauses_2 = pair_clauses[1].copy()
    complementary_once = False
    for cl1 in pair_clauses[0]:
        for cl2 in pair_clauses[1]:
            if ((cl1 == ('-' + cl2)) or ('-' + cl1 == cl2)) and not(complementary_once):
                clauses_1.remove(cl1)
                clauses_2.remove(cl2)
                complementary_once = True

            if (cl1 == cl2):
                clauses_1.remove(cl1)
                break


    return list(clauses_1 + clauses_2)

def isComplementaryClause(resolvents):
    for pair_clauses in itertools.combinations(resolvents, 2):
        if (pair_clauses[0] == ('-' + pair_clauses[1])) or ('-' + pair_clauses[0] == pair_clauses[1]):
            return True
    return False

def createClause(query, allAdj):
    clause = []
    for i in range(len(allAdj)):
        position_xy = str(allAdj[i][0]) + str(allAdj[i][1])

        clause.append(query + position_xy)
    return clause

def addClauseToKB(KB, query, allAdj):
    for i in range(len(allAdj)):
        position_xy = str(allAdj[i][0]) + str(allAdj[i][1])

        if [query + position_xy] not in KB:
            KB.append([query + position_xy])
    return KB

def findPossibleMove(KB, allAdj, W_killed, countW):
    possible_move = []
    checkP = True
    checkW = True
    for i in range(len(allAdj)):
        position_xy = str(allAdj[i][0]) + str(allAdj[i][1])
        # KB ^ -alpha
        checkP = Resolution(KB, '-P' + position_xy)

        if W_killed != countW:
            checkW = Resolution(KB, '-W' + position_xy)

        if ((checkP == True) and (checkW == True)):
            possible_move.append([allAdj[i][0], allAdj[i][1]])


    return possible_move

def findImpossibleMove(KB, allAdj, maze, W_killed, countW):
    kill = 0
    for i in range(len(allAdj)):
        position_xy = str(allAdj[i][0]) + str(allAdj[i][1])
        # KB ^ -alpha
        checkP = Resolution(KB, 'P' + position_xy)
        checkW = Resolution(KB, 'W' + position_xy)

        if checkP == True:
            if ['P' + position_xy] not in KB:
                KB.append(['P' + position_xy])
                KB.append(['-W' + position_xy])


        if checkW == True:
            if ['P' + position_xy] not in KB:
                KB.append(['-P' + position_xy])

            # Kill
            maze[allAdj[i][0]][allAdj[i][1]] = '-'
            W_adj = getAllAdj(maze, allAdj[i][0], allAdj[i][1])

            #delete all S near the Wumbus
            for j in range(len(W_adj)):
                x_ = W_adj[j][0]
                y_ = W_adj[j][1]
                if (maze[x_][y_] == 'S'):
                    maze[x_][y_] = '-'
                elif (maze[x_][y_].__contains__('S')):
                    maze[x_][y_] = maze[x_][y_].replace('S', '')

            #delete all Wij in KB
            del_clauses = []
            for j in range(len(W_adj)):
                clauses = []
                Adj_of_W_adj = getAllAdj(maze,W_adj[j][0], W_adj[j][1])
                for k in range (len(Adj_of_W_adj)):
                    clauses.append('W' + str(Adj_of_W_adj[k][0]) + str(Adj_of_W_adj[k][1]))
                del_clauses.append(clauses)
            # for j in range(len(KB)):
            #     for k in range(len(del_clauses)):
            #         if (KB[j].__contains__(del_clauses[k])):
            #             KB[j].remove(del_clauses[k])
            for cl in del_clauses:
                if(KB.__contains__(cl)):
                    KB.remove(cl)
            kill += 1
            print(f"Kill Wumpus at {allAdj[i][0] + 1, allAdj[i][1] + 1} - 100 point")
            fo.write(f"Kill Wumpus at: {i_agent + 1, j_agent + 1} - 100 point\n")


    return KB, maze, kill


def updateKB(KB, cur_states, allAdj, W_killed, countW):
    isGold = False
    state = [s for s in cur_states]
    for j in range(len(state)):

        # Breeze
        if state[j] == 'B':
            clause = createClause('P', allAdj)
            if clause not in KB:
                KB.append(clause)

            if 'S' not in state and W_killed != countW:
                KB = addClauseToKB(KB, '-W', allAdj)


        # Stench
        elif state[j] == 'S':
            clause = createClause('W', allAdj)
            if clause not in KB:
                KB.append(clause)

            if 'B' not in state:
                KB = addClauseToKB(KB, '-P', allAdj)

        # Gold
        elif state[j] == 'G':
            isGold = True
            if (len(state) == 1):
                KB = addClauseToKB(KB, '-P', allAdj)
                if W_killed != countW:
                    KB = addClauseToKB(KB, '-W', allAdj)

        # Empty
        elif state[j] == '-':
            KB = addClauseToKB(KB, '-P', allAdj)
            if W_killed != countW:
                KB = addClauseToKB(KB, '-W', allAdj)
    return KB, isGold

if __name__ == '__main__':
    maze = input.inputFile("map4x4.txt", "r")
    # maze = input.inputFile("maptab4.txt", "r")
    # Count the number of gold and wumpus
    countG = 0
    countW = 0
    for i in range(len(maze)):
        for j in range(len(maze)):
            if ('G' in maze[i][j]):
                countG += 1
            if ('W' in maze[i][j]):
                countW += 1
    i_agent = 0
    j_agent = 0
    # while True:
    #     i_agent, j_agent = random.randint(0, len(maze) - 1), random.randint(0, len(maze) - 1)
    #     if maze[i_agent][j_agent] != 'P' and maze[i_agent][j_agent] != 'W':
    #         break

    with open("output.txt", 'wt') as fo:
        fo.write(f"Start position for Agent: {i_agent + 1, j_agent + 1}\n")
        fo.write(f"Room: {maze[i_agent][j_agent]}\n")
        print(f"Start position for Agent: {i_agent + 1, j_agent + 1}")
        print(f"Room: {maze[i_agent][j_agent]}")

        KB = []
        score = 0
        gold_collect = 0
        W_killed = 0
        visited = []
        path = []
        possible_move = []
        previous_move = []
        isFirstMove = True

        while True:
            print(f"Move to {(i_agent + 1, j_agent + 1)}")
            cur_states = maze[i_agent][j_agent]
            visited.append([i_agent, j_agent])

            if [i_agent, j_agent] in path:
                path.pop(-1)
            else:
                path.append([i_agent, j_agent])

            if cur_states == 'P' or cur_states == 'W':
                score -= 10000
                print("LOSE")
                fo.write("LOSE\n")
                break

            else:
                allAdj = getAllAdj(maze, i_agent, j_agent)
                if ['-P' + str(i_agent) + str(j_agent)] not in KB:
                    KB.append(['-P' + str(i_agent) + str(j_agent)])

                if ['-W' + str(i_agent) + str(j_agent)] not in KB and W_killed != countW:
                    KB.append(['-W' + str(i_agent) + str(j_agent)])

                KB, isGold = updateKB(KB, cur_states, allAdj, W_killed, countW)

                if isGold:
                    if len(cur_states) > 1:
                        maze[i_agent][j_agent] = maze[i_agent][j_agent].replace('G', '')

                    else:
                        maze[i_agent][j_agent] = maze[i_agent][j_agent].replace('G', '-')


                    score += 100
                    gold_collect += 1
                    print(f"Grab gold at: {i_agent + 1, j_agent + 1} + 100 point")
                    fo.write(f"Grab gold at: {i_agent + 1, j_agent + 1} + 100 point\n")

                    if gold_collect == countG and countW == W_killed:
                        print("Killed all Wumpus and Got all Gold")
                        fo.write("Killed all Wumpus and Got all Gold\n")
                        score -= (len(visited) - 1) * 10
                        break


                # Find possible move
                possible = findPossibleMove(KB, allAdj, W_killed, countW)
                # KB, maze, kill = findImpossibleMove(KB, allAdj, maze)
                # if kill > 0:
                #     score -= 100
                #     W_killed += kill
                # if (W_killed == countW and gold_collect == countG):
                #     print("Killed all Wumpus and Got all Gold")
                #     fo.write("Killed all Wumpus and Got all Gold\n")
                #     score -= (len(visited) - 1) * 10
                #     break

                newMove = False
                for i in range(len(possible)):
                    if possible[i] not in visited:
                        if possible[i] in possible_move:
                            possible_move.remove(possible[i])
                        possible_move.append(possible[i])
                        newMove = True


                if len(possible_move) > 0:
                    isFirstMove = False
                    if newMove:
                        previous_move.append(list((i_agent, j_agent)))
                        i_agent, j_agent = possible_move[-1]
                        possible_move.pop(-1)
                    else:
                        # Find impossible move, update KB
                        KB, maze, kill = findImpossibleMove(KB, allAdj, maze, W_killed, countW)
                        if kill > 0:
                            score -= 100
                            W_killed += kill
                        if (W_killed == countW and gold_collect == countG):
                            print("Killed all Wumpus and Got all Gold")
                            fo.write("Killed all Wumpus and Got all Gold\n")
                            score -= (len(visited) - 1) * 10
                            break
                        # Go back
                        i_agent, j_agent = previous_move[-1]
                        previous_move.pop(-1)



                else:

                    # Random for first move
                    if isFirstMove:
                        i = random.randint(0, len(allAdj) - 1)
                        i_agent, j_agent = allAdj[i]
                        isFirstMove = False
                    # Climb out of cave
                    else:
                        print(f"Climb out of the cave ")
                        fo.write(f"Climb out of the cave ")

                        # Go back
                        path.reverse()
                        goal = []
                        findGoal = False
                        for i in range(len(path)):
                            adjPath = getAllAdj(maze, path[i][0], path[i][1])
                            for j in range(len(adjPath)):
                                if adjPath[j] == visited[0]:
                                    goal.append(path[i].copy())
                                    goal.append(visited[0].copy())
                                    findGoal = True
                                    break
                            if findGoal:
                                break
                            else:
                                goal.append(path[i])
                        goal.pop(0)
                        visited += goal
                        score -= (len(visited) - 2) * 10

                        break

        for i in range(len(visited)):
            visited[i][0] += 1
            visited[i][1] += 1
        print(f"Score: {score}")
        print(f"Explored path: {visited}")
        fo.write(f"Score: {score}\n")
        fo.write(f"Explored path: {visited}\n")
    





