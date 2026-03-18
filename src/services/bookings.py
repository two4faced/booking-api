from src.api.dependencies import UserIdDep
from src.exceptions import DateFromLaterThenOrEQDateToException
from src.schemas.bookings import BookingsAddRequest, BookingsAdd
from src.services.base import BaseService
from src.services.hotels import HotelsService
from src.services.rooms import RoomsService


class BookingsService(BaseService):
    async def get_bookings(self):
        return await self.db.bookings.get_all()

    async def get_my_bookings(self, user_id: UserIdDep):
        return await self.db.bookings.get_all(user_id=user_id)

    async def book_room(self, user_id: UserIdDep, booking_data: BookingsAddRequest):
        await HotelsService(self.db).check_hotel_existence(booking_data.hotel_id)
        await RoomsService(self.db).check_room_existence(booking_data.room_id)

        if booking_data.date_to <= booking_data.date_from:
            raise DateFromLaterThenOrEQDateToException

        room = await self.db.rooms.get_one(id=booking_data.room_id)
        hotel = await self.db.hotels.get_one(id=room.hotel_id)
        price = room.price * (booking_data.date_to - booking_data.date_from).days

        _booking_data = BookingsAdd(
            user_id=user_id,
            price=price,
            **booking_data.model_dump(),
        )
        booking = await self.db.bookings.add_booking(_booking_data, hotel_id=hotel.id)

        await self.db.commit()
        return booking
