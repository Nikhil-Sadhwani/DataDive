"""Add tokens_used to PromptLog

Revision ID: 46888f3090eb
Revises: 0ff835c1a3b2
Create Date: 2024-11-20 22:03:09.899906

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '46888f3090eb'
down_revision = '0ff835c1a3b2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('prompt_log', schema=None) as batch_op:
        batch_op.add_column(sa.Column('tokens_used', sa.Integer(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('prompt_log', schema=None) as batch_op:
        batch_op.drop_column('tokens_used')

    # ### end Alembic commands ###
