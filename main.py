import random
import time

from fastapi import FastAPI, HTTPException, Request
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

resource = Resource.create()
tracer_provider = TracerProvider(resource=resource)
tracer_provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))
trace.set_tracer_provider(tracer_provider)

app = FastAPI()

FastAPIInstrumentor.instrument_app(app, tracer_provider=tracer_provider)

tracer = trace.get_tracer("saleor.service")


@app.post("/")
def list_shipping_methods(request: Request):
    with tracer.start_as_current_span("external API call") as span:
        span.set_attribute(
            "saleor.environment.domain", request.headers.get("saleor-domain") or ""
        )
        time.sleep(random.random() * 0.250)
        if random.random() < 0.01:
            raise HTTPException(status_code=500, detail="Unknow error")
    return {}
