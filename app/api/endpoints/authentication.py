from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Request, Response, Cookie, Header, HTTPException
from uuid import uuid4

from fastapi.params import Depends

from app.api.schemas.authentication import UserLogin, CommonHeaders
from app.db.users import fake_db, session

router = APIRouter(prefix='', tags=['auth'])


@router.post('/login')
async def login(user: UserLogin, response: Response):
    for person in fake_db:
        if person.username == user.username and person.password == user.password:
            session_token = 'abc123xyz456'
            session[session_token] = user
            response.set_cookie(key='session_token', value=session_token, httponly=True)
            return {'message': 'Cookie installed'}
        return {'message': 'Invalid username or password'}


@router.get('/user')
async def get_user(session_token = Cookie()):
    user = session.get(session_token)
    if user:
        # return user.dict()
        return UserLogin(**user.dict())
    return {'message': 'Unauthorized'}


# @router.get('/headers')  ### тоже рабочий вариант и хорош!
# async def get_headers(
#         user_agent: Annotated[str | None, Header()] = None,
#         accept_language: Annotated[str | None, Header()] = None
# ):
#     if not user_agent or not accept_language:
#         raise HTTPException(status_code=400, detail='no headers!')
#     return {'User-Agent': user_agent, 'Accept-Language': accept_language}

# @router.get('/headers')
# async def get_headers(request: Request):
#     user_agent = request.headers.get('User-Agent')
#     accept_language = request.headers.get('Accept-Language')
#
#     if not user_agent or not accept_language:
#         raise HTTPException(status_code=400, detail='no headers!')
#     return {'User-Agent': user_agent, 'Accept-Language': accept_language}

@router.get('/headers')
async def get_headers(headers: CommonHeaders = Depends(CommonHeaders.from_headers)):
    # return {
    #     'User-Agent': headers.user_agent,
    #     'Accept-Language': headers.accept_language,
    #     'X-Current-Version': headers.x_current_version
    # }
    return headers.model_dump(by_alias=True)
#
#
# @router.get('/info')
# async def get_info(headers: CommonHeaders = Depends(CommonHeaders.from_headers)):
#     return {
#         'message': 'Добро пожаловать! Ваши заголовки успешно обработаны.',
#         'headers': {
#             'User-Agent': headers.user_agent,
#             'Accept-Language': headers.accept_language,
#             'X-Server-Time': datetime.now().isoformat()
#     }
# }

