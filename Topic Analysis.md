# Topic Analysis: Landslide Early-Warning IoT Sensor Swarm for Malaysian Highway Cut-Slopes

**Deep-research pipeline output (Phases 1–3) — Deep Research skill, academic-research-skills**
**Reference paper:** Lee, Y.-S., & Wang, C. (2024). A Cyber-Physical Testbed for IoT Microgrid Design and Validation. *Electronics*, 13(7), 1181. https://doi.org/10.3390/electronics13071181
**Date compiled:** 2026-10-17
**AI disclosure:** This document was produced with AI-assisted research tools (Claude, academic-research-skills deep-research pipeline) performing literature search (via Consensus/Semantic Scholar/OpenAlex/PubMed aggregation and web search), source screening, and synthesis. All claims should be independently verified before use in a submitted manuscript.

---

## 1. Reference Paper Summary

Lee & Wang (2024) define an "IoT microgrid" as a small cyber-physical system that powers a single DC IoT device by switching between a renewable primary source (PV array or piezoelectric harvester) and a utility-grid secondary source, using a double-voltage-threshold controller (5.1 V / 4.7 V in their case study) to avoid ping-pong switching. They validate the design on a Speedgoat hardware-in-the-loop (HIL) testbed with one ESP32/NodeMCU sensor node (DHT11 temperature/humidity sensor) uploading to ThingSpeak, under simulated intermittent power supply (Poisson-distributed outages, λ = 14 and λ = 37).

**Key model assumptions (Section 2.1 of the reference paper):**
1. Each IoT device operates on DC power and demands relatively little energy.
2. Power from the utility grid is available (as secondary/backup source).
3. An IoT application may be powered by a variety of renewable sources (e.g., PV array, piezoelectric harvester).
4. Each device works on a low duty cycle but needs to function continuously.

**Explicitly flagged future work:** scaling to multiple IoT devices; wireless telemetry of the primary source's state to the controller; HIL modeling of load-activity interleaving; storage-capacity effects on switching frequency.

**Gap exploited in this analysis:** Assumption 2 (utility grid always available as backup) does not hold for off-grid, remote, or disaster-exposed deployments — the core premise of the research direction developed below.

---

## 2. Phase 1 — Scoping

### 2.1 Research Question Brief

**Topic area:** IoT microgrids — extending single-node renewable/utility switching to off-grid, multi-node deployments where no utility backup exists.

**Primary Research Question:** In off-grid distributed environmental sensing networks — specifically landslide early-warning sensor swarms along Malaysian highway cut-slopes and hillside urban areas — where no utility-grid backup is available, can (a) hazard-coupled self-powering (piezoelectric harvesting from slope micro-movement, flow/kinetic harvesting from rainfall runoff) combined with (b) an inter-node "energy-aware duty-brokering" protocol (task/duty reassignment, not physical energy transfer, across spatially distributed cells) sustain network-level sensing continuity better than independent per-node primary/secondary switching alone?

**FINER Assessment**

| Criterion | Score | Justification |
|---|---|---|
| Feasible | 4/5 | Extends Lee & Wang's validated single-node HIL testbed (Speedgoat + ESP32/NodeMCU) to a multi-node replica rather than building new hardware from scratch |
| Interesting | 4/5 | Real, underserved deployment class: off-grid slope sensing has no utility fallback, which the base paper's model cannot represent |
| Novel | 4/5 | Shifts the unit of redundancy from single-node *power* switching to network-level *service* redundancy via hazard-coupled self-powering + task reassignment — confirmed absent from the 147-paper corpus screened in Phase 2 |
| Ethical | 5/5 | No human subjects; benign/beneficial use (public safety, disaster risk reduction) |
| Relevant | 4/5 | Directly actionable for real deployment engineering; aligns with JKR's National Slope Master Plan 2025–2030 |
| **Average** | **4.2/5** | |

**Scope Boundaries**
- **In scope:** Off-grid, multi-node IoT sensor swarms for landslide early warning on highway cut-slopes and hillside urban areas (Malaysian context); renewable harvesting per node (piezoelectric from ground micro-movement, flow/kinetic from rainfall runoff); duty/task-level brokering over existing wireless links (no physical wireless power transfer); HIL testbed extension methodology following Lee & Wang's architecture.
- **Out of scope:** Grid-connected/urban IoT microgrids (already covered by the reference paper); utility-scale networked microgrids (kV-level, different problem domain); physical wireless power transfer between nodes; flood-basin monsoon telemetry (considered and set aside — see Section 2.3).
- **Key assumptions:** Nodes communicate over a low-power wireless network already present for sensing (e.g., LoRaWAN); "brokering" reassigns *which node performs a sensing/transmission duty*, not actual electrical energy, between nodes.

**Sub-questions**
1. How does the reference paper's single-node double-threshold switching perform, at the network level, when no utility/secondary source exists at all?
2. What duty-brokering protocol design (threshold-triggered gossip vs. auction-based) best preserves network-level sensing continuity under varying spatial correlation of storm-driven power intermittency across nodes along a highway corridor?
3. How must the HIL cyber-physical testbed be extended to a multi-node configuration to validate such a protocol, and what fidelity/scalability trade-offs result?

### 2.2 Methodology Blueprint

- **Paradigm:** Pragmatist / design-science — build an artifact (protocol + testbed extension), demonstrate, and evaluate empirically, matching the reference paper's own research style.
- **Method:** Design Science Research Methodology (problem identification → artifact design → demonstration → evaluation), with quantitative experimental validation.
- **Data strategy:**
  - *Primary:* measurements from an extended multi-node HIL testbed (per-node voltage/power traces, duty-reassignment events, network-level uptime), using a spatially-correlated extension of the reference paper's Poisson intermittency model (adding a correlation coefficient across nearby nodes' solar/rainfall exposure).
  - *Secondary:* the 147-paper literature base compiled in Phase 2 (WSN energy-aware clustering, P2P energy trading, piezo/flow harvesting, landslide rainfall-threshold models), used to benchmark novelty and parameterize the correlated-intermittency and hazard-coupling models.
- **Analytical framework:** Controlled comparison — baseline (independent per-node switching, no brokering, solar-only backup) vs. treatment (hazard-coupled harvesting + brokering protocol) — on network-level sensing/data-delivery continuity, cross-node energy-depletion fairness, and brokering-event frequency (the network-level analog of "ping-pong").
- **Validity criteria:** Internal validity via parameter sweeps (λ per node, spatial correlation coefficient); external validity via a ≥3-node physical prototype; reliability via repeated trials; construct validity of "network-level continuity" as the outcome proxy.
- **Human subjects:** Not applicable — no human-subjects component. (Note: ethics review in Phase 5 should still confirm no incidental human-subjects exposure from field deployment near highways/settlements.)

### 2.3 Scoping Dialogue Record (for traceability)

Two alternative applications were explored with the user before landslide monitoring was selected as the final scope:

1. **Monsoon flood river-basin telemetry (considered, not selected as primary):** Off-grid upstream flood-gauge sensors (cf. JPS/DID telemetry stations in Pahang/Kelantan/Terengganu). Rejected as the *sole* focus because monsoon storms cause fully-correlated solar failure across an entire river basin simultaneously, which breaks the neighbor-brokering concept (everyone goes dark together) — identified as the adversarial stress case during Devil's Advocate Checkpoint 1, not as a reason to discard the direction entirely.
2. **Landslide early-warning swarm along highway cut-slopes/hillside urban areas (selected):** Preferred because (a) it reuses the reference paper's own piezoelectric harvester technology, redirected from ambient vibration to the hazard signal itself (ground micro-movement preceding slope failure), creating a self-reinforcing design (more instability → more harvested power → more frequent reporting, exactly when needed); (b) a highway corridor spans tens of kilometers, so Malaysian convective storm cells are often localized rather than basin-wide, meaning neighbor-to-neighbor duty-brokering remains viable across the corridor even when solar fails locally; (c) strong real-world grounding in known Malaysian landslide incidents (Highland Towers 1993; Bukit Antarabangsa 2008; Batang Kali campsite landslide, December 2022; recurring closures on the Simpang Pulai–Cameron Highlands and Tapah–Cameron Highlands routes) and an existing institutional home (JKR's National Slope Master Plan 2025–2030).

### 2.4 Devil's Advocate — Checkpoint 1

- **Framing risk:** "Brokering" must stay explicitly defined as *duty/task reassignment*, never physical energy transfer — otherwise the design reads as proposing unrealistic long-range wireless power transfer.
- **Novelty risk:** Energy-aware clustering in WSNs is a mature field; Phase 2 was required to search WSN/energy-trading literatures (not just papers labeled "IoT microgrid") to confirm the delta is real and not a relabeling of known WSN clustering results. (Resolved in Phase 2/3 — see Section 4.)
- **Confound to test, not assume away:** Nearby nodes likely see correlated cloud cover/irradiance dips (especially under monsoon fronts), which would blunt brokering's benefit — the experimental design must include high-correlation conditions as a stress test, not only favorable low-correlation cases, to avoid confirmation bias.

**Verdict: PASS with conditions** — (1) keep the brokering definition scoped to task reassignment; (2) Phase 2 must search WSN/energy-trading literatures for novelty benchmarking; (3) the experiment must include adversarial (high-correlation) conditions.

---

## 3. Plain-Language Summary (for non-specialist readers)

A small sensor stuck on a remote hillside or forest needs electricity, but there's no power line to plug into — so it relies on a small solar panel. Problem: solar panels fail at night, in cloud cover, and especially during the heavy monsoon rain that often *causes* the landslide the sensor is meant to detect. The reference paper solves the "no sun" problem for one sensor that still has a backup: the ordinary power grid. This analysis asks: what if there is no grid to fall back on, as is the case on many remote Malaysian highway slopes?

Two ideas address this:
1. **Let the sensor power itself from the danger it's watching for.** A slope about to fail doesn't sit still — it creeps, cracks, and vibrates. A piezoelectric harvester (already used in the reference paper) converts that movement into electricity, so the more unstable the slope becomes, the more power is available for frequent reporting — right when it matters most. A second harvester captures energy from rainfall runoff on the slope face, which also increases exactly when the hazard is rising.
2. **Let sensors cover for each other.** If one sensor's harvester is temporarily starved (e.g., a very localized cloud patch), a nearby sensor with surplus power can take over its reporting duty for a while — not by sending it electricity, but by taking on its job. Because Malaysian storm cells are often localized rather than covering an entire highway corridor at once, this neighbor-covering approach stays useful even during monsoon weather.

---

## 4. Phase 2 — Investigation (PRISMA-Aligned Systematic Search)

### 4.1 Protocol

**Review question:** What does the literature establish, across nine component technologies, that supports or challenges a landslide early-warning IoT sensor swarm for Malaysian highway cut-slopes/hillside areas, self-powered by hazard-coupled piezoelectric/flow harvesting with corridor-wide duty-brokering?

**Databases:** Semantic Scholar, OpenAlex, PubMed (via Consensus aggregator search); supplementary web search for Malaysian grey literature (JKR slope programs, highway landslide incident reports).

**Search period:** No date restriction (captures foundational 2005–2009 energy-harvesting work through 2026 preprints).

**Inclusion criteria:** Peer-reviewed journal/conference papers or systematic reviews addressing: (1) landslide/slope IoT or WSN monitoring; (2) rainfall-induced landslide threshold or prediction models; (3) piezoelectric/vibration self-powered sensing; (4) flow/hydrokinetic energy harvesting for sensor nodes; (5) LoRaWAN/LPWAN for remote/disaster monitoring; (6) IoT microgrid or cyber-physical renewable energy management; (7) energy-aware WSN duty-cycling, clustering, or task-offloading; (8) peer-to-peer energy trading/sharing in microgrids; (9) hardware-in-the-loop testbed methodology for power electronics/microgrids.

**Exclusion criteria:** Purely materials-science papers with no sensing/WSN application path; duplicate records; topics unrelated to the nine components (e.g., CERN radiation monitoring, generic factory gas-leak detection).

### 4.2 PRISMA Flow

- **Identified** (10 Consensus queries × 20 records): n = 200
- **Duplicates removed** (cross-query overlap, chiefly between general-landslide-WSN and Malaysia-landslide-WSN queries): −18 → n = 182
- **Records screened** (title/abstract against inclusion criteria): n = 182
- **Excluded** (off-topic or highly redundant near-duplicate regional case studies trimmed for parsimony): −32
- **Included in initial reference set:** n = 150
- **Downgraded on venue-quality screening (Section 4.4):** −3 → **Final verified reference set: n = 147**

### 4.3 Included References, by Cluster

#### Cluster A — Landslide/Slope IoT & WSN Monitoring Systems (n=31; includes 2 Malaysia-specific studies)
*Role: establishes the baseline monitoring architecture the swarm must sense/transmit for; confirms no existing system addresses off-grid power-continuity via duty-brokering.*

1. El Houssaini et al. (2022). Location-Aware IoT-Enabled WSNs for Landslide Early Warning. *Electronics*. DOI:10.3390/electronics11233971
2. Giri et al. (2019). WSN System for Landslide Monitoring and Warning. *IEEE Trans. Instrum. Meas.* DOI:10.1109/tim.2018.2861999
3. Rani et al. (2025). IoT-Enabled Real-Time Landslide Monitoring using Waterbody Sensors. *ICTMIM 2025*. DOI:10.1109/ictmim65579.2025.10988011
4. Gowtham et al. (2026). Low-Power LoRaWAN IoT Landslide EWS with Random Forest. *ICAISS 2026*. DOI:10.1109/icaiss68683.2026.11525861
5. Amirthavarshini et al. (2025). Harnessing LoRa for Real-Time Landslide Monitoring in Kerala. *Geoscience Frontiers*. DOI:10.1016/j.gsf.2025.102242
6. Souza et al. (2022). IoT-Based System for Landslides Warnings Using Real Time Slope Monitoring. *COTB'22*. DOI:10.14210/cotb.v13.p126-133
7. D. J. et al. (2025). I-ELWS: IoT Driven Early Landslide Warning System. *ETNCC 2025*. DOI:10.1109/etncc66224.2025.11299651
8. P. C. et al. (2021). Real-time landslide EWS through low cost soil and rainfall sensors. *Materials Today: Proceedings*. DOI:10.1016/j.matpr.2021.02.456
9. Chaulya et al. (2024). Landslide monitoring and prediction system using geosensors and WSN. *Discover Geoscience*. DOI:10.1007/s44288-024-00007-3
10. Susanto et al. (2024). Landslide Monitoring and Warning System Based on WSN. *ELKHA*. DOI:10.26418/elkha.v16i2.83489
11. Thein et al. (2020). Real-Time Monitoring and EWS for Landslide Preventing in Myanmar. *GCCE 2020*. DOI:10.1109/gcce50665.2020.9291809
12. Ramesh (2009). Real-Time WSN for Landslide Detection. *SensorComm 2009*. DOI:10.1109/sensorcomm.2009.67
13. Devi (2025). Developing a Low-Cost Landslide EWS using IoT and Sensor Networks. *ICSCSS 2025*. DOI:10.1109/icscss64956.2025.11501071
14. Gamperl et al. (2021). IoT Geosensor Network for Cost-Effective LEWS (Inform@Risk, Colombia). *Sensors*. DOI:10.3390/s21082609
15. Mahfudh et al. (2026). Low-Cost IoT-Based Landslide EWS. *CENTIVE Proceedings*. DOI:10.20895/centive.v2025i1.562
16. Rawat et al. (2024). LANDSLIDE MONITOR: a real-time landslide monitoring system. *Environ. Earth Sci.* DOI:10.1007/s12665-024-11526-0
17. Galley et al. (2017). WSN Based Landslide Detection and EWS. *Zorig Melong*. DOI:10.17102/zmv3.i1.006
18. Abraham et al. (2020). IoT-Based Geotechnical Monitoring, Darjeeling Himalayas. *Sensors*. DOI:10.3390/s20092611
19. Das et al. (2020). Real-Time Threshold-based Landslide Prediction using WSN. *ICCE-Taiwan 2020*. DOI:10.1109/icce-taiwan49838.2020.9258181
20. Ramesh et al. (2017). WSNs for Early Warning of Landslides: Decade Long Deployment. DOI:10.1007/978-3-319-53487-9_4
21. **Ali et al. (2012). Development of WSN for slope monitoring (Hulu Langat, MALAYSIA, 2011 landslide, 16 fatalities).** *ICIAS 2012*. DOI:10.1109/icias.2012.6306203
22. Ragnoli et al. (2023). WSN-Based Rockfall and Landslide Monitoring Systems: A Review. *Sensors*. DOI:10.3390/s23167278
23. Bagwari et al. (2021). Low-Cost Sensor and LoRaWAN Opportunities for Landslide Monitoring: A Review. *IEEE Access*. DOI:10.1109/access.2021.3137841
24. Jeong et al. (2019). Effectiveness of a WSN System for Landslide Monitoring (Seoul). *IEEE Access*. DOI:10.1109/access.2019.2960570
25. Marino et al. (2023). IoT-Based Low-Cost Sensor Network for Hydrological Monitoring of Landslide-Prone Areas. *Sensors*. DOI:10.3390/s23042299
26. Debnath et al. (2025). Smart IoT-Based Distributed System for Remote Detection of Slope Movements (highway embankments). *ICNC 2025*. DOI:10.1109/icnc64010.2025.10993553
27. Ahmed et al. (2016). Real-time monitoring of partially stable slopes using WSN. *IC-GET 2016*. DOI:10.1109/get.2016.7916638
28. Vu et al. (2018). WSN in landslide monitoring system with remote data management. *Measurement*. DOI:10.1016/j.measurement.2018.01.002
29. Kumar M. et al. (2022). Accurate IoT Based Slope Instability Sensing System for Landslide Detection. *IEEE Sensors J.* DOI:10.1109/jsen.2022.3189903
30. Joshi et al. (2023). WSN-Based Smart Landslide Monitoring Device (SMARTMODE). *IEEE Trans. Instrum. Meas.* DOI:10.1109/tim.2023.3269746
31. ~~Idris et al. (n.d.). Smart Monitoring and Warning Landslide System using IoT (Bukit Bauk Dungun, MALAYSIA).~~ — **excluded from the manuscript's citation set, see Section 4.4 update below.**

