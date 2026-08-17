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


def euclidean_distance (player1, player2):
    distance = 0
    
    for i in range(len(player1)):
        distance += (player1[i] - player2[i]) **2

    return math.sqrt(distance)

salah = [90, 88, 85, 92, 45, 75]
player_a = [88, 86, 83, 90, 47, 74]

distance = euclidean_distance(salah, player_a)
print(distance)




    






