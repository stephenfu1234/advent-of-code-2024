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

    expanded = expand(data)

    validate(expanded)

    end_time = int(time.time() * 1000)
    print(f'Time taken for {filename} (ms): {end_time - start_time}')

def validate(reports):
    valid = {}
    for report_index, report_list in reports.items():
        # print(report_index)
        for report in report_list:
            valid_flag = True

            # check if asc or desc
            # print(report)
            if report[1] > report[0]:
                for level in range(1, len(report)):
                    if report[level] < report[level-1] or abs(report[level] - report[level-1]) > 3 or report[level] == report[level-1]:
                        valid_flag = False

            elif report[1] < report[0]:
                for level in range(1, len(report)):
                    if report[level] > report[level-1] or abs(report[level] - report[level-1]) > 3 or report[level] == report[level-1]:
                        valid_flag = False

            else:
                valid_flag = False
        
            if valid_flag == True:
                valid = add(valid, report_index)

    print(len(valid))

def expand(data):
    reports = {}
    for report_index, report in enumerate(data):
        reports[report_index] = [report]

        for level in range(len(report)):
            new_report = report.copy()
            del new_report[level]
            reports[report_index].append(new_report)
    return reports

def add(valid, report_index):
    if report_index in valid:
        valid[report_index].append(True)
    else:
        valid[report_index] = [True]

    return valid

solve('test.txt')
solve('input.txt')