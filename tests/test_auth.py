import pytest

from typing import Any, Dict
from unittest.mock import MagicMock, AsyncMock

from aiohttp import web

from ai.backend.console.auth import get_api_session, get_anonymous_session


class DummyRequest:
    def __init__(self, app_data: Dict[str, Any]) -> None:
        self.app = app_data


@pytest.mark.asyncio
async def test_get_api_session(mocker):
    mock_request = DummyRequest({'config': {
        'api': {'domain': 'default', 'endpoint': 'https://api.backend.ai'},
    }})

    mock_get_session = AsyncMock(return_value={
        'authenticated': False
    })
    mocker.patch('ai.backend.console.auth.get_session', mock_get_session)
    with pytest.raises(web.HTTPUnauthorized):
        await get_api_session(mock_request)
    mock_get_session.assert_awaited_once()

    mock_get_session = AsyncMock(return_value={
        'authenticated': True,
        'token': {'type': 'something-else', },
    })
    mocker.patch('ai.backend.console.auth.get_session', mock_get_session)
    with pytest.raises(web.HTTPBadRequest):
        await get_api_session(mock_request)
    mock_get_session.assert_awaited_once()

    mock_get_session = AsyncMock(return_value={
        'authenticated': True,
        'token': {'type': 'keypair', 'access_key': 'ABC', 'secret_key': 'xyz'},
    })
    mocker.patch('ai.backend.console.auth.get_session', mock_get_session)
    api_session = await get_api_session(mock_request)
    try:
        mock_get_session.assert_awaited_once()
        assert not api_session.config.is_anonymous
        assert api_session.config.domain == 'default'
        assert str(api_session.config.endpoint) == 'https://api.backend.ai'
        assert api_session.config.access_key == 'ABC'
        assert api_session.config.secret_key == 'xyz'
    finally:
        await api_session.close()


@pytest.mark.asyncio
async def test_get_anonymous_session(mocker):
    mock_request = DummyRequest({'config': {
        'api': {'domain': 'default', 'endpoint': 'https://api.backend.ai'},
    }})
    mock_get_session = MagicMock()
    mocker.patch('ai.backend.console.auth.get_session', mock_get_session)
    api_session = await get_anonymous_session(mock_request)
    try:
        mock_get_session.assert_not_called()
        assert api_session.config.is_anonymous
        assert api_session.config.domain == 'default'
        assert str(api_session.config.endpoint) == 'https://api.backend.ai'
        assert api_session.config.access_key == ''
        assert api_session.config.secret_key == ''
    finally:
        await api_session.close()
