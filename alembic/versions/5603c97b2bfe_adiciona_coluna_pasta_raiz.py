"""Adiciona coluna pasta_raiz

Revision ID: 5603c97b2bfe
Revises: 
Create Date: 2025-05-23 12:02:59.483534

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5603c97b2bfe'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('nomes_pasta',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('pasta_raiz', sa.String(), nullable=True),
    sa.Column('nome_original', sa.String(), nullable=False),
    sa.Column('nome_sugerido', sa.String(), nullable=True),
    sa.Column('corrigido', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('nomes_pasta')
    # ### end Alembic commands ###
