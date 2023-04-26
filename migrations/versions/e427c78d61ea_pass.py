"""pass

Revision ID: e427c78d61ea
Revises: d6f1b8b8306d
Create Date: 2023-04-26 21:45:03.252561

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e427c78d61ea'
down_revision = 'd6f1b8b8306d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('profile', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password', sa.String(length=128), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('profile', schema=None) as batch_op:
        batch_op.drop_column('password')

    # ### end Alembic commands ###
