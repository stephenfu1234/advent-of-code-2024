import time
import itertools

# generalise part 1 to find N inter-connected computers
# then recursively find N+1 inter-connected computers using the previous as the in-scope computers
# once we no longer can find any inter-connected computers then the previous iteration is the longest network chain
def solve(filename):
    start_time = int(time.time() * 1000)

    raw_input = open(filename).read()

    # read into a list of lists, split by new line and then by space using list comprension
    connections = [i.split('-') for i in raw_input.split('\n')]

    connection_groups, _ = get_connection_groups(connections)
    starting_computers = connection_groups.keys()
    
    # print(connection_groups)
    # print(starting_computers)

    for n in range(3, len(starting_computers)):
        inscope_computers = find_inter_connected_computers(connection_groups, starting_computers, n)
        print(len(inscope_computers), 'inscope computers')
        print(','.join(sorted(inscope_computers)))

        if len(inscope_computers) == 0:
            break

        # start the next iteration with the output of the previous iteration to reduce the search space
        starting_computers = inscope_computers
       
    end_time = int(time.time() * 1000)
    print(f'Time taken for {filename} (ms): {end_time - start_time}')

# generalised version of part 1 where this will return n size rather than fixed 3 size inter-connected network
def find_inter_connected_computers(connection_groups, starting_computers, n):
    print('finding inter-connected computers of size', n)
    inscope_computers = set()
    for c1 in starting_computers:
        # create all N sized combinations from a given list
        combinations = list(itertools.combinations(connection_groups[c1], n-1))
        
        for combination in combinations:
            all_computers = connection_groups[c1].copy()
            for c_n in combination:
                all_computers.extend(connection_groups[c_n])
            inter_connected_check = [all_computers.count(c1) == n-1]
                        
            for c_n in combination:
                inter_connected_check.append(all_computers.count(c_n) == n-1)
        
            if all(inter_connected_check):
                inscope_computers.add(c1)
                inscope_computers.update(combination)

    return inscope_computers

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