"""Use plain text passwords

Revision ID: ad844b6e6296
Revises: ea46b904986f
Create Date: 2025-04-08 19:04:58.168057

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'ad844b6e6296'
down_revision: Union[str, None] = 'ea46b904986f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('password', sa.String(length=255), nullable=False))
    op.drop_column('users', 'hashed_password')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('hashed_password', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=255), nullable=False))
    op.drop_column('users', 'password')
    # ### end Alembic commands ###
