from collections import defaultdict, deque
from time import time
from threading import Lock

from fastapi import HTTPException, Request, status


class FixedWindowRateLimiter:
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._requests: dict[str, deque[float]] = defaultdict(deque)
        self._lock = Lock()

    def __call__(self, request: Request) -> None:
        client_host = request.client.host if request.client else "unknown"
        now = time()
        window_start = now - self.window_seconds

        with self._lock:
            bucket = self._requests[client_host]
            while bucket and bucket[0] < window_start:
                bucket.popleft()
            if len(bucket) >= self.max_requests:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="Too many requests. Please try again later.",
                )
            bucket.append(now)

    def reset(self) -> None:
        with self._lock:
            self._requests.clear()
