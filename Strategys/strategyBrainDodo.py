from Utilitaires.utils import Environment,ActionDodo,State,Player,Time 
import Utilitaires.hexMap as HexMap

def strategyBrainDodo(env: Environment,grille: State, player: Player,timeLeft: Time) -> ActionDodo:
    grille = HexMap.convertStatetoDict(grille)
    utils = env["UtilsGame"]
    while True:
        cell_depart = tuple(map(int, input("Entrez les coordonnées de la cellule de départ (x y) : ").split()))
        cell_arrive = tuple(map(int, input("Entrez les coordonnées de la cellule d'arrivée (x y) : ").split()))
        coup = (cell_depart, cell_arrive)
        if utils.isLegal(coup, player, grille):
            return env,coup
        print("Action imposible !")
