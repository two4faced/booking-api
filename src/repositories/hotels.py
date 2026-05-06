from sqlalchemy import select, update, func

from src.exceptions import DateFromLaterThenOrEQDateToException
from src.models.hotels import HotelsORM
from src.models.rooms import RoomsORM
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import HotelDataMapper
from src.repositories.utils import rooms_ids_for_booking, get_average_rating


class HotelsRepository(BaseRepository):
    model = HotelsORM
    mapper = HotelDataMapper

    async def get_filtered_by_time(
        self,
        date_from,
        date_to,
        location,
        title,
        offset,
        limit,
        guests_count: int | None = None,
        min_price: int | None = None,
        max_price: int | None = None,
        sort_by: str | None = 'price_asc',
    ):
        if date_to <= date_from:
            raise DateFromLaterThenOrEQDateToException

        rooms_ids_to_get = rooms_ids_for_booking(
            date_from=date_from,
            date_to=date_to,
            guests_count=guests_count,
        )

        hotels_ids = (
            select(RoomsORM.hotel_id, func.min(RoomsORM.price).label('min_price'))
            .select_from(RoomsORM)
            .filter(RoomsORM.id.in_(rooms_ids_to_get))
            .group_by(RoomsORM.hotel_id)
            .subquery()
        )

        query = select(HotelsORM).join(hotels_ids, HotelsORM.id == hotels_ids.c.hotel_id)

        if sort_by == 'price_desc':
            query = query.order_by(hotels_ids.c.min_price.desc())

        elif sort_by == 'rating_desc':
            query = query.order_by(HotelsORM.rating.desc())

        elif sort_by == 'rating_asc':
            query = query.order_by(HotelsORM.rating.asc())

        else:
            query = query.order_by(hotels_ids.c.min_price.asc())

        if min_price is not None:
            query = query.filter(hotels_ids.c.min_price >= min_price)

        if max_price is not None:
            query = query.filter(hotels_ids.c.min_price <= max_price)

        if location:
            query = query.filter(HotelsORM.location.icontains(location.strip()))
        if title:
            query = query.filter(HotelsORM.title.icontains(title.strip()))

        query = query.limit(limit).offset(offset)
        result = await self.session.execute(query)

        return [self.mapper.map_to_domain_entity(hotel) for hotel in result.scalars().all()]

    async def change_rating(self, hotel_id: int):
        avg_rating = get_average_rating(hotel_id=hotel_id)

        result = await self.session.execute(avg_rating)
        new_rating = result.scalars().one_or_none() or 0.0

        update_stmt = update(HotelsORM).where(HotelsORM.id == hotel_id).values(rating=new_rating)

        await self.session.execute(update_stmt)
