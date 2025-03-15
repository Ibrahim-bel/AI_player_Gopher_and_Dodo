import Utilitaires.utils as utils
from Utilitaires.utils import State,Player,ActionDodo,EMPTY,R,B 
### DODO ###

def switchPlayer(currentPlayer: Player) -> Player:
    if currentPlayer == R:
        return B
    else:
        return R


def remplir_grid(n: int, move_played: State) -> State:
    taille = 2 * n - 1
    lim_ligne = taille // 2
    lim_colone = taille // 2
    null_index = 0
    grid: dict = {}
    for i in range(lim_colone, -(lim_colone + 1), -1):
        for j in range(-lim_ligne, lim_ligne + 1):
            if ((j >= null_index) and (null_index <= 0)) or (((j < null_index) and (null_index > 0))):
                if ((j, i), R) in move_played:
                    grid[(j, i)] = R
                elif ((j, i), B) in move_played:
                    grid[(j, i)] = B
                else:
                    grid[(j, i)] = EMPTY
        null_index -= 1
        if null_index < -lim_ligne:  # Passage aux positifs
            null_index = lim_ligne
    return grid

def remplir_rouge(grille: State, x: int, y: int, taille: int):
    if taille == 0:
        return
    if (x, y) in grille:
        grille[(x, y)] = R  # Place un pion rouge à la position actuelle

    if (x + 1, y) in grille:
        remplir_rouge(grille, x + 1, y, taille - 1)
    if (x, y + 1) in grille:
        remplir_rouge(grille, x, y + 1, taille - 1)
    if (x + 1, y + 1) in grille:
        remplir_rouge(grille, x + 1, y - 1, taille - 1)

def remplir_bleu(grille: State, x: int, y: int, taille: int):
    if taille == 0:
        return
    if (x, y) in grille:
        grille[(x, y)] = B  # Place un pion bleu à la position actuelle

    if (x - 1, y) in grille:
        remplir_bleu(grille, x - 1, y, taille - 1)
    if (x, y - 1) in grille:
        remplir_bleu(grille, x, y - 1, taille - 1)
    if (x - 1, y + 1) in grille:
        remplir_bleu(grille, x - 1, y + 1, taille - 1)

def annuler_coup(coup: ActionDodo, grille: State):
    cell_depart, cell_arrive = coup
    grille[cell_depart] = grille[cell_arrive]
    grille[cell_arrive] = EMPTY
    
def isLegal(coup: ActionDodo, player: Player, grille: State) -> bool:
    cell_depart, cell_arrive = coup

    if player == R:
        if grille.get(cell_depart) == R and grille.get(cell_arrive) == EMPTY:
            if (cell_arrive[0] == cell_depart[0] and cell_arrive[1] == cell_depart[1] + 1) or \
                    (cell_arrive[0] == cell_depart[0] + 1 and cell_arrive[1] == cell_depart[1]) or \
                    (cell_arrive[0] == cell_depart[0] + 1 and cell_arrive[1] == cell_depart[1] + 1):
                return True
            return False

    elif player == B:
        if grille.get(cell_depart) == B and grille.get(cell_arrive) == EMPTY:
            if (cell_arrive[0] == cell_depart[0] and cell_arrive[1] == cell_depart[1] - 1) or \
                    (cell_arrive[0] == cell_depart[0] - 1 and cell_arrive[1] == cell_depart[1]) or \
                    (cell_arrive[0] == cell_depart[0] - 1 and cell_arrive[1] == cell_depart[1] - 1):
                return True
            return False

    return False

def Final(grille: State, player: Player) -> bool:
    if not isinstance(grille, dict):
        raise ValueError("La grille doit être un dictionnaire.")
    for cle, valeur in grille.items():
        if valeur == player:
            x, y = cle
            if player == R:
                if isLegal(((x, y), (x + 1, y + 1)), player, grille):
                    return False
                if isLegal(((x, y), (x, y + 1)), player, grille):
                    return False
                if isLegal(((x, y), (x + 1, y)), player, grille):
                    return False
            elif player == B:
                if isLegal(((x, y), (x - 1, y - 1)), player, grille):
                    return False
                if isLegal(((x, y), (x, y - 1)), player, grille):
                    return False
                if isLegal(((x, y), (x - 1, y)), player, grille):
                    return False
    return True
