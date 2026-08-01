from typing import Any, Literal, overload

import requests
from pyrate_limiter import Limiter, Rate

from parsons.utilities.api_connector import APIConnector


class RateLimitedAPIConnector(APIConnector):
    """
    A wrapper around APIConnector that adds rate limiting using pyrate-limiter.

    Args:
        ratelimit:
            The rate limit to apply to API calls, as a pyrate-limiter :class:`pyrate_limiter.abstracts.Rate` object.

    """

    def __init__(self, *args, ratelimit: Rate, **kwargs) -> None:
        self.limiter = Limiter(ratelimit)
        super().__init__(*args, **kwargs)

    def request(
        self,
        *args,
        **kwargs,
    ) -> requests.Response:
        self.limiter.try_acquire("api_call")
        return super().request(*args, **kwargs)

    @overload
    def get_request(
        self,
        url: ...,
        *,
        params: ... = ...,
        return_format: Literal["json"] = "json",
        raise_on_error: ... = ...,
        **kwargs,
    ) -> dict[str, Any]: ...

    @overload
    def get_request(
        self,
        url: ...,
        *,
        params: ... = ...,
        return_format: Literal["content"],
        raise_on_error: ... = ...,
        **kwargs,
    ) -> bytes: ...

    def get_request(
        self,
        *args,
        **kwargs,
    ) -> dict[str, Any] | bytes:
        self.limiter.try_acquire("api_call")
        return super().get_request(*args, **kwargs)

    def post_request(
        self,
        *args,
        **kwargs,
    ) -> dict[str, Any] | int | None:
        self.limiter.try_acquire("api_call")
        return super().post_request(*args, **kwargs)

    def delete_request(
        self,
        *args,
        **kwargs,
    ) -> dict[str, Any] | int | None:
        self.limiter.try_acquire("api_call")
        return super().delete_request(*args, **kwargs)

    def put_request(
        self,
        *args,
        **kwargs,
    ) -> dict[str, Any] | int | None:
        self.limiter.try_acquire("api_call")
        return super().put_request(*args, **kwargs)

    def patch_request(
        self,
        *args,
        **kwargs,
    ) -> dict[str, Any] | int | None:
        self.limiter.try_acquire("api_call")
        return super().patch_request(*args, **kwargs)
