"""add content column to posts table

Revision ID: 36a68a6282d5
Revises: e5524a08074d
Create Date: 2021-11-07 16:24:32.797641

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.schema import Column


# revision identifiers, used by Alembic.
revision = '36a68a6282d5'
down_revision = 'e5524a08074d'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
