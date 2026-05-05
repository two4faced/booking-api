"""add hotel_owner and phone for hotels

Revision ID: 9686d689b670
Revises: e06120bd604a
Create Date: 2026-05-05 11:38:52.202478

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9686d689b670'
down_revision: Union[str, Sequence[str], None] = 'e06120bd604a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('hotels', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.add_column('hotels', sa.Column('phone', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'hotels', 'users', ['owner_id'], ['id'], ondelete='CASCADE')


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, 'hotels', type_='foreignkey')
    op.drop_column('hotels', 'phone')
    op.drop_column('hotels', 'owner_id')
