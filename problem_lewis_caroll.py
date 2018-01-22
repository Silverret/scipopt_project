

from pyscipopt import Model, quicksum

def lewis_caroll_zebra(positions, carac):
    """
    Parameters:
        - n: Integer, number of queen and size of the grid
    Returns a model, ready to be solved.
    """

    m = Model()

    # create a binary variable for every field and value
    x = {}
    for i in range(5):
        for j in range(5):
            for k in range(5):
                name = str(i)+','+str(j)+','+str(k)
                x[i, j, k] = m.addVar(name, vtype='B')

    # only one value per carac in every field
    for i in range(5):
        for j in range(5):
            m.addCons(quicksum(x[i, j, k] for k in range(5)) == 1)

    # only "one coffee" constraint
    for j in range(5):
        for k in range(5):
            m.addCons(quicksum(x[i, j, k] for i in range(5)) == 1)

    m.addCons(x[0, 1, 0] == 1) # Le norvégien habite la première maison,
    m.addCons(x[1, 0, 0] == 1) # La maison à coté de celle du norvégien est bleue,
    m.addCons(x[2, 2, 0] == 1) # L’habitant de la troisième maison boit du lait,

    for i in range(5):
        m.addCons(x[i, 1, 1] == x[i, 0, 1]) # L’anglais habite la maison rouge,
        m.addCons(x[i, 2, 2] == x[i, 0, 3]) # L’habitant de la maison verte boit du café
        m.addCons(x[i, 0, 2] == x[i, 3, 0]) # L’habitant de la maison jaune fume des Kools,
        m.addCons(x[i, 1, 2] == x[i, 4, 1]) # L’espagnol a un chien,
        m.addCons(x[i, 1, 4] == x[i, 2, 3]) # L'ukrainien boit du thé
        m.addCons(x[i, 1, 3] == x[i, 3, 1]) # Le japonais fume des cravens
        m.addCons(x[i, 3, 2] == x[i, 4, 3]) # Le fumeur de old golds a un escargot
        m.addCons(x[i, 3, 3] == x[i, 2, 1]) # Le fumeur de gitanes boit du vin,

    m.addCons(x[0, 0, 4] == 0)
    for i in range(4):
        m.addCons(x[i, 0, 3] == x[i+1, 0, 4]) # La maison blanche se trouve juste après la verte,
    
    m.addCons(x[0, 3, 4]==x[1, 4, 2])
    m.addCons(x[0, 3, 0]==x[1, 4, 4])
    for i in range(1, 4):
        m.addCons(x[i, 3, 4]*(x[i+1, 4, 2] + x[i-1, 4, 2]) == x[i, 3, 4]) # Un voisin du fumeur de Chesterfields a un renard,
        m.addCons(x[i, 3, 0]*(x[i+1, 4, 4] + x[i-1, 4, 4]) == x[i, 3, 0]) # Un voisin du fumeur de Kools a un cheval.
    
    m.addCons(x[4, 3, 4]==x[3, 4, 2])
    m.addCons(x[4, 3, 0]==x[3, 4, 4])

    return m, x

if __name__ == '__main__':
    POSITIONS = range(5)
    COLORS = ["Blue", "Red", "Yellow", "Green", "White"]
    NATIONS = ["Norvegien", "Anglais", "Espagnol", "Japonais", "Ukrainien"]
    BOISSONS = ["Lait", "Vin", "Café", "Thé", "Autre"]
    CIGARS = ["Kools", "Cravens", "Old Gold", "Gitane", "Chester"]
    ANIMALS = ["Zebre", "Chien", "Renard", "Escargot", "Cheval"]
    CARAC = [COLORS, NATIONS, BOISSONS, CIGARS, ANIMALS]
    MODEL, X = lewis_caroll_zebra(POSITIONS, CARAC)

    MODEL.count()
    print("Solution Count : " + str(MODEL.getNCountedSols()))
    
    MODEL.optimize()

    print('\nSolution:\n')
    for i in range(5):
        print("Maison : " + str(i), end='\n\t')
        for j in range(5):
            for k in range(5):
                if MODEL.getVal(X[i, j, k]) == 1:
                    print(CARAC[j][k], end='\n\t')
        print()
