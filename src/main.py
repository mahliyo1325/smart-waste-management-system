from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(
    title="Aqlli chiqindilarni qayta ishlash tizimi API",
    version="1.0.0",
    description="Chiqindilarni qayta ishlash va tejalgan energiyani hisoblash xizmati"
)

CHIQINDI_KATEGORIYALARI = [
    {"id": 1, "nomi": "Plastik", "kwh_tonna": 5774.0, "qayta_ishlash_foizi": 4.0},
    {"id": 2, "nomi": "Qogʻoz", "kwh_tonna": 4100.0, "qayta_ishlash_foizi": 38.0},
    {"id": 3, "nomi": "Shisha", "kwh_tonna": 42.0, "qayta_ishlash_foizi": 11.0},
    {"id": 4, "nomi": "Qora metall", "kwh_tonna": 642.0, "qayta_ishlash_foizi": 99.0},
    {"id": 5, "nomi": "Rangli metall", "kwh_tonna": 14000.0, "qayta_ishlash_foizi": 98.0},
]

DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Aqlli chiqindilarni qayta ishlash tizimi</title>
  <style>
    :root { --primary: #14532d; --accent: #0d9488; --bg: #f0fdf4; --card: #ffffff; --text: #1f2937; --muted: #4b5563; --border: #bbf7d0; }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: var(--bg); color: var(--text); line-height: 1.6; padding: 24px; }
    .container { max-width: 1040px; margin: 0 auto; }
    header { background: var(--primary); color: #fff; padding: 28px; border-radius: 14px; margin-bottom: 24px; }
    header h1 { font-size: 1.8rem; margin-bottom: 6px; }
    header p { color: #dcfce7; font-size: 0.95rem; }
    .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; margin-bottom: 24px; }
    .card { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.04); }
    .card h2 { font-size: 1.15rem; color: var(--primary); margin-bottom: 14px; border-bottom: 2px solid var(--bg); padding-bottom: 8px; }
    label { display: block; font-size: 0.9rem; font-weight: 600; margin-bottom: 6px; color: var(--muted); }
    select, input { width: 100%; padding: 10px 12px; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 1rem; margin-bottom: 14px; }
    button { width: 100%; background: var(--primary); color: #fff; border: none; padding: 12px; border-radius: 8px; font-size: 1rem; font-weight: 600; cursor: pointer; }
    button:hover { background: #166534; }
    .result-box { margin-top: 16px; background: var(--bg); border-left: 4px solid var(--accent); padding: 12px 14px; border-radius: 6px; display: none; }
    .bar-row { margin-bottom: 12px; }
    .bar-label { display: flex; justify-content: space-between; font-size: 0.9rem; font-weight: 600; margin-bottom: 4px; }
    .bar-track { background: #e2e8f0; border-radius: 999px; height: 10px; overflow: hidden; }
    .bar-fill { background: var(--accent); height: 100%; border-radius: 999px; }
    table { width: 100%; border-collapse: collapse; font-size: 0.92rem; }
    th, td { text-align: left; padding: 10px 8px; border-bottom: 1px solid #e2e8f0; }
    th { color: var(--primary); font-weight: 700; }
    .badge { padding: 3px 9px; border-radius: 999px; font-size: 0.8rem; font-weight: 600; }
    .badge-ok { background: #dcfce7; color: #166534; }
    .badge-warn { background: #fef3c7; color: #92400e; }
    .badge-crit { background: #fee2e2; color: #991b1b; }
    footer { text-align: center; font-size: 0.85rem; color: var(--muted); margin-top: 24px; }
    footer a { color: var(--primary); font-weight: 600; }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <h1>Aqlli chiqindilarni qayta ishlash tizimi</h1>
      <p>Smart Waste Management System &middot; Muallif: Nurmuhammedova Mahliyo</p>
    </header>

    <div class="grid">
      <div class="card">
        <h2>Tejalgan energiya kalkulyatori</h2>
        <label for="wasteType">Chiqindi turini tanlang</label>
        <select id="wasteType">
          <option value="5774">Plastik (5 774 kWh / tonna)</option>
          <option value="4100">Qogʻoz (4 100 kWh / tonna)</option>
          <option value="42">Shisha (42 kWh / tonna)</option>
          <option value="642">Qora metall (642 kWh / tonna)</option>
          <option value="14000">Rangli metall (14 000 kWh / tonna)</option>
        </select>
        <label for="tonnes">Qayta ishlangan hajm (tonna)</label>
        <input type="number" id="tonnes" value="150" min="1" step="1" />
        <button onclick="hisoblash()">Energiyani hisoblash</button>
        <div id="natija" class="result-box"></div>
      </div>

      <div class="card">
        <h2>Qayta ishlash koʻrsatkichlari (%)</h2>
        <div class="bar-row">
          <div class="bar-label"><span>Qora metall</span><span>99%</span></div>
          <div class="bar-track"><div class="bar-fill" style="width:99%"></div></div>
        </div>
        <div class="bar-row">
          <div class="bar-label"><span>Rangli metall</span><span>98%</span></div>
          <div class="bar-track"><div class="bar-fill" style="width:98%"></div></div>
        </div>
        <div class="bar-row">
          <div class="bar-label"><span>Qogʻoz</span><span>38%</span></div>
          <div class="bar-track"><div class="bar-fill" style="width:38%"></div></div>
        </div>
        <div class="bar-row">
          <div class="bar-label"><span>Shisha</span><span>11%</span></div>
          <div class="bar-track"><div class="bar-fill" style="width:11%"></div></div>
        </div>
        <div class="bar-row">
          <div class="bar-label"><span>Plastik</span><span>4%</span></div>
          <div class="bar-track"><div class="bar-fill" style="width:4%"></div></div>
        </div>
      </div>
    </div>

    <div class="card">
      <h2>Aqlli konteynerlar holati (IoT monitoring)</h2>
      <table>
        <thead>
          <tr><th>ID</th><th>Manzil</th><th>Chiqindi turi</th><th>Toʻlish darajasi</th><th>Holat</th></tr>
        </thead>
        <tbody>
          <tr><td>#BIN-101</td><td>Markaziy koʻcha, 14</td><td>Plastik</td><td>92%</td><td><span class="badge badge-crit">Zudlik bilan olish</span></td></tr>
          <tr><td>#BIN-102</td><td>Universitet hududi</td><td>Qogʻoz</td><td>68%</td><td><span class="badge badge-warn">Rejali yigʻish</span></td></tr>
          <tr><td>#BIN-103</td><td>Istirohat bogʻi</td><td>Shisha</td><td>34%</td><td><span class="badge badge-ok">Meʼyorda</span></td></tr>
          <tr><td>#BIN-104</td><td>Sanoat zonasi</td><td>Qora metall</td><td>85%</td><td><span class="badge badge-crit">Zudlik bilan olish</span></td></tr>
        </tbody>
      </table>
    </div>

    <footer>
      <p>Backend REST API: <a href="/docs" target="_blank">/docs (Swagger UI)</a> &middot; <a href="/api/v1/kategoriyalar" target="_blank">JSON Kategoriyalar</a></p>
    </footer>
  </div>

  <script>
    async function hisoblash() {
      const kwhPerTonne = document.getElementById("wasteType").value;
      const tonnes = document.getElementById("tonnes").value || 0;
      const res = await fetch(`/api/v1/tejalgan-energiya?qayta_ishlangan_tonna=${tonnes}&bir_tonna_uchun_kwh=${kwhPerTonne}`);
      const data = await res.json();
      const box = document.getElementById("natija");
      box.style.display = "block";
      box.innerHTML = `<strong>Natija:</strong><br>Tejalgan energiya: <b>${data.tejalgan_energiya_kwh.toLocaleString()} kWh</b> (${data.tejalgan_energiya_gwh} GWh)`;
    }
  </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def bosh_sahifa():
    return DASHBOARD_HTML

@app.get("/api/v1/holat")
def holatni_tekshirish():
    return {"holat": "ishlamoqda", "xizmat": "Aqlli chiqindilarni qayta ishlash tizimi"}

@app.get("/api/v1/kategoriyalar")
def kategoriyalar_royxati():
    return {"kategoriyalar": CHIQINDI_KATEGORIYALARI}

@app.get("/api/v1/tejalgan-energiya")
def tejalgan_energiyani_hisoblash(qayta_ishlangan_tonna: float, bir_tonna_uchun_kwh: float):
    jami_kwh = qayta_ishlangan_tonna * bir_tonna_uchun_kwh
    return {
        "qayta_ishlangan_tonna": qayta_ishlangan_tonna,
        "tejalgan_energiya_kwh": round(jami_kwh, 2),
        "tejalgan_energiya_gwh": round(jami_kwh / 1_000_000, 4),
    }
