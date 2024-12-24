import time

def solve(filename):
    start_time = int(time.time() * 1000)

    generations = 2000
    iteration = 0
    all_secrets = []
    for line in open(filename).read().splitlines():
        secret = int(line)
        # print('initial secret', secret)
        for generation in range(generations):
            secret = process(secret)
            iteration += 1
            # print(secret)

            # just store the last generation
            if generation == 1999:
                all_secrets.append(secret)
    
    print(sum(all_secrets))

    end_time = int(time.time() * 1000)
    print(f'Time taken for {filename} (ms): {end_time - start_time}')

def process(secret):
    step_1_secret = prune(mix(secret, secret * 64))
    step_2_secret = prune(mix(step_1_secret, step_1_secret // 32))
    return prune(mix(step_2_secret, step_2_secret * 2048))

def mix(secret, value):
    return secret ^ value

def prune(secret):
    return secret % 16777216

solve('test.txt')
solve('test2.txt')
solve('input.txt')