#!/usr/bin/env python3
"""
Build the IT-spend time series chart and summary from it_spend.csv.

"IT spend" = total operating expenses of the City of Troy's Information
Technology internal service fund, as reported in each ACFR's Internal Service
Funds combining statement (FY2005-FY2025). This figure includes depreciation
and excludes capital asset purchases (which flow through the fund's balance
sheet / cash-flow statement, not operating expenses).

Outputs: it_spend_chart.png  and a printed summary table.
"""
import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

HERE = os.path.dirname(os.path.abspath(__file__))

rows = []
with open(os.path.join(HERE, "it_spend.csv")) as f:
    for r in csv.DictReader(f):
        rows.append((int(r["fiscal_year"]),
                     int(r["it_operating_expenses"]),
                     int(r["it_operating_revenues"])))
rows.sort()
years = [r[0] for r in rows]
exp = [r[1] for r in rows]
rev = [r[2] for r in rows]

# ---- chart ----------------------------------------------------------------
fig, ax = plt.subplots(figsize=(12, 6))
ax.bar([y - 0.2 for y in years], exp, width=0.4, label="Operating expenses (IT spend)",
       color="#1f77b4")
ax.bar([y + 0.2 for y in years], rev, width=0.4, label="Operating revenues (charges billed)",
       color="#aec7e8")
ax.set_title("City of Troy — Information Technology Internal Service Fund\n"
             "Operating expenses & revenues, FY2005–FY2025 (from ACFRs)", fontsize=13)
ax.set_xlabel("Fiscal year (ended June 30)")
ax.set_ylabel("Dollars")
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"${v/1e6:.1f}M"))
ax.set_xticks(years)
ax.set_xticklabels([f"'{y % 100:02d}" for y in years])
ax.legend()
ax.grid(axis="y", alpha=0.3)
ax.margins(x=0.01)
fig.tight_layout()
out_png = os.path.join(HERE, "it_spend_chart.png")
fig.savefig(out_png, dpi=130)
print(f"Wrote {out_png}")

# ---- summary --------------------------------------------------------------
first_y, first_e = years[0], exp[0]
last_y, last_e = years[-1], exp[-1]
n = last_y - first_y
cagr = (last_e / first_e) ** (1 / n) - 1
peak_y, peak_e = max(rows, key=lambda r: r[1])[0], max(exp)
low_y, low_e = min(rows, key=lambda r: r[1])[0], min(exp)

print(f"""
================  City of Troy — IT internal service fund  ================
   "IT spend" = IT internal service fund TOTAL OPERATING EXPENSES per ACFR
   (includes depreciation; excludes capital asset purchases)

   {'FY':<6}{'Operating expenses':>20}{'YoY':>9}{'Operating revenues':>22}""")
prev = None
for y, e, r in rows:
    yoy = f"{(e/prev-1)*100:+.1f}%" if prev else "   --"
    print(f"   {y:<6}{'$'+format(e,','):>20}{yoy:>9}{'$'+format(r,','):>22}")
    prev = e
print(f"""
   FY{first_y}: ${first_e:,}   ->   FY{last_y}: ${last_e:,}
   Total change over {n} years : {(last_e/first_e-1)*100:+.0f}%   (CAGR {cagr*100:.1f}%/yr)
   Peak: FY{peak_y} ${peak_e:,}   |   Low: FY{low_y} ${low_e:,}
   (for comparison, US CPI rose ~67% over FY2005-FY2025, ~2.6%/yr)
============================================================================""")
