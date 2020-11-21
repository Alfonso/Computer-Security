import hashlib
import sys
import time

hex_dict = { '0': 4, '1': 3, '2':2, '3':2, '4':1, '5':1, '6':1, '7':1, '8':0, '9':0, 'a':0, 'b':0, 'c':0, 'd':0, 'e':0,'f':0 }

def get_hash(str):
    m = hashlib.sha256()
    m.update(bytes(str, 'utf-8'))
    return m.hexdigest()

def check_leading(nbits, hash):
    # each 0 char is 
    leading_char_zero = nbits // 4
    if hash[:leading_char_zero] != ''.join(['0' for _ in range(leading_char_zero)]):
        return False
    
    remaining_zero = nbits % 4
    
    return hex_dict[ hash[leading_char_zero] ] >= remaining_zero

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

def gen_work(nbits, hash):

    if check_leading( nbits, hash ):
        return "", hash, 0

    # 7-bit : 33 - 126
    char = 33
    # has to be a list because strings are immutable
    work = [chr(char)]
    length = 0
    iteration = 1
    new_mes = "".join(work) + hash
    new_hash = get_hash( new_mes )
    while not check_leading( nbits, new_hash ):
        char += 1
        if char > 126:
            char = 33
            work, length = work_back(work, length)
        else:
            work[length] = chr(char)
        
        new_mes = "".join(work) + hash
        new_hash = get_hash( new_mes )
        iteration += 1

    # work, hash, iteration
    return work, new_hash, iteration

def main():
    
    # check args
    if len(sys.argv) != 3:
        print('Please input correct number of args')
        return -1

    # error check for nbits
    try:
        nbits = int(sys.argv[1])
        if nbits < 0:
            print('Please input a proper integer value for nbits')
            return -1
    except:
        print('Please input a proper integer value for nbits')
        return -1

    file_name = sys.argv[2]

    # error check for file
    f = open(file_name, 'r')
    if not f:
        print('File cannot open')
        return -1

    mes = f.read()

    initial_hash = get_hash(mes)

    start = time.time()
    work, new_hash, iterations = gen_work(nbits, initial_hash)
    compute_time = time.time() - start

    # outputs
    print('File: {}'.format( file_name ))
    print('Initial-hash: {}'.format( initial_hash ))
    print('Proof-of-work: {}'.format( "".join(work) ))
    print('Hash: {}'.format( new_hash ))
    print('Leading-bits: {}'.format( nbits ))               #FIXME have to print the actual number of leading bits
    print('Iterations: {}'.format( iterations ))
    print('Compute-time: {}'.format( compute_time ))

    f.close()


if __name__ == "__main__":
    main()