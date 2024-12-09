import time

# messy solution, went down the rabbit hole and haven't cleaned it up

def solve(filename):
    start_time = int(time.time() * 1000)

    disk_map = open(filename).read()

    # take first element and every 2nd afterwards and then cast to inst
    files = list(map(int,list(disk_map[0::2])))
    # take second element and every 2nd afterwards and then cast to int
    free_space = list(map(int, list(disk_map[1::2])))
    
    # print(files)
    # print(free_space)

    defragged = {}
    for i, _ in enumerate(free_space):
        defragged[i] = []

    # run a recurive function to move the blocks
    file_id = len(files) - 1
    free_space_id = 0
    free_space_remaining = free_space[free_space_id]
    for file_id in reversed(range(len(files))):
        file_defrag_remaining = files[file_id]
        (defragged, free_space_id, free_space_remaining) = defrag(files, free_space, defragged, file_id, free_space_id, free_space_remaining, file_defrag_remaining)

        if file_id == free_space_id:
            # print('defrag complete')
            # print(defragged)

            checksum = 0
            idx = 0
            moved = {}

            for file_id, filesize in enumerate(files):
                # print(file_id, defragged[file_id])

                # if its the last moved file
                if defragged[file_id] == []:
                    # check how much of the last file has been moved to the previous free space
                    last_file_moved_amount = moved[file_id]
                    # print('file id' ,file_id - 1, 'last ',last_file_moved_amount)
                    # print('a', [position * file_id for position in range(idx, idx + filesize - last_file_moved_amount)])
                    checksum += sum([position * file_id for position in range(idx, idx + filesize - last_file_moved_amount)])
                    break
                else:
                    # print([position * file_id for position in range(idx, idx + filesize)])
                    checksum += sum([position * file_id for position in range(idx, idx + filesize)])

                    idx += filesize
                    for file in defragged[file_id]:
                        # print([position * file[1] for position in range(idx, idx + file[0])])
                        checksum += sum([position * file[1] for position in range(idx, idx + file[0])])
                        idx += file[0]

                        if file[1] not in moved:
                            moved[file[1]] = 0
                        moved[file[1]] += file[0]

            print(checksum)
            break   

    end_time = int(time.time() * 1000)
    print(f'Time taken for {filename} (ms): {end_time - start_time}')

def defrag(files, free_space, defragged_disk, file_id, free_space_id, free_space_remaining, file_defrag_remaining):
    # print('file_id', file_id, 'free_space_id', free_space_id, 'free_space_remaining', free_space_remaining, 'file_defrag_remaining', file_defrag_remaining, 'defragged_disk', defragged_disk)
    # if no more files to move then finish
    if file_id < 0:
        print('no more files to move then finish')
        return (defragged_disk, free_space_id, free_space_remaining)

    # if no more free space then finish
    if free_space_id + 1 == len(free_space):
        print('no more free space then finish')
        return (defragged_disk, free_space_id, free_space_remaining)
    
    # if free space id is the same as file id then finish
    if file_id == free_space_id:
        print('max files moved then finish')
        return (defragged_disk, free_space_id, free_space_remaining)
    
    if file_defrag_remaining > 0:
        file_defrag_processed = free_space_remaining

        # if we can move entire file into free space
        if file_defrag_remaining <= free_space_remaining:
            # print('can move entire file, finished moving this file')
            file_defrag_processed = file_defrag_remaining

            # store a tuple of how much space was used and by which file for a given free space id
            defragged_disk[free_space_id].append((file_defrag_processed, file_id))
        
            # now that the entire file has been moved, lets move onto the next file to move
            new_file_id = file_id - 1
            new_file_defrag_remaining = files[new_file_id]
            new_free_space_remaining = free_space_remaining - file_defrag_processed

            new_free_space_id = free_space_id
            if new_free_space_remaining == 0:
                new_free_space_id += 1
                new_free_space_remaining = free_space[new_free_space_id]
            
            # return defrag(files, free_space, defragged_disk, new_file_id, new_free_space_id, new_free_space_remaining, new_file_defrag_remaining)
            return (defragged_disk, new_free_space_id, new_free_space_remaining)

        # if the file is too big then move as much as we can
        if file_defrag_remaining > free_space_remaining:
            # print('can partially move file')

            # store a tuple of how much space was used and by which file for a given free space id
            defragged_disk[free_space_id].append((file_defrag_processed, file_id))
        
            # then continue to defrag with the next available free space id
            new_free_space_id = free_space_id + 1
            new_file_defrag_remaining = file_defrag_remaining - file_defrag_processed
            new_free_space_remaining = free_space[new_free_space_id]
            
            return defrag(files, free_space, defragged_disk, file_id, new_free_space_id, new_free_space_remaining, new_file_defrag_remaining)   

solve('test.txt')
solve('input.txt')