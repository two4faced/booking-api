from fastapi import HTTPException


class BookingException(Exception):
    detail = 'Непредвиденная ошибка'

    def __init__(self, *args):
        super().__init__(self.detail, *args)


class IncorrectStringValueException(BookingException):
    detail = 'Неверное значение строки'


class ObjectNotFoundException(BookingException):
    detail = 'Объект не найден'


class HotelNotFoundException(ObjectNotFoundException):
    detail = 'Отель не найден'


class RoomNotFoundException(ObjectNotFoundException):
    detail = 'Номер не найден'


class UserNotFoundException(ObjectNotFoundException):
    detail = 'Пользователь не найден'


class ObjectAlreadyExistsException(BookingException):
    detail = 'Объект уже существует'


class AllRoomsBookedException(BookingException):
    detail = 'Не осталось свободных номеров'


class DateFromLaterThenOrEQDateToException(BookingException):
    detail = 'Дата заезда позже или равна дате выезда'


class WrongPassOrEmailException(BookingException):
    detail = 'Имя пользователя или пароль неверные'


class NothingChangedException(BookingException):
    detail = 'Ничего не было изменено'


class ObjectBookedException(BookingException):
    detail = 'Объект забронирован и не может быть удален'


class ObjectCantBeDeletedException(BookingException):
    detail = 'Объект не может быть удалён'


class BookingHTTPException(HTTPException):
    status_code = 500
    detail = 'Непредвиденная ошибка'

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class HotelNotFoundHTTPException(BookingHTTPException):
    status_code = 404
    detail = 'Данный отель не найден'


class HotelAlreadyExistsHTTPException(BookingHTTPException):
    status_code = 400
    detail = 'Данный отель уже существует'


class RoomNotFoundHTTPException(BookingHTTPException):
    status_code = 404
    detail = 'Данный номер не найден'


class UserNotFoundHTTPException(BookingHTTPException):
    status_code = 401
    detail = 'Пользователь не найден'


class FacilitiesNotFoundHTTTPException(BookingHTTPException):
    status_code = 400
    detail = 'Добавленные удобства не найдены'


class WrongPassOrEmailHTTPException(BookingHTTPException):
    status_code = 401
    detail = 'Пользователь не найден'


class AllRoomsBookedHTTPException(BookingHTTPException):
    status_code = 409
    detail = 'Не осталось свободных номеров'


class StringIsToLongHTTPException(BookingHTTPException):
    status_code = 400
    detail = 'Длина строки превышает допустимый лимит'


class NotAuthenticatedHTTPException(BookingHTTPException):
    status_code = 401
    detail = 'Вы не аутентифицированы'


class FacilityAlreadyExists(BookingHTTPException):
    status_code = 400
    detail = 'Данное удобство уже существует'


class NothingChangedHTTPException(BookingHTTPException):
    status_code = 400
    detail = 'Ничего не было изменено'


class HotelBookedHTTPException(BookingHTTPException):
    status_code = 409
    detail = 'Отель забронирован и не может быть удален'


class RoomBookedHTTPException(BookingHTTPException):
    status_code = 409
    detail = 'Номер забронирован и не может быть удален'


class RatingIsAlreadyPostedHTTPException(BookingHTTPException):
    status_code = 409
    detail = 'Вы уже оставляли отзыв для этого отеля'


class NotEnoughPermissionsHTTPException(BookingHTTPException):
    status_code = 403
    detail = 'Недостаточно прав доступа'
