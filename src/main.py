from contextlib import asynccontextmanager
import sys
import logging
from pathlib import Path

from src.admin.admin import setup_admin
from src.api.hotels import router as router_hotels
from src.api.auth import router as router_auth
from src.api.rooms import router as router_rooms
from src.api.bookings import router as router_bookings
from src.api.facilities import router as router_facilities
from src.api.images import router as router_images
from src.api.ratings import router as router_ratings
from src.config import settings


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from starlette.middleware.sessions import SessionMiddleware
import uvicorn

from src.setup import redis_manager

sys.path.append(str(Path(__file__).parent.parent))

logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_manager.connect()
    FastAPICache.init(RedisBackend(redis_manager.redis), prefix='fastapi-cache')
    logging.info('FastAPICache инициализирован')
    yield
    await redis_manager.close()


app = FastAPI(lifespan=lifespan)

setup_admin(app)

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.JWT_SECRET_KEY,
    same_site='lax',
    https_only=False,
)


app.include_router(router_auth)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_bookings)
app.include_router(router_facilities)
app.include_router(router_ratings)
app.include_router(router_images)


from fastapi.staticfiles import StaticFiles

app.mount('/static', StaticFiles(directory='src/static'), name='static')


app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000', 'http://localhost:5173', 'http://127.0.0.1:5173'],
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'],
    allow_headers=['*'],
    expose_headers=['*'],
)

if __name__ == '__main__':
    uvicorn.run('__main__:app', reload=True)
