"""add hotels_images table

Revision ID: 3d4a4a0db38e
Revises: 88e78301332a
Create Date: 2026-05-07 10:15:43.099484

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3d4a4a0db38e'
down_revision: Union[str, Sequence[str], None] = '88e78301332a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'hotels_images',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('hotel_id', sa.Integer(), nullable=False),
        sa.Column('path', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ['hotel_id'],
            ['hotels.id'],
        ),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('hotels_images')
