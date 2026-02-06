import csv
import time

def sensor_stream():
    """
    Simulates live sensor data by reading CSV row by row.
    """

    print("📡 Starting simulated live sensor stream...\n")

    with open("data/sample_sensor.csv", "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            time.sleep(1)  # simulate real-time delay
            yield {
                "location": row["location"],
                "pm25": int(row["pm25"])
            }
