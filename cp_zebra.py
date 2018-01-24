from constraint_programming import constraint_programming

# Modèle
maisons = range(1, 6)
noms = [
    ["jaune", "blanche", "bleue", "rouge", "verte"], # couleurs
    ["café", "thé", "lait", "vin", "eau"], # boissons
    ["cheval", "renard", "escargot", "chien", "zèbre"], # animaux
    ["Kools", "cravens", "old golds", "gitanes", "Chesterfields"], # cigarettes
    ["norvégien", "anglais", "espagnol", "japonais", "ukrainien"] # nationalités
]
vars = {x: set(maisons) for cotegorie in noms for x in cotegorie}

# Contraintes unaires
vars["norvégien"] = set([1])
vars["lait"] = set([3])

P = constraint_programming(vars)

# relations
EQ = {(i, i) for i in maisons}

NEQ = {(i, j) for i in maisons for j in maisons if i != j}

NEXT = {(i, j) for i in maisons for j in maisons if j == i+1}
BEFORE = {(i, j) for i in maisons for j in maisons if j == i-1}
NEXTORBEFORE = {(i, j) for i in maisons for j in maisons if j == i+1 or j == i-1}

P.addConstraint("norvégien", "bleue", NEXTORBEFORE)
P.addConstraint("anglais", "rouge", EQ)
P.addConstraint("verte", "café", EQ)
P.addConstraint("jaune", "Kools", EQ)
P.addConstraint("blanche", "verte", NEXT)
P.addConstraint("espagnol", "chien", EQ)
P.addConstraint("ukrainien", "thé", EQ)
P.addConstraint("japonais", "cravens", EQ)
P.addConstraint("old golds", "escargot", EQ)
P.addConstraint("gitanes", "vin", EQ)
P.addConstraint("Chesterfields", "renard", EQ)
P.addConstraint("Kools", "cheval", EQ)

for categorie in noms:
    for x in categorie:
        for y in categorie:
            if x != y:
                P.addConstraint(x, y, NEQ)

count = 0
for sol in P.solve():
    count += 1

dic_solve = P.solve()

result = {}

for key, value in dic_solve.items():
    result[value] = ""

for key, value in dic_solve.items():
    result[value] += str(key) + ","

for key, value in result.items():
    print("Maison " + str(key) + ": " + str(value))

if count == 0:
    print("There is no solution")
elif count == 1:
    print("The solution is unique")
else:
    print("There are %i solutions" % count)


    # Le norvégien habite la première maison,
    # La maison à coté de celle du norvégien est bleue,
    # L’habitant de la troisième maison boit du lait,
    # L’anglais habite la maison rouge,
    # L’habitant de la maison verte boit du café,
    # L’habitant de la maison jaune fume des Kools,
    # La maison blanche se trouve juste après la verte,
    # L’espagnol a un chien,
    # L’ukrainien boit du thé,
    # Le japonais fume des cravens,
    # Le fumeur de old golds a un escargot,
    # Le fumeur de gitanes boit du vin,
    # Un voisin du fumeur de Chesterfields a un renard,
    # Un voisin du fumeur de Kools a un cheval.
