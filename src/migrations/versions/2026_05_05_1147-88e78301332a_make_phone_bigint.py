"""make phone bigint

Revision ID: 88e78301332a
Revises: 9686d689b670
Create Date: 2026-05-05 11:47:20.791461

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '88e78301332a'
down_revision: Union[str, Sequence[str], None] = '9686d689b670'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        'hotels',
        'phone',
        existing_type=sa.INTEGER(),
        type_=sa.BIGINT(),
        existing_nullable=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        'hotels',
        'phone',
        existing_type=sa.BIGINT(),
        type_=sa.INTEGER(),
        existing_nullable=False,
    )
