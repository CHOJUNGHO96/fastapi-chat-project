"""create_friendship

Revision ID: 80bafa332979
Revises: d45b56a56eb9
Create Date: 2024-05-22 20:53:48.618183

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "80bafa332979"
down_revision: Union[str, None] = "d45b56a56eb9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "friendship",
        sa.Column("friendship_id", sa.Integer(), sa.Identity(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("friend_id", sa.Integer(), nullable=False),
        sa.Column("reg_date", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.PrimaryKeyConstraint("friendship_id", name=op.f("friendship_pkey")),
    )

    op.create_index(
        "friendship_user_id_key",
        "friendship",
        ["user_id"],
        unique=True,
    )

    op.create_index(
        "friendship_friend_id_key",
        "friendship",
        ["friend_id"],
        unique=True,
    )


def downgrade() -> None:
    pass
