# Idling ROI Tool

A browser-based tool that connects to a MyGeotab database to analyse vehicle idling behaviour and calculate the financial impact of reducing idle time across a fleet.

Built for fleet managers and sales professionals to quantify and present idling ROI — no installation required.

---

## How It Works

```
MyGeotab API
  │
  ├─ Device + Groups       → Vehicle list with powertrain classification
  ├─ Trip                  → Idle duration per vehicle
  └─ FuelAndEnergyUsed     → Actual fuel/energy consumed while idling
        │
        ▼
  Browser-side JavaScript
        │
        ├─ Idle Cost         → Fuel/energy × configured price per unit
        ├─ Annual Savings    → Annualised from period data × reduction scenarios
        └─ Scaled Savings    → Projected to estimated total fleet size
              │
              ▼
  Single-page report  →  Print as PDF  /  Download HTML  /  Diagnostic CSV
```

The tool runs entirely in the browser — no server, no build step, no installation.

---

## Features

| Metric | Description |
|--------|-------------|
| Idle duration | Total and per-vehicle idle hours for the analysis period |
| Idling % | Idle hours as a share of total engine-on time |
| Fuel & energy consumed | Actual telemetry if available; idle rate estimate as fallback |
| Total idle cost | Fuel/energy × configured price, across all powertrain types |
| Savings at 25% reduction | Annualised savings for the current fleet at 25% idle reduction |
| Scaled annual savings | Same savings projected to an estimated total fleet size |
| Savings to reach 10% | Savings required to hit the industry top-quartile benchmark |
| Fleet benchmark | Contextual comparison against the 10% and ~20% industry benchmarks |
| Activity trend | Driving vs idle hours over time, auto-bucketed by period length |

Supports all MyGeotab powertrain types: ICE Petrol, ICE Diesel, BEV, PHEV, FCEV, Biodiesel, Ethanol, CNG, LPG.

---

## Prerequisites

- A MyGeotab account with access to the target database
- Vehicles assigned to the correct **Powertrain and Fuel Type** groups in MyGeotab
- Trip data present in the selected analysis period

Vehicles without a valid fuel type assignment are excluded from calculations and flagged in the report.

---

## Project Structure

```
idling-roi-tool/
├── index.html        # Full application (single file — no build required)
├── USER_GUIDE.md     # Detailed user guide
├── mockup.html       # UI mockup (development reference)
└── README.md         # This file
```

---

## Getting Started

The tool is hosted on GitHub Pages:

**https://farindn.github.io/idling-roi-tool/**

1. Open the URL in a browser
2. Enter your MyGeotab username, database, and password
3. Configure the analysis period, currency, and fuel/idle rates
4. Click **Generate Idling ROI Report**

For detailed instructions on each screen and an explanation of all calculations, see the [User Guide](USER_GUIDE.md).

---

## Add-In Installation

For partners or customers who prefer a native MyGeotab experience, the tool is also available as a ZIP-based add-in. No login screen — MyGeotab passes credentials automatically.

### Step 1 — Download the add-in

Download `addin/releases/idling-roi-tool.zip` from this repository.

### Step 2 — Upload to MyGeotab

1. Sign in to MyGeotab as an **Administrator**
2. Go to **Administration → System → System Settings → Add-Ins**
3. Click **New Add-In**
4. Click the upload button and select `idling-roi-tool.zip`
5. Click **OK** → **Save**
6. Refresh the page (Ctrl+R / Cmd+R)

The tool now appears under **Reports → Idling ROI Tool** in the left-hand navigation.

### Updating to a new version

1. Download the latest `idling-roi-tool.zip` from `addin/releases/`
2. Go to **Administration → System → System Settings → Add-Ins**
3. Click the existing **Idling ROI Tool** entry → **Remove**
4. Click **New Add-In**, upload the new ZIP → **OK** → **Save** → Refresh

### Rebuilding the ZIP

If you need to build the ZIP from source (after modifying `addin/index.html`):

```
cd addin
python build_zip.py
```

Requires Python 3.6+. No external dependencies.

---

## Known Limitations

- **Trip boundary variance** — the tool may include slightly more boundary trips than MyGeotab's built-in reports, resulting in a typical 1–2% variance. Use the Diagnostic CSV to investigate discrepancies.
- **PHEV telemetry** — MyGeotab does not split PHEV fuel consumption into electric and combustion components. The tool uses a combined idle rate estimate for PHEVs without telemetry.
- **Rate limiting** — large fleets or long analysis periods fetch more data and take longer to generate. Expect additional time for multi-month periods.
- **Idle rate fallback** — idle rate settings are only used for vehicles without `FuelAndEnergyUsed` telemetry. Vehicles with telemetry always use recorded values.

---

*For feedback or issues, contact Revenue Generation International — SEA*
