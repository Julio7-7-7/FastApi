"""refactor: estandarizando la tabla de  programas

Revision ID: a3f8283f36a7
Revises: 931d830bbf6a
Create Date: 2026-04-25 14:55:56.089964

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a3f8283f36a7'
down_revision: Union[str, Sequence[str], None] = '931d830bbf6a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.rename_table('programa', 'programas')
    op.alter_column('programas', 'nombre_programa', type_=sa.String(200), existing_nullable=False)
    op.create_unique_constraint('uq_programas_nombre_programa', 'programas', ['nombre_programa'])
    op.drop_index(op.f('ix_programa_id_programa'), table_name='programas')
    op.create_index(op.f('ix_programas_id_programa'), 'programas', ['id_programa'], unique=False)
    op.drop_constraint('programa_version_id_programa_fkey', 'programa_version', type_='foreignkey')
    op.create_foreign_key(None, 'programa_version', 'programas', ['id_programa'], ['id_programa'])
    op.drop_index(op.f('ix_tipo_programa_id_tipo_programa'), table_name='tipos_programa')
    op.create_index(op.f('ix_tipos_programa_id_tipo_programa'), 'tipos_programa', ['id_tipo_programa'], unique=False)

def downgrade() -> None:
    op.drop_index(op.f('ix_tipos_programa_id_tipo_programa'), table_name='tipos_programa')
    op.create_index(op.f('ix_tipo_programa_id_tipo_programa'), 'tipos_programa', ['id_tipo_programa'], unique=False)
    op.drop_constraint(None, 'programa_version', type_='foreignkey')
    op.create_foreign_key('programa_version_id_programa_fkey', 'programa_version', 'programas', ['id_programa'], ['id_programa'])
    op.drop_constraint('uq_programas_nombre_programa', 'programas', type_='unique')
    op.drop_index(op.f('ix_programas_id_programa'), table_name='programas')
    op.create_index(op.f('ix_programa_id_programa'), 'programas', ['id_programa'], unique=False)
    op.rename_table('programas', 'programa')