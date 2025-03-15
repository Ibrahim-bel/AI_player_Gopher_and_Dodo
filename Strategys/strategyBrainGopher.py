import ast
import Utilitaires.hexMap as HexMap
from Utilitaires.utils import Environment,ActionGopher,State,Player,Time 

def strategyBrainGopher(env: Environment,hexMap: State, player: Player,timeLeft: Time) -> tuple[Environment, ActionGopher]:
    hexMap = HexMap.convertStatetoDict(hexMap)
    utils = env["UtilsGame"]
    while True:
        t =-1
        print("à vous de jouer  ",player,":", end="")
        actions = utils.getLegals(player,hexMap)
        print(actions)
        s = input()
        print()
        t = ast.literal_eval(s)
        if  0<= t and t <= len(actions)-1:
            return env,actions[t]
