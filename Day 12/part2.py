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
        area = len(region_data)
        # print('region id', region_id)
        price += area * calculate_sides(region_data)
        # print()

    print(price)

    end_time = int(time.time() * 1000)
    print(f'Time taken for {filename} (ms): {end_time - start_time}')

def calculate_sides(region_data):
    # filter to get the region edges
    edge_locations = [location for location in region_data if location[2] != []]

    # to calculate a side sort all the edges by row location, then iterate over
    # if current col is 1 greater than previous it must be a side so decrement the perimeter size
    # then repeat sorted by col location
    perimeter = sum([len(region[2]) for region in region_data])
    # print('starting perimeter', perimeter)
    sorted_by_col = sorted(edge_locations, key=lambda tup: tup[0])
    sorted_by_col_row = sorted(sorted_by_col, key=lambda tup: tup[1])
    previous_region = None
    for i, region in enumerate(sorted_by_col_row):
        
        if i == 0:
            previous_region = region
            continue
        
        # print('checking location', region, 'against previous', previous_region)
        if region[1] == previous_region[1]:
            # print('is vertical side', region[1], previous_region, region[2]) 
            # check if we have perimeter on both E and W sides
            current_has_east_perimeter = (0,1) in region[2]
            current_has_west_perimeter = (0,-1) in region[2]
            previous_has_east_perimeter = (0,1) in previous_region[2]
            previous_has_west_perimeter = (0,-1) in previous_region[2]
            
            # if the two has the same perimeter and are next to each other then it must be part of the same side
            if current_has_east_perimeter and previous_has_east_perimeter and (region[0] - previous_region[0] == 1):
                # print('same east side')
                perimeter -= 1

            if current_has_west_perimeter and previous_has_west_perimeter and (region[0] - previous_region[0] == 1):
                # print('same west side')
                perimeter -= 1

        previous_region = region

    sorted_by_row = sorted(edge_locations, key=lambda tup: tup[1])
    sorted_by_row_col = sorted(sorted_by_row, key=lambda tup: tup[0])
    sorted_by_col = sorted(edge_locations, key=lambda tup: tup[1])
    previous_region = None
    for i, region in enumerate(sorted_by_row_col):
        if i == 0:
            previous_region = region
            continue

        # print('checking location', region, 'against previous', previous_region)
        if region[0] == previous_region[0]:
            # print('is horizontal side', region[1], previous_region, region[2])    
            # check if we have perimeter on both N and S sides
            current_has_north_perimeter = (-1,0) in region[2]
            current_has_south_perimeter = (1,0) in region[2]
            previous_has_north_perimeter = (-1,0) in previous_region[2]
            previous_has_south_perimeter = (1,0) in previous_region[2]

            if current_has_north_perimeter and previous_has_north_perimeter and (region[1] - previous_region[1] == 1):
                # print('same north side')
                perimeter -= 1

            if current_has_south_perimeter and previous_has_south_perimeter and (region[1] - previous_region[1] == 1):
                # print('same south side')
                perimeter -= 1
        
        previous_region = region

    # print('final perimeter', perimeter)
    return perimeter


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

        # store the perimeter location details in a list as we now need to calculate sides
        perimeter = []
        # check each direct in N, E, S, W directions
        for dr, dc in [(-1,0), (0,1), (1,0), (0,-1)]:
            neighbour_value = grid[row + dr][col + dc]
            # print('checking neighbour', row + dr, col + dc, neighbour_value, 'against current location', location_value)
            if location_value == neighbour_value:
                # neighbour is of same region so add it to the next place to visit
                to_visit.append((row + dr, col + dc))
            else:
                # neighbour is not of same region so store the perimeter location
                perimeter.append((dr, dc))
        
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
solve('test4.txt')
print()
solve('test5.txt')
print()
solve('input.txt')