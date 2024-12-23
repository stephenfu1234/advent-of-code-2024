import time

def solve(filename):
    start_time = int(time.time() * 1000)

    raw_input = open(filename).read()

    # read into a list of lists, split by new line and then by space using list comprension
    connections = [i.split('-') for i in raw_input.split('\n')] #if i == to apply filtering

    connection_groups, starting_computers = get_connection_groups(connections)
    # print(connection_groups)
    # print(starting_computers)

    inscope_computers = set()
    for c1 in starting_computers:
        # get pairs of the connected groups to c1
        pairs = [(a, b) for idx, a in enumerate(connection_groups[c1]) for b in connection_groups[c1][idx + 1:]]

        # then the 3 computer names should each appear twice in the union list of connections to indicate all connected to each other
        for c2, c3 in pairs:
            all_computers = connection_groups[c1] + connection_groups[c2] + connection_groups[c3]
            # print(c1, c2, c3)
            # print(all_computers)
            # there is duplicated detection here so we'll have to check on the sorted set to exclude
            if all([all_computers.count(c1) == 2, all_computers.count(c2) == 2, all_computers.count(c3) == 2]):
                inscope_computers.add('-'.join(sorted([c1,c2,c3])))

    # for c in inscope_computers:
    #     print(c)

    print(len(inscope_computers))
                
    end_time = int(time.time() * 1000)
    print(f'Time taken for {filename} (ms): {end_time - start_time}')

def get_connection_groups(connections):
    connection_groups = {}
    starting_computers = []
    for c1, c2 in connections:
        if c1 in connection_groups: connection_groups[c1].append(c2)
        if c2 in connection_groups: connection_groups[c2].append(c1)
        if c1 not in connection_groups: connection_groups[c1] = [c2]
        if c2 not in connection_groups: connection_groups[c2] = [c1]

        if c1[0] == 't': starting_computers.append(c1)
        if c2[0] == 't': starting_computers.append(c2)
    return connection_groups, starting_computers
    

solve('test.txt')
solve('input.txt')