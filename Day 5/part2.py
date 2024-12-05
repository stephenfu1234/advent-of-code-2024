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

    incorrect = []
    fixed = []

    # review each update as pairwise pages
    updates = [i.split(',') for i in bottom.split('\n')]
    for update in updates:
        # for each pair of an update
        valid = True        
        for x, y in zip(update, update[1:]):
            # check if the first value (x) is allowed to be before the second value [y]
            if x not in order_rules or y not in order_rules[x]:
                incorrect.append(update)
                break

    for update in incorrect:
        corrected = []
        while len(update) > 0:
            page = update.pop(0)
            
            if corrected == []:
                corrected.append(page)
            else:
                 # check if the page should go at the head of corrected
                if page in order_rules and corrected[0] in order_rules[page]:
                    corrected.insert(0, page)
                else:
                    # check for last element that has a match
                    matches = []
                    for correct_page in corrected:
                        if correct_page in order_rules and page in order_rules[correct_page]:
                            matches.append(correct_page)
                    
                    # after checking against all current correct pages then insert after the last match
                    last_match = matches[-1:][0]                    
                    last_match_position = corrected.index(last_match)
                    corrected.insert(last_match_position+1, page)
        
        # add the corrected update to the overall fixed list for later calculation of middle elements
        fixed.append(corrected)
    
    # get middle element of all correct updates and sum, assume all updates are odd size
    total = 0
    for update in fixed:  
        total += int(update[len(update) // 2])
    
    print(total)
    
    end_time = int(time.time() * 1000)
    print(f'Time taken for {filename} (ms): {end_time - start_time}')
    
solve('test.txt')
solve('input.txt')