#!/usr/bin/env python3
"""Generate real figures from the actual 50-seed sweep data (Table in manuscript),
not illustrative/fake placeholders. Data transcribed exactly from sweep_output.txt."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# Exact data from Data/_scripts/sweep_output.txt
panel_effs = [0.10, 0.15, 0.20, 0.30]
buffer_hours = [0.5, 1.0, 2.0, 4.0]

stress_change = {
    0.10: [-32.69, -20.75, -9.36, -2.60],
    0.15: [-32.16, -20.62, -10.18, -4.40],
    0.20: [-31.79, -20.25, -10.01, -4.84],
    0.30: [-31.21, -19.82, -9.93, -3.11],
}
stress_sd = {
    0.10: [1.22, 1.09, 1.50, 1.08],
    0.15: [1.48, 1.53, 1.61, 1.67],
    0.20: [1.46, 1.87, 2.04, 3.30],
    0.30: [1.61, 2.20, 2.52, 3.03],
}
baseline_dark = {
    0.10: [50.92, 48.14, 46.59, 45.17],
    0.15: [37.69, 34.52, 28.79, 13.04],
    0.20: [31.40, 28.09, 20.90, 6.43],
    0.30: [24.05, 20.80, 12.04, 2.29],
}

fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

colors = {0.10: "#1b9e77", 0.15: "#d95f02", 0.20: "#7570b3", 0.30: "#e7298a"}

ax = axes[0]
for pe in panel_effs:
    ax.errorbar(buffer_hours, stress_change[pe], yerr=stress_sd[pe],
                marker='o', capsize=3, label=f"panel eff. = {pe}", color=colors[pe])
ax.set_xlabel("Energy buffer (hours of demand)")
ax.set_ylabel("Stress-day dark-time change (%)")
ax.set_title("(a) Duty-brokering effect across the sweep")
ax.axhline(0, color='gray', linewidth=0.8, linestyle='--')
ax.legend(fontsize=8)
ax.grid(alpha=0.3)

ax2 = axes[1]
for pe in panel_effs:
    ax2.plot(buffer_hours, baseline_dark[pe], marker='s', label=f"panel eff. = {pe}", color=colors[pe])
ax2.set_xlabel("Energy buffer (hours of demand)")
ax2.set_ylabel("Baseline dark-time (%)")
ax2.set_title("(b) Baseline resource constraint level")
ax2.legend(fontsize=8)
ax2.grid(alpha=0.3)

plt.tight_layout()
plt.savefig("/home/s/Documents/MicroGrid-IoT/LaTeX/fig_sweep.pdf", dpi=300, bbox_inches='tight')
print("Wrote fig_sweep.pdf")

# Event cross-check figure: real percentile data
fig2, ax3 = plt.subplots(figsize=(7, 4.5))
events = ["Cameron Highlands\n6 Jan 2025", "Cameron Highlands\n21 Sep 2024",
          "Batang Kali\n16 Dec 2022", "Hulu Langat\n21 May 2011"]
rain_pctl = [95.6, 8.2, 63.9, 70.5]
solar_pctl = [11.8, None, 91.8, 36.1]  # Sep 2024 reported within-window pctl differently; show rain only where solar pctl unavailable
# For event 2 we only have the within-window same-day rain percentile value from the cross-check
x = np.arange(len(events))
width = 0.35
rain_bars = ax3.bar(x - width/2, rain_pctl, width, label="Rainfall percentile (same day)", color="#2166ac")
solar_vals = [v if v is not None else 0 for v in solar_pctl]
solar_bars = ax3.bar(x + width/2, solar_vals, width, label="Solar percentile (same day)", color="#f4a582")
ax3.axhline(50, color='gray', linewidth=0.8, linestyle='--', label="Median (50th pctl.)")
ax3.set_ylabel("Percentile within reference year/window")
ax3.set_title("Real weather conditions on four documented landslide event dates")
ax3.set_xticks(x)
ax3.set_xticklabels(events, fontsize=8)
ax3.legend(fontsize=8)
ax3.set_ylim(0, 105)
for i, v in enumerate(solar_pctl):
    if v is None:
        ax3.text(x[i] + width/2, 3, "N/A\n(same-day)", ha='center', fontsize=6)
plt.tight_layout()
plt.savefig("/home/s/Documents/MicroGrid-IoT/LaTeX/fig_events.pdf", dpi=300, bbox_inches='tight')
print("Wrote fig_events.pdf")
