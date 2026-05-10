from pydantic import BaseModel


class HotelImageAdd(BaseModel):
    hotel_id: int
    path: str


class HotelImage(HotelImageAdd):
    id: int
