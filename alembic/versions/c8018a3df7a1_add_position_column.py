"""Add Position column

Revision ID: c8018a3df7a1
Revises: 711b974bfa5e
Create Date: 2026-08-17 14:28:30.963319

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c8018a3df7a1'
down_revision: Union[str, Sequence[str], None] = '711b974bfa5e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('players', sa.Column('position', sa.String(), nullable=True))

  


def downgrade() -> None:
    """Downgrade schema."""
    pass
