import time
import functools

# observations
# break the problem into smaller sub problems (dynamic programming principle)
# a robot's action must end with A to get the next robot to do something
# an optimal route will ever move away from the target location (unlike a maze)
# favour moving in a single direction as its cheaper e.g. V<< is cheaper than <v< as the robot doesnt have to keep moving
# also favour < first as subsequent v or ^ we will be closer to A which is required to terminate the sub sequence
# changing to 25 robots makes the sequence explode in size
# however we don't actually need to maintain the actual sequence, instead let's keep a frequency map of the required sub moves
# as there are many repeated patterns, we can also apply caching

# lets make as global variables so we don't have to keep passing variables around in the functions unlike previous days
D_PAD = 'd'
D_PAD_COORDS = {
    ' ': (0,0),
    '^': (0,1),
    'A': (0,2),
    '<': (1,0),
    'v': (1,1),
    '>': (1,2)
}

N_PAD = 'n'
N_PAD_COORDS = {
    '7': (0, 0),
    '8': (0, 1),
    '9': (0, 2),
    '4': (1, 0),
    '5': (1, 1),
    '6': (1, 2),
    '1': (2, 0),
    '2': (2, 1),
    '3': (2, 2),
    ' ': (3, 0),
    '0': (3, 1),
    'A': (3, 2)
}

TOTAL_N_PAD_ROBOTS = 25

def solve(filename):
    start_time = int(time.time() * 1000)   
    
    scores = []
    for code in open(filename).read().splitlines():
        print(code)

        # create the sequence required to enter the code on the number pad
        robot_1 = generate_optimal_sequence(code, N_PAD)
        # print('robot 1', robot_1)

        # now that we have the sequence required, we again find the optimal path to generate the given directions rather than the code
        # repeat per N pad robot
        previous_sequence_frequency = generate_sequence_frequency_map(robot_1)
        print(previous_sequence_frequency)

        for i in range(2, TOTAL_N_PAD_ROBOTS + 2):
            robot_i_sequence_frequency = {}

            # generate the optimal sequence only on sections (as A is a terminator) instead of joining the entire sequence together
            # we can then just keep track of frequencies of each generated sub sequence and avoid repeating the same action over and over
            for sub_sequence, sub_sequence_frequency in previous_sequence_frequency.items():
                robot_i_sub_sequence = generate_optimal_sequence(sub_sequence, D_PAD)                
                robot_i_sub_sequence_frequency = generate_sequence_frequency_map(robot_i_sub_sequence)

                # sum the dicts together and repeat for each original frequency
                for seq, count in robot_i_sub_sequence_frequency.items():
                    if seq not in robot_i_sequence_frequency:
                        robot_i_sequence_frequency[seq] = 0
                    robot_i_sequence_frequency[seq] += count * sub_sequence_frequency
                                                                
            previous_sequence_frequency = robot_i_sequence_frequency

            print('robot', i, robot_i_sequence_frequency)
        
        length = 0
        for seq, count in robot_i_sequence_frequency.items():
            length += len(seq) * count
        scores.append(length * int(code[:3]))
        
        print()

    print('final complexity score', sum(scores))            
    
    end_time = int(time.time() * 1000)
    print(f'Time taken for {filename} (ms): {end_time - start_time}')

def generate_sequence_frequency_map(sequence):
    return {key: sequence.count(key) for key in sequence}

@functools.cache
def optimal_path(key_1, key_2, pad_type):
    key_1_row, key_1_col = coords(key_1, pad_type)
    key_2_row, key_2_col = coords(key_2, pad_type)

    vertical_moves = get_vertical_moves(key_1_row, key_2_row)
    horizonal_moves = get_horizontal_moves(key_1_col, key_2_col)

    # we now know how many times we need to move up/down or left/right and we've also kept the moves in a straight line
    # we now have to decide if we should apply vertical or horizontal movement first
    # try to move vertically first unless its an invalid move into a gap
    if key_2_col > key_1_col and not invalid_move(key_2_row, key_1_col, pad_type):
        return vertical_moves + horizonal_moves + 'A'
    
    # else try to move horizontally unless its an invalid move into a gap
    if not invalid_move(key_1_row, key_2_col, pad_type):
        return horizonal_moves + vertical_moves + 'A'

    return vertical_moves + horizonal_moves + 'A'

@functools.cache
def generate_optimal_sequence(sequence, pad_type):
    keys_pressed = []

    # default starting position
    previous_key = 'A'
    for key in sequence:
        # keep track of keys pressed as we move from one number in the code to another
        keys_pressed.append(optimal_path(previous_key, key, pad_type));
        previous_key = key

    return keys_pressed

def get_vertical_moves(key_1_row, key_2_row):
    # move up or down n number of times depending on the distance between keys
    # we should favour moving in a straight line as much as possible to minimze robots having to move arms
    distance = abs(key_1_row - key_2_row)
    if key_2_row > key_1_row:
        return 'v' * distance
    return '^' * distance

def get_horizontal_moves(key_1_col, key_2_col):
    # move left or right n number of times depending on the distance between keys
    # we should favour moving in a straight line as much as possible to minimze robots having to move arms
    distance = abs(key_1_col - key_2_col)
    if key_2_col > key_1_col:
        return '>' * distance
    return '<' * distance

def coords(key, pad_type):
    if pad_type == N_PAD:
        return N_PAD_COORDS[key]
    return D_PAD_COORDS[key]

def invalid_move(row, col, pad_type):
    # do not move over the gaps
    if pad_type == N_PAD:
        return (row, col) == N_PAD_COORDS[' ']   
    return (row, col) == D_PAD_COORDS[' ']

solve('test.txt')
solve('input.txt')
154115708116294
246810588779586