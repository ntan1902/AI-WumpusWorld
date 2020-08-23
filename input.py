def inputFile(filename, mode):
    maze = []
    try:
        with open(filename, mode) as f:
            # Input size
            size = int(f.readline())
            d = f.read().splitlines()
            for i in range(len(d)):
                # maze.append(list(map(str, d[i].split('.'))))
                maze.append(list(map(str, d[i].split('\t'))))


    except IOError as err:
        print(err)

    return maze








