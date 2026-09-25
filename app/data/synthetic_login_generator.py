"""
data/synthetic_login_generator.py
Generates synthetic login/session logs for the account-takeover / anomaly
scenario, with 3 injected anomaly patterns: impossible travel, password
spraying, and unusual device/new-location logins.

Writes a labeled CSV to data/raw/synthetic_logins.csv. Ground-truth labels
(is_anomaly, anomaly_type) are included so anomaly_detector.py's precision/
recall can be measured later (feeds Deliverable #11 - performance evaluation).
data_loader.py is responsible for reading this CSV into the DB; this file
does not touch SQLite directly.

Owner: Sai
"""

import csv
import random
import uuid
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from pathlib import Path

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
NUM_USERS = 65          # per team decision: 60-70
NUM_DAYS = 14            # span of normal activity to simulate
LOGINS_PER_USER_PER_DAY = (1, 3)  # min, max normal logins/day

NUM_IMPOSSIBLE_TRAVEL = 8
NUM_PASSWORD_SPRAY_WAVES = 4       # each wave hits several accounts from one source
NUM_NEW_DEVICE_LOCATION = 10

OUTPUT_PATH = Path(__file__).resolve().parent / "raw" / "synthetic_logins.csv"

CITIES = [
    ("Bhubaneswar", "IN"), ("Delhi", "IN"), ("Mumbai", "IN"), ("Bengaluru", "IN"),
    ("Kolkata", "IN"), ("Hyderabad", "IN"), ("Pune", "IN"), ("Chennai", "IN"),
]
# Rare/suspicious locations used for injected anomalies (far from any home city)
FAR_LOCATIONS = [
    ("Moscow", "RU"), ("Lagos", "NG"), ("Sao Paulo", "BR"),
    ("Bucharest", "RO"), ("Jakarta", "ID"),
]

random.seed(42)  # reproducible dataset across the team


@dataclass
class LoginEvent:
    event_id: str
    user_id: str
    timestamp: str          # ISO 8601
    ip_address: str
    city: str
    country: str
    device_id: str
    login_success: bool
    is_anomaly: bool
    anomaly_type: str        # "" if not an anomaly
    source_type: str = "synthetic"


def make_ip() -> str:
    return f"{random.randint(1, 223)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"


def make_users(n: int):
    """Each user has a home city/country/device — their normal baseline."""
    users = []
    for i in range(n):
        city, country = random.choice(CITIES)
        users.append({
            "user_id": f"user_{i:03d}",
            "home_city": city,
            "home_country": country,
            "home_device_id": f"device_{uuid.uuid4().hex[:8]}",
            "home_ip": make_ip(),
        })
    return users


def generate_normal_logins(users, num_days: int):
    events = []
    start = datetime.utcnow() - timedelta(days=num_days)
    for user in users:
        for day in range(num_days):
            for _ in range(random.randint(*LOGINS_PER_USER_PER_DAY)):
                ts = start + timedelta(
                    days=day,
                    hours=random.randint(6, 23),
                    minutes=random.randint(0, 59),
                )
                events.append(LoginEvent(
                    event_id=f"evt_{uuid.uuid4().hex[:10]}",
                    user_id=user["user_id"],
                    timestamp=ts.isoformat(),
                    ip_address=user["home_ip"],
                    city=user["home_city"],
                    country=user["home_country"],
                    device_id=user["home_device_id"],
                    login_success=True,
                    is_anomaly=False,
                    anomaly_type="",
                ))
    return events


def inject_impossible_travel(users, count: int):
    """Same user, two logins from far-apart cities within an impossibly short window."""
    events = []
    for _ in range(count):
        user = random.choice(users)
        far_city, far_country = random.choice(FAR_LOCATIONS)
        base_ts = datetime.utcnow() - timedelta(days=random.randint(0, NUM_DAYS - 1))

        # Login 1: home location
        events.append(LoginEvent(
            event_id=f"evt_{uuid.uuid4().hex[:10]}",
            user_id=user["user_id"],
            timestamp=base_ts.isoformat(),
            ip_address=user["home_ip"],
            city=user["home_city"],
            country=user["home_country"],
            device_id=user["home_device_id"],
            login_success=True,
            is_anomaly=True,
            anomaly_type="impossible_travel",
        ))
        # Login 2: far-away location, ~20 minutes later - not physically possible
        second_ts = base_ts + timedelta(minutes=20)
        events.append(LoginEvent(
            event_id=f"evt_{uuid.uuid4().hex[:10]}",
            user_id=user["user_id"],
            timestamp=second_ts.isoformat(),
            ip_address=make_ip(),
            city=far_city,
            country=far_country,
            device_id=f"device_{uuid.uuid4().hex[:8]}",
            login_success=True,
            is_anomaly=True,
            anomaly_type="impossible_travel",
        ))
    return events


def inject_password_spraying(users, num_waves: int):
    """One source IP attempts logins across many accounts in a short window - mostly failed."""
    events = []
    for _ in range(num_waves):
        attacker_ip = make_ip()
        targets = random.sample(users, k=min(12, len(users)))
        base_ts = datetime.utcnow() - timedelta(days=random.randint(0, NUM_DAYS - 1))
        for i, user in enumerate(targets):
            ts = base_ts + timedelta(seconds=i * 15)  # rapid-fire attempts
            events.append(LoginEvent(
                event_id=f"evt_{uuid.uuid4().hex[:10]}",
                user_id=user["user_id"],
                timestamp=ts.isoformat(),
                ip_address=attacker_ip,
                city="Unknown",
                country="Unknown",
                device_id=f"device_{uuid.uuid4().hex[:8]}",
                login_success=random.random() < 0.1,  # mostly fail
                is_anomaly=True,
                anomaly_type="password_spraying",
            ))
    return events


def inject_new_device_location(users, count: int):
    """A single login from a device/location never seen before for that account."""
    events = []
    for _ in range(count):
        user = random.choice(users)
        city, country = random.choice(CITIES + FAR_LOCATIONS)
        ts = datetime.utcnow() - timedelta(days=random.randint(0, NUM_DAYS - 1))
        events.append(LoginEvent(
            event_id=f"evt_{uuid.uuid4().hex[:10]}",
            user_id=user["user_id"],
            timestamp=ts.isoformat(),
            ip_address=make_ip(),
            city=city,
            country=country,
            device_id=f"device_{uuid.uuid4().hex[:8]}",  # new, unseen device
            login_success=True,
            is_anomaly=True,
            anomaly_type="new_device_or_location",
        ))
    return events


def generate_dataset():
    users = make_users(NUM_USERS)
    events = []
    events += generate_normal_logins(users, NUM_DAYS)
    events += inject_impossible_travel(users, NUM_IMPOSSIBLE_TRAVEL)
    events += inject_password_spraying(users, NUM_PASSWORD_SPRAY_WAVES)
    events += inject_new_device_location(users, NUM_NEW_DEVICE_LOCATION)
    events.sort(key=lambda e: e.timestamp)
    return events


def write_csv(events, output_path: Path = OUTPUT_PATH):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(asdict(events[0]).keys()))
        writer.writeheader()
        for e in events:
            writer.writerow(asdict(e))
    print(f"Wrote {len(events)} events to {output_path}")


if __name__ == "__main__":
    dataset = generate_dataset()
    write_csv(dataset)

    anomaly_count = sum(1 for e in dataset if e.is_anomaly)
    print(f"Total events: {len(dataset)}")
    print(f"Anomalous events: {anomaly_count} ({anomaly_count / len(dataset):.1%})")
