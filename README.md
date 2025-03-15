# Projet DODO & GOPHER - Minimax AI Implementation

## 📌 **Description**
Ce projet implémente une intelligence artificielle basée sur **l'algorithme Minimax** avec mémoïsation pour jouer aux jeux **DODO** et **GOPHER**, deux jeux de stratégie à deux joueurs conçus par **Mark Steere**.

## 🎮 **Présentation des jeux**
### **DODO**
- Se joue sur une **grille hexagonale**.
- Deux joueurs : **Rouge** et **Bleu**.
- Chaque joueur déplace un pion à tour de rôle vers l'avant (directement ou en diagonale).
- **Objectif** : Le joueur qui ne peut plus bouger au début de son tour **perd** la partie.

📜 Voir [`Dodo_rules.pdf`](Dodo_rules.pdf) pour les règles complètes.

### **GOPHER**
- Se joue sur une **grille hexagonale de taille 6 ou 8**.
- Deux joueurs : **Rouge** et **Bleu**.
- Les joueurs placent des pierres sur la grille selon des règles spécifiques.
- **Objectif** : Le dernier joueur à placer une pierre gagne la partie.

📜 Voir [`Gopher_hex_rules.pdf`](Gopher_hex_rules.pdf) pour les règles complètes.

## 🤖 **Stratégie d'Intelligence Artificielle**
Le projet utilise l'algorithme **Minimax avec mémoïsation** pour évaluer les coups possibles et maximiser les chances de victoire.

### **DODO - Approches d'évaluation**
Deux fonctions d'évaluation ont été développées pour estimer l'état du jeu et aider à la prise de décision dans l'algorithme Minimax :

1️⃣ **evaluateNodeBasic** (Rapide et efficace) :
   - Calcule la différence entre le nombre de mouvements légaux disponibles pour chaque joueur.
   - Se base uniquement sur le nombre de coups possibles sans prise en compte des positions stratégiques.
   - ✅ Très rapide et optimisée pour les appels récursifs de Minimax.
   - ❌ Ne considère pas les blocages ni l'avancement stratégique des pions.

2️⃣ **evaluateNode** (Approche avancée) :
   - Analyse l'état du jeu de manière plus détaillée :
     - Prend en compte l'avancement des pions sur la grille.
     - Détecte les blocages potentiels.
     - Évalue la flexibilité des mouvements restants.
   - ✅ Fournit une évaluation plus précise du positionnement stratégique.
   - ❌ Plus coûteuse en calcul, ce qui peut ralentir Minimax dans les recherches profondes.

### **Choix stratégique**
Pour la stratégie Minimax avec mémoïsation, **evaluateNodeBasic** a été privilégiée en raison de sa rapidité d'exécution et de son taux de victoire élevé (90%+ contre un adversaire aléatoire, avec +3 victoires en tournoi). Bien que **evaluateNode** fournisse une meilleure analyse, son coût computationnel est trop élevé pour une exploration exhaustive de la grille. **evaluateNodeBasic** permet d'assurer des performances optimales, notamment pour une grille de **taille 4** avec une profondeur de Minimax de **3, 4 et 5**, rendant l'algorithme efficace pour un jeu en temps réel.



## 🛠 **Fonctionnalités**
✅ Implémentation de **Minimax avec mémoïsation**.
✅ Sélection dynamique de la **profondeur de recherche**.
✅ Interface CLI pour observer le déroulement des parties.
✅ Optimisé pour une grille de taille réduite pour un jeu rapide.

## 🚀 **Améliorations possibles**
- Intégrer **Alpha-Beta Pruning** pour améliorer l'efficacité du Minimax.
- Tester l'utilisation de **evaluateNode** avec une meilleure gestion du temps de calcul.
- Ajouter une **interface graphique** pour rendre les jeux plus interactifs.

## 📜 **Références**
- [Règles du jeu DODO](Dodo_rules.pdf)
- [Règles du jeu GOPHER](Gopher_hex_rules.pdf)
- [Article sur l'algorithme Minimax](https://en.wikipedia.org/wiki/Minimax)

🎲 **Prêt à défier l'IA ?** Amusez-vous bien ! 🚀
