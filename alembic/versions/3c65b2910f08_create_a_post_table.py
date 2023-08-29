"""Create a post table

Revision ID: 3c65b2910f08
Revises: 
Create Date: 2023-08-26 17:14:13.958345

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3c65b2910f08'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("posts", sa.Column("id", sa.Integer, primary_key=True, nullable=False, autoincrement=True), sa.Column("title", sa.String, nullable=False))


def downgrade() -> None:
    op.drop_table(table_name="posts")