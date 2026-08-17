"""addings the rest of the player attributes

Revision ID: 711b974bfa5e
Revises: 7c898d02166b
Create Date: 2026-08-12 12:57:03.950783

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '711b974bfa5e'
down_revision: Union[str, Sequence[str], None] = '7c898d02166b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('players', sa.Column('pace', sa.Integer(), nullable=False))
    op.add_column('players', sa.Column('shooting', sa.Integer(), nullable=False))
    op.add_column('players', sa.Column('dribbling', sa.Integer(), nullable=False))
    op.add_column('players', sa.Column('passing', sa.Integer(), nullable=False))
    op.add_column('players', sa.Column('physical', sa.Integer(), nullable=False))
    op.add_column('players', sa.Column('defending', sa.Integer(), nullable=False))

def downgrade() -> None:
    op.drop_column("players", 'pace')
    op.drop_column("players", 'shooting')
    op.drop_column("players", 'dribbling')
    op.drop_column("players", 'passing')
    op.drop_column("players", 'physical')
    op.drop_column("players", 'defending')
    
