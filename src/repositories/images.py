from src.models.hotels import HotelsImagesORM
from src.models.rooms import RoomsImagesORM
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import HotelsImagesDataMapper, RoomsImagesDataMapper


class HotelsImagesRepository(BaseRepository):
    model = HotelsImagesORM
    mapper = HotelsImagesDataMapper


class RoomsImagesRepository(BaseRepository):
    model = RoomsImagesORM
    mapper = RoomsImagesDataMapper
