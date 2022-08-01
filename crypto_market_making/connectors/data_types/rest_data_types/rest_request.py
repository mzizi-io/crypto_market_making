from dataclasses import dataclass
from typing import Mapping, Optional, Any
from crypto_market_making.connectors.data_types.rest_data_types.rest_method import RESTMethod

@dataclass
class RESTRequest:
    method: RESTMethod
    url: Optional[str] = None
    endpoint_url: Optional[str] = None
    params: Optional[Mapping[str, str]] = None
    data: Any = None
    headers: Optional[Mapping[str, str]] = None
    is_auth_required: bool = False
    throttler_limit_id: Optional[str] = None