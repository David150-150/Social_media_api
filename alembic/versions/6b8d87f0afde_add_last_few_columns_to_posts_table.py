"""add last few columns to posts table

Revision ID: 6b8d87f0afde
Revises: 08bdf64abe42
Create Date: 2025-01-21 08:11:27.316345

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6b8d87f0afde'
down_revision: Union[str, None] = '08bdf64abe42'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text
                                     ('NOW()')),)
    
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.add_column('posts', 'created_at')
    pass
