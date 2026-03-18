"""add hotel id for bookings

Revision ID: c89fe2b6f11f
Revises: 41dcd2909388
Create Date: 2026-03-14 13:15:56.476863

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c89fe2b6f11f'
down_revision: Union[str, Sequence[str], None] = '41dcd2909388'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('bookings', sa.Column('hotel_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'bookings', 'hotels', ['hotel_id'], ['id'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, 'bookings', type_='foreignkey')
    op.drop_column('bookings', 'hotel_id')
