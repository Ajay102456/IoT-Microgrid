# Hazard-Coupled Self-Powering and Corridor-Wide Duty-Brokering for Off-Grid Landslide Early-Warning IoT Sensor Swarms: A Design and Simulation Study for Malaysian Highway Cut-Slopes

**[Author Name]¹***

¹ [Affiliation]

\* Correspondence: [email]

## Abstract

Microgrid-powered Internet of Things (IoT) sensing has been shown to sustain continuous monitoring by switching between renewable and utility-grid power sources, but this model assumes utility backup is always available — an assumption that fails for landslide-monitoring sensor swarms on remote, off-grid highway cut-slopes. This paper proposes extending the single-node IoT-microgrid model in two directions: (1) hazard-coupled self-powering, in which a piezoelectric harvester mechanically coupled to the monitored slope generates power that increases with ground micro-movement rather than the solar supply that decreases under the same monsoon conditions that drive instability; and (2) corridor-wide duty-brokering, in which spatially distributed nodes reassign sensing duties — not electrical energy — to neighbors with surplus harvested power, exploiting the localized nature of tropical convective storm cells along a highway corridor. A systematic review of 147 sources across nine technology clusters established that no existing system combines hazard-coupled powering with duty-level brokering for this application. The design was evaluated through a controlled, 50-seed Monte Carlo simulation driven by real solar irradiance data (Kuala Lumpur, full year 2025, 1-minute resolution) and real piezoelectric harvester characterization data (23 laboratory experiments); duty-brokering reduced sensing downtime during correlated monsoon-front conditions by up to 32.7% (large-effect settings) and the finding survived an ablation removing the one unvalidated model component. A real-data cross-check against rainfall and solar conditions at an actual highland corridor site, and against four independently documented Malaysian landslide incidents, found a genuinely mixed but informative pattern that motivated a revision of the original design: a planned flow/runoff harvester component was found, through a literature-grounded model driven by real rainfall data, to be viable for well under 1% of the year and is downgraded to a rare-event supplement rather than a core design element. The paper reports this result, and the broader evidentiary picture, as a preliminary computational feasibility study — not a validated field deployment — and specifies the hardware-in-the-loop and physical-prototype work still required before deployment.

**Keywords:** IoT microgrid; landslide early warning; energy harvesting; piezoelectric; duty cycling; hardware-in-the-loop; wireless sensor network; Malaysia

## 1. Introduction

Internet of Things (IoT) sensing has become central to natural-hazard monitoring, but IoT devices require continuous power, and continuous power is the scarcest resource in exactly the remote, off-grid locations where hazard sensing matters most. Lee and Wang [1] address this for grid-adjacent deployments with an "IoT microgrid" architecture: a single DC sensor node switches between a renewable primary source and a utility-grid secondary source using a double-voltage-threshold controller, validated on a hardware-in-the-loop (HIL) testbed. Their model rests on four assumptions, the second of which — that utility-grid power is available as backup — does not hold for landslide-monitoring sensors on remote highway cut-slopes, a deployment class with no utility access and frequently canopy-shaded or monsoon-obscured solar exposure.

Malaysia provides a concrete setting for this gap. The Public Works Department (Jabatan Kerja Raya, JKR) maintains a hazard-and-risk inventory of 34,714 slopes along federal roads nationwide, of which 1,577 are classed high-risk, under the National Slope Master Plan 2025–2030 [2]. Historical incidents — the 1993 Highland Towers collapse, the 2008 Bukit Antarabangsa landslide, and the 2022 Batang Kali campsite landslide (31 deaths) — demonstrate the consequence of slope failure, while recurring closures on routes such as Simpang Pulai–Cameron Highlands show the continuing operational burden. JKR already operates 49 rainfall telemetry stations and robotic total stations at selected federal-road sections [2], but no system identified in the literature review underlying this paper (Section 2) reports a self-powering or inter-node redundancy mechanism for the specific condition where solar power and ground instability change together — a monsoon-triggered correlation this paper treats as the central design problem.

This paper asks: can hazard-coupled self-powering, combined with corridor-wide duty-brokering, sustain network-level sensing continuity for an off-grid landslide early-warning swarm, where the reference architecture's utility-backup assumption cannot be satisfied? The paper does not answer this with field data — no hardware has been deployed — but establishes, through systematic literature review, real-data-grounded simulation, and direct cross-checking against real weather and incident records, that the proposed design is mechanistically sound, identifies which of its components are and are not currently well supported, and specifies the validation path required before deployment.

The remainder of this paper is organized as follows. Section 2 reviews related work across nine technology clusters. Section 3 presents the proposed system design and algorithm. Section 4 describes the simulation methodology and the real and modeled data used to drive it. Section 5 reports results, including a sensitivity sweep, an ablation study, and a cross-check against real weather and incident data. Section 6 discusses implications, limitations, and the revision this process produced to the original design. Section 7 concludes.

## 2. Related Work

A PRISMA-aligned search across Semantic Scholar, OpenAlex, and PubMed (via a Consensus aggregator) identified 200 candidate records across nine thematic queries; after deduplication, screening, and venue-quality verification (three sources downgraded on review quality — Section 6.4), 147 sources were retained across nine clusters.

**Landslide/slope IoT monitoring (31 sources)**, including deployments in Kerala [3,4], the Darjeeling Himalayas [5], Colombia [6], and two Malaysian systems [7,8], consistently rely on solar-plus-battery or grid power, with no reviewed system modeling continuity when neither is available.

**Rainfall-induced landslide threshold models (18 sources)** [9–13] establish that landslide risk escalates during sustained or intense rainfall — the same conditions under which solar generation is most degraded, a structural conflict this literature does not address at the power-architecture level.

**Piezoelectric and vibration-based self-powered sensing (15 sources)** is a mature, field-validated technology [14–17]. Two sources [18,19] already embed piezoelectric elements into slope geosynthetics for strain and microseismic *sensing* — but not for harvesting usable *power*.

**Flow/hydrokinetic energy harvesting for remote sensors (15 sources)** [20–23] reliably produces 0.1 mW to several hundred mW from low-velocity water flow in clean, controlled conditions (domestic pipes, laboratory flow rigs); none report performance under sediment-laden, intermittent field runoff.

**LoRaWAN/LPWAN for remote disaster monitoring (15 sources)** [24–27] provides the communication substrate a brokering protocol must run over; terrain-degraded connectivity is a reported constraint in both a rural African deployment [24] and a Malaysian hilly-suburban study [28].

**IoT microgrid and cyber-physical renewable energy management (18 sources)**, including the primary reference [1], establishes the baseline single-node architecture this paper extends.

**Energy-aware duty-cycling, clustering, and task-offloading WSN protocols (15 sources)** [29–33] provide the generic algorithmic basis adapted here for duty-brokering, but none address a spatially-correlated storm-cell topology.

**Peer-to-peer energy trading in microgrids (12 sources)** [34–37] establishes a negotiation-based precedent for a shared resource among autonomous nodes, here reinterpreted as a traded *duty* rather than a traded *kWh*.

**Hardware-in-the-loop testbed methodology (12 sources)** [1,38–41] provides the validation approach this paper's Section 6.5 identifies as the necessary next step beyond the simulation reported here.

No source in this corpus combines hazard-coupled harvesting (powering rather than only sensing from ground movement) with duty-level task brokering across a spatially-correlated storm topology — the gap this paper addresses.

## 3. Proposed System Design

### 3.1 Architecture

Building on the reference architecture's controller–energy-source–IoT-load structure [1], the proposed design makes two structural changes, revised once during this study in response to real-data testing (Section 6.1).

**Hazard-coupled harvesting.** Each node pairs a piezoelectric harvester mechanically coupled to the monitored slope segment with a baseline solar panel retained as a tertiary source. As originally proposed, a flow/runoff harvester was included as a second complementary source; Section 5.3 reports a real-data-driven finding that revises this component's role to a rare-event supplement rather than a core element, for reasons given there.

**Corridor-wide duty-brokering.** A node whose harvested-energy state drops below a threshold signals neighboring nodes, over the same LoRaWAN link already required for sensing, to temporarily assume its reporting duty. This adapts cluster-head rotation logic from energy-aware WSN clustering [29] with the negotiation structure of peer-to-peer energy-trading mechanisms [35], substituting "sensing/reporting duty" for "kWh" as the traded unit. Because tropical convective storms are frequently localized rather than basin-wide, nodes spaced tens of kilometers apart along a highway corridor are more likely to retain surplus capacity even when a nearer cluster is storm-affected.

### 3.2 Algorithm

**Algorithm 1 (per-node source selection)** extends the reference paper's double-threshold switching [1] to a no-utility-grid, multi-source node:

```
for each node i, each timestep t:
    solar_i(t)  = f(GHI_i(t), panel area, panel efficiency)
    piezo_i(t)  = stochastically-triggered draw from measured
                  harvester output, trigger probability elevated
                  under monsoon-correlated conditions
    harvested_i(t) = solar_i(t) + piezo_i(t)
    buffer_i(t) = clip(buffer_i(t-1) + (harvested_i(t) - demand)/60,
                       0, capacity)
    if buffer_i(t) >= lower_threshold:
        node i reports normally
    else:
        node i is a brokering candidate (Algorithm 2)
```

**Algorithm 2 (corridor-wide duty-brokering)**:

```
for each timestep t, after Algorithm 1 updates all buffers:
    for each node i with buffer_i(t) < lower_threshold
                      and not currently covered:
        for each neighbor j != i:
            if buffer_j(t) > upper_threshold:
                attempt hand-off request i -> j
                if link succeeds (probability = measured PDR):
                    j covers i's duty for a fixed cooldown window
                    break
        # on failure to find a donor, or a failed link attempt,
        # node i falls back to Algorithm 1's own local behavior,
        # degrading gracefully to the already-validated
        # single-node baseline rather than failing outright
```

## 4. Materials and Methods

### 4.1 Real data used to parameterize the simulation

- **Solar driver:** full calendar year 2025, 1-minute Global Horizontal Irradiation, Kuala Lumpur, Malaysia (Mendeley Data, DOI 10.17632/bgch4tw79k.1, CC BY 4.0).
- **Piezoelectric harvester power draws:** instantaneous measured power values pooled from 23 characterized experiments of a low-frequency vibration harvester (Mendeley Data, DOI 10.17632/y4cmrsdv9f.1, CC BY 4.0; companion paper [15]).
- **Node power demand:** 295.49 mW, the measured average reported in the reference paper's own case study [1].
- **Panel dimensions:** 118 mm × 70 mm, the exact panel used in the reference paper's own validation [1].
- **LoRaWAN link-success probability:** 0.89, a measured packet-delivery ratio from a rural hilly-terrain deployment [24].
- **Independent cross-check data (Section 5.4):** NASA POWER hourly solar irradiance and precipitation (MERRA-2/SYN1DEG reanalysis) for four real coordinates along and beyond the Simpang Pulai–Cameron Highlands corridor, and for two further real Malaysian landslide sites, full years as needed.

### 4.2 Modeled parameters (explicitly disclosed, not derived from measurement)

Panel efficiency (swept 0.10–0.30), energy-buffer sizing (swept 0.5–4.0 h of demand), the correlation structure between nodes (ρ = 1 on days classified "sustained overcast"; independent local-cloud attenuation otherwise), and movement-trigger probabilities are modeling assumptions, not measurements, and are treated as such throughout — swept in a sensitivity analysis (Section 5.2) rather than fixed at one arbitrary value.

### 4.3 Simulation and statistical design

A 5-node corridor was simulated at 1-minute resolution over the full real solar year (262,800 node-timesteps). Baseline (Algorithm 1 only) and treatment (Algorithm 1 + Algorithm 2) conditions were compared using a common-random-numbers paired design: both conditions draw from an identical environmental random-number stream (local-cloud masks, piezo-trigger events) that is entirely independent of a separate brokering-only random stream, so that duty-brokering is the only difference between the paired runs. Each of 16 points in a 4×4 grid (panel efficiency × buffer hours) was run across 50 independent seeds; results are reported as mean ± standard deviation across seeds. An ablation removing the one model component with no empirical grounding (the original flow-harvester placeholder) was run across 8 representative grid points at the same seed count.

## 5. Results

### 5.1 Baseline literature-gap confirmation

Section 2's review confirms the proposed combination — hazard-coupled powering plus duty-level brokering under a spatially-correlated storm topology — does not appear in the 147-source corpus, supporting the novelty claim underlying this design.

### 5.2 Simulation: duty-brokering effect, 50-seed sensitivity sweep

Across all 16 tested combinations of panel efficiency and buffer sizing, duty-brokering reduced dark-time during sustained-overcast (storm-correlated) conditions in every case (16/16), with the effect's statistical clarity depending on how resource-constrained the system is. At the most constrained setting tested (panel efficiency 0.10, buffer 0.5 h), the reduction was 32.7% ± 1.2% (n = 50 seeds) — a large, clearly significant effect. At the most comfortably provisioned setting tested (panel efficiency 0.30, buffer 4.0 h), the baseline system was already dark only 2.3% of the time, and the residual effect (3.1% ± 3.0%) was directionally consistent but not clearly distinguishable from zero — a physically sensible pattern, since a system that rarely fails has little for brokering to fix. The mechanism driving the effect was non-obvious at design time: even on fully solar-correlated storm days, independently-triggered piezoelectric harvesting events create enough node-to-node buffer asymmetry for brokering to remain useful, rather than the simpler expectation that a fully-correlated storm would leave all nodes equally dark.

### 5.3 Ablation: removing the one unvalidated model component

Setting the flow-harvester placeholder to exactly zero across 8 representative grid points (400 further seeded runs) left the brokering effect essentially unchanged (e.g., 32.16% ± 1.48% with the placeholder versus 31.97% ± 1.47% without, at panel efficiency 0.15, buffer 0.5 h) — the headline finding does not depend on the one model component that had no empirical grounding.

A subsequent literature-grounded replacement for that placeholder — driven by real hourly rainfall at an actual highland site and a power-velocity curve fitted from two real measured points in a published microturbine characterization [20] — found that, at the only catchment geometry where the implied channel velocity stayed within the literature's tested range (1,000–2,000 m²), the harvester would be active for under 1% of the year, producing sub-milliwatt power even when active. Larger, still-plausible catchments produced larger numbers only by extrapolating the fitted power curve far beyond its validated velocity range (up to 7.6 m/s against a 2.0 m/s upper test limit) and are not reported as credible. This is an unfavorable, quantified result for this specific design component, reported as such rather than adjusted until favorable.

### 5.4 Real-data cross-checks

Real paired hourly solar and precipitation data at an actual highland corridor site (NASA POWER, MERRA-2/SYN1DEG) showed a moderate negative correlation between daily rainfall and daily peak solar (r = −0.454, n = 365 days), with the wettest-quartile days averaging 15.9% lower peak solar than the driest quartile, and November showing both the highest mean rainfall and the lowest mean peak solar of any month — independently matching a solar-only-derived monsoon-suppression signature from the Kuala Lumpur dataset. The same reanalysis data, however, returned byte-identical values across three real points spanning a 35 km stretch of the actual highway corridor, confirming the product's ~100 km native resolution cannot resolve the within-corridor spatial decorrelation this paper's correlation-structure assumption (Section 4.2) requires; this specific question remains open pending ground-station data.

Cross-checking four independently documented, precisely-dated real Malaysian landslide incidents (a January 2025 Cameron Highlands slide; a September 2024 Cameron Highlands slide; the December 2022 Batang Kali campsite slide, 31 deaths; and the May 2011 Hulu Langat slide, 16 deaths) against real weather data on their actual dates produced a mixed result: one event showed a clean same-day match to the predicted high-rain/low-solar signature (rainfall in the 95.6th percentile of its year, solar in the 11.8th); one showed no same-day match but a plausible antecedent/cumulative-rainfall pattern; the deadliest event in the set (Batang Kali) failed on a comparatively sunny day three days after an extreme dark-and-wet signature, consistent with the responsible agency's own stated cause of delayed subsurface saturation; and one showed no clear match in either direction. This heterogeneity, from a sample of four, supports a design conclusion rather than a statistical one: a purely weather-coupled harvesting design would have been at its most relaxed state at exactly the moment the deadliest event in this set actually failed, which is a direct argument for ground-movement-coupled (piezoelectric) rather than weather-coupled harvesting as the primary design element.

## 6. Discussion

### 6.1 What this process revised in the original design

The flow-harvester component, present in the design as originally conceived, is downgraded to a rare-event supplement rather than a core element following Section 5.3's finding — a revision produced directly by testing the design against real data rather than retained on the strength of the original rationale alone. The piezoelectric component's justification is correspondingly strengthened by Section 5.4's event-level finding, independent of the aggregate correlation statistics that motivated it originally.

### 6.2 Internal validity

Two implementation errors were identified and corrected during this work before any result was reported: an uncontrolled random-number confound that let the baseline and treatment conditions draw from different random environments, and a day-boundary indexing error that caused a 30-minute brokering hand-off to become effectively permanent. Both are reported here, rather than silently corrected, as part of the verification standard applied throughout this study — including to its own simulation code, not only to cited literature.

### 6.3 External validity — explicitly limited

This is a single-site solar driver (Kuala Lumpur) applied to a hypothetical 5-node corridor with an assumed, not measured, spatial correlation structure; an assumed panel and buffer sizing (swept, not calibrated); and, following Section 5.3, a flow-harvester component now understood to be largely non-viable as originally conceived. It demonstrates that the proposed algorithm is implementable and produces a mechanistically traceable, statistically robust effect under a stated and partly real-data-grounded set of assumptions. It does not demonstrate that effect's magnitude at an actual highway cut-slope deployment.

### 6.4 Source and data verification

Venue-quality screening during the literature review identified one source from a publisher with documented, unrelated large-scale peer-review integrity concerns [15] (retained with this caveat, as the specific article's status could not be independently confirmed) and two sources from venues whose indexing status could not be confirmed (excluded from the final citation set). All datasets used for simulation input were confirmed to exist via direct retrieval before use; their license terms are stated in Section 4.1.

### 6.5 Required steps before deployment

Real multi-site weather data at the resolution needed to validate the spatial-correlation assumption (ground-station data, not satellite reanalysis, per Section 5.4); a real flow-harvester characterization under sediment-laden, intermittent field conditions, if that component is pursued further; calibrated rather than assumed structural constants; and the hardware-in-the-loop and physical-prototype validation stages the reference architecture itself used [1], extended to the multi-node configuration this paper's algorithm requires. None of these have yet been carried out.

## 7. Conclusion

This paper proposes and computationally tests an extension of a validated single-node IoT-microgrid architecture to a deployment class — off-grid landslide-monitoring swarms on Malaysian highway cut-slopes — where the original architecture's utility-backup assumption does not hold. A 50-seed Monte Carlo simulation, driven by real solar and piezoelectric harvester data, shows that corridor-wide duty-brokering produces a statistically robust reduction in sensing downtime concentrated specifically on the correlated storm conditions the design targets, and that this finding is not an artifact of its one unvalidated model component. Cross-checking the design's premises against real weather data and real documented landslide incidents produced genuinely mixed evidence that nonetheless motivated a concrete, favorable revision to the design (strengthening the case for ground-movement-coupled harvesting) and a concrete, unfavorable one (downgrading the flow-harvester component). The result is a preliminary feasibility study, not a field validation; the paper specifies the real-world data and hardware-in-the-loop work still required to close that gap.

## Data Availability Statement

Datasets used: Kuala Lumpur solar irradiance (Mendeley Data, DOI 10.17632/bgch4tw79k.1, CC BY 4.0); piezoelectric harvester characterization (Mendeley Data, DOI 10.17632/y4cmrsdv9f.1, CC BY 4.0); NASA POWER hourly reanalysis data (publicly available via the POWER Project API, power.larc.nasa.gov, no registration required). Simulation code is available at [repository/institutional location to be added by author].

## Author Contributions

[To be completed by author per CRediT taxonomy — e.g., Conceptualization, Methodology, Software, Formal Analysis, Investigation, Writing.]

## Funding

[To be completed by author. State "This research received no external funding" if applicable.]

## Conflicts of Interest

The author(s) declare no conflict of interest. [Confirm and complete.]

## Ethics Statement

Not applicable. This study involved no human subjects, animal subjects, or personally identifiable data; all datasets used are publicly available environmental and laboratory measurement data.

## AI Tool Usage Disclosure

Portions of this research — literature search and screening, source verification, simulation code implementation, and manuscript drafting — were performed with AI-assisted tools. All quantitative claims were independently computed by executing the described code against the cited datasets rather than generated from model memory; two implementation errors identified during this process are disclosed in Section 6.2. The author(s) take full responsibility for the content and conclusions of this manuscript.

## References

*(Selected and renumbered from the 147-source systematic review corpus; full list available in the accompanying research log. Representative subset shown — complete to the target venue's required count and format before submission.)*

1. Lee, Y.-S.; Wang, C. A Cyber-Physical Testbed for IoT Microgrid Design and Validation. *Electronics* **2024**, *13*, 1181.
2. [JKR National Slope Master Plan 2025–2030 — institutional source; to be cited per agency documentation once obtained, Section 6.5]
3. Giri, P.; et al. Wireless Sensor Network System for Landslide Monitoring and Warning. *IEEE Trans. Instrum. Meas.* **2019**.
4. Ramesh, M. Real-Time Wireless Sensor Network for Landslide Detection. In Proc. SensorComm **2009**.
5. Abraham, M.T.; et al. IoT-Based Geotechnical Monitoring of Unstable Slopes for Landslide Early Warning in the Darjeeling Himalayas. *Sensors* **2020**, *20*, 2611.
6. Gamperl, M.; et al. Internet of Things Geosensor Network for Cost-Effective Landslide Early Warning Systems. *Sensors* **2021**, *21*, 2609.
7. Ali, N.A.; et al. Development of Wireless Sensor Network for Slope Monitoring. In Proc. ICIAS **2012**.
8. Idris, A.; et al. Smart Monitoring and Warning Landslide System Using Internet of Things.
9. Piciullo, L.; et al. Definition and Performance of a Threshold-Based Regional Early Warning Model for Rainfall-Induced Landslides. *Landslides* **2017**, *14*, 995–1008.
10. Guzzetti, F.; et al. Landslide Predictions Through Combined Rainfall Threshold Models. *Landslides* **2024**.
11–13. [Additional Cluster B sources — see research log Section 4.3]
14. Rubeš, O.; et al. Development and Experimental Validation of Self-Powered Wireless Vibration Sensor Node Using Vibration Energy Harvester. *Mech. Syst. Signal Process.* **2021**, *160*, 107890.
15. Plaza, A.; Iriarte, X.; Castellano-Aldave, C.; Carlosena, A.; Bacaicoa, J. [Companion characterization paper for the piezoelectric harvester dataset used in Section 4.1]. *Sensors* **2024**, *24*, 3813. [Publisher-level integrity caveat — see Section 6.4]
16. Rigo, F.; et al. Piezoelectric Sensors as Energy Harvesters for Ultra Low-Power IoT Applications. *Sensors* **2024**, *24*, 2587.
17. Das Mahapatra, S.; et al. Piezoelectric Materials for Energy Harvesting and Sensing Applications. *Adv. Sci.* **2021**, *8*, 2100864.
18. Wang, J.; et al. Sensor-Enabled Piezoelectric Geocable–Geogrid Composite Structure for Slope Rehabilitation and Monitoring. *Eng. Geol.* **2024**, *337*, 107780.
19. Wang, J.; et al. Reinforcement and Microseismic Monitoring of Slopes with a Self-Sensing Smart Geosynthetic. *Geosynth. Int.* **2026**.
20. Lepipas, G.; et al. Miniature Water Flow Energy Harvester Based on Savonius-Type Microturbine: An Experimental Study. *Smart Mater. Struct.* **2024**, *33*.
21–23. [Additional Cluster D sources — see research log Section 4.3]
24. Chapungo, N.J.; Postolache, O. Experimental Evaluation of LoRaWAN Connectivity Reliability in Remote Rural Areas of Mozambique. *Sensors* **2025**, *25*, 6027.
25–27. [Additional Cluster E sources — see research log Section 4.3]
28. Anzum, R.; Habaebi, M.H.; Islam, M.R.; Hakim, G.P.N. A Study of LoRa Signal Propagation in Hilly Suburban Area for Smart City Applications. In Proc. IEEE ICSIMA **2021**.
29. Bahbahani, M.S.; et al. A Cooperative Clustering Protocol With Duty Cycling for Energy Harvesting Enabled Wireless Sensor Networks. *IEEE Trans. Wirel. Commun.* **2017**.
30–33. [Additional Cluster G sources — see research log Section 4.3]
34. Zhang, C.; et al. Peer-to-Peer Energy Trading in a Microgrid. *Appl. Energy* **2018**, *220*, 1–12.
35. Paudel, A.; et al. Peer-to-Peer Energy Trading in a Prosumer-Based Community Microgrid: A Game-Theoretic Model. *IEEE Trans. Ind. Electron.* **2019**.
36–37. [Additional Cluster H sources — see research log Section 4.3]
38. Lauss, G.; et al. Accurate and Stable Hardware-in-the-Loop (HIL) Real-Time Simulation of Integrated Power Electronics and Power Systems. *IEEE Trans. Power Electron.* **2021**.
39–41. [Additional Cluster I sources — see research log Section 4.3]

---

*Note to author before submission: this reference list is a representative subset of the 147-source corpus documented in full in the accompanying research log (`Topic Analysis.md`, Section 4.3). Complete numbering, verify all DOIs directly, and expand bracketed placeholders to the target venue's required format and count before submission. The venue-quality caveat on reference 15 (Section 6.4) should be resolved — by direct verification of that specific article — before submission, not left as a standing caveat in a submitted manuscript.*
