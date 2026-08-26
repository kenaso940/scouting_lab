"""create player stats table

Revision ID: 33fde74e2b62
Revises: b83000bcd43f
Create Date: 2026-08-23 20:49:32.398850

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '33fde74e2b62'
down_revision: Union[str, Sequence[str], None] = 'f28668008ead'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_unique_constraint(
        "uq_players_player_id",
        "players",
        ["player_id"]
    )



    op.create_table(
        "player_stats",

        sa.Column("player_id", sa.Integer(), nullable=False),
        sa.Column("season", sa.Integer(), nullable=False),

        sa.Column("appearances", sa.Integer(), nullable=False),
        sa.Column("minutes", sa.Integer(), nullable=False),

        sa.Column("goals", sa.Integer(), nullable=False),
        sa.Column("assists", sa.Integer(), nullable=False),

        sa.Column("shots_total", sa.Integer(), nullable=False),
        sa.Column("shots_on_target", sa.Integer(), nullable=False),

        sa.Column("passes_total", sa.Integer(), nullable=False),
        sa.Column("key_passes", sa.Integer(), nullable=False),
        sa.Column("pass_accuracy", sa.Integer(), nullable=False),

        sa.Column("tackles", sa.Integer(), nullable=False),
        sa.Column("interceptions", sa.Integer(), nullable=False),

        sa.Column("duels_total", sa.Integer(), nullable=False),
        sa.Column("duels_won", sa.Integer(), nullable=False),

        sa.Column("dribbles_attempted", sa.Integer(), nullable=False),
        sa.Column("dribbles_successful", sa.Integer(), nullable=False),

        sa.Column("fouls_drawn", sa.Integer(), nullable=False),
        sa.Column("fouls_committed", sa.Integer(), nullable=False),

        sa.Column("yellow_cards", sa.Integer(), nullable=False),
        sa.Column("red_cards", sa.Integer(), nullable=False),

        sa.ForeignKeyConstraint(
            ["player_id"],
            ["players.player_id"]
        ),

        sa.PrimaryKeyConstraint("player_id")
    )
    
    pass


def downgrade() -> None:
    op.drop_table("player_stats")
    pass




