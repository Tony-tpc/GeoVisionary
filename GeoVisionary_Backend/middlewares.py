class StreamingMiddleware:
    """
    让 Daphne 支持 StreamingHttpResponse
    """

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            scope["asgi.http_version"] = "1.1"  # 确保使用 HTTP/1.1，启用分块传输
            scope["asgi.spec_version"] = "2.1"  # 兼容 ASGI 2.1，防止 Daphne 缓存
        await self.app(scope, receive, send)
