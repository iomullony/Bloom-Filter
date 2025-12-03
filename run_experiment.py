from bloom_filter import BloomFilter, estimate_fpr, estimation

n1 = 10000   # number of items expected to be insert in filter
p1 = 0.01    # False Positive probability (1%)

bf1 = BloomFilter(n1, p1)

# Insert n items
for i in range(n1):
    bf1.insert(f"elemet_{i}")

# Estimate FPR
measured_fpr = estimate_fpr(bf1, trials=20000)

print("---- Bloom Filter Experiment 1 with p = 1% ----")
print(f"p (target FPR): {p1}")
print(f"m (bits): {bf1.m}")
print(f"k (hash functions): {bf1.k}")
print(f"n (number of inserted elements): {bf1.count}") # check that n elements have been inserted
print(f"Measured false-positive rate: {measured_fpr:.5f}\n")

# =============================================

n2 = 10000
p2 = 0.001    # False Positive probability (0.1%)

bf2 = BloomFilter(n2, p2)

for i in range(n2):
    bf2.insert(f"elemet_{i}")

measured_fpr = estimate_fpr(bf2, trials=20000)

print("---- Bloom Filter Experiment 2 with p = 0.1% ----")
print(f"p (target FPR): {p2}")
print(f"m (bits): {bf2.m}")
print(f"k (hash functions): {bf2.k}")
print(f"n (number of inserted elements): {bf2.count}")
print(f"Measured false-positive rate: {measured_fpr:.5f}")