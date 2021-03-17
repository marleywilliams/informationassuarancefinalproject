import numpy as np
import time, math

def generate_vals():
    prime_values = np.array([1009,1013,1019,1021,1031,1033,1039,1049,1051,1061,1063,1069,1087,1091,1093,1097,1103,1109,1117,1123,1129,1151,1153,1163,1171,1181,1187,1193,1201,1213,1217,1223,1229,1231,1237,1249,1259,1277,1279,1283,1289,1291,1297,1301,1303,1307,1319,1321,1327,1361,1367,1373,1381,1399,1409,1423,1427,1429,1433,1439,1447,1451,1453,1459,1471,1481,1483,1487,1489,1493,1499,1511,1523,1531,1543,1549,1553,1559,1567,1571,1579,1583,1597,1601,1607,1609,1613,1619,1621,1627,1637,1657,1663,1667,1669,1693,1697,1699,1709,1721,1723,1733,1741,1747,1753,1759,1777,1783,1787,1789,1801,1811,1823,1831,1847,1861,1867,1871,1873,1877,1879,1889,1901,1907,1913,1931,1933,1949,1951,1973,1979,1987,1993,1997,1999,2003,2011,2017,2027,2029,2039,2053,2063,2069,2081,2083,2087,2089,2099,2111,2113,2129,2131,2137,2141,2143,2153,2161,2179,2203,2207,2213,2221,2237,2239,2243,2251,2267,2269,2273,2281,2287,2293,2297,2309,2311,2333,2339,2341,2347,2351,2357,2371,2377,2381,2383,2389,2393,2399,2411,2417,2423,2437,2441,2447,2459,2467,2473,2477,2503,2521,2531,2539,2543,2549,2551,2557,2579,2591,2593,2609,2617,2621,2633,2647,2657,2659,2663,2671,2677,2683,2687,2689,2693,2699,2707,2711,2713,2719,2729,2731,2741,2749,2753,2767,2777,2789,2791,2797,2801,2803,2819,2833,2837,2843,2851,2857,2861,2879,2887,2897,2903,2909,2917,2927,2939,2953,2957,2963,2969,2971,2999])
    p = prime_values[np.random.randint(0,len(prime_values))]
    q = prime_values[np.random.randint(0, len(prime_values))]
    while(p==q):
        q = prime_values[np.random.randint(0, len(prime_values))]
    n = p * q
    temp = (p-1) * (q-1)

    for e in range(2, temp):
        if math.gcd(e, temp) == 1:
            break

    for i in range(1, 10):
        x = 1 + i * temp
        if x % e == 0:
            d = int(x / e)
            break
        else:
            for e in range (e,temp):
                if math.gcd(e,temp) == 1 :
                    i = 1
                    break

    return n,e,d


def encrypt(vals, text):
    e = int(vals[1])
    c = text ** e
    c = c % int(vals[0])
    return c


def decrypt(vals, text):
    q = text ** int(vals[2])
    q = q % int(vals[0])

    return q


def prime():
    lower = 1000
    upper = 3000

    #print("Prime numbers between", lower, "and", upper, "are:")

    for num in range(lower, upper + 1):
        # all prime numbers are greater than 1
        if num > 1:
            for i in range(2, num):
                if (num % i) == 0:
                    break
            else:
                print(str(num) + ",", end='')


def convert_to_number(msg):
    output = ''
    for i in range(len(msg)):
        output += str(ord(msg[i]) - 96)
    return output


def main():
    n, e, d = generate_vals()

    print('Enter the value to encrypt: ')
    x = input()
    try:
        msg = int(x)
    except:
        msg = convert_to_number(x)

    print("How many times would you like to run: ")
    num_run = input()
    for i in range(int(num_run)):
        x = np.array([n, e, d])
        start = time.time()
        msg_len = len(str(msg))
        if (msg_len % 5 == 0):
            chunks = [str(msg)[i:i + 5] for i in range(0, len(str(msg)), 5)]
        elif (msg_len % 4 == 0):
            chunks = [str(msg)[i:i + 4] for i in range(0, len(str(msg)), 4)]
        elif (msg_len % 3 == 0):
            chunks = [str(msg)[i:i + 3] for i in range(0, len(str(msg)), 3)]
        elif (msg_len % 2 == 0):
            chunks = [str(msg)[i:i + 2] for i in range(0, len(str(msg)), 2)]
        else:
            chunks = [str(msg)[i:i + 4] for i in range(0, len(str(msg)), 4)]
        print("chunks: ", chunks)
        for val in chunks:
            print(val)
            enc = encrypt(x, int(val))
            print("entered: " + str(val))
            print("encrypted text: " + str(enc))
            print("decrypted text: " + str(decrypt(x, int(enc))))
            # file1 = open('passwords.txt', 'r')
            #         Lines = file1.readlines()
            #         for line in Lines:
            #             print("entered: " + str(val))
            #             print("decrypted text: " + str(enc))
            #             print("encrypted text: " + str(decrypt(x, int(enc)))

        end = time.time()
        print("Time :", end-start)


if __name__ == '__main__':
    main()