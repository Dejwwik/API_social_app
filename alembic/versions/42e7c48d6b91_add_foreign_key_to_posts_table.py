"""Add foreign key to posts table

Revision ID: 42e7c48d6b91
Revises: 889649e92a4d
Create Date: 2023-08-28 19:48:47.174602

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '42e7c48d6b91'
down_revision: Union[str, None] = '889649e92a4d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("owner_id", sa.Integer, nullable=False))
    op.create_foreign_key("posts_users_fk", "posts", "users", ["owner_id"], ["id"], ondelete="CASCADE")
    #Name of key, source table, dest table, source column, dest column

def downgrade() -> None:
    op.drop_constraint("posts_users_fk", "posts")
    op.drop_column("posts", "owner_id")
