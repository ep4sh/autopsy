"""empty message

Revision ID: 3f8a1776124b
Revises: ee9c2caf9d31
Create Date: 2021-04-01 01:46:23.922905

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3f8a1776124b'
down_revision = 'ee9c2caf9d31'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('mortems', sa.Column('mortem_impact', sa.String(length=20), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('mortems', 'mortem_impact')
    # ### end Alembic commands ###