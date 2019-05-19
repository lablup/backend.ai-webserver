import asyncio
import logging
import logging.config
import os
import sys
import time
from types import SimpleNamespace

from aiohttp import web
import aiohttp_cors
from aiohttp_session import get_session, setup as setup_session
from aiohttp_session.redis_storage import RedisStorage
import aiotools
import aioredis
import click
from setproctitle import setproctitle
import uvloop

from . import __version__
from .logging import BraceStyleAdapter

log = BraceStyleAdapter(logging.getLogger('ai.backend.console.server'))


async def hello(request: web.Request) -> web.Response:
    session = await get_session(request)
    if 'first_visit' not in session:
        session['first_visit'] = time.time()
    return web.Response(body=f"OK (your first visit: {session['first_visit']}")


@aiotools.server
async def server_main(loop, pidx, args):
    app = web.Application()
    app['config'] = args[0]
    app['redis'] = await aioredis.create_pool(
        (app['config'].redis_host, app['config'].redis_port))
    setup_session(app, RedisStorage(app['redis']))
    app.router.add_route('GET', '/', hello)

    # app.on_shutdown.append(gw_shutdown)
    # app.on_cleanup.append(gw_cleanup)

    cors_options = {
        '*': aiohttp_cors.ResourceOptions(
            allow_credentials=False,
            expose_headers="*", allow_headers="*"),
    }
    cors = aiohttp_cors.setup(app, defaults=cors_options)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(
        runner,
        str(app['config'].service_ip),
        app['config'].service_port,
        backlog=1024,
        reuse_port=True,
        # ssl_context=app['sslctx'],
    )
    await site.start()
    log.info('started.')

    try:
        yield
    finally:
        log.info('shutting down...')
        await runner.cleanup()


@click.command()
@click.argument('service_ip')
@click.argument('service_port')
@click.option('--redis-host', default='localhost',
              help='The hostname of a Redis server used for session storage.')
@click.option('--redis-port', type=int, default=6379,
              help='The port number of the Redis server.')
def main(service_ip, service_port, redis_host, redis_port):
    setproctitle(f'backend.ai: console-server '
                 f'{service_ip}:{service_port}')
    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'colored': {
                '()': 'coloredlogs.ColoredFormatter',
                'format': '%(asctime)s %(levelname)s %(name)s '
                          '[%(process)d] %(message)s',
                'field_styles': {'levelname': {'color': 248, 'bold': True},
                                 'name': {'color': 246, 'bold': False},
                                 'process': {'color': 'cyan'},
                                 'asctime': {'color': 240}},
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'DEBUG',
                'formatter': 'colored',
                'stream': 'ext://sys.stderr',
            },
            'null': {
                'class': 'logging.NullHandler',
            },
        },
        'loggers': {
            '': {
                'handlers': ['console'],
                'level': 'INFO',
            },
        },
    })
    log.info('Backend.AI Console Server {0}', __version__)
    log.info('runtime: {0}', sys.prefix)
    log_config = logging.getLogger('ai.backend.console.config')
    log_config.debug('debug mode enabled.')
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    
    config = SimpleNamespace()
    config.service_ip = service_ip
    config.service_port = service_port
    config.redis_host = redis_host
    config.redis_port = redis_port
    try:
        aiotools.start_server(
            server_main,
            num_workers=min(4, os.cpu_count()),
            args=(config,),
        )
    finally:
        log.info('terminated.')


if __name__ == '__main__':
    main()
