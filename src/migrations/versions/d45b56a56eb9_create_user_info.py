"""create_user_info

Revision ID: d45b56a56eb9
Revises:
Create Date: 2024-05-22 20:18:27.860144

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d45b56a56eb9"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "user_info",
        sa.Column("user_id", sa.Integer(), sa.Identity(), nullable=False),
        sa.Column("login_id", sa.VARCHAR(255), nullable=False),
        sa.Column("password", sa.VARCHAR(255), nullable=False),
        sa.Column("email", sa.VARCHAR(255), nullable=False),
        sa.Column("user_name", sa.VARCHAR(255), nullable=False),
        sa.Column("user_type", sa.SmallInteger, nullable=False, server_default="3"),
        sa.Column("status", sa.SmallInteger, nullable=False, server_default="1"),
        sa.Column("is_enable", sa.Integer(), server_default="1", nullable=False),
        sa.Column("reg_date", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.PrimaryKeyConstraint("user_id", name=op.f("user_info_pkey")),
    )

    op.create_index(
        "user_info_login_id_key",
        "user_info",
        ["login_id"],
        unique=True,
    )


def downgrade() -> None:
    pass