from typing import List

def getLegals(player: Player, grille: State) -> List[ActionDodo]:
    possible_moves = []
    
    for cell_depart, occupant in grille.items():
        if occupant == player:
            x, y = cell_depart

            # Vérifier les mouvements pour le joueur Rouge
            if player == R:
                # Mouvement vers le haut
                if isLegal(((x, y), (x, y + 1)), player, grille):
                    possible_moves.append(((x, y), (x, y + 1)))
                # Mouvement diagonal haut-droit
                if isLegal(((x, y), (x + 1, y)), player, grille):
                    possible_moves.append(((x, y), (x + 1, y)))
                # Mouvement diagonal haut-gauche
                if isLegal(((x, y), (x + 1, y + 1)), player, grille):
                    possible_moves.append(((x, y), (x + 1, y + 1)))

            # Vérifier les mouvements pour le joueur Bleu
            elif player == B:
                # Mouvement vers le bas
                if isLegal(((x, y), (x, y - 1)), player, grille):
                    possible_moves.append(((x, y), (x, y - 1)))
                # Mouvement diagonal bas-droit
                if isLegal(((x, y), (x - 1, y)), player, grille):
                    possible_moves.append(((x, y), (x - 1, y)))
                # Mouvement diagonal bas-gauche
                if isLegal(((x, y), (x - 1, y - 1)), player, grille):
                    possible_moves.append(((x, y), (x - 1, y - 1)))

    return possible_moves


def updateGrid(player: Player, Coup: ActionDodo, grille: State) -> bool:
    cell_depart, cell_arrive = Coup
    if isLegal(Coup, player, grille):
        grille[cell_arrive] = grille[cell_depart]
        grille[cell_depart] = EMPTY
        return True
    else:
        print("Coup illégal")
        return False
        
 
def countLegalMoves(grille: State, joueur: Player) -> int:
    return len(getLegals(joueur, grille))
 

def evaluateNodeBasic(grille: State) -> int:
    coups_legaux_joueur1 = countLegalMoves(grille, 1)
    coups_legaux_joueur2 = countLegalMoves(grille, 2)
    return coups_legaux_joueur1 - coups_legaux_joueur2



'''
def evaluateNode(grille: Grid) -> int:
    # Nombre de coups légaux pour chaque joueur
    coups_legaux_rouge = compter_coups_legaux(grille, R)
    coups_legaux_bleu = compter_coups_legaux(grille, B)

    # Avancement des pions
    avancement_rouge = sum(y for (x, y), joueur in grille.items() if joueur == R)
    avancement_bleu = sum(-y for (x, y), joueur in grille.items() if joueur == B)

    # Détection des blocages
    blocage_rouge = 0
    blocage_bleu = 0
    for move in get_possible_moves(R, grille):
        jouer_coup(R, move, grille)
        if not get_possible_moves(B, grille):
            blocage_rouge += 1
        annuler_coup(move, grille)
        
    for move in get_possible_moves(B, grille):
        jouer_coup(B, move, grille)
        if not get_possible_moves(R, grille):
            blocage_bleu += 1
        annuler_coup(move, grille)

    # Flexibilité de retard
    retard_rouge = coups_legaux_rouge - blocage_rouge
    retard_bleu = coups_legaux_bleu - blocage_bleu

    # Calcul final de l'évaluation
    evaluation = (
        2 * (coups_legaux_rouge - coups_legaux_bleu) +
        (avancement_rouge - avancement_bleu) +
        3 * (blocage_rouge - blocage_bleu) +
        (retard_rouge - retard_bleu)
    )
    
    return evaluation
'''
