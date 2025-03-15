from typing import Callable
import Utilitaires.utils as Utils
import Utilitaires.hexMap as HexMap
import Strategys.strategyRandom as strategyRandom
from Utilitaires.utils import Environment,Action, State,Player,Time 
import copy

def memoizeMinMax(f: Callable[[State,Player,int,bool], tuple[float, Action]])  -> Callable[[State,Player,int], tuple[float, Action]]:
    cache = {}  # closure
    def g(utils,hexMap: State, player: Player, depth: int, maximizingPlayer:bool) -> tuple[int, Action]:
        
        key = (tuple(hexMap.items()))
        if key in cache:
            return cache[key]

        Score,Action  = f(utils,hexMap,player,depth,maximizingPlayer)
        cache[key] = (Score, Action)
        return Score,Action
    return g


@memoizeMinMax
def minmax(utils,hexMap: State,player: Player, depth: int, maximizingPlayer:bool) -> tuple[int, Action]:
    if depth == 0 or utils.Final(hexMap,player):
        return utils.evaluateNode(hexMap,player), None
    
    actions = utils.getLegals(player,hexMap)
    scoreAction = []
    
    if not actions:
        # Si aucune action n'est disponible, évaluer le nœud actuel
        return utils.evaluateNode(hexMap,player), None
    
    for action  in actions:
        childMap = copy.deepcopy(hexMap)
        utils.updateGrid(player,action,childMap)
        nextPlayer = utils.switchPlayer(player)
        
        nextScore,_ = minmax(utils,childMap,nextPlayer, depth - 1, not(maximizingPlayer))
        scoreAction.append((nextScore, action))
    if maximizingPlayer:
        maxScoreAction = max(scoreAction, key=lambda x: x[0])
        return maxScoreAction
    else:
        minScoreAction = min(scoreAction, key=lambda x: x[0])
        return minScoreAction
    

def strategyMinmax(env: Environment,hexMap: State, player: Player,timeLeft: Time) -> tuple[Environment, Action]:
    hexMap = HexMap.convertStatetoDict(hexMap)
    utils = env["UtilsGame"]
    _, action = minmax(utils,hexMap, player,3,True)
     
    env["currCoup"] = env["currCoup"] +1
    return env,action