from aiohttp import web
from aiohttp_session import get_session

from ai.backend.client.session import AsyncSession as APISession
from ai.backend.client.config import APIConfig

from . import user_agent


async def get_api_session(request: web.Request) -> APISession:
    config = request.app['config']
    session = await get_session(request)
    if not session.get('authenticated', False):
        raise web.HTTPUnauthorized()
    if 'token' not in session:
        raise web.HTTPUnauthorized()
    token = session['token']
    if token['type'] != 'keypair':
        raise web.HTTPInternalServerError(text='Incompatible auth token.')
    ak, sk = token['access_key'], token['secret_key']
    config = APIConfig(
        domain=config['api']['domain'],
        endpoint=config['api']['endpoint'],
        access_key=ak,
        secret_key=sk,
        user_agent=user_agent,
        skip_sslcert_validation=config['api'].get('ssl-verify', True),
    )
    return APISession(config=config)


async def get_anonymous_session(request: web.Request) -> APISession:
    config = request.app['config']
    config = APIConfig(
        domain=config['api']['domain'],
        endpoint=config['api']['endpoint'],
        access_key='',
        secret_key='',
        user_agent=user_agent,
        skip_sslcert_validation=config['api'].get('ssl-verify', True),
    )
    return APISession(config=config)
