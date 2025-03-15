import requests

URL = "http://localhost:8080/play"  # Remplacez par l'URL correcte

def sendRequest(player: int, x: int, y: int):
    """
    Envoie une requête HTTP POST avec les données du joueur et de la position.
    
    Args:
        player (int): Le numéro du joueur (1 ou 2).
        x (int): La coordonnée x de la position.
        y (int): La coordonnée y de la position.
        url (str): L'URL à laquelle envoyer la requête.
        
    Returns:
        response: La réponse de la requête HTTP.
    """
    data = {
        "Player": player,
        "Position": {
            "x": x,
            "y": y
        }
    }
    
    response = requests.post(URL, json=data)
    return response
