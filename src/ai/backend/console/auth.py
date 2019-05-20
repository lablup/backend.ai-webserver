from aiohttp import web


async def get_api_session(request: web.Request) -> web.Response:
    config = request.app['config']
    session = await get_session(request)
    authenticated = session.get('authenticated', False)
    if not authenticated:
        return web.HTTPFound('/login')
    if 'access_key' not in session:
        session['user_id']
        session['password']
        # TODO: get API keypair from user credential

    # config = Config()
    # api_session = APISession(config)
    # return api_session
    return None
