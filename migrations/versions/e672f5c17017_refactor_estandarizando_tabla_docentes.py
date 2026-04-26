"""refactor: estandarizando tabla docentes

Revision ID: e672f5c17017
Revises: adf6273f51ee
Create Date: 2026-04-25 23:05:16.374816

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'e672f5c17017'
down_revision: Union[str, Sequence[str], None] = 'adf6273f51ee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.rename_table('docente', 'docentes')
    op.add_column('docentes', sa.Column('genero', sa.String(20), nullable=True))
    op.add_column('docentes', sa.Column('titulo', sa.String(100), nullable=True))
    op.add_column('docentes', sa.Column('estado', sa.String(20), nullable=False, server_default='disponible'))
    op.drop_column('docentes', 'vigente')
    op.alter_column('docentes', 'ci', type_=sa.String(20), existing_nullable=False)
    op.alter_column('docentes', 'nombre', type_=sa.String(100), existing_nullable=False)
    op.alter_column('docentes', 'apellido', type_=sa.String(100), existing_nullable=False)
    op.alter_column('docentes', 'celular', type_=sa.String(20), existing_nullable=True)
    op.alter_column('docentes', 'correo', type_=sa.String(100), existing_nullable=False)
    op.drop_index(op.f('ix_docente_id_docente'), table_name='docentes')
    op.create_index(op.f('ix_docentes_id_docente'), 'docentes', ['id_docente'], unique=False)
    op.drop_constraint(op.f('detalle_programa_modulo_id_docente_fkey'), 'detalle_programa_modulo', type_='foreignkey')
    op.create_foreign_key('detalle_programa_modulo_id_docente_fkey', 'detalle_programa_modulo', 'docentes', ['id_docente'], ['id_docente'])

def downgrade() -> None:
    op.drop_constraint('detalle_programa_modulo_id_docente_fkey', 'detalle_programa_modulo', type_='foreignkey')
    op.create_foreign_key('detalle_programa_modulo_id_docente_fkey', 'detalle_programa_modulo', 'docentes', ['id_docente'], ['id_docente'])
    op.drop_index(op.f('ix_docentes_id_docente'), table_name='docentes')
    op.create_index(op.f('ix_docente_id_docente'), 'docentes', ['id_docente'], unique=False)
    op.drop_column('docentes', 'estado')
    op.drop_column('docentes', 'titulo')
    op.drop_column('docentes', 'genero')
    op.add_column('docentes', sa.Column('vigente', sa.Boolean(), nullable=False, server_default='true'))
    op.rename_table('docentes', 'docente')
