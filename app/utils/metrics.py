from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from opentelemetry.metrics import Meter
import time



class AppMetrics:
    def __init__(self, meter: Meter):
        self.request_counter = meter.create_counter(
            name="http_requests_total",
            unit="1",
            description="Total de requisições HTTP",
        )

        self.error_counter = meter.create_counter(
            name="http_errors_total",
            unit="1",
            description="Total de erros HTTP (4xx/5xx)",
        )

        self.latency_histogram = meter.create_histogram(
            name="http_request_duration_seconds",
            unit="s",
            description="Duração das requisições HTTP",
        )


class MetricsMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, metrics: AppMetrics):
        super().__init__(app)
        self.metrics = metrics

    async def dispatch(self, request: Request, call_next):
        start = time.time()

        try:
            response = await call_next(request)
        except Exception:
            self.metrics.error_counter.add(1, {"route": request.url.path, "status": "500"})
            raise

        duration = time.time() - start

        self.metrics.request_counter.add(1, {
            "route": request.url.path,
            "method": request.method,
            "status": str(response.status_code)
        })

        if response.status_code >= 400:
            self.metrics.error_counter.add(1, {
                "route": request.url.path,
                "method": request.method,
                "status": str(response.status_code)
            })

        self.metrics.latency_histogram.record(duration, {
            "route": request.url.path,
            "method": request.method,
            "status": str(response.status_code)
        })

        return response
