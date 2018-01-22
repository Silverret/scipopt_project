#/usr/bin/env pypy

from pyscipopt import Model, quicksum

def chessqueen_mip(n):
    """
    Parameters:
        - n: Integer, number of queen and size of the grid
    Returns a model, ready to be solved.
    """
    model = Model()

    x = {}
    for i in range(1, n+1):
        for j in range(1, n+1):
            # Pour chaque case :
            x[i, j] = model.addVar(vtype="B", name="x(%s,%s)"%(i, j))

    for i in range(1, n+1):
        # Pour chaque ligne :
        model.addCons(quicksum(x[i, j] for j in range(1, n+1)) == 1)

    for j in range(1, n+1):
        # Pour chaque colonne :
        model.addCons(quicksum(x[i, j] for i in range(1, n+1)) == 1)

    for d in range(1, (2*n-1)+1):
        # Pour chaque diagonale ←↑ →↓ :
        if d <= n:
            model.addCons(quicksum(x[k, d+1-k] for k in range(1, n-abs(n-d)+1)) <= 1)
        else:
            model.addCons(quicksum(x[d-n+k, n-k+1] for k in range(1, n-abs(n-d)+1)) <= 1)

    for d in range(1, (2*n-1)+1):
        # Pour chaque diagonale →↑ ←↓ :
        if d <= n:
            model.addCons(quicksum(x[k, n-d+k] for k in range(1, n-abs(n-d)+1)) <= 1)
        else:
            model.addCons(quicksum(x[d-n+k, k] for k in range(1, n-abs(n-d)+1)) <= 1)

    return model

if __name__ == '__main__':
    MIP = chessqueen_mip(10)
    MIP.optimize()