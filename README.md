# IoT Microgrid: Hazard-Coupled Self-Powering and Corridor-Wide Duty-Brokering for Off-Grid Landslide Early-Warning IoT Sensor Swarms

A design-and-simulation study extending Lee & Wang's (2024) single-node "IoT microgrid" architecture (*Electronics* 13(7):1181) to off-grid landslide-monitoring sensor swarms on Malaysian highway cut-slopes, where the original architecture's utility-grid-backup assumption does not hold.

## Repository Contents

- **`Topic Analysis.md`** — the full research log: PRISMA-aligned systematic review (147 screened / 146 cited sources across 9 clusters), dataset discovery, real-data analyses, simulation design, sensitivity sweep, ablation study, and real-event cross-checks. This is the working document the manuscript below was drafted from.
- **`Manuscript.md`** — the manuscript in Markdown form.
- **`LaTeX/`** — the submission-ready manuscript for MDPI *Electronics*, using the journal's own LaTeX class (`Definitions/mdpi.cls`). Includes `manuscript.tex`, the compiled `manuscript.pdf` (21 pages), the generated bibliography (`bibliography_block.tex`, 146 verified references), and the two data figures (`fig_sweep.pdf`, `fig_events.pdf`).
- **`LaTeX_blind/`** — an anonymized version of the same manuscript for double-blind review (author names, affiliation, correspondence, ORCID iDs, and author-contributions statement removed; checked for residual identity leaks).
- **`Data/_scripts/`** — the actual simulation and analysis code: `corridor_sim.py` (the core duty-brokering simulation, Algorithms 1–2), `sensitivity_sweep.py` (the 50-seed Monte Carlo sweep), `ablation_no_flow.py` (the flow-harvester ablation), `flow_harvester_model.py` (the literature-grounded flow-harvester viability model), `make_figures.py` (figure generation from real sweep data), and `verify_all_dois.py` (CrossRef-based bibliography verification). Also `verified_refs.txt`, the final checked 146-entry reference list.

## Data Availability

Raw third-party datasets used to drive the simulation are not redistributed in this repository (see `.gitignore`) but are freely available at their original sources:
- Kuala Lumpur solar irradiance: Mendeley Data, DOI [10.17632/bgch4tw79k.1](https://doi.org/10.17632/bgch4tw79k.1) (CC BY 4.0)
- Piezoelectric harvester characterization: Mendeley Data, DOI [10.17632/y4cmrsdv9f.1](https://doi.org/10.17632/y4cmrsdv9f.1) (CC BY 4.0)
- NASA POWER hourly reanalysis data: freely accessible via the [POWER Project API](https://power.larc.nasa.gov/), no registration required

## Status

This is reported throughout as a **preliminary computational feasibility study**, not a field validation. See the manuscript's Discussion section for the real-world data collection and hardware-in-the-loop work still required before deployment.

## AI Disclosure

Portions of this research — literature search and screening, source verification, simulation code implementation, and manuscript drafting — were performed with AI-assisted tools. All quantitative claims were independently computed by executing the described code against the cited datasets. Two implementation errors identified and corrected during this process are disclosed in the manuscript (Discussion, Internal Validity).
