#!/usr/bin/env python3
"""
Ablation check requested directly in response to "I want publishable results,
valid and accurate; no fake": the flow/runoff harvester term in corridor_sim.py
is ENTIRELY FABRICATED (Topic Analysis.md Section 10.4 confirms no open dataset
exists anywhere to ground it; it is currently just random.uniform(0.5, 5.0) mW
on stress days). This script sets that term to exactly zero and re-runs a
representative subset of the sensitivity grid (50 seeds each) to check whether
the headline finding -- brokering helps more on stress days than non-stress
days -- survives with the fabricated component completely removed.

If the finding does NOT survive, that is the honest result to report, not
something to paper over.
"""

import sys
import os
import statistics

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import corridor_sim as cs
import sensitivity_sweep as sw

# Monkey-patch the flow harvester to always return 0 -- remove the fabricated
# component entirely rather than just disclosing it.
def flow_mw_zero(sustained_overcast, env_rng):
    return 0.0

cs.flow_mw = flow_mw_zero


def main():
    print("Loading real data once...")
    piezo = cs.load_piezo_power_draws()
    low = cs.load_low_power_draws()
    solar = cs.load_solar_days()
    print(f"  piezo draws: {len(piezo)}, solar days: {len(solar)}")
    print()
    print("FLOW HARVESTER TERM SET TO EXACTLY ZERO (ablation of the fabricated component)")
    print()

    # Representative subset: same panel_eff=0.15 and 0.20 (the two "middle"
    # settings) across all 4 buffer_hours values, 50 seeds each -- 8 points,
    # matching corresponding rows in the full sweep for direct comparison.
    points = [(0.15, b) for b in [0.5, 1.0, 2.0, 4.0]] + [(0.20, b) for b in [0.5, 1.0, 2.0, 4.0]]

    sw.PIEZO_DRAWS = piezo
    sw.LOW_DRAWS = low
    sw.SOLAR_DAYS = solar

    print(f"{'panel_eff':>9s} {'buf_hrs':>8s} {'base_dark%':>14s} {'fullnet_base%':>16s} {'fullnet_treat%':>16s} "
          f"{'stress_chg%':>16s} {'nonstr_chg%':>16s} {'brokers':>8s}")
    results = []
    for pe, bh in points:
        r = sw.run_point(pe, bh)
        results.append(r)
        print(f"{r['panel_eff']:>9.2f} {r['buffer_hours']:>8.1f} "
              f"{r['baseline_dark_pct_mean']:>7.2f}+-{r['baseline_dark_pct_sd']:<5.2f} "
              f"{r['full_net_baseline_mean']:>8.2f}+-{r['full_net_baseline_sd']:<5.2f} "
              f"{r['full_net_treatment_mean']:>8.2f}+-{r['full_net_treatment_sd']:<5.2f} "
              f"{r['stress_change_mean']:>8.2f}+-{r['stress_change_sd']:<5.2f} "
              f"{r['nonstress_change_mean']:>8.2f}+-{r['nonstress_change_sd']:<5.2f} "
              f"{r['broker_events_mean']:>8.1f}")

    print()
    count = sum(1 for r in results if r["stress_change_mean"] < r["nonstress_change_mean"])
    print(f"Stress-day benefit > non-stress-day benefit: {count} / {len(results)} points (with flow harvester REMOVED)")


if __name__ == "__main__":
    main()
