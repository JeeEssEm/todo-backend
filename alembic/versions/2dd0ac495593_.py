"""empty message

Revision ID: 2dd0ac495593
Revises: e005eaccd893
Create Date: 2024-09-15 16:11:05.988549

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2dd0ac495593'
down_revision: Union[str, None] = 'e005eaccd893'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('User',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('token_date_valid', sa.DateTime(), nullable=True),
    sa.Column('xp', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_index(op.f('ix_User_id'), 'User', ['id'], unique=False)
    op.create_table('Team',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['User.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_Team_id'), 'Team', ['id'], unique=False)
    op.create_table('Task',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('status', sa.Enum('planning', 'running', 'done', 'archived', 'cancelled', name='taskstatus'), nullable=False),
    sa.Column('importance', sa.Enum('regular', 'important', 'extremely_important', name='taskimportance'), nullable=False),
    sa.Column('reminder', sa.DateTime(), nullable=True),
    sa.Column('attendant_id', sa.Integer(), nullable=True),
    sa.Column('team_id', sa.Integer(), nullable=True),
    sa.Column('xp', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['attendant_id'], ['User.id'], ),
    sa.ForeignKeyConstraint(['team_id'], ['Team.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_Task_id'), 'Task', ['id'], unique=False)
    op.create_table('UsersTeams',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('team_id', sa.Integer(), nullable=True),
    sa.Column('rights', sa.Enum('admin', 'member', name='rights'), nullable=True),
    sa.Column('xp', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['team_id'], ['Team.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['User.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_UsersTeams_id'), 'UsersTeams', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_UsersTeams_id'), table_name='UsersTeams')
    op.drop_table('UsersTeams')
    op.drop_index(op.f('ix_Task_id'), table_name='Task')
    op.drop_table('Task')
    op.drop_index(op.f('ix_Team_id'), table_name='Team')
    op.drop_table('Team')
    op.drop_index(op.f('ix_User_id'), table_name='User')
    op.drop_table('User')
    # ### end Alembic commands ###
