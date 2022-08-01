from abc import ABC, abstractmethod
from typing import Mapping, Any, Optional
from dataclasses import dataclass

class WSRequest(ABC):
    @abstractmethod
    async def send_with_connection(self, connection: 'WSConnector'):
        return NotImplemented

@dataclass
class WSJSONRequest(WSRequest):
    payload: Mapping[str, Any]
    throttler_limit_id: Optional[str] = None
    is_auth_required: bool = False

    async def send_with_connection(self, connection: 'WSConnector'):
        await connection._send_json(payload=self.payload)


@dataclass
class WSPlainTextRequest(WSRequest):
    payload: str
    throttler_limit_id: Optional[str] = None
    is_auth_required: bool = False

    async def send_with_connection(self, connection: 'WSConnector'):
        await connection._send_plain_text(payload=self.payload)

