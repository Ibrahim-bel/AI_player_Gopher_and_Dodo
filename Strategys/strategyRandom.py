import random
import Utilitaires.hexMap as HexMap
from Utilitaires.utils import Environment,State,Player,ActionGopher,Time


def strategyRandom(env: Environment,hexMap: State, player: Player,timeLeft: Time) -> tuple[Environment, ActionGopher]:
    hexMap = HexMap.convertStatetoDict(hexMap)
    utils = env["UtilsGame"]
    actions = utils.getLegals(player,hexMap)
    if not actions:
        raise ValueError("Aucun coup légal disponible")
    return env,random.choice(actions)