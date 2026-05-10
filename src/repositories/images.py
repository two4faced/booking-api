from src.models.hotels import HotelsImagesORM
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import HotelsImagesDataMapper


class HotelsImagesRepository(BaseRepository):
    model = HotelsImagesORM
    mapper = HotelsImagesDataMapper
