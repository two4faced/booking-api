"""add cascade

Revision ID: e06120bd604a
Revises: 27df8cb32a21
Create Date: 2026-04-25 19:03:01.917023

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'e06120bd604a'
down_revision: Union[str, Sequence[str], None] = '27df8cb32a21'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint(op.f('bookings_hotel_id_fkey'), 'bookings', type_='foreignkey')
    op.drop_constraint(op.f('bookings_room_id_fkey'), 'bookings', type_='foreignkey')
    op.drop_constraint(op.f('bookings_user_id_fkey'), 'bookings', type_='foreignkey')
    op.create_foreign_key(None, 'bookings', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'bookings', 'rooms', ['room_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'bookings', 'hotels', ['hotel_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint(op.f('ratings_user_id_fkey'), 'ratings', type_='foreignkey')
    op.drop_constraint(op.f('ratings_hotel_id_fkey'), 'ratings', type_='foreignkey')
    op.create_foreign_key(None, 'ratings', 'hotels', ['hotel_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'ratings', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint(op.f('room_facilities_room_id_fkey'), 'room_facilities', type_='foreignkey')
    op.drop_constraint(
        op.f('room_facilities_facility_id_fkey'), 'room_facilities', type_='foreignkey'
    )
    op.create_foreign_key(None, 'room_facilities', 'rooms', ['room_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(
        None,
        'room_facilities',
        'facilities',
        ['facility_id'],
        ['id'],
        ondelete='CASCADE',
    )
    op.drop_constraint(op.f('rooms_hotel_id_fkey'), 'rooms', type_='foreignkey')
    op.create_foreign_key(None, 'rooms', 'hotels', ['hotel_id'], ['id'], ondelete='CASCADE')


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, 'rooms', type_='foreignkey')
    op.create_foreign_key(op.f('rooms_hotel_id_fkey'), 'rooms', 'hotels', ['hotel_id'], ['id'])
    op.drop_constraint(None, 'room_facilities', type_='foreignkey')
    op.drop_constraint(None, 'room_facilities', type_='foreignkey')
    op.create_foreign_key(
        op.f('room_facilities_facility_id_fkey'),
        'room_facilities',
        'facilities',
        ['facility_id'],
        ['id'],
    )
    op.create_foreign_key(
        op.f('room_facilities_room_id_fkey'),
        'room_facilities',
        'rooms',
        ['room_id'],
        ['id'],
    )
    op.drop_constraint(None, 'ratings', type_='foreignkey')
    op.drop_constraint(None, 'ratings', type_='foreignkey')
    op.create_foreign_key(op.f('ratings_hotel_id_fkey'), 'ratings', 'hotels', ['hotel_id'], ['id'])
    op.create_foreign_key(op.f('ratings_user_id_fkey'), 'ratings', 'users', ['user_id'], ['id'])
    op.drop_constraint(None, 'bookings', type_='foreignkey')
    op.drop_constraint(None, 'bookings', type_='foreignkey')
    op.drop_constraint(None, 'bookings', type_='foreignkey')
    op.create_foreign_key(op.f('bookings_user_id_fkey'), 'bookings', 'users', ['user_id'], ['id'])
    op.create_foreign_key(op.f('bookings_room_id_fkey'), 'bookings', 'rooms', ['room_id'], ['id'])
    op.create_foreign_key(
        op.f('bookings_hotel_id_fkey'), 'bookings', 'hotels', ['hotel_id'], ['id']
    )
