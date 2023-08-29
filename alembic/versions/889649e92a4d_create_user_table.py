"""Create user table

Revision ID: 889649e92a4d
Revises: d50e999d2a17
Create Date: 2023-08-26 17:45:01.133225

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '889649e92a4d'
down_revision: Union[str, None] = 'd50e999d2a17'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("users",  
        sa.Column("id", sa.Integer, primary_key=True, nullable=False, autoincrement=True),
        sa.Column("email", sa.String, nullable=False, unique=True),
        sa.Column("password", sa.String, nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()"))
    )

def downgrade() -> None:
    op.drop_table("users")
    pass
