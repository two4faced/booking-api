"""add rooms_images table

Revision ID: ec4062900ea6
Revises: 3d4a4a0db38e
Create Date: 2026-05-12 11:48:31.625052

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ec4062900ea6'
down_revision: Union[str, Sequence[str], None] = '3d4a4a0db38e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'rooms_images',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('room_id', sa.Integer(), nullable=False),
        sa.Column('path', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ['room_id'],
            ['rooms.id'],
        ),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('rooms_images')
