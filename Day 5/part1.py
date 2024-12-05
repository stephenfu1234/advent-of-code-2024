import time

def read_file(filename):
    return open(filename).read()

def solve(filename):
    start_time = int(time.time() * 1000)

    top, bottom = read_file(filename).split('\n\n') 

    # store the order rules in a dict with key being the page that must precede all the dict values for that key
    # e.g. '47': ['53', '13', '61', '29']
    order_rules = {}
    for rule in [i.split('|') for i in top.split('\n')]:
        if rule[0] in order_rules:
            order_rules[rule[0]].append(rule[1])
        else:
            order_rules[rule[0]] = [rule[1]]

    correct = []

    # review each update as pairwise pages
    updates = [i.split(',') for i in bottom.split('\n')]
    for update in updates:
        # for each pair of an update
        valid = True        
        for x, y in zip(update, update[1:]):
            # check if the first value (x) is allowed to be before the second value [y]
            if x not in order_rules or y not in order_rules[x]:
                valid = False
                break

        if valid:
            correct.append(update)

    # get middle element of all correct updates and sum, assume all updates are odd size
    total = 0
    for update in correct:  
        total += int(update[len(update) // 2])
    
    print(total)
    
    end_time = int(time.time() * 1000)
    print(f'Time taken for {filename} (ms): {end_time - start_time}')
    
solve('test.txt')
solve('input.txt')