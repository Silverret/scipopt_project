from collections import defaultdict
import sys

from constraint_programming import constraint_programming as CSP

with open(sys.argv[1], 'r') as f:
    words = set(word.lower().replace("'", "") for word in f.read().split('\n'))
words -= set([''])

words_by_length = defaultdict(set)
for word in words:
    words_by_length[len(word)].add(word)

letters = set(let for word in words for let in word)

with open(sys.argv[2], 'r') as f:
    crosswords = f.read()

# crosswords="#"*6+'\n'+'#...##'+'\n'+'#.'+'#'*4+"\n"+'#.'+'#'*4+'\n'+"#"*6+'\n'
cases = set()
i = -1
j = 0
for char in crosswords:
    if char == ".":
        cases.add((i, j))
    elif char == "\n":
        i = -1
        j += 1
    i += 1

domains = dict()

first_horizontal = set()
first_vertical = set()
# Domain restriction for starting letters
for x, y in cases:
    horizontal_test = (x + 1, y) in cases and (x - 1, y) not in cases
    vertical_test = (x, y + 1) in cases and (x, y - 1) not in cases
    if horizontal_test:
        first_horizontal.add((x, y))
    if vertical_test:
        first_vertical.add((x, y))

for x, y in first_horizontal:
    length = 1
    while (x + length, y) in cases:
        length += 1
    # domains[(x, y)] &= set(x[0] for x in words_by_length[length])
    for i in range(length):
        domains[(x + i, y)] = set((x[i], x) for x in words_by_length[length])

for x, y in first_vertical:
    length = 1
    while (x, y + length) in cases:
        length += 1
    # domains[(x, y)] &= set(x[0] for x in words_by_length[length])
    for i in range(length):
        if (x, y + i) in first_horizontal:
            domains[(x, y + i)] &= set((x[i], x) for x in words_by_length[length])
        else:
            domains[(x, y + i)] = set((x[i], x) for x in words_by_length[length])

P = CSP(domains)

# Relations for inner letters
for x, y in first_horizontal:
    length = 1
    while (x + length, y) in cases:
        length += 1

    for l in range(1, length):
        relations = set(((word[0], word), (word[l], word)) for word in words_by_length[length])
        P.addConstraint((x + i, y), (x + l, y), relations)
        # for i in range(l):
        #     relations = set(((word[i],word), (word[l],word)) for word in words_by_length[length])
        #     P.addConstraint((x + i, y), (x + l, y), relations)

for x, y, in first_vertical:

    length = 1
    while (x, y + length) in cases:
        length += 1

    for l in range(1, length):
        relations = set(((word[0], word), (word[l], word)) for word in words_by_length[length])
        P.addConstraint((x + i, y), (x + l, y), relations)
        # for i in range(l):
        #    relations = set(((word[i], word), (word[l], word)) for word in words_by_length[length])
        #    P.addConstraint((x, y + i), (x, y + l), relations)

sol = P.solve()
n_col = len(crosswords.split('\n')[0])
n_line = crosswords.count('\n')
for j in range(n_line):
    line = ["#"] * n_col
    for i in range(n_col):
        if (i, j) in sol:
            line[i] = sol[(i, j)][0]
    print("".join(line))
