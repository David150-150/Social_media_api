"""add content column to the posts table

Revision ID: d5ab2d61af33
Revises: e695961645ba
Create Date: 2025-01-21 07:10:58.412522

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd5ab2d61af33'
down_revision: Union[str, None] = 'e695961645ba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
