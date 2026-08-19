"""adding league column

Revision ID: b83000bcd43f
Revises: c8018a3df7a1
Create Date: 2026-08-19 10:48:53.230519

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b83000bcd43f'
down_revision: Union[str, Sequence[str], None] = 'c8018a3df7a1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('players', sa.Column('league', sa.String(), nullable=True))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
