from typing import Any, Dict, Optional, Type, TypeVar, Mapping, Union
from urllib.parse import urljoin

import httpx
from pydantic import BaseModel, ValidationError

T = TypeVar('T', bound=BaseModel)


class APIClient:
    def __init__(
            self,
            url: str,
            token: Optional[str] = None,
            *,
            timeout: Union[float, httpx.Timeout] = 10.0,
            follow_redirects: bool = True,
            verify: Union[bool, str] = True,
    ) -> None:
        self.url = url
        self.token = token
        self.timeout = timeout
        self.follow_redirects = follow_redirects
        self.verify = verify
        self._client = self.create_client()

    async def __aenter__(self) -> 'APIClient':
        return self

    async def __aexit__(self, *args, **kwargs) -> None:
        await self._client.aclose()

    def create_client(self):
        return httpx.AsyncClient(
            base_url=self.url,
            timeout=self.timeout,
            headers=self.get_headers(),
            follow_redirects=self.follow_redirects,
            verify=self.verify,
        )

    async def request(
            self,
            path: str,
            method: str = 'get',
            *,
            params: Optional[dict[str, Any]] = None,
            json: Optional[Any] = None,
            data: Optional[Union[dict[str, Any], bytes]] = None,
    ) -> httpx.Response:
        url = urljoin(self.url, path)
        try:
            response = await self._client.request(
                method=method.upper(),
                url=url,
                params=params,
                json=json,
                data=data,
                headers=self.get_headers(),
            )
            response.raise_for_status()
            return response

        except httpx.HTTPStatusError as e:
            body = e.response.text
            ...
        except httpx.RequestError as e:
            ...
        except ValidationError:
            ...
        except ValueError:
            ...

    def get_headers(self) -> dict:
        if self.token:
            return {'Authorization': f'Token {self.token}'}
        return {}

    async def get_profiles(self, params: Optional[dict] = None):
        path = 'api/v1/profiles/'
        return await self.request(path=path, params=params)

    async def get_players(self, params: Optional[dict] = None):
        path = 'api/v1/players/'
        return await self.request(path=path, params=params)

    async def create_player(self, data: dict):
        path = f'api/v1/players/'
        return await self.request(method='post', path=path, data=data)

    async def edit_player(self, player_id: int, data: dict):
        path = f'api/v1/players/{player_id}/'
        return await self.request(method='patch', path=path, data=data)

    async def get_tournament(self, tournament_id: int):
        path = f'api/v1/tournaments/{tournament_id}/'
        return await self.request(path=path)

    async def get_tournaments(self, params: Optional[dict] = None):
        path = 'api/v1/tournaments/'
        return await self.request(path=path, params=params)

    async def get_teams(self, params: Optional[dict] = None):
        path = 'api/v1/teams/'
        return await self.request(path=path, params=params)

    async def create_team(self, data: dict):
        path = 'api/v1/teams/'
        return await self.request(method='post', path=path, data=data)

    async def add_team_player(self, team_id: int, data: dict):
        path = f'api/v1/teams/{team_id}/players/'
        return await self.request(method='post', path=path, data=data)

    async def get_tournament_players(self, params: dict):
        path = f'api/v1/tournament_players/'
        return await self.request(path=path, params=params)

    async def create_tournament_players(self, data: dict):
        path = f'api/v1/tournament_players/'
        return await self.request(method='post', path=path, data=data)

    async def edit_tournament_players(self, tournament_player_id: int, data: dict):
        path = f'api/v1/tournament_players/{tournament_player_id}/'
        return await self.request(method='patch', path=path, data=data)
