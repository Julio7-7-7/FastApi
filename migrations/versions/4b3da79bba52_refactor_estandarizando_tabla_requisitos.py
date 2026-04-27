"""refactor: estandarizando tabla requisitos

Revision ID: 4b3da79bba52
Revises: ca5db6c70c08
Create Date: 2026-04-26 23:33:59.735369

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '4b3da79bba52'
down_revision: Union[str, Sequence[str], None] = 'ca5db6c70c08'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.rename_table('requisito', 'requisitos')
    op.add_column('requisitos', sa.Column('estado', sa.String(20), nullable=False, server_default='activo'))
    op.alter_column('requisitos', 'nombre', type_=sa.String(200), existing_nullable=False)
    op.alter_column('requisitos', 'descripcion', type_=sa.String(500), existing_nullable=True)
    op.create_unique_constraint('uq_requisito_nombre_modalidad', 'requisitos', ['nombre', 'id_modalidad_academica'])
    op.drop_index(op.f('ix_requisito_id_requisito'), table_name='requisitos')
    op.create_index(op.f('ix_requisitos_id_requisito'), 'requisitos', ['id_requisito'], unique=False)
    op.drop_constraint(op.f('control_documentacion_id_requisito_fkey'), 'control_documentacion', type_='foreignkey')
    op.create_foreign_key('control_documentacion_id_requisito_fkey', 'control_documentacion', 'requisitos', ['id_requisito'], ['id_requisito'])
    op.drop_constraint(op.f('tipos_descuento_id_requisito_extra_fkey'), 'tipos_descuento', type_='foreignkey')
    op.create_foreign_key('tipos_descuento_id_requisito_extra_fkey', 'tipos_descuento', 'requisitos', ['id_requisito_extra'], ['id_requisito'])

def downgrade() -> None:
    op.drop_constraint('tipos_descuento_id_requisito_extra_fkey', 'tipos_descuento', type_='foreignkey')
    op.create_foreign_key('tipos_descuento_id_requisito_extra_fkey', 'tipos_descuento', 'requisitos', ['id_requisito_extra'], ['id_requisito'])
    op.drop_constraint('control_documentacion_id_requisito_fkey', 'control_documentacion', type_='foreignkey')
    op.create_foreign_key('control_documentacion_id_requisito_fkey', 'control_documentacion', 'requisitos', ['id_requisito'], ['id_requisito'])
    op.drop_index(op.f('ix_requisitos_id_requisito'), table_name='requisitos')
    op.create_index(op.f('ix_requisito_id_requisito'), 'requisitos', ['id_requisito'], unique=False)
    op.drop_constraint('uq_requisito_nombre_modalidad', 'requisitos', type_='unique')
    op.drop_column('requisitos', 'estado')
    op.rename_table('requisitos', 'requisito')
