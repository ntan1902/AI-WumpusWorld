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


if __name__ == '__main__':
    # maze = input.inputFile("map1.txt", "r")
    maze = input.inputFile("maptab.txt", "r")

    # Count the number of gold and wumpus
    # TODO
    countG = 0
    countW = 0
    for i in range(len(maze)):
        for j in range(len(maze)):
            if ("G" in maze[i][j]):
                countG += 1
            if ("W" in maze[i][j]):
                countW += 1

    # while True:
    #     x_agent, y_agent = random.randint(0, len(maze) - 1), random.randint(0, len(maze) - 1)
    #     if maze[x_agent][y_agent] != 'P' and maze[x_agent][y_agent] != 'W':
    #         break
    # print(f"Start position for Agent: {x_agent + 1, y_agent + 1}")
    # print(f"Room: {maze[x_agent][y_agent]}")
    i_agent = 0
    j_agent = 0
    KB = []
    score = 0
    gold_collect = 0
    visited = []

    while True:
        cur_states = maze[i_agent][j_agent]
        if cur_states == 'P' or cur_states == 'W':
            print("LOSE")
            break
        else:
            allAdj = getAllAdj(maze, i_agent, j_agent)
            KB.append(['-P' + str(i_agent) + str(j_agent)])
            KB.append(['-W' + str(i_agent) + str(j_agent)])
            state = [s for s in cur_states]
            for j in range(len(state)):
                clause = []
                if state[j] == 'B':
                    for i in range(len(allAdj)):
                        clause.append('P' + str(allAdj[i][0]) + str(allAdj[i][1]))

                        if len(state) == 1:
                            KB.append(['-W' + str(allAdj[i][0]) + str(allAdj[i][1])])

                    KB.append(clause)

                elif state[j] == 'S':
                    for i in range(len(allAdj)):
                        clause.append('W' + str(allAdj[i][0]) + str(allAdj[i][1]))
                        if len(state) == 1:
                            KB.append(['-P' + str(allAdj[i][0]) + str(allAdj[i][1])])
                    KB.append(clause)

                elif state[j] == 'G':
                    score += 100
                    gold_collect+= 1
                    if(gold_collect == countG):
                        print("WIN")
                        break

                elif state[j] == '-':
                    for i in range(len(allAdj)):
                    # KB = toKB(maze, KB, i_agent, j_agent, '-P')
                        KB.append(['-P' + str(allAdj[i][0]) + str(allAdj[i][1])])
                        KB.append(['-W' + str(allAdj[i][0]) + str(allAdj[i][1])])


            visited.append([i_agent, j_agent])
            possible_move = []
            count_move = 0
            for i in range(len(allAdj)):
                # KB ^ -alpha
                checkP = Resolution(KB, '-P' + str(allAdj[i][0]) + str(allAdj[i][1]))
                checkW = Resolution(KB, '-W' + str(allAdj[i][0]) + str(allAdj[i][1]))

                if ((checkP == True) and (checkW == True)):
                    possible_move.append([allAdj[i][0],allAdj[i][1]])
                    count_move += 1

            if(count_move > 1):
                for i in range(count_move):
                    new_i_j = possible_move[i]
                    if (not_in(new_i_j, visited) == True):
                        i_agent = new_i_j[0]
                        j_agent = new_i_j[1]
                        break
                    else:
                            count_move -= 1
            else:
                i_agent = visited[0][0]
                j_agent = visited[0][1]
