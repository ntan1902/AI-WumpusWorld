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
                resolvents = sorted(resolvents, key=lambda x:x[-1])
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
    for i in range(len(resolvents)):
        for j in range(len(resolvents)):
            if (resolvents[i] == ('-' + resolvents[j])) or ('-' + resolvents[i] == resolvents[j]):
                return True
    return False

def checkSubset(a, b):
    count = 0
    for a_ in a:
        for b_ in b:
            if a_ == b_:
                count += 1
                break

    if count == len(a):
        return True
    else:
        return False

def not_in(a, b):
    for i in range (len(b)):
        if(a == b[i]):
            return False
    return True

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

def findPossibleMove(KB, allAdj, visited):
    possible_move = []
    previous_move = []
    for i in range(len(allAdj)):
        position_xy = str(allAdj[i][0]) + str(allAdj[i][1])
        # KB ^ -alpha
        checkP = Resolution(KB, '-P' + position_xy)
        checkW = Resolution(KB, '-W' + position_xy)

        if ((checkP == True) and (checkW == True)):
            possible_move.append([allAdj[i][0], allAdj[i][1]])

    for possible in possible_move.copy():
        if possible in visited:
            previous_move.append(possible)
            possible_move.remove(possible)

    return possible_move, previous_move

def findImpossibleMove(KB, allAdj):
    impossible_move = []
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
            if ['W' + position_xy] not in KB:
                KB.append(['W' + position_xy])
                KB.append(['-P' + position_xy])


        if ((checkP == True) or (checkW == True)):
            impossible_move.append([allAdj[i][0], allAdj[i][1]])

    return impossible_move, KB

def findRandomMove(KB, allAdj, impossible_move, previous_move):
    while True:
        i = random.randint(0, len(allAdj) - 1)
        if (allAdj[i] not in impossible_move) and (allAdj[i] not in previous_move):
            return allAdj[i]

if __name__ == '__main__':
    # maze = input.inputFile("map1.txt", "r")
    maze = input.inputFile("maptab4.txt", "r")
    # Count the number of gold and wumpus
    countG = 0
    countW = 0
    for i in range(len(maze)):
        for j in range(len(maze)):
            if ("G" in maze[i][j]):
                countG += 1
            if ("W" in maze[i][j]):
                countW += 1
    i_agent = 0
    j_agent = 0
    # while True:
    #     i_agent, j_agent = random.randint(0, len(maze) - 1), random.randint(0, len(maze) - 1)
    #     if maze[i_agent][j_agent] != 'P' and maze[i_agent][j_agent] != 'W':
    #         break
    print(f"Start position for Agent: {i_agent + 1, j_agent + 1}")
    print(f"Room: {maze[i_agent][j_agent]}")

    KB = []
    score = 0
    gold_collect = 0
    visited = []
    path = []
    count_possible_move = 0

    while True:
        cur_states = maze[i_agent][j_agent]
        visited.append([i_agent, j_agent])

        if [i_agent, j_agent] in path:
            path.pop(-1)
        else:
            path.append([i_agent, j_agent])

        if cur_states == 'P' or cur_states == 'W':
            score -= 10000
            print("LOSE")
            print(f"Score: {score}")
            break
        else:
            allAdj = getAllAdj(maze, i_agent, j_agent)
            KB.append(['-P' + str(i_agent) + str(j_agent)])
            KB.append(['-W' + str(i_agent) + str(j_agent)])
            state = [s for s in cur_states]
            for j in range(len(state)):

                # Breeze
                if state[j] == 'B':
                    clause = createClause('P', allAdj)
                    if clause not in KB:
                        KB.append(clause)

                    if 'S' not in state:
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
                    score += 100
                    gold_collect += 1
                    if(gold_collect == countG):
                        print("WIN")
                        print(visited)
                        print(path)
                        break

                # Empty
                elif state[j] == '-':
                    KB = addClauseToKB(KB, '-P', allAdj)
                    KB = addClauseToKB(KB, '-W', allAdj)

            # Find possible move
            possible_move, previous_move = findPossibleMove(KB, allAdj, visited)
            count_possible_move += len(possible_move)


            if len(possible_move) > 0:
                for i in range(len(possible_move)):
                    if (not_in(possible_move[i], visited) == True):
                        i_agent, j_agent = possible_move[i]
                        count_possible_move -= 1
                        score -= 10
                        break

            else:
                # Random move or go back

                # Find impossible move, update KB
                impossible_move, KB = findImpossibleMove(KB, allAdj)

                # Go back
                if count_possible_move > 0:
                    i_agent, j_agent = previous_move[0]
                    score -= 10
                    count_possible_move -= 1

                # Random move
                else:
                    i_agent, j_agent = findRandomMove(KB, allAdj, impossible_move, previous_move)
                    score -= 10




