from pydantic import BaseModel


class HotelImageAdd(BaseModel):
    hotel_id: int
    path: str


class HotelImage(HotelImageAdd):
    id: int


class RoomImageAdd(BaseModel):
    room_id: int
    path: str


class RoomImage(RoomImageAdd):
    id: int
