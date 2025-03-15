import collections
from typing import Dict, List

Cell = collections.namedtuple("Cell", ["q", "r"])
HexMap = Dict[Cell, int]


def CellAdd(a: Cell, b: Cell) -> Cell:
    return Cell(a.q + b.q, a.r + b.r)

CellDirections = [Cell(1, 1), Cell(1, 0), Cell(0, -1), Cell(-1, -1), Cell(-1, 0), Cell(0, 1)]

def getCellNeighbor(cell: Cell) -> List[Cell]:
    neighbors = []
    for direction in CellDirections:
        neighbors.append(CellAdd(cell, direction))
    return neighbors 
        
def generateHexMap(N: int) -> HexMap:
    hexMap = {}
    for q in range(-N, N+1):
        r1 = max(-N, q - N)
        r2 = min(N, q + N)
        for r in range(r1, r2+1):
            cell = Cell(q, r)
            hexMap[cell] = 0
    return hexMap

def convertStatetoDict(hexmap):
    hex_dict = {}
    for cell in hexmap:
        if len(cell) == 2:
            coordinates, value = cell
            cell = Cell(coordinates[0],coordinates[1])
            hex_dict[cell] = value
        else:
            # Handle cases with malformed entries (ignore or raise an error)
            print(f"Malformed cell: {cell}")
    return hex_dict

def initHexMap() -> HexMap:
    print("Choisissez une taille de l'hexagone entre 1 et 10 :")
    while True:
        taille = input("Taille de l'hexagone : ")
        if taille.isdigit():
            taille = int(taille)
            if 1 <= taille <= 10:
                return generateHexMap(taille)
            else:
                print("Taille de map invalide. Veuillez choisir une taille entre 1 et 10.")
        else:
            print("Veuillez entrer un nombre entier.")