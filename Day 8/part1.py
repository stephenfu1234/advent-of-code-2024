import time

def solve(filename):
    start_time = int(time.time() * 1000)

    # store all antennas in a dict with value set to list of it's locations
    data = open(filename).read().splitlines()
    
    antinodes = []
    antennas = {}
    for row_idx, row in enumerate(data):
        for col_idx, col in enumerate(row):
            if col != '.':
                if col in antennas:
                    antennas[col].append((row_idx, col_idx))
                else:
                    antennas[col] = [(row_idx, col_idx)]

    max_height = len(data)
    max_width = len(data[0])

    # for each antenna, get locations by pairwise
    for antenna in antennas:
        antenna_locations = antennas[antenna]
        antenna_pairs = [(r, c) for idx, r in enumerate(antenna_locations) for c in antenna_locations[idx + 1:]]

        # for each pair, add each antinode location
        for antenna_pair in antenna_pairs:
            # get the distance between antenna
            distance = tuple(map(lambda a, b: a - b, antenna_pair[0], antenna_pair[1]))
            
            # derivate antinode locations in each direction
            antinode_1 = generate_antinode(antenna_pair[0], distance, '+')            
            antinode_2 = generate_antinode(antenna_pair[1], distance, '-')
            # print(antenna, antenna_pair, distance, antinode_1, valid_antinode(antinode_1, max_height, max_width), antinode_2, valid_antinode(antinode_2, max_height, max_width))

            # add if valid antinode
            if valid_antinode(antinode_1, max_height, max_width):
                antinodes.append(antinode_1)

            if valid_antinode(antinode_2, max_height, max_width):
                antinodes.append(antinode_2)
    
    # print(set(antinodes))
    print(len(set(antinodes)))
    
    end_time = int(time.time() * 1000)
    print(f'Time taken for {filename} (ms): {end_time - start_time}')

def generate_antinode(antenna_location, distance, op):
    return tuple(map(lambda a, b: eval(str(a) + op + str(b)), antenna_location, distance))

def valid_antinode(antinode, max_height, max_width):
    row = antinode[0]
    col = antinode[1]
    return not any([row < 0, row >= max_height, col < 0, col >= max_width])
    
solve('test.txt')
solve('input.txt')