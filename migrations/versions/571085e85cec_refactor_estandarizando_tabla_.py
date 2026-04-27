"""refactor: estandarizando tabla modalidades_academicas

Revision ID: 571085e85cec
Revises: a59d38eb2bad
Create Date: 2026-04-26 21:28:47.501336

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '571085e85cec'
down_revision: Union[str, Sequence[str], None] = 'a59d38eb2bad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.rename_table('modalidad_academica', 'modalidades_academicas')
    op.add_column('modalidades_academicas', sa.Column('descripcion', sa.String(500), nullable=True))
    op.add_column('modalidades_academicas', sa.Column('requiere_titulo', sa.Boolean(), nullable=False, server_default='false'))
    op.add_column('modalidades_academicas', sa.Column('uso_unico', sa.Boolean(), nullable=False, server_default='false'))
    op.add_column('modalidades_academicas', sa.Column('estado', sa.String(20), nullable=False, server_default='activo'))
    op.drop_column('modalidades_academicas', 'vigente')
    op.alter_column('modalidades_academicas', 'nombre_modalidad', type_=sa.String(100), existing_nullable=False)
    op.create_unique_constraint('uq_modalidades_academicas_nombre', 'modalidades_academicas', ['nombre_modalidad'])
    op.drop_index(op.f('ix_modalidad_academica_id_modalidad_academica'), table_name='modalidades_academicas')
    op.create_index(op.f('ix_modalidades_academicas_id_modalidad_academica'), 'modalidades_academicas', ['id_modalidad_academica'], unique=False)
    op.drop_constraint(op.f('detalle_programa_alumno_id_modalidad_academica_fkey'), 'detalle_programa_alumno', type_='foreignkey')
    op.create_foreign_key('detalle_programa_alumno_id_modalidad_academica_fkey', 'detalle_programa_alumno', 'modalidades_academicas', ['id_modalidad_academica'], ['id_modalidad_academica'])
    op.drop_constraint(op.f('requisito_id_modalidad_academica_fkey'), 'requisito', type_='foreignkey')
    op.create_foreign_key('requisito_id_modalidad_academica_fkey', 'requisito', 'modalidades_academicas', ['id_modalidad_academica'], ['id_modalidad_academica'])

def downgrade() -> None:
    op.drop_constraint('requisito_id_modalidad_academica_fkey', 'requisito', type_='foreignkey')
    op.create_foreign_key('requisito_id_modalidad_academica_fkey', 'requisito', 'modalidades_academicas', ['id_modalidad_academica'], ['id_modalidad_academica'])
    op.drop_constraint('detalle_programa_alumno_id_modalidad_academica_fkey', 'detalle_programa_alumno', type_='foreignkey')
    op.create_foreign_key('detalle_programa_alumno_id_modalidad_academica_fkey', 'detalle_programa_alumno', 'modalidades_academicas', ['id_modalidad_academica'], ['id_modalidad_academica'])
    op.drop_index(op.f('ix_modalidades_academicas_id_modalidad_academica'), table_name='modalidades_academicas')
    op.create_index(op.f('ix_modalidad_academica_id_modalidad_academica'), 'modalidades_academicas', ['id_modalidad_academica'], unique=False)
    op.drop_constraint('uq_modalidades_academicas_nombre', 'modalidades_academicas', type_='unique')
    op.drop_column('modalidades_academicas', 'estado')
    op.drop_column('modalidades_academicas', 'uso_unico')
    op.drop_column('modalidades_academicas', 'requiere_titulo')
    op.drop_column('modalidades_academicas', 'descripcion')
    op.add_column('modalidades_academicas', sa.Column('vigente', sa.Boolean(), nullable=False, server_default='true'))
    op.rename_table('modalidades_academicas', 'modalidad_academica')
