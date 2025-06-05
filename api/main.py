import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi_pagination import add_pagination

from routers import router as student_router
from database import init_db, engine

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Приложение запускается…")
    await init_db()
    yield
    logger.info("Приложение завершает работу…")
    await engine.dispose()

app = FastAPI(
    title="Student Management API",
    description="API для управления учётом студентов",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(student_router, prefix="/api")
add_pagination(app)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
