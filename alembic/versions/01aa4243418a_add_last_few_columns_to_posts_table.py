"""add last few columns to posts table

Revision ID: 01aa4243418a
Revises: 274b91b636b3
Create Date: 2021-11-07 16:51:25.412808

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '01aa4243418a'
down_revision = '274b91b636b3'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
