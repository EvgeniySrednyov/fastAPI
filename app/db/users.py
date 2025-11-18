from app.api.schemas.authentication import UserLogin


### имитируем хранилище юзеров

# создали тестового юзера, якобы он уже зарегистрирован у нас
sample_user: dict = {"username": "user123", "password": "password123"}

# имитируем базу данных
fake_db: list[UserLogin] = [UserLogin(**sample_user)]

# имитируем хранилище сессий
session: dict = {}

# session: dict = {"0d6f089c-3b77-42d5-9046-cc10903c3539": {
#             "username": "user123",
#             "password": "password123"
#         }}

# token = '0d6f089c-3b77-42d5-9046-cc10903c3539'
# print(fake_db)
# print(UserLogin(**session[token]))