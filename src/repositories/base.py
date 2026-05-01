import logging
from typing import Any

from asyncpg.exceptions import (
    UniqueViolationError,
    StringDataRightTruncationError,
    ForeignKeyViolationError,
)
from sqlalchemy.exc import NoResultFound, IntegrityError, DBAPIError
from pydantic import BaseModel
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import Base
from src.exceptions import (
    ObjectNotFoundException,
    ObjectAlreadyExistsException,
    IncorrectStringValueException,
    ObjectCantBeDeletedException,
)
from src.repositories.mappers.base import DataMapper


class BaseRepository:
    model: type[Base]
    mapper: type[DataMapper]
    session: AsyncSession

    def __init__(self, session):
        self.session = session

    async def get_all(self, *filter, **filter_by) -> list[BaseModel | Any]:
        query = select(self.model).filter(*filter).filter_by(**filter_by)
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(elem) for elem in result.scalars().all()]

    async def get_one_or_none(self, **filter_by) -> BaseModel | None | Any:
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        res = result.scalars().one_or_none()
        if res is None:
            return None
        else:
            return self.mapper.map_to_domain_entity(res)

    async def get_one(self, **filter_by) -> BaseModel:
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        try:
            res = result.scalar_one()
        except NoResultFound:
            raise ObjectNotFoundException
        return self.mapper.map_to_domain_entity(res)

    async def add(self, data: BaseModel) -> BaseModel | Any:
        try:
            add_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
            result = await self.session.execute(add_stmt)
            model = result.scalars().one()
            inserted_data = self.mapper.map_to_domain_entity(model)
        except IntegrityError as exc:
            logging.error(
                f'Не удалось добавить данные в базу, входные данные: {data}, тип ошибки: {exc.orig.__cause__}'
            )
            if isinstance(exc.orig.__cause__, UniqueViolationError):
                raise ObjectAlreadyExistsException from exc
            else:
                logging.error(
                    f'Незнакомая ошибка, входные данные: {data}, тип ошибки: {exc.orig.__cause__}'
                )
                raise exc
        except DBAPIError as exc:
            if isinstance(exc.orig.__cause__, StringDataRightTruncationError):
                raise IncorrectStringValueException from exc
            else:
                logging.error(
                    f'Незнакомая ошибка, входные данные: {data}, тип ошибки: {exc.orig.__cause__}'
                )
                raise exc

        return inserted_data

    async def add_batch(self, data: list[BaseModel]) -> None:
        try:
            add_data_stmt = insert(self.model).values([item.model_dump() for item in data])
            await self.session.execute(add_data_stmt)
        except IntegrityError as exc:
            logging.error(
                f'Не удалось добавить данные в базу, входные данные: {data}, тип ошибки: {exc.orig.__cause__}'
            )
            if isinstance(exc.orig.__cause__, ForeignKeyViolationError):
                raise ObjectNotFoundException from exc
            else:
                logging.error(
                    f'Незнакомая ошибка, входные данные: {data}, тип ошибки: {exc.orig.__cause__}'
                )
                raise exc

    async def delete(self, **filter_by) -> None:
        try:
            del_stmt = delete(self.model).filter_by(**filter_by)
            await self.session.execute(del_stmt)
        except IntegrityError as exc:
            if isinstance(exc.orig.__cause__, ForeignKeyViolationError):
                raise ObjectCantBeDeletedException
            else:
                logging.error(
                    f'Незнакомая ошибка, входные данные: {filter_by}, тип ошибки: {exc.orig.__cause__}'
                )
                raise exc

    async def edit(self, data: BaseModel, is_patch: bool = False, **filter_by) -> None:
        values_to_update = data.model_dump(exclude_unset=is_patch)

        filtered_values = {k: v for k, v in values_to_update.items() if v is not None}

        if not filtered_values:
            return

        update_stmt = update(self.model).filter_by(**filter_by).values(**filtered_values)
        await self.session.execute(update_stmt)
