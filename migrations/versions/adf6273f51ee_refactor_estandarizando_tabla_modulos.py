"""refactor: estandarizando tabla modulos

Revision ID: adf6273f51ee
Revises: 5e613b7a7ef9
Create Date: 2026-04-25 22:10:58.580663

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'adf6273f51ee'
down_revision: Union[str, Sequence[str], None] = '5e613b7a7ef9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.rename_table('modulo', 'modulos')
    op.add_column('modulos', sa.Column('estado', sa.String(20), nullable=False, server_default='activo'))
    op.alter_column('modulos', 'sigla', type_=sa.String(20), existing_nullable=False)
    op.alter_column('modulos', 'nombre_modulo', type_=sa.String(200), existing_nullable=False)
    op.alter_column('modulos', 'descripcion', type_=sa.String(500), existing_nullable=True)
    op.drop_column('modulos', 'vigente')
    op.drop_index(op.f('ix_modulo_id_modulo'), table_name='modulos')
    op.create_index(op.f('ix_modulos_id_modulo'), 'modulos', ['id_modulo'], unique=False)
    op.drop_constraint(op.f('detalle_programa_modulo_id_modulo_fkey'), 'detalle_programa_modulo', type_='foreignkey')
    op.create_foreign_key('detalle_programa_modulo_id_modulo_fkey', 'detalle_programa_modulo', 'modulos', ['id_modulo'], ['id_modulo'])

def downgrade() -> None:
    op.drop_constraint('detalle_programa_modulo_id_modulo_fkey', 'detalle_programa_modulo', type_='foreignkey')
    op.create_foreign_key('detalle_programa_modulo_id_modulo_fkey', 'detalle_programa_modulo', 'modulos', ['id_modulo'], ['id_modulo'])
    op.drop_index(op.f('ix_modulos_id_modulo'), table_name='modulos')
    op.create_index(op.f('ix_modulo_id_modulo'), 'modulos', ['id_modulo'], unique=False)
    op.drop_column('modulos', 'estado')
    op.add_column('modulos', sa.Column('vigente', sa.Boolean(), nullable=False, server_default='true'))
    op.rename_table('modulos', 'modulo')
