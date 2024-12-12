import time

# rewrite from part1, still not an optimal solution as it takes ~10s to run

def solve(filename):
    start_time = int(time.time() * 1000)

    disk_map = open(filename).read()

    # take first element and every 2nd afterwards and then cast to inst
    files = list(map(int,list(disk_map[0::2])))
    # take second element and every 2nd afterwards and then cast to int
    free_space = list(map(int, list(disk_map[1::2])))
    
    # print(files)
    # print(free_space)

    disk = []

    # dict key = start location and value = number of free blocks e.g. 2 -> 3
    available = {}
    original_file_location = {}

    disk_idx = 0
    for file_idx, filesize in enumerate(files):
        
        if disk_idx > 0:            
            # add the file
            disk.extend([file_idx] * filesize)
            original_file_location[file_idx] = disk_idx
            # add the free space
            if len(free_space) > file_idx:
                disk.extend([0] * free_space[file_idx])

                # store how much free space is available at this starting location
                available[disk_idx + filesize] = free_space[file_idx]
                disk_idx += filesize + free_space[file_idx]
        else:
            disk = [file_idx] * filesize
            original_file_location[file_idx] = 0
            disk.extend([0] * free_space[file_idx])

            available[filesize] = free_space[file_idx]
            disk_idx += filesize + free_space[file_idx]

    for file_idx in reversed(range(len(files))):
        required_filesize = files[file_idx]

        # find the slot available free slot to the left        
        for location in sorted(available.keys()):
            space = available[location]
            if required_filesize <= space and location < original_file_location[file_idx]:
                remaining_space = space - required_filesize

                # move the file
                disk = disk[:location] + ([file_idx] * required_filesize) + ([0] * remaining_space) + disk[space + location:]

                # update the available space
                available[location] = 0
                available[location+required_filesize] = remaining_space

                # free up space for the moved file
                disk = disk[:original_file_location[file_idx]] + ([0] * files[file_idx]) + disk[files[file_idx] + original_file_location[file_idx]:]

                break
            
    # multiply element of the disk against its index.  Unpack the range sequence into a list
    checksum = [a*b for a,b in zip(disk,[*range(len(disk))])]
    print(sum(checksum))
    
    end_time = int(time.time() * 1000)
    print(f'Time taken for {filename} (ms): {end_time - start_time}')

solve('test.txt')
solve('input.txt')