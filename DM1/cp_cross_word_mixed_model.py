import string
import sys

from constraint_programming import constraint_programming


def read_inputs():
    """
    read inputs

    :return grid (list of list): [['#', '#', '#', '#', '#'], ['#', '#', '.', '#', '#']]
    : return words : ['to', 'at', 'tea', 'eat']
    """

    with open(sys.argv[1], "r") as words_file:
        words = list(map(str.lower, words_file.read().split("\n")))

    with open(sys.argv[2], "r") as crossword_file:
        grid = list(map(list, crossword_file.read().split("\n")))

    return grid, words


def find_segments(case, cases):
    """
    Function which find zero, one or two segments for the case (input)

    :return [((1, 2), (2, 2), (3, 2)), ((2, 1), (2, 2), (2, 3))] for input = (2, 2)
    """
    i, j = case

    same_row_cases = sorted([case for case in cases if case[0] == i], key=lambda x: abs(x[1] - j))
    row_seg = {case}
    for same_row_case in same_row_cases:
        if same_row_case[1] + 1 in {case[1] for case in row_seg} or \
                                same_row_case[1] - 1 in {case[1] for case in row_seg}:
            row_seg.add(same_row_case)

    same_col_cases = sorted([case for case in cases if case[1] == j], key=lambda x: abs(x[0] - i))
    col_seg = {case}
    for same_col_case in same_col_cases:
        if same_col_case[0] + 1 in {case[0] for case in col_seg} or \
                                same_col_case[0] - 1 in {case[0] for case in col_seg}:
            col_seg.add(same_col_case)

    segments = []
    if len(row_seg) > 1:
        segments.append(tuple(sorted(row_seg, key=lambda x: x[1])))
    if len(col_seg) > 1:
        segments.append(tuple(sorted(col_seg, key=lambda x: x[0])))

    return segments


def main():
    grid, words = read_inputs()

    # cases = {(1, 2), (2, 1), (2, 2), (2, 3), (3, 2)} par exemple
    cases = {(i, j) for i, row in enumerate(grid) for j, x in enumerate(row) if x == '.'}

    # segments = [((1,2),(2,2),(3,2)),((2,1),(2,2),(2,3))] par exemple
    segments = list()
    for case in cases:
        for seg in find_segments(case, cases):
            if not seg in segments:
                segments.append(seg)

    # Modèle : les variables sont : cases + segments
    var = {}
    for case in cases:
        var[case] = set(string.ascii_lowercase)
    for seg in segments:
        var[seg] = {word for word in words if len(seg) == len(word)}

    # Solver instanciation
    P = constraint_programming(var)
    P.maintain_AC = False

    # Relations
    for seg in segments:
        for i, case in enumerate(seg):
            word_letter_set = set()
            for word in var[seg]:
                word_letter_set.add((word, word[i]))
            P.addConstraint(seg, case, word_letter_set)

    print("Let's solve it !")
    dic_solve = P.solve()

    # Résultats
    if dic_solve is None:
        print("No solution was found.")
        return

    # Print it !
    n_col = len(grid[0])
    n_row = len(grid)
    new_grid = list(grid)
    for var, value in dic_solve.items():
        if value in set(string.ascii_lowercase):
            i, j = var
            new_grid[i][j] = value
    grid_str = ""
    for i in range(n_row):
        for j in range(n_col):
            grid_str += new_grid[i][j]
        grid_str += "\n"

    print(grid_str)
    return grid_str


if __name__ == '__main__':
    main()