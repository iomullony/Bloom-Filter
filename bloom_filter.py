import math
import hashlib
import random
import string
from bitarray import bitarray

# optimal Bloom filter parameters m and k for n and p
def compute_parameters(n, p):
    m = int(math.ceil(-n * math.log(p) / (math.log(2) ** 2))) # size of bit array
    k = int(round((m / n) * math.log(2))) # number of hash functions to be used

    return m, k


# h_i(x) = h1(x) + i * h2(x) mod m
def double_hashing(item, m, k):
    indexes = []

    # To be able to use the hash functions we need to convert first to bytes
    if isinstance(item, str):
        item = item.encode("utf-8")

    h1 = int(hashlib.sha256(item).hexdigest(), 16)
    h2 = int(hashlib.md5(item).hexdigest(), 16)
    if h2 == 0: h2 = 1 # make sure that h2 is not 0

    for i in range(k):
        indexes.append((h1 + i * h2) % m)

    return indexes


class BloomFilter:
    def __init__(self, n, p):
        self.n = n
        self.p = p
        self.count = 0

        self.m, self.k = compute_parameters(n, p)
        self.bit_array = bitarray(self.m)
        self.bit_array.setall(0) # initialize all bits to 0

    def insert(self, element):
        for idx in double_hashing(element, self.m, self.k):
            self.bit_array[idx] = 1
        self.count += 1

    def lookup(self, element):
        return all(self.bit_array[idx] for idx in double_hashing(element, self.m, self.k))


# Query random elements NOT inserted into the Bloom filter
# and estimate the empirical false-positive rate
def estimate_fpr(bf, trials=10000):
    false_positives = 0
    tested = 0

    for _ in range(trials):
        # random string not likely to be inserted
        x = ''.join(random.choice(string.ascii_letters) for _ in range(10))

        if bf.lookup(x):
            false_positives += 1
        tested += 1
 
    return false_positives / tested


def estimation(bf, n):
    p = (1 - (1 - (1 / bf.m))**(bf.k * n)) ** bf.k
    return p