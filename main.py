import input
import random
import itertools
def toKB(maze, KB, ih, iw, state):
    sentence = []
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            # Not diag of maze
            if i != j:
                ii = i + ih
                jj = j + iw
                if validCell(ii, jj, len(maze)):
                    sentence.append(state + str(ii) + str(jj))
    KB.append(sentence)
    return KB
def getAllAdj(maze, ih, iw):
    res = []
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            # Not diag of maze
            if i != j:
                ii = i + ih
                jj = j + iw
                if validCell(ii, jj, len(maze)):
                    res.append(list((ii, jj)))
    return res

def validCell(i, j, shape):
    return 0 <= i and i < shape and 0 <= j and j < shape

def Resolution(KB, alpha):
    clauses = KB.copy()
    not_alpha = alpha.replace('~', '')
    clauses.append(not_alpha)
    new = []
    while True:
        # Tổ hợp chập 2
        for pair_clauses in itertools.combinations(clauses, 2):
            resolvents = Resolve(pair_clauses)

def Resolve(pair_clauses):
    pass

if __name__ == '__main__':
    # maze = input.inputFile("map1.txt", "r")
    maze = input.inputFile("maptab.txt", "r")

    # Count the number of gold
    # TODO

    # Count the number of wumpus
    # TODO

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
    while True:
        cur_states = maze[i_agent][j_agent]
        if cur_states == 'P' or cur_states == 'W':
            print("LOSE")
            break
        else:
            KB.append(['~P' + str(i_agent) + str(j_agent)])
            KB.append(['~W' + str(i_agent) + str(j_agent)])
            state = [s for s in cur_states]
            for i in range(len(state)):
                if state[i] == 'B':
                    KB = toKB(maze, KB, i_agent, j_agent, 'P')
                elif state[i] == 'S':
                    KB = toKB(maze, KB, i_agent, j_agent, 'W')
                elif state[i] == 'G':
                    score += 100
            allAdj = getAllAdj(maze, i_agent, j_agent)
            for i in range(len(allAdj)):
                # KB ^ ~alpha
                check = Resolution(KB, '~P' + str(allAdj[i][0]) + str(allAdj[i][1]))
                




