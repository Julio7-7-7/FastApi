"""refactor: estandarizando tabla horarios

Revision ID: a59d38eb2bad
Revises: 549e6f3ac16b
Create Date: 2026-04-26 20:07:16.486023

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a59d38eb2bad'
down_revision: Union[str, Sequence[str], None] = '549e6f3ac16b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.rename_table('horario', 'horarios')
    op.add_column('horarios', sa.Column('aula', sa.String(200), nullable=True))
    op.alter_column('horarios', 'dia', type_=sa.String(20), existing_nullable=False)
    op.drop_index(op.f('ix_horario_id_horario'), table_name='horarios')
    op.create_index(op.f('ix_horarios_id_horario'), 'horarios', ['id_horario'], unique=False)

def downgrade() -> None:
    op.drop_index(op.f('ix_horarios_id_horario'), table_name='horarios')
    op.create_index(op.f('ix_horario_id_horario'), 'horarios', ['id_horario'], unique=False)
    op.drop_column('horarios', 'aula')
    op.rename_table('horarios', 'horario')
