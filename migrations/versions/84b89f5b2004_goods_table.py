"""goods table

Revision ID: 84b89f5b2004
Revises: 0152b376485c
Create Date: 2022-08-17 22:47:42.282957

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '84b89f5b2004'
down_revision = '0152b376485c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('goods', sa.Column('category', sa.String(), nullable=True))
    op.add_column('goods', sa.Column('condition', sa.String(), nullable=True))
    op.drop_column('goods', 'descripton')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('goods', sa.Column('descripton', sa.VARCHAR(length=500), nullable=True))
    op.drop_column('goods', 'condition')
    op.drop_column('goods', 'category')
    # ### end Alembic commands ###
