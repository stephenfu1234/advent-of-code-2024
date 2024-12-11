import time

def solve(filename):
    start_time = int(time.time() * 1000)

    # for line in open(filename).read().splitlines():
    #     dir, dist = line.split()
    raw_input = open(filename).read()

    # read into a list of lists, split by new line and then by space using list comprension
    maze = [[int(j) for j in list(i)] for i in raw_input.split('\n')]
    
    # add border to avoid having to handle out of bounds
    add_border_to_maze(maze)

    start_locations = []
    for row_idx, row in enumerate(maze):
        for col_idx, col in enumerate(row):
            if col == 0:
                start_locations.append((row_idx, col_idx))

    # print(start_locations)

    scores = []
    for location in start_locations:
        visited = []
        trail_heads = []       
        move(maze, location, visited, trail_heads)
        scores.append(len(set(trail_heads)))

    # print(scores)
    print(sum(scores))

    end_time = int(time.time() * 1000)
    print(f'Time taken for {filename} (ms): {end_time - start_time}')

def move(maze, location, visited, trail_heads):
    for dy, dx in [(-1,0), (0,1), (1,0), (0,-1)]:
        height = maze[location[0]][location[1]]

        new_location = (location[0] + dy, location[1] + dx)
        new_height = maze[new_location[0]][new_location[1]]

        visited.append(location)

        if new_location in visited:
            continue

        if new_height == height + 1:
            if new_height == 9:
                # print('found trailhead at', new_location)
                trail_heads.append(new_location)
                continue
            else:
                # print('moving from', location, height, 'to', new_location, new_height)
                move(maze, new_location, visited, trail_heads)
        else:
            # print('cannot move from', location, height, 'to', new_location, new_height)
            continue

def add_border_to_maze(maze):
    # add left and right border
    for row in maze:
        row.insert(0, '-1')
        row.append('-1')

    # add top border
    maze.insert(0, len(maze[0]) * ['-1']) 
    # add bottom border
    maze.append(maze[0])

solve('test.txt')
solve('input.txt')