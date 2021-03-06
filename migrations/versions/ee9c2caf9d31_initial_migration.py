"""Initial migration

Revision ID: ee9c2caf9d31
Revises: 
Create Date: 2021-04-01 00:39:58.002389

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ee9c2caf9d31'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_name', sa.String(length=20), nullable=False),
    sa.Column('user_email', sa.String(length=20), nullable=False),
    sa.Column('user_password', sa.String(length=100), nullable=False),
    sa.Column('user_image', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_email')
    )
    op.create_table('mortems',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('mortem_name', sa.String(length=100), nullable=False),
    sa.Column('mortem_url', sa.String(length=16), nullable=False),
    sa.Column('mortem_content', sa.Text(), nullable=False),
    sa.Column('mortem_created', sa.DateTime(), nullable=False),
    sa.Column('mortem_updated', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('support',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('support_subject', sa.String(length=100), nullable=False),
    sa.Column('support_content', sa.Text(), nullable=False),
    sa.Column('support_created', sa.DateTime(), nullable=False),
    sa.Column('support_attach', sa.LargeBinary(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('support')
    op.drop_table('mortems')
    op.drop_table('users')
    # ### end Alembic commands ###
