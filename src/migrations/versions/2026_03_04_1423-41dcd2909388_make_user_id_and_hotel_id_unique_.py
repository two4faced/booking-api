"""make user id and hotel id unique constraint in ratings

Revision ID: 41dcd2909388
Revises: 5c270dfdb28c
Create Date: 2026-03-04 14:23:02.011844

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '41dcd2909388'
down_revision: Union[str, Sequence[str], None] = '5c270dfdb28c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint('_user_hotel_ids_uc', 'ratings', ['user_id', 'hotel_id'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('_user_hotel_ids_uc', 'ratings', type_='unique')
