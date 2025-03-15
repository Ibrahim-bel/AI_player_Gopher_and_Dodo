import Utilitaires.hexMap as HexMap
import Utilitaires.utils as utils
from Utilitaires.utils import State,Player,ActionGopher,EMPTY,R,B 

### GOPHER ###

def switchPlayer(currentPlayer: Player) -> Player:
    if currentPlayer == R:
        return B
    else:
        return R

def mapEmpty(hexMap: State) -> bool:
    for coord in hexMap: 
        if hexMap[coord] is not EMPTY:
            return False
    return True 
            

def isLegal(joueur: int, coord, hexMap: State) -> bool:
    player = R if joueur == R else B
    adversaire = B if joueur == R else R
    placementJoueur = 0
    placementAdversaire = 0
    if coord in hexMap:
        case = hexMap[coord]
        if mapEmpty(hexMap):
            return 1
        else:
            neighbors = HexMap.getCellNeighbor(coord)
            for neighbor in neighbors:
                if neighbor in hexMap:
                    case = hexMap[neighbor]
                    if case == adversaire:
                        placementAdversaire += 1
                    elif case == player:
                        placementJoueur += 1
            if placementJoueur == 0 and placementAdversaire == 1:
                return 1
            else:
                return 0
    else:
        return 0



def getLegals(player: int ,hexMap : State) -> list[ActionGopher]:
    legals = []
    empty = True
    
    for coord in hexMap: 
        if hexMap[coord] is EMPTY: 
            if isLegal(player, coord, hexMap):  
                legals.append(coord)
        else:
            empty = False
    if empty:
        legals = [coord for coord in hexMap.keys()]
    return legals

def updateGrid(joueur: int, action, hexMap: State) -> bool:
    coord = action
    if (coord) in hexMap:
        hex = hexMap[coord]
        if hex is None:
            if isLegal(joueur, coord, hexMap):
                hexMap[coord] = R if joueur == R else B      
                
                print(f"Le joueur {joueur} a joué à l'endroit {coord}")
     
                return 1
            else:
                print("Coup illegal")
                return 0
        else:
            print("Case deja  occupee !")
            return 0
    else:
        print("CoordonnÃ©es invalides !")
        return 0
    

def Final(hexMap: State, player: Player) -> bool:
    empty = True    
    for coord in hexMap: 
        if hexMap[coord] is EMPTY: 
            if isLegal(player, coord, hexMap):  
                return False  # Au moins un coup légal est possible, la partie n'est pas terminée
        else:
            empty = False
    if empty:
        return False
    return True  # Aucun coup légal possible pour chaque joueur, partie terminée

def countLegalMoves(hexMap: State, player: Player) -> int:
    legalMoves = 0
    for coord, value in hexMap.items():
        x, y = coord
        if value is EMPTY and isLegal(player, coord, hexMap):
            legalMoves += 1
    return legalMoves


def evaluateNodeBasic(hexMap: State) -> int:
    legalMovesPlayer1 = countLegalMoves(hexMap, 1)
    legalMovesPlayer2 = countLegalMoves(hexMap, 2)
    return legalMovesPlayer1 - legalMovesPlayer2


def evaluateNode(hexMap: State, player: Player) -> int:
    otherPlayer: Player = B if player == R else R
    value = 0

    playerLegals = getLegals(player, hexMap)
    otherPlayerLegals = getLegals(otherPlayer, hexMap)

    # Si le joueur actuel n'a pas de coups légaux, il perd
    if not playerLegals:
        return -1000  # Valeur très basse pour une perte certaine

    # Si l'adversaire n'a pas de coups légaux, le joueur actuel gagne
    if not otherPlayerLegals:
        return 1000  # Valeur très élevée pour une victoire certaine

    # Calculer la valeur de l'état actuel
    value = len(playerLegals) - len(otherPlayerLegals)

    # Ajouter des poids supplémentaires pour les coups potentiels
    for action in playerLegals:
        childMap = dict(hexMap)
        childMap[action] = player
        newLegals = getLegals(otherPlayer, childMap)
        if not newLegals:
            value += 50  # Bonus si un coup peut potentiellement gagner

    for action in otherPlayerLegals:
        childMap = dict(hexMap)
        childMap[action] = otherPlayer
        new_legals = getLegals(player, childMap)
        if not new_legals:
            value -= 50  # Malus si un coup peut potentiellement perdre

    # Ajouter des pondérations pour la position sur le plateau (centre plus précieux)
    center_bonus = 10
    for action in playerLegals:
        if action == (0, 0):
            value += center_bonus
        elif abs(action[0]) <= 1 and abs(action[1]) <= 1:
            value += center_bonus // 2

    for action in otherPlayerLegals:
        if action == (0, 0):
            value -= center_bonus
        elif abs(action[0]) <= 1 and abs(action[1]) <= 1:
            value -= center_bonus // 2
            
    value += countConnections(hexMap, player) * 2
    value -= countConnections(hexMap, otherPlayer) * 2

    return value

# Ajouter des pondérations pour les connexions potentielles
def countConnections(hexMap: State, player: Player) -> int:
    connections = 0
    for coord, val in hexMap.items():
        if val == player:
            neighbors = HexMap.getCellNeighbor(coord)
            for cell in neighbors:
                if cell in hexMap and hexMap[cell] == EMPTY:
                    connections += 1
    return connections

