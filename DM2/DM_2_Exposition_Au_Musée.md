# DM2 Exposition au Musée

par Silvestre Perret et Mathieu Seris

# Approche
Nous avons essayé plusieurs approches pour résoudre ce problème:

## Résolution par programmation linéaire
Variables :
Nos variables sont les emplacements des caméras dans le musée. Nous créons un ensemble (finis) de positions possibles pour les caméras et nous associons à chaque position deux variables booléennes (une par type de caméra) qui indiquent si oui ou non une caméra (petite ou grande) est installée sur cette position.

Nous avons essayé plusieurs ensembles de positions possibles pour résoudre le problème.
Notre première approche a été de considérer un quadrillage de la zone à couvrir. Sur une sous problème de taille 20\*20, les résultats étaient bons. Malheureusement le passage à l'échelle s'est avéré difficile (800\*800\*2 variables), même en augmentant la maille du quadrillage.

Notre deuxième approche a eu pour but de diminuer le nombre de variables de notre modèle, nous nous sommes inspirés du *Bomb Problem* ou du *Texas sharpshooter fallacy Problem*. Pour chaque couple d'oeuvres suffisamment proches pour être couvertes par une caméra nous trouvons les deux points tels que la distance entre un point et chacune des deux oeuvres soit égale au rayon de la caméra. Cela nous réduit le nombre de variable à environ 15 000 et nous obtenons un temps de résolution d'une dizaine de minute (la résolution des problèmes géométriques étant la tâche prenant le plus de temps). 


### Contraintes :
Nous créons une contrainte par oeuvre dans le musée. Pour chaque oeuvre, nous imposons qu'au moins une caméra soit installée sur une position à portée de l'oeuvre (tous types confondues) 


### Critère d'optimisation :
Nous demandons au solveur de minimiser le coût total de l'installation.


## Résolution par recherche locale
Nous avons repris l'approche de la première partie pour trouver un premier ensemble de positions de caméras à partir de 
positions de cercles couvrant au moins une paires de caméras non couvertes jusque là prises aléatoirement. Nous avons découpé 
l'espace de des objets d'art en carré de coté 100 (soit en 64 carrées différents). La solution obtenue est ainsi non optimale
mais acceptable, avec des scores moyens proches de 3600.

Ensuite, nous améliorons cette solution par plusieurs approches :
* en supprimant les petites caméras dans les zone couvertes par les grandes,
* en supprimant les caméras qui peuvent être supprimées sans qu'un objet d'art devienne non couvert par une caméra.

Après améliorations, nous arrivons à des scores proches de 3500.


Nous avons pensé à plusieurs autres pistes d'améliorations, que nous n'avons pas eu le temps d'implémenter, comme :
* décaler les caméras existantes avec des objets d'art proches,
* remplacer des petites caméras adjacentes par une unique grande caméra.

Actuellement, les améliorations implémentées ne modifient pas suffisamment la solution obtenue pour réaliser plusieurs boucles
d'optimisation en recherche locale.