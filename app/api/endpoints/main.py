from typing import Annotated

from fastapi import FastAPI, Header

from app.core.config import load_config
from app.core.logger import logger
from app.api.schemas.models import User, UserResponse, Feedback, UserCreate

app = FastAPI()
config = load_config()

from app.api.endpoints import products, authentication

app.include_router(products.router)
app.include_router(authentication.router)

fake_users = {
    1: {"username": "john_doe", "email": "john@example.com"},
    2: {"username": "jane_smith", "email": "jane@example.com"}
}

feedback_list = []

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/custom")
def read_custom_message():
    return {"message": "This is a custom message!"}


@app.get("/db")
def get_db_info():
    logger.info(f"Connecting to database: {config.db.database_url}")
    return {"database_url": config.db.database_url}


@app.get('/users/{user_id}')
def get_user(user_id: int):
    if user_id in fake_users:
        return fake_users[user_id]
    return {'error': 'User not found'}


@app.post('/user')
async def create_user(user: User) -> UserResponse:
    return UserResponse(
        name=user.name,
        age=user.age,
        is_adult=user.age >= 18
    )


@app.delete('/users/{user_id}')
async def delete_user(user_id: int):
    return {"message": f"Пользователь с ID {user_id} был удален"}


@app.post('/feedback')
async def feedback_processing(feedback: Feedback, is_premium: bool = False):
    feedback_list.append(feedback)
    default_phrase = f'Спасибо, {feedback.name}! Ваш отзыв сохранён.'
    if is_premium:
        return f'{default_phrase} Ваш отзыв будет рассмотрен в приоритетном порядке.'
    else:
        return default_phrase


@app.post('/create_user', response_model=UserCreate)
async def create_user(user: UserCreate) -> UserCreate:
    return user


@app.get('/items/')
async def read_items(user_agent: Annotated[str | None, Header()] = None):
    return {'User-Agent': user_agent}