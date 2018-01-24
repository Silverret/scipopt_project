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

    model.setObjective(
        quicksum(x[i, j]*j*4**(n-i) for i in range(1, n+1) for j in range(1, n+1)),
        "minimize")
    return model, x

def chessqueen_cp(n):
    """
    Parameters:
        - n: Integer, number of queen and size of the grid
    Returns a model, ready to be solved.
    """
    model = Model()
    pass


if __name__ == '__main__':

    N = 20
    MIP, X = chessqueen_mip(N)
    MIP.optimize()

    print("\n=================================================")
    print("Optimal value: %f" % MIP.getObjVal())
    for i in range(1, N+1):
        for j in range(1, N+1):
            x_ij = MIP.getVal(X[i, j])
            if x_ij >= 0.5:
                print("x[%d, %d]\t:= %f" %(i, j, x_ij))

    print("\n=================================================")
    print("Answer is (index from 1 to N): ", end='')
    for i in range(1, N+1):
        for j in range(1, N+1):
            x_ij = MIP.getVal(X[i, j])
            if x_ij >= 0.5:
                print('{:0>2}'.format(j), end='')
    print("\nor with index from 0 to N-1: ", end='')
    for i in range(1, N+1):
        for j in range(1, N+1):
            x_ij = MIP.getVal(X[i, j])
            if x_ij >= 0.5:
                print('{:0>2}'.format(j-1), end='')
    print("\n=================================================")

    # On print l'échiquier
    print("\t|", end='')
    for j in range(1, N+1):
        print('{:>5}'.format(f" {j} |"), end='')
    print("\n" + "-" * (8+N*5))
    for i in range(1, N+1):
        print(f"x{i}  \t|", end='')
        for j in range(1, N+1):
            x_ij = MIP.getVal(X[i, j])
            if x_ij >= 0.5:
                print("  O |", end='')
            else:
                print("    |", end='')
        print("\n" + "-" * (8+N*5))
