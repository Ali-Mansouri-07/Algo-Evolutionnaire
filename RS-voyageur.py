import random
import math
import copy

# --- Fonctions de Base (Reprise du code AG/Tabou) ---

# Matrice de Distances (pour 10 villes)
matrice_distances = [
    [0, 2, 7, 15, 2, 5, 7, 6, 5, 5],
    [2, 0, 10, 4, 7, 3, 7, 15, 8, 2],
    [7, 10, 0, 1, 4, 3, 3, 4, 2, 3],
    [7, 4, 1, 0, 2, 15, 7, 7, 5, 4],
    [7, 10, 4, 2, 0, 7, 3, 2, 2, 7],
    [2, 3, 3, 7, 7, 0, 1, 7, 2, 10],
    [5, 7, 3, 7, 3, 1, 0, 2, 1, 3],
    [7, 7, 4, 7, 2, 7, 2, 0, 1, 10],
    [6, 8, 2, 5, 2, 2, 1, 1, 0, 15],
    [5, 2, 3, 4, 7, 10, 3, 10, 15, 0]
]
NOMBRE_VILLES = len(matrice_distances)

def calculer_distance_totale(solution, matrice_distances):
    """ Calcule la distance totale d'un chemin cyclique. """
    distance_totale = 0
    for i in range(len(solution) - 1):
        distance_totale += matrice_distances[solution[i]][solution[i+1]]
    distance_totale += matrice_distances[solution[-1]][solution[0]]
    return distance_totale

def generer_un_voisin_aleatoire(solution):
    """ Génère un seul voisin par échange de deux villes aléatoires (Swap Mutation). """
    n = len(solution)
    i, j = random.sample(range(n), 2) 
    
    voisin = solution[:]
    voisin[i], voisin[j] = voisin[j], voisin[i]
    return voisin

# --- Algorithme de Recuit Simulé ---

def recuit_simule(matrice_distances, temperature_initiale, facteur_refroidissement, iterations_max):
    """
    Implémentation de l'algorithme de Recuit Simulé pour le TSP.
    """
    nombre_villes = len(matrice_distances)
    
    # Initialisation de la solution initiale (chemin aléatoire)
    solution_actuelle = list(range(nombre_villes))
    random.shuffle(solution_actuelle)
    
    meilleure_solution = solution_actuelle[:]
    meilleure_distance = calculer_distance_totale(solution_actuelle, matrice_distances)
    
    T = temperature_initiale # Température actuelle
    
    for i in range(iterations_max):
        # 1. Refroidissement (Calendrier Géométrique)
        T *= facteur_refroidissement
        
        if T < 0.0001: # Condition d'arrêt
            break

        # 2. Générer un voisin
        nouveau_voisin = generer_un_voisin_aleatoire(solution_actuelle)
        
        distance_actuelle = calculer_distance_totale(solution_actuelle, matrice_distances)
        distance_voisin = calculer_distance_totale(nouveau_voisin, matrice_distances)
        
        delta_E = distance_voisin - distance_actuelle # Changement de coût/énergie
        
        # 3. Critère d'Acceptation
        if delta_E < 0:
            # Le voisin est meilleur, on l'accepte toujours (mouvement d'exploitation)
            solution_actuelle = nouveau_voisin
            
            # Mise à jour de la meilleure solution globale
            if distance_voisin < meilleure_distance:
                meilleure_solution = nouveau_voisin[:]
                meilleure_distance = distance_voisin
                
        else:
            # Le voisin est pire (delta_E > 0), on l'accepte avec une probabilité
            # Probabilité de Metropolis: P = e^(-Delta_E / T)
            probabilite_acceptation = math.exp(-delta_E / T)
            
            if random.random() < probabilite_acceptation:
                solution_actuelle = nouveau_voisin
                
    return meilleure_solution, meilleure_distance

# --- EXÉCUTION DU RECUIT SIMULÉ ---
TEMPERATURE_INIT = 100.0
FACTEUR_REFROID = 0.999
ITERATIONS_MAX = 50000 

solution_sa, distance_sa = recuit_simule(matrice_distances, TEMPERATURE_INIT, FACTEUR_REFROID, ITERATIONS_MAX)

print(NOMBRE_VILLES)

print("--- Résultat du Recuit Simulé (SA) ---")
print(f"Meilleur chemin SA: {solution_sa}")
print(f"Distance minimale SA: {distance_sa}")