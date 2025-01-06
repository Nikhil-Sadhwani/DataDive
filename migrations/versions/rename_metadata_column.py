"""Rename metadata to data_metadata

Revision ID: rename_metadata_column
Revises: 
Create Date: 2025-01-06 18:55:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'rename_metadata_column'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Rename the column from metadata to data_metadata
    op.alter_column('scraped_data', 'metadata', new_column_name='data_metadata')


def downgrade():
    # Revert the column name back to metadata
    op.alter_column('scraped_data', 'data_metadata', new_column_name='metadata')
