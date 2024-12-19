import time
import math
from sympy import symbols, Eq, linsolve

# use linsolve to solve parallel equations
def solve(filename):
    start_time = int(time.time() * 1000)

    # for line in open(filename).read().splitlines():
    #     dir, dist = line.split()
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

        games.append([(ax, bx, x_target), (ay, by, y_target)])

    # this could be optimised by removing the additional iteration
    required_tokens = 0
    for game in games:
        if is_winnable(game):
            solutions = find_solutions(game)
            required_tokens += get_optimal_solution(solutions)
            
    print(required_tokens)

    end_time = int(time.time() * 1000)
    print(f'Time taken for {filename} (ms): {end_time - start_time}')

def get_optimal_solution(solutions):
    fewest_tokens = 0
    for a_n, b_n in solutions:
        
        solution_tokens = (a_n * 3) + b_n
        # print('a_n', a_n, 'b_n', b_n, 'requires', solution_tokens, 'tokens')
        if fewest_tokens == 0:
            fewest_tokens = solution_tokens
            continue

        if solution_tokens < fewest_tokens:
            fewest_tokens = solution_tokens
    
    return fewest_tokens


def find_solutions(game):
    # print('optimising game', game)

    # solve for X and then try all solutions to see which work with Y
    a, b, target = game[0]

    possible_solutions = []
    for a_n in range((target // a) + 1):
        b_n = (target - a * a_n) / b
        if b_n.is_integer() and b_n >= 0:
            possible_solutions.append((a_n, b_n))
        
    # print('found possible solutions', possible_solutions)

    # now see which solution fits y_target
    solutions = []
    a, b, target = game[1]
    for possible_solution in possible_solutions:
        a_n, b_n = possible_solution
        if a * a_n + b * b_n == target:
            solutions.append(possible_solution)
        
    return solutions

# to be a valid game the target must be wholly divisible of greatest common divisor of a and b
# this calc is actually wrong as it tests the equations independently whereas the equations need to be solved in parallel
def is_winnable(game):
    for button in game:
        a, b, target = button
        gcd = math.gcd(a, b)
        # print(gcd)
        if target % gcd > 0:
            return False

    return True

solve('test.txt')
solve('input.txt')