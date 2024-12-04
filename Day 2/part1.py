import time

def read_file(filename):
    return open(filename).read()

def solve(filename):
    start_time = int(time.time() * 1000)

    # for line in read_file(filename).splitlines():
    #     dir, dist = line.split()
    raw_input = read_file(filename)

    # read into a list of lists, split by new line and then by space using list comprension
    data = [[int(j) for j in i.split(' ')] for i in raw_input.split('\n')]

    invalid = 0
    for report in data:
        # check if asc or desc
        if report[1] > report[0]:
            for level in range(1, len(report)):
                if report[level] < report[level-1] or abs(report[level] - report[level-1]) > 3 or report[level] == report[level-1]:
                    invalid += 1
                    break

        elif report[1] < report[0]:
            for level in range(1, len(report)):
                if report[level] > report[level-1] or abs(report[level] - report[level-1]) > 3 or report[level] == report[level-1]:
                    invalid += 1
                    break

        else:
            invalid += 1
            
    print(len(data) - invalid)

    end_time = int(time.time() * 1000)
    print(f'Time taken for {filename} (ms): {end_time - start_time}')

solve('test.txt')
solve('input.txt')