from fastapi import APIRouter

from src.api.dependencies import UserIdDep, DBDep
from src.exceptions import (
    HotelNotFoundException,
    HotelNotFoundHTTPException,
    IncorrectStringValueException,
    StringIsToLongHTTPException,
    ObjectAlreadyExistsException,
    RatingIsAlreadyPostedHTTPException,
    NothingChangedHTTPException,
    NothingChangedException,
)
from src.schemas.ratings import RatingRequestAdd, RatingPatch
from src.services.ratings import RatingService

router = APIRouter(prefix='/ratings', tags=['Отзывы'])


@router.get('/{hotel_id}')
async def get_ratings(hotel_id: int, db: DBDep):
    return await RatingService(db).get_ratings(hotel_id)


@router.post('/{hotel_id}')
async def add_rating(data: RatingRequestAdd, hotel_id: int, user_id: UserIdDep, db: DBDep):
    try:
        rating = await RatingService(db).add_rating(data, hotel_id, user_id)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except IncorrectStringValueException:
        raise StringIsToLongHTTPException
    except ObjectAlreadyExistsException:
        raise RatingIsAlreadyPostedHTTPException

    return rating


@router.patch('/{hotel_id}')
async def patch_rating(data: RatingPatch, hotel_id: int, user_id: UserIdDep, db: DBDep):
    try:
        await RatingService(db).patch_rating(rating_data=data, hotel_id=hotel_id, user_id=user_id)
    except NothingChangedException:
        raise NothingChangedHTTPException

    return {'status': 'OK'}
