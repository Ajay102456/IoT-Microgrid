#!/usr/bin/env python3
"""
Replaces the FAKE random.uniform(0.5, 5.0) flow-harvester placeholder in
corridor_sim.py with a model driven by REAL data and REAL literature
measurements, with every remaining assumption stated explicitly.

REAL INPUTS:
  - Hourly rainfall (mm/hr), Cameron Highlands, full year 2025, NASA POWER
    (Data/nasa_power_corridor/cameron_tanahrata.json, PRECTOTCORR).
  - Power-vs-velocity curve fitted from two REAL measured points in Lepipas
    et al. (2024, Smart Materials and Structures): 125 uW at 0.5 m/s,
    5.1 mW at 2.0 m/s (Savonius-type microturbine, water-pipe rig). Fitted
    exponent = 2.68, close to the theoretical v^3 kinetic-turbine scaling --
    a sanity check that these are physically consistent real measurements,
    not noise.

DISCLOSED ENGINEERING ASSUMPTIONS (no real data exists for these specific
numbers at an actual highway cut-slope; this is a plausible design, not a
measurement):
  - Catchment area draining to one monitoring point: 500 m^2 (half a
    hectare of slope face -- a order-of-magnitude judgment call, not a
    surveyed value).
  - Rational-method runoff coefficient C = 0.6 (standard hydrology range
    0.5-0.7 for a graded/semi-vegetated slope surface).
  - A CONCENTRATED OUTLET design: runoff is assumed channeled into a narrow
    50mm x 50mm pipe (0.0025 m^2 cross-section) before the harvester, rather
    than spread across a wide drain -- this is a deliberate, stated design
    choice to reach the harvester's real reported cut-in velocity (0.5 m/s),
    not an arbitrary parameter chosen to make the result come out well. The
    choice itself is disclosed so it can be challenged.

This script computes what this model ACTUALLY predicts when driven by the
REAL rainfall record, rather than assuming it works.
"""

import json
import math
import statistics

LEPIPAS_V1, LEPIPAS_P1_MW = 0.5, 0.125
LEPIPAS_V2, LEPIPAS_P2_MW = 2.0, 5.1
N_EXP = math.log(LEPIPAS_P2_MW / LEPIPAS_P1_MW) / math.log(LEPIPAS_V2 / LEPIPAS_V1)
A_COEF = LEPIPAS_P1_MW / (LEPIPAS_V1 ** N_EXP)
CUT_IN_V = 0.5  # m/s, Lepipas et al.'s reported minimum functioning velocity

CATCHMENT_AREA_M2 = 500.0
RUNOFF_COEF = 0.6
CHANNEL_AREA_M2 = 0.05 * 0.05  # 50mm x 50mm concentrated outlet


def rain_mm_hr_to_velocity(rain_mm_hr):
    i_m_s = rain_mm_hr / 1000.0 / 3600.0            # mm/hr -> m/s intensity
    q_m3_s = RUNOFF_COEF * i_m_s * CATCHMENT_AREA_M2  # rational method
    v = q_m3_s / CHANNEL_AREA_M2
    return v


def velocity_to_power_mw(v):
    if v < CUT_IN_V:
        return 0.0
    return A_COEF * (v ** N_EXP)


def main():
    print(f"Fitted curve: P(v) = {A_COEF:.4f} * v^{N_EXP:.3f} mW  (from 2 real Lepipas et al. 2024 points)")
    print(f"Cut-in velocity: {CUT_IN_V} m/s (real, reported)")
    print(f"Catchment={CATCHMENT_AREA_M2} m^2, C={RUNOFF_COEF}, channel={CHANNEL_AREA_M2*1e4:.1f} cm^2 (ASSUMED)")
    print()

    with open("/home/s/Documents/MicroGrid-IoT/Data/nasa_power_corridor/cameron_tanahrata.json") as f:
        d = json.load(f)
    rain = d["properties"]["parameter"]["PRECTOTCORR"]

    hours_with_rain = [(k, v) for k, v in rain.items() if v > 0]
    print(f"Total hours in year: {len(rain)}; hours with nonzero rain: {len(hours_with_rain)} "
          f"({100*len(hours_with_rain)/len(rain):.1f}%)")

    velocities = [rain_mm_hr_to_velocity(v) for k, v in hours_with_rain]
    powers_mw = [velocity_to_power_mw(v) for v in velocities]

    active_hours = [p for p in powers_mw if p > 0]
    print(f"Hours where the modeled harvester would be ABOVE cut-in: {len(active_hours)} "
          f"({100*len(active_hours)/len(rain):.2f}% of all hours in the year)")
    if active_hours:
        print(f"  Power when active: min={min(active_hours):.4f} mW, "
              f"max={max(active_hours):.4f} mW, mean={statistics.mean(active_hours):.4f} mW, "
              f"median={statistics.median(active_hours):.4f} mW")

    max_rain = max(v for k, v in hours_with_rain)
    max_v = rain_mm_hr_to_velocity(max_rain)
    print()
    print(f"Heaviest real rain hour this year: {max_rain:.2f} mm/hr -> modeled velocity {max_v:.3f} m/s "
          f"-> modeled power {velocity_to_power_mw(max_v):.4f} mW")

    # what rain rate is needed to just reach cut-in?
    # v = C * (rain/1000/3600) * A_catch / A_channel = CUT_IN_V
    rain_for_cutin = CUT_IN_V * CHANNEL_AREA_M2 / (RUNOFF_COEF * CATCHMENT_AREA_M2) * 1000 * 3600
    print(f"Rain rate needed to just reach cut-in velocity: {rain_for_cutin:.2f} mm/hr")
    heavier = sum(1 for k, v in hours_with_rain if v >= rain_for_cutin)
    print(f"Real hours this year at or above that rate: {heavier} ({100*heavier/len(rain):.2f}% of the year)")


if __name__ == "__main__":
    main()
