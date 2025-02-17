# algorithms Project 1 - RSA
# objective: implement RSA Encryption and apply it to digital signature

import pandas as pd
import numpy as np
import hashlib
import random
import time

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

# check for gcd
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

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
    if gcd(e, phi_n) == 1:
        return e
    
    # if 65537 isn't valid, we pick a different e
    while True:
        # make e range from 3 to phi_n and increment by 2 for odd
        e = random.randrange(3, phi_n, 2)
        if gcd(e, phi_n) == 1:
            return e
        
# read private key (d, n) from d_n.txt
def read_private_key():
    with open("d_n.txt", "r") as file:
        d = int(file.readline().strip())
        n = int(file.readline().strip())
    return d, n

# read public key (e, n) from e_n.txt
def read_public_key():
    with open("e_n.txt", "r") as file:
        e = int(file.readline().strip())
        n = int(file.readline().strip())
    return e, n

# sign file using RSA private key
def Signing(doc, key):
    d, n = key

    # read original file content
    with open(doc, "rb") as file:
        content = file.read()

    # sha-256 hash of file content
    hash_value = hashlib.sha256(content).digest()
    hash_int = int.from_bytes(hash_value, byteorder="big")

    # signing
    signature = pow(hash_int, d, n)

    # convert signature to 64-byte for appending to original content
    # because n is slightly less than 512 bits (64 bytes)
    signature_bytes = signature.to_bytes(64, byteorder="big", signed=False)

    # save signed file
    signed_file = doc + ".signed"
    with open(signed_file, "wb") as file:
        # write the original file content
        file.write(content)
        # append the signature
        file.write(signature_bytes)

    print("\nSigned ...")
    return signed_file

# verify signed file
def verification(doc, key):
    e, n = key

    # read signed file
    with open(doc, "rb") as file:
        content = file.read()

    # everything except the last 64 bytes
    original_content = content[:-64]

    # the last 64 bytes (signature)
    signature_bytes = content[-64:]

    # compute sha-256 of the extracted original file
    new_hash_value = hashlib.sha256(original_content).digest()
    new_hash_int = int.from_bytes(new_hash_value, byteorder="big")

    # convert signature_bytes to int
    signature_int = int.from_bytes(signature_bytes, byteorder="big")

    # verify
    decrypted_signature = pow(signature_int, e, n)

    # compare decrypt with new hash
    if decrypted_signature == new_hash_int:
        print("\nAuthentic!")
    else:
        print("\nModified!")
    
    return decrypted_signature == new_hash_int

# No need to change the main function.
# 
def CPSC_435_Project1(part, task="", fileName=""):
    # part I, command-line arguments will be: python yourProgram.py 1
    if part == 1:
        RSA_key_generation()
    # part II, command-line will be for example: python yourProgram.py 2 s file.txt
    #                                       or   python yourProgram.py 2 v file.txt.signed
    else:
        if "s" in task:  # do signing
            doc = fileName   # you figure out
            key = read_private_key()   # you figure out
            Signing(doc, key)
        else:
            # do verification
            doc = fileName   # you figure out
            key = read_public_key()   # you figure out
            verification(doc, key)

    print("done!")
    
    return

# when we grade your part 1 - RSA_key_generation
CPSC_435_Project1(1)

# when we grade your part 2a - signing
docName = "contract.txt" # the fileName is just an example
CPSC_435_Project1(2, "s", docName)

# when we grade your part 2b - verification
docName = "contract.txt.signed" # the fileName is just an example
CPSC_435_Project1(2, "v", docName)
