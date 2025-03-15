from Utilitaires.utils import State
from typing import Callable
import copy

def rotate60(q: int, r: int) -> tuple[int, int]:
    return q-r, q

def rotate120(q: int, r: int) -> tuple[int, int]:
    return -r, q-r

def rotate180(q: int, r: int) -> tuple[int, int]:
    return -q, -r

def rotate240(q: int, r: int) -> tuple[int, int]:
    return -q+r , -q

def rotate300(q: int, r: int) -> tuple[int, int]:
    return r, -q +r
   
   
   
def reflectY(q: int, r: int) -> tuple[int, int]:
    return r, q

def reflectX(q: int, r: int) -> tuple[int, int]:
    return -q, -r

def reflectPiSurTrois(q: int, r: int) -> tuple[int, int]:
    return q, q-r

def reflectPiSurSix(q: int, r: int) -> tuple[int, int]:
    return q-r, -r

def reflectDeuxPiSurTrois(q: int, r: int) -> tuple[int, int]:
    return r-q, r

def reflectCinqPiSurSix(q: int, r: int) -> tuple[int, int]:
    return -q, r-q

transformations = [
        rotate60, rotate120, rotate180, rotate240, rotate300,
        reflectY, reflectX, reflectPiSurTrois, reflectPiSurSix, reflectDeuxPiSurTrois, reflectCinqPiSurSix
]

def inverseTransformation(transform: Callable) -> Callable:
    if transform == rotate60:
        return rotate300
    elif transform == rotate120:
        return rotate240
    elif transform == rotate180:
        return rotate180
    elif transform == rotate180:
        return rotate120
    elif transform == rotate240:
         return rotate120
    elif transform == rotate300:
        return rotate60
    elif transform == reflectY:
        return reflectY
    elif transform == reflectX:
        return reflectX
    elif transform == reflectPiSurTrois:
        return reflectPiSurTrois
    elif transform == reflectPiSurSix:
        return reflectPiSurSix
    elif transform == reflectDeuxPiSurTrois:
        return reflectDeuxPiSurTrois
    elif transform == reflectCinqPiSurSix:
        return reflectCinqPiSurSix
    raise ValueError("Transformation not recognized.")

def applyTransformation(hexMap: State,transform: Callable[[tuple[int, int]],tuple[int, int]]) -> State:
    transformed_grid = copy.deepcopy(hexMap)
    for (q,r) in hexMap:
        transformed_grid[transform(q,r)] = hexMap[q,r]
    return transformed_grid