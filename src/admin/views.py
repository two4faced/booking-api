from starlette_admin.contrib.sqla import ModelView


class UsersView(ModelView):
    label = 'Users'

    fields = ['id', 'name', 'email', 'role']

    sortable_fields = ['id', 'email']
    searchable_fields = ['email', 'name']
    column_details_exclude_list = ['hashed_password']


class HotelsView(ModelView):
    label = 'Hotels'

    fields = ['id', 'title', 'location', 'stars', 'phone', 'rating', 'owner_id']

    searchable_fields = ['id', 'title', 'location', 'owner_id']
    sortable_fields = ['id', 'stars', 'rating']


class HotelsImagesView(ModelView):
    label = 'Hotel Images'

    fields = ['id', 'hotel_id', 'path']

    searchable_fields = ['path', 'hotel_id']


class RoomsView(ModelView):
    label = 'Rooms'

    fields = ['id', 'hotel_id', 'title', 'description', 'price', 'quantity', 'guests_count']

    searchable_fields = ['title', 'hotel_id']
    sortable_fields = ['id', 'hotel_id', 'title', 'price', 'quantity', 'guests_count']


class RoomsImagesView(ModelView):
    label = 'Room Images'

    fields = ['id', 'room_id', 'path']

    searchable_fields = ['path', 'room_id']
    sortable_fields = ['id', 'room_id']


class FacilitiesView(ModelView):
    label = 'Facilities'

    fields = ['id', 'title']

    searchable_fields = ['title']


class RoomFacilitiesView(ModelView):
    label = 'Room Facilities'

    fields = ['id', 'room_id', 'facility_id']

    searchable_fields = ['id', 'room_id', 'facility_id']


class BookingsView(ModelView):
    label = 'Bookings'

    fields = ['id', 'user_id', 'hotel_id', 'room_id', 'date_from', 'date_to', 'price']

    searchable_fields = ['user_id', 'hotel_id']
    sortable_fields = ['id', 'date_from', 'date_to', 'price']


class RatingsView(ModelView):
    label = 'Ratings'

    column_list = ['id', 'user_id', 'hotel_id', 'rating', 'rating_text']

    searchable_fields = ['id', 'rating_text']
    sortable_fields = ['id', 'user_id', 'hotel_id', 'rating']

