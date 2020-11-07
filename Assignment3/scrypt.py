#!/usr/bin/python3
import sys

# linear congruential generator
def lcg(x_n):
    return (1103515245 * x_n + 12345) % 256

# sbdm hash
def sbdm(str):
    max = 18446744073709551615 + 1
    hash, c = 0, 0
    for char in str:
        c = ord(char)
        hash = c + (hash << 6) + (hash << 16) - hash
        # print("{}: {}".format(c, hash))

    # have to mod by max because I am using python
    return hash % max

def main():
    # error check
    if len(sys.argv) != 4:
        print("Wrong number of arguments")
        return -1
    
    password = sys.argv[1]
    
    # check files
    start_file = open(sys.argv[2], "rb")
    end_file = open(sys.argv[3], "wb+")

    if not start_file:
        print("File does not exist")
        return -1

    seed = sbdm(password)
    key = lcg(seed)

    while True:
        m = start_file.read(1)
        if not m:
            break
        xor = int.from_bytes(m, byteorder=sys.byteorder) ^ key
        end_file.write( int.to_bytes(xor,byteorder=sys.byteorder, length=1) )
        key = lcg(key)


    start_file.close()
    end_file.close()

if __name__ == "__main__":
    main()