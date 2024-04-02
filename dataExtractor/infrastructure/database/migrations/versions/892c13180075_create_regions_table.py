"""Create regions table

Revision ID: 892c13180075
Revises: 
Create Date: 2024-03-21 21:04:01.363753

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '892c13180075'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('regions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('x1', sa.Integer(), nullable=False),
    sa.Column('y1', sa.Integer(), nullable=False),
    sa.Column('x2', sa.Integer(), nullable=False),
    sa.Column('y2', sa.Integer(), nullable=False),
    sa.Column('external_id', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('regions')
    # ### end Alembic commands ###