import input
import random
if __name__ == '__main__':
    maze = input.inputFile("map1.txt", "r")
    while True:
        x_agent, y_agent = random.randint(0, len(maze) - 1), random.randint(0, len(maze) - 1)
        if maze[x_agent][y_agent] != 'P' or maze[x_agent][y_agent] != 'W':
            break
    print(f"Start position for Agent: {x_agent + 1, y_agent + 1}, Room: {maze[x_agent][y_agent]}")
