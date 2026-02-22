import pathway as pw

def classify_severity(avg_aqi: float) -> str:
    if avg_aqi >= 300:
        return "SEVERE"
    elif avg_aqi >= 200:
        return "POOR"
    elif avg_aqi >= 100:
        return "MODERATE"
    else:
        return "GOOD"

def process_environmental_stream(table: pw.Table) -> pw.Table:
    # Tumbling window of 10 units for real-time aggregation
    windowed = table.groupby(pw.this.city).windowby(
        pw.this.timestamp,
        window=pw.temporal.tumbling(duration=10),
    ).reduce(
        city=pw.reducers.min(pw.this.city),
        avg_aqi=pw.reducers.avg(pw.this.aqi),
        max_aqi=pw.reducers.max(pw.this.aqi),
    )

    return windowed.select(
        pw.this.city,
        pw.this.avg_aqi,
        pw.this.max_aqi,
        severity=pw.apply(classify_severity, pw.this.avg_aqi),
    )