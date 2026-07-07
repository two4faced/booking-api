from fastapi import FastAPI
from starlette_admin.contrib.sqla import Admin

from src.admin.views import UsersView, HotelsView, RoomsView, BookingsView, RatingsView, FacilitiesView, \
    RoomFacilitiesView, RoomsImagesView, HotelsImagesView
from src.database import engine
from src.models import UsersORM, HotelsORM, RoomsORM, BookingsORM, RatingsORM, FacilitiesORM, RoomFacilitiesORM
from src.models.hotels import HotelsImagesORM
from src.models.rooms import RoomsImagesORM


def setup_admin(app: FastAPI):
    admin = Admin(engine)

    admin.add_view(UsersView(UsersORM))
    admin.add_view(HotelsView(HotelsORM))
    admin.add_view(RoomsView(RoomsORM))
    admin.add_view(BookingsView(BookingsORM))
    admin.add_view(RatingsView(RatingsORM))
    admin.add_view(FacilitiesView(FacilitiesORM))
    admin.add_view(RoomFacilitiesView(RoomFacilitiesORM))
    admin.add_view(RoomsImagesView(RoomsImagesORM))
    admin.add_view(HotelsImagesView(HotelsImagesORM))

    admin.mount_to(app)