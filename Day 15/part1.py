import time

# opportunity to refactor to generalised functions
def solve(filename):
    start_time = int(time.time() * 1000)

    raw_input = open(filename).read()

    # read into a list of lists, split by new line and then by space using list comprension
    data = [i.split('\n') for i in raw_input.split('\n\n')] #if i == to apply filtering

    grid = list(map(list, data[0]))
    moves = list(''.join(data[1]))
    start_location = None

    for row_idx, row in enumerate(grid):
        for col_idx, col in enumerate(row):
            if col == '@':
                start_location = (row_idx, col_idx)
    
    directions = {'^': (-1,0),'>': (0,1),'<': (0,-1),'v': (1,0)}

    r, c = start_location
    while moves != []:
        moved = False
        # get next move
        move = moves.pop(0)
        # print()
        # print('moving', move)
        # for line in grid:
        #     print(''.join(line))
        
        # get the delta change in location
        dr, dc = directions[move]

        # skip move if wall infront
        if grid[r + dr][c + dc] == '#':
            continue

        # move if empty space
        if grid[r + dr][c + dc] == '.':
            # clear old location
            grid[r][c] = '.'

            # update new location
            r += dr
            c += dc
            grid[r][c] = '@'
            continue

        # we must be pushing a box
        # get the locations of everything in front        
        if move == '^':
            col = [row[c] for row in grid]
            # find the position of the first . before current row.  This should be before the first #
            if '.' in col[:r] and list(reversed(col[:r])).index('.') < list(reversed(col[:r])).index('#'):
                moved = True
                idx = r - 1 - list(reversed(col[:r])).index('.')

                # remove the .
                col.pop(idx)

                # prepend a . to push the box along
                col.insert(r, ".")

                for row_idx, col_val in enumerate(col):
                    grid[row_idx][c] = col_val

        elif move == '>':
            # find the position of the first . after current col.  This should be before the first #
            if '.' in grid[r][c+1:] and grid[r].index('.', c) < grid[r].index('#', c):
                moved = True
                idx = grid[r].index('.', c)

                # remove the .
                grid[r].pop(idx)

                # prepend a . to push the box along
                grid[r].insert(c, ".")

        elif move == '<':
            # find the position of the first . before current col.  This should be before the first #
            if '.' in grid[r][:c] and list(reversed(grid[r][:c])).index('.') < list(reversed(grid[r][:c])).index('#'):
                moved = True
                idx = c - 1 - list(reversed(grid[r][:c])).index('.')

                # remove the .
                grid[r].pop(idx)

                # prepend a . to push the box along
                grid[r].insert(c, ".")

        elif move == 'v':
            col = [row[c] for row in grid]
            # find the position of the first . after current row.  This should be before the first #
            if '.' in col[r+1:] and col.index('.', r) < col.index('#', r):
                moved = True
                idx = col.index('.', r)

                # remove the .
                col.pop(idx)

                # prepend a . to push the box along
                col.insert(r, ".")

                for row_idx, col_val in enumerate(col):
                    grid[row_idx][c] = col_val

        # update new location
        if moved: 
            r += dr
            c += dc
    
        # print('after move')
        # for line in grid:
        #     print(''.join(line))

    # calculate score
    scores = []
    for row_idx, row in enumerate(grid):
        for col_idx, col in enumerate(row):
            if col == 'O':
                scores.append(100 * row_idx + col_idx)

    print(sum(scores))
    end_time = int(time.time() * 1000)
    print(f'Time taken for {filename} (ms): {end_time - start_time}')
    
solve('test.txt')
solve('test2.txt')
solve('input.txt')