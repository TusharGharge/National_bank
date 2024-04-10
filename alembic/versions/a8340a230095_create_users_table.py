"""create users table

Revision ID: a8340a230095
Revises: 
Create Date: 2024-04-10 15:48:15.174330

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a8340a230095'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("user",sa.Column('id',sa.Integer(),nullable=False,primary_key=True),sa.Column('name',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('user')
    pass
