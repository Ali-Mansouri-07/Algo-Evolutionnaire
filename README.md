# Algo-Evolutionnaire
# 🌍 Optimisation du Problème du Voyageur de Commerce (TSP)

Ce dépôt contient trois implémentations en Python de métaheuristiques classiques pour résoudre le Problème du Voyageur de Commerce (TSP) : le **Recuit Simulé (RC)**, l'**Algorithme Génétique avec Sélection par Roulette (AG-Roulette)** et l'**Algorithme Génétique avec Sélection par Rang (AG-Rang)**.

## 📁 Structure du Projet

Le dépôt est organisé autour des fichiers Python qui contiennent les algorithmes d'optimisation :

| Fichier Python | Algorithme | Type | Description |
| :--- | :--- | :--- | :--- |
| `RS-voyageur.py` | Recuit Simulé (SA / RC) | Recherche Locale | Utilise le critère de Metropolis pour accepter des mouvements défavorables et échapper aux optima locaux. |
| `roulette-VC.py` | Algorithme Génétique | Populationnel | Utilise le croisement PMX et la mutation par échange. La sélection se fait par la méthode de la **Roue de Roulette**. |
| `rang-VC.py` | Algorithme Génétique | Populationnel | Utilise le croisement PMX et la mutation par échange. La sélection se fait par la méthode du **Rang**. |

## ⚙️ Dépendances

Ce projet ne nécessite que les bibliothèques Python standards :

* **Python 3.x**
* **`random`**
* **`math`**
* **`copy`**

## 🎯 Le Problème du Voyageur de Commerce (TSP)

Le TSP est un problème d'optimisation combinatoire où un vendeur doit trouver le chemin le plus court possible en visitant une liste donnée de villes exactement une fois et en revenant à la ville de départ.

### Représentation du Problème

* **Solution/Chromosome :** Une permutation ordonnée des indices des villes (ex: `[0, 4, 2, 1, 3]`).
* **Fitness/Coût :** La distance totale parcourue pour ce chemin.

## 🚀 Mise en œuvre des Algorithmes

Tous les algorithmes utilisent la même **matrice de distances symétrique $10 \times 10$** définie dans chaque fichier Python.

### 1. Recuit Simulé (`RS-voyageur.py`) 🔥

Le RC explore l'espace de recherche en acceptant des solutions moins bonnes avec une probabilité décroissante basée sur une **température $T$** (analogie au refroidissement des métaux).

* **Opérateur de Mouvement :** **Swap Mutation** (échange de deux villes).
* **Paramètres Clés :** `temperature_initiale`, `facteur_refroidissement` (taux de diminution de $T$).

### 2. Algorithme Génétique (AG) 🧬

Les deux versions de l'AG partagent les opérateurs spécifiques au problème de permutation du TSP :

* **Croisement :** **PMX (Partially Mapped Crossover)**, indispensable pour générer des descendants valides (sans villes dupliquées).
* **Mutation :** **Swap Mutation** (échange de deux villes).
* **Évaluation :** La **fitness** est calculée comme l'inverse de la distance ($\frac{1}{\text{Distance}}$).

#### A. Sélection par Roulette (`roulette-VC.py`) 🎡

La probabilité d'être choisi est **directement proportionnelle à la fitness** de l'individu. Les individus très performants (haute fitness) ont une chance beaucoup plus élevée de reproduction.

#### B. Sélection par Rang (`rang-VC.py`) 🏅

Les individus sont triés par distance (fitness). La probabilité de sélection est basée sur leur **rang** dans le classement (le meilleur rang reçoit la plus haute probabilité). Cette méthode réduit l'impact des "super-individus" et maintient une meilleure **diversité** génétique en évitant la convergence prématurée.

## 🛠️ Comment Exécuter

Pour exécuter un algorithme, ouvrez votre terminal, naviguez vers le répertoire contenant les fichiers et exécutez le script souhaité :

```bash
# Exécution du Recuit Simulé
python RS-voyageur.py

# Exécution de l'AG (Sélection par Roulette)
python roulette-VC.py

# Exécution de l'AG (Sélection par Rang)
python rang-VC.py
