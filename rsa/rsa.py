# algorithms Project 1 - RSA
# objective: implement RSA Encryption and apply it to digital signature

import pandas as pd
import numpy as np
import hashlib
import random
import time
import math

print (hashlib.algorithms_guaranteed)

h = hashlib.sha256(b'computer science at UA is the best')
m = h.hexdigest()
print(m)

# if 'p' is prime, then for any integer 'a' such that 1 < a < p, we have:
# a^(p-1) congruent to 1(mod p)
#
# if equation holds, p might be prime
# if it does NOT hold, then p is definitely NOT prime (composite)

# this function check if the input is a relative prime or not
def FermatPrimalityTest(p):
    # print(p)
    a = False
    # to be completed
    if p <= 1:
        return a
    if p == 2 or p == 3:
        return True
    
    # fixed number of test for better accuracy
    num_test = 2

    for _ in range(num_test):
        # pick a random base for range [2, p-2]
        base = random.randint(2, p-2)

        # check if base^(p-1) is congruent to 1 (mod p)
        if pow(base, p-1, p) != 1:
            return a
    return True

# you need to modify this function to generate two pairs of keys
def RSA_key_generation():

    p = generate_prime()
    q = generate_prime()
    # make sure p and q are different
    while p == q:
        q = generate_prime()

    n = p*q
    
    phi_n = (p - 1) * (q - 1)

    e = find_e(phi_n)

    gcd, d, _ = extended_euclidean(e, phi_n)

    # make sure d is positive
    if d < 0:
        d += phi_n
    

    # open a file in write mode ('w') and save integers
    with open('p_q.txt', 'w') as file:
        file.write(f"{p}\n")
        file.write(f"{q}")

    with open('e_n.txt', 'w') as file:
        file.write(f"{e}\n")
        file.write(f"{n}")

    with open('d_n.txt', 'w') as file:
        file.write(f"{d}\n")
        file.write(f"{n}")

    print("done with key generation!")

    return n, e, d

def generate_prime():
    while True:
        # generate random number between [2^127 to 2^256 -1] and ensure odd (bitwise)
        candidate = random.randint(2**127, 2**256 - 1) | 1
        
        # this ensure that its not a multiple of 5
        if candidate % 5 == 0:
            continue
        
        if FermatPrimalityTest(candidate):
            return candidate

# extended euclidean algorithm
def extended_euclidean(a, b):
    if b == 0:
        # base case
        return a, 1, 0
    # recursive step
    gcd, x1, y1 = extended_euclidean(b, a % b)

    # update x and y using result from recursion
    x = y1
    y = x1 - (a // b) * y1

    #return gcd, x (modular inverse), and y (coefficient for b)
    return gcd, x, y

# finding public key (e)
def find_e(phi_n):
    # common starting e
    e = 65537
    
    # check if e is coprime with phi_n
    if math.gcd(e, phi_n) == 1:
        return e
    
    # if 65537 isn't valid, we pick a different e
    while True:
        # make e range from 3 to phi_n and increment by 2 for odd
        e = random.randrange(3, phi_n, 2)
        if math.gcd(e, phi_n) == 1:
            return e
        
def main():
    RSA_key_generation()

if __name__ == "__main__":
    main()
=======
# algorithms Project 1 - RSA
# objective: implement RSA Encryption and apply it to digital signature

import pandas as pd
import numpy as np
import hashlib
import random
import time
import math

print (hashlib.algorithms_guaranteed)

h = hashlib.sha256(b'computer science at UA is the best')
m = h.hexdigest()
print(m)

# if 'p' is prime, then for any integer 'a' such that 1 < a < p, we have:
# a^(p-1) congruent to 1(mod p)
#
# if equation holds, p might be prime
# if it does NOT hold, then p is definitely NOT prime (composite)

# this function check if the input is a relative prime or not
def FermatPrimalityTest(p):
    # print(p)
    a = False
    # to be completed
    if p <= 1:
        return a
    if p == 2 or p == 3:
        return True
    
    # fixed number of test for better accuracy
    num_test = 2

    for _ in range(num_test):
        # pick a random base for range [2, p-2]
        base = random.randint(2, p-2)

        # check if base^(p-1) is congruent to 1 (mod p)
        if pow(base, p-1, p) != 1:
            return a
    return True

# you need to modify this function to generate two pairs of keys
def RSA_key_generation():

    p = generate_prime()
    q = generate_prime()
    # make sure p and q are different
    while p == q:
        q = generate_prime()

    n = p*q
    
    phi_n = (p - 1) * (q - 1)

    e = find_e(phi_n)

    gcd, d, _ = extended_euclidean(e, phi_n)

    # make sure d is positive
    if d < 0:
        d += phi_n
    

    # open a file in write mode ('w') and save integers
    with open('p_q.txt', 'w') as file:
        file.write(f"{p}\n")
        file.write(f"{q}")

    with open('e_n.txt', 'w') as file:
        file.write(f"{e}\n")
        file.write(f"{n}")

    with open('d_n.txt', 'w') as file:
        file.write(f"{d}\n")
        file.write(f"{n}")

    print("done with key generation!")

    return n, e, d

def generate_prime():
    while True:
        # generate random number between [2^127 to 2^256 -1] and ensure odd (bitwise)
        candidate = random.randint(2**127, 2**256 - 1) | 1
        
        # this ensure that its not a multiple of 5
        if candidate % 5 == 0:
            continue
        
        if FermatPrimalityTest(candidate):
            return candidate

# extended euclidean algorithm
def extended_euclidean(a, b):
    if b == 0:
        # base case
        return a, 1, 0
    # recursive step
    gcd, x1, y1 = extended_euclidean(b, a % b)

    # update x and y using result from recursion
    x = y1
    y = x1 - (a // b) * y1

    #return gcd, x (modular inverse), and y (coefficient for b)
    return gcd, x, y

# finding public key (e)
def find_e(phi_n):
    # common starting e
    e = 65537
    
    # check if e is coprime with phi_n
    if math.gcd(e, phi_n) == 1:
        return e
    
    # if 65537 isn't valid, we pick a different e
    while True:
        # make e range from 3 to phi_n and increment by 2 for odd
        e = random.randrange(3, phi_n, 2)
        if math.gcd(e, phi_n) == 1:
            return e
        
def main():
    RSA_key_generation()

if __name__ == "__main__":
    main()