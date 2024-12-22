import time
import copy

# now that boxes have double width, we will explicitly track their location and use these to draw on the grid
# could do with some refactoring
def solve(filename):
    start_time = int(time.time() * 1000)

    draw_individual_moves = False
    raw_input = open(filename).read()
    expanded_input = expand_input(raw_input)
    data = [i.split('\n') for i in expanded_input.split('\n\n')]

    grid = list(map(list, data[0]))
    moves = list(''.join(data[1]))

    start_location = None
    box_locations = {}
    wall_locations = {}

    start_location = setup_locations(grid, box_locations, wall_locations)

    if draw_individual_moves:
        print(start_location)
        print('box locations', box_locations.keys())
        print('wall locations', wall_locations.keys())

    directions = {'^': (-1,0),'>': (0,1),'<': (0,-1),'v': (1,0)}

    r, c = start_location
    while moves != []:
        if draw_individual_moves:
            input("Press the enter for next move") 

        move = moves.pop(0)
        
        # get the delta change in location
        dr, dc = directions[move]
        new_r = r + dr
        new_c = c + dc

        if draw_individual_moves:
            print()
            print('current location', r, c, ', trying to move', move, 'to', new_r, new_c)
            draw_grid(grid, box_locations, r, c)

        # skip move if wall infront
        if (new_r, new_c) in wall_locations:
            continue

        # move if empty space
        if (new_r, new_c) not in box_locations and (new_r, new_c - 1) not in box_locations:
            # update new location
            r += dr
            c += dc
            
            if draw_individual_moves:
                print('after move')
                draw_grid(grid, box_locations, r, c)
            continue
        
        # we must be pushing a box
        # find all connected boxes
        boxes = []
        can_move = can_move_all_linked_boxes(wall_locations, box_locations, r, c, dr, dc, boxes)
        
        # update new location if we managed to push
        if can_move:
            r, c = attempt_move(box_locations, boxes, r, c, dr, dc)
        
        if draw_individual_moves:
            print('after move')
            draw_grid(grid, box_locations, r, c)
            
    print('final grid')
    draw_grid(grid, box_locations, r, c)
        
    # calculate score
    scores = []
    for r, c in box_locations:
        scores.append(100 * r + c)

    print()
    print(sum(scores))
    end_time = int(time.time() * 1000)
    print(f'Time taken for {filename} (ms): {end_time - start_time}')

def can_move_all_linked_boxes(wall_locations, box_locations, r, c, dr, dc, boxes_to_push):
    # if pushing up or down
    # print('location', r, c, 'pushing in direction', dr, dc)
    if (dr != 0):
        # if we are pushing [
        box_to_push = None
        if (r + dr, c) in box_locations:
            box_to_push = (r + dr, c)
        
        # if we are pushing ], then its a box to the left
        if (r + dr, c - 1) in box_locations:
            box_to_push = (r + dr, c - 1)

        if box_to_push is not None:
            boxes_to_push.append(box_to_push)
            # add all other boxes that this box may also push
            if (r + dr, c) in box_locations:
                can_move_all_linked_boxes(wall_locations, box_locations, r + dr, c, dr, dc, boxes_to_push)
                can_move_all_linked_boxes(wall_locations, box_locations, r + dr, c + 1, dr, dc, boxes_to_push)
            elif (r + dr, c - 1) in box_locations:
                can_move_all_linked_boxes(wall_locations, box_locations, r + dr, c, dr, dc, boxes_to_push)
                can_move_all_linked_boxes(wall_locations, box_locations, r + dr, c - 1, dr, dc, boxes_to_push)
            # print('boxes to push', set(boxes_to_push))

        # check if any of the linked boxes have an obstacle in its way
        # if so, then we can't push any of the boxes so return empty list of boxes to push
        for box_r, box_c in boxes_to_push:
            if (box_r + dr, box_c) in wall_locations or (box_r + dr, box_c +1 ) in wall_locations:
                return False
            
        # if no further boxes and not a wall then it must be empty space to move into
        # stop the recursion and return
        return True

    else:
        # pushing left and right
        # get next box and then iteratively get the next touching
        box_to_push = None
        # try push the box to the left
        if dc == -1:
            if (r, c + (dc * 2)) in box_locations:
                box_to_push = (r, c + (dc * 2))
        elif dc == 1:
            # try push the box to the left
            if (r, c + 1) in box_locations:
                box_to_push = (r, c + 1)
        

        if box_to_push is not None:
            # print('adding box to push', box_to_push)
            boxes_to_push.append(box_to_push)
            # add all other boxes that this box may also push.  Need to move 2 squares to account for extra width
            # try push the box to the left
            can_move_all_linked_boxes(wall_locations, box_locations, r, c + (dc * 2), dr, dc, boxes_to_push)            
            # print('boxes to push', set(boxes_to_push))

        # check if any of the linked boxes have an obstacle in its way
        # if so, then we can't push any of the boxes so return empty list of boxes to push
        for box_r, box_c in boxes_to_push:
            if dc == -1:
                if (box_r, box_c + dc) in wall_locations:
                    return False
            elif dc == 1:
                if (box_r, box_c + (dc * 2)) in wall_locations:
                    return False

        # if no further boxes and not a wall then it must be empty space to move into
        # stop the recursion and return
        return True

def attempt_move(box_locations, boxes, r, c, dr, dc):
    if boxes != []: 
        # print('all boxes to push', boxes)
        r += dr
        c += dc

        # remove old box locations
        for box_r, box_c in set(boxes):
            box_locations.pop((box_r, box_c))
        # then add the new locations
        for box_r, box_c in set(boxes):
            box_locations[(box_r + dr, box_c + dc)] = True

    return r, c

def draw_grid(grid, box_locations, current_r, current_c):
    new_grid = copy.deepcopy(grid)
    
    for r, c in box_locations.keys():
        new_grid[r][c] = '['
        new_grid[r][c+1] = ']'

    new_grid[current_r][current_c] = '@'

    for line in new_grid:
        print(''.join(line))

def setup_locations(grid, box_locations, wall_locations):
    start_location = None
    for row_idx, row in enumerate(grid):
        for col_idx, col in enumerate(row):
            if col == '@':
                start_location = (row_idx, col_idx)
                grid[row_idx][col_idx] = '.'
            elif col == '[':
                box_locations[(row_idx, col_idx)] = True
                grid[row_idx][col_idx] = '.'
                grid[row_idx][col_idx+1] = '.'
            elif col == '#':
                wall_locations[(row_idx, col_idx)] = True
    return start_location

def expand_input(raw_input):
    expanded_input = raw_input.replace('#', '##')
    expanded_input = expanded_input.replace('O', '[]')
    expanded_input = expanded_input.replace('.', '..')
    expanded_input = expanded_input.replace('@', '@.')    
    return expanded_input

# solve('test.txt')
# solve('test2.txt')
# solve('test3.txt')
solve('input.txt')