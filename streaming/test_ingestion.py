import pathway as pw
from streaming.ingestion import ingest_stream
from streaming.processor import process_environmental_stream

raw_table = ingest_stream()
processed_table = process_environmental_stream(raw_table)

# ✅ Correct streaming output
pw.io.csv.write(processed_table, "/dev/stdout")

# ✅ REQUIRED for streaming
pw.run()