from fastapi import FastAPI

app = FastAPI(
    title="Aqlli chiqindilarni qayta ishlash tizimi API",
    version="0.1.0",
    description="Chiqindilarni qayta ishlash va tejalgan energiyani hisoblash xizmati"
)

@app.get("/")
def holatni_tekshirish():
    return {"holat": "ishlamoqda", "xizmat": "Aqlli chiqindilarni qayta ishlash tizimi"}

@app.get("/api/v1/tejalgan-energiya")
def tejalgan_energiyani_hisoblash(qayta_ishlangan_tonna: float, bir_tonna_uchun_kwh: float):
    # Qayta ishlangan chiqindidan tejalgan jami energiyani kWh va GWh da hisoblash
    jami_kwh = qayta_ishlangan_tonna * bir_tonna_uchun_kwh
    return {
        "qayta_ishlangan_tonna": qayta_ishlangan_tonna,
        "tejalgan_energiya_kwh": round(jami_kwh, 2),
        "tejalgan_energiya_gwh": round(jami_kwh / 1_000_000, 4),
    }
