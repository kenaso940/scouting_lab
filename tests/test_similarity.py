
import pytest

from app.services.scouting import get_features, euclidean_distance


def test_euclidean_distance_without_weights():
    player1 = [10, 20, 30]
    player2 = [13, 24, 30]

    distance = euclidean_distance(player1, player2)

    assert distance == pytest.approx(5.0)



def test_euclidean_distance_with_weights():
    player1 = [10, 20]
    player2 = [12, 24]

    weights = [2, 1]

    distance = euclidean_distance(
        player1,
        player2,
        weights
    )

    expected = (2 * (10 - 12) ** 2 + 1 * (20 - 24) ** 2) ** 0.5

    assert distance == pytest.approx(expected)