from fastapi import FastAPI

app = FastAPI(title="Smart Waste Management System API", version="0.1.0")

@app.get("/")
def health_check():
    return {"status": "ok", "service": "Smart Waste Management System"}

@app.get("/api/v1/energy-saved")
def calculate_energy_saved(recycled_tonnes: float, kwh_per_tonne: float):
    total_kwh = recycled_tonnes * kwh_per_tonne
    return {
        "recycled_tonnes": recycled_tonnes,
        "total_energy_saved_kwh": round(total_kwh, 2),
        "total_energy_saved_gwh": round(total_kwh / 1_000_000, 4),
    }
