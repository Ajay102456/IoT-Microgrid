#!/usr/bin/env python3
"""
Corridor-wide landslide-sensor-swarm simulation.

Compares BASELINE (independent per-node double-threshold switching, no utility
backup, replicating Lee & Wang 2024's logic under this project's no-grid
assumption) against TREATMENT (dual hazard-coupled harvesting + duty-brokering,
as proposed in Topic Analysis.md Section 7.3).

REAL DATA INPUTS (not synthetic):
  - Solar driver: full year 2025, 1-minute GHI, Kuala Lumpur (Mendeley
    10.17632/bgch4tw79k.1). File: Data/kl_solar_irradiance_bgch4tw79k/*.csv
  - Piezoelectric harvester power draws: real measured 'power' column values
    from 23 characterized experiments (Mendeley 10.17632/y4cmrsdv9f.1).
    File: Data/piezo_harvester_y4cmrsdv9f/post-processed_exp*.csv
  - Node power demand: 295.49 mW average, taken directly from Lee & Wang
    (2024) Table 2 (measured IoT device power over a 300s cycle).
  - Small PV panel area: 118mm x 70mm (0.00826 m^2), the exact YML-118X70MM
    panel dimensions named in Lee & Wang (2024) Section 2.2.1.

MODELED / ASSUMED (no real data exists for these; disclosed explicitly):
  - Multi-node spatial correlation structure: on days classified as
    "sustained-overcast" (real, per Section 11.2's zero-dip+low-peak
    criterion), ALL nodes share the identical regional GHI signal (rho=1,
    monsoon-front assumption). On other days, each node's GHI is the regional
    signal with an independent random local-cloud multiplicative mask
    (representing localized convective cells) -- this decorrelation
    probability (LOCAL_CLOUD_PROB) is an assumed parameter, not measured.
  - "Ground movement" / piezo-triggering process: modeled as a Bernoulli
    process per node per minute, with a higher probability on
    sustained-overcast days than on clear days (rain -> higher instability
    probability is a physically motivated but UNVALIDATED assumption -- no
    real geotechnical displacement data was available to calibrate this).
  - PV panel efficiency: assumed 15% (not stated in the reference paper,
    which reports only a lab charging curve, not efficiency).
  - Flow/runoff harvester: no open dataset exists anywhere for this (Topic
    Analysis.md Section 10.4/10.6); modeled via a simple literature-bounded
    power law (0 on dry days, ramping toward the ~0.1-5 mW range reported in
    Section 10.4's cited papers on sustained-overcast/rain days) as a
    placeholder, NOT a validated harvester model.
  - Energy-buffer abstraction: thresholds are expressed as % of an assumed
    1-hour-deficit-bridging capacity, NOT a literal replication of the
    reference paper's mF-scale capacitor circuit (which operates at
    sub-second timescales irrelevant to this minute-resolution simulation).
    True circuit-level fidelity belongs to the Stage 1 HIL testbed described
    in Topic Analysis.md Section 4, not this desktop-level simulation.

This script performs an actual computation of its own -- it is not re-stating
numbers from any cited source.
"""

import csv
import glob
import os
import random
import statistics

random.seed(42)  # fixed seed for reproducibility of this run

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOLAR_DIR = os.path.join(BASE, "kl_solar_irradiance_bgch4tw79k")
PIEZO_DIR = os.path.join(BASE, "piezo_harvester_y4cmrsdv9f")

N_NODES = 5
DEMAND_MW = 295.49          # Lee & Wang (2024) Table 2, real measured value
PANEL_AREA_M2 = 0.118 * 0.070  # YML-118X70MM, real panel dims from reference paper
PANEL_EFF = 0.15            # ASSUMED, not stated in reference paper
BUFFER_HOURS = 1.0          # ASSUMED design parameter (1-hour deficit bridge)
BUFFER_CAPACITY_MWH = DEMAND_MW * BUFFER_HOURS
UPPER_THRESH = 0.80 * BUFFER_CAPACITY_MWH
LOWER_THRESH = 0.20 * BUFFER_CAPACITY_MWH
LOCAL_CLOUD_PROB = 0.25     # ASSUMED per-minute localized-cloud-mask probability
LOCAL_CLOUD_ATTEN = 0.3     # ASSUMED attenuation factor when locally clouded
RAIN_DAY_MOVEMENT_P = 0.02  # ASSUMED per-minute movement probability on rain days
DRY_DAY_MOVEMENT_P = 0.002  # ASSUMED per-minute movement probability on dry days
BROKER_COOLDOWN_MIN = 30    # ASSUMED broker hand-off duration
LINK_SUCCESS_PROB = 0.89    # REAL figure: Chapungo et al. (2025) Mozambique PDR,
                             # used here as the lossy-link probability per attempt


def load_piezo_power_draws():
    """Return list of real instantaneous power values pooled from all 23
    characterized experiments (post-processed_exp*.csv 'power' column)."""
    draws = []
    for fn in sorted(glob.glob(os.path.join(PIEZO_DIR, "post-processed_exp*.csv"))):
        with open(fn, newline="") as f:
            r = csv.DictReader(f)
            for row in r:
                try:
                    draws.append(float(row["power"]))
                except (KeyError, ValueError):
                    pass
    return draws


def load_low_power_draws():
    """Subset: pooled draws from the single lowest-mean experiment (exp13),
    used to represent ambient/background (non-rain-day) vibration levels."""
    draws = []
    fn = os.path.join(PIEZO_DIR, "post-processed_exp13.csv")
    with open(fn, newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            try:
                draws.append(float(row["power"]))
            except (KeyError, ValueError):
                pass
    return draws


def load_solar_days():
    """Return list of (filename, ghi_list[720]) for all 365 real days,
    sorted by date, plus a per-day 'sustained_overcast' flag computed the
    same way as Topic Analysis.md Section 11.2 (zero cloud-transient dips
    AND peak below the year's median peak)."""
    files = sorted(glob.glob(os.path.join(SOLAR_DIR, "*.csv")))
    days = []
    peaks = []
    for fn in files:
        vals = []
        with open(fn, newline="") as f:
            r = csv.DictReader(f)
            for row in r:
                try:
                    vals.append(float(row["SolarIrradianceWm2"]))
                except (KeyError, ValueError):
                    pass
        if not vals:
            continue
        days.append((os.path.basename(fn), vals))
        daytime = [v for v in vals if v > 0]
        peaks.append(max(daytime) if daytime else 0)

    median_peak = statistics.median(peaks)
    out = []
    for (fn, vals), peak in zip(days, peaks):
        dips = 0
        for i in range(1, len(vals)):
            if vals[i - 1] > 0.3 * peak and vals[i] < vals[i - 1] - 0.4 * peak:
                dips += 1
        sustained_overcast = (dips == 0) and (peak < median_peak)
        out.append({"file": fn, "ghi": vals, "sustained_overcast": sustained_overcast})
    return out


def ghi_to_solar_mw(ghi_wm2):
    return ghi_wm2 * PANEL_AREA_M2 * PANEL_EFF * 1000.0  # W/m2 * m2 * eff -> W -> mW


def flow_mw(sustained_overcast, env_rng):
    # ASSUMED literature-bounded placeholder (Section 10.4 cited range ~0.1-5 mW)
    return env_rng.uniform(0.5, 5.0) if sustained_overcast else 0.0


class Node:
    def __init__(self, idx):
        self.idx = idx
        self.buffer = 0.6 * BUFFER_CAPACITY_MWH  # start at 60% charge
        self.covered_by_neighbor_until = -1
        self.being_covered_for = None
        self.reporting_minutes = 0
        self.covered_minutes = 0
        self.dark_minutes = 0
        self.broker_events = 0

    def harvested_mw(self, local_ghi, sustained_overcast, piezo_draws, low_draws, env_rng):
        solar = ghi_to_solar_mw(local_ghi)
        p = RAIN_DAY_MOVEMENT_P if sustained_overcast else DRY_DAY_MOVEMENT_P
        if env_rng.random() < p:
            piezo = env_rng.choice(piezo_draws if sustained_overcast else low_draws)
        else:
            piezo = 0.0
        flow = flow_mw(sustained_overcast, env_rng)
        return solar + piezo + flow


def run_simulation(solar_days, piezo_draws, low_draws, brokering_enabled, seed):
    # TWO INDEPENDENT RNG STREAMS, both re-seeded identically per run:
    #   env_rng  -- drives ALL environment/harvesting randomness (local-cloud
    #               masks, piezo-trigger events, piezo draw selection, flow
    #               draws). Consumed in EXACTLY the same sequence regardless
    #               of brokering_enabled, because the harvesting code path
    #               never branches on brokering_enabled.
    #   link_rng -- drives ONLY the brokering link-success check, which by
    #               construction is never called when brokering_enabled is
    #               False.
    # This guarantees baseline and treatment see an IDENTICAL physical
    # environment at every timestep; brokering_enabled is the sole
    # difference between the two runs, isolating its causal effect from
    # random-draw noise.
    env_rng = random.Random(seed)
    link_rng = random.Random(seed + 1)
    nodes = [Node(i) for i in range(N_NODES)]
    total_minutes = 0
    network_covered_minutes = 0          # at least 1 node reporting/covered
    full_network_covered_minutes = 0     # ALL nodes reporting/covered
    total_broker_events = 0
    per_node_dark_minutes = [0] * N_NODES
    stress_total = 0
    stress_covered = 0  # network coverage specifically on sustained-overcast days

    per_node_dark_stress = [0] * N_NODES
    per_node_dark_nonstress = [0] * N_NODES
    global_t = -1  # monotonic minute counter across the WHOLE year, not per-day
    for day in solar_days:
        regional_ghi = day["ghi"]
        overcast = day["sustained_overcast"]
        for g in regional_ghi:
            global_t += 1
            total_minutes += 1
            if overcast:
                stress_total += 1
            active_count = 0
            for node in nodes:
                if overcast:
                    local_ghi = g  # rho=1 under monsoon-front assumption
                else:
                    if env_rng.random() < LOCAL_CLOUD_PROB:
                        local_ghi = g * LOCAL_CLOUD_ATTEN
                    else:
                        local_ghi = g

                harvested = node.harvested_mw(local_ghi, overcast, piezo_draws, low_draws, env_rng)
                node.buffer += (harvested - DEMAND_MW) / 60.0  # mW*min -> mWh/60
                node.buffer = max(0.0, min(BUFFER_CAPACITY_MWH, node.buffer))

                self_ok = node.buffer >= LOWER_THRESH
                covered = (node.covered_by_neighbor_until >= global_t) if not self_ok else False

                if self_ok or covered:
                    active_count += 1
                    if self_ok:
                        node.reporting_minutes += 1
                    else:
                        node.covered_minutes += 1
                else:
                    node.dark_minutes += 1
                    per_node_dark_minutes[node.idx] += 1
                    if overcast:
                        per_node_dark_stress[node.idx] += 1
                    else:
                        per_node_dark_nonstress[node.idx] += 1

            if brokering_enabled:
                for node in nodes:
                    if node.buffer < LOWER_THRESH and node.covered_by_neighbor_until < global_t:
                        for neighbor in nodes:
                            if neighbor.idx == node.idx:
                                continue
                            if neighbor.buffer > UPPER_THRESH:
                                if link_rng.random() < LINK_SUCCESS_PROB:
                                    node.covered_by_neighbor_until = global_t + BROKER_COOLDOWN_MIN
                                    total_broker_events += 1
                                    break

            if active_count >= 1:
                network_covered_minutes += 1
                if overcast:
                    stress_covered += 1
            if active_count == N_NODES:
                full_network_covered_minutes += 1

    return {
        "total_minutes": total_minutes,
        "network_covered_pct": 100.0 * network_covered_minutes / total_minutes,
        "full_network_covered_pct": 100.0 * full_network_covered_minutes / total_minutes,
        "stress_covered_pct": 100.0 * stress_covered / stress_total if stress_total else None,
        "stress_minutes": stress_total,
        "total_broker_events": total_broker_events,
        "per_node_dark_minutes": per_node_dark_minutes,
        "per_node_covered_minutes": [n.covered_minutes for n in nodes],
        "per_node_reporting_minutes": [n.reporting_minutes for n in nodes],
        "per_node_dark_stress": per_node_dark_stress,
        "per_node_dark_nonstress": per_node_dark_nonstress,
        "dark_fairness_stdev": statistics.stdev(per_node_dark_minutes) if len(set(per_node_dark_minutes)) > 1 else 0.0,
    }


def main():
    print("Loading real data...")
    piezo_draws = load_piezo_power_draws()
    low_draws = load_low_power_draws()
    solar_days = load_solar_days()
    print(f"  piezo power draws pooled: {len(piezo_draws)} (all experiments)")
    print(f"  low-power (ambient) draws: {len(low_draws)} (exp13 only)")
    print(f"  solar days loaded: {len(solar_days)}")
    n_overcast = sum(1 for d in solar_days if d["sustained_overcast"])
    print(f"  sustained-overcast days (stress condition): {n_overcast} / {len(solar_days)}")
    print()

    SEED = 42
    print("Running BASELINE (no brokering, solar+piezo+flow, independent nodes)...")
    baseline = run_simulation(solar_days, piezo_draws, low_draws, brokering_enabled=False, seed=SEED)
    print("Running TREATMENT (with duty-brokering, lossy-link-aware), SAME seed...")
    treatment = run_simulation(solar_days, piezo_draws, low_draws, brokering_enabled=True, seed=SEED)

    print()
    print("=" * 70)
    print(f"{'Metric':45s} {'Baseline':>10s} {'Treatment':>10s}")
    print("-" * 70)
    print(f"{'Network coverage, all minutes (%)':45s} {baseline['network_covered_pct']:>10.3f} {treatment['network_covered_pct']:>10.3f}")
    print(f"{'Full-network (all 5 nodes) coverage (%)':45s} {baseline['full_network_covered_pct']:>10.3f} {treatment['full_network_covered_pct']:>10.3f}")
    print(f"{'Network coverage on STRESS days only (%)':45s} {baseline['stress_covered_pct']:>10.3f} {treatment['stress_covered_pct']:>10.3f}")
    print(f"{'Total broker hand-off events':45s} {baseline['total_broker_events']:>10d} {treatment['total_broker_events']:>10d}")
    print(f"{'Dark-minute fairness (stdev across nodes)':45s} {baseline['dark_fairness_stdev']:>10.1f} {treatment['dark_fairness_stdev']:>10.1f}")
    print("=" * 70)
    print()
    print("Per-node dark minutes, baseline:  ", baseline["per_node_dark_minutes"])
    print("Per-node dark minutes, treatment: ", treatment["per_node_dark_minutes"])
    print("Per-node covered minutes, treatment:  ", treatment["per_node_covered_minutes"])
    print("Per-node reporting minutes, baseline: ", baseline["per_node_reporting_minutes"])
    print("Per-node reporting minutes, treatment: ", treatment["per_node_reporting_minutes"])
    print("Sanity: dark+covered+reporting should equal total_minutes for each node")
    print("  baseline node0:", baseline["per_node_dark_minutes"][0], "+", baseline["per_node_reporting_minutes"][0],
          "=", baseline["per_node_dark_minutes"][0] + baseline["per_node_reporting_minutes"][0], "vs total", baseline["total_minutes"])
    print("  treatment node0:", treatment["per_node_dark_minutes"][0], "+", treatment["per_node_covered_minutes"][0],
          "+", treatment["per_node_reporting_minutes"][0], "=",
          treatment["per_node_dark_minutes"][0] + treatment["per_node_covered_minutes"][0] + treatment["per_node_reporting_minutes"][0],
          "vs total", treatment["total_minutes"])
    print()
    print("Stress-condition minutes (sustained-overcast days):", baseline["stress_minutes"],
          "out of", baseline["total_minutes"], "total simulated minutes")
    print()
    print("Dark minutes split: STRESS (correlated, rho=1) vs NON-STRESS (locally decorrelated)")
    print(f"{'':12s} {'baseline-stress':>16s} {'treatment-stress':>17s} {'baseline-nonstr':>16s} {'treatment-nonstr':>17s}")
    for i in range(N_NODES):
        print(f"node{i:<8d} {baseline['per_node_dark_stress'][i]:>16d} {treatment['per_node_dark_stress'][i]:>17d} "
              f"{baseline['per_node_dark_nonstress'][i]:>16d} {treatment['per_node_dark_nonstress'][i]:>17d}")
    bs = sum(baseline['per_node_dark_stress']); ts = sum(treatment['per_node_dark_stress'])
    bn = sum(baseline['per_node_dark_nonstress']); tn = sum(treatment['per_node_dark_nonstress'])
    print(f"{'TOTAL':12s} {bs:>16d} {ts:>17d} {bn:>16d} {tn:>17d}")
    print(f"  Stress-day dark-time change: {bs} -> {ts}  ({100.0*(ts-bs)/bs:+.2f}%)")
    print(f"  Non-stress dark-time change: {bn} -> {tn}  ({100.0*(tn-bn)/bn:+.2f}%)")


if __name__ == "__main__":
    main()
