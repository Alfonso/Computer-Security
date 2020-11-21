def work_back(work, length):

    go_back = 1
    # loop in reverse
    for idx in range( length, -1, -1 ):
        # check if at last char
        if work[idx] == chr(126):
            go_back = 1
            work[idx] = chr(33)
        else:
            go_back = 0
            work[idx] = chr( ord(work[idx]) + 1 )
            break

    if go_back == 1:
        work.append( chr(33) )
        length += 1

    return work, length

work = [chr(126), chr(126), chr(126)]
print(work)
length = 2
work, length = work_back(work, length)
print(work)
work, length = work_back(work, length)
print("{} {}".format(work,length))