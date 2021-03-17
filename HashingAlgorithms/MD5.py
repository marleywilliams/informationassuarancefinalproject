import math, time

# initialize chaining variables
A = 0x67452301
B = 0xefcdab89
C = 0x98badcfe
D = 0x10325476


def left_rotate(x, amount):
    x &= 0xffffffff
    return ((x << amount) | (x >> (32 - amount))) & 0xffffffff


def md5(msg):
    a, b, c, d = A, B, C, D

    sin_constant = [int(2 ** 32 * abs(math.sin(i + 1))) & 0xffffffff for i in range(64)]

    # padding
    msg = bytearray(msg)
    length_bits = (8 * len(msg)) & 0xffffffff
    msg.append(0x80)
    while len(msg) % 64 != 56:
        msg.append(0)
    msg = msg + length_bits.to_bytes(8, byteorder='little')

    # main loop
    for chunks in range(0, len(msg), 64):
        a1, b1, c1, d1 = A, B, C, D

        chunk = msg[chunks:chunks + 64]
        for i in range(0, 64):
            if i < 16:
                f = (b1 & c1) | (~b1 & d1)
                g = i
                rotate_amount = [7, 12, 17, 22]

            elif i < 32:
                f = (d1 & b1) | (~d1 & c1)
                g = (5 * i + 1) % 16
                rotate_amount = [5, 9, 14, 20]

            elif i < 48:
                f = b1 ^ c1 ^ d1
                g = (3 * i + 5) % 16
                rotate_amount = [4, 11, 16, 23]

            else:
                f = c1 ^ (b1 | ~d1)
                g = (7 * i) % 16
                rotate_amount = [6, 10, 15, 21]

            temp = a1 + f + sin_constant[i] + int.from_bytes(chunk[4 * g:4 * g + 4], byteorder='little')
            temp1 = (b1 + left_rotate(temp, rotate_amount[i % 4])) & 0xffffffff
            a1, b1, c1, d1 = d1, temp1, b1, c1 # change variables

        a = a + a1 & 0xffffffff
        b = b + b1 & 0xffffffff
        c = c + c1 & 0xffffffff
        d = d + d1 & 0xffffffff
        abcd = [a, b, c, d]

        # convert
        return '{:032x}'.format(int.from_bytes((sum(j << (32 * i) for i, j in enumerate(abcd))).to_bytes(16, byteorder='little'), byteorder='big'))


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
            text = md5(bytes(line.strip(), 'utf8'))
            print(text)

    end = time.time()
    x = end - start
    print("Total Time: ", x)


if __name__ == '__main__':
    main()