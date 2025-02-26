"""Added Roles

Revision ID: 8815e40ed712
Revises: 14c6d9977ed7
Create Date: 2025-02-25 15:24:37.723048

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8815e40ed712'
down_revision: Union[str, None] = '14c6d9977ed7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# Define the ENUM type
user_role_enum = sa.Enum("admin", "user", "author", "guest", name="user_role_enum")

def upgrade():
    # Create the ENUM type in PostgreSQL
    op.execute("CREATE TYPE user_role_enum AS ENUM ('admin', 'user', 'author', 'guest');")

    # Add the column after ensuring the ENUM type exists
    op.add_column("users", sa.Column("role", user_role_enum, nullable=False, server_default="guest"))

def downgrade():
    # Drop the column
    op.drop_column("users", "role")

    # Drop the ENUM type (only if no other table is using it)
    op.execute("DROP TYPE IF EXISTS user_role_enum;")
