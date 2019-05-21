import json

from aiohttp import web
from aiohttp_session import get_session

from ai.backend.client.session import AsyncSession as APISession
from ai.backend.client.config import APIConfig

from . import __version__


async def get_api_session(request: web.Request) -> APISession:
    config = request.app['config']
    session = await get_session(request)
    if 'token' not in session:
        raise web.HTTPUnauthorized()
    token = json.loads(session['token'])
    if token['type'] != 'keypair':
        raise web.HTTPInternalServerError(text='Incompatible auth token.')
    ak, sk = token['content'].split(':', maxsplit=1)
    config = APIConfig(
        domain=config['api']['domain'],
        endpoint=config['api']['endpoint'],
        access_key=ak,
        secret_key=sk,
        user_agent=f'Backend.AI Console Server {__version__}',
    )
    return APISession(config=config)
