from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.config.database import Base, engine
from app.models import book, book_copy, user, borrow_record
from app.api.book_routes import router as book_router
from app.api.users_api import router as user_router
from app.api.borrow_api import router as borrow_router
import logging

logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library Management System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred"}
    )

app.include_router(book_router)
app.include_router(user_router)
app.include_router(borrow_router)