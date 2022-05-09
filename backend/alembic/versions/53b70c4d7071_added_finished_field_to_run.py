"""Added finished field to run

Revision ID: 53b70c4d7071
Revises: 2a846ee9cec9
Create Date: 2022-05-09 16:59:34.580269

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '53b70c4d7071'
down_revision = '2a846ee9cec9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('runs', sa.Column('finished', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('runs', 'finished')
    # ### end Alembic commands ###
