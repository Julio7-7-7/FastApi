"""refactor: cambiar vigente por estado en tabla programas

Revision ID: 7b4b157a0c25
Revises: 4b3da79bba52
Create Date: 2026-05-19 11:33:59.280546

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7b4b157a0c25'
down_revision: Union[str, Sequence[str], None] = '4b3da79bba52'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Agregar columna nullable primero para datos existentes
    op.add_column('programas', sa.Column('estado', sa.String(length=20), nullable=True))

    # 2. Migrar datos: vigente=True → 'activo', vigente=False → 'inactivo'
    op.execute("UPDATE programas SET estado = 'activo' WHERE vigente = TRUE")
    op.execute("UPDATE programas SET estado = 'inactivo' WHERE vigente = FALSE")

    # 3. Hacer NOT NULL ahora que todos los registros tienen valor
    op.alter_column('programas', 'estado', nullable=False)

    # 4. Eliminar columna vieja
    op.drop_column('programas', 'vigente')


def downgrade() -> None:
    # 1. Agregar columna boolean nullable
    op.add_column('programas', sa.Column('vigente', sa.BOOLEAN(), nullable=True))

    # 2. Migrar datos inverso
    op.execute("UPDATE programas SET vigente = TRUE WHERE estado = 'activo'")
    op.execute("UPDATE programas SET vigente = FALSE WHERE estado = 'inactivo'")

    # 3. Hacer NOT NULL
    op.alter_column('programas', 'vigente', nullable=False)

    # 4. Eliminar columna nueva
    op.drop_column('programas', 'estado')
