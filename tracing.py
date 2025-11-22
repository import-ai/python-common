import os.path

from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource, SERVICE_NAME, DEPLOYMENT_ENVIRONMENT
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


def setup_opentelemetry(service_name: str, env_key: str = "OTEL_EXPORTER_OTLP_ENDPOINT") -> bool:
    if not (base_endpoint := os.environ.get(env_key, None)):
        return False
    endpoint = base_endpoint + "/v1/traces"
    otlp_exporter = OTLPSpanExporter(endpoint=endpoint)
    span_processor = BatchSpanProcessor(otlp_exporter)

    resource = Resource.create(attributes={
        SERVICE_NAME: service_name,
        DEPLOYMENT_ENVIRONMENT: os.environ.get("ENV", "unknown")
    })

    trace_provider = TracerProvider(resource=resource)
    trace_provider.add_span_processor(span_processor)
    trace.set_tracer_provider(trace_provider)
    return True


def fastapi_patch_opentelemetry(app: FastAPI):
    FastAPIInstrumentor.instrument_app(app, excluded_urls="api/v1/health", exclude_spans=["send"])
