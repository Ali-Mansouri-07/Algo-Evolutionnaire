import random
import copy
import math

# --- PARAMÈTRES ET DONNÉES DU TSP (10 villes) ---

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

# --- FONCTIONS DE BASE ---

def calculer_distance_totale(solution, matrice_distances):
    """ Calcule la distance totale d'un chemin cyclique. """
    distance_totale = 0
    for i in range(len(solution) - 1):
        distance_totale += matrice_distances[solution[i]][solution[i+1]]
    distance_totale += matrice_distances[solution[-1]][solution[0]]
    return distance_totale

def calculer_fitness(distance):
    """ Fitness pour un problème de MINIMISATION: 1 / distance. """
    if distance == 0: return float('inf')
    return 1.0 / distance

def initialiser_population(taille_population, nombre_villes):
    """ Crée une population de permutations aléatoires. """
    population = []
    villes = list(range(nombre_villes))
    for _ in range(taille_population):
        chromosome = copy.deepcopy(villes)
        random.shuffle(chromosome)
        population.append(chromosome)
    return population

def pmx_crossover(parent1, parent2):
    """ Croisement à Cartographie Partielle (PMX) pour préserver les permutations. """
    size = len(parent1)
    enfant1, enfant2 = [0] * size, [0] * size

    point1 = random.randint(0, size - 2)
    point2 = random.randint(point1 + 1, size - 1)

    # Étape 1: Copier la section mappée directement
    enfant1[point1:point2] = parent2[point1:point2]
    enfant2[point1:point2] = parent1[point1:point2]

    mapping1 = {parent2[i]: parent1[i] for i in range(point1, point2)}
    mapping2 = {parent1[i]: parent2[i] for i in range(point1, point2)}

    def transfer_genes(parent, enfant, mapping):
        for i in range(size):
            if i < point1 or i >= point2:
                gene = parent[i]
                while gene in mapping:
                    gene = mapping[gene]
                enfant[i] = gene

    transfer_genes(parent1, enfant1, mapping1)
    transfer_genes(parent2, enfant2, mapping2)
    return enfant1, enfant2

def swap_mutation(chromosome, taux_mutation):
    """ Mutation par échange de deux villes. """
    mutated_chromosome = chromosome[:]
    if random.random() < taux_mutation:
        n = len(chromosome)
        i, j = random.sample(range(n), 2)
        mutated_chromosome[i], mutated_chromosome[j] = mutated_chromosome[j], mutated_chromosome[i]
    return mutated_chromosome
def roulette_selection(population_avec_fitness, nombre_parents):
    """ Sélection par Roulette. """
    solutions = [indiv[0] for indiv in population_avec_fitness]
    fitnesses = [indiv[1] for indiv in population_avec_fitness]
    somme_fitness = sum(fitnesses)
    
    if somme_fitness == 0:
        return random.sample(solutions, nombre_parents)

    probabilites = [f / somme_fitness for f in fitnesses]
    
    parents_selectionnes = random.choices(
        population=solutions,
        weights=probabilites,
        k=nombre_parents,
    )
    return parents_selectionnes

def genetic_algorithm_roulette(matrice_distances, taille_population, generations_max, taux_croisement, taux_mutation):
    """ Algorithme Génétique pour le TSP utilisant la Sélection par Roulette. """
    
    population = initialiser_population(taille_population, NOMBRE_VILLES)
    meilleure_solution_globale = None
    meilleure_distance_globale = float('inf')
    
    for generation in range(generations_max):
        # 1. Évaluation et enregistrement de l'élite
        population_avec_eval = []
        for chromosome in population:
            distance = calculer_distance_totale(chromosome, matrice_distances)
            fitness = calculer_fitness(distance)
            population_avec_eval.append((chromosome, fitness, distance))
            
            if distance < meilleure_distance_globale:
                meilleure_distance_globale = distance
                meilleure_solution_globale = chromosome[:]

        population_trie = sorted(population_avec_eval, key=lambda x: x[2])
        elite = population_trie[0][0] # Le meilleur individu
        
        # 2. Sélection
        parents = roulette_selection(population_avec_eval, taille_population)
        
        # 3. Création de la nouvelle population (avec élitisme)
        nouvelle_population = [elite]
        
        while len(nouvelle_population) < taille_population:
            parent1, parent2 = random.sample(parents, 2)
            
            # Croisement et Mutation
            if random.random() < taux_croisement:
                enfant1, enfant2 = pmx_crossover(parent1, parent2)
            else:
                enfant1, enfant2 = parent1[:], parent2[:]
            
            enfant1 = swap_mutation(enfant1, taux_mutation)
            enfant2 = swap_mutation(enfant2, taux_mutation)
            
            nouvelle_population.append(enfant1)
            if len(nouvelle_population) < taille_population:
                nouvelle_population.append(enfant2)
        
        population = nouvelle_population[:taille_population]
        
        # print(f"Roulette - Génération {generation+1}: Distance min = {meilleure_distance_globale}")

    return meilleure_solution_globale, meilleure_distance_globale

# --- EXÉCUTION DU CODE AVEC SÉLECTION PAR ROULETTE ---
print("--- Algorithme Génétique (Sélection par Roulette) ---")
solution_roulette, distance_roulette = genetic_algorithm_roulette(
    matrice_distances, 
    taille_population=100, 
    generations_max=500, 
    taux_croisement=0.85, 
    taux_mutation=0.05
)

print(f"Meilleur chemin (Roulette): {solution_roulette}")
print(f"Distance minimale (Roulette): {distance_roulette}")