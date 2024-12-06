import time

def read_file(filename):
    return open(filename).read()

def solve(filename):
    start_time = int(time.time() * 1000)

    raw_input = read_file(filename)

    # read into a list of lists, split by new line and then by space using list comprension
    maze = [list(i) for i in raw_input.split('\n')] #if i == to apply filtering

    add_border_to_maze(maze)
    
    start_position = next(((i, row.index('^')) for i, row in enumerate(maze) if '^' in row), None)
    next_direction_dict = {'^': '>', '>': 'v', '<': '^', 'v': '<'}

    finished = False
    positions_visited = [[start_position]]
    current_position = start_position
    current_direction = '^'

    # should be refactored to avoid duplication
    while not finished:
        # find the first # or E based on current location and direction faced
        # if moving horizontal then we can slice the list
        if current_direction == '>':
            # if facing east then get all the steps from current position to east side of the board
            current_row = maze[current_position[0]]
            # find first obstacle in direction faced
            obstacle_idx = current_row.index('#', current_position[1]) if '#' in current_row[current_position[1]:] else -1

            # move X steps to the obstacle
            if obstacle_idx != -1 :
                steps_to_move = obstacle_idx - current_position[1] - 1
            else:
                steps_to_move = len(maze) - current_position[1] - 2 # account for 2 edges
            new_position = (current_position[0], current_position[1] + steps_to_move)
            positions_visited.append(get_visited_positions(True, current_position, new_position))
            current_position = new_position

        if current_direction == '<':
            # if facing west then get all the steps from current position to west side of the board
            current_row = maze[current_position[0]]
            # find first obstacle in direction faced
            indices = [i for i, x in enumerate(current_row[:current_position[1]]) if x == "#"][-1:]
            obstacle_idx = get_index(indices)   
        
            # move X steps to the obstacle
            if obstacle_idx != -1 :
                steps_to_move =  current_position[1] - obstacle_idx - 1
            else:
                steps_to_move = current_position[1] - 1 # account for left edge
            new_position = (current_position[0], current_position[1] - steps_to_move)
            positions_visited.append(get_visited_positions(True, current_position, new_position))
            current_position = new_position
        
        if current_direction == '^':
            # if facing north then get all the steps from current position to north side of the board
            current_col = [row[current_position[1]] for row in maze][:current_position[0]]
            # find first obstacle in direction faced
            indices = [i for i, x in enumerate(current_col[:current_position[0]]) if x == "#"][-1:]
            obstacle_idx = get_index(indices)  

            # move X steps to the obstacle
            if obstacle_idx != -1 :
                steps_to_move = current_position[0] - obstacle_idx - 1
            else:
                steps_to_move = current_position[0] - 1 # account for top edge
            new_position = (current_position[0] - steps_to_move, current_position[1])
            positions_visited.append(get_visited_positions(False, current_position, new_position))
            current_position = new_position

        if current_direction == 'v':
            # if facing south then get all the steps from current position to south side of the board
            current_col = [row[current_position[1]] for row in maze]
            # find first obstacle in direction faced
            obstacle_idx = current_col.index('#', current_position[0]) if '#' in current_col[current_position[0]:] else -1

            # move X steps to the obstacle
            if obstacle_idx != -1 :
                steps_to_move = obstacle_idx - current_position[0] - 1
            else:
                steps_to_move = len(maze) - current_position[0] - 2 # account for 2 edges
            new_position = (current_position[0] + steps_to_move, current_position[1])
            positions_visited.append(get_visited_positions(False, current_position, new_position))
            current_position = new_position
        
        current_direction = next_direction_dict[current_direction]

        # if current location is E then exit
        if obstacle_idx == -1:
            finished = True
    
    flattened_positions_visited = [item for sublist in positions_visited for item in sublist]
    print(len(set(flattened_positions_visited)))

    end_time = int(time.time() * 1000)
    print(f'Time taken for {filename} (ms): {end_time - start_time}')

def get_index(indices):
    if indices == []:
        return -1
    return indices[0]

def get_visited_positions(is_horizontal, old_position, new_position):
    if is_horizontal:
        if old_position[1] < new_position[1]:
            return [(old_position[0], old_position[1] + x) for x in range(abs(old_position[1] - new_position[1]) + 1)]
        return [(old_position[0], old_position[1] - x) for x in range(abs(old_position[1] - new_position[1]) + 1)]

    if old_position[0] < new_position[0]:
        return [(old_position[0] + x, old_position[1]) for x in range(abs(old_position[0] - new_position[0]) + 1)]
    return [(old_position[0] - x, old_position[1]) for x in range(abs(old_position[0] - new_position[0]) + 1)]
    

def add_border_to_maze(maze):
    # add left and right border
    for row in maze:
        row.insert(0, 'E')
        row.append('E')

    # add top border
    maze.insert(0, len(maze[0]) * ['E']) 

    # add bottom border
    maze.append(maze[0])

solve('test.txt')
solve('input.txt')