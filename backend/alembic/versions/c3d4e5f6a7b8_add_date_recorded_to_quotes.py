"""add date_recorded to quotes

Revision ID: c3d4e5f6a7b8
Revises: b2c3d4e5f6a7
Create Date: 2026-03-22 18:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'c3d4e5f6a7b8'
down_revision: Union[str, Sequence[str], None] = 'b2c3d4e5f6a7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('quotes', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('date_recorded', sa.Date(), nullable=True)
        )


def downgrade() -> None:
    with op.batch_alter_table('quotes', schema=None) as batch_op:
        batch_op.drop_column('date_recorded')
