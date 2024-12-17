import time

def solve(filename):
    start_time = int(time.time() * 1000)

    # for line in open(filename).read().splitlines():
    #     dir, dist = line.split()
    raw_input = open(filename).read()

    # read into a list of lists, split by new line and then by space using list comprension
    grid = [i for i in raw_input.split('\n')] #if i == to apply filtering

    # add border so we don't have to handle out of bounds during scanning
    add_border(grid)
    
    # apply flood fill starting at 1,1 with boundaries being neighbout letter != starting letter
    # track everywhere we've visited in a seen dict with key as (row, col) value as True
    seen = {}
    # track each region with key as region sequence id, value as list of (row, col, perimeter)
    # track how many sides have a neighbour where letter != current letter, this will help with perimeter calculation
    regions = {}
    
    # start scanning at 1, 1 as we added a border
    region_id = 0
    for row in range(1, len(grid)):
        for col in range(1, len(grid[0])):
            # only scan if we haven't scanned previously and if its not a border location
            if (row, col) not in seen and grid[row][col] != '#':
                flood_fill_scan(grid, seen, regions, [(row, col)], region_id)
                region_id += 1
    
    # print(regions)

    price = 0
    for region_id, region_data in regions.items():
        perimeter = 0
        area = len(region_data)
        for location in region_data:
            perimeter += location[2]
        # print(region_id, area, perimeter, area * perimeter)
        price += area * perimeter

    print(price)

    end_time = int(time.time() * 1000)
    print(f'Time taken for {filename} (ms): {end_time - start_time}')

def flood_fill_scan(grid, seen, regions, to_visit, current_region):
    row, col = to_visit[-1]
    location_value = grid[row][col]
    
    while to_visit != []:
        row, col = to_visit.pop()
        # print('checking', row, col)
        # avoid duplicate scans and infinite loops
        if (row, col) in seen:
            continue 

        # since we haven't been here before, lets now track we have visited
        seen[(row, col)] = True

        perimeter = 0
        # check each direct in N, E, S, W directions
        for dr, dc in [(-1,0), (0,1), (1,0), (0,-1)]:
            neighbour_value = grid[row + dr][col + dc]
            # print('checking neighbour', row + dr, col + dc, neighbour_value, 'against current location', location_value)
            if location_value == neighbour_value:
                # neighbour is of same region so add it to the next place to visit
                to_visit.append((row + dr, col + dc))
            else:
                # neighbour is not of same region so extend the perimeter
                perimeter += 1
        
        # keep track of region locations with perimeter
        if current_region not in regions:
            regions[current_region] = []
        regions[current_region].append((row, col, perimeter))

def add_border(grid):
    # add left and right border
    for i in range(len(grid)):
        grid[i] = '#' + grid[i] + '#'

    # add top border
    grid.insert(0, '#' * len(grid[0])) 
    # add bottom border
    grid.append(grid[0])

solve('test.txt')
print()
solve('test2.txt')
print()
solve('test3.txt')
print()
solve('input.txt')