"""create player table

Revision ID: 7c898d02166b
Revises: 
Create Date: 2026-08-12 12:38:28.647280

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7c898d02166b'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
     op.create_table('players', sa.Column('player_name', sa.String(), nullable=False, primary_key=True),
    sa.Column('player_age', sa.Integer(), nullable=False))
    


def downgrade() -> None:
    op.drop_table('players')
    pass
