"""Add content column into posts

Revision ID: d50e999d2a17
Revises: 3c65b2910f08
Create Date: 2023-08-26 17:36:29.374145

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd50e999d2a17'
down_revision: Union[str, None] = '3c65b2910f08'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(table_name="posts", column=sa.Column(name="content", type_=sa.String, nullable=False))

def downgrade() -> None:
    op.drop_column(table_name="posts", column_name="content")
