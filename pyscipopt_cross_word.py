
def read_inputs(n):

    grid = [[]]
    with open("./crossword_problem/crossword%s.txt" % str(n), "r") as crossword_file:
        grid = list(map(list, crossword_file.read().split("\n")))

    with open("./crossword_problem/words%s.txt" % str(n), "r") as words_file:
        words = words_file.read().split("\n")
    
    return grid, words

if __name__ == '__main__':
    grid, words = read_inputs(1)