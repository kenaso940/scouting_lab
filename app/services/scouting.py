import math

def get_features(player):
    return [
        player.pace,
        player.shooting,
        player.dribbling,
        player.passing,
        player.defending,
        player.physical
    ]


def euclidean_distance (player1, player2, weights=None):
    if len(player1) != len(player2):
        raise ValueError("Players must have the same number of features")

    if weights is None:
        weights = [1] * len(player1)

    if len(weights) != len(player1):
        raise ValueError("Weights must match the number of features")

    distance = 0
    
    for i in range(len(player1)):
        distance += weights[i] * (player1[i] - player2[i]) **2

    return math.sqrt(distance)





    






