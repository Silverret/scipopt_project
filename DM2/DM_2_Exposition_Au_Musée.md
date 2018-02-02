# DM2 Exposition au Musée

par Silvestre Perret et Mathieu Seris

# Approche
Nous avons essayé plusieurs approches pour résoudre ce problème:

## Résolution par programmation linéaire
Variables :
Nos variables sont les emplacements des caméras dans le musée. Nous créons un ensemble (finis) de positions possibles pour les caméras et nous associons à chaque position deux variables booléennes (une par type de caméra) qui indiquent si oui ou non une caméra (petite ou grande) est installée sur cette position.

Nous avons essayé plusieurs ensembles de positions possibles pour résoudre le problème.
Notre première approche a été de considérer un quadrillage de la zone à couvrir. Sur une sous problème de taille 20\*20, les résultats étaient bons. Malheureusement le passage à l'échelle s'est avéré difficile (800\*800\*2 variables), même en augmentant la maille du quadrillage.

Notre deuxième approche a eu pour but de diminuer le nombre de variables de notre modèle, nous nous sommes inspirés de ???? (Mathieu tu avais vu où ce qu'on a fait avec des cercles). Pour chaque couple d'oeuvres suffisamment proches pour être couvertes par une caméra nous trouvons les deux points tels que la distance entre un point et chacune des deux oeuvres soit égale au rayon de la caméra. Cela nous réduit le nombre de variable à environ 15 000 et nous obtenons un temps de résolution d'une dizaine de minute (la résolution des problèmes géométriques étant la tâche prenant le plus de temps). 


Contraintes :
Nous créons une contrainte par oeuvre dans le musée. Pour chaque oeuvre, nous imposons qu'au moins une caméra soit installée sur une position à portée de l'oeuvre (tous types confondues) 


Critère d'optimisation :
Nous demandons au solveur de minimiser le coût total de l'installation.


## Résolution par recherche locale