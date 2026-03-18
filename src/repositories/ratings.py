import logging
from typing import Any

from asyncpg import StringDataRightTruncationError, UniqueViolationError
from pydantic import BaseModel
from sqlalchemy import select, insert
from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.orm import joinedload

from src.exceptions import IncorrectStringValueException, ObjectAlreadyExistsException
from src.models import RatingsORM
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import RatingsDataMapper
from src.schemas.ratings import Rating


class RatingsRepository(BaseRepository):
    model = RatingsORM
    mapper = RatingsDataMapper

    async def get_all(self, *filter, **filter_by) -> list[Rating]:
        query = (
            select(self.model)
            .options(joinedload(self.model.user))
            .filter(*filter)
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(elem) for elem in result.scalars().unique().all()]

    async def add(self, data: BaseModel) -> BaseModel | Any:
        try:
            add_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
            result = await self.session.execute(add_stmt)
            inserted_model = result.scalar_one()

            stmt = (
                select(self.model)
                .options(joinedload(self.model.user))
                .filter_by(id=inserted_model.id)
            )
            final_result = await self.session.execute(stmt)
            model_with_user = final_result.scalar_one()

            return self.mapper.map_to_domain_entity(model_with_user)
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
