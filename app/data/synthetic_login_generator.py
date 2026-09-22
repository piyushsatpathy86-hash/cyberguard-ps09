"""
Task 1: Synthetic login-log generator for the anomaly detection scenario.

Explicitly allowed per the PS (Deliverable #10 requires simulated,
authorised, or publicly available datasets — not real user data).

Generates realistic-looking login events (timestamp, user_id, ip, device_id,
geo) with a controllable fraction of injected anomalies: impossible travel,
password spraying, new-device + new-location combos.
"""

import random
from datetime import datetime, timedelta


def generate_normal_login(user_id: str, base_time: datetime) -> dict:
    """Owner: fill in realistic normal-pattern generation."""
    raise NotImplementedError("Task 1 owner: implement generate_normal_login")


def generate_anomalous_login(user_id: str, base_time: datetime, anomaly_type: str) -> dict:
    """
    anomaly_type: "impossible_travel" | "password_spray" | "new_device_location"
    Owner: fill in anomaly injection logic.
    """
    raise NotImplementedError("Task 1 owner: implement generate_anomalous_login")


def generate_dataset(n_users: int = 20, n_events: int = 500, anomaly_rate: float = 0.05) -> list[dict]:
    """Owner: combine normal + anomalous events into a labelled dataset."""
    raise NotImplementedError("Task 1 owner: implement generate_dataset")
