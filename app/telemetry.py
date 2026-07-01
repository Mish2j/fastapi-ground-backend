from datetime import datetime
import random 

def generate_telemetry():
    return {
        "satellite_id": "SAT-001",
        "timestamp": datetime.now().isoformat(),
        "latitude": round(random.uniform(-90, 90), 4),
        "longitude": round(random.uniform(-180, 180), 4),
        "altitude_km": round(random.uniform(400, 420), 2),
        "battery_percent": round(random.uniform(70, 100), 1),
        "temperature_c": round(random.uniform(15, 35), 1),
        "status": "nominal"
    }