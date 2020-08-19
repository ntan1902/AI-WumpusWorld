def inputFile(filename, mode):
    maze = []
    try:
        with open(filename, mode) as f:
            # Input size
            size = int(f.readline())

            # Input maze
            # for _ in range(size * size):
            #     d = f.readline()
            #     maze.append(list(map(str, d.split('.'))))
            d = f.read().splitlines()
            for i in range(len(d)):
                maze.append(list(map(str, d[i].split('.'))))

    except IOError as err:
        print(err)

    return maze








