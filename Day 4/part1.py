import time

def read_file(filename):
    return open(filename).read()

def solve(filename):
    start_time = int(time.time() * 1000)

    # for line in open(filename).read().splitlines():
    #     dir, dist = line.split()
    raw_input = read_file(filename)

    # read into a list of lists, split by new line and then by space using list comprension
    data = [list(i) for i in raw_input.split('\n')]

    # add border thickness of 3 to avoid needing to handle out of bounds exceptions during text scanning
    add_border_to_puzzle(data)

    # list of scan directions (north, north east, east etc)
    directions = [(-1,0), (-1,1), (0,1), (1,1), (1,0), (1,-1), (0,-1), (-1,-1)]

    # get the coordinates of each X
    x_locations  = []
    for row_idx, row in enumerate(data):
        for col_idx, letter in enumerate(row):
            if letter == 'X':
                x_locations.append((row_idx, col_idx))

    total = 0

    # for each X, scan for XMAS in each direction
    for row_idx, col_idx in x_locations:
        for direction in directions:
            total += is_xmas(data, row_idx, col_idx, direction[0], direction[1])

    print(total)
        
    end_time = int(time.time() * 1000)
    print(f'Time taken for {filename} (ms): {end_time - start_time}')

def is_xmas(data, row_idx, col_idx, row_direction, col_direction):
    text = ''
    for i in range(4):
        text += data[row_idx + (i * row_direction)][col_idx + (i * col_direction)] 
   
    # return 1 if any of the strings match forward or backwards XMAS
    return any((text == 'XMAS', text == 'SAMX'))

def add_border_to_puzzle(data):
    # this should be cleaned up to remove repetition
    # add left and right border
    for row in data:
        row.insert(0,'#')
        row.insert(0,'#')
        row.insert(0,'#')
        row.append('#')
        row.append('#')
        row.append('#')

    # add top border
    data.insert(0, len(data[0]) * ['#']) 
    data.insert(0, len(data[0]) * ['#']) 
    data.insert(0, len(data[0]) * ['#']) 

    # add bottom border
    data.append(data[0])
    data.append(data[0])
    data.append(data[0])

solve('test.txt')
solve('input.txt')