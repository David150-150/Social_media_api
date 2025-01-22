# """add user table

# Revision ID: 0621400dc6a0
# Revises: d5ab2d61af33
# Create Date: 2025-01-21 07:24:29.541804

# """
# from typing import Sequence, Union

# from alembic import op
# import sqlalchemy as sa


# # revision identifiers, used by Alembic.
# revision: str = '0621400dc6a0'
# down_revision: Union[str, None] = 'd5ab2d61af33'
# branch_labels: Union[str, Sequence[str], None] = None
# depends_on: Union[str, Sequence[str], None] = None


# def upgrade() -> None:
#     op.create_table('users',
#                     sa.Column('id', sa.Integer(), nullable=False),
#                     sa.Column('email', sa.String(), nullable=False),
#                      sa.Column('password', sa.String(), nullable=False),
#                       sa.Column('created_at', sa.TIMESTAMP(timezone=True),
#                             sa.PrimaryKeyConstraint('id'),
#                             sa.UniqueConstraint('email')))
#     pass


# def downgrade() -> None:
#     op.drop_table('users')
#     pass


"""add user table

Revision ID: 0621400dc6a0
Revises: d5ab2d61af33
Create Date: 2025-01-21 07:24:29.541804

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0621400dc6a0'
down_revision: Union[str, None] = 'd5ab2d61af33'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('email', sa.String(), unique=True, nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('users')

