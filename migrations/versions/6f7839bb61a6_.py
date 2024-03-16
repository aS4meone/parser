"""empty message

Revision ID: 6f7839bb61a6
Revises: e1984fed54eb
Create Date: 2024-03-15 16:52:12.022602

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6f7839bb61a6'
down_revision: Union[str, None] = 'e1984fed54eb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('link', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('orders', 'link')
    # ### end Alembic commands ###