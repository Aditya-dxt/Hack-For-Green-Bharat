import pathway as pw
from .data_source import live_environmental_stream


class EnvironmentalEvent(pw.Schema):
    raw: bytes


def ingest_stream():
    """
    Ingests live environmental data into Pathway as a real-time stream.
    """
    return pw.io.python.read(
        live_environmental_stream,
        schema=EnvironmentalEvent
    )
