"""add player id to players table

Revision ID: f28668008ead
Revises: 33fde74e2b62
Create Date: 2026-08-23 21:37:52.758988

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f28668008ead'
down_revision: Union[str, Sequence[str], None] = 'b83000bcd43f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("players", sa.Column("player_id", sa.Integer, nullable=True))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
