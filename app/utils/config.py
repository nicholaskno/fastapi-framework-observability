from fastapi.middleware.cors import CORSMiddleware
from app.settings import settings
from fastapi.openapi.utils import get_openapi

# Otel - Traces
from opentelemetry import trace
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.trace.export import ConsoleSpanExporter

# Otel - logger
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter


# Otel - Métricas
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter

import logging

# Jobs
# from apscheduler.schedulers.background import BackgroundScheduler

# Routes
from app.observability.routes import userRoute as observabilityUserRoute


def setCors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=settings.cors_methods,
        allow_headers=settings.cors_headers,
    )


def setRoutes(app):
    # Observability
    app.include_router(observabilityUserRoute.router_register)
    app.include_router(observabilityUserRoute.router_login)
    app.include_router(observabilityUserRoute.router_user)


# def setJobs(app):
#     @app.on_event('startup')
#     def init_jos():
        


def setOpenApiCfg(app):
    if app.openapi_schema:
        return app.openapi_schema
    
    project_info = {
        "title": settings.project_title,
        "version": settings.project_version,
        "description": settings.project_description
    }
    
    openapi_schema = get_openapi(
        **project_info,
        routes=app.routes,
    )
    
    if settings.logo_path:
        openapi_schema["info"]["x-logo"] = {
            "url": settings.logo_path
        }

    app.openapi_schema = openapi_schema

    return app.openapi_schema


def initObservability(app):
    resource = Resource(attributes={SERVICE_NAME: "observability-api-server"})

    # Configura o provedor de trace
    tracer_provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(tracer_provider)

    # Exportador OTLP para o collector (gRPC)
    otlp_exporter = OTLPSpanExporter(endpoint="otel:4317", insecure=True)
    span_processor = BatchSpanProcessor(otlp_exporter)

    # Adiciona o processor
    tracer_provider.add_span_processor(span_processor)

    # Opcional: log para console
    tracer_provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))   

    # Logger
    # resource = Resource.create({"service.name": "fastapi-otel-logs"})
    provider = LoggerProvider(resource=resource)
    exporter = OTLPLogExporter(endpoint="otel:4317", insecure=True)
    processor = BatchLogRecordProcessor(exporter)
    provider.add_log_record_processor(processor)
    set_logger_provider(provider)

    logger = logging.getLogger("observability")
    logger.setLevel(logging.DEBUG)  # fundamental!
    handler = LoggingHandler(level=logging.NOTSET, logger_provider=provider)
    logger.addHandler(handler) 


    # MÉTRICAS
    metric_exporter = OTLPMetricExporter(endpoint="otel:4317", insecure=True)
    metric_reader = PeriodicExportingMetricReader(metric_exporter)
    meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
    metrics.set_meter_provider(meter_provider)

    meter = metrics.get_meter("observability-api-server")

    FastAPIInstrumentor.instrument_app(app)

    return logger, meter
    