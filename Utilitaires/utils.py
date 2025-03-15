import Utilitaires.hexMap as HexMap
from typing import Dict, Any



# Types de base utilisés par l'arbitre
Environment = Dict[str, Any] # Ensemble des données utiles (cache, état de jeu...) pour
                  # que votre IA puisse jouer (objet, dictionnaire, autre...)
Cell = tuple[int, int]
ActionGopher = Cell
ActionDodo = tuple[Cell, Cell] # case de départ -> case d'arrivée
#Action = Union[ActionGopher, ActionDodo]
Player = int # 1 ou 2
State = HexMap.HexMap # État du jeu pour la boucle de jeu
Score = int
Time = int
Action = Any

EMPTY = 0
R = 1
B = 2

