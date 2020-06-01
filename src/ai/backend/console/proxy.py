from __future__ import annotations

import asyncio
import logging
import json
from typing import (
    Optional, Union,
    Tuple,
    cast,
)

import aiohttp
from aiohttp import web

from ai.backend.client.exceptions import BackendAPIError, BackendClientError
from ai.backend.client.request import Request

from .auth import get_api_session, get_anonymous_session
from .logging import BraceStyleAdapter

log = BraceStyleAdapter(logging.getLogger('ai.backend.console.proxy'))


class WebSocketProxy:
    __slots__ = (
        'up_conn', 'down_conn',
        'upstream_buffer', 'upstream_buffer_task',
    )

    up_conn: aiohttp.ClientWebSocketResponse
    down_conn: web.WebSocketResponse
    upstream_buffer: asyncio.Queue[Tuple[Union[str, bytes], aiohttp.WSMsgType]]
    upstream_buffer_task: Optional[asyncio.Task]

    def __init__(self, up_conn: aiohttp.ClientWebSocketResponse,
                 down_conn: web.WebSocketResponse) -> None:
        self.up_conn = up_conn
        self.down_conn = down_conn
        self.upstream_buffer = asyncio.Queue()
        self.upstream_buffer_task = None

    async def proxy(self) -> None:
        asyncio.ensure_future(self.downstream())
        await self.upstream()

    async def upstream(self) -> None:
        try:
            async for msg in self.down_conn:
                if msg.type in (aiohttp.WSMsgType.TEXT, aiohttp.WSMsgType.BINARY):
                    await self.send(msg.data, msg.type)
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    log.error("WebSocketProxy: connection closed with exception {}",
                              self.up_conn.exception())
                    break
                elif msg.type == aiohttp.WSMsgType.CLOSE:
                    break
            # here, client gracefully disconnected
        except asyncio.CancelledError:
            # here, client forcibly disconnected
            pass
        finally:
            await self.close_downstream()

    async def downstream(self) -> None:
        try:
            self.upstream_buffer_task = \
                    asyncio.create_task(self.consume_upstream_buffer())
            async for msg in self.up_conn:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    await self.down_conn.send_str(msg.data)
                elif msg.type == aiohttp.WSMsgType.BINARY:
                    await self.down_conn.send_bytes(msg.data)
                elif msg.type == aiohttp.WSMsgType.CLOSED:
                    break
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    break
            # here, server gracefully disconnected
        except asyncio.CancelledError:
            pass
        except Exception as e:
            log.error('WebSocketProxy: unexpected error: {}', e)
        finally:
            await self.close_upstream()

    async def consume_upstream_buffer(self) -> None:
        try:
            while True:
                data, tp = await self.upstream_buffer.get()
                if not self.up_conn.closed:
                    if tp == aiohttp.WSMsgType.BINARY:
                        await self.up_conn.send_bytes(cast(bytes, data))
                    elif tp == aiohttp.WSMsgType.TEXT:
                        await self.up_conn.send_str(cast(str, data))
        except asyncio.CancelledError:
            pass

    async def send(self, msg: str, tp: aiohttp.WSMsgType) -> None:
        await self.upstream_buffer.put((msg, tp))

    async def close_downstream(self) -> None:
        if not self.down_conn.closed:
            await self.down_conn.close()

    async def close_upstream(self) -> None:
        if self.upstream_buffer_task is not None and not self.upstream_buffer_task.done():
            self.upstream_buffer_task.cancel()
            await self.upstream_buffer_task
        if not self.up_conn.closed:
            await self.up_conn.close()


async def web_handler(request, *, is_anonymous=False) -> web.StreamResponse:
    path = request.match_info.get('path', '')
    if is_anonymous:
        api_session = await asyncio.shield(get_anonymous_session(request))
    else:
        api_session = await asyncio.shield(get_api_session(request))
    try:
        # We treat all requests and responses as streaming universally
        # to be a transparent proxy.
        api_rqst = Request(
            api_session, request.method, path, request.content,
            params=request.query)
        if 'Content-Type' in request.headers:
            api_rqst.content_type = request.content_type                        # set for signing
            api_rqst.headers['Content-Type'] = request.headers['Content-Type']  # preserve raw value
        if 'Content-Length' in request.headers:
            api_rqst.headers['Content-Length'] = request.headers['Content-Length']
        # Uploading request body happens at the entering of the block,
        # and downloading response body happens in the read loop inside.
        async with api_rqst.fetch() as up_resp:
            down_resp = web.StreamResponse()
            down_resp.set_status(up_resp.status, up_resp.reason)
            down_resp.headers.update(up_resp.headers)
            # We already have configured CORS handlers and the API server
            # also provides those headers.  Just let them as-is.
            await down_resp.prepare(request)
            while True:
                chunk = await up_resp.aread(8192)
                if not chunk:
                    break
                await down_resp.write(chunk)
            return down_resp
    except asyncio.CancelledError:
        raise
    except BackendAPIError as e:
        return web.Response(body=json.dumps(e.data),
                            content_type="application/problem+json",
                            status=e.status, reason=e.reason)
    except BackendClientError:
        log.exception('web_handler: BackendClientError')
        return web.HTTPBadGateway(text=json.dumps({
            'type': 'https://api.backend.ai/probs/bad-gateway',
            'title': "The proxy target server is inaccessible.",
        }), content_type='application/problem+json')
    except Exception:
        log.exception('web_handler: unexpected error')
        return web.HTTPInternalServerError(text=json.dumps({
            'type': 'https://api.backend.ai/probs/internal-server-error',
            'title': "Something has gone wrong.",
        }), content_type='application/problem+json')
    finally:
        await api_session.close()


