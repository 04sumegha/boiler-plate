from fastapi import FastAPI
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from config.database import Base, engine
from urls.auth import router as auth_route
from urls.item import router as item_route
from middleware import auth_middleware
from utils.cache import cache_manager

load_dotenv()

Base.metadata.create_all(bind = engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await cache_manager.initialize()
    yield
    cache_manager.redis.close()

app = FastAPI(lifespan = lifespan)

app.middleware("http")(auth_middleware)

app.include_router(auth_route)
app.include_router(item_route)


@app.get("/")
def read_root():
    return {"message": "Boilerplate is running"}