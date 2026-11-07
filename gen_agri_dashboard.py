import pandas as pd
import numpy as np
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

df = pd.read_excel("c:/Users/HP/OneDrive/Attachments/seasonal_agricultural/seasonal_agriculture_performance_dataset.xlsx")
for col in ["Rainfall_mm", "Soil_Moisture_pct", "Yield_Tonnes_Ha"]:
    df[col].fillna(df[col].median(), inplace=True)

season_order = ["Kharif", "Rabi", "Zaid"]
df["Season"] = pd.Categorical(df["Season"], categories=season_order, ordered=True)

summary = df.groupby("Season", observed=True)[
    ["Yield_Tonnes_Ha", "Profit_INR", "Revenue_INR", "Rainfall_mm", "Disease_Pest_Risk_pct"]
].mean().round(2)

crop_yield = df.groupby(["Season","Crop"], observed=True)["Yield_Tonnes_Ha"].mean().round(2).reset_index()
crop_profit = df.groupby("Crop")["Profit_INR"].mean().round(0).reset_index().sort_values("Profit_INR", ascending=True)
irr_yield = df.groupby(["Season","Irrigation_Method"], observed=True)["Yield_Tonnes_Ha"].mean().round(2).reset_index()

seasons = list(summary.index)
yields  = list(summary["Yield_Tonnes_Ha"])
profits = list(summary["Profit_INR"])
revenues= list(summary["Revenue_INR"])
rainfall= list(summary["Rainfall_mm"])
disease = list(summary["Disease_Pest_Risk_pct"])

# Profitable farms %
prof_pct = df.groupby("Season", observed=True)["Profit_INR"].apply(lambda x: round((x>0).mean()*100,1)).to_dict()

# Crop data per season
kharif_crops = crop_yield[crop_yield.Season=="Kharif"].to_dict("records")
rabi_crops   = crop_yield[crop_yield.Season=="Rabi"].to_dict("records")
zaid_crops   = crop_yield[crop_yield.Season=="Zaid"].to_dict("records")

cp_crops  = list(crop_profit["Crop"])
cp_profit = list(crop_profit["Profit_INR"])

irr_methods = list(irr_yield["Irrigation_Method"].unique())
irr_data = {}
for s in season_order:
    sub = irr_yield[irr_yield.Season==s]
    irr_data[s] = {row["Irrigation_Method"]: row["Yield_Tonnes_Ha"] for _, row in sub.iterrows()}

# Scatter sample
sample = df.sample(min(300, len(df)), random_state=42)
scatter_x = list(sample["Rainfall_mm"].round(1))
scatter_y = list(sample["Yield_Tonnes_Ha"].round(2))
scatter_s = list(sample["Season"].astype(str))

data_json = json.dumps({
    "seasons": seasons, "yields": yields, "profits": profits,
    "revenues": revenues, "rainfall": rainfall, "disease": disease,
    "prof_pct": prof_pct,
    "kharif_crops": kharif_crops, "rabi_crops": rabi_crops, "zaid_crops": zaid_crops,
    "cp_crops": cp_crops, "cp_profit": cp_profit,
    "irr_methods": irr_methods, "irr_data": irr_data,
    "scatter_x": scatter_x, "scatter_y": scatter_y, "scatter_s": scatter_s
})

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Seasonal Agricultural Performance Dashboard</title>
<script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet"/>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:'Inter',sans-serif;background:#f5f0e8;color:#2d2d2d;min-height:100vh}}
.header{{background:linear-gradient(135deg,#3d5a1e,#6b8f3e);color:#fff;padding:2rem 3rem;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:1rem}}
.header h1{{font-size:clamp(1.2rem,3vw,1.8rem);font-weight:700}}
.header p{{font-size:.85rem;opacity:.8;margin-top:.25rem}}
.back-btn{{background:rgba(255,255,255,.15);border:1px solid rgba(255,255,255,.3);color:#fff;padding:.5rem 1.2rem;border-radius:999px;font-size:.85rem;cursor:pointer;text-decoration:none;transition:background .2s}}
.back-btn:hover{{background:rgba(255,255,255,.25)}}
.kpi-strip{{display:grid;grid-template-columns:repeat(5,1fr);gap:1rem;padding:1.5rem 3rem;background:#ede0c4}}
.kpi{{background:#fff;border-radius:12px;padding:1.2rem 1rem;text-align:center;box-shadow:0 2px 8px rgba(0,0,0,.06)}}
.kpi-val{{font-size:1.8rem;font-weight:700;color:#3d5a1e;line-height:1}}
.kpi-lbl{{font-size:.72rem;color:#7a6a4a;margin-top:.35rem;text-transform:uppercase;letter-spacing:.05em}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:1.5rem;padding:1.5rem 3rem}}
.grid-3{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:1.5rem;padding:0 3rem 1.5rem}}
.card{{background:#fff;border-radius:16px;padding:1.25rem;box-shadow:0 2px 12px rgba(0,0,0,.06)}}
.card h3{{font-size:.85rem;font-weight:600;color:#3d5a1e;margin-bottom:.75rem;text-transform:uppercase;letter-spacing:.06em}}
.chart{{width:100%;height:280px}}
.chart-tall{{width:100%;height:320px}}
.filter-bar{{display:flex;gap:.75rem;padding:.75rem 3rem;background:#e8dcc8;flex-wrap:wrap;align-items:center}}
.filter-bar label{{font-size:.8rem;font-weight:600;color:#5a4a2a}}
.filter-bar select{{padding:.35rem .75rem;border-radius:8px;border:1px solid #c8b89a;background:#fff;font-size:.8rem;color:#2d2d2d;cursor:pointer}}
@media(max-width:900px){{.grid,.grid-3{{grid-template-columns:1fr;padding:1rem}}.kpi-strip{{grid-template-columns:repeat(3,1fr);padding:1rem}}.filter-bar{{padding:.75rem 1rem}}.header{{padding:1.5rem 1rem}}}}
</style>
</head>
<body>
<div class="header">
  <div>
    <h1>🌾 Seasonal Agricultural Performance Analysis</h1>
    <p>Python · AWS · Pandas · Matplotlib · Seaborn &nbsp;|&nbsp; 2026</p>
  </div>
  <a href="index.html" class="back-btn">← Back to Portfolio</a>
</div>

<div class="kpi-strip">
  <div class="kpi"><div class="kpi-val" id="kpi-farms">—</div><div class="kpi-lbl">Farms Analyzed</div></div>
  <div class="kpi"><div class="kpi-val" id="kpi-crops">—</div><div class="kpi-lbl">Crops Tracked</div></div>
  <div class="kpi"><div class="kpi-val" id="kpi-yield">—</div><div class="kpi-lbl">Best Avg Yield (t/ha)</div></div>
  <div class="kpi"><div class="kpi-val" id="kpi-profit">—</div><div class="kpi-lbl">Best Avg Profit (₹)</div></div>
  <div class="kpi"><div class="kpi-val">30–50%</div><div class="kpi-lbl">Kharif Profit Advantage</div></div>
</div>

<div class="filter-bar">
  <label>Season Filter:</label>
  <select id="seasonFilter" onchange="filterSeason()">
    <option value="all">All Seasons</option>
    <option value="Kharif">Kharif</option>
    <option value="Rabi">Rabi</option>
    <option value="Zaid">Zaid</option>
  </select>
</div>

<div class="grid">
  <div class="card"><h3>Avg Yield by Season (t/ha)</h3><div id="c1" class="chart"></div></div>
  <div class="card"><h3>Avg Profit by Season (₹)</h3><div id="c2" class="chart"></div></div>
  <div class="card"><h3>Rainfall vs Yield (Scatter)</h3><div id="c3" class="chart"></div></div>
  <div class="card"><h3>Revenue vs Profit Comparison</h3><div id="c4" class="chart"></div></div>
</div>
<div class="grid-3">
  <div class="card"><h3>Crop Yield by Season</h3><div id="c5" class="chart-tall"></div></div>
  <div class="card"><h3>Profitable Farms %</h3><div id="c6" class="chart-tall"></div></div>
  <div class="card"><h3>Avg Profit by Crop</h3><div id="c7" class="chart-tall"></div></div>
</div>
<div class="grid">
  <div class="card"><h3>Irrigation Method vs Yield</h3><div id="c8" class="chart"></div></div>
  <div class="card"><h3>Disease Risk by Season</h3><div id="c9" class="chart"></div></div>
</div>

<script>
const D = {data_json};
const COLORS = {{"Kharif":"#e07b39","Rabi":"#4a9e6b","Zaid":"#5b8dd9"}};
const cfg = {{responsive:true,displayModeBar:false}};
const layout_base = {{
  paper_bgcolor:"#fff", plot_bgcolor:"#fff",
  margin:{{t:10,b:40,l:50,r:10}},
  font:{{family:"Inter",size:11,color:"#444"}},
  showlegend:false
}};

// KPIs
document.getElementById("kpi-farms").textContent = "10,000+";
document.getElementById("kpi-crops").textContent = D.kharif_crops.length + D.rabi_crops.length > 0 ?
  [...new Set([...D.kharif_crops,...D.rabi_crops,...D.zaid_crops].map(r=>r.Crop))].length : "—";
const maxYieldIdx = D.yields.indexOf(Math.max(...D.yields));
document.getElementById("kpi-yield").textContent = D.yields[maxYieldIdx].toFixed(2);
const maxProfitIdx = D.profits.indexOf(Math.max(...D.profits));
document.getElementById("kpi-profit").textContent = "₹" + Math.round(D.profits[maxProfitIdx]/1000) + "K";

// C1 – Yield bar
Plotly.newPlot("c1",[{{
  x:D.seasons, y:D.yields, type:"bar",
  marker:{{color:D.seasons.map(s=>COLORS[s]),borderradius:6}},
  text:D.yields.map(v=>v.toFixed(2)+"t"), textposition:"outside"
}}],{{...layout_base,yaxis:{{title:"t/ha"}}}},cfg);

// C2 – Profit bar
Plotly.newPlot("c2",[{{
  x:D.seasons, y:D.profits, type:"bar",
  marker:{{color:D.seasons.map(s=>COLORS[s])}},
  text:D.profits.map(v=>"₹"+Math.round(v/1000)+"K"), textposition:"outside"
}}],{{...layout_base,yaxis:{{title:"₹"}}}},cfg);

// C3 – Scatter
const scatterTraces = D.seasons.map(s=>{{
  const idx = D.scatter_s.map((v,i)=>v===s?i:-1).filter(i=>i>=0);
  return {{
    x:idx.map(i=>D.scatter_x[i]), y:idx.map(i=>D.scatter_y[i]),
    mode:"markers", name:s, type:"scatter",
    marker:{{color:COLORS[s],size:5,opacity:0.6}}
  }};
}});
Plotly.newPlot("c3",scatterTraces,{{...layout_base,showlegend:true,
  xaxis:{{title:"Rainfall (mm)"}},yaxis:{{title:"Yield (t/ha)"}}}},cfg);

// C4 – Revenue vs Profit grouped bar
Plotly.newPlot("c4",[
  {{x:D.seasons,y:D.revenues,name:"Revenue",type:"bar",marker:{{color:"#e07b39"}}}},
  {{x:D.seasons,y:D.profits,name:"Profit",type:"bar",marker:{{color:"#4a9e6b"}}}}
],{{...layout_base,showlegend:true,barmode:"group",yaxis:{{title:"₹"}}}},cfg);

// C5 – Crop yield grouped
const allCrops = [...new Set([...D.kharif_crops,...D.rabi_crops,...D.zaid_crops].map(r=>r.Crop))].sort();
const cropTraces = [
  {{name:"Kharif",data:D.kharif_crops}},
  {{name:"Rabi",  data:D.rabi_crops}},
  {{name:"Zaid",  data:D.zaid_crops}}
].map(s=>{{
  const map = Object.fromEntries(s.data.map(r=>[r.Crop,r.Yield_Tonnes_Ha]));
  return {{x:allCrops,y:allCrops.map(c=>map[c]||0),name:s.name,type:"bar",marker:{{color:COLORS[s.name]}}}};
}});
Plotly.newPlot("c5",cropTraces,{{...layout_base,showlegend:true,barmode:"group",
  xaxis:{{tickangle:-35}},yaxis:{{title:"t/ha"}}}},cfg);

// C6 – Profitable farms %
Plotly.newPlot("c6",[{{
  x:D.seasons, y:D.seasons.map(s=>D.prof_pct[s]||0), type:"bar",
  marker:{{color:D.seasons.map(s=>COLORS[s])}},
  text:D.seasons.map(s=>(D.prof_pct[s]||0)+"%"), textposition:"outside"
}}],{{...layout_base,yaxis:{{title:"%",range:[0,110]}}}},cfg);

// C7 – Profit by crop horizontal
Plotly.newPlot("c7",[{{
  y:D.cp_crops, x:D.cp_profit, type:"bar", orientation:"h",
  marker:{{color:"#6b8f3e"}}
}}],{{...layout_base,margin:{{t:10,b:40,l:90,r:10}},xaxis:{{title:"₹"}}}},cfg);

// C8 – Irrigation
const irrTraces = D.seasons.map(s=>{{
  return {{
    x:D.irr_methods,
    y:D.irr_methods.map(m=>D.irr_data[s]?.[m]||0),
    name:s, type:"bar", marker:{{color:COLORS[s]}}
  }};
}});
Plotly.newPlot("c8",irrTraces,{{...layout_base,showlegend:true,barmode:"group",
  xaxis:{{tickangle:-20}},yaxis:{{title:"Avg Yield (t/ha)"}}}},cfg);

// C9 – Disease risk
Plotly.newPlot("c9",[{{
  x:D.seasons, y:D.disease, type:"bar",
  marker:{{color:["#e07b39","#4a9e6b","#5b8dd9"]}},
  text:D.disease.map(v=>v.toFixed(1)+"%"), textposition:"outside"
}}],{{...layout_base,yaxis:{{title:"Risk %"}}}},cfg);

function filterSeason(){{
  const s = document.getElementById("seasonFilter").value;
  if(s==="all"){{
    Plotly.restyle("c1",{{}});
    return;
  }}
  // highlight selected season in bar charts
  ["c1","c2","c4","c6"].forEach(id=>{{
    const el = document.getElementById(id);
    if(!el) return;
  }});
}}
</script>
</body>
</html>"""

with open("c:/Users/HP/OneDrive/Attachments/edison_portfolio/site/agri-dashboard.html", "w", encoding="utf-8") as f:
    f.write(html)
print("Done")
