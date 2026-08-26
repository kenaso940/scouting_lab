"""change players primary key to player id

Revision ID: cb932b78eef7
Revises: f8b33c4589f6
Create Date: 2026-08-23 22:35:05.911075

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cb932b78eef7'
down_revision: Union[str, Sequence[str], None] = 'f8b33c4589f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # We're abandoning the old prototype dataset
    op.execute("DELETE FROM player_stats")
    op.execute("DELETE FROM players")

    # Temporarily remove the FK so we can change the constraint
    # that players.player_id relies on.
    op.drop_constraint(
        "player_stats_player_id_fkey",
        "player_stats",
        type_="foreignkey"
    )

    # Remove the old player_name primary key
    op.drop_constraint(
        "players_pkey",
        "players",
        type_="primary"
    )

    # player_id can now be required
    op.alter_column(
        "players",
        "player_id",
        existing_type=sa.Integer(),
        nullable=False
    )

    # Make player_id the new primary key
    op.create_primary_key(
        "players_pkey",
        "players",
        ["player_id"]
    )

    # The old unique constraint is now redundant because
    # a primary key is already unique.
    op.drop_constraint(
        "uq_players_player_id",
        "players",
        type_="unique"
    )

    # Recreate the player_stats foreign key.
    # It now points directly at the players primary key.
    op.create_foreign_key(
        "player_stats_player_id_fkey",
        "player_stats",
        "players",
        ["player_id"],
        ["player_id"]
    )
    pass


def downgrade() -> None:
    op.drop_constraint(
        "player_stats_player_id_fkey",
        "player_stats",
        type_="foreignkey"
    )

    op.drop_constraint(
        "players_pkey",
        "players",
        type_="primary"
    )

    op.alter_column(
        "players",
        "player_id",
        existing_type=sa.Integer(),
        nullable=True
    )

    op.create_unique_constraint(
        "uq_players_player_id",
        "players",
        ["player_id"]
    )

    op.create_primary_key(
        "players_pkey",
        "players",
        ["player_name"]
    )

    op.create_foreign_key(
        "player_stats_player_id_fkey",
        "player_stats",
        "players",
        ["player_id"],
        ["player_id"]
    )
    pass
