"""Initial migration.

Revision ID: 7806b1db044c
Revises: 
Create Date: 2020-11-07 17:17:53.566274

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7806b1db044c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=16), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('joined_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_joined_at'), 'user', ['joined_at'], unique=False)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_joined_at'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###