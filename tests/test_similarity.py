import pytest

from app.models.players import PlayerStats

from app.services.scouting import (
    per90,
    ratio,
    get_features,
    normalize_feature_vectors,
    euclidean_distance,
)


def test_per90():
    result = per90(
        value=10,
        minutes=900
    )

    assert result == pytest.approx(1.0)


def test_per90_with_zero_minutes():
    result = per90(
        value=10,
        minutes=0
    )

    assert result == 0.0


def test_ratio():
    result = ratio(
        successful=50,
        total=100
    )

    assert result == pytest.approx(0.5)


def test_ratio_with_zero_total():
    result = ratio(
        successful=10,
        total=0
    )

    assert result == 0.0


def test_get_features():
    stats = PlayerStats(
        player_id=999,
        season=2024,

        appearances=10,
        minutes=900,

        goals=10,
        assists=5,

        shots_total=40,
        shots_on_target=20,

        passes_total=500,
        key_passes=30,
        pass_accuracy=80,

        tackles=20,
        interceptions=10,

        duels_total=100,
        duels_won=50,

        dribbles_attempted=40,
        dribbles_successful=20,

        fouls_drawn=30,
        fouls_committed=15,

        yellow_cards=2,
        red_cards=0
    )

    features = get_features(stats)

    assert len(features) == 15

    # Goals per 90
    assert features[0] == pytest.approx(1.0)

    # Assists per 90
    assert features[1] == pytest.approx(0.5)

    # Shot-on-target rate
    assert features[3] == pytest.approx(0.5)

    # Pass accuracy converted to 0-1
    assert features[6] == pytest.approx(0.8)

    # Duel win rate
    assert features[10] == pytest.approx(0.5)

    # Dribble success rate
    assert features[12] == pytest.approx(0.5)


def test_normalize_feature_vectors():
    vectors = [
        [1.0, 10.0],
        [3.0, 20.0]
    ]

    normalized = normalize_feature_vectors(
        vectors
    )

    assert normalized[0][0] == pytest.approx(-1.0)
    assert normalized[1][0] == pytest.approx(1.0)

    assert normalized[0][1] == pytest.approx(-1.0)
    assert normalized[1][1] == pytest.approx(1.0)


def test_euclidean_distance_without_weights():
    player1 = [10, 20, 30]
    player2 = [13, 24, 30]

    distance = euclidean_distance(
        player1,
        player2
    )

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

    expected = (
        2 * (10 - 12) ** 2
        + 1 * (20 - 24) ** 2
    ) ** 0.5

    assert distance == pytest.approx(
        expected
    )