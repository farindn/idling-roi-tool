# User Guide — Idling ROI Tool (MyGeotab Add-In Version)

**Table of contents**

- Introduction
  - Document Disclaimer
  - Prerequisites
  - Differences from the Web Version
- Installation
  - Step 1 — Download the Add-In ZIP
  - Step 2 — Upload to MyGeotab
  - Step 3 — Access the Tool
  - Updating to a New Version
- Dashboard Page
  - Fleet Summary
  - Unassigned Vehicles
  - Estimated Fleet Size
  - Analysis Period
  - Currency & Fuel / Idling Settings
- Report Page
  - Report Header
  - Activity Trend
  - Trip Activity
  - Idling Cost Overview
  - Fleet Idling Benchmark
  - Exporting the Report
- Understanding the Calculations
  - How Idling Cost is Calculated
  - How Annual Savings are Calculated
  - Idling Benchmark Reference
  - Data Sources and Variance
- Troubleshooting
  - Common Issues
  - Diagnostic CSV

---

# Introduction

The Idling ROI Tool is available as a MyGeotab add-in — installed directly into your MyGeotab database via a ZIP file upload. Once installed, it appears in the **Reports** menu alongside other MyGeotab reports, with no separate login required.

This guide covers the add-in version. For the standalone web version (hosted on GitHub Pages), see [USER_GUIDE.md](USER_GUIDE.md).

## Document Disclaimer

This document's content, including specifications, procedures, and screenshots, is subject to review and revision. We may make changes, updates, or modifications to product features, specifications, procedures, or the visual presentation without prior notice. Users should consult the current guide version for the most accurate information.

## Prerequisites

- **MyGeotab Administrator account** — required to install add-ins via System Settings
- **Powertrain & Fuel Type Configuration** — vehicles must be assigned to the correct Powertrain and Fuel Type groups in MyGeotab; vehicles without valid fuel type assignments will be excluded from calculations
- **Trip Data** — the selected analysis period must contain trip data for accurate calculations

## Differences from the Web Version

| Aspect | Web Version | Add-In Version |
|--------|-------------|----------------|
| Access | Browser, separate URL | MyGeotab → Reports → Idling ROI Tool |
| Login | Required (enter credentials manually) | Not required (MyGeotab passes credentials automatically) |
| Sign out | Navbar sign-out button | Sign out from MyGeotab directly |
| Installation | None | ZIP upload via System Settings (one-time) |
| Offline use | Accessible from any browser | Requires MyGeotab login |

All report calculations, dashboard settings, export options, and chart features are identical between both versions.

---

# Installation

## Step 1 — Download the Add-In ZIP

Download `addin/releases/idling-roi-tool.zip` from the project repository.

## Step 2 — Upload to MyGeotab

1. Sign in to MyGeotab as an **Administrator**
2. Go to **Administration → System → System Settings → Add-Ins**
3. Click **New Add-In**
4. Click the upload button and select `idling-roi-tool.zip`
5. Click **OK**
6. Click **Save**
7. Refresh the page (Ctrl+R / Cmd+R)

## Step 3 — Access the Tool

After installation, the tool appears in the left-hand navigation under **Reports → Idling ROI Tool**.

MyGeotab passes your session credentials to the tool automatically — no login screen will be shown.

## Updating to a New Version

When a new version of the add-in is available:

1. Download the latest `idling-roi-tool.zip` from `addin/releases/`
2. Go to **Administration → System → System Settings → Add-Ins**
3. Click the existing **Idling ROI Tool** entry → **Remove**
4. Click **New Add-In**, upload the new ZIP → **OK** → **Save** → Refresh

**Note**: MyGeotab does not support in-place add-in updates. You must remove the old version before installing the new one.

---

# Dashboard Page

When you open the tool, you will land directly on the **Idling ROI Analysis** dashboard. This page allows you to configure the report parameters before generating your Idling ROI Report.

## Fleet Summary

The Fleet Summary section displays:

- **Total Devices**: The total number of vehicles in your database with a valid powertrain/fuel type assignment
- **Fuel Type Breakdown**: Cards showing the count of vehicles by fuel type (e.g., Gasoline, Diesel, BEV)

Vehicles are auto-resolved from the `GroupPowertrainAndFuelTypeId` hierarchy in MyGeotab. The tool walks each device's group ancestry to determine the correct fuel type.

## Unassigned Vehicles

If any vehicles in your database have an invalid or missing fuel type assignment, they will appear in the **Unassigned Vehicles** section with a warning banner.

These vehicles are **excluded** from cost calculations until their powertrain/fuel type is corrected in MyGeotab.

For each unassigned vehicle, you can click **Edit in MyGeotab** to open the device settings page and assign the correct group. The link will open the device page within your current MyGeotab session.

## Estimated Fleet Size

This optional field allows you to project savings for a larger fleet size.

- Enter the total number of vehicles you expect to have (e.g., 100)
- The report will scale the annual savings proportionally
- If left at the current fleet size, no scaling is applied

Use this feature when presenting ROI projections to customers who plan to expand their fleet.

## Analysis Period

Define the date range for your analysis:

- **Start Date**: The beginning of the analysis period
- **End Date**: The end of the analysis period

The tool will fetch all trip and fuel data within this window. The analysis period can range from a single day to multiple months.

**Note**: A hint below the date fields shows the calculated period length (e.g., "Analysis period: May 1, 2026 – May 15, 2026").

**Performance Note**: Longer analysis periods require more data to be fetched from MyGeotab and will take longer to load. For large fleets or multi-month periods, expect additional time for report generation.

## Currency & Fuel / Idling Settings

This section allows you to configure pricing and idle consumption rates.

### Currency

Select your preferred currency from the dropdown. The currency is auto-detected from your MyGeotab user profile but can be changed as needed. Supported currencies include USD, CAD, EUR, GBP, AUD, TWD, and others.

### Fuel Settings Table

The table displays the following columns for each fuel type present in your fleet:

| Column | Description | Editable |
|--------|-------------|----------|
| **Fuel Type** | The fuel/energy type (auto-detected from MyGeotab) | No |
| **Powertrain** | The powertrain category (ICE, Electric, Plug-in, Fuel Cell) | No |
| **Vehicles** | Number of vehicles with this fuel type | No |
| **Price / Unit** | The cost per unit of fuel (L, kWh, or kg) | Yes |
| **Idle Rate** | The estimated fuel/energy consumption rate while idling | Yes |

**Note**: Fuel Type, Powertrain, and Vehicle counts are read-only. To change a vehicle's fuel type or powertrain assignment, update the vehicle's group membership in MyGeotab.

**Tip**: For accurate fuel pricing, visit [Global Petrol Prices](https://www.globalpetrolprices.com/countries/) and select your country to find current average fuel prices in your region.

### Default Idle Rates

The tool uses industry-standard default idle consumption rates:

| Powertrain | Default Idle Rate | Source |
|------------|-------------------|--------|
| ICE Petrol | 0.6 L/hr | EPA/DOE Fact #861 |
| ICE Diesel | 3.0 L/hr | Argonne/DOE heavy-duty data |
| BEV | 3.0 kWh/hr | DOE Vehicle Technologies Office |
| PHEV | 1.5 kWh/hr + 0.3 L/hr | Combined estimate |
| FCEV | 0.3 kg/hr | Industry estimate |

**Important**: When actual fuel consumption data is available from `FuelAndEnergyUsed` records in MyGeotab, the tool uses the recorded values instead of the estimated idle rates. The idle rate setting is a fallback for vehicles without fuel telemetry.

---

# Report Page

After configuring your settings, click **Generate Idling ROI Report** to create the report. A loading overlay will appear with progress steps while the tool fetches and processes your fleet data.

## Report Header

The report header displays:

- **Database**: The MyGeotab database name
- **Period**: The analysis date range
- **Vehicles Included**: The number of vehicles with valid data
- **Generated Date**: When the report was created

### Export Options

Three buttons are available in the header:

| Button | Description |
|--------|-------------|
| **Print as PDF** | Opens the browser print dialog for PDF export |
| **Download HTML** | Downloads a standalone HTML file of the report |
| **Diagnostic CSV** | Downloads a per-vehicle breakdown for data validation |

## Activity Trend

This chart shows driving and idle hours over time as a stacked bar chart — each bar represents a time bucket, with the green segment (driving) stacked below the red segment (idling). The chart automatically adjusts its bucketing based on the analysis period length:

| Period Length | Bucketing |
|---------------|-----------|
| 1–14 days | Daily |
| 15–90 days | Weekly |
| 91+ days | Monthly |

- **Green bars**: Driving hours
- **Red bars** (stacked on top): Idle hours

**Weekly label format**: Weekly buckets are labelled by their week-of-month based on the Monday of each week. For example, if the Monday of a week falls on 30 March, it is labelled "Week 5 - Mar 2026" — even if trips from that week extend into April.

## Trip Activity

Four stat cards summarise driving, idling, and fuel consumption for the period:

| Card | Description |
|------|-------------|
| **Total Driving Duration** | Total hours vehicles were in motion |
| **Total Idle Duration** | Total hours engines were running with speed = 0 |
| **Idling %** | Idle hours as a percentage of total engine-on time |
| **Fuel & Energy Consumed** | Total fuel (litres) and energy (kWh) consumed while idling |

**Conditional colour coding**: The **Total Idle Duration** and **Idling %** cards change colour based on the fleet's idling rate against the 10% industry benchmark:
- **Red** — fleet idling is above 10% (improvement opportunity)
- **Green** — fleet idling is at or below 10% (top quartile performance)

**Fuel & Energy Consumed — Per-Vehicle Calculation Logic:**

For each vehicle, the tool checks whether actual fuel telemetry is available:

1. **If `FuelAndEnergyUsed` records exist**: The tool uses the actual `totalIdlingFuelUsedL` and `totalIdlingEnergyUsedKwh` values from MyGeotab.
2. **If no fuel records exist**: The tool estimates consumption using `Idle Hours × Idle Rate` based on the vehicle's fuel type settings.

In mixed fleets, each vehicle is handled independently and all per-vehicle values are summed into the fleet totals shown on the report.

## Idling Cost Overview

Four stat cards show the financial analysis:

### Total Idle Cost

The cost of fuel and energy consumed during idling for the analysis period.

**Calculation**: `Idle Fuel (L) × Fuel Price ($/L)` or `Idle Energy (kWh) × Electricity Price ($/kWh)`

The sub-text shows the period length (e.g., "15-day period at configured prices").

### Savings at 25% Reduction

The projected **annual** savings if the fleet's idling ratio is reduced by 25% from its current level, based on the vehicles currently included in the analysis.

**Calculation**:
```
Annual Idle Cost = Period Idle Cost × (365 / Period Days)
Savings at 25% = Annual Idle Cost × 0.25
```

The 25% reduction applies to the idling ratio itself — for example, a fleet currently idling at 28.7% would drop to 21.5% under this scenario.

The sub-text shows the vehicle count and the resulting idling rate change (e.g., "Annually based on 59 vehicles" / "22.1% → 16.6%").

### Scaled Annual Savings

The same 25% reduction savings, scaled up to your **Estimated Total Vehicles** figure from the dashboard. This is the number most relevant for sales conversations.

**Calculation**:
```
Scale Factor = Estimated Vehicles / Current Vehicles
Scaled Annual Savings = Savings at 25% × Scale Factor
```

If no estimated fleet size is set, this card shows the same value as Savings at 25% Reduction.

### Savings to Reach 10%

The projected **annual** savings if the fleet reduces its idling rate to the **10% industry benchmark** (top quartile). Also scaled to the estimated fleet size.

**Calculation**:
```
Savings to Reach 10% = Annual Idle Cost × (1 − 10 / Idling%)
Scaled Savings = Savings to Reach 10% × Scale Factor
```

This card only appears when the fleet's idling rate is **above 10%**. If the fleet is already at or below 10%, this card is replaced by a **Top Quartile Fleet** recognition card.

## Fleet Idling Benchmark

A reference strip at the bottom of the Idling Cost Overview shows where the fleet stands against established benchmarks:

| Tier | Idling Rate | Meaning |
|------|-------------|---------|
| **Top Quartile** | ≤ 10% | Best-in-class — fleet coaching is working |
| **Industry Average** | ~20% | Typical baseline for mixed-use commercial fleets |
| **Your Fleet** | Actual % | The fleet's measured idling rate for this period |

The **Your Fleet** indicator is colour-coded: green if at or below 10%, red if above 10%.

---

# Understanding the Calculations

## How Idling Cost is Calculated

The tool calculates idling cost per vehicle using the following logic:

1. **Fetch Trip Data**: For each vehicle, retrieve all trips in the analysis period using `Get<Trip>`
2. **Sum Idle Duration**: Add up the `idlingDuration` field from each trip
3. **Fetch Fuel Data**: Retrieve fuel consumption records using `Get<FuelAndEnergyUsed>`
4. **Calculate Fuel Used**:
   - If fuel records exist: Use `totalIdlingFuelUsedL` and `totalIdlingEnergyUsedKwh` from the records
   - If no fuel records: Estimate using `Idle Hours × Idle Rate`
5. **Calculate Cost**: Multiply fuel/energy by the configured price per unit

## How Annual Savings are Calculated

```
Period Days      = (End Date − Start Date) + 1
Annual Factor    = 365 / Period Days
Annual Idle Cost = Total Period Idle Cost × Annual Factor

Savings at 25%        = Annual Idle Cost × 0.25
Scale Factor          = max(1, Estimated Vehicles / Current Vehicles)
Scaled Annual Savings = Savings at 25% × Scale Factor

Idling% After 25% Reduction = Current Idling% × 0.75
Savings to Reach 10%  = Annual Idle Cost × (1 − 10 / Idling%)   [only when Idling% > 10]
Scaled Savings to 10% = Savings to Reach 10% × Scale Factor
```

**Example**: A 15-day analysis with 50 vehicles shows $1,500 in idle cost. The database has 100 total vehicles. Measured idling rate is 28.7%.
- Annual idle cost = $1,500 × (365 / 15) = $36,500
- Savings at 25% = $36,500 × 0.25 = $9,125 *(current 50 vehicles)*
- Scale factor = 100 / 50 = 2
- Scaled Annual Savings = $9,125 × 2 = $18,250 *(projected to 100 vehicles)*
- Idling % after 25% reduction = 28.7% × 0.75 = **21.5%**
- Savings to Reach 10% = $36,500 × (1 − 10 / 28.7) = $23,710 *(current 50 vehicles)*
- Scaled Savings to Reach 10% = $23,710 × 2 = $47,420 *(projected to 100 vehicles)*

## Idling Benchmark Reference

| Tier | Rate | Basis |
|------|------|-------|
| Top Quartile | ≤ 10% | Best-in-class fleets with active idling coaching programmes |
| Industry Average | ~20% | Standard baseline for regional delivery and mixed-use commercial fleets |

These benchmarks are directional references — exact figures vary by industry segment, region, and fleet type.

## Data Sources and Variance

The Idling ROI Tool pulls data directly from the MyGeotab API. You may notice small variances (typically 1–2%) when comparing to MyGeotab's built-in reports. This is expected due to:

1. **Trip Boundary Handling**: The tool's `Get<Trip>` API call may include slightly more boundary trips than pre-built MyGeotab reports
2. **Archived Devices**: The tool filters to currently active devices by default

These variances are proportional across all vehicles and do not significantly impact ROI projections.

---

# Troubleshooting

## Common Issues

### Tool does not appear in Reports menu after installation

**Cause**: The page was not refreshed after saving the add-in, or the add-in upload failed.

**Solution**: Go to **Administration → System → System Settings → Add-Ins**, verify the Idling ROI Tool entry is present, click Save, then do a hard refresh (Ctrl+Shift+R / Cmd+Shift+R).

### Dashboard shows "Total Devices: 0" or fleet summary is empty

**Cause**: The add-in bootstrap is still initialising, or no vehicles have a valid fuel type assignment.

**Solution**: Wait a few seconds for the fleet data to load. If the issue persists, check that vehicles are assigned to the correct Powertrain and Fuel Type groups in MyGeotab.

### "No vehicles with valid powertrain" error

**Cause**: None of your vehicles are assigned to a valid Powertrain and Fuel Type group in MyGeotab.

**Solution**: In MyGeotab, navigate to **Assets > Vehicles** and assign each vehicle to the appropriate group under the `Powertrain and Fuel Type` hierarchy.

### Report shows fewer vehicles than expected

**Cause**: Vehicles may be excluded due to:
- Missing fuel type assignment (shown in Unassigned Vehicles section)
- No trip activity in the analysis period (counted as "inactive")

**Solution**: Check the Unassigned Vehicles section and expand your analysis period if needed.

### Idle cost seems too high or too low

**Cause**: The default idle rates may not match your specific fleet.

**Solution**: Adjust the Idle Rate values in the Fuel Settings table on the dashboard before generating the report.

### How do I sign out?

The add-in uses your MyGeotab session — to sign out, log out from MyGeotab directly.

## Diagnostic CSV

For detailed data validation, click **Diagnostic CSV** in the report header. This downloads a CSV file containing per-vehicle breakdowns:

| Column | Description |
|--------|-------------|
| Vehicle Name | The device name in MyGeotab |
| Serial Number | The GO device serial number |
| Device ID | The MyGeotab device ID |
| Fuel | The resolved fuel type |
| Trip Count | Number of trips in the period |
| Fuel Records | Number of fuel consumption records |
| Driving Hours | Total driving time |
| Idling Hours | Total idling time |
| Idle Fuel (L) | Fuel consumed while idling |
| Idle Energy (kWh) | Energy consumed while idling |
| Note | Any flags (e.g., "no activity", "estimated") |

Use this file to:
- Cross-check totals against MyGeotab's Trips Detail Report
- Identify outlier vehicles with unusually high or low idling
- Diagnose data discrepancies reported by customers

---

*Last Updated: 26 May 2026*
*For feedback or issues, contact Revenue Generation International — SEA*
