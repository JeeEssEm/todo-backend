"""empty message

Revision ID: 6bb4549d0bc8
Revises: 2dd0ac495593
Create Date: 2024-09-15 16:16:23.324444

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6bb4549d0bc8'
down_revision: Union[str, None] = '2dd0ac495593'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('User', 'xp')
    op.drop_column('UsersTeams', 'xp')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('UsersTeams', sa.Column('xp', sa.INTEGER(), nullable=True))
    op.add_column('User', sa.Column('xp', sa.INTEGER(), nullable=True))
    # ### end Alembic commands ###
