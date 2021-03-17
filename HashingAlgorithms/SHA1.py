import time

# chaining variables
A = 0x67452301
B = 0xEFCDAB89
C = 0x98BADCFE
D = 0x10325476
E = 0xC3D2E1F0


def make_chunks(l, n):
    return [l[i:i + n] for i in range(0, len(l), n)]


def left_rotate(n, b):
    return ((n << b) | (n >> (32 - b))) & 0xffffffff


def sha1(msg):

    a, b, c, d, e = A, B, C, D, E

    msg_bytes = ""
    for n in range(len(msg)):
        msg_bytes = msg_bytes + '{0:08b}'.format(ord(msg[n]))

    # add 1
    bits = msg_bytes+"1"
    bits_1 = bits

    # padding
    while len(bits_1) % 512 != 448:
        bits_1 = bits_1 + "0"
    bits_1 = bits_1 + '{0:064b}'.format(len(bits)-1)

    # main loop
    for x in make_chunks(bits_1, 512):
        word_chunks = make_chunks(x, 32)

        a1, b1, c1, d1, e1 = A, B, C, D, E

        w = [0] * 80  # words
        for i in range(80):
            if i < 20:
                f = (b1 & c1) | ((~b1) & d1)
                k = 0x5A827999
                if i < 16:
                    w[i] = int(word_chunks[i], 2)
                else:
                    w[i] = left_rotate((w[i - 3] ^ w[i - 8] ^ w[i - 14] ^ w[i - 16]), 1)

            elif i < 40:
                f = b1 ^ c1 ^ d1
                k = 0x6ED9EBA1
                w[i] = left_rotate((w[i - 3] ^ w[i - 8] ^ w[i - 14] ^ w[i - 16]), 1)

            elif i < 60:
                f = (b1 & c1) | (b1 & d1) | (c1 & d1)
                k = 0x8F1BBCDC
                w[i] = left_rotate((w[i - 3] ^ w[i - 8] ^ w[i - 14] ^ w[i - 16]), 1)

            else:
                f = b1 ^ c1 ^ d1
                k = 0xCA62C1D6
                w[i] = left_rotate((w[i - 3] ^ w[i - 8] ^ w[i - 14] ^ w[i - 16]), 1)

            temp = left_rotate(a1, 5) + f + e1 + k + w[i] & 0xffffffff
            e1, d1, c1, b1, a1 = d1, c1, left_rotate(b1, 30), a1, temp  # reassign variables

        a = a + a1 & 0xffffffff
        b = b + b1 & 0xffffffff
        c = c + c1 & 0xffffffff
        d = d + d1 & 0xffffffff
        e = e + e1 & 0xffffffff

    return '%08x%08x%08x%08x%08x' % (a, b, c, d, e)


def main():
    print('Enter the file: ')
    x = input()
    file1 = open(x, 'r')
    print("How many times would you like to run: ")
    num_run = input()
    start = time.time()
    for i in range(int(num_run)):
        Lines = file1.readlines()
        for line in Lines:
            print(sha1(str(line.strip())))
    end = time.time()
    x = end - start
    print("Total Time: ", x)


if __name__ == '__main__':
    main()