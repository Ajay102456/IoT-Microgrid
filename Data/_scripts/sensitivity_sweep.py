#!/usr/bin/env python3
"""
Sensitivity sweep over corridor_sim.py's two most consequential ASSUMED
parameters: PV panel efficiency and energy-buffer sizing (hours of demand
bridged). Purpose: check whether the Section 13.6 finding (brokering's
benefit concentrates on correlated stress days, not non-stress days) is
robust across the assumption space, or an artifact of one arbitrary choice
-- and find the point at which baseline dark-fraction becomes "reasonable"
(i.e., stops being dominated by chronic under-provisioning).

Reuses corridor_sim's real-data loaders and simulation engine; overrides its
module-level ASSUMED constants per sweep point (PANEL_EFF, BUFFER_HOURS and
the thresholds derived from it) before each run.

SEEDS PER RUN: each (panel_eff, buffer_hours) point is run across N_SEEDS
independent seeds (not just 1), and this script reports the mean and stdev
across seeds -- a single-seed result cannot distinguish a genuine effect
from noise specific to that one random realization. The original Section
13.6 result (corridor_sim.py run directly) used only seed=42 and should be
read as one realization, not a statistically validated mean; this sweep
corrects that for every point it covers.
"""

import statistics
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import corridor_sim as cs

N_SEEDS = 50
# Deterministic list of 50 distinct seeds, generated once from a fixed master
# seed so this sweep itself is reproducible.
SEEDS = list(__import__("random").Random(0).sample(range(1, 10_000_000), 50))


def run_point(panel_eff, buffer_hours):
    cs.PANEL_EFF = panel_eff
    cs.BUFFER_HOURS = buffer_hours
    cs.BUFFER_CAPACITY_MWH = cs.DEMAND_MW * buffer_hours
    cs.UPPER_THRESH = 0.80 * cs.BUFFER_CAPACITY_MWH
    cs.LOWER_THRESH = 0.20 * cs.BUFFER_CAPACITY_MWH

    baseline_dark_pcts, full_net_bases, full_net_treats = [], [], []
    stress_changes, nonstress_changes, broker_counts = [], [], []

    for seed in SEEDS[:N_SEEDS]:
        baseline = cs.run_simulation(SOLAR_DAYS, PIEZO_DRAWS, LOW_DRAWS, brokering_enabled=False, seed=seed)
        treatment = cs.run_simulation(SOLAR_DAYS, PIEZO_DRAWS, LOW_DRAWS, brokering_enabled=True, seed=seed)

        total = baseline["total_minutes"] * cs.N_NODES
        baseline_dark_pcts.append(100.0 * sum(baseline["per_node_dark_minutes"]) / total)
        full_net_bases.append(baseline["full_network_covered_pct"])
        full_net_treats.append(treatment["full_network_covered_pct"])

        bs = sum(baseline["per_node_dark_stress"]); ts = sum(treatment["per_node_dark_stress"])
        bn = sum(baseline["per_node_dark_nonstress"]); tn = sum(treatment["per_node_dark_nonstress"])
        stress_changes.append(100.0 * (ts - bs) / bs if bs else 0.0)
        nonstress_changes.append(100.0 * (tn - bn) / bn if bn else 0.0)
        broker_counts.append(treatment["total_broker_events"])

    def m(lst):
        return statistics.mean(lst)

    def s(lst):
        return statistics.stdev(lst) if len(lst) > 1 else 0.0

    return {
        "panel_eff": panel_eff,
        "buffer_hours": buffer_hours,
        "n_seeds": N_SEEDS,
        "baseline_dark_pct_mean": m(baseline_dark_pcts), "baseline_dark_pct_sd": s(baseline_dark_pcts),
        "full_net_baseline_mean": m(full_net_bases), "full_net_baseline_sd": s(full_net_bases),
        "full_net_treatment_mean": m(full_net_treats), "full_net_treatment_sd": s(full_net_treats),
        "stress_change_mean": m(stress_changes), "stress_change_sd": s(stress_changes),
        "nonstress_change_mean": m(nonstress_changes), "nonstress_change_sd": s(nonstress_changes),
        "broker_events_mean": m(broker_counts),
    }


if __name__ == "__main__":
    print("Loading real data once...")
    PIEZO_DRAWS = cs.load_piezo_power_draws()
    LOW_DRAWS = cs.load_low_power_draws()
    SOLAR_DAYS = cs.load_solar_days()
    print(f"  piezo draws: {len(PIEZO_DRAWS)}, solar days: {len(SOLAR_DAYS)}")
    print()

    panel_effs = [0.10, 0.15, 0.20, 0.30]
    buffer_hours_list = [0.5, 1.0, 2.0, 4.0]
    print(f"Grid: {len(panel_effs)} x {len(buffer_hours_list)} points, {N_SEEDS} seeds each, "
          f"2 conditions = {len(panel_effs)*len(buffer_hours_list)*N_SEEDS*2} total full-year runs")
    print()

    print(f"{'panel_eff':>9s} {'buf_hrs':>8s} {'base_dark%':>14s} {'fullnet_base%':>16s} {'fullnet_treat%':>16s} "
          f"{'stress_chg%':>16s} {'nonstr_chg%':>16s} {'brokers':>8s}")
    results = []
    for pe in panel_effs:
        for bh in buffer_hours_list:
            r = run_point(pe, bh)
            results.append(r)
            print(f"{r['panel_eff']:>9.2f} {r['buffer_hours']:>8.1f} "
                  f"{r['baseline_dark_pct_mean']:>7.2f}+-{r['baseline_dark_pct_sd']:<5.2f} "
                  f"{r['full_net_baseline_mean']:>8.2f}+-{r['full_net_baseline_sd']:<5.2f} "
                  f"{r['full_net_treatment_mean']:>8.2f}+-{r['full_net_treatment_sd']:<5.2f} "
                  f"{r['stress_change_mean']:>8.2f}+-{r['stress_change_sd']:<5.2f} "
                  f"{r['nonstress_change_mean']:>8.2f}+-{r['nonstress_change_sd']:<5.2f} "
                  f"{r['broker_events_mean']:>8.1f}")

    print()
    print("Summary: in how many of the", len(results), "sweep points does brokering help MORE (on mean) on stress days than non-stress days?")
    count = sum(1 for r in results if r["stress_change_mean"] < r["nonstress_change_mean"])
    print(f"  {count} / {len(results)} points show stress-day benefit > non-stress-day benefit")
    print()
    print("Full results list:")
    for r in results:
        print(" ", r)