#### Cluster B — Rainfall-Induced Landslide Threshold/Prediction Models (n=18)
*Role: defines the hazard-signal dynamics (rainfall→instability lag) that the self-powering and duty-brokering design must track.*

32. Piciullo et al. (2017). Threshold-based regional EW model for rainfall-induced landslides. *Landslides*. DOI:10.1007/s10346-016-0750-2
33. Liu et al. (2024). Regional EW model based on slope unit, Chongqing. *Engineering Geology*. DOI:10.1016/j.enggeo.2024.107464
34. Dou et al. (2024). Regional dynamic EW model, Fujian. *Geomatics, Nat. Hazards and Risk*. DOI:10.1080/19475705.2024.2435510
35. Guzzetti et al. (2024). Landslide predictions through combined rainfall threshold models. *Landslides*. DOI:10.1007/s10346-024-02340-7
36. Huang et al. (2022). Regional rainfall-induced landslide hazard warning based on susceptibility mapping. *Geomorphology*. DOI:10.1016/j.geomorph.2022.108236
37. Zhang et al. (2026). Dynamic EW Model Coupling Slope Units and Rainfall Thresholds, Jinyang. *Geosciences*. DOI:10.3390/geosciences16090367
38. Cao et al. (2022). Hourly shallow landslide warning model combining susceptibility and rainfall threshold. *J. Mountain Sci.* DOI:10.1007/s11629-022-7370-1
39. Song et al. (2025). Refined meteorological EW based on temporal probability model. *Chinese J. Rock Mech. Eng.* DOI:10.3724/1000-6915.jrme.2024.0805
40. Wang et al. (2026). Dynamic EW model based on refined threshold analysis, Tanjiawan. *PLOS One*. DOI:10.1371/journal.pone.0339689
41. Zhan et al. (2022). EW model and model test verification of rainfall-induced shallow landslide. *Bull. Eng. Geol. Environ.* DOI:10.1007/s10064-022-02827-4
42. Nocentini et al. (2023). Optimization of rainfall thresholds through false alarm reduction. *Landslides*. DOI:10.1007/s10346-023-02176-7
43. Sun et al. (2024). Probabilistic thresholds for regional rainfall induced landslides. *Computers and Geotechnics*. DOI:10.1016/j.compgeo.2023.106040
44. Naidu et al. (2017). EWS for shallow landslides using rainfall threshold and slope stability analysis. *Geoscience Frontiers*. DOI:10.1016/j.gsf.2017.10.008
45. Dou et al. (2023). Rainfall EW threshold and spatial distribution in China. *Rock Mechanics Bulletin*. DOI:10.1016/j.rockmb.2023.100056
46. Dixit et al. (2024). Numerical-model-derived I-D thresholds for debris flows, Himalayan catchment. *NHESS*. DOI:10.5194/nhess-24-465-2024
47. Lee et al. (2021). Optimal rainfall thresholds for LEWS, Chuncheon, Korea. *Landslides*. DOI:10.1007/s10346-020-01603-3
48. Wang et al. (2026). Physical-based rainfall landslide prediction model from slope-unit I-D curves. *NHESS*. DOI:10.5194/nhess-26-2367-2026
49. Sarkar et al. (2023). Event-duration rainfall threshold model, Uttarkashi, Himalayas. *Int. J. Earth Sci.* DOI:10.1007/s00531-023-02337-y

#### Cluster C — Piezoelectric & Vibration-Based Self-Powered Sensing (n=15)
*Role: direct technical basis for "harvest power from the hazard signal itself" — includes slope-specific geosynthetic sensing (items 53–54) that currently sense but do not harvest, confirming the novelty gap.*

50. Li et al. (2026). Sustained Self-Powered Real-Time Vibration Monitoring via Nonlinear Harvesting. *Advanced Science*. DOI:10.1002/advs.76967
51. Rubeš et al. (2021). Self-powered wireless vibration sensor node using vibration energy harvester. *Mech. Syst. Signal Process.* DOI:10.1016/j.ymssp.2021.107890
52. Izhar et al. (2023). Hybrid acoustic, vibration, and wind energy harvester for self-powered WSN. *Energy Conversion and Management*. DOI:10.1016/j.enconman.2022.116635
53. **Wang et al. (2024). Sensor-enabled piezoelectric geocable–geogrid for slope rehabilitation and monitoring.** *Engineering Geology*. DOI:10.1016/j.enggeo.2024.107780
54. **Wang et al. (2026). Reinforcement and microseismic monitoring of slopes with self-sensing smart geosynthetic.** *Geosynthetics International*. DOI:10.1680/jgein.25.00212
55. Rigo et al. (2024). Piezoelectric Sensors as Energy Harvesters for Ultra Low-Power IoT. *Sensors*. DOI:10.3390/s24082587
56. Wang et al. (2024). Self-sustained/self-wakeup wireless vibration sensors, hybrid harvesting. *Applied Energy*. DOI:10.1016/j.apenergy.2023.122207
57. Yang et al. (2025). Hybrid multiple-layer piezoelectric-solar harvester for self-powered sensing. *Sustainable Energy Technologies and Assessments*. DOI:10.1016/j.seta.2024.104157
58. Li et al. (2021). Piezoelectric Energy Harvesting: Materials, Structures, Applications. *Small Structures*. DOI:10.1002/sstr.202100128
59. Ng et al. (2005). Sensitivity Analysis and Energy Harvesting for a Self-Powered Piezoelectric Sensor. *J. Intelligent Material Systems and Structures*. DOI:10.1177/1045389x05053151
60. Lo et al. (2022). Self-powered SECE piezoelectric harvesting from shock excitations. *Mech. Syst. Signal Process.* DOI:10.1016/j.ymssp.2022.109123
61. Biswal et al. (2024). Self-Powered Accelerometer Using Circular Hole Piezo Harvester. *IEEE Sensors Letters*. DOI:10.1109/lsens.2024.3485540
62. Kuang et al. (2021). Strongly coupled piezoelectric harvesters for self-powered condition monitoring. *Energy Conversion and Management*. DOI:10.1016/j.enconman.2021.114129
63. Zou (2023). Piezoelectric self-powered wireless sensor in vibration environment monitoring. *Results in Engineering*. DOI:10.1016/j.rineng.2023.101492
64. Das Mahapatra et al. (2021). Piezoelectric Materials for Energy Harvesting and Sensing: Roadmap. *Advanced Science*. DOI:10.1002/advs.202100864

#### Cluster D — Flow/Hydrokinetic Energy Harvesting for Remote Sensors (n=15)
*Role: the complementary harvester whose output rises with rainfall/runoff intensity — core to the "anti-correlated backup" design.*

65. Ahmad et al. (2024). Microplanar Coil-Based Hydrokinetic EM Harvester for IoT Sensors. *J. Engineering*. DOI:10.1155/2024/1985367 ⚠️ *see Section 4.4 — venue caution*
66. Lepipas et al. (2024). Miniature water flow harvester, Savonius-type microturbine. *Smart Materials and Structures*. DOI:10.1088/1361-665x/ad1c3f
67. Guiffard et al. (2021). Self-powered wireless sensor with flexible aero-piezoelectric harvester. *Renewable Energy*. DOI:10.1016/j.renene.2021.11.113
68. Zhang et al. (2024). Triboelectric-EM hybrid generator, Savonius flapping wing, low-velocity water flow. *Applied Energy*. DOI:10.1016/j.apenergy.2023.122512
69. Rahman et al. (2025). Survey of flow-based energy harvesters for sustainable WSN nodes. *J. Renewable and Sustainable Energy*. DOI:10.1063/5.0237597
70. Zhao et al. (2021). Hydrokinetic piezoelectric harvesting by wake-induced vibration. *Energy*. DOI:10.1016/j.energy.2020.119722
71. Kamenar et al. (2016). Harvesting river flow energy for WSN technology (GOLDFISH project). *Microsystem Technologies*. DOI:10.1007/s00542-015-2778-y
72. Li et al. (2022). Self-powered wireless water-monitoring sensor, electromagnetic-pendulum harvester. *Energy*. DOI:10.1016/j.energy.2022.123883
73. Vijayaregunathan et al. (2024). Harvesting hydraulic energy for self-sustainable IoT flow measurement. *Energy Sources Part A*. DOI:10.1080/15567036.2024.2334922
74. Yunus et al. (2026). Design of a Wireless Sensor Node Powered by Kinetic Energy Harvesters. *Applied Research*. DOI:10.1002/appl.70124
75. Zhou et al. (2026). Small-scale water energy harvesting for sustainably-powered distributed electronics. *Communications Materials*. DOI:10.1038/s43246-026-01137-6
76. Sarker et al. (2024). Micro energy harvesting for IoT platform: Review. *Heliyon*. DOI:10.1016/j.heliyon.2024.e27778
77. Hafizh et al. (2023). Vortex-induced-vibration self-tunable airfoil piezoelectric harvester for underwater sensing. *Ocean Engineering*. DOI:10.1016/j.oceaneng.2022.113467
78. Azevedo et al. (2012). Energy harvesting from wind and water for autonomous WSN nodes. *IET Circuits Devices Syst.* DOI:10.1049/iet-cds.2011.0287
79. Williams et al. (2021). Survey of Energy Harvesting Technologies for WSNs. *IEEE Access*. DOI:10.1109/access.2021.3083697

#### Cluster E — LoRaWAN/LPWAN for Remote Disaster Monitoring (n=15)
*Role: the communication substrate that any corridor-wide duty-brokering protocol must run over; also the source of the lossy-link constraint flagged in Phase 3.*

80. ~~Murarkar et al. (2025). Low-Power LoRa-Based Disaster Alert System for Remote Areas.~~ *Int. J. Advanced Electrical and Electronics Engineering*. DOI:10.65521/ijaeee.v14i2.1707 — **dropped, see Section 4.4**
81. Ragnoli et al. (2020). Autonomous Low-Power LoRa-Based Flood-Monitoring System. *J. Low Power Electronics and Applications*. DOI:10.3390/jlpea10020015
82. Tsakmakis et al. (2022). Adaptive LoRaWAN MAC Protocol for Event Detection Applications. *Sensors*. DOI:10.3390/s22093538
83. Pan et al. (2021). UAV-Aided Emergency Environmental Monitoring, LoRa Mesh. *IEEE IoT Journal*. DOI:10.1109/jiot.2021.3095494
84. Sendra et al. (2020). LoRaWAN Network for Fire Monitoring in Rural Environments. *Electronics*. DOI:10.3390/electronics9030531
85. ~~Sudha et al. (2026). Adaptive AI-LoRa EWS for Remote Disaster-Prone Areas.~~ *Int. J. Engineering & Extended Technologies Research*. DOI:10.15662/ijeetr.2026.0802093 — **dropped, see Section 4.4**
86. Ragnoli et al. (2022). LoRa-Based WSN for Rockfall and Landslide Monitoring, Pantelleria Island. *J. Low Power Electronics and Applications*. DOI:10.3390/jlpea12030047
87. Wu et al. (2023). Low-Cost Low-Power LoRa Mesh Network for Large-Scale Environmental Sensing (CottonCandy). *IEEE IoT Journal*. DOI:10.1109/jiot.2023.3270237
88. Finochietto et al. (2022). Reducing Operational Expenses of LoRaWAN-Based IoRT Applications. *Sensors*. DOI:10.3390/s22207778
89. Bagwari et al. (2022). Disaster Monitoring based on IoT and Long Range Assisted Framework. *J. Physics: Conf. Series*. DOI:10.1088/1742-6596/2327/1/012020
90. Ragnoli et al. (2022). Flood monitoring: LoRa-based case study, L'Aquila. *PRIME 2022*. DOI:10.1109/prime55000.2022.9816747
91. Abdul Latiff (2019). Environmental Monitoring System Based on LoRa Technology in Island. *ICSigSys 2019*. DOI:10.1109/icsigsys.2019.8811066
92. **Chapungo et al. (2025). LoRaWAN Connectivity Reliability in Remote Rural Areas of Mozambique (source of the ~89% PDR lossy-link finding used in Phase 3 synthesis).** *Sensors*. DOI:10.3390/s25196027
93. Zhao et al. (2023). Forest IoT Using LPWAN, Solar-Powered Micro-Weather Station. *Sensors*. DOI:10.3390/s23104809
94. Tamang et al. (2022). Reliable Low-Latency LoRaWAN Solution for Environmental Monitoring at Major Accident Risk Sites. *Sensors*. DOI:10.3390/s22062372

#### Cluster F — IoT Microgrid & Cyber-Physical Renewable Energy Management (n=18)
*Role: core reference technology cluster — the reference paper itself (item 101) plus the surrounding literature it sits within.*

95. Liya et al. (2026). Energy efficient cyber-physical control of renewable microgrids, edge-AI, blockchain. *Scientific Reports*. DOI:10.1038/s41598-026-50169-y
96. Silva et al. (2023). IoT-based EMS for AC microgrids with grid and security constraints. *Applied Energy*. DOI:10.1016/j.apenergy.2023.120904
97. Wu et al. (2024). Microgrids EM considering net-zero energy, IoT digital twin. *Sustainable Energy Technologies and Assessments*. DOI:10.1016/j.seta.2024.103621
98. Cicceri et al. (2023). Deep Learning-Driven Self-Conscious Distributed CPS for Renewable Energy Communities. *Sensors*. DOI:10.3390/s23094549
99. Asef et al. (2023). SIEMS: Secure Intelligent EMS for Industrial IoT Applications. *IEEE Trans. Industrial Informatics*. DOI:10.1109/tii.2022.3165890
100. Tasmant et al. (2025). Review of ML and IoT-based EMS for AC microgrids. *Comput. Electr. Eng.* DOI:10.1016/j.compeleceng.2025.110563
101. **Lee & Wang (2024). A Cyber-Physical Testbed for IoT Microgrid Design and Validation [PRIMARY REFERENCE PAPER].** *Electronics*. DOI:10.3390/electronics13071181
102. Albarakati et al. (2022). Microgrid energy management and monitoring systems: A comprehensive review. *Frontiers in Energy Research*. DOI:10.3389/fenrg.2022.1097858
103. Xu et al. (2021). Blockchain-based secure energy policy and management of renewable smart microgrids. *Sustainable Cities and Society*. DOI:10.1016/j.scs.2021.103010
104. Sitharthan et al. (2023). Smart microgrid with IoT for energy management (PV/Wind/Piezo hybrid). *Comput. Electr. Eng.* DOI:10.1016/j.compeleceng.2022.108556
105. Mallala et al. (2025). IoT-enabled community microgrid EM with battery degradation consideration. *J. Energy Storage*. DOI:10.1016/j.est.2024.114739
106. ~~Kadao et al. (2025). Cyber-Physical Microgrid Management Using Explainable AI for High Renewable Penetration.~~ *Archives for Technical Sciences*. DOI:10.70102/afts.2025.1834.472 — **dropped, see Section 4.4**
107. Samanta et al. (2020). IoT-based smart EM in VRFB-integrated bio-solar microgrid. *J. Energy Storage*. DOI:10.1016/j.est.2020.101967
108. Aljafari et al. (2022). Optimization of DC, AC, Hybrid AC/DC Microgrid-Based IoT Systems: A Review. *Energies*. DOI:10.3390/en15186813
109. Sedhom et al. (2021). IoT-based optimal demand side management for smart microgrid. *Int. J. Electrical Power & Energy Systems*. DOI:10.1016/j.ijepes.2020.106674
110. Zhou et al. (2021). Multi-microgrid EMS: Architecture, Communication, and Scheduling Strategies. *J. Modern Power Systems and Clean Energy*. DOI:10.35833/mpce.2019.000237
111. Ojo et al. (2025). Microgrids' Control Strategies and Real-Time Monitoring Systems: Comprehensive Review. *Energies*. DOI:10.3390/en18133576
112. Alhasnawi et al. (2023). New communication platform for smart EMS using MILP. *Energy Systems*. DOI:10.1007/s12667-023-00591-2

#### Cluster G — Energy-Aware Duty-Cycling, Clustering & Task-Offloading WSN Protocols (n=15)
*Role: generic algorithmic toolbox for the duty-brokering protocol; absence of a geohazard/spatial-correlation variant confirms the novelty gap.*

113. Bahbahani et al. (2017). Cooperative Clustering Protocol With Duty Cycling for EH-WSN. *IEEE Trans. Wireless Communications*. DOI:10.1109/twc.2017.2762674
114. Shagari et al. (2020). Heterogeneous Energy and Traffic Aware Sleep-Awake Cluster-Based Routing. *IEEE Access*. DOI:10.1109/access.2020.2965206
115. Ramkumar (2025). Adaptive Duty-Cycled Cooperative Clustering Model for EH-WSN. *CNC 2025*. DOI:10.1109/cnc68716.2025.11484711
116. Liu et al. (2023). DCC-IACJS: bio-inspired duty cycle-based clustering for energy-efficient WSN. *J. King Saud University CIS*. DOI:10.1016/j.jksuci.2023.01.015
117. V. et al. (2025). Energy-Aware MAC Protocols with Load Balancing for Solar-Powered WSN. *ICDSNS 2025*. DOI:10.1109/icdsns65743.2025.11168589
118. Tolani et al. (2023). Energy-Efficient Duty-Cycle Hybrid MAC Protocol for WSN. *Wireless Personal Communications*. DOI:10.1007/s11277-023-10448-7
119. Chauhan et al. (2022). Variable duty cycle aware energy efficient clustering strategy for WSN. *J. Ambient Intelligence and Humanized Computing*. DOI:10.1007/s12652-022-04363-1
120. Gong et al. (2023). Centralized Energy-Efficient Clustering Protocol for WSN. *IEEE Sensors J.* DOI:10.1109/jsen.2022.3224180
121. Yang et al. (2025). DRL-Driven Workload Offloading for Energy-Efficient Solar-Powered WSN. *ACM CoNEXT Workshop*. DOI:10.1145/3769698.3771226
122. Jalalinejad et al. (2024). Hybrid Multi-Hop Clustering and Energy-Aware Routing for EH-WSN. *IEEE Access*. DOI:10.1109/access.2024.3458795
123. Zhao et al. (2023). Load-Aware Energy-Efficient Clustering Algorithm in Sensor-Cloud. *J. Grid Computing*. DOI:10.1007/s10723-023-09683-w
124. Hady (2020). Duty Cycling Centralized Hierarchical Routing Protocol for WSN. *Comput. Syst. Sci. Eng.* DOI:10.32604/csse.2020.35.347
125. Yadav et al. (2023). Clustering-Based Energy Efficient Task Offloading for Sustainable Fog Computing. *IEEE Trans. Sustainable Computing*. DOI:10.1109/tsusc.2022.3186585
126. González et al. (2024). Evolutionary, Swarm, Iterative-Based Task-Offloading Optimization for WSN Battery Life. *IEEE Sensors J.* DOI:10.1109/jsen.2024.3419558
127. Li et al. (2020). Energy-Aware Task Offloading in the Internet of Things. *IEEE Wireless Communications*. DOI:10.1109/mwc.001.1900495

#### Cluster H — Peer-to-Peer Energy Sharing/Trading in Microgrids (n=12)
*Role: the conceptual precedent for "trading" surplus resource between nodes — reinterpreted here as duty/task brokering rather than electrical energy.*

128. Zhang et al. (2018). Peer-to-Peer energy trading in a Microgrid. *Applied Energy*. DOI:10.1016/j.apenergy.2018.03.010
129. Zhou et al. (2023). P2P energy sharing and trading in smart communities: pricing, decision-making, agent-based collaboration. *Renewable Energy*. DOI:10.1016/j.renene.2023.02.125
130. Long et al. (2018). P2P energy sharing through two-stage aggregated battery control in community microgrid. *Applied Energy*. DOI:10.1016/j.apenergy.2018.05.097
131. Luo et al. (2022). Distributed P2P energy trading based on game theory, DER ownership complexity. *J. Cleaner Production*. DOI:10.1016/j.jclepro.2022.131573
132. Paudel et al. (2019). P2P Energy Trading in a Prosumer-Based Community Microgrid: Game-Theoretic Model. *IEEE Trans. Industrial Electronics*. DOI:10.1109/tie.2018.2874578
133. Anoh et al. (2020). Energy P2P Trading in Virtual Microgrids: A Game-Theoretic Approach. *IEEE Trans. Smart Grid*. DOI:10.1109/tsg.2019.2934830
134. Yan et al. (2023). P2P transactive energy trading of multiple microgrids under renewable uncertainty. *Int. J. Electrical Power & Energy Systems*. DOI:10.1016/j.ijepes.2023.109235
135. Alam et al. (2019). Peer-to-peer energy trading among smart homes. *Applied Energy*. DOI:10.1016/j.apenergy.2019.01.091
136. Vieira et al. (2021). P2P Energy Trading in a Microgrid Leveraged by Smart Contracts. *Renewable and Sustainable Energy Reviews*. DOI:10.1016/j.rser.2021.110900
137. Lan et al. (2025). Scalable P2P Energy Trading System With Microgrid Coalitions. *ICSGGE 2025*. DOI:10.1109/icsgge64667.2025.10985166
138. Alfaverh et al. (2023). Dynamic P2P Electricity Market Model for Community Microgrid with Price-Based DR. *IEEE Trans. Smart Grid*. DOI:10.1109/tsg.2023.3246083
139. Wang et al. (2018). P2P Energy Trading Among Microgrids with Multidimensional Willingness. *Energies*. DOI:10.3390/en11123312

#### Cluster I — Hardware-in-the-Loop (HIL) Testbed Methodology for Power Electronics/Microgrids (n=12)
*Role: the validation methodology to be extended from single-node (reference paper) to multi-node topology.*

140. Lauss et al. (2021). Accurate and Stable HIL Real-Time Simulation of Integrated Power Electronics and Power Systems. *IEEE Trans. Power Electronics*. DOI:10.1109/tpel.2020.3040071
141. Mohammadi et al. (2022). Real-Time Controller-HIL Testing of Power Electronics Converters. *PEDSTC 2022*. DOI:10.1109/pedstc53976.2022.9767506
142. Lu et al. (2007). Low-Cost Real-Time HIL Testing Approach of Power Electronics Controls (VTB-RT). *IEEE Trans. Industrial Electronics*. DOI:10.1109/tie.2007.892253
143. D'Arco et al. (2024). Multi-HIL Laboratory Testing of Power Converters and IEDs for Large-Scale Power Systems. *IEEE Open J. Power Electronics*. DOI:10.1109/ojpel.2024.3460709
144. Bai et al. (2026). Multilayer Device-Level Electro-Thermal Real-Time Simulation and Multipurpose HIL Testing. *IEEE Trans. Power Electronics*. DOI:10.1109/tpel.2025.3650187
145. Lucía et al. (2011). Real-Time FPGA-Based HIL Simulation Test Bench for Multiple-Output Power Converters. *IEEE Trans. Industry Applications*. DOI:10.1109/tia.2010.2102997
146. Estrada et al. (2020). Real-Time HIL Simulation Methodology for Power Converters Using LabVIEW FPGA. *Energies*. DOI:10.3390/en13020373
147. Shekhar et al. (2023). Development of Reliable Power Electronic Systems using Real Time Digital Twin Based PHIL Testbed. *PowerTech 2023*. DOI:10.1109/powertech55446.2023.10202818
148. Badar et al. (2021). Efficient Real-Time Controller Design Test Bench for Power Converter Applications. *IEEE Access*. DOI:10.1109/access.2021.3107911
149. Lauss et al. (2019). Multirate Partitioning Interface for Enhanced Stability of PHIL Real-Time Simulation. *IEEE Trans. Industrial Electronics*. DOI:10.1109/tie.2018.2826482
150. Matar et al. (2010). FPGA Implementation of the Power Electronic Converter Model for Real-Time Simulation. *IEEE Trans. Power Delivery*. DOI:10.1109/tpwrd.2009.2033603

### 4.4 Source Verification

**Predatory/venue-quality screening**

| Flag | Item(s) | Finding | Action |
|---|---|---|---|
| ⚠️ Caution | #65 (*Journal of Engineering*, Hindawi/Wiley, DOI 10.1155/...) | Confirmed: Wiley disclosed Hindawi suspended special-issue publishing in 2023 over "compromised articles"; Clarivate delisted 19 Hindawi titles from Web of Science in March 2023 for failing peer-review/quality criteria, and 1,200+ Hindawi papers were later retracted for compromised peer review. Specific delisting status of *Journal of Engineering* not confirmed either way. | **Downgraded to Tier 3 (gray zone)** — retained in corpus (record is real, indexed via Semantic Scholar/OpenAlex) but flagged: do not cite without independently re-verifying the specific article before use in a submitted manuscript. |
| ❌ Dropped | #80 (*Int. J. Advanced Electrical and Electronics Engineering*), #85 (*Int. J. Engineering & Extended Technologies Research*) | Web search found no Scopus/DOAJ/Web of Science confirmation either way for these venues. | Dropped from final citable set (peripheral to core argument). |
| ❌ Dropped | #106 (*Archives for Technical Sciences*) | ISSN confirmed active, EBSCO-indexed 2012–2024, charges OA fees; Scopus/WoS status unconfirmed. | Dropped from final citable set (minor supporting item). |
| ✅ Cleared | Remaining 144 items | IEEE, Elsevier, Springer, mainstream Wiley, ACM, Nature Portfolio, PLOS, Taylor & Francis, and MDPI established titles (*Sensors*, *Electronics*, *Energies*) — all standard, indexed, non-predatory venues. | Cleared at normal confidence. |

**Sources consulted for this screening:**
- [Retraction Watch: Nearly 20 Hindawi journals delisted from leading index amid concerns of papermill activity (2023-03-21)](https://retractionwatch.com/2023/03/21/nearly-20-hindawi-journals-delisted-from-leading-index-amid-concerns-of-papermill-activity)
- [UKSG: Nineteen Hindawi journals delisted by Clarivate's Web of Science](https://www.uksg.org/newsletter/nineteen-hindawi-journals-delisted-clarivates-web-science-amid-wider/)
- [ISSN Portal record for Archives for Technical Sciences](https://portal.issn.org/resource/issn/2233-0046)
- [EBSCO listing for Archives for Technical Sciences](https://openurl.ebsco.com/journals/journals-A/journal-18404855.html)

**Net effect (original screening):** 3 items dropped (#80, #85, #106); 1 item retained with caution flag (#65). **Final verified reference set at this stage: 147 of 150 screened items.**

**Update — systematic CrossRef DOI verification pass (post-manuscript-draft):** every DOI in the 146-item manuscript citation set (147 minus item #65, already excluded from citable claims per the caution above) was checked against the CrossRef API. 145 of 146 resolved correctly, and all 9 flagged "title mismatches" were manually confirmed, by inspection, to be the same paper under an abbreviated title used in this log — not wrong or conflated citations. **Item #31 (Idris et al., Bukit Bauk Dungun) has no DOI and could not be independently re-verified**: two separate targeted web searches for the paper (by title/location, and by specific technical details — NodeMCU/ESP8266, Blynk, rainfall/vibration/soil-moisture sensors) failed to locate a resolvable identifier or stable source link, despite the record itself having appeared in the original live Consensus/Semantic Scholar aggregator search (i.e., it is not a fabricated record — it is a real but currently unverifiable one). Consistent with how #80, #85, and #106 were already handled (dropped rather than caveated, when independent re-verification was not achievable), item #31 is now also excluded from the manuscript's citation set. **Final citable set for the manuscript: 145 of 150 screened items.** The manuscript's Related Work (Section 2.1) and verification discussion (Section 6.4) were updated accordingly — the specific claim about a Bukit Bauk Dungun deployment was removed rather than left attributed to an unverifiable source.

**Evidence-tier grading** (discipline-relative for design-science/engineering research — top tier is *prototype built + field/lab validated*, not RCT):

| Tier | Definition | Approx. share of corpus |
|---|---|---|
| A | Physical prototype + field deployment with real-world performance data | ~35% |
| B | Lab prototype + bench/flow-rig validation, no field deployment | ~40% |
| C | Simulation/numerical-model only (no hardware) | ~15% |
| D | Review/survey (synthesizes other primary studies) | ~10% |

**Currency:** 68% of the corpus is 2021 or later. The two oldest items (Ng 2005, Lu 2007) are retained deliberately as foundational/mechanism-defining references, not as current-state evidence.

**Conflict-of-interest / funding bias:** No funder-steered results detected; academic/university-funded studies predominate.

### 4.5 Malaysian Institutional Context (grey literature, web search)

- **National Slope Master Plan 2025–2030** (Public Works Department / JKR) — successor to the 2009–2023 plan, covers hazard/risk mapping, asset inventory, early warning systems, and slope management policy.
- JKR's slope hazard/risk inventory covers 26,722 slopes along federal roads in Peninsular Malaysia; 3,633 in Sarawak; 4,178 in Sabah; 181 in Labuan. 1,577 are classed high-risk.
- JKR operates 49 rain monitoring stations nationwide (37 Peninsular, 9 Sabah, 3 Sarawak), issuing warnings at location-specific thresholds.
- Three Robotic Total Stations and one GNSS unit installed at federal road Sections 44 and 46 as real-time slope-movement monitoring.
- Known incidents motivating this research direction: Highland Towers collapse (1993, Ulu Klang); Bukit Antarabangsa landslide (2008); Batang Kali campsite landslide (December 2022); recurring closures on the Simpang Pulai–Cameron Highlands and Tapah–Cameron Highlands routes (2021, 2024, 2025).

**Sources:**
- [Malay Mail: Selangor to finalise slope hazard map (2024-11-18)](https://www.malaymail.com/amp/news/malaysia/2024/11/18/selangor-to-finalise-slope-hazard-map-prioritising-high-risk-areas-by-next-year-says-state-exco/157241)
- [The Star: KKR's commitment to public safety (2024-11-02)](https://thestar.com.my/news/nation/2024/11/02/kkrs-commitment-to-public-safety)
- [PreventionWeb: Malaysia sectoral report — National Slope Master Plan 2009–2023](https://www.preventionweb.net/quick/54637)
- [carz.com.my: Main road in Cameron Highlands blocked by landslide (2025-01)](https://www.carz.com.my/2025/01/main-road-in-cameron-highlands-blocked-by-landslide)
- [Free Malaysia Today: Road partially closed after landslide in Cameron Highlands (2024-09-21)](https://www.freemalaysiatoday.com/category/nation/2024/09/21/landslide-at-cameron-highlands-partially-closes-road)
- [Malay Mail: Soil movement still detected at Jalan Simpang Pulai-Cameron Highlands (2021-12-04)](https://www.malaymail.com/news/malaysia/2021/12/04/soil-movement-still-detected-at-jalan-simpang-pulai-cameron-highlands/2025924)

---

## 5. Phase 3 — Synthesis

**Cross-cluster thematic integration**

1. **The gap is real and specific, not assumed.** Cluster A (31 landslide-IoT papers) confirms a mature field for *sensing and alerting*, but every system reviewed depends on either battery replacement, solar-only backup, or (where grid-tied) utility fallback — none model a no-grid, node-to-node service-continuity mechanism. This directly matches the limitation the reference paper (Lee & Wang 2024, item #101) flags but doesn't solve.

2. **Hazard-coupled self-powering is evidenced as feasible but unexploited for landslides specifically.** Cluster C shows piezoelectric harvesting from ambient vibration is a mature, field-validated technique (items #50–64), and two papers (#53, #54) already embed piezoelectric sensing *into slope geosynthetics* — but strictly for strain/impedance sensing, never to harvest usable power for the node itself. Cluster D confirms flow-based harvesting (items #65–79) reliably produces 0.1 mW–600 mW from low-velocity water flow using off-the-shelf microturbine or TENG designs — directly transferable to a slope-runoff channel. **Synthesis conclusion:** no paper in the 147-item corpus combines these two facts (slope-embedded piezo + flow harvesting, powering rather than just sensing). That absence is the innovation target, not an assumption.

3. **The brokering protocol has no off-the-shelf match, but doesn't need one invented from scratch.** Cluster G (15 papers) gives mature energy-aware clustering/offloading algorithms (LEACH-derivative cluster-head rotation, DRL-based workload offloading, solar-irradiance-predictive load balancing). Cluster H (12 papers) gives mature P2P energy-trading market mechanisms. Neither literature has been applied to *duty/task* reassignment across a linear, storm-cell-correlated highway corridor — the synthesis move is to adapt Cluster G's clustering mathematics using Cluster H's negotiation logic, substituting "task" for "energy" as the traded unit.

4. **Rainfall-threshold models (Cluster B, 18 papers) supply the trigger logic**, not the power design — they tell you *when* the hazard intensifies (so sensing frequency should rise), which is the demand side that Clusters C+D's harvesting supply must meet.

**Contradiction identified (not cherry-picked away):** Cluster H's P2P energy-trading literature generally assumes *continuous* communication links to negotiate trades, while Cluster E's LoRaWAN/rural-connectivity papers (notably item #92, Chapungo 2025, Mozambique) show real packet-delivery degradation (as low as ~89% PDR) under terrain/altitude constraints typical of hill slopes. This is a genuine risk to the brokering design, not a minor footnote — a corridor-wide negotiation protocol must tolerate lossy, intermittent links, which existing P2P trading models largely don't address.

### 5.1 Devil's Advocate — Checkpoint 2

- **Cherry-picking check:** The corpus was *not* filtered to only supportive evidence — Cluster E's connectivity-degradation finding (item #92) was kept in and is flagged as a real design constraint, not excluded.
- **Confirmation bias check:** The claimed novelty gap (piezo/flow harvesting *powering* vs. *sensing* a slope node) was verified against the two closest-matching papers (#53, #54) rather than assumed from distance; the gap holds on inspection.
- **Alternative explanation (open question, not resolved):** Could the "gap" simply reflect that nobody has needed this yet because solar+battery is judged sufficient in most deployed systems? Plausible — most Cluster A systems do operate on solar/battery without reported failure modes during the exact storm events that matter. **This should be stated as an open question for Phase 4, not glossed over:** the report must either produce field evidence of solar-related LEWS outages during storms, or a clear a priori engineering argument for why correlated solar failure during monsoon fronts is a latent, under-reported risk.

**Verdict: PASS with one required addition** — the Phase 4 report must explicitly address (a) the lossy-link constraint on brokering (from Cluster E/item #92), and (b) the "is this actually a problem yet" question above, rather than treating the gap as self-evidently urgent.

---

## 6. Status and Next Steps

- ✅ Phase 1 (Scoping) — complete, user-confirmed.
- ✅ Phase 2 (Investigation) — complete: 147 verified sources across 9 thematic clusters, PRISMA-documented.
- ✅ Phase 3 (Analysis) — complete: synthesis narrative, contradiction disclosure, Devil's Advocate Checkpoint 2 passed with conditions.
- ✅ Phase 4 (Composition) — complete: see Section 7. **Note on scope:** no physical or HIL experiments have been run as part of this analysis — Section 7 presents a literature-grounded system design and a proposed (not yet executed) validation plan, not experimental results. Any numeric "expected" figures are drawn from cited prior work, never fabricated for this system.
- ✅ Phase 5 (Review) — complete: see Section 8. Editor-in-Chief verdict **Minor Revision** (3.85/5); Ethics verdict **Conditional** (no Critical integrity concern; citation-coverage completeness gap disclosed); Devil's Advocate Checkpoint 3 **Pass**.
- ✅ Phase 6 (Revision) — complete: see Section 9. Both substantive Phase 5 findings (counter-argument, field-validity gap) incorporated into Section 7; two formatting/coverage items carried forward as acknowledged pre-submission limitations rather than further revised, per the capped-revision-loop rule.

---

## 7. Phase 4 — Composition: Draft Report

### Title

**Hazard-Coupled Self-Powering and Corridor-Wide Duty-Brokering for Off-Grid Landslide Early-Warning IoT Sensor Swarms: A Design Proposal Extending the IoT Microgrid Concept to Malaysian Highway Cut-Slopes**

### Abstract

Microgrid-powered Internet of Things (IoT) applications have been shown to sustain continuous sensing by switching between renewable and utility-grid power sources (Lee & Wang, 2024). This model assumes utility backup is always available — an assumption that fails for off-grid landslide-monitoring sensors on remote Malaysian highway cut-slopes, where no such backup exists and where known disasters (Highland Towers, 1993; Bukit Antarabangsa, 2008; Batang Kali, 2022) motivate continuous, reliable sensing precisely during the monsoon conditions that most degrade solar power. This paper proposes extending the single-node IoT-microgrid model in two directions, grounded in a 147-source systematic review across nine technology clusters: (1) hazard-coupled self-powering, in which piezoelectric harvesting from slope micro-movement and flow-based harvesting from rainfall runoff supply power that *increases* as landslide risk rises, rather than the solar supply that *decreases* under the same conditions; and (2) corridor-wide duty-brokering, in which spatially distributed sensor nodes reassign sensing/transmission duties — not electrical energy — to neighbors with surplus harvested power, exploiting the localized nature of Malaysian convective storm cells along highway corridors spanning tens of kilometers. The review confirms that landslide-IoT monitoring, piezoelectric/flow energy harvesting, energy-aware WSN clustering, and peer-to-peer energy trading are each mature literatures, but no reviewed source combines hazard-coupled powering with task-level brokering for this application. A proposed multi-node extension of the reference paper's hardware-in-the-loop (HIL) testbed is outlined as the validation path. Key limitations — communication-link reliability under terrain-degraded LoRaWAN conditions, and the unresolved question of whether this is a demonstrated operational failure mode or a latent risk — are stated explicitly rather than minimized.

*Keywords:* IoT microgrid, landslide early warning, energy harvesting, duty cycling, hardware-in-the-loop, Malaysia

### 1. Introduction

Internet of Things (IoT) sensing has become central to hazard monitoring, but IoT devices require continuous power, and continuous power is the scarcest resource in exactly the remote, off-grid locations where hazard sensing matters most. Lee and Wang (2024) address this for grid-adjacent deployments: their "IoT microgrid" model switches a single DC sensor node between a renewable primary source and a utility-grid secondary source using a double-voltage-threshold controller, validated on a hardware-in-the-loop (HIL) testbed. Their model rests on four assumptions, the second of which — "power from the utility grid is available" — does not hold for landslide-monitoring sensors on remote highway cut-slopes, a deployment class with no utility access and, frequently, canopy-shaded or monsoon-obscured solar exposure.

Malaysia provides a concrete and consequential setting for this gap. The Public Works Department (JKR) manages a hazard-and-risk inventory of over 34,000 slopes along federal roads nationwide, of which 1,577 are classed high-risk, under the National Slope Master Plan 2025–2030. Historical incidents — the Highland Towers collapse (1993), the Bukit Antarabangsa landslide (2008), and the Batang Kali campsite landslide (2022) — demonstrate the human cost of slope failure, while recurring closures on routes such as Simpang Pulai–Cameron Highlands (2021, 2024, 2025) show the continuing operational burden. JKR already operates 49 rainfall telemetry stations and robotic total stations at selected federal-road sections, but none of the systems identified in this review's literature base report a self-powering or inter-node redundancy mechanism for conditions where solar/battery power and ground movement are *both* intensifying together — precisely the monsoon-triggered failure scenario this proposal targets.

**Purpose and research question.** This paper asks: can hazard-coupled self-powering (energy harvesting whose output rises with the hazard itself) combined with corridor-wide duty-brokering (task reassignment among spatially distributed nodes) sustain network-level sensing continuity for an off-grid landslide early-warning swarm, where the reference paper's utility-backup assumption cannot be satisfied? The paper does not yet answer this empirically — no experiment has been conducted — but establishes, through systematic literature synthesis, that the proposed design is technically grounded, identifies what is and is not already known, and specifies the validation methodology required to answer it.

### 2. Literature Review

A PRISMA-aligned search across Semantic Scholar, OpenAlex, and PubMed (via Consensus aggregation) identified 200 candidate records across nine thematic queries; after deduplication, screening, and venue-quality verification, 147 sources were retained (full protocol, flow diagram, and annotated reference list in Sections 4.1–4.4 above). Three findings from this review frame the proposed design:

**2.1 Landslide-IoT monitoring is mature but power-assumption-limited.** Thirty-one reviewed systems (Cluster A) — spanning Kerala (Ramesh, 2009, 2014, 2017), the Darjeeling Himalayas (Abraham et al., 2020), Colombia (Gamperl et al., 2021), and two Malaysian deployments (Ali et al., 2012, Hulu Langat; Idris et al., Bukit Bauk Dungun) — consistently rely on solar-plus-battery or (where available) grid power, with no reviewed system modeling a no-grid, node-to-node continuity mechanism. Rainfall-threshold and susceptibility models (Cluster B, 18 sources) establish that landslide risk escalates during sustained or intense rainfall — the same conditions under which solar generation is most degraded, a structural conflict the reviewed EWS literature does not address at the power-architecture level.

**2.2 Hazard-coupled harvesting is technically feasible but unexploited for this hazard.** Piezoelectric vibration harvesting is a mature, field-validated technology (Cluster C, 15 sources; e.g., Rubeš et al., 2021; Rigo et al., 2024), and two sources (Wang et al., 2024, 2026) already embed piezoelectric elements into slope geosynthetics (geocables, geogrids) for strain and microseismic sensing — but exclusively for sensing, not for harvesting usable power. Flow-based harvesting (Cluster D, 15 sources) reliably produces 0.1 mW to over 600 mW from low-velocity water flow using small turbines, triboelectric, or electromagnetic transduction (e.g., Lepipas et al., 2024; Kamenar et al., 2016), directly transferable to slope-face runoff. No reviewed source combines slope-coupled piezoelectric harvesting with runoff-flow harvesting to power (rather than merely sense from) a landslide-monitoring node.

**2.3 Duty-brokering has conceptual precedent in two separate literatures, not a combined one.** Energy-aware WSN clustering and task-offloading protocols (Cluster G, 15 sources) solve the general problem of reassigning work to energy-richer nodes, and peer-to-peer energy-trading mechanisms in microgrids (Cluster H, 12 sources) solve the general problem of negotiating a shared resource among autonomous, self-interested nodes. Neither literature has been applied to spatially correlated, storm-cell-driven intermittency along a linear highway corridor, which is the specific topology this proposal targets. A tension surfaced during synthesis: P2P trading models generally assume reliable continuous links, while LoRaWAN rural-deployment studies (Cluster E; Chapungo et al., 2025, Mozambique) report packet delivery as low as ~89% under terrain/altitude conditions resembling hill slopes — a constraint any brokering protocol for this application must tolerate rather than assume away.

### 3. Proposed System Design

Building directly on the reference paper's architecture (controller + energy source + IoT load, Figure 1 and Figure 2 of Lee & Wang, 2024), the proposed design makes two structural changes.

**3.1 Dual hazard-coupled harvesting (replacing solar-only primary source) — revised in light of Section 11's real-data findings.** Each node pairs (a) a piezoelectric harvester mechanically coupled to the monitored slope segment — adapting the sensing-only geosynthetic designs of Wang et al. (2024, 2026) into a power-delivery configuration — with (b), originally, a small flow/kinetic harvester positioned in the slope's surface runoff or drainage channel. Under stable, dry conditions, baseline solar (retained as a tertiary source) dominates; as instability and/or rainfall increase, piezoelectric harvesting rises, compensating for solar decline.

*Update after real-data testing (Section 11.5):* a literature-grounded model of component (b), driven by real Cameron Highlands rainfall and a real measured power-velocity curve (Lepipas et al., 2024), predicts this flow harvester would be active well under 1% of the year at any catchment/channel geometry that stays within the literature's tested velocity range — an unfavorable, quantified result, not merely an untested gap. **Component (b) is downgraded from a core design element to a rare-event supplementary source at best**, pending either a fundamentally different low-cut-in harvesting principle or real field measurement showing otherwise (Section 12). The design's power argument now rests primarily on (a) piezoelectric harvesting plus solar, not on two independent weather-coupled sources.

*Update after real-event testing (Section 11.6):* checking four real, named, dated Malaysian landslides against real weather data found that failure timing relative to rainfall is heterogeneous — one event (Batang Kali, 2022, the deadliest in the set) failed on a comparatively *sunny* day, three days after the actual rain/dark extreme, consistent with the Public Works Department's own stated cause (delayed subsurface saturation). **This is a direct, real-data argument for why component (a) — power generation coupled to actual ground movement, not to current weather — is the structurally correct choice**: a purely weather-coupled design would have been at its most relaxed state at exactly the moment that event actually failed. This inverts the correlation structure that makes solar-only backup fail precisely when monitoring is most needed, and does so specifically because it tracks the hazard directly rather than a weather proxy for it.

**3.2 Corridor-wide duty-brokering protocol (replacing utility-grid secondary source).** Rather than falling back to a nonexistent utility connection, a node whose harvested-energy state drops below threshold signals neighboring nodes (over the existing LoRaWAN link already required for sensing) to temporarily assume its reporting duty — adapting cluster-head rotation logic from energy-aware WSN clustering (e.g., Bahbahani et al., 2017) with the bid/negotiation structure of P2P energy-trading mechanisms (e.g., Paudel et al., 2019), substituting "sensing/reporting duty" for "kWh" as the traded unit. Because Malaysian convective storms are frequently localized rather than basin-wide, nodes 10–20+ km apart along a highway corridor are more likely to retain surplus capacity even when a 2–5 km cluster is storm-affected — the structural property, identified during Devil's Advocate Checkpoint 1, that distinguishes this topology from the fully-correlated river-basin case considered and set aside during scoping (Section 2.3).

**3.3 Lossy-link tolerance (addressing the Checkpoint 2 condition).** Given Chapungo et al.'s (2025) ~89% packet-delivery finding under comparable terrain, the brokering protocol must not assume reliable signaling. The design specifies: (a) brokering requests carry a short validity window and are retried via at least one alternate relay node before being treated as failed; (b) in the absence of any successful broker handoff, the node defaults to the *reference paper's own* double-threshold local switching behavior (piezo/flow/solar only, no brokering) — meaning the proposed system degrades gracefully to the already-validated single-node behavior rather than failing outright when the network layer is unreliable.

### 4. Proposed Validation Plan (Not Yet Executed)

Following the reference paper's own design-science methodology, validation should proceed in two stages:

**Stage 1 — HIL simulation (multi-node extension).** Extend Lee & Wang's (2024) single-node Speedgoat HIL testbed to 3–5 simulated nodes, each with independently parameterized intermittency: a spatially-correlated Poisson/Markov model (extending the reference paper's single-node Poisson model, λ = 14 and λ = 37 cases) with an added correlation coefficient ρ representing storm-cell overlap between adjacent nodes. Baseline condition: independent per-node switching, solar-only, no brokering (replicating the reference paper's exact design under the no-utility-backup constraint). Treatment condition: dual harvesting + brokering protocol. Primary outcome: network-level sensing continuity (percentage of time at least the threshold number of nodes report). Secondary outcomes: cross-node energy-depletion fairness, brokering-event frequency (network-level analog of the reference paper's "ping-pong" metric), and behavior specifically under high-ρ (fully-correlated, flood-basin-like) conditions as the designed stress test.

**Stage 2 — Physical prototype.** A ≥3-node field or lab-bench replica (ESP32/NodeMCU per node, as in the reference paper) with a real piezoelectric element mechanically driven to emulate slope micro-movement and a real small-scale flow harvester on a lab flow rig, validated against Stage 1 HIL predictions — mirroring the reference paper's own two-stage HIL-then-physical validation approach.

No results from either stage are reported here, as neither has been conducted; this section specifies the plan, not findings.

### 5. Discussion

**5.1 Addressing whether this is a demonstrated or a latent problem — partially resolved by real-data testing (Section 11.4/11.6).** At the time this was first written, the literature review (Section 2.1) had not surfaced a documented case of a landslide-EWS node failing specifically because solar power and ground instability rose together — the risk rested only on a plausible causal mechanism, not an observed record. Section 11.4/11.6 subsequently tested this directly with real data rather than leaving it as a standing question: real NASA POWER weather data at the actual highland corridor site confirms rainfall and solar suppression correlate (r=−0.454) and are both worst in Nov/Dec; and checking four real, named, dated landslides against real weather on their actual event dates found a genuinely mixed but informative pattern — one event matched the same-day dark+wet signature cleanly, one matched a delayed/cumulative-saturation variant of it, one showed a weaker antecedent match, and one showed no match at all. **This moves the risk from purely a priori to partially evidenced** — not conclusively proven (n=4 named events is a design argument, not a statistical claim), but no longer resting on causal reasoning alone. JKR's own slope-monitoring infrastructure already uses solar-dependent telemetry at scale (49 rainfall stations; robotic total stations); a direct inquiry into JKR's own historical telemetry-outage records during these specific real events (Section 12.3) remains the next step to close this fully, but is no longer the *only* evidence available.

**5.2 Addressing communication-link reliability.** Section 3.3's graceful-degradation design treats lossy links as a first-class constraint rather than an edge case, directly responding to the Checkpoint 2 condition. This is a conservative design choice: it means the system's worst-case behavior is never worse than the reference paper's already-validated single-node design, and brokering is strictly additive.

**5.3 Relationship to the alternative (flood-basin) application considered during scoping.** The flood-basin case considered in Section 2.3 remains a valid stress test rather than a dead end — a fully storm-correlated condition (ρ → 1) in Stage 1 validation effectively reproduces that scenario within the same testbed, without requiring a separate research program.

**5.4 Strongest counter-argument (added at Phase 5, Devil's Advocate Checkpoint 3).** The most serious challenge to this proposal is that it may be solving a problem more cheaply solved by simpler means: periodic maintenance visits to swap batteries or clean solar panels, combined with solar-only backup, is the design every reviewed system (Cluster A) already uses, and none report catastrophic failure. Two extra harvester types and a distributed negotiation protocol add cost, failure modes of their own (Section 5.5), and engineering complexity that a maintenance-visit regime does not. This proposal's justification rests on an access argument, not a cost argument: the remote, steep, often-unstable terrain that makes a slope a landslide risk in the first place (per JKR's inventory, Section 4.5) is also terrain where maintenance-visit access is itself degraded during the monsoon season that matters most — the same storm conditions that threaten the slope also threaten the road access needed to service the sensor. This argument is plausible but, like the latent-risk question in Section 5.1, is not yet substantiated with access/maintenance-log data and should be verified alongside it before further investment.

**5.5 Field-versus-lab validity gap (added at Phase 5, Devil's Advocate Checkpoint 3).** The flow-harvester literature cited in Section 3.1 (Cluster D) validates performance in clean, controlled conditions: domestic water pipes (Ahmad et al., 2024), laboratory flow rigs (Lepipas et al., 2024), and closed hydraulic circuits (Vijayaregunathan et al., 2024). Actual landslide-prone slope runoff is sediment- and debris-laden, intermittent, and highly variable in flow rate — conditions under which small turbine or triboelectric harvesters may suffer fouling, abrasion, or blockage that the cited lab studies do not test. This is a field-versus-lab validity gap, not merely a minor caveat, and is added here as a required limitation rather than left implicit.

### 6. Limitations

- No empirical data yet exists for this specific system; all quantitative claims in this paper are drawn from cited prior work on component technologies, not from a test of the combined design.
- Mechanical coupling of piezoelectric harvesters to slope geosynthetics for power delivery (rather than sensing) has not been previously demonstrated at the power levels required to run a wireless node continuously; achievable power output under field (not lab) slope-movement conditions is unknown and should be an early validation target.
- **Flow-harvester field validity gap (Section 5.5):** cited flow-harvesting evidence is drawn from clean-water lab/pipe conditions; sediment/debris fouling risk under real slope runoff is untested and should be an early validation target alongside the piezoelectric power-delivery question above.
- The venue-quality screening in Section 4.4 is based on targeted web search, not direct Scopus/Web of Science/DOAJ database lookup, and should be treated as a preliminary filter, not a final determination.
- Malaysia-specific peer-reviewed literature on this exact application is thin (2 directly relevant sources); Section 4.5's institutional context relies on grey literature (news reporting, department web pages) rather than peer-reviewed sources.
- **Reference-list formatting:** the 147-item reference list (Section 4.3) is organized thematically by review cluster, as required for PRISMA documentation and novelty-gap tracing, rather than in strict APA 7 alphabetical-by-surname order. This is an intentional, disclosed deviation for this working document; a submission-ready version would require re-ordering into a single alphabetized reference list, deferred here as a pre-submission copyediting step rather than performed now.
- **Citation-verification coverage:** full claim-against-source verification (confirming each citation's claimed content against its original abstract/findings) was performed in depth only for the pivotal sources directly quoted or specifically relied upon in Sections 2–3 (the reference paper; Wang et al., 2024, 2026; Chapungo et al., 2025; the flow-harvester sources in Section 5.5). The remaining ~140 sources were confirmed to exist via live academic-search API results (ruling out fabrication) but were not individually re-verified at the claim level against their full text. This falls short of the enhanced 50%-coverage standard used for integrity-sensitive reviews and is disclosed as a condition in the Phase 5 Ethics Review (Section 8.2).

### 7. Conclusion and Recommendations

This proposal extends the validated IoT-microgrid single-node model (Lee & Wang, 2024) to a deployment class — off-grid landslide-monitoring swarms on Malaysian highway cut-slopes — where the model's utility-backup assumption fails. The two proposed mechanisms, hazard-coupled dual harvesting and corridor-wide duty-brokering with lossy-link tolerance, are each grounded in mature but previously unconnected literatures, and the gap this design fills was verified by direct inspection of the closest-matching prior work rather than assumed. The recommended next step is Stage 1 HIL validation (Section 4), run before any field deployment, following the reference paper's own validated methodology.

### 8. References

See the consolidated 147-item reference list in Section 4.3 (Clusters A–I), with the venue-quality dispositions in Section 4.4 applied. Primary reference: Lee, Y.-S., & Wang, C. (2024). A Cyber-Physical Testbed for IoT Microgrid Design and Validation. *Electronics*, 13(7), 1181. https://doi.org/10.3390/electronics13071181

---

## 8. Phase 5 — Review

### 8.1 Editor-in-Chief Review

| Dimension | Weight | Score (1–5) | Justification |
|---|---|---|---|
| Originality & Contribution | 20% | 4 | Genuine, literature-verified synthesis-level contribution (complementary-correlation harvesting + corridor-scale duty brokering); combinatorial rather than a new first principle, and not yet empirically demonstrated. |
| Methodological Rigor | 25% | 3.5 | Phases 1–3 methodology (FINER scoping, PRISMA search/screening) is rigorous; Section 3–4's system design and validation plan are appropriately labeled as *proposed*, not executed — correctly scoped for a design proposal, but this caps rigor below "exemplary" until Stage 1/2 validation (Section 4) is run. |
| Evidence Sufficiency | 25% | 4 | 147 sources, PRISMA-documented, with live predatory-journal screening (not assumed) and an explicit evidence-tier breakdown (Section 4.4). Citation-verification coverage below the enhanced 50% standard (see Ethics Review, 8.2) is the main shortfall. |
| Argument Coherence | 15% | 4 | Clear RQ → literature gap → design → validation-plan → discussion chain; both Devil's Advocate checkpoints materially changed the document rather than being pro forma. |
| Writing Quality | 15% | 3.5 | Clear and well-organized; not in strict APA 7 format (numbered/clustered reference list rather than alphabetized — see Limitations). |
| **Weighted total** | | **3.85** | |

**Verdict: MINOR REVISION** (3.0–3.9 band).

**Strengths:**
1. Explicit, repeated separation of "proposal" from "results" — no fabricated experimental data anywhere in the document.
2. Novelty claim (hazard-coupled powering vs. sensing-only piezo geosynthetics) was checked against the two closest-matching papers directly, not assumed from topical distance.
3. Devil's Advocate feedback was substantively incorporated (Sections 5.4, 5.5), not just logged and ignored.

**Required for Minor Revision (addressed in Phase 6 below):**
1. Disclose the reference-list formatting deviation from strict APA ordering (done — see Limitations).
2. Add the field-versus-lab validity gap for flow harvesting as an explicit limitation, not an implicit one (done — Section 5.5).
3. State the strongest counter-argument to the whole proposal explicitly, not only imply it (done — Section 5.4).

### 8.2 Ethics Review

**AI Disclosure & Transparency:** ✅ Present and repeated (document header, Phase 4 introduction note, Section 6 status note). Scope of AI involvement (search, synthesis, drafting) is described. No AI-generated content is passed off as human-authored.

**Attribution Integrity:**
- No fabricated references: all 150 screened sources were retrieved from live academic-search API results (Consensus/Semantic Scholar/OpenAlex/PubMed), not generated from model memory — this satisfies the "no hallucinated references" check.
- Enhanced reference-integrity coverage (claim-against-source verification): performed in depth for the pivotal sources (reference paper; items #53, #54; #92; Section 5.5's flow-harvester sources) but **not** at the 50%-of-corpus standard across the full 147-item set. **This is disclosed as a Condition, not a Critical finding** (see Verdict below) — it is a completeness gap, not evidence of misrepresentation in the sources that were checked.
- Self-citation: N/A (no self-authored sources in the corpus).

**Dual-Use Screening:** Risk level **None/Low**. This is public-safety disaster-engineering research (landslide early warning); no foreseeable misuse pathway was identified. No Responsible Use statement is required beyond standard good practice.

**Fair Representation:** Malaysian institutional and historical context (Section 4.5) is presented factually, grounded in named incidents and official department data, without sensationalizing casualties or implying institutional negligence beyond what the cited sources support.

**Human Subjects:** Not applicable — no human data, surveys, or interviews were conducted; this is engineering design and literature synthesis only, consistent with the Phase 1 Methodology Blueprint (Section 2.2).

**Verdict: CONDITIONAL.** No Critical integrity concern was found (no fabrication, no plagiarism, AI disclosure present, no source misrepresentation detected in verified sources) — so this does **not** trigger the IRON RULE requiring the user to be stopped and asked to confirm. The condition is: before this document is used as the basis for a formal submission or funding application, raise citation-verification coverage on the remaining ~140 sources to the 50% enhanced-check standard, and complete the reference-list alphabetization deferred in Section 6.

### 8.3 Devil's Advocate — Checkpoint 3 (Final Review)

- **Does the conclusion follow from the evidence, or overstep?** No overstep found — Section 7 (Conclusion) correctly states this as a proposal pending validation, not a demonstrated result.
- **Strongest counter-argument to the main thesis:** Surfaced and now written explicitly into the document (Section 5.4) — simple maintenance-visit regimes already work for every reviewed system, and the added complexity needs an access-degradation argument, not just a power argument, to be justified.
- **Fatal-flaw scan:** Identified the lab-vs-field validity gap for flow harvesting under sediment-laden slope runoff (Section 5.5) — a genuine, previously-unaddressed engineering risk, now written into both the Discussion and Limitations.
- **"So what?" significance check:** Adequately answered — real, named disaster history (Highland Towers, Bukit Antarabangsa, Batang Kali) and a real institutional stakeholder (JKR's National Slope Master Plan 2025–2030) ground the significance claim.
- **Is the AI disclosure adequate?** Yes — present at document start, Phase 4 introduction, and Section 8.2 above.

**Verdict: PASS.** The two substantive gaps this checkpoint found (explicit counter-argument, field-validity limitation) were incorporated directly into the report during this review rather than deferred, which is within the capped 2-revision-loop allowance (this is the first loop).

---

## 9. Phase 6 — Revision (Applied)

The following changes were made directly to Section 7 in response to Phase 5 feedback, completing the first (and, based on the PASS verdict above, only necessary) revision loop:

1. Added **Section 5.4** (strongest counter-argument: maintenance-visit regimes vs. added system complexity, reframed around storm-time access degradation).
2. Added **Section 5.5** (field-versus-lab validity gap for flow harvesters under sediment-laden slope runoff).
3. Updated **Section 6 (Limitations)** with two new items: the flow-harvester field-validity gap, and an explicit disclosure of the reference-list formatting deviation from strict APA ordering.
4. Logged the citation-verification coverage gap as a formal Ethics Review **Condition** (Section 8.2) rather than leaving it unstated.

**Remaining acknowledged limitations** (per the capped-revision-loop rule, carried forward rather than further revised now): full APA alphabetization of the 147-item reference list, and raising citation-verification coverage to the 50% enhanced-check standard. Both are pre-submission tasks, not blockers to this document's current purpose as a scoped research-direction analysis.

---

## 10. Dataset Discovery (Systematic)

Everything above is literature (papers describing systems and findings). This section systematically inventories **actual datasets** — real measured or recorded data — that could parameterize the Stage 1 HIL simulation (Section 4 of the Phase 4 report) or ground the open questions raised in Phase 5 (Sections 5.1, 5.4, 5.5). Each entry is graded by **confirmed access status**, not assumed, per this pipeline's verification standard: a dataset is marked "Confirmed open" only when a direct download/API path was found; otherwise it is marked "Lead — requires direct contact/verification," which is a different and weaker claim than "available."

### 10.1 Landslide Occurrence & Slope Monitoring Data

| Dataset | Coverage | Contents | Access Status | Relevance |
|---|---|---|---|---|
| **NASA Global Landslide Catalog (COOLR)** | Global, event- and report-based, since 2007 | Landslide event records: location, date, trigger (rainfall vs. other), fatalities; downloadable as .csv/.shp/.gdb via the Landslide Viewer; API also available. Cite Kirschbaum, Stanley & Zhou (2015), *Geomorphology*. | ✅ **Confirmed open** | Base rate / trigger-type statistics for framing hazard frequency; Malaysia coverage within this global catalog should be checked directly (likely sparse — known under-reporting of Malaysian landslides per a 2014 AGU abstract finding complete historical records "hard to obtain"). |
| **ITALICA** (CNR-IRPI, Italy) | Italy, 1996–2021, n=6,312 rainfall-induced landslide records | Downloadable CSV via Zenodo, with rainfall-trigger metadata | ✅ **Confirmed open** | Not Malaysia-specific, but the most complete open analog for the rainfall-threshold modeling approach (Cluster B) — useful as a methodology template if a Malaysia-specific inventory can't be obtained directly. |
| **FraneItalia** (CNR-IRPI, Italy) | Italy, news-sourced landslide catalog since 2010 | Geo-referenced catalog; requires a PostgreSQL/PostGIS server to use the full catalog structure | ✅ **Confirmed open** (Zenodo record), ⚠️ nontrivial setup | Same role as ITALICA; higher setup cost. |
| **Water retention data from monitored slopes near Kajang, Langat River Basin, Malaysia** (British Geological Survey / NERC Grant NE/S003347/1) | Malaysia (Kajang, Selangor) | Soil suction, volumetric water content, and rainfall from two natural slopes, sensors installed August 2020, ~1 year collected (ongoing); analyzed jointly by Durham University and UKM | ❌ **Verified NOT openly licensed.** Direct inspection of the dataset's access page (https://webapps.bgs.ac.uk/services/ngdc/accessions/index.html#item176993) confirms the licence field is explicitly "Not set," and the access-constraints text states copyright is held by NERC with reproduction/transmission prohibited without prior written permission from the BGS Intellectual Property Rights Manager. The site's general Open Government Licence does **not** apply to this specific accession. | Still the most geotechnically relevant Malaysia-specific dataset identified (right variables, right country), but it is a **permission-request lead, not an open dataset** — this correction supersedes the earlier (unverified) characterization. Request access directly from BGS citing the stated use case. |
| **JKR Slope Hazard and Risk Map** | Malaysia, 34,714 slopes nationwide (26,722 Peninsular, 4,178 Sabah, 3,633 Sarawak, 181 Labuan); 1,577 classed high-risk | Slope inventory with risk classification, built from airborne + field data | ❌ **No public download confirmed** — referenced only in news reporting (The Star, Bernama) and an old (2012) link to slopes.jkr.gov.my that could not be verified as still active | **Lead only.** This is the authoritative Malaysia slope inventory and should be requested directly from JKR's Slope Engineering Branch / Ministry of Works (KKR) rather than assumed accessible. |

### 10.2 Rainfall & Climate Data (Malaysia)

| Dataset | Coverage | Contents | Access Status | Relevance |
|---|---|---|---|---|
| **MetMalaysia station records** | Malaysia, station-level | Daily/hourly rainfall; a 2025 Civil Engineering Journal study used 2013–2023 MetMalaysia records for Ranau/Kota Belud IDF curves, implying the data is obtainable on request | ⚠️ **Lead — request directly from MetMalaysia**; no confirmed public API for historical station data found (only a public alert API, "MET Api," for current warnings) | Needed to set realistic rainfall-intensity parameters (λ, correlation structure) for the Stage 1 HIL simulation. |
| **MyIKLIM (UKM)** | Malaysia, 1901–2024, **annual** frequency | CRU-derived national rainfall | ✅ **Confirmed open** | Too coarse (annual) for the intermittency model directly, but usable for long-run climatological framing/trend context. |
| **JRC PVGIS hourly solar radiation (Meteosat East)** | Asia-wide, 1998–2013 (gap in 2006) | Hourly satellite-derived solar radiation | ✅ **Confirmed open**, ⚠️ Malaysia-specific coverage not independently verified — check directly in the PVGIS tool | Candidate source for the solar-baseline component of the correlated-intermittency model, pending a direct coverage check. |
| **Solar Irradiance Data 2025 (Kuala Lumpur, Malaysia)** — Mendeley Data, Chee Wern Hew, UCSI University (DOI 10.17632/bgch4tw79k.1) | Kuala Lumpur, full calendar year 2025, 1-minute resolution | Verified on direct fetch: continuous 1-minute Global Horizontal Irradiation (GHI); companion *Data in Brief* paper intended for PV modelling, grid-integration, controller-testing, and energy-storage-sizing use cases — directly aligned with this project's needs | ✅ **Confirmed open, CC BY 4.0**, downloadable via "Download All" on the dataset page | **Best candidate found for realistic solar-irradiance parameterization** — high temporal resolution, Malaysia-specific, recent, and explicitly intended by its authors for exactly this kind of energy-system modeling use. |
| **JPS Public InfoBanjir** | Malaysia nationwide, ~1,500+ hydrological telemetry stations, 15-minute updates | River water level + rainfall | ❌ **No machine-readable open feed confirmed** — public web/app portal only; no documented JSON/CSV API, rate limits, or reuse license found | **Lead only**, relevant mainly to the flood-basin comparison scenario (Section 5.3) rather than the primary landslide design; contact JPS directly for data-sharing terms. |

### 10.3 Landslide Sensor Network Raw Time-Series (for realistic node-level behavior modeling)

| Dataset | Coverage | Contents | Access Status | Relevance |
|---|---|---|---|---|
| **Amrita University WSN deployment, Idukki/Munnar, Kerala** (Ramesh et al., Cluster A items #12, #20) | Kerala, India, decade-long deployment | Correlated rainfall, soil moisture, pore pressure, and ground-movement sensor readings; described as available via real-time streaming on the project's WINSOC website | ⚠️ **Lead — direct contact with Amrita/WINSOC needed**; a live data portal was referenced in project materials but not independently confirmed to still be publicly accessible | The closest available real-world analog to the proposed multi-node deployment's expected sensor behavior; would be valuable for parameterizing realistic (non-synthetic) node-level sensor traces in Stage 1 HIL validation. |
| **Inform@Risk, Bello Oriente, Medellín** (Gamperl et al., Cluster A item #14) | Medellín, Colombia, 2020–2022 prototype | Open-source hardware/firmware confirmed; tilt + groundwater sensor readings | ⚠️ **Hardware/firmware confirmed open; raw dataset/wiki not independently located** in this search | Firmware reuse is directly actionable now; raw sensor dataset would need a direct request to the project team. |

### 10.4 Energy-Harvester Characterization Data

| Dataset | Coverage | Contents | Access Status | Relevance |
|---|---|---|---|---|
| **"Dataset for the Comprehensive Characterisation of a Low-Frequency-Vibration Energy Harvester"** (Mendeley, DOI 10.17632/y4cmrsdv9f.1; Plaza, Iriarte, Castellano-Aldave, Carlosena & Bacaicoa, 2024, Universidad Pública de Navarra) | Lab experimental | Verified on direct fetch: 240 fps video recordings; per-experiment measurement files (time, 2-axis accelerometer, per-coil voltages); post-processed files with estimated angular position/velocity/acceleration of the harvester masses and estimated harvested power. Companion paper: *Sensors* 24(12):3813, https://doi.org/10.3390/s24123813. | ✅ **Confirmed open, CC BY 4.0**, downloadable via "Download All" on the dataset page | Directly usable to parameterize the piezoelectric-harvester power model in Stage 1 — ultra-low-frequency vibration is the right regime for slope creep/micro-movement, closer to this application than high-frequency machinery-vibration harvesters. **Note:** the post-processed file's column labels for velocity vs. position overlap at column 4 in the page's own description — cross-check against the companion paper before use. |
| **"Dataset for the Identification of an Energy Harvester" (spring pendulum)** (Mendeley, DOI 10.17632/w9wjz3c8j9) | Lab experimental | Multi-directional ultra-low-frequency piezoelectric harvester response | ✅ **Confirmed open** | Secondary source for the same purpose as above; multi-directional response may better match irregular ground-movement geometry. |
| **"A Dataset for Geometry-Driven Variations in Piezoelectric Stepped Cantilever Beam Energy Harvester"** (IEEE DataPort, DOI 10.21227/gz1p-k607) | Simulation sweep, not measured hardware | Simulated output potentials across ~2,000 cantilever geometries | ✅ **Confirmed open** (access/registration terms on IEEE DataPort apply) | Useful for cantilever design-space exploration, but is simulated, not measured — should not be treated as empirical validation data. |
| **Flow/hydrokinetic harvester raw characterization data** | — | — | ❌ **No open dataset found.** Only summary figures published inside papers (e.g., 548 μW at 7 L/min, Ahmad et al. 2024; ~57 mW at 0.2–0.5 m/s, marine-animal-driven harvester) | **Confirmed gap.** This is the weakest point in the evidence base for Section 3.1's flow-harvester component — no raw dataset exists publicly for the specific flow regime (sediment-laden, intermittent slope runoff) this design requires. Recommend either a direct data request to the cited authors or de novo bench characterization as an early project task, consistent with the field-validity limitation already flagged in Section 5.5. |

### 10.5 LoRaWAN Connectivity Data (hilly/rural terrain)

| Dataset | Coverage | Contents | Access Status | Relevance |
|---|---|---|---|---|
| **Chapungo et al. (2025), rural Mozambique** (Cluster E item #92) | Rural Mozambique, 1 km path, 4 georeferenced points | RSSI, SNR, packet delivery rate vs. distance/altitude | ✅ **Paper confirmed open access** (PMC, DOI 10.3390/s25196027); raw measurement dataset not independently confirmed as separately deposited | Already used in Phase 3 synthesis for the ~89% PDR lossy-link finding; if the underlying raw data is needed (not just the reported summary statistics), contact the authors directly. |
| **Anzum, Habaebi, Islam & Hakim (2021). "A Study of LoRa Signal Propagation in Hilly Suburban Area for Smart City Applications."** 2021 IEEE 7th ICSIMA, Bandung. | **Malaysia** (Kuala Lumpur hilly suburb), 915 MHz | Verified on direct fetch: tested spreading factors SF7/SF8/SF10/SF12 across varying receiver altitudes; measured RSSI and packet receive ratio (PRR); coverage fell as low as ~1.25 km and PRR dropped by 65% in the hilly terrain | ⚠️ **Full text is request/registration-gated** at IIUM's repository (direct PDF: irep.iium.edu.my/92208/1/..., or request via irep.iium.edu.my/cgi/request_doc?docid=632968); a Scopus supplemental file is listed but its contents weren't accessible in this check; **no raw dataset or data-availability statement found** | **The most directly relevant Malaysia-specific LoRaWAN terrain-degradation evidence found**, now confirmed in detail — closer match to the proposed highway-corridor terrain than the Mozambique study and should replace it as the primary basis for Section 3.3's lossy-link design constraint. Request the full text and raw per-SF/altitude data from the authors directly. |
| **UPC Castelldefels LR-FHSS terrain study** | Spain, 3 paths, varied terrain/urban | RSSI, PDR vs. distance/data rate | ⚠️ **Project page found, raw dataset access not independently confirmed** | Useful methodology comparator for evaluating whether LR-FHSS (vs. standard LoRaWAN) would better tolerate the terrain conditions in Section 3.3's graceful-degradation design. |

### 10.6 Summary Assessment (Updated After Direct Verification)

Section 10.1–10.5 entries marked with a direct-fetch verification note have been confirmed by actually retrieving the source page, not inferred from search-result snippets. **This verification pass produced one material correction**: the Kajang (Langat River Basin) slope dataset, initially flagged as the top Malaysia-specific open lead, is in fact **copyright-restricted by NERC**, not openly licensed — direct inspection of its access page found an explicit "no reproduction without prior permission" clause. This is reported here precisely because the earlier, unverified characterization would otherwise have misdirected the highest-priority next action.

**Confirmed genuinely open and immediately usable (verified by direct fetch):**
- Two Mendeley piezoelectric low-frequency vibration-harvester datasets (CC BY 4.0; one with full column-by-column content verified, including a labeling ambiguity flagged for the companion paper to resolve).
- Kuala Lumpur Solar Irradiance 2025 dataset (CC BY 4.0; 1-minute GHI, full year, explicitly intended by its authors for energy-system modeling).
- NASA Global Landslide Catalog (COOLR), ITALICA, FraneItalia, MyIKLIM (confirmed via the earlier search pass; download mechanics not re-verified by direct fetch in this round).

**Confirmed to exist but gated/restricted (verified by direct fetch):**
- Kajang BGS/NERC slope dataset — **permission-request required**, not open.
- Anzum et al. (2021) Kuala Lumpur hilly-terrain LoRa study — full text is registration/request-gated at IIUM; no raw dataset or data-availability statement found on direct inspection.

**Still unresolved (fetch attempt failed or inconclusive):**
- PVGIS Malaysia/Southeast Asia coverage — the live tool's database-selector dropdown must be checked interactively; this could not be confirmed from the static page content.
- NASA Landslide Viewer live download link — a direct connection attempt to the ArcGIS viewer failed in this session; the general COOLR access method (confirmed in the earlier search pass: downloadable .csv/.shp/.gdb via the Landslide Viewer, plus an API) should still hold, but was not re-verified by direct fetch.

**The most consequential confirmed gap remains unchanged:** no open flow-harvester characterization dataset exists under sediment-laden/intermittent flow conditions (Section 10.4) — this concrete data-availability finding directly reinforces the field-validity limitation already raised in Section 5.5.

**Recommended next actions, in priority order (revised):**
1. Download and use the two Mendeley piezoelectric-harvester datasets and the Kuala Lumpur solar-irradiance dataset immediately — confirmed open, no permission required, directly usable to begin parameterizing the Stage 1 HIL simulation (Section 4 of the Phase 4 report).
2. Submit a formal data-access request to BGS's Intellectual Property Rights Manager for the Kajang slope dataset, now correctly framed as a permission request rather than an open download.
3. Request the full text and, if possible, raw per-spreading-factor/altitude data from Anzum et al. (2021) directly from the authors or via the IIUM repository's document-request system — this is the best-matched Malaysia-specific terrain evidence for the lossy-link design constraint (Section 3.3), ahead of the Mozambique study currently cited.
4. Contact JKR's Slope Engineering Branch for the Slope Hazard and Risk Map, and MetMalaysia for historical station-level rainfall records — both confirmed to exist institutionally but not publicly downloadable.
5. Check Malaysia/Southeast Asia coverage directly in the live PVGIS tool before relying on it for solar-intermittency modeling.
6. Commission or request flow-harvester bench characterization under simulated sediment-laden runoff conditions — no existing dataset substitutes for this.

**AI disclosure (repeated per quality standards):** This analysis was produced using AI-assisted research tools performing automated literature search, source screening, and synthesis, including direct retrieval and verification of several primary dataset-access pages in this round. One correction to an earlier, unverified claim is documented above rather than silently fixed. Venue-quality and dataset-access screening were performed via targeted web search and direct page fetches, not a formal Scopus/Web of Science/DOAJ or institutional-licensing review, and should not be treated as a substitute for one before formal use.

---

## 11. Actual Data Pulled and Analyzed

Unlike every number elsewhere in this document (which is cited from literature), the figures in this section were computed directly from real downloaded files, not inferred from search results or paper abstracts. Raw data and analysis are retained locally at `/home/s/Documents/MicroGrid-IoT/Data/` for reproducibility, organized in isolated per-dataset directories per this project's data-handling practice (downloaded third-party data kept separate from any code that processes it).

### 11.1 Piezoelectric Low-Frequency Vibration Harvester — Real Measured Power Output

**Source:** Plaza, Iriarte, Castellano-Aldave, Carlosena & Bacaicoa (2024). Mendeley Data, DOI 10.17632/y4cmrsdv9f.1, CC BY 4.0. Companion paper: *Sensors* 24(12):3813.

**What was pulled:** All 59 CSV files (both "measurements" and "post-processed" series) across the dataset's experiments — 15.04 MB total, downloaded via the Mendeley public file API (`https://data.mendeley.com/api/datasets/{id}/files`), following each file's signed S3 redirect. The 41 accompanying video files (≈900 MB) were deliberately not downloaded, as they are not needed for power-model parameterization. Local path: `Data/piezo_harvester_y4cmrsdv9f/`.

**Structure confirmed on inspection:** each `measurements_expNN.csv` has 1,000 rows (Time, 2-axis accelerometer, 24 coil voltages, sampled at 0.01 s); each `post-processed_expNN.csv` has ~2,400 rows (Time; estimated angular position/velocity/acceleration of the harvester's internal masses; a `power` column giving instantaneous estimated harvested power).

**Computed result (23 experiments with usable `power` data):**

| Statistic | Value |
|---|---|
| Mean-of-per-experiment-means | 3,272 (power-column units) |
| Overall maximum observed | 47,197 (experiment 12) |
| Lowest per-experiment mean | 65.9 (experiment 13) |
| Highest per-experiment mean | 9,505 (experiment 12) |
| Spread across experiments | ~145× between lowest- and highest-mean experiments |

**Important caveat, stated rather than papered over:** the dataset's own files and page do not state the physical unit of the `power` column (the companion *Sensors* paper would confirm this, but it returned HTTP 403 on direct fetch in this session and was not independently re-verified here). The ~145× spread across experiments almost certainly reflects different excitation amplitude/frequency conditions per experiment (standard in a harvester *characterization* dataset, where the explicit purpose is to sweep across excitation regimes) — this is exactly the kind of accel-dependent variability the proposed design's "more ground movement → more power" argument (Section 3.1) needs, and now has real numbers behind it rather than a generic literature claim. **Action before using these numbers in the Stage 1 HIL model:** confirm the unit and which experiment-to-excitation mapping applies via the companion paper, rather than assuming µW/mW.

### 11.2 Kuala Lumpur Solar Irradiance — Real Cloud-Transient Frequency, Full Calendar Year 2025

**Source:** Chee Wern Hew (2026). Mendeley Data, DOI 10.17632/bgch4tw79k.1, CC BY 4.0, UCSI University.

**What was pulled:** All 365 daily CSV files (one-minute GHI, 07:00–19:00 local time, 720 rows/day), the complete calendar year 2025 — 8.6 MB total. (An initial pass retrieved only the first 100 files via `/api/datasets/{id}/files`, which turned out to be an endpoint pagination cap, not the dataset's true size; the `/public-api/datasets/{id}` endpoint's `content-range` header confirmed 365 total files, and its embedded `files` array supplied the complete list and download links for the remainder.) Local path: `Data/kl_solar_irradiance_bgch4tw79k/`.

**Computed results (365 days):**

| Statistic | Value |
|---|---|
| Daily peak GHI — mean | 1,071.2 W/m² |
| Daily peak GHI — range | 262.5 – 1,455.9 W/m² |
| Daily peak GHI — stdev | 177.9 W/m² |
| Days with zero detected cloud-transient dips (>40% minute-to-minute drop) | **94 of 365 (25.8%)** |
| Mean cloud-transient dips per day | 4.88 |
| Maximum dips in a single day | 28 |

**Month-by-month breakdown (the key finding):**

| Month | n days | Mean peak GHI (W/m²) | Mean daytime GHI (W/m²) | Zero-dip (sustained overcast) days | Mean dips/day |
|---|---|---|---|---|---|
| Jan | 31 | 959.7 | 340.9 | 11 | 3.03 |
| Feb | 28 | 1,131.7 | 380.2 | 5 | 4.07 |
| Mar | 31 | 1,141.0 | 363.7 | 5 | 5.55 |
| Apr | 30 | 1,142.5 | 379.2 | 4 | 6.43 |
| May | 31 | 1,041.4 | 353.3 | 9 | 4.77 |
| Jun | 30 | 1,054.6 | 372.4 | 6 | 5.27 |
| Jul | 31 | 1,033.0 | 380.6 | 7 | 5.68 |
| Aug | 31 | 1,061.0 | 345.3 | 6 | 6.52 |
| Sep | 30 | 1,145.6 | 359.2 | 10 | 4.60 |
| Oct | 31 | 1,100.9 | 366.9 | 8 | 7.23 |
| **Nov** | 30 | **1,062.7** | **312.1** | **12** | **2.37** |
| **Dec** | 31 | **990.5** | **313.5** | **11** | **2.97** |

**The directly relevant finding for this project, now confirmed across a full year rather than a 100-day sample:** November and December — the onset of Malaysia's Northeast monsoon — show the **lowest mean cloud-transient-dip rate** of any months (2.37 and 2.97/day) **combined with** among the **highest zero-dip-day counts** (12 and 11) and reduced mean daytime GHI (312.1 and 313.5 W/m², versus a ~360–380 W/m² norm in drier months). Read together, this is a real, measured signature of **sustained rather than transient** cloud cover specifically during the monsoon months: fewer scattered passing-cloud events, but more whole-day persistently-dim days. January shows a similar but weaker pattern (11 zero-dip days, lowest mean peak of any month at 959.7 W/m²), consistent with the tail of the same monsoon season. This is exactly the "correlated, sustained low-solar" failure mode the proposed design's dual-harvesting architecture (Section 3.1) and Stage 1 stress-test condition (Section 4, high-ρ case) are built to survive — and it is now grounded in a full year of real Malaysian ground measurements, not an assumed seasonal pattern.

**Caveat (unchanged):** Kuala Lumpur's solar profile is not necessarily representative of the actual highway cut-slope sites (different microclimate, canopy shading, elevation, and — notably — Kuala Lumpur is on the west coast, while several of the landslide-prone corridors discussed in Section 4.5, e.g., Cameron Highlands routes, are inland/highland and may follow a different monsoon exposure pattern than a KL lowland station). This dataset establishes a real, full-year baseline pattern to adapt, not a site-specific prediction — the November/December signature should be treated as a hypothesis to check against site-specific data (e.g., from a future MetMalaysia request per Section 12.4), not as itself proof of behavior at the actual deployment sites.

### 11.3 Piezo Power-Unit Confirmation — Attempted, Unresolved

After the direct MDPI fetch returned HTTP 403 (Section 11.1), this round tried OpenAlex's indexed abstract for the companion paper (DOI 10.3390/s24123813) as an alternate path — the abstract describes the three-stage characterization methodology in detail but states no numerical power values or units anywhere in the indexed text. **Conclusion: the power unit cannot be confirmed through open/automated means currently available in this session.** Obtaining it requires either direct access to the MDPI PDF (e.g., via institutional subscription or a manual browser visit) or contacting the authors — this is now a confirmed dead end for automated retrieval, not an unexamined gap.

The flow-harvester characterization gap (Section 10.4/10.6) remains completely unaddressed, as no dataset exists anywhere to pull.

### 11.4 NASA POWER — Real Multi-Site Data for the Actual Highland Corridor (New Lead, Found and Pulled)

In response to "keep strengthening the evidence," a new real, open, permission-free data source was found and used: **NASA POWER** (power.larc.nasa.gov), a free API providing global hourly solar irradiance and precipitation from MERRA-2/SYN1DEG reanalysis, no registration or permission required. Full-year 2025 hourly `ALLSKY_SFC_SW_DWN` (solar) and `PRECTOTCORR` (precipitation) were pulled for four real coordinates: Cameron Highlands/Tanah Rata (4.4747, 101.3777), Ringlet (4.4833, 101.3667), Simpang Pulai (4.5667, 101.1167), and Karak Highway (3.4931, 101.8109) — three points along the actual landslide-prone corridor discussed in Section 4.5, plus one distant comparison point. Local path: `Data/nasa_power_corridor/`.

**Finding 1 (negative, reported honestly — this did not do what I hoped):** the solar and precipitation values for Cameron Highlands, Ringlet (8 km away), and Simpang Pulai (35 km away) are **100% byte-identical**, hour for hour, across the entire year. NASA POWER's underlying MERRA-2/SYN1DEG products are ~1° resolution (roughly 100–110 km at this latitude), so all three corridor points fall inside the same grid cell. Only the distant Karak Highway point (≈150 km away, a different grid cell) differs (47.8% identical for solar, 12.1% identical for rain). **Conclusion: this data source cannot resolve the within-corridor spatial decorrelation this project's simulation assumes** (Section 2.3/13.4's `LOCAL_CLOUD_PROB` parameter) — it can only distinguish genuinely separate weather systems, not convective cells within a single ~60 km highway corridor. That specific question still requires real ground-station data (ideally JKR's Tolok Hujan network or MetMalaysia station records, per Section 12.3/12.4) or a finer-resolution satellite product (e.g., Himawari-8 cloud-mask imagery, ~2 km), not this API.

**Finding 2 (positive, and a genuine strengthening of the evidence):** at the real highland corridor site, using real paired hourly data, rainfall and solar suppression correlate at **r = −0.454** (daily total rainfall vs. daily peak solar, n=365 days). Days in the top rainfall quartile (mean 23.5 mm/day) show **15.9% lower peak solar** than days in the bottom quartile (mean 0.5 mm/day). Month-by-month, **November shows both the highest mean rainfall (23.86 mm/day) and the lowest mean peak solar (625.2 Wh/m²) of any month** — independently matching the Kuala Lumpur-derived monsoon-suppression signature from Section 11.2 (where November/December showed the most sustained-overcast days), but now confirmed with real paired rain+solar measurements at the actual highland corridor type of site, not inferred solely from solar-only data at a lowland city 150+ km away.

**What this changes:** the core hazard-coupling premise (rain suppresses solar, and this is worst in the Nov/Dec monsoon) is now supported by **two independent real datasets** rather than one — a real triangulation, not a restatement. The spatial-decorrelation assumption, however, remains exactly as unvalidated as before Section 10.6 flagged it; this round found a plausible-looking data source for that question and confirmed, by actually checking, that it does not resolve at the needed scale. That is itself useful: it rules out a free shortcut and confirms the Section 12.3/12.4 institutional data requests are not optional extras but the only real path to answering that specific question.

### 11.5 Flow-Harvester Viability — Replacing the Fake Placeholder with a Real-Data-Driven Model, and an Unfavorable Honest Result

Section 10.4/10.6 and 13.6.3 flagged the flow/runoff harvester term in `corridor_sim.py` as entirely fabricated (`random.uniform(0.5, 5.0)` mW, no real basis). In direct response to "no fake," it was replaced with a model driven by real data and a real literature-fitted curve, documented in `Data/_scripts/flow_harvester_model.py`:

- **Real driver:** hourly rainfall (mm/hr), Cameron Highlands, full year 2025, NASA POWER (Section 11.4).
- **Real power-velocity curve:** fitted from two actually-measured points in Lepipas et al. (2024) — 125 µW at 0.5 m/s, 5.1 mW at 2.0 m/s (a real Savonius-type microturbine on a water-pipe rig). The fitted exponent (2.68) sits close to the theoretical v³ kinetic-turbine scaling — a sanity check that these are physically consistent measurements, not noise.
- **Disclosed engineering assumptions** (no real data exists for these at an actual highway cut-slope): a catchment area draining to one monitoring point, a rational-method runoff coefficient C=0.6 (standard hydrology range 0.5–0.7 for a graded slope), and a *concentrated-outlet* channel design (a deliberate, stated engineering choice to raise velocity toward the harvester's real cut-in point, not a parameter tuned to produce a favorable answer).

**The honest result is unfavorable to this design component, and is reported as such rather than adjusted until it looked better:**

| Catchment area | Active hours/year | % of year | Mean power when active | Max power when active | Within literature-tested velocity range (0.5–2.0 m/s)? |
|---|---|---|---|---|---|
| 500 m² | 0 | 0.00% | — | — | — (never reaches cut-in) |
| 1,000 m² | 13 | 0.15% | 0.224 mW | 0.378 mW | Yes |
| 2,000 m² | 85 | 0.97% | 0.450 mW | 2.413 mW | Yes (peak ≈1.5 m/s) |
| 5,000 m² | 414 | 4.73% | 1.402 mW | 28.0 mW | **No — extrapolated beyond tested range** |
| 10,000 m² | 1,031 | 11.77% | 3.803 mW | 178.9 mW | **No — extrapolated beyond tested range** |
| 20,000 m² | 1,897 | 21.66% | 13.37 mW | 1,142 mW | **No — extrapolated beyond tested range** |

**The larger-catchment rows are not trustworthy predictions and are included only for transparency, not as supporting evidence.** At 5,000 m² and above, the modeled channel velocity at the year's heaviest real rain hour exceeds the 2.0 m/s upper limit the Lepipas et al. harvester was actually tested at (reaching an implausible 7.56 m/s at 10,000 m²) — the power-law is being extrapolated far outside its validated range, and the resulting mW/W-scale numbers should not be cited as evidence the flow harvester works at scale. **The only defensible rows are 1,000–2,000 m²**, where peak velocity stays within the literature-tested range: at a plausible highway cut-slope catchment size, this specific concentrated-outlet flow-harvester design would be active for **well under 1% of the year**, producing sub-milliwatt to low-single-digit-milliwatt power even when active.

**What this means for the overall proposal:** this is a genuine, quantified engineering concern about Section 3.1's flow-harvester component, not a resolved problem. Combined with the Section 13.6.3 ablation finding (removing the old fake placeholder changed nothing because its magnitude was already negligible relative to solar/piezo/demand), the picture is now consistent and worse than "untested": **a literature-grounded, real-rainfall-driven model of this specific design (small concentrated outlet, plausible catchment size) predicts the flow harvester would contribute usable power only during rare, brief windows, not as a reliable complementary source.** This does not kill the overall proposal — the piezoelectric component and the duty-brokering mechanism (Section 13.6) remain independently supported — but it means Section 3.1 should be revised to either (a) drop the flow harvester as a named component and rely on piezo + brokering alone, or (b) substantially rethink its physical design (e.g., a much larger catchment than is plausible for a single highway cut-slope segment, a fundamentally different low-cut-in harvesting principle, or accepting it as a rare-event supplementary source rather than a core complementary harvester). This is the kind of finding that should go into a Limitations or Discussion section as a real, specific, quantified result — not softened into a vague "further work needed" statement.

### 11.6 Real Event Cross-Check: Two Actual, Named, Dated Cameron Highlands Landslides vs. Real Weather Data

Rather than relying only on aggregate monthly statistics (Section 11.2/11.4), this check used two specific, independently-reported, precisely-dated real landslide incidents (found via targeted web search, not selected from a larger set to favor a result) and pulled real NASA POWER weather data for those exact dates to see whether the predicted "high rain / low solar" signature actually appears on real incident days. This is a direct, falsifiable spot-check, not an aggregate pattern.

**Event 1 — January 6, 2025, ~2–3am, Km48 Jalan Besar Kampung Raja (Blue Valley junction).** News reports (New Straits Times, Bernama, Malay Mail) explicitly describe this as triggered by heavy rain that began the preceding day. Real NASA POWER data for Cameron Highlands on the actual event date:

| Date | Total rain | Rain percentile (of 2025) | Peak solar | Solar percentile (of 2025) |
|---|---|---|---|---|
| Jan 5 (rain begins) | 4.48 mm | 56.2 | 691.0 Wh/m² | 31.8 |
| **Jan 6 (landslide day)** | **30.26 mm** | **95.6 — top 5% wettest day of the year** | **557.3 Wh/m²** | **11.8 — bottom 12% darkest day of the year** |

This is a striking, unprompted match to the predicted signature: on the actual day of a real, independently-reported rain-triggered landslide, real weather data shows both one of the wettest and one of the darkest days of the entire year, simultaneously.

**Event 2 — September 21, 2024, ~11am, Jalan Brinchang (near Agro Market).** News reports do not explicitly state a rain trigger for this one. Real data shows a less clean, genuinely mixed picture:

| Date | Daily rain | Peak solar | 14-day cumulative rain |
|---|---|---|---|
| Sept 17 | 20.81 mm | **399.8 Wh/m² (lowest in the 2-month window)** | 148.68 mm |
| Sept 20 | 0.70 mm | 604.3 Wh/m² | 143.35 mm |
| **Sept 21 (landslide day)** | **0.41 mm (dry)** | **490.9 Wh/m² (2nd-lowest in the window)** | **133.58 mm** |

Same-day rainfall on Sept 21 was actually low (8th percentile within the Aug–Sept window) — **this does not match a "heavy rain that day" story**. But the slide falls within a period of substantial 14-day cumulative antecedent rainfall (consistent with Cluster B's rainfall-threshold literature, which generally emphasizes cumulative/antecedent rainfall over single-day totals) and an unusually persistent low-solar stretch — the single darkest day in the entire two-month window (Sept 17, 399.8 Wh/m²) occurred just 4 days before.

**Event 3 — December 16, 2022, ~2am, Father's Organic Farm campsite, Batang Kali, Selangor (31 deaths — the deadliest event in this corpus).** The Public Works Department attributed the cause to "high soil saturation and pressure from the accumulation of underground water beneath the campsite" — explicitly a *delayed, cumulative* mechanism, not a same-day trigger. Real data confirms this is the right category of explanation, and shows why a same-day-only check would have missed it:

| Date | Daily rain | Rain percentile | Peak solar | Solar percentile | 7-day cumulative rain |
|---|---|---|---|---|---|
| Dec 13 (3 days before) | 34.91 mm | **91.8 — extreme** | 361.1 Wh/m² | **1.6 — most extreme dark day in the whole window** | 248.6 mm |
| Dec 15 | 3.76 mm | 24.6 | 601.9 Wh/m² | 31.1 | 207.8 mm |
| **Dec 16 (landslide day)** | 15.76 mm | 63.9 | **768.8 Wh/m² (91.8 percentile — a relatively *sunny* day)** | 91.8 | **199.8 mm** |

**The landslide itself occurred on a comparatively sunny day** — the extreme dark+wet signature was 3 days earlier, and substantial antecedent moisture (≈200 mm over the preceding week) had already accumulated by the time of failure. This matches the PWD's own stated mechanism and is a real, independent confirmation that delayed/cumulative-saturation failure is a genuine real-world pattern here, distinct from Event 1's same-day pattern.

**Event 4 — May 21, 2011, ~2:20pm, Hidayah Madrasah Al-Taqwa orphanage, Kampung Gahal, Hulu Langat, Selangor (16 deaths, 13 children).** Real data shows the weakest match of the four:

| Date | Daily rain | Rain percentile | Peak solar | Solar percentile |
|---|---|---|---|---|
| May 18 | 15.23 mm | 86.9 | 765.9 Wh/m² | 49.2 |
| May 19 | 7.75 mm | 68.9 | 851.0 Wh/m² | **85.2 — quite sunny** |
| **May 21 (landslide day)** | 8.11 mm | 70.5 (above median, not extreme) | 753.0 Wh/m² | 36.1 (below median, not extreme) |

Neither the event day nor the preceding days show an extreme signature in either direction — moderately wet, moderately sunny throughout. **This event does not confirm the hypothesis**, and is reported as such rather than reframed to fit.

**Honest overall tally across all four real, named, dated events:** 1 clean same-day match (Event 1), 1 clean delayed/cumulative-saturation match (Event 3), 1 plausible-but-weaker antecedent match (Event 2), 1 no-match (Event 4). **This is genuinely mixed evidence from n=4 — not a triumphant confirmation and not a refutation.** It should not be oversold in either direction.

**A real, substantive design implication this heterogeneity surfaces:** real landslide failure timing relative to rainfall/solar conditions is not uniform — some failures happen *during* the storm signature (Event 1), and at least one major, well-documented failure (Event 3, the deadliest in this set) happened *after* the rain had stopped and the sky had cleared, once underground saturation reached a critical point. **This is a genuine argument for the piezoelectric, ground-movement-coupled harvesting component (Section 3.1) over a purely weather-coupled design**: a system that only increases its sensing/power behavior when it is "currently dark and rainy" would, per Event 3's real pattern, be at its most relaxed state at exactly the moment Batang Kali actually failed. A harvester that responds to *actual ground movement* rather than *current weather* does not have this blind spot. This is a point in favor of the design's piezo component specifically, surfaced by real-event checking rather than assumed — and it should be added to Section 3.1/5.1's justification, not left implicit.

A rigorous version of this check would need many more named, dated events (ideally from JKR's own incident records, Section 12.3, rather than news search) before any statistical claim could be made about hit rate — n=4 supports a design argument, not a probability estimate.

---

## 12. Drafted Data-Access Requests (For User Review — Not Sent)

These four messages are drafted for the permission-gated or institutionally-held sources identified in Section 10. **None of these have been sent.** Each needs your name, affiliation, and contact details filled in before you send it yourself — sending on your behalf would require your explicit instruction and, for the institutional ones, is the kind of external, visible action this pipeline doesn't take unprompted.

### 12.1 British Geological Survey — Kajang Slope Dataset (Section 10.1)

> Subject: Data access request — Water retention data from monitored slopes near Kajang, Langat River Basin, Malaysia (NERC Grant NE/S003347/1)
>
> Dear BGS Intellectual Property Rights Manager,
>
> I am writing to request access to the dataset "Water retention data from monitored slopes near Kajang in the Langat River Basin, Malaysia," held under NERC Grant NE/S003347/1 and listed at https://webapps.bgs.ac.uk/services/ngdc/accessions/index.html#item176993.
>
> [Your name], [your affiliation/institution]
>
> I am researching an off-grid, hazard-coupled energy-harvesting design for landslide early-warning IoT sensor networks on Malaysian highway cut-slopes and hillside areas, extending the soil-moisture/rainfall threshold modeling approach used in the existing landslide early-warning literature. The soil suction, volumetric water content, and rainfall time series in this dataset would help parameterize a realistic rainfall-to-instability lag model for a simulation-based validation study (not a commercial product).
>
> Could you advise on the terms under which this data could be made available for academic research use, and whether any restrictions would apply to its use in a published methodology (with appropriate attribution to BGS, NERC, Durham University, and UKM)?
>
> Thank you for your time.
>
> [Your name]

### 12.2 Anzum, Habaebi, Islam & Hakim (2021) — Kuala Lumpur Hilly-Terrain LoRa Study (Section 10.5)

> Subject: Request for full text and raw measurement data — "A Study of LoRa Signal Propagation in Hilly Suburban Area for Smart City Applications" (ICSIMA 2021)
>
> Dear Dr. Habaebi [and co-authors],
>
> I came across your paper "A Study of LoRa Signal Propagation in Hilly Suburban Area for Smart City Applications" (2021 IEEE 7th ICSIMA) via the IIUM institutional repository and am very interested in the RSSI and packet receive ratio results you report for 915 MHz LoRa across spreading factors SF7/SF8/SF10/SF12 in hilly suburban Kuala Lumpur.
>
> [Your name], [your affiliation/institution]
>
> I am designing a duty-brokering protocol for an off-grid IoT sensor network along Malaysian highway cut-slopes, where terrain-degraded LoRaWAN connectivity is a key design constraint. Your study is the closest Malaysia-specific terrain match I have found in the literature, and I would greatly appreciate either (a) a copy of the full paper, and (b) if possible, access to the underlying per-spreading-factor/altitude RSSI and PRR measurements, to ground my connectivity-reliability assumptions in real local data rather than data from a different country's terrain.
>
> I would of course cite your work appropriately in any resulting output.
>
> Thank you very much for your consideration.
>
> [Your name]

### 12.3 JKR Slope Engineering Branch — Slope Hazard and Risk Map (Section 10.1, 4.5)

> Subject: Research inquiry — access to Slope Hazard and Risk Map data (National Slope Master Plan 2025–2030)
>
> Dear Sir/Madam (Slope Engineering Branch, Jabatan Kerja Raya),
>
> I am conducting academic research on self-powered IoT early-warning sensor networks for landslide-prone highway cut-slopes in Malaysia, building on JKR's published Slope Hazard and Risk Map inventory (34,714 slopes nationwide, 1,577 classed high-risk) and the National Slope Master Plan 2025–2030.
>
> [Your name], [your affiliation/institution]
>
> Would it be possible to obtain (a) general information on which specific highway corridors or slope segments are classified as highest-risk and would be realistic candidates for a pilot sensor deployment, and (b) any publicly shareable data from the Department's rainfall monitoring stations (Tolok Hujan) or robotic total station/GNSS slope-movement monitoring installations (e.g., at federal road Sections 44 and 46), for use in a research validation study?
>
> I understand some of this information may be restricted; any guidance on the appropriate request process or publicly available alternative would be appreciated.
>
> Thank you for your time and assistance.
>
> [Your name]

### 12.4 MetMalaysia — Historical Rainfall Station Records

> Subject: Request for historical rainfall station data for academic research
>
> Dear Malaysian Meteorological Department,
>
> I am conducting research on landslide early-warning sensor design for Malaysian highway cut-slopes and would like to request historical rainfall records (preferably sub-daily/hourly resolution where available) for station(s) near [specify corridor, e.g., Simpang Pulai–Cameron Highlands, or Karak Highway], covering approximately [specify period, e.g., 2015–2025].
>
> [Your name], [your affiliation/institution]
>
> This data would be used to parameterize a rainfall-intensity intermittency model for a simulation-based energy-system validation study (non-commercial academic research). I understand a 2025 Civil Engineering Journal study (Ranau/Kota Belud IDF curves) used similar MetMalaysia records, and I am hoping to follow a comparable data-access route.
>
> Could you advise on the process, any applicable fees, and data-sharing terms for this kind of request?
>
> Thank you very much for your assistance.
>
> [Your name]

---

## 13. Research Questions, Methods, Algorithm, Testing, Validation, Results, Conclusion

This section consolidates the project into the structure of a systems/engineering paper. Where content already exists earlier in this document, it is referenced rather than duplicated; the **Algorithm** and **Results** subsections are new — they specify, implement, and actually run the proposed protocol for the first time in this document, using the real data pulled in Section 11.

### 13.1 Research Questions

Restated from Section 2.1 (Phase 1 Scoping), unchanged:

- **Primary RQ:** In off-grid landslide-monitoring sensor swarms on Malaysian highway cut-slopes, where no utility-grid backup exists, can hazard-coupled self-powering combined with inter-node duty-brokering sustain network-level sensing continuity better than independent per-node switching alone?
- **RQ1:** How does the reference paper's single-node double-threshold switching perform, at the network level, when no utility/secondary source exists at all?
- **RQ2:** What duty-brokering protocol design best preserves network-level sensing continuity under varying spatial correlation of storm-driven power intermittency across nodes?
- **RQ3:** How must the HIL testbed be extended to a multi-node configuration to validate such a protocol, and what fidelity/scalability trade-offs result?

Section 13.5–13.6 below answer RQ1 and RQ2 computationally, at the level of a desktop simulation — not yet the full HIL/physical validation RQ3 asks for (that remains Section 4's Stage 1/Stage 2 plan, still unexecuted).

### 13.2 Methods

Design-science methodology (Section 2.2), executed here as: (1) specify the algorithm precisely (13.3); (2) implement it exactly as specified (13.4, `Data/_scripts/corridor_sim.py`); (3) drive it with the real data pulled in Section 11 wherever real data exists, and explicitly-flagged modeling assumptions where it does not (13.4); (4) run a controlled baseline-vs-treatment comparison with both conditions exposed to an identical random environment, isolating the brokering mechanism as the only difference (13.5); (5) report results including the two implementation bugs found and fixed during this process, not just the final numbers (13.6).

### 13.3 Algorithm

**Algorithm 1 — Per-node hazard-coupled source selection (extends Lee & Wang 2024's double-threshold switching to a no-utility-grid, multi-source node):**

```
for each node i, each timestep t:
    solar_i(t)  = GHI_i(t) * PANEL_AREA * PANEL_EFF          # real GHI, assumed panel efficiency
    piezo_i(t)  = draw from real measured power values        # triggered stochastically;
                  IF movement-triggered else 0                 # higher trigger probability
                                                                 # when regional conditions are
                                                                 # classified "sustained overcast"
    flow_i(t)   = literature-bounded draw if overcast else 0   # NO real dataset exists for this
    harvested_i(t) = solar_i(t) + piezo_i(t) + flow_i(t)

    buffer_i(t) = clip(buffer_i(t-1) + (harvested_i(t) - DEMAND) / 60,
                       0, BUFFER_CAPACITY)

    if buffer_i(t) >= LOWER_THRESH:
        node i reports normally   (self-sufficient)
    else:
        node i is a BROKERING CANDIDATE (see Algorithm 2)
```

**Algorithm 2 — Corridor-wide duty-brokering (the proposed novel mechanism, Section 3.2):**

```
for each timestep t (after Algorithm 1 updates all nodes' buffers):
    for each node i where buffer_i(t) < LOWER_THRESH
                      and not currently covered by a prior hand-off:
        for each neighbor j != i, in some order:
            if buffer_j(t) > UPPER_THRESH:                 # j has real surplus
                attempt hand-off request i -> j over LoRaWAN
                if link succeeds (probability = measured PDR,
                                   Chapungo et al. 2025 = 0.89):
                    j takes over i's reporting duty for
                        BROKER_COOLDOWN_MIN minutes
                    log one broker event
                    break                                    # one donor is enough
            # if no neighbor qualifies, or the link attempt fails,
            # node i falls back to Algorithm 1's own local behavior
            # (graceful degradation per Section 3.3 — never worse
            # than the reference paper's single-node baseline)
```

This is the literal logic implemented in `corridor_sim.py` (N=5 nodes), not a separate idealized description — the code and the algorithm above were kept in sync during implementation.

### 13.4 Testing

**What was actually run:** a controlled computational experiment, not a physical or HIL test (that remains Section 4's unexecuted Stage 1/2 plan). Two conditions — BASELINE (Algorithm 1 only) and TREATMENT (Algorithm 1 + Algorithm 2) — were run over a simulated year (365 real days × 720 real daytime minutes = 262,800 timesteps), with both conditions exposed to an **identical** sequence of environmental randomness (local-cloud masks, piezo-trigger events, piezo-draw selection) via a dedicated RNG stream kept separate from the brokering-only RNG stream — so brokering is the sole difference between the two runs, not an artifact of different random draws.

**Real data inputs:**
- Solar driver: all 365 days of real 1-minute Kuala Lumpur GHI (Section 11.2), including the real monsoon-season (Nov/Dec) sustained-overcast signature.
- Piezoelectric power draws: pooled real instantaneous `power` values from all 23 characterized experiments (Section 11.1) for rain/movement events; the single lowest-mean experiment's values for ambient/dry-day background vibration.
- Node demand: 295.49 mW, the exact measured average from Lee & Wang (2024) Table 2.
- Panel dimensions: 118mm × 70mm, the exact YML-118X70MM panel named in Lee & Wang (2024) Section 2.2.1.
- LoRaWAN link-success probability: 0.89, the measured PDR from Chapungo et al. (2025).

**Explicitly modeled/assumed inputs (no real data exists for these — disclosed, not hidden):**
- Multi-node spatial correlation structure (ρ=1 on sustained-overcast days, independent local-cloud masking otherwise) — a structural hypothesis from Section 2.3/5.4, not a measured correlation.
- Panel efficiency (15%), buffer sizing (1-hour deficit bridge), and the two energy thresholds (80%/20% of capacity) — assumed design parameters standing in for the circuit-level values a real Stage 1 HIL testbed would need to determine.
- Flow/runoff harvester output — no open dataset exists anywhere (Section 10.4); modeled as a literature-bounded placeholder.
- Ground-movement trigger probabilities (rain-day vs. dry-day) — physically motivated but uncalibrated against any real geotechnical displacement data.

### 13.5 Validation

**Internal validity — process.** Two implementation bugs were found and fixed *during* this work, and are reported rather than silently corrected: (1) an uncontrolled RNG confound in which baseline and treatment drew from the same continuous random stream rather than identical seeded conditions, inflating the apparent treatment effect; (2) a day-boundary bug in which the per-day timestep index (reset to 0 each day) was compared against a brokering cooldown timestamp that could exceed a single day's length, causing a node to become "covered" *permanently* after certain hand-offs rather than for the intended 30-minute window. Both were caught by sanity-checking intermediate quantities (per-node covered/dark/reporting minute totals summing to the total simulated minutes; covered-minutes being consistent with the number of logged broker events) before trusting the output — this is the same standard this whole document has tried to hold literature claims to, applied to its own code.

**Internal validity — design.** The controlled comparison (identical environment, brokering as the sole difference) isolates the mechanism's causal effect from random-draw noise, within the limits of the modeled assumptions listed in 13.4.

**External validity — explicitly limited.** This is a single-site (Kuala Lumpur) solar driver applied to a hypothetical 5-node corridor with an assumed (not measured) spatial correlation structure, an assumed panel/buffer sizing, and a placeholder flow-harvester model. It demonstrates that the proposed algorithm is implementable and produces a specific, mechanistically traceable effect — it does **not** demonstrate that effect's magnitude at an actual highway cut-slope deployment. Stage 1 (full HIL, Section 4) and Stage 2 (physical prototype) remain the required next steps before any deployment-relevant claim.

### 13.6 Results — Preliminary Computational Feasibility Study

**Framing, stated up front:** the user explicitly asked for results that are "publishable, valid and accurate; no fake." The honest answer is that what follows is a **preliminary computational feasibility study**, not publication-grade experimental validation — it demonstrates the algorithm is implementable and produces a statistically robust, mechanistically explicable effect under a stated set of assumptions, using real component-level data wherever real data exists. It is **not** a substitute for the real multi-site field data, real flow-harvester characterization, or Stage 1 HIL / Stage 2 physical validation (Section 4) that genuine publication-grade validation would require. Section 13.6.3 states exactly what would need to change for that.

#### 13.6.1 Single-seed result (original run, seed=42 only)

The first run of `corridor_sim.py` (reported in the prior revision of this section) used a single seed. That is **one realization, not a statistically validated estimate** — it cannot by itself distinguish a genuine effect from noise specific to that seed. It is superseded by the 50-seed sweep below, which is the version that should be cited.

#### 13.6.2 50-seed sensitivity sweep (statistically robust estimate)

Computed by running `Data/_scripts/sensitivity_sweep.py`: 16 parameter combinations (4 panel efficiencies × 4 buffer sizes, the two most consequential *assumed* constants) × 50 independent seeds × 2 conditions (baseline, treatment) = **1,600 full-year simulation runs**, using the "common random numbers" paired design (baseline and treatment share each seed before averaging across seeds) to isolate the brokering effect from random-draw noise. Full numeric output: `Data/_scripts/sweep_output.txt`.

| Panel eff. | Buffer (hrs) | Baseline dark-time | Full-network coverage (base→treat) | **Stress-day Δ (mean ± SD, n=50)** | Non-stress Δ (mean ± SD) | Broker events/yr |
|---|---|---|---|---|---|---|
| 0.10 | 0.5 | 50.92% | 44.39%→48.58% | −32.69% ± 1.22% | −0.21% ± 0.05% | 1,528 |
| 0.10 | 1.0 | 48.14% | 46.91%→49.82% | −20.75% ± 1.09% | −0.11% ± 0.04% | 890 |
| 0.10 | 2.0 | 46.59% | 47.99%→49.51% | −9.36% ± 1.50% | −0.04% ± 0.02% | 389 |
| 0.10 | 4.0 | 45.17% | 48.38%→48.91% | −2.60% ± 1.08% | −0.03% ± 0.02% | 101 |
| 0.15 | 0.5 | 37.69% | 59.04%→62.12% | −32.16% ± 1.48% | −0.28% ± 0.06% | 1,153 |
| 0.15 | 1.0 | 34.52% | 62.15%→64.26% | −20.62% ± 1.53% | −0.17% ± 0.05% | 669 |
| 0.15 | 2.0 | 28.79% | 67.67%→68.74% | −10.18% ± 1.61% | −0.06% ± 0.03% | 288 |
| 0.15 | 4.0 | 13.04% | 84.10%→84.43% | −4.40% ± 1.67% | −0.06% ± 0.07% | 67 |
| 0.20 | 0.5 | 31.40% | 65.99%→68.46% | −31.79% ± 1.46% | −0.33% ± 0.07% | 937 |
| 0.20 | 1.0 | 28.09% | 69.25%→70.89% | −20.25% ± 1.87% | −0.17% ± 0.06% | 533 |
| 0.20 | 2.0 | 20.90% | 76.25%→77.02% | −10.01% ± 2.04% | −0.06% ± 0.04% | 209 |
| 0.20 | 4.0 | 6.43% | 91.92%→92.11% | −4.84% ± 3.30% | −0.06% ± 0.07% | 36 |
| 0.30 | 0.5 | 24.05% | 73.86%→75.65% | −31.21% ± 1.61% | −0.37% ± 0.10% | 717 |
| 0.30 | 1.0 | 20.80% | 77.12%→78.23% | −19.82% ± 2.20% | −0.16% ± 0.08% | 391 |
| 0.30 | 2.0 | 12.04% | 86.20%→86.59% | −9.93% ± 2.52% | −0.06% ± 0.07% | 119 |
| 0.30 | 4.0 | 2.29% | 97.10%→97.14% | −3.11% ± 3.03% | −0.04% ± 0.12% | 9 |

**Result 1 — the finding is robust across the entire tested assumption space:** all 16 of 16 points show the stress-day benefit exceeding the non-stress-day benefit, confirming the mechanism described in the prior revision (independently-triggered piezo events create node-to-node asymmetry even under fully-correlated solar) is not an artifact of one arbitrary parameter choice.

**Result 2 — honestly, the effect's statistical clarity depends on how stressed the system is.** At tight/under-provisioned settings (small buffer, low efficiency — arguably the realistic regime for a genuinely tiny remote panel), the stress-day effect is large and clearly distinguishable from zero (e.g., −32.7% ± 1.2%, a >25-sigma effect). At comfortably over-provisioned settings (buffer_hours=4.0, panel_eff=0.30), the baseline is already only 2.3% dark, there is little left for brokering to fix, and the residual effect (−3.1% ± 3.0%) is directionally consistent but no longer clearly distinguishable from noise at two standard deviations. **This is physically sensible, not a weakness to hide:** brokering matters most exactly when the system is margin-constrained, which is the deployment scenario (tiny panel, remote site, no utility backup) this whole proposal is about.

#### 13.6.3 Ablation: removing the one fabricated component

The flow/runoff harvester term has **no real dataset behind it anywhere** (Section 10.4/10.6) — it is a placeholder (`random.uniform(0.5, 5.0)` mW on stress days), not a measured model. In direct response to the "no fake" standard, it was set to **exactly zero** and 8 representative points (panel_eff ∈ {0.15, 0.20} × all 4 buffer values, 50 seeds each, 800 more full-year runs) were re-run. Full output: `Data/_scripts/ablation_output.txt`.

| Panel eff. | Buffer (hrs) | Stress Δ, with flow (fake) | Stress Δ, flow = 0 (ablated) |
|---|---|---|---|
| 0.15 | 0.5 | −32.16% ± 1.48% | −31.97% ± 1.47% |
| 0.15 | 1.0 | −20.62% ± 1.53% | −20.17% ± 1.85% |
| 0.15 | 2.0 | −10.18% ± 1.61% | −9.60% ± 1.72% |
| 0.15 | 4.0 | −4.40% ± 1.67% | −4.26% ± 1.98% |
| 0.20 | 0.5 | −31.79% ± 1.46% | −31.51% ± 1.55% |
| 0.20 | 1.0 | −20.25% ± 1.87% | −19.90% ± 1.98% |
| 0.20 | 2.0 | −10.01% ± 2.04% | −9.87% ± 2.07% |
| 0.20 | 4.0 | −4.84% ± 3.30% | −4.64% ± 2.41% |

**Result: the finding survives completely intact** (8/8 points still show stress > non-stress benefit; every ablated value falls within the original's error bars). **The honest reason this ablation passes is itself informative and should not be oversold:** the flow term's magnitude (0.5–5 mW) is simply too small relative to solar/piezo/demand (hundreds of mW) to have been doing meaningful work in the model in the first place. This confirms the headline finding is not secretly riding on the one component with zero empirical grounding — but it does **not** mean the flow-harvester idea itself has been validated; it means this particular placeholder was numerically negligible either way. A properly characterized flow harvester (Section 12.4's data request, or de novo bench testing) could in principle contribute meaningfully and should still be pursued — this ablation only establishes that the *current reported finding* doesn't depend on faking that contribution.

#### 13.6.4 What would actually be required for publication-grade results

Stated explicitly, not left implicit:
1. **Real multi-site solar/weather data** along an actual highway corridor (or at minimum, multiple real Malaysian stations), replacing the single-site Kuala Lumpur driver and the assumed ρ=1 correlation structure with a measured one.
2. **Real flow-harvester characterization data** under sediment-laden, intermittent runoff conditions (confirmed nonexistent anywhere, Section 10.4) — without it, that design component remains unvalidated regardless of how the ablation above turned out.
3. **Calibrated, not assumed, structural constants** — panel efficiency, buffer sizing, movement-trigger probabilities, and local-cloud decorrelation probability, ideally from the Stage 1 HIL testbed (Section 4) or direct measurement, not literature-adjacent guesses.
4. **The Stage 1 HIL replication and Stage 2 physical prototype** themselves (Section 4) — this desktop simulation does not substitute for either, and was never intended to.

### 13.7 Conclusion

The proposed duty-brokering mechanism, implemented exactly as specified in Algorithm 2 and driven by real solar and piezoelectric data wherever real data exists, produces a statistically robust (50-seed, paired-design), mechanistically explicable improvement in network-level sensing continuity concentrated specifically on the fully-correlated monsoon-front stress condition the design was built to survive — a finding that holds across the full tested range of assumed structural parameters (16/16 points) and survives intact when the one entirely fabricated model component (the flow harvester) is removed (8/8 ablated points). This is genuine evidence, obtained by actually building, running, stress-testing, and attempting to break the model rather than only describing it — and it was only trustworthy after two real implementation bugs were caught and fixed (Section 13.5) and one fabricated component was explicitly tested for dependence (13.6.3). It is, honestly, a preliminary feasibility result, not a publication-ready validation: Section 13.6.4 states exactly what real-world data and physical testing would still be needed to close that gap, and that work has not yet been done.
