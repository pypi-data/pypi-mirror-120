import typing
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from skywalking.trace.carrier import Carrier
from skywalking.trace.context import Span, get_context, SpanContext
from skywalking import Layer, Component
from skywalking.trace.tags import TagHttpMethod, TagHttpURL, TagHttpStatusCode, TagHttpStatusMsg
from starlette.types import ASGIApp
from skywalking import config
from skywalking import agent


RequestResponseEndpoint = typing.Callable[[Request], typing.Awaitable[Response]]

DispatchFunction = typing.Callable[
    [Request, RequestResponseEndpoint], typing.Awaitable[Response]
]

class SkywalkingMiddleware(BaseHTTPMiddleware):

    def __init__(self, 
                app: ASGIApp, 
                dispatch: DispatchFunction = None,
                service_name='Python Service Name',
                collector_address='35.237.148.228:12800',
                protocol = 'http',
                log_reporter_active= False
                ) -> None:
        self.app = app
        config.init(service_name=service_name, 
                    collector_address= collector_address, 
                    protocol=protocol,
                    log_reporter_active=log_reporter_active
                    )
        agent.start()
        self.dispatch_func = self.dispatch if dispatch is None else dispatch

    async def dispatch(self, request, call_next):
        context: SpanContext = get_context()
        with context.new_entry_span(op=request.url.path, carrier=Carrier()) as span:
            span.layer = Layer.Http
            span.component = Component.Requests
            span.peer = f"{request.client.host}:{request.client.port}"
            span.tag(TagHttpMethod(request.method))
            span.tag(TagHttpURL(request.url._url))
            try:
                response = await call_next(request)
                span.tag(tag=TagHttpStatusCode(response.status_code))
                if response.status_code >= 400:
                    span.error_occurred = True
                span.stop()
                return response
            except:
                span.raised()
                raise