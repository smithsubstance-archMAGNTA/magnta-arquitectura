"""Simulator that sends periodic signals to MAGNTA API for testing.

Uses environment variables to configure target and interval.
"""

import os
import time
import json
import random
import requests

TARGET = os.getenv("SIM_TARGET", "http://web:8000/ingest-signal")
INTERVAL = float(os.getenv("SIM_INTERVAL", "5"))
SOURCE = os.getenv("SIM_SOURCE", "simulator-1")


def random_payload():
    # generate sample sensor payload with random floats
    return {
        "a": round(random.uniform(0.0, 1.5), 3),
        "b": round(random.uniform(0.0, 1.5), 3),
        "c": round(random.uniform(0.0, 1.5), 3),
        "latency": round(random.uniform(0.0, 0.2), 3),
    }


def main():
    print(f"Simulator target={TARGET} interval={INTERVAL}s")
    while True:
        payload = {
            "source": SOURCE,
            "timestamp": time.time(),
            "payload": random_payload(),
        }
        try:
            r = requests.post(TARGET, json=payload, timeout=5)
            print("sent", payload, "status", r.status_code)
        except Exception as e:
            print("error sending", e)
        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()
