import asyncio
import logging
import logging.config
import os
from pathlib import Path
import sys
import time
from types import SimpleNamespace
import pkg_resources

from aiohttp import web
import aiohttp_cors
from aiohttp_session import get_session, setup as setup_session
from aiohttp_session.redis_storage import RedisStorage
import aiotools
import aioredis
import click
import jinja2
from setproctitle import setproctitle
import toml
import uvloop

from . import __version__
from .logging import BraceStyleAdapter
from .proxy import web_handler, websocket_handler

log = BraceStyleAdapter(logging.getLogger('ai.backend.console.server'))

static_path = Path(pkg_resources.resource_filename('ai.backend.console', 'static')).resolve()
assert static_path.is_dir()


console_config_template = jinja2.Template('''[general]
apiEndpoint = {{endpoint_url}}
apiEndpointText = {{endpoint_text}}
defaultSessionEnvironment =
siteDescription = {{site_description}}

[wsproxy]
proxyURL = {{proxy_url}}/
proxyBaseURL =
proxyListenIP =
''')


async def console_handler(request: web.Request) -> web.Response:
    request_path = request.match_info['path']
    config = request.app['config']

    if request_path == 'config.ini':
        config_content = console_config_template.render(**{
            'endpoint_url': f'{request.scheme}://{request.host}/func',  # must be absolute
            'endpoint_text': config['api']['text'],
            'site_description': config['ui']['brand'],
            'proxy_url': config['service']['wsproxy']['url'],
        })
        return web.Response(text=config_content)

    file_path = (static_path / request_path).resolve()
    # SECURITY: only allow reading files under static_path
    try:
        file_path.relative_to(static_path)
    except (ValueError, FileNotFoundError):
        return web.HTTPNotFound()
    if file_path.is_file():
        return web.FileResponse(file_path)

    return web.FileResponse(static_path / 'index.html')


async def login_handler(request: web.Request) -> web.Response:
    session = await get_session(request)
    if session['authenticated']:
        return web.HTTPInvalidRequest('You have already logged in.')
    creds = await request.json()
    # TODO: implement
    session['authenticated'] = True
    return web.Response(text='not implemented yet')


async def server_shutdown(app):
    pass


async def server_cleanup(app):
    app['redis'].close()
    await app['redis'].wait_closed()


@aiotools.server
async def server_main(loop, pidx, args):
    config = args[0]
    app = web.Application()
    app['config'] = config
    app['redis'] = await aioredis.create_pool(
        (config['session']['redis']['host'],
         config['session']['redis']['port']),
        db=config['session']['redis'].get('db', 0),
        password=config['session']['redis'].get('password', None))

    if pidx == 0 and config['session'].get('flush_on_startup', False):
        await app['redis'].execute('flushdb')
        log.info('flushed session storage.')
    redis_storage = RedisStorage(
        app['redis'],
        max_age=config['session']['max_age'])

    setup_session(app, redis_storage)
    cors_options = {
        '*': aiohttp_cors.ResourceOptions(
            allow_credentials=False,
            expose_headers="*", allow_headers="*"),
    }
    cors = aiohttp_cors.setup(app, defaults=cors_options)

    cors.add(app.router.add_route('POST', '/server/login', login_handler))
    cors.add(app.router.add_route('GET', '/func/{path:stream/.*$}', websocket_handler))
    cors.add(app.router.add_route('GET', '/func/{path:.*$}', web_handler))
    cors.add(app.router.add_route('POST', '/func/{path:.*$}', web_handler))
    cors.add(app.router.add_route('PATCH', '/func/{path:.*$}', web_handler))
    cors.add(app.router.add_route('DELETE', '/func/{path:.*$}', web_handler))
    cors.add(app.router.add_route('GET', '/{path:.*$}', console_handler))

    app.on_shutdown.append(server_shutdown)
    app.on_cleanup.append(server_cleanup)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(
        runner,
        str(config['service']['ip']),
        config['service']['port'],
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
@click.option('-f', '--config', type=click.Path(exists=True),
              default='console-server.conf',
              help='The configuration file to use.')
@click.option('--debug', is_flag=True,
              default=False,
              help='Use more verbose logging.')
def main(config, debug):
    config = toml.loads(Path(config).read_text(encoding='utf-8'))
    config['debug'] = debug

    setproctitle(f"backend.ai: console-server "
                 f"{config['service']['ip']}:{config['service']['port']}")

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
