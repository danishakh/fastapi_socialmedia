"""add users table

Revision ID: a36e76f47bd9
Revises: 36a68a6282d5
Create Date: 2021-11-07 16:42:16.006895

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a36e76f47bd9'
down_revision = '36a68a6282d5'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                        sa.Column('id', sa.Integer(), nullable=False),
                        sa.Column('email', sa.String(), nullable=False),
                        sa.Column('password', sa.String(), nullable=False),
                        sa.Column('name', sa.String(), nullable=False),
                        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
                        sa.PrimaryKeyConstraint('id'),
                        sa.UniqueConstraint('email')
                        )
    pass


def downgrade():
    op.drop_table('users')
    pass
