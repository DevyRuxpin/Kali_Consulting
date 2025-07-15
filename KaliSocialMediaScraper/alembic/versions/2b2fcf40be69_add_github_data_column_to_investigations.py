"""add github_data column to investigations

Revision ID: 2b2fcf40be69
Revises: a832f2d9761d
Create Date: 2025-07-13 21:41:44.968566

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '2b2fcf40be69'
down_revision = 'a832f2d9761d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('investigations', sa.Column('github_data', sa.JSON(), nullable=True))


def downgrade() -> None:
    op.drop_column('investigations', 'github_data') 