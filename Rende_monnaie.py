
import tracemalloc
import time
# --------------------------------------------------------------------------
# Partie 1 : Algorithme Gluton

def gloutton(S:list[int],M:int):
    T = {}
    m = M

    for valeur in S:
        d = m//valeur

        T[valeur] = d
        m %= valeur
        
    if sum(map(lambda x,y:x*y, S,T)) == M:
        return T
    else:
        return None

def gloutton_pieces(S:dict[int,int],M:int):
    T = {}
    m = M
    for valeur,nombre in reversed(S.items()):
        d = m//valeur

        if d>nombre: #Nombre limité de monnaies
            d = nombre

        T[valeur] = d
        m %= valeur
        
    if sum(map(lambda e: e[0]*e[1],T.items()))==M:
        return T
    else:
        return None

def gloutton_poids(S:dict[int,int],M:int):
    T = {value : 0 for value in S}
    L = [(poids/valeur, valeur, poids) for valeur,poids in S.items()]
    L.sort(key = lambda l:l[0]) #trie par le premier élément de la tuple
    m = M

    for _,s,_ in L:
        if s<=m:
            T[s] = (m//s)
            m %= s

    if sum(map(lambda e: e[0]*e[1],T.items()))==M:
        return T
    else:
        return None

# --------------------------------------------------------------------------
# Partie 2 : Graphe

def descendre_niveau(etage_graphe: dict[int, list[int]], S: list[int]):

    new_level = {}
    for argent ,list_monaies in etage_graphe.items():
        for indice ,valeur_monaie in enumerate(S):
            ag = argent
            l_m = list_monaies.copy()

            l_m[indice] += 1
            ag -= valeur_monaie

            if ag>=0:
                new_level[ag] = l_m
    
    return new_level
    

def monnaie_graphe(S: list[int] , M: int):
    graphe = {M : [0 for _ in S] } # exemple {28 : [0,0,0]}

    while 0 not in graphe.keys() and len(graphe)>0 :
        graphe = descendre_niveau(graphe,S)

    if len(graphe)>0:
        return dict(zip(S,graphe[0]))
    else:
        return None

# --------------------------------------------------------------------------
# Partie 3 : Programmation Dynamique

from math import inf
from re import S

def matrice_monnaie(S : list, M: int) ->list[list[int]]:
    S_copy = [0] + S.copy()
    matrice = []
    for i, v in enumerate(S_copy):
        ligne = []
        for m in range(M+1):
            if m ==0:
                ligne.append(0)
            elif i ==0:
                ligne.append(inf)
            else:
                if m - v >=0:

                    e1 = 1 + ligne[m - v]
                else:
                    e1 = inf
                
                if i>=1:
                    e2 = matrice[i-1][m]
                else:
                    e2 = inf
                ligne.append(min(e1,e2))
        matrice.append(ligne)
    
    return matrice

def matrice_poids(S : dict[int,float], M: int) ->list[list[float]]: # S = {valeur de la pièce : poids d'une pièce}
    S_copy = S.copy()
    S_copy[0] = 0

    matrice = []
    i = 0 # indice de la ligne de la matrice
    for valeur,poids in S_copy.items():

        ligne = []
        for m in range(M+1):
            if m ==0:
                ligne.append(0)
            elif valeur == 0:
                ligne.append(inf)
            else:
                if m - valeur >=0:
                    e1 = poids + ligne[m - valeur] # somme le poids de la pièce au total
                else:
                    e1 = inf
                

                if i>=1:
                    e2 = matrice[i-1][m]
                else:
                    e2 = inf
                ligne.append(min(e1,e2))
        i+=1 #mise a jour de l'indice

        matrice.append(ligne)
    matrice = [matrice[-1]] + matrice[:-1]

    return matrice

def monnaie_table(S: list[int] , M: int):
    matrice = matrice_monnaie(S,M)
    T = {value : 0 for value in S}
    
    i = len(S)
    j = M
    if matrice[-1][-1] == inf:
        return None
    else:
        while matrice[i][j] > 0:
            valeur = S[i-1]
            if matrice[i][j] == matrice[i-1][j]:
                i-=1
            else:
                j -= valeur
                T[ valeur ] += 1
        return T
        
def monnaie_pieces_limitees(S : dict[int,int],M : int): # S = {valeur de la pièce : nombre de pièces dispos}
    matrice = matrice_monnaie(list(S.keys()),M)
    T = {value : 0 for value in S}
    
    i = len(S)
    j = M
    if matrice[-1][-1] == inf:
        return None
    else:
        while matrice[i][j] > 0:
            valeur = list(S.keys())[i-1]
            if matrice[i][j] == matrice[i-1][j] or T[valeur] == S[valeur]: #depasser le stock
                i-=1
            else:
                j -= valeur
                T[ valeur ] += 1
        return T

def monnaie_poids(S : dict[int,int],M : int): # S = {valeur de la pièce : nobre de pièces dispos}
    matrice = matrice_poids(S,M)
    T = {value : 0 for value in S}
    
    i = len(S)
    j = M
    if matrice[-1][-1] == inf:
        return None
    else:
        while matrice[i][j] > 0:
            valeur = list(S.keys())[i-1]
            if matrice[i][j] == matrice[i-1][j]:
                i-=1
            else:
                j -= valeur
                T[ valeur ] += 1
        return T

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
#Questions

#S={4:2, 6:2, 9:20, 20:10} # The 43 Chicken McNuggets' Problem (exemple)
Sm={1:10 ,7:10 ,23:10} #{valeur de la monnaie : nombre de monnaies dispos}
M=43 #somme de monnaie à rendre

print("Résolution pour donner M=", M, "Avec les pièces disponibles ")
#tracemalloc.start()    #Fonction que vérifie la mémoire utilisée 
print("Gloutone:", gloutton_pieces(Sm, M))
#current, peak = tracemalloc.get_traced_memory()
#print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
#tracemalloc.stop()
# --------------------------------------------------------------------------
#tracemalloc.start()    #Fonction que vérifie la mémoire utilisée
print("Graphe:", monnaie_graphe(Sm, M))
#current, peak = tracemalloc.get_traced_memory()
#print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
#tracemalloc.stop()
# --------------------------------------------------------------------------
#tracemalloc.start()    #Fonction que vérifie la mémoire utilisée
#t0=time.time()       # Mesurer les temps d'éxecution
print("Programmation Dynamique:", monnaie_pieces_limitees(Sm, M))
#current, peak = tracemalloc.get_traced_memory()
#tg = time.time()-t0
#print("temps d'execution:", tg)
#print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
#tracemalloc.stop()

# --------------------------------------------------------------------------
#Sp={1:2.3 , 2:3.06 , 5:3.92 , 10:4.1 , 20:5.74 , 50:7.8 , 100:7.5, 200:8.5, 500:0.6, 1000:0.7, 2000:0.8, 5000:0.9, 10000:1} # {valeur de la pièce : poids d'une pièce} #Table 2
#M2=350 #somme monnaie

Sp={1:10 , 3:27 , 4:32 , 7:55} #Table 3
M2 = 20 #somme monnaie

print("Résolution en minimisant le poids avec la table 3 et M=", M2)
print("Poids:", monnaie_poids(Sp, M2))
print("Poids_gloutone:", gloutton_poids(Sp, M2))