async def web_plugin_handler(request, *, is_anonymous=False) -> web.StreamResponse:
    '''
    This handler is almost same to web_handler, but does not manipulate the
    content-type and content-length headers before sending up-requests.
    It also configures the domain in the json body for "auth/signup" requests.
    '''
    path = request.match_info['path']
    if is_anonymous:
        api_session = await asyncio.shield(get_anonymous_session(request))
    else:
        api_session = await asyncio.shield(get_api_session(request))
    try:
        # We treat all requests and responses as streaming universally
        # to be a transparent proxy.
        content = request.content
        if path == 'auth/signup':
            body = await request.json()
            body['domain'] = request.app['config']['api']['domain']
            content = json.dumps(body).encode('utf8')
        api_rqst = Request(
            api_session, request.method, path, content,
            params=request.query,
            content_type=request.content_type)
        # Uploading request body happens at the entering of the block,
        # and downloading response body happens in the read loop inside.
        async with api_rqst.fetch() as up_resp:
            down_resp = web.StreamResponse()
            down_resp.set_status(up_resp.status, up_resp.reason)
            down_resp.headers.update(up_resp.headers)
            # We already have configured CORS handlers and the API server
            # also provides those headers.  Just let them as-is.
            await down_resp.prepare(request)
            while True:
                chunk = await up_resp.aread(8192)
                if not chunk:
                    break
                await down_resp.write(chunk)
            return down_resp
    except asyncio.CancelledError:
        raise
    except BackendAPIError as e:
        return web.Response(body=json.dumps(e.data),
                            content_type='application/problem+json',
                            status=e.status, reason=e.reason)
    except BackendClientError:
        log.exception('web_plugin_handler: BackendClientError')
        return web.HTTPBadGateway(text=json.dumps({
            'type': 'https://api.backend.ai/probs/bad-gateway',
            'title': "The proxy target server is inaccessible.",
        }), content_type='application/problem+json')
    except Exception:
        log.exception('web_plugin_handler: unexpected error')
        return web.HTTPInternalServerError(text=json.dumps({
            'type': 'https://api.backend.ai/probs/internal-server-error',
            'title': "Something has gone wrong.",
        }), content_type='application/problem+json')
    finally:
        await api_session.close()


async def websocket_handler(request, *, is_anonymous=False) -> web.StreamResponse:
    path = request.match_info['path']
    if is_anonymous:
        api_session = await asyncio.shield(get_anonymous_session(request))
    else:
        api_session = await asyncio.shield(get_api_session(request))
    try:
        params = request.query if request.query else None
        api_rqst = Request(
            api_session, request.method, path, request.content,
            params=params,
            content_type=request.content_type)
        async with api_rqst.connect_websocket() as up_conn:
            down_conn = web.WebSocketResponse()
            await down_conn.prepare(request)
            web_socket_proxy = WebSocketProxy(up_conn, down_conn)
            await web_socket_proxy.proxy()
            return down_conn
    except asyncio.CancelledError:
        raise
    except BackendAPIError as e:
        return web.Response(body=json.dumps(e.data),
                            status=e.status, reason=e.reason)
    except BackendClientError:
        log.exception('websocket_handler: BackendClientError')
        return web.HTTPBadGateway(text=json.dumps({
            'type': 'https://api.backend.ai/probs/bad-gateway',
            'title': "The proxy target server is inaccessible.",
        }), content_type='application/problem+json')
    except Exception:
        log.exception('websocket_handler: unexpected error')
        return web.HTTPInternalServerError(text=json.dumps({
            'type': 'https://api.backend.ai/probs/internal-server-error',
            'title': "Something has gone wrong.",
        }), content_type='application/problem+json')
    finally:
        await api_session.close()
