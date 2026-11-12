---
name: FYI — Who Gets an Answer?
description: Public Dossier and Government Queue Ticket visual system for the CS 132 Philippine eFOI 2025 research portfolio.
---

<!-- SEED: established with the user before implementation; re-run $impeccable document once there's code to capture the actual tokens and components. -->

# Design System: FYI — Who Gets an Answer?

## Overview

**Creative North Star: "The Public Dossier & Queue Ticket"**

This visual system replaces generic warm-cream/forest-green editorial styling with the material authority of an official Philippine public-records audit: crisp bond-paper white sheets, dense ink-black typography, 1px hairline ledger rules, tabular monospace timestamps, and rectangular ink rubber stamps. Every surface reads like a verifiable civic filing rather than a marketing showcase, balancing interactive browser exploration with complete, high-contrast A4 Print-to-PDF fidelity.

Depth comes from ruled structure, ink weight, and intentional contrast inversions (such as framing the dark PilipiNuts 2026 exhibit inside an ink-black specimen panel) rather than soft shadows or decorative gradients. Motion is sequential, mechanical, and restrained—mirroring a queue counter advancing, an SVG `stroke-dashoffset` routing path drawing along the paper trail, and an audit stamp landing—governed by a `--1s` duration multiplier (`1ms` by default; `1s` only under `prefers-reduced-motion: no-preference`) so every state snaps cleanly to its final resting state in reduced-motion and print output.

**Key Characteristics:**
- Bond-paper white ground with crisp ink-black type and 1px ledger rules replacing tinted cream/green chrome.
- Restrained palette: neutral paper and ink carry structure, while semantic stamp and chart inks signal verdicts and outcomes sparingly.
- Tabular monospace numerals and timestamps paired with authoritative civic editorial prose.
- Ink-black darkroom specimen framing for pre-rendered dark-ground exhibits (`nutshell.png`).
- Sequential mechanical motion (ticket counter, scroll-drawn routing line, verdict stamps) with full static parity in `@media print` and `prefers-reduced-motion`.

## Colors

A **Restrained** paper-and-ink palette where crisp neutrals govern layout and structure, and saturated signal inks are reserved strictly for rubber-stamp verdicts, EO No. 2 compliance indicators, and data encodings. Exact hex/OKLCH values are `[to be resolved during implementation]`.

### Primary
- **Audit Ink (Black)** (`[to be resolved during implementation]`): Primary typography, 1px ledger rules, active tab/control states, and the ink-black Exhibit A specimen container that anchors `nutshell.png`.
- **Stamp Signal Ink (Verdict / Alert)** (`[to be resolved during implementation]`): Reserved strictly for rectangular rubber-stamp verdicts (`H0 REJECTED`), EO No. 2 15-working-day threshold warnings, and non-response/silence emphasis (e.g., Water District 26.1% no-reply share).

### Secondary
- **Verification / Neutral Verdict Ink** (`[to be resolved during implementation]`): Used for null/retained-hypothesis stamps (`NO LINK FOUND · p = 0.99`) and secondary statistical annotations where red/alert framing would falsely imply failure.
- **Outcome Chart Encodings** (`[to be resolved during implementation]`): Distinct, colorblind-safe, print-legible series colors differentiating `Successful`, `Partially successful`, `Unsuccessful`, `Open`, and `Referred` states across SVG charts.

### Neutral
- **Bond Paper White** (`[to be resolved during implementation]`): Primary page and card ground across screen and A4 print.
- **Tinted Ledger Paper** (`[to be resolved during implementation]`): Subtle off-white/cool-gray surface reserved for ticket stubs, `<details>` appendix summaries, and table header bands.
- **Muted Slate Ink** (`[to be resolved during implementation]`): Secondary captions, methodological footnotes, and axis labels while maintaining strong contrast on paper white.
- **Ledger Hairline Rule** (`[to be resolved during implementation]`): 1px structural dividers, table rules, and ticket perforation/stub boundaries.

### Named Rules
**The Paper-First Rule.** Bond-paper white and ink black own at least 85% of the visual field; semantic stamp and chart colors earn attention through scarcity and never bleed into decorative page chrome.

**The Print-Safe Contrast Rule.** Every interactive chart series, stamp, and muted label must remain legible both on screen and when printed in color or grayscale onto A4 paper.

## Typography

**Display Font:** `[to be resolved during implementation]` (authoritative civic/editorial display face, avoiding overused defaults)
**Body Font:** `[to be resolved during implementation]` (high-legibility workhorse sans or serif suited to dense reading and A4 print)
**Label / Data Font:** `[to be resolved during implementation]` (crisp monospace with `tabular-nums` for tracking numbers, elapsed-day counters, p-values, and ledger columns)

**Character:** Clinical civic clarity—combining crisp headline authority with strict tabular alignment so statistical comparisons, timestamps, and ticket counters scan vertically without digit jitter.

### Hierarchy
- **Display** (`[to be resolved during implementation]`): Dossier cover headline only.
- **Headline** (`[to be resolved during implementation]`): Major numbered dossier section headers (`01`–`06`).
- **Title** (`[to be resolved during implementation]`): Research question cards, queue ticket header, and exhibit titles.
- **Body** (`[to be resolved during implementation]`): Narrative prose, methodology explanations, and caveats, constrained to a comfortable reading measure.
- **Label / Tabular Data** (`[to be resolved during implementation]`): Uppercase tracked section stamps, queue ticket counters, statistical ledger cells, axis ticks, and timestamps.

### Named Rules
**The Tabular Numerals Rule.** Every numerical column, queue counter, elapsed-day readout, and statistical table cell enforces lining tabular numerals (`"tnum" 1, "onum" 0`) so figures align vertically across interactive states and A4 print pages.

## Layout

An asymmetric yet disciplined dossier ledger grid built around continuous 1px structural rules, generous reading margins, and clear numbered sections that translate cleanly from responsive web viewports down to A4 page widths.

- **Web container & rhythm:** Full-width masthead and cover-sheet ledger followed by a sticky-right / scrolling-left scrollytelling sequence (`svh`-height sticky routing diagram paired with spaced narrative steps), a centered Queue Ticket spotlight selector, a completion-tracked 6-group agency dashboard grid with a sticky sort/jump toolbar, and balanced two-column ledger splits for exhibits and archival methodology. Exact container widths, breakpoints, and spacing scale are `[to be resolved during implementation]`.
- **Collapsible density management:** Detailed verification tables (Shapiro–Wilk tests, 15 Bonferroni pairwise comparisons, sensitivity checks) live inside semantic disclosure containers (`<details>`) so the web reading flow stays scannable without losing completeness.
- **A4 Print pagination (`@media print`):** Single-column/print-tuned flow on A4 (`@page { size: A4 }`), hiding web-only navigation, sticky toolbars, and print triggers; collapsing all sticky `svh` containers and tall `vh` scrollytelling step margins into static, compact stacked blocks (`position: static; height: auto`); rendering the SVG paper-trail routing line at full `stroke-dashoffset: 0`; auto-revealing all `<details>` statistical appendices; locking interactive charts, completion grids, and stamped verdicts into complete static snapshots; and preventing mid-element page breaks across cards, stamps, figures, and tables.

### Named Rules
**The Complete-Snapshot Print Rule.** Nothing essential to grading or research verification may stay hidden behind an unexpanded toggle, unclicked simulator state, or incomplete scroll animation in `@media print`.

## Elevation & Depth

**Flat paper and ink hierarchy.** Surfaces sit on the same bond-paper plane and never use soft drop shadows, blurs, or floating glass panels. Hierarchy is established exclusively through 1px ledger rules, thicker structural top bars, ink-weight contrast, and deliberate dark-canvas inversion for `nutshell.png` Exhibit A.

### Named Rules
**The Zero-Shadow Ledger Rule.** Depth comes from ruled lines, ink density, and crisp 1px borders—never diffused drop shadows or decorative elevation.

## Shapes

Sharp, rectilinear government-form and queue-ticket geometry: square or near-square corners, crisp 1px rectangular borders, perforated/notched ticket dividers where functional, and rectangular ink rubber-stamp frames angled slightly only on verdict stamps.

- **Buttons & selectors:** Rectilinear control geometry with clear 1px borders and unambiguous inverted active states.
- **Rubber stamps:** Rectangular double- or heavy-bordered ink frames in uppercase monospace, appearing cleanly in final resting position in print and reduced-motion modes.
- **No pill clutter:** Avoid rounded pill badges and soft bubbly cards across the entire system.

## Do's and Don'ts

### Do:
- **Do** enforce crisp bond-paper white, ink-black type, and 1px ledger rules across all sections and controls.
- **Do** isolate the dark-background `nutshell.png` inside a high-contrast ink-black Exhibit A frame so it reads as an intentional photographic/data plate rather than an unstyled mismatch.
- **Do** keep every animation (queue ticket counter, SVG `stroke-dashoffset` paper-trail routing line, rubber-stamp verdicts) sequential, purposeful, and immediately settled via `--1s: 1ms` under reduced-motion and in `@media print`.
- **Do** collapse tall `vh`/`svh` scrollytelling spacers and `position: sticky` panels into static, compact print flow under `@media print` so A4 PDFs contain zero blank vertical gaps.
- **Do** format all dates, durations, counts, and test statistics in `tabular-nums` monospace or aligned numeric columns.

### Don't:
- **Don't** retain warm-cream paper tints, forest-green brand fills, or generic editorial card drop-shadows from the prior template.
- **Don't** gate methodology, sources, or later sections behind `display: none` until scroll completion; keep all dossier sections accessible on initial load and in print.
- **Don't** use saturated colors as large decorative backgrounds or non-semantic accents; reserve signal inks for stamps, thresholds, and data encodings.
- **Don't** hide statistical appendices, stamped verdicts, or simulator outputs when printing to A4 PDF.
- **Don't** load external JS/CSS frameworks or charting libraries that break static GitHub Pages delivery or print rendering.

