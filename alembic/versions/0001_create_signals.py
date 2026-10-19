"""create signals table
Revision ID: 0001_create_signals
Revises: 
Create Date: 2026-10-19 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001_create_signals'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'signals',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('source', sa.String(length=128), nullable=False),
        sa.Column('timestamp', sa.Float, nullable=False),
        sa.Column('payload', sa.Text, nullable=False),
    )


def downgrade():
    op.drop_table('signals')
