import time
import copy

def solve(filename, max_bytes):
    start_time = int(time.time() * 1000)

    raw_input = open(filename).read()

    # read into a list of lists, split by new line and then by space using list comprension
    bytes = [[int(j) for j in i.split(',')] for i in raw_input.split('\n')]

    memory_space, height, width = create_memory_space(bytes, max_bytes)

    # start location is 1,1 as we added a maze border
    find_shortest_path(memory_space, (1,1), (height,width))
    
    end_time = int(time.time() * 1000)
    print(f'Time taken for {filename} (ms): {end_time - start_time}')

def find_shortest_path(maze, start, end):
    draw_individual_moves = False
    directions = [(-1,0),(0,1),(0,-1),(1,0)]
    to_visit = [(start[0], start[1], [], 0)]
    seen = {}
    iterations = 1
    
    while to_visit != []:
        iterations += 1
        # r, c, visited, cost = to_visit.pop() # LIFO for deep first search
        r, c, visited, cost = to_visit.pop(0) # FIFO for breadth first search
        
        if draw_individual_moves:
            input("Press the enter for next move") 
            draw_maze(maze, visited)

        # if we've been here before and it was cheaper then stop
        if (r, c) in seen and seen[(r,c)] <= cost:
            continue
        else:
            # track where we have currently visited and what the current cost to reach here is
            new_visited = copy.deepcopy(visited)
            new_visited.append((r, c))
            seen[(r, c)] = cost

            if (r, c) == end:
                print('found end location with cost', cost)
                print('route taken')
                draw_maze(maze, new_visited)
                continue
                print('finished with lowest cost', seen[end], 'after', iterations, 'iterations')
                return # for immediate stop

            for dr, dc in directions:
                if maze[r+dr][c+dc] == '#':
                    continue
            
                # now add it to the stack of places to next visit and increment the step cost
                to_visit.append((r+dr, c+dc, new_visited, cost+1))

    print('finished with lowest cost', seen[end], 'after', iterations, 'iterations')
    
def draw_maze(maze, steps_taken):
    completed_maze = copy.deepcopy(maze)

    if steps_taken != None:
        for r, c in steps_taken:
            completed_maze[r][c] = 'O'

    for line in completed_maze:
        print(''.join(line))

def create_memory_space(bytes, max_bytes):
    height = 0
    width = 0
    for c, r in bytes:
        if c > width: width = c
        if r > height: height = r
    
    # add 1 to account for zero based index
    height += 1
    width += 1

    memory_space = [['.'] * width for _ in range(height)]
    
    for idx, byte in enumerate(bytes):
        if idx < max_bytes:
            r = byte[1]
            c = byte[0]
            memory_space[r][c] = '#'

    add_border_to_maze(memory_space)
    
    return memory_space, height, width

def add_border_to_maze(maze):
    # add left and right border
    for row in maze:
        row.insert(0, '#')
        row.append('#')

    # add top border
    maze.insert(0, len(maze[0]) * ['#']) 
    # add bottom border
    maze.append(maze[0])

solve('test.txt', 12)
solve('input.txt', 1024)