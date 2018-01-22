#/usr/bin/env pypy

from pyscipopt import Model

def threecolorsgraph(v, e):
    """
    Parameters:
        - V: set/list of nodes in the graph
        - E: set/list of edges in the graph
    Returns a model, ready to be solved.
    """
    model = Model()

    x = {}
    y = {}
    for i in v:
        x[i*3+1] = model.addVar(vtype="B", name="x(%s)"%(i*3+1))
        x[i*3+2] = model.addVar(vtype="B", name="x(%s)"%(i*3+2))
        x[i*3+3] = model.addVar(vtype="B", name="x(%s)"%(i*3+3))

        model.addCons(x[i*3+1] + x[i*3+2] + x[i*3+3] == 1)

    for (i, j) in e:
        model.addCons(x[i*3+1] + x[j*3+1] <= 1)
        model.addCons(x[i*3+2] + x[j*3+2] <= 1)
        model.addCons(x[i*3+3] + x[j*3+3] <= 1)

    return model

if __name__ == '__main__':
    V = range(10)
    E = [
        (0, 1), (0, 4), (0, 7),
        (1, 5), (1, 2),
        (2, 3), (2, 9),
        (3, 4), (3, 6),
        (4, 8),
        (5, 6), (5, 8),
        (6, 7),
        (7, 9),
        (8, 9)
        ]

    MODEL = threecolorsgraph(V, E)
    MODEL.count()
    print(MODEL.getNCountedSols())
