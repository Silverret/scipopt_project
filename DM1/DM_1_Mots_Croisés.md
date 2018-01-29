# DM1 Mots-Croisés 

par Silvestre Perret et Mathieu Seris

# Approche
Nous avons essayé plusieurs approches pour résoudre ce problème à contraintes:

## Approche par les lettres (primal)
Dans un premier temps, nous avons essayé de résoudre une grille de mots-croisés en modélisant les lettres (ou cases à remplir).
Nous restreignions le domaine des lettres (nos variables) aux lettres possibles (selon la taille du mots et la position de la lettre).
Cette approche induit de mauvais résultats car les lettres ont des relations plus complexes qu'unaires et binaires pour former des mots.

Exemple :
ABC, EBD et AFD comme mots possibles de notre problème avec des relations unaires et binaires sur les lettres peuvent générer comme mot possible : ABD (qui ne fait pas partie des mots possibles)


## Approche par les mots (dual)
Dans un second temps, nous avons essayé de modéliser le problème par 'segment': chaque segment pouvait recevoir des mots de taille correspondante (domaines de variables).
Nous contraignions ces segments sur chaque intersection en couple de mots possibles (partageant une même lettre au niveau de cette intersection).
Bien que cette approche marche correctement sur un petit exemple (words1 et crosswrod1), la création des contraintes binaires est très longue.

## Approche mixte lettres/mots
Enfin, nous définissons comme variables à la fois les lettres (cases) et mots(segments).
Les segments ont pour domaine des mots de taille correspondante. Nous n'avons pas mis de contraintes unaires sur les lettres.
Pour chaque couple de case/segment, on associe la lettre correspondante au mot possible.
Nous n'obtenons avec cette approche de bons résultats en temps raisonnables.

#  Expérimentation

Nous avons testé de résoudre ce problème par contrainte en maintenant ou non l'arc consistance.

Voici nos résultats expérimentaux:
- sans maintenir l'Arc Consistence  : 2.140 s
- en maintenant l'Arc Consistence   : 6.223 s

Conclusion: l'Arc Consistence donne ici des résultats plus rapidement.