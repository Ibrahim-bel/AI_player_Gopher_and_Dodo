from typing import Callable
import Utilitaires.utils as Utils
import Utilitaires.hexMap as HexMap
import Utilitaires.symetrie as Symetrie
from Utilitaires.utils import Environment,Action, State,Player,Time

def memoizeAlphaBeta(f: Callable[[State,Player,int,int,int,bool], tuple[float, Action]])  -> Callable[[State,Player,int], tuple[float, Action]]:
    cache = {}  # closure
    def g(utils,hexMap: State,player, α: float, β: float, depth: int, maximizingPlayer: bool) -> tuple[float, Action]:
        
        for transformation in Symetrie.transformations:
            transformedGrid = Symetrie.applyTransformation(hexMap,transformation)
            transformedKey = (tuple(transformedGrid.items()))

            if transformedKey in cache:
                score, cached_action = cache[transformedKey]
                if cached_action is None:
                    return score,None
                
                # Appliquer la transformation inverse à l'action pour obtenir le bon coup
                inverse_transform = Symetrie.inverseTransformation(transformation)
                correct_action = inverse_transform(cached_action.q,cached_action.r)
                return score, correct_action
        
        key = (tuple(hexMap.items()))
        Score,Action  = f(utils,hexMap,player,α, β,depth,maximizingPlayer)
        cache[key] = (Score, Action)
        return Score,Action
    return g

@memoizeAlphaBeta
def alphabeta(utils,hexMap: State,player, α: int, β: int, depth: int, maximizingPlayer: bool) -> tuple[int, Action]:
    if depth == 0 or utils.Final(hexMap,player):
        return utils.evaluateNode(hexMap,player), None
    
    if maximizingPlayer:
        bestValue = float('-inf')
        bestAction = None
        actions = utils.getLegals(player,hexMap)
        for action in actions:
            childMap = dict(hexMap)
            utils.updateGrid(player,action,childMap)
            nextPlayer = utils.switchPlayer(player)
            childScore,_ = alphabeta(utils,childMap,nextPlayer, α, β, depth - 1, False)
            if(childScore > bestValue):
                bestValue = childScore
                bestAction = action
            α = max(α, bestValue)
            if α >= β:
                break  # β cut-off
        return bestValue,bestAction
    else:
        bestValue = float('inf')
        bestAction = None
        actions = utils.getLegals(player,hexMap)
        for action in actions:
            childMap = dict(hexMap)
            utils.updateGrid(player,action,childMap)
            nextPlayer = utils.switchPlayer(player)
            childScore,_ = alphabeta(utils,childMap,nextPlayer, α, β, depth - 1, True)
            if(childScore < bestValue):
                bestValue = childScore
                bestAction = action
            β = min(β, bestValue)
            if α >= β:
                break  # α cut-off
        return bestValue,bestAction

def strategyAlphaBeta(env: Environment,hexMap: State, player: Player,timeLeft: Time) -> tuple[Environment, Action]:
    hexMap = HexMap.convertStatetoDict(hexMap)
    utils = env["UtilsGame"]
    _, action = alphabeta(utils,hexMap, player,float('-inf'),float('inf'),3,True)
    return env,action