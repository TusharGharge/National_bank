"""add email to user table

Revision ID: 0f4fbef48472
Revises: a8340a230095
Create Date: 2024-04-10 16:00:44.733191

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0f4fbef48472'
down_revision: Union[str, None] = 'a8340a230095'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("user",sa.Column('email',sa.String(),nullable=False,unique=True))
    pass


def downgrade() -> None:
    op.drop_column("user","email")
    pass
