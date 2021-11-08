"""add foreign key to posts table

Revision ID: 274b91b636b3
Revises: a36e76f47bd9
Create Date: 2021-11-07 16:46:56.498474

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import null


# revision identifiers, used by Alembic.
revision = '274b91b636b3'
down_revision = 'a36e76f47bd9'
branch_labels = None
depends_on = None


def upgrade():
    # add user_id column to posts table
    op.add_column('posts', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table='posts', referent_table='users', local_cols=['user_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts', 'user_id')
    pass
