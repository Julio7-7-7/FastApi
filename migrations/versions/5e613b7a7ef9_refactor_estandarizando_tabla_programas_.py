"""refactor: estandarizando tabla programas_version

Revision ID: 5e613b7a7ef9
Revises: f3514d928da6
Create Date: 2026-04-25 15:18:40.415691

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '5e613b7a7ef9'
down_revision: Union[str, Sequence[str], None] = 'a3f8283f36a7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # renombrar en lugar de drop+create
    op.rename_table('programa_version', 'programas_version')
    
    # agregar columnas nuevas
    op.add_column('programas_version', sa.Column('descripcion', sa.String(500), nullable=True))
    op.add_column('programas_version', sa.Column('vigente', sa.Boolean(), nullable=False, server_default='true'))
    
    # actualizar indices
    op.drop_index(op.f('ix_programa_version_id_programa_version'), table_name='programas_version')
    op.create_index(op.f('ix_programas_version_id_programa_version'), 'programas_version', ['id_programa_version'], unique=False)
    
    # actualizar FK de modulo
    op.drop_constraint(op.f('modulo_id_programa_version_fkey'), 'modulo', type_='foreignkey')
    op.create_foreign_key('modulo_id_programa_version_fkey', 'modulo', 'programas_version', ['id_programa_version'], ['id_programa_version'])
    
    # actualizar FK de programa_version_edicion
    op.drop_constraint(op.f('programa_version_edicion_id_programa_version_fkey'), 'programa_version_edicion', type_='foreignkey')
    op.create_foreign_key('programa_version_edicion_id_programa_version_fkey', 'programa_version_edicion', 'programas_version', ['id_programa_version'], ['id_programa_version'])


def downgrade() -> None:
    op.drop_constraint('programa_version_edicion_id_programa_version_fkey', 'programa_version_edicion', type_='foreignkey')
    op.create_foreign_key('programa_version_edicion_id_programa_version_fkey', 'programa_version_edicion', 'programas_version', ['id_programa_version'], ['id_programa_version'])
    
    op.drop_constraint('modulo_id_programa_version_fkey', 'modulo', type_='foreignkey')
    op.create_foreign_key('modulo_id_programa_version_fkey', 'modulo', 'programas_version', ['id_programa_version'], ['id_programa_version'])
    
    op.drop_index(op.f('ix_programas_version_id_programa_version'), table_name='programas_version')
    op.create_index(op.f('ix_programa_version_id_programa_version'), 'programas_version', ['id_programa_version'], unique=False)
    
    op.drop_column('programas_version', 'vigente')
    op.drop_column('programas_version', 'descripcion')
    
    op.rename_table('programas_version', 'programa_version')
