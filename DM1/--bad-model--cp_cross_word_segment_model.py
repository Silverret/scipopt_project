"""
This module implements our last model for the crossword problem : the dual one.

Please see DM_1_Mots_Croisés.md for more details.

Use the command below to launch it:
python cp_cross_word_mixed_model <path_to_word_list> <path_to_grid>
"""
import sys

from constraint_programming import constraint_programming as CSP

with open(sys.argv[1], 'r') as f:
    words = set(f.read().split('\n'))
words -= set([''])

with open(sys.argv[2], 'r') as f:
    crosswords = f.read()

empty_boxes = set()
i = -1
j = 0
for char in crosswords:
    if char == ".":
        empty_boxes |= set([(i, j)])
    elif char == "\n":
        i = -1
        j += 1
    i += 1

first_horizontal = set()
first_vertical = set()
# Domain restriction for starting letters
for x, y in empty_boxes:
    horizontal_test = (x + 1, y) in empty_boxes and (x - 1, y) not in empty_boxes
    vertical_test = (x, y + 1) in empty_boxes and (x, y - 1) not in empty_boxes
    if horizontal_test:
        first_horizontal |= set([(x, y)])
    if vertical_test:
        first_vertical |= set([(x, y)])

domains = {}
for x, y in first_horizontal:
    length = 1
    while (x + length, y) in empty_boxes:
        length += 1

    domains[(x, y, length, "h")] = set(filter(lambda w: len(w) == length, words))

for x, y, in first_vertical:

    length = 1
    while (x, y + length) in empty_boxes:
        length += 1
    domains[(x, y, length, "v")] = set(filter(lambda w: len(w) == length, words))
P = CSP(domains)

for x_h, y_h in first_horizontal:
    l_h = 1
    while (x_h + l_h, y_h) in empty_boxes:
        l_h += 1

    for x_v, y_v in first_vertical:
        l_v = 1
        while (x_v, y_v + l_v) in empty_boxes:
            l_v += 1
        if x_h <= x_v <= x_h + l_h - 1 and y_v <= y_h <= y_v + l_v - 1:
            relations = set()
            for word_h in filter(lambda w: len(w) == l_h, words):
                common_letter = word_h[x_v - x_h]
                for word_v in filter(lambda w: len(w) == l_v, words):
                    if common_letter == word_v[y_h - y_v]:
                        relations |= set([(word_h, word_v)])
            P.addConstraint((x_h, y_h, l_h, "h"), (x_v, y_v, l_v, "v"), relations)

sol = P.solve()

n_col = len(crosswords.split('\n')[0])
n_line = crosswords.count('\n')
matrix = [["#"] * n_col for _ in range(n_line)]
for x, y, l, o in sol:
    if o == "h":
        matrix[y][x:x + l] = list(sol[(x, y, l, o)])
    if o == "v":
        for j in range(l):
            matrix[y + j][x] = sol[(x, y, l, o)][j]

for line in matrix:
    print("".join(line))
