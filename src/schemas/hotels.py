from pydantic import BaseModel, Field


class RequestHotelAdd(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    location: str = Field(min_length=5)
    stars: int = Field(gt=0, le=5)
    phone: int


class HotelAdd(RequestHotelAdd):
    owner_id: int


class Hotel(HotelAdd):
    id: int
    rating: float | None = Field(None, ge=0, le=5)


class HotelPatch(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=100)
    location: str | None = Field(None, min_length=5)
    stars: int | None = Field(None, gt=0, le=5)
    phone: int | None
