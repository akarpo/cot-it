#!/usr/bin/env python3
"""Build the IT assets / endpoints / asset-spend chart from it_assets.csv.

Two panels, shared fiscal-year axis (FY2004-FY2026):
  top    — counts IT maintains: applications, PCs, printers, servers
  bottom — IT asset spend: adopted capital budget + equipment maintenance cost

Source: City of Troy Adopted Budget "Performance Indicators" tables. See
extract_it_assets.py for per-figure provenance and caveats.

Output: it_assets_chart.png  and a printed summary.
"""
import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

HERE = os.path.dirname(os.path.abspath(__file__))


def num(x):
    return int(x) if x not in ("", None) else None


rows = []
with open(os.path.join(HERE, "it_assets.csv")) as f:
    for r in csv.DictReader(f):
        rows.append({k: (int(v) if v not in ("", None) and k != "fiscal_year"
                         else (int(v) if k == "fiscal_year" else None))
                     for k, v in r.items()})
rows.sort(key=lambda r: r["fiscal_year"])
yrs = [r["fiscal_year"] for r in rows]


def series(key):
    return [r[key] for r in rows]


def plot_line(ax, key, label, **kw):
    xs = [y for y, r in zip(yrs, rows) if r[key] is not None]
    ys = [r[key] for r in rows if r[key] is not None]
    ax.plot(xs, ys, marker="o", ms=3, label=label, **kw)


fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 9), sharex=True)

# ---- top: what IT maintains ----------------------------------------------
plot_line(ax1, "personal_computers", "Personal computers", color="#1f77b4")
plot_line(ax1, "applications_supported", "Applications supported", color="#d62728")
plot_line(ax1, "printers", "Printers", color="#2ca02c")
plot_line(ax1, "servers", "Servers", color="#ff7f0e")
ax1.set_title("City of Troy — IT department: assets maintained & applications "
              "supported\n(from Adopted Budget Performance Indicators, "
              "FY2004–FY2026)", fontsize=13)
ax1.set_ylabel("Count")
ax1.legend(ncol=2, fontsize=9)
ax1.grid(alpha=0.3)
ax1.annotate("printers & servers\nfirst reported FY2014", xy=(2014, 60),
             xytext=(2009.3, 250), fontsize=8, color="#555",
             arrowprops=dict(arrowstyle="->", color="#999"))

# ---- bottom: IT asset spend ----------------------------------------------
cap_x = [y for y, r in zip(yrs, rows) if r["it_capital_budget_adopted"]]
cap_y = [r["it_capital_budget_adopted"] for r in rows
         if r["it_capital_budget_adopted"]]
ax2.bar(cap_x, cap_y, width=0.6, color="#9467bd",
        label="IT capital budget (adopted)")
act_x = [y for y, r in zip(yrs, rows) if r["isf_capital_actual"]]
act_y = [r["isf_capital_actual"] for r in rows if r["isf_capital_actual"]]
ax2.scatter(act_x, act_y, color="#000", zorder=5, s=28,
            label="ISF capital actually booked (sporadic)")
plot_line(ax2, "equipment_maintenance_cost", "Equipment maintenance cost",
          color="#8c564b")
ax2.set_title("IT asset spend: adopted capital budget vs. equipment "
              "maintenance cost", fontsize=12)
ax2.set_ylabel("Dollars")
ax2.set_xlabel("Fiscal year (ended June 30)")
ax2.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"${v/1e3:.0f}k"))
ax2.set_xticks(yrs)
ax2.set_xticklabels([f"'{y % 100:02d}" for y in yrs])
ax2.legend(fontsize=9)
ax2.grid(axis="y", alpha=0.3)
ax2.margins(x=0.01)

fig.tight_layout()
out = os.path.join(HERE, "it_assets_chart.png")
fig.savefig(out, dpi=130)
print(f"Wrote {out}")

# ---- summary --------------------------------------------------------------
def span(key):
    pts = [(r["fiscal_year"], r[key]) for r in rows if r[key] is not None]
    return pts[0], pts[-1]

print("\n=============  City of Troy IT — assets, endpoints, asset spend  "
      "=============")
for key, lbl in [("applications_supported", "Applications supported"),
                 ("personal_computers", "Personal computers"),
                 ("printers", "Printers"),
                 ("servers", "Servers")]:
    (fy0, v0), (fy1, v1) = span(key)
    print(f"  {lbl:<24} FY{fy0}: {v0:>6}  ->  FY{fy1}: {v1:>6}   "
          f"({(v1/v0-1)*100:+.0f}%)")
caps = [r["it_capital_budget_adopted"] for r in rows
        if r["it_capital_budget_adopted"]]
print(f"  {'IT capital budget':<24} adopted total FY2008–FY2026: "
      f"${sum(caps):,}  (avg ${sum(caps)//len(caps):,}/yr)")
em = [r["equipment_maintenance_cost"] for r in rows
      if r["equipment_maintenance_cost"]]
print(f"  {'Equipment maintenance':<24} ranged ${min(em):,}–${max(em):,}/yr")
print("=" * 78)
