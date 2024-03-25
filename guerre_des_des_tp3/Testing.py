import operator

# verifier disponible pour attaque


# cases_joueur = {}
# for key, value in self.cases.items():
#     if value.appartenance == joueur:
#         cases_joueur[key] = self.cases[key]
# return cases_joueur

# print([k for k, v in stats.items() if v == 1000])
#
# print([k for k, v in self.cases.items() if v.appartenance == joueur])

# print(u"\u2680")
# print(u"\u2681")
# print(u"\u2685")


des = [6, 6, 6, 6, 6]
# passer chaque dés
# lancer le dés puis obtenir le chiffre
# additionner



from random import randint

dice_item = lambda: randint(1, 6)  # lancer

# def dice(n):
#     return sum(dice_item() for y in range(n))
#
# stats = {'a':1000, 'b':3000, 'c': 100, 'd':500, 'e':3000}
#
# print(max(stats, key=stats.get))


# unpacker tous les objets  case =  *cases.values() ---> acces tout les objets
# trouver case nombre des maximum   maximum = max(case.nombre_de_des())
# retourne les coors de cette case

# stats = max(stats, key=stats.get)
# print("Maximum value:", stats)
"""
x\y |   0    1    2    3    
----|---------------------
0   | [ 8 ][ 5 ][ 4 ]     
1   |      [ 5 ][ 2 ][ 5 ]
2   | [ 5 ][ 7 ][ 5 ][ 6 ]
3   | [ 4 ][ 7 ][ 7 ][ 4 ]

value dans joueur <case.Case object at Andre>
voison [<case.Case object at 0x0000013F9CA55A60>, <case.Case object at 0x0000013F9CA559A0>, <case.Case object at Tristan>, <case.Case object at Sophie>]

value dans joueur <case.Case object at Sophie>
voison [<case.Case object at Andre>, <case.Case object at Mathis>]

value dans joueur <case.Case object at Julie>
voison [0x0000013F9CA55CA0>, <0x0000013F9CA55A60>, <0x0000013F9CA600A0>, <Tristan>]

value dans joueur <case.Case object at Tristan>
voison [Julie>, <Andre>, <Louis>, <Mathis>]

value dans joueur <Mathis>
voison [Tristan>, <Sophie>, <0x0000013F9CA60220>]

value dans joueur <case.Case object at Louis>
voison [0x0000013F9CA600A0>, Tristan>, 0x0000013F9CA60220>]


Exemple 1

value dans joueur <case.Case object at Andre>
voison [<case.Case object at 0x0000013F9CA55A60>, <case.Case object at 0x0000013F9CA559A0>,

value dans joueur <case.Case object at Sophie>
voison 

value dans joueur <case.Case object at Julie>
voison [0x0000013F9CA55CA0>, <0x0000013F9CA55A60>, 

value dans joueur <case.Case object at Tristan>
voison 

value dans joueur <Mathis>
voison <0x0000013F9CA60220>]

value dans joueur <case.Case object at Louis>
voison [0x0000013F9CA600A0>,  0x0000013F9CA60220>]



value dans joueur <Julie>
voison [0x0000013F9CA55CA0>, <0x0000013F9CA55A60>, <0x0000013F9CA600A0>, <Tristan>]

(0,1) : "Andre"


"""
list = ["Patate", "Manon", "Sophie"]
voisin = ["Andre", "Chose", "Patate"]

liste_att = []

for name in list:
    if name in voisin:
        voisin.remove(name)
    if len(voisin) != 0:
        liste_att.append(list)
#print(len(voisin))

"""
Loop dict pour avoir case.object  ---> case.object de k
Verifier les voisins    case.voisins  ---> liste voisins
Verifier au moins 1 ennemi dans la liste voisins (verifier appartenance)
si oui, ajouter 



"""
#loop case.object
#case.object verifie voisins
#retirer les cases joueurs des cases voisins


