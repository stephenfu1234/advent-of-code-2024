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

    # get the coordinates of each A
    a_locations  = []
    for row_idx, row in enumerate(data):
        for col_idx, letter in enumerate(row):
            if letter == 'A':
                a_locations.append((row_idx, col_idx))

    total = 0

    # for each A, scan for X-MAS pattern
    for row_idx, col_idx in a_locations:
        total += is_xmas(data, row_idx, col_idx)

    print(total)
        
    end_time = int(time.time() * 1000)
    print(f'Time taken for {filename} (ms): {end_time - start_time}')

def is_xmas(data, row_idx, col_idx):
    # return 1 if X-MAS pattern is matched, we have 4 patterns due to pattern rotation being accepted
    pattern_1 = all((data[row_idx - 1][col_idx - 1] == 'M', data[row_idx + 1][col_idx - 1] == 'M', data[row_idx - 1][col_idx + 1] == 'S', data[row_idx + 1][col_idx + 1] == 'S'))
    pattern_2 = all((data[row_idx - 1][col_idx - 1] == 'M', data[row_idx + 1][col_idx - 1] == 'S', data[row_idx - 1][col_idx + 1] == 'M', data[row_idx + 1][col_idx + 1] == 'S'))
    pattern_3 = all((data[row_idx - 1][col_idx - 1] == 'S', data[row_idx + 1][col_idx - 1] == 'S', data[row_idx - 1][col_idx + 1] == 'M', data[row_idx + 1][col_idx + 1] == 'M'))
    pattern_4 = all((data[row_idx - 1][col_idx - 1] == 'S', data[row_idx + 1][col_idx - 1] == 'M', data[row_idx - 1][col_idx + 1] == 'S', data[row_idx + 1][col_idx + 1] == 'M'))

    return any((pattern_1, pattern_2, pattern_3, pattern_4))

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