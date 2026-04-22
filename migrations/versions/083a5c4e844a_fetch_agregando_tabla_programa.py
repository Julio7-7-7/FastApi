"""fetch: agregando tabla programa

Revision ID: 083a5c4e844a
Revises: 08ccdffc578a
Create Date: 2026-04-20 22:42:39.737878

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '083a5c4e844a'
down_revision: Union[str, Sequence[str], None] = '08ccdffc578a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('programa',
        sa.Column('id_programa', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('id_tipo_programa', sa.Integer(), nullable=False),
        sa.Column('nombre_programa', sa.String(), nullable=False),
        sa.Column('vigente', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['id_tipo_programa'], ['tipo_programa.id_tipo_programa'], ),
        sa.PrimaryKeyConstraint('id_programa')
    )
    op.create_index(op.f('ix_programa_id_programa'), 'programa', ['id_programa'], unique=False)

def downgrade() -> None:
    op.drop_index(op.f('ix_programa_id_programa'), table_name='programa')
    op.drop_table('programa')
