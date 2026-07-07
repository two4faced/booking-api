import os
import shutil
from pathlib import Path

from fastapi import UploadFile

from src.exceptions import WrongExtensionException
from src.schemas.images import HotelImageAdd, RoomImageAdd
from src.services.base import BaseService
from src.services.hotels import HotelsService


class ImagesService(BaseService):
    async def add_hotel_image(self, file: UploadFile, hotel_id: int):
        directory = Path(f'src/static/images/{hotel_id}')
        directory.mkdir(parents=True, exist_ok=True)
        image_path = directory / file.filename

        with open(image_path, 'wb+') as new_file:
            self.check_extension(file)
            shutil.copyfileobj(file.file, new_file)

        new_image = HotelImageAdd(hotel_id=hotel_id, path=str(image_path))
        await self.db.hotels_images.add(new_image)
        await self.db.commit()

    async def get_all_hotel_images(self, hotel_id: int):
        return await self.db.hotels_images.get_all(hotel_id=hotel_id)

    async def add_room_image(self, file: UploadFile, hotel_id: int, room_id: int):
        directory = Path(f'src/static/images/{hotel_id}/{room_id}')
        os.makedirs(directory, exist_ok=True)
        image_path = directory / file.filename

        self.check_extension(file)

        with open(image_path, 'wb+') as new_file:
            shutil.copyfileobj(file.file, new_file)

        new_image = RoomImageAdd(room_id=room_id, path=str(image_path))
        await self.db.rooms_images.add(new_image)
        await self.db.commit()

    async def get_all_room_images(self, room_id: int):
        return await self.db.rooms_images.get_all(room_id=room_id)

    @staticmethod
    def check_extension(file: UploadFile):
        allowed_extensions = {'.jpg', '.jpeg', '.png', '.webp'}
        file_extension = Path(file.filename).suffix.lower()
        if file_extension not in allowed_extensions:
            raise WrongExtensionException
