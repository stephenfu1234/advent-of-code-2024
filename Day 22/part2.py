import time
import pandas as pd

def solve(filename):
    start_time = int(time.time() * 1000)

    generations = 2000
    buyers = {}
    for line in open(filename).read().splitlines():
        secret = int(line)
        buyers[secret] = [secret]
        for i in range(generations):
            secret = process(secret)            
            buyers[int(line)].append(secret)

    process_prices(buyers)
    
    end_time = int(time.time() * 1000)
    print(f'Time taken for {filename} (ms): {end_time - start_time}')

def get_col(list_of_lists, c):
    return [row[c] for row in list_of_lists]

def process_prices(buyers):
    buyers_price_history = {}
    buyers_price_change_history = {}

    window_size = 4
    buyers_sliding_windows = {}

    for buyer_id, buyer_secrets in buyers.items():
        previous_price = 0

        if buyer_id not in buyers_price_history: 
            buyers_price_history[buyer_id] = []
            buyers_price_change_history[buyer_id] = []            

        for i, secret in enumerate(buyer_secrets):
            price = int(str(secret)[-1:])
            
            price_change = None
            if i > 0:
                price_change = price - previous_price            
            
            buyers_price_history[buyer_id].append(price)
            buyers_price_change_history[buyer_id].append(price_change)
            
            previous_price = price
        
        # print('buyer id', buyer_id)
        # print('buyers_price_history', buyers_price_history[buyer_id])
        # print('buyers_price_change_history', buyers_price_change_history[buyer_id])

        buyers_sliding_windows[buyer_id] = get_previous_sliding_windows(buyers_price_history[buyer_id], buyers_price_change_history[buyer_id], window_size, buyer_id)
        # print('buyers_sliding_windows', buyers_sliding_windows[buyer_id])

    find_best_price(buyers, buyers_sliding_windows)    

def find_best_price(buyers, buyers_sliding_windows):
    # buyers_sliding_windows stores data for a given buyer, their sequences as keys, and the value as the price
    # e.g. 123 -> { [-3,6,-1,-1] -> 4 }
    # so combine all the buyers sliding windows data together and group by sequence and sum the bananas.  The highest sum is the best price
    all_data = []
    for buyer in buyers:
        for sequence, price in buyers_sliding_windows[buyer].items():
            all_data.append((sequence, price))   
    
    df = pd.DataFrame(all_data)
    grouped_by_sequence = df.groupby([0]).sum()

    # print by ascending total price, last row will be the best price for a given sequence
    print(grouped_by_sequence.sort_values(1))

def get_previous_sliding_windows(price_history, price_change_history, window_size, i):
    sliding_windows = {}

    # get all the sliding windows and its price for that window e.g we would have -3,6,-1,-1 -> 4 and 6,-1,-1,0 -> 4
    #      123: 3 
    # 15887950: 0 (-3)
    # 16495136: 6 (6)
    #   527345: 5 (-1)
    #   704524: 4 (-1)
    #  1553684: 4 (0)
    # then we only want to keep the first of any given sequence

    for i in range(window_size, len(price_history)):
        price = price_history[i]

        sequence = tuple(price_change_history[i - window_size +1:i +1])        
        if sequence not in sliding_windows: 
            sliding_windows[sequence] = price

    return sliding_windows

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
solve('test3.txt')
solve('input.txt')