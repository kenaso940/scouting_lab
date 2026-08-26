import pytest

from fastapi.testclient import TestClient
from app.main import app


pytestmark = pytest.mark.usefixtures(
    "seed_test_database"
)


client = TestClient(app)


def test_player_not_found():
    response = client.get(
        "/players/DefinitelyNotARealPlayer/similar?k=3"
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Player not found"
    }


def test_k_cannot_be_zero():
    response = client.get(
        "/players/Salah/similar?k=0"
    )

    assert response.status_code == 422


def test_k_cannot_be_over_100():
    response = client.get(
        "/players/Salah/similar?k=101"
    )

    assert response.status_code == 422


def test_k_returns_correct_number_of_players():
    response = client.get(
        "/players/Salah/similar"
        "?k=3"
        "&position=RW"
    )

    assert response.status_code == 200

    players = response.json()

    assert len(players) == 3


def test_position_filter():
    response = client.get(
        "/players/Salah/similar"
        "?k=10"
        "&position=RW"
    )

    assert response.status_code == 200

    players = response.json()

    for player in players:
        assert player["position"] == "RW"


def test_league_filter():
    response = client.get(
        "/players/Rodrygo/similar"
        "?k=10"
        "&position=RW"
        "&league=La%20Liga"
    )

    assert response.status_code == 200

    players = response.json()

    for player in players:
        assert player["league"] == "La Liga"


def test_target_player_is_not_returned():
    response = client.get(
        "/players/Salah/similar"
        "?k=10"
        "&position=RW"
    )

    assert response.status_code == 200

    names = [
        player["name"]
        for player in response.json()
    ]

    assert "Salah" not in names


def test_players_are_sorted_by_distance():
    response = client.get(
        "/players/Salah/similar"
        "?k=5"
        "&position=RW"
    )

    assert response.status_code == 200

    players = response.json()

    distances = [
        player["similarity"]
        for player in players
    ]

    assert distances == sorted(distances)