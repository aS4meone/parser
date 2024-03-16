"""empty message

Revision ID: e1984fed54eb
Revises: 411dd1f1daa2
Create Date: 2024-03-15 16:32:41.833563

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e1984fed54eb'
down_revision: Union[str, None] = '411dd1f1daa2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('statuses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_statuses_id'), 'statuses', ['id'], unique=False)
    op.create_index(op.f('ix_statuses_name'), 'statuses', ['name'], unique=True)
    op.add_column('orders', sa.Column('status_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'orders', 'statuses', ['status_id'], ['id'])
    op.drop_column('orders', 'status')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('status', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'orders', type_='foreignkey')
    op.drop_column('orders', 'status_id')
    op.drop_index(op.f('ix_statuses_name'), table_name='statuses')
    op.drop_index(op.f('ix_statuses_id'), table_name='statuses')
    op.drop_table('statuses')
    # ### end Alembic commands ###