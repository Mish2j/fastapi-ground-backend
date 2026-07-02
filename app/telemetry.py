from datetime import datetime, timezone
import random 

telemetry_history = []
MAX_HISTORY = 500

satellite_state = {
    "satellite_id": "SAT-001",
    "mode": "NOMINAL",
    "downlink_rate": "LOW",
    "faults": []
}

def generate_telemetry():
    telemetry = {
        "satellite_id": satellite_state["satellite_id"],
        "timestamp":  datetime.now(timezone.utc).isoformat(),
        "mode": satellite_state["mode"],
        "downlink_rate": satellite_state["downlink_rate"],
        "latitude": round(random.uniform(-90, 90), 4),
        "longitude": round(random.uniform(-180, 180), 4),
        "altitude_km": round(random.uniform(400, 420), 2),
        "battery_percent": round(random.uniform(70, 100), 1),
        "temperature_c": round(random.uniform(15, 35), 1),
        "faults": satellite_state["faults"]
    }

    save_telemetry(telemetry)

    return telemetry


def get_latest_telemetry():
    if not telemetry_history:
        return generate_telemetry
    
    return telemetry_history[-1]

def get_telemetry_history(limit: int = 100):
    return telemetry_history[-limit:]

def save_telemetry(telemetry):
    telemetry_history.append(telemetry)

    if(len(telemetry_history)) > MAX_HISTORY:
        telemetry_history.pop(0)
    
def set_mode(mode: str):
    allowed_modes = ["NOMINAL", "SAFE", "SCIENCE"]

    if mode not in allowed_modes:
        return {
            "status": "REJECTED",
            "message": f"Invalid mode: {mode}"
        }

    satellite_state["mode"] = mode

    return {
        "status": "ACCEPTED",
        "message": f"Mode changed to {mode}"
    }
    