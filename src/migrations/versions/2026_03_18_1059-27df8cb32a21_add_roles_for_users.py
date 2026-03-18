"""add roles for users

Revision ID: 27df8cb32a21
Revises: c89fe2b6f11f
Create Date: 2026-03-18 10:59:14.739095

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '27df8cb32a21'
down_revision: Union[str, Sequence[str], None] = 'c89fe2b6f11f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


user_role_enum = sa.Enum('ADMIN', 'HOTEL_OWNER', 'USER', name='userrole')


def upgrade() -> None:
    """Upgrade schema."""
    user_role_enum.create(op.get_bind())
    op.add_column(
        'users',
        sa.Column(
            'role',
            sa.Enum('ADMIN', 'HOTEL_OWNER', 'USER', name='userrole'),
            nullable=False,
            server_default='USER',
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'role')
    user_role_enum.drop(op.get_bind())
