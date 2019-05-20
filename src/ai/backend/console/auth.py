from aiohttp import web
from aiohttp_session import get_session

from ai.backend.client.session import AsyncSession as APISession
from ai.backend.client.config import APIConfig, get_config

from . import __version__


async def get_api_session(request: web.Request) -> web.Response:
    config = request.app['config']
    session = await get_session(request)
    authenticated = session.get('authenticated', False)
    # if not authenticated:
    #     return web.HTTPFound('/login')
    if 'access_key' not in session:
        pass
        # session['user_id']
        # session['password']
        # TODO: query the manager from user credential

    config = APIConfig(
        # TODO: add domain argument to client-py
        endpoint='http://localhost:8081',
        access_key='AKIAIOSFODNN7EXAMPLE',
        secret_key='wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
        user_agent=f'Backend.AI Console Server {__version__}',
    )
    return APISession(config=config)
