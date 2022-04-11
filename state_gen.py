M = 10
N = 20
Q = 500

S_gen = set()
S_ref = set()

# Case 1
for z in range(N):
    S_gen.add((0, 0, z))

# Case 2
for y in range(1, M + 1):
    for z in range(1, N):
        S_gen.add((0, y, z))

# Case 3
S_gen.add((1, 0, 0))

# Case 4
for x in range(1, Q):
    for z in range(N):
        S_gen.add((x, 0, z))

# Case 5
for x in range(1, Q):
    for y in range(1, M + 1):
        S_gen.add((x, y, 0))

# Case 6
for x in range(1, Q):
    for y in range(1, M + 1):
        for z in range(1, N):
            S_gen.add((x, y, z))

# Case 7
for x in range(2, Q):
    S_gen.add((x, 0, 0))

# Case 8
for y in range(M + 1):
    for z in range(N):
        S_gen.add((Q, y, z))

# Case 9
for y in range(1, M + 1):
    S_gen.add((0, y, 0))

for x in range(Q + 1):
    for y in range(M + 1):
        for z in range(N):
            S_ref.add((x, y, z))

print(len(S_ref), len(S_gen))
print(len(S_ref.difference(S_gen)))
print(len(S_gen.difference(S_ref)))
for state in S_ref.difference(S_gen):
    print(state)
    input()