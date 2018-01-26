import string

from constraint_programming import constraint_programming


def read_inputs(n):
    """
    read inputs

    :param n : integer in [1, 2], tells which crossword game to solve
    :return grid (list of list): [['#', '#', '#', '#', '#'], ['#', '#', '.', '#', '#']]
    : return words : ['to', 'at', 'tea', 'eat']
    """
    grid = [[]]
    with open("./crossword_problem/crossword%s.txt" % str(n), "r") as crossword_file:
        grid = list(map(list, crossword_file.read().split("\n")))

    with open("./crossword_problem/words%s.txt" % str(n), "r") as words_file:
        words = list(map(str.lower, words_file.read().split("\n")))

    return grid, words

def find_segments(case, cases):
    """
    Function which find zero, one or two segments for the case (input)
    """
    i, j = case

    same_row_cases = sorted([case for case in cases if case[0] == i], key=lambda x: abs(x[1]-j))
    row_seg = {case}
    for same_row_case in same_row_cases:
        if same_row_case[1]+1 in {case[1] for case in row_seg} or   \
                same_row_case[1]-1 in {case[1] for case in row_seg}:
            row_seg.add(same_row_case)

    same_col_cases = sorted([case for case in cases if case[1] == j], key=lambda x: abs(x[0]-i))
    col_seg = {case}
    for same_col_case in same_col_cases:
        if same_col_case[0]+1 in {case[0] for case in col_seg} or   \
                same_col_case[0]-1 in {case[0] for case in col_seg}:
            col_seg.add(same_col_case)

    segments = []
    if len(row_seg) > 1:
        segments.append(tuple(sorted(row_seg, key=lambda x: x[1])))
    if len(col_seg) > 1:
        segments.append(tuple(sorted(col_seg, key=lambda x: x[0])))

    return segments

def create_words_set(seg1, seg2, case, var, words):
    words_set = set()
    for letter in string.ascii_lowercase:
        for i in [i for i in var[seg1] if words[i][seg1.index(case)] == letter]:
            for j in [j for j in var[seg2] if words[j][seg2.index(case)] == letter]:
                words_set.add((i, j))
    return words_set

def main(n):
    grid, words = read_inputs(n)

    # cases = {(1, 2), (2, 1), (2, 2), (2, 3), (3, 2)} par exemple
    cases = {(i, j) for i, row in enumerate(grid) for j, x in enumerate(row) if x == '.'}

    # segments = [((1,2),(2,2),(3,2)),((2,1),(2,2),(2,3))] par exemple
    segments = []
    for case in cases:
        for case_seg in find_segments(case, cases):
            if not case_seg in segments:
                segments.append(case_seg)

    # Modèle
    var = {seg: {i for i, word in enumerate(words) if len(word) == len(seg)} for seg in segments}

    # Contraintes unaires

    # Solver instaciation
    P = constraint_programming(var)

    # relation
    intersections_number = 0
    for i, seg1 in enumerate(segments):
        for seg2 in segments[i+1:]:
            common_case = [case for case in seg1 if case in seg2]
            if common_case:
                intersections_number += 1
    print("Number of intersections : "+str(intersections_number))

    intersections_number = 0
    for i, seg1 in enumerate(segments):
        for seg2 in segments[i+1:]:
            common_case = [case for case in seg1 if case in seg2]
            if common_case:
                intersections_number += 1
                words_set = create_words_set(seg1, seg2, common_case[0], var, words)
                P.addConstraint(seg1, seg2, words_set)
                print(intersections_number, seg1, seg2, common_case, len(words_set))

    # Résultats
    print("Let solve it !")
    P.maintain_arc_consistency()
    dic_solve = P.solve()

    for seg, l in dic_solve.items():
        for k, case in enumerate(seg):
            i, j = case
            grid[i][j] = words[l][k]

    for row in grid:
        for c in row:
            print(c, end='')
        print()


if __name__ == '__main__':
    main(3)
