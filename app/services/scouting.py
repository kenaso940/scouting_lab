import math

from app.models.players import PlayerStats


MIN_MINUTES = 450


def per90(value, minutes):
    """
    Convert a counting statistic into a per-90 value.
    """

    if minutes <= 0:
        return 0.0

    return (value / minutes) * 90


def ratio(successful, total):
    """
    Convert two counts into a success rate between 0 and 1.
    """

    if total <= 0:
        return 0.0

    return successful / total


def get_features(stats: PlayerStats):
    """
    Convert a player's raw season statistics into
    a feature vector suitable for similarity comparison.
    """

    return [
        # Attacking
        per90(stats.goals, stats.minutes),
        per90(stats.assists, stats.minutes),
        per90(stats.shots_total, stats.minutes),

        ratio(
            stats.shots_on_target,
            stats.shots_total
        ),

        # Passing
        per90(stats.passes_total, stats.minutes),
        per90(stats.key_passes, stats.minutes),

        stats.pass_accuracy / 100
        if stats.pass_accuracy
        else 0.0,

        # Defending
        per90(stats.tackles, stats.minutes),
        per90(stats.interceptions, stats.minutes),

        # Duels
        per90(stats.duels_total, stats.minutes),

        ratio(
            stats.duels_won,
            stats.duels_total
        ),

        # Dribbling
        per90(stats.dribbles_attempted, stats.minutes),

        ratio(
            stats.dribbles_successful,
            stats.dribbles_attempted
        ),

        # Fouls
        per90(stats.fouls_drawn, stats.minutes),
        per90(stats.fouls_committed, stats.minutes),
    ]


def normalize_feature_vectors(vectors):
    """
    Z-score normalize every feature so that features
    measured on different scales can be compared fairly.

    normalized_value = (value - mean) / std
    """

    if not vectors:
        return []

    feature_count = len(vectors[0])

    means = []
    standard_deviations = []

    for feature_index in range(feature_count):
        values = [
            vector[feature_index]
            for vector in vectors
        ]

        mean = sum(values) / len(values)

        variance = sum(
            (value - mean) ** 2
            for value in values
        ) / len(values)

        standard_deviation = math.sqrt(variance)

        means.append(mean)
        standard_deviations.append(
            standard_deviation
        )

    normalized_vectors = []

    for vector in vectors:
        normalized_vector = []

        for feature_index, value in enumerate(vector):

            standard_deviation = (
                standard_deviations[feature_index]
            )

            if standard_deviation == 0:
                normalized_value = 0.0

            else:
                normalized_value = (
                    value - means[feature_index]
                ) / standard_deviation

            normalized_vector.append(
                normalized_value
            )

        normalized_vectors.append(
            normalized_vector
        )

    return normalized_vectors


def euclidean_distance(
    player1,
    player2,
    weights=None
):
    """
    Calculate weighted Euclidean distance.

    Lower distance means the players are more similar.
    """

    if len(player1) != len(player2):
        raise ValueError(
            "Players must have the same number of features"
        )

    if weights is None:
        weights = [1] * len(player1)

    if len(weights) != len(player1):
        raise ValueError(
            "Weights must match the number of features"
        )

    distance = 0

    for i in range(len(player1)):
        distance += (
            weights[i]
            * (player1[i] - player2[i]) ** 2
        )

    return math.sqrt(distance)