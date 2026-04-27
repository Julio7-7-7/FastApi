"""refactor: estandarizando tabla alumnos

Revision ID: ca5db6c70c08
Revises: 0873f12310c1
Create Date: 2026-04-26 22:53:36.111452

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'ca5db6c70c08'
down_revision: Union[str, Sequence[str], None] = '0873f12310c1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.rename_table('alumno', 'alumnos')
    op.add_column('alumnos', sa.Column('pasaporte', sa.String(30), nullable=True))
    op.add_column('alumnos', sa.Column('estado', sa.String(20), nullable=False, server_default='activo'))
    op.alter_column('alumnos', 'ci', nullable=True, existing_nullable=False)
    op.alter_column('alumnos', 'ci', type_=sa.String(20), existing_nullable=True)
    op.alter_column('alumnos', 'nombre', type_=sa.String(100), existing_nullable=False)
    op.alter_column('alumnos', 'apellido', type_=sa.String(100), existing_nullable=False)
    op.alter_column('alumnos', 'celular', type_=sa.String(20), existing_nullable=True)
    op.alter_column('alumnos', 'correo', type_=sa.String(100), existing_nullable=False)
    op.alter_column('alumnos', 'direccion', type_=sa.String(300), existing_nullable=True)
    op.create_unique_constraint('uq_alumnos_pasaporte', 'alumnos', ['pasaporte'])
    op.drop_index(op.f('ix_alumno_id_alumno'), table_name='alumnos')
    op.create_index(op.f('ix_alumnos_id_alumno'), 'alumnos', ['id_alumno'], unique=False)
    op.drop_constraint(op.f('detalle_programa_alumno_id_alumno_fkey'), 'detalle_programa_alumno', type_='foreignkey')
    op.create_foreign_key('detalle_programa_alumno_id_alumno_fkey', 'detalle_programa_alumno', 'alumnos', ['id_alumno'], ['id_alumno'])

def downgrade() -> None:
    op.drop_constraint('detalle_programa_alumno_id_alumno_fkey', 'detalle_programa_alumno', type_='foreignkey')
    op.create_foreign_key('detalle_programa_alumno_id_alumno_fkey', 'detalle_programa_alumno', 'alumnos', ['id_alumno'], ['id_alumno'])
    op.drop_index(op.f('ix_alumnos_id_alumno'), table_name='alumnos')
    op.create_index(op.f('ix_alumno_id_alumno'), 'alumnos', ['id_alumno'], unique=False)
    op.drop_constraint('uq_alumnos_pasaporte', 'alumnos', type_='unique')
    op.drop_column('alumnos', 'estado')
    op.drop_column('alumnos', 'pasaporte')
    op.alter_column('alumnos', 'ci', nullable=False, existing_nullable=True)
    op.rename_table('alumnos', 'alumno')
