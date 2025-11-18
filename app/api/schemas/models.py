import pymorphy3
from pydantic import BaseModel, field_validator, Field, EmailStr

morph = pymorphy3.MorphAnalyzer()


class User(BaseModel):
    name: str
    age: int


class UserResponse(User):
    is_adult: bool


bad_words = ['редиска', 'бяка', 'козявка']


class Contact(BaseModel):
    email: EmailStr
    phone: int | None = Field(None, ge=1000000, le=999999999999999, strict=True)


class Feedback(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    message: str = Field(min_length=10, max_length=500)
    contact: Contact

    @field_validator('message')
    def check_message(cls, value):
        words_in_phrase = value.lower().split()
        for word in words_in_phrase:
            parsed = morph.parse(word)[0]
            if parsed.normal_form in bad_words:
                raise ValueError('Использование недопустимых слов')
        return value


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: int = Field(None, ge=1)
    is_subscribed: bool = None

# x = UserCreate(name='wdsw', email='wdsw@ed.ed', is_subscription=True)
# print(x)