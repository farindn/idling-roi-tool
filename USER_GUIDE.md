# User Guide — Idling ROI Tool (Web Version)

**Version:** 1.0.0

**Table of contents**

- Introduction
  - Document Disclaimer
  - Prerequisites
- Getting Started
  - Accessing the Tool
  - Logging In
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
  - Saving Opportunity Overview
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

The Idling ROI Tool is a web-based application that connects to your MyGeotab database to analyse vehicle idling behaviour and calculate the potential return on investment (ROI) from reducing idle time across your fleet.

This tool is designed for fleet managers and sales professionals to demonstrate the financial impact of idling and project potential savings from idling reduction initiatives.

For the MyGeotab add-in version (no login required, installed directly into MyGeotab), see [USER_GUIDE_ADDIN.md](USER_GUIDE_ADDIN.md).

## Document Disclaimer

This document's content, including specifications, procedures, and screenshots, is subject to review and revision. We may make changes, updates, or modifications to product features, specifications, procedures, or the visual presentation without prior notice. Users should consult the current guide version for the most accurate information.

## Prerequisites

**IMPORTANT**: To use the Idling ROI Tool, you must have:

- **MyGeotab Account**
  - A valid MyGeotab username and password
  - Access to the database you want to analyse

- **Powertrain & Fuel Type Configuration**
  - Vehicles must be assigned to the correct Powertrain and Fuel Type groups in MyGeotab
  - Vehicles without valid fuel type assignments will be excluded from calculations
  - Valid fuel types include: Gasoline/Petrol, Diesel, BEV, PHEV, FCEV, Biodiesel, Ethanol, CNG, and LPG

- **Trip Data**
  - The selected analysis period must contain trip data for accurate calculations
  - Vehicles with no trips or fuel records in the period will be flagged as "inactive"

---

# Getting Started

## Accessing the Tool

The Idling ROI Tool is available at:

**https://farindn.github.io/idling-roi-tool/**

No installation is required. The tool runs entirely in your web browser and connects directly to the MyGeotab API.

## Logging In

1. Open the tool URL in your browser.
2. Click **Sign In** on the landing screen.
3. Enter your MyGeotab credentials in the login modal:
   - **Username**: Your MyGeotab email address
   - **Database**: The MyGeotab database name (e.g., `my_company_db`)
   - **Password**: Your MyGeotab password
4. Click **Sign In**.

The tool will authenticate with MyGeotab and load your fleet data. Your session will persist until you log out or close the browser.

To sign out, click the user avatar in the top-right corner of the navbar and select **Sign Out**.

---

# Dashboard Page

After logging in, you will see the **Idling ROI Analysis** dashboard. This page allows you to configure the report parameters before generating your Idling ROI Report.

## Fleet Summary

The Fleet Summary section displays:

- **Total Devices**: The total number of vehicles in your database with a valid powertrain/fuel type assignment
- **Fuel Type Breakdown**: Cards showing the count of vehicles by fuel type (e.g., Gasoline, Diesel, BEV)

Vehicles are auto-resolved from the `GroupPowertrainAndFuelTypeId` hierarchy in MyGeotab. The tool walks each device's group ancestry to determine the correct fuel type.

## Unassigned Vehicles

If any vehicles in your database have an invalid or missing fuel type assignment, they will appear in the **Unassigned Vehicles** section with a warning banner.

These vehicles are **excluded** from cost calculations until their powertrain/fuel type is corrected in MyGeotab.

For each unassigned vehicle, you can click **Edit in MyGeotab** to open the device settings page and assign the correct group.

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

**Performance Note**: Longer analysis periods require more data to be fetched from MyGeotab and will take longer to load. For large fleets or multi-month periods, expect the report generation to take additional time.

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

The following export option is available in the header:

| Button | Description |
|--------|-------------|
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

This section establishes the baseline — **how much the fleet is currently spending on idling**. It is laid out as a 2×2 matrix so you can read across time and across fleet size at a glance:

|  | Selected Period | Annual |
|--|-----------------|--------|
| **Existing Fleet** | Total Idle Cost for the analysis period | Same cost extrapolated to 12 months |
| **Projected Fleet** | Period cost scaled to your estimated fleet | Annual cost scaled to your estimated fleet |

- **Existing Fleet** — the vehicles with valid data in the current analysis. The vehicle count is shown on the row label.
- **Projected Fleet** — the same figures scaled up to the **Estimated Total Vehicles** value from the dashboard. These rows only appear when you set an estimated fleet size larger than the current fleet.

**Calculation**: `Idle Fuel (L) × Fuel Price` or `Idle Energy (kWh) × Electricity Price`, summed across all vehicles. The Annual column multiplies the period figure by `365 ÷ period days`.

Each card carries a sub-line describing its basis, for example:
- "15-day period at configured prices"
- "15-day period extrapolated to 12 months"
- "Scaled from 59 to 100 vehicles"

### Fleet Idling Benchmark

A reference strip below the cost matrix shows where the fleet stands against established benchmarks:

| Tier | Idling Rate | Meaning |
|------|-------------|---------|
| **Top Quartile** | ≤ 10% | Best-in-class — fleet coaching is working |
| **Industry Average** | ~20% | Typical baseline for mixed-use commercial fleets |
| **Your Fleet** | Actual % | The fleet's measured idling rate for this period |

The **Your Fleet** indicator is colour-coded: green if at or below 10%, red if above 10%.

## Saving Opportunity Overview

This section presents the opportunity — **how much the fleet can save by reducing idling by 25%**. It uses the same 2×2 matrix layout:

|  | Selected Period | Annual |
|--|-----------------|--------|
| **Existing Fleet** | Saving at 25% reduction for the period | Annual saving at 25% reduction |
| **Projected Fleet** | Period saving scaled to your estimated fleet | Annual saving scaled to your estimated fleet |

**Calculation**: `Idle Cost × 0.25`. The 25% applies to the idling ratio itself — a fleet currently idling at 28.7% would drop to 21.5% (28.7 × 0.75).

Each savings card's sub-line shows the basis plus the resulting idling-rate change, for example:
- "15-day period at configured prices" / "28.7% → 21.5%"
- "Scaled from 59 to 100 vehicles" / "28.7% → 21.5%"

### Stretch Goal — Reach the 10% Benchmark

Below the savings matrix, a highlighted strip shows the aspirational target:

- **If the fleet idles above 10%**: it shows the additional annual saving available by cutting idling all the way to the 10% top-quartile benchmark — e.g. "Stretch goal — cut idling from 28.7% to the 10% benchmark to save USD 23,710 annually fleet-wide."
- **If the fleet already idles at or below 10%**: it shows a **Top Quartile Fleet** recognition message instead.

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

### Session expired error

**Cause**: Your MyGeotab session has timed out.

**Solution**: Click **Sign In** to re-authenticate with your MyGeotab credentials. The tool will automatically retry the last action after re-authentication.

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

*Version 1.0.0 — Last Updated: 24 June 2026*
