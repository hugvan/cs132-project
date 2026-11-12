---
name: FYI — Who Gets an Answer?
description: Public Dossier + Editorial Scrollytelling visual system for the CS 132 Philippine eFOI 2025 research portfolio.
colors:
  bond-paper: "#FFFFFF"
  paper-tint: "#F7F7F5"
  stone-band: "#ECECE8"
  hairline-rule: "#D2D4CF"
  audit-ink: "#0E0E0E"
  muted-slate: "#4B5058"
  cobalt-blue: "#1D4ED8"
  cobalt-hover: "#1E40AF"
  cobalt-tint: "#EFF4FD"
  signal-orange: "#F46201"
  orange-hover: "#e45b00"
  orange-tint: "#FFF4EC"
  category-teal: "#155E63"
  category-steel: "#3B82A6"
  category-gold: "#D49B2A"
  category-gray: "#6B7280"
  darkroom-ground: "#0B0D10"
typography:
  display:
    fontFamily: "Source Serif 4, Iowan Old Style, Georgia, Times New Roman, serif"
    fontSize: "clamp(2.65rem, 5.4vw, 4.35rem)"
    fontWeight: 700
    lineHeight: 0.96
    letterSpacing: "-0.03em"
  headline:
    fontFamily: "Source Serif 4, Iowan Old Style, Georgia, Times New Roman, serif"
    fontSize: "clamp(1.45rem, 2.5vw, 1.95rem)"
    fontWeight: 700
    lineHeight: 1.18
    letterSpacing: "-0.02em"
  title:
    fontFamily: "Source Serif 4, Iowan Old Style, Georgia, Times New Roman, serif"
    fontSize: "1.35rem"
    fontWeight: 700
    lineHeight: 1.22
  body:
    fontFamily: "Public Sans, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.45
  label:
    fontFamily: "JetBrains Mono, ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
    fontSize: "0.75rem"
    fontWeight: 700
    letterSpacing: "0.06em"
    fontFeature: "\"kern\" 1, \"onum\" 0, \"liga\" 0, \"tnum\" 1"
rounded:
  subtle: "3px"
spacing:
  xs: "8px"
  sm: "12px"
  md: "18px"
  lg: "24px"
  xl: "36px"
components:
  button-primary:
    backgroundColor: "{colors.signal-orange}"
    textColor: "{colors.bond-paper}"
    rounded: "{rounded.subtle}"
    padding: "0.75rem 1.25rem"
  button-primary-hover:
    backgroundColor: "{colors.orange-hover}"
    textColor: "{colors.bond-paper}"
  selector-tile:
    backgroundColor: "{colors.cobalt-tint}"
    textColor: "{colors.audit-ink}"
    rounded: "{rounded.subtle}"
    padding: "0.78rem 0.85rem"
  stamp-alert:
    backgroundColor: "{colors.orange-tint}"
    textColor: "{colors.signal-orange}"
    rounded: "{rounded.subtle}"
    padding: "0.3rem 0.65rem"
  stamp-neutral:
    backgroundColor: "{colors.cobalt-tint}"
    textColor: "{colors.cobalt-blue}"
    rounded: "{rounded.subtle}"
    padding: "0.3rem 0.65rem"
  agency-panel:
    backgroundColor: "{colors.paper-tint}"
    textColor: "{colors.audit-ink}"
    rounded: "{rounded.subtle}"
    padding: "1.45rem 1.35rem"
---

# Design System: FYI — Who Gets an Answer?

## Overview

**Creative North Star: "Editorial Civic Scrollytelling × The Public Dossier"**

This visual system pairs crisp public-audit contrast — bond-paper white (`#FFFFFF` / `#F7F7F5`) and audit-ink black (`#0E0E0E`) with **Verification Cobalt** (`#1D4ED8`) and **Signal Orange** (`#F46201`, `#e45b00` hover from the reference) — across an uncluttered editorial scrollytelling layout (`#intro` → `#pick` → `#dashboard` → `#methodology`). Clean Google Fonts typography (`Source Serif 4` serif headings without italic slant on `#title`, `Public Sans` interface/analytical prose, and `JetBrains Mono` lining tabular numerals) replaces hotlinked third-party fonts while preserving generous tonal surfaces, borderless structural separation, SVG `stroke-dashoffset` routing animations, interactive agency comparison (`#pick`), completion tracking, interactive RQ1–RQ3 SVG charts, and native browser A4 `@media print` support without cluttering the masthead with an extra button.

Every factual statistical claim, sample caveat, calendar-vs-working-day qualifier, and A4 Print-to-PDF layout discipline from our audit remains intact. Motion continues to be governed by `--1s` (`1ms` by default; `1s` under `@media screen and (prefers-reduced-motion: no-preference)`), ensuring reduced-motion parity and instant static A4 print snapshots.

**Key Characteristics:**
- Bond-paper canvas (`#FFFFFF` / `#F7F7F5`) paired with audit-ink typography (`#0E0E0E`), muted slate secondary copy (`#4B5058`), and stone structural banding (`#ECECE8`).
- Masthead wordmark (`FYI.`) styled in cobalt blue (`#1D4ED8`) with an orange period (`#F46201`) beside spacious single-row desktop navigation links.
- Clean Google Fonts stack: `Source Serif 4` headings + `Public Sans` body copy + `JetBrains Mono` lining tabular numerals (`"kern" 1, "onum" 0, "liga" 0, "tnum" 1`).
- Verification Cobalt (`#1D4ED8` / hover `#1E40AF` / tint `#EFF4FD`) for SVG routing progress, selector states, and neutral completion badges; Signal Orange (`#F46201` / hover `#e45b00` / surface `#FFF4EC`) for primary CTAs, alert metrics, EO No. 2 15-day benchmark line, Water District silence alerts (`26.1%`), and rejected-hypothesis stamps.
- Print-safe chart palette (`#155E63` teal successful, `#3B82A6` steel partial, `#F46201` orange unsuccessful, `#D49B2A` gold referred, `#6B7280` slate open) for crisp stacked and strip-chart discrimination in SVG exhibits.

## Colors

### Primary
- **Audit Ink** (`#0E0E0E`): Primary typography, structural rules, 3px table header bottoms, median reply bars, and inverted footer ground.
- **Bond Paper** (`#FFFFFF` / `#F7F7F5`): Primary canvas (`#FFFFFF`) and borderless tonal panel/card surface (`#F7F7F5`).
- **Verification Cobalt** (`#1D4ED8`, hover `#1E40AF`, tint `#EFF4FD`): `.brand-mark` (`FYI`), SVG routing stroke, active toggle buttons, inspected cards, and audit verification stamps.
- **Signal Orange** (`#F46201`, hover `#e45b00`, tint `#FFF4EC`): `.brand-mark` accent dot (`.`), primary action CTA (`Inspect an Agency Group`), EO No. 2 15-day reference line, `Replay` button, silence alerts, and rejected-hypothesis stamps.

### Neutral Surfaces & Structural Banding
- **Stone Band** (`#ECECE8`): Sticky completion tracker bar (`.tracker-bar`) and archival `#methodology` band.
- **Paper Tint** (`#F7F7F5`): Scoped panels, chart bar tracks, and tabular summary cards.
- **Hairline Rule** (`#D2D4CF`): Subtle SVG gridlines, row separators, and unreached routing track.
- **Muted Slate** (`#4B5058`): Secondary metadata, links (`border-bottom: 2px solid currentColor`), axis labels, and captions.

### Chart Semantics & Exhibit A
- **RQ1 / RQ2 / RQ3 Series Palette**:
  - Successful / quartile fill: `#155E63`
  - Partially successful: `#3B82A6`
  - Unsuccessful / 15 d ref.: `#F46201`
  - Referred: `#D49B2A`
  - Open: `#6B7280`
- **Darkroom Specimen Bezel (`#nutshell`)**: `#0B0D10` dark frame with `#FFFFFF` / `#E2E8F0` / `#93C5FD` contrast around `assets/figures/nutshell.png` (`PilipiNuts 2026`), collapsing to white/black outline in `@media print`.

## Typography

- **Display / Editorial Serif (`--serif`):** `"Source Serif 4", Iowan Old Style, Georgia, "Times New Roman", serif` — upright (non-italic) `#title`, numbered section `<h2>` headings, card titles, and team names.
- **Body / Interface Sans (`--sans`):** `"Public Sans", -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif` — analytical prose, nav items, bold underlined links, buttons, and labels.
- **Monospace Data (`--mono`):** `"JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, Consolas, monospace` — forced lining tabular numerals (`"kern" 1, "onum" 0, "liga" 0, "tnum" 1`) for timestamps, sample counts, p-values, IQRs, and SVG axis readouts.

## Layout & Components

- **Measure & Surfaces:** `--measure: 1120px`, borderless editorial cards/steps/panels using tonal fills (`#F7F7F5`, `#ECECE8`, `#EFF4FD`) and generous whitespace; uncluttered single-row desktop `.masthead` featuring blue `.brand-mark` with orange dot (`FYI.`) and 7 uppercase navigation links (`Request Lifecycle`, `Agency Explorer`, `Analysis`, `Nutshell`, `Methodology`, `Action`, `Team`).
- **Border Radius:** Unified `3px` (`--border-radius: 3px`) across buttons, tiles, stamps, and cards.
- **Copy Discipline:** Paperwork, clock, and comparison metaphors are communicated through visual styling, SVG routing, and numeric transitions rather than literal meta-labels in navigation, buttons, or record headers.

## Do's and Don'ts

### Do:
- **Do** keep navigation links single-row on desktop `>960px` (`flex-wrap: nowrap`) so `.masthead` never overlaps `.tracker-bar`, and wrap gracefully on narrower viewports.
- **Do** enforce `"kern" 1, "onum" 0, "liga" 0, "tnum" 1` across numbers, tables, counters, and stamps.
- **Do** settle all `stroke-dashoffset`, animated counters, stamps, and `<details>` tables in `@media print` and `beforeprint`.
- **Do** preserve every factual statistical qualifier (calendar days vs. EO No. 2 working days, 90-day Q2 gap, 22 vanished pages, exploratory permutation caveats).

### Don't:
- **Don't** hotlink proprietary external fonts (`pudding.cool`) or leave development live-reload scripts in `docs/index.html`.
- **Don't** gate methodology, sources, or sensitivity tables behind required clicks.
- **Don't** uppercase Greek symbols (`α = 0.05`).
