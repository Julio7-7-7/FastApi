"""feat: estandarizando la tabla tipos de programa

Revision ID: 931d830bbf6a
Revises: 9263e1c455a2
Create Date: 2026-04-25 13:33:00.851067

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '931d830bbf6a'
down_revision: Union[str, Sequence[str], None] = '9263e1c455a2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.rename_table('tipo_programa', 'tipos_programa')
    op.drop_constraint('programa_id_tipo_programa_fkey', 'programa', type_='foreignkey')
    op.add_column('tipos_programa', sa.Column('estado', sa.String(20), nullable=False, server_default='activo'))
    op.alter_column('tipos_programa', 'nombre', type_=sa.String(100), existing_nullable=False)
    op.create_unique_constraint('uq_tipos_programa_nombre', 'tipos_programa', ['nombre'])
    op.create_foreign_key('programa_id_tipo_programa_fkey', 'programa', 'tipos_programa', ['id_tipo_programa'], ['id_tipo_programa'])

def downgrade() -> None:
    op.drop_constraint('programa_id_tipo_programa_fkey', 'programa', type_='foreignkey')
    op.drop_constraint('uq_tipos_programa_nombre', 'tipos_programa', type_='unique')
    op.drop_column('tipos_programa', 'estado')
    op.rename_table('tipos_programa', 'tipo_programa')
    op.create_foreign_key('programa_id_tipo_programa_fkey', 'programa', 'tipo_programa', ['id_tipo_programa'], ['id_tipo_programa'])
