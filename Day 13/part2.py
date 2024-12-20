import time
import sympy

# fresh simplified approach to solve simulatenous equations using sympy after taking a step back
# part 1, I got stuck focusing on getting all the solutions for one linear equation
# then checking which solution worked for the second equation
# this is inefficient and the search space quickly expands and is unworkable for part 2
def solve(filename):
    start_time = int(time.time() * 1000)

    raw_input = open(filename).read()

    # read into a list of lists, split by new line and then by space using list comprension
    data = [i.split('\n') for i in raw_input.split('\n\n')] #if i == to apply filtering

    games = []
    # convert into a format of list of lists.  Each child list contains 2 tuples of representing each button and its target
    for game in data:
        ax = int(game[0].split(", Y+")[0].split('+')[1])
        bx = int(game[1].split(", Y+")[0].split('+')[1])
        x_target = int(game[2].split(", Y=")[0].split('=')[1])       

        ay = int(game[0].split(", Y+")[1])
        by = int(game[1].split(", Y+")[1])
        y_target = int(game[2].split(", Y=")[1])

        # games.append([(ax, bx, x_target), (ay, by, y_target)])
        games.append([(ax, bx, x_target + 10000000000000), (ay, by, y_target + 10000000000000)])

    # this could be optimised by removing the additional iteration
    required_tokens = 0
    for game in games:
        # print(game)
        a1, b1, target1 = game[0]
        a2, b2, target2 = game[1]
        a_n, b_n = sympy.symbols('a_n, b_n')
        eq1 = sympy.Eq(a1 * a_n + b1 * b_n, target1)
        eq2 = sympy.Eq(a2 * a_n + b2 * b_n, target2)

        solutions = sympy.solve([eq1, eq2], (a_n, b_n))
        if len(solutions)> 2:
            print(len(solutions), game)
        # print(solutions)

        required_tokens += calculate_required_tokens(solutions)
    
    print(required_tokens)

    end_time = int(time.time() * 1000)
    print(f'Time taken for {filename} (ms): {end_time - start_time}')

def calculate_required_tokens(solutions):
    a_n, b_n = sympy.symbols('a_n, b_n')
    a_n_val = solutions[a_n]
    b_n_val = solutions[b_n]

    # we only want integer solutions
    if a_n_val.is_integer and b_n_val.is_integer:
        #  print('found solution')
         return (a_n_val * 3) + b_n_val
    
    # print('no solution')
    return 0

solve('test.txt')
solve('input.txt')