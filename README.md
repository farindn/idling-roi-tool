# MyGeotab User Guide: Idling ROI Tool

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
  - Monthly Activity Trend
  - Trip Activity
  - Idling Cost Overview
  - Exporting the Report
- Understanding the Calculations
  - How Idling Cost is Calculated
  - How Annual Savings are Calculated
  - Data Sources and Variance
- Troubleshooting
  - Common Issues
  - Diagnostic CSV

---

# Introduction

The Idling ROI Tool is a web-based application that connects to your MyGeotab database to analyse vehicle idling behaviour and calculate the potential return on investment (ROI) from reducing idle time across your fleet.

This tool is designed for fleet managers and sales professionals to demonstrate the financial impact of idling and project potential savings from idling reduction initiatives.

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

https://farindn.github.io/idling-roi-tool/

No installation is required. The tool runs entirely in your web browser and connects directly to the MyGeotab API.

## Logging In

1. Open the tool URL in your browser.
2. Enter your MyGeotab credentials:
   - **Username**: Your MyGeotab email address
   - **Database**: The MyGeotab database name (e.g., `my_company_db`)
   - **Password**: Your MyGeotab password
3. Click **Sign In**.

The tool will authenticate with MyGeotab and load your fleet data. Your session will persist until you log out or close the browser.

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

**Note**: A hint below the date fields shows the calculated period length (e.g., "Analysis period: May 1, 2026 - May 15, 2026").

**Performance Note**: Longer analysis periods require more data to be fetched from MyGeotab and will take longer to load. For large fleets or multi-month periods, expect the report generation to take additional time.

## Currency & Fuel / Idling Settings

This section allows you to configure pricing and idle consumption rates:

### Currency

Select your preferred currency from the dropdown. The currency is auto-detected from your MyGeotab user profile but can be changed as needed. Supported currencies include USD, CAD, EUR, GBP, AUD, TWD, and others.

### Fuel Settings Table

The table displays the following columns for each fuel type present in your fleet:

| Column | Description | Editable |
|--------|-------------|----------|
| **Fuel Type** | The fuel/energy type (auto-detected from MyGeotab) | No (change in MyGeotab) |
| **Powertrain** | The powertrain category (ICE, Electric, Plug-in, Fuel Cell) | No (change in MyGeotab) |
| **Vehicles** | Number of vehicles with this fuel type | No (change in MyGeotab) |
| **Price / Unit** | The cost per unit of fuel (L, kWh, or kg) | Yes |
| **Idle Rate** | The estimated fuel/energy consumption rate while idling | Yes |

**Note**: Fuel Type, Powertrain, and Vehicle counts are read-only in this tool. To change a vehicle's fuel type or powertrain assignment, update the vehicle's group membership in MyGeotab.

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

**Important**: When actual fuel consumption data is available from `FuelAndEnergyUsed` records in MyGeotab, the tool uses the recorded values instead of the estimated idle rates. The idle rate setting is a fallback for vehicles without fuel telemetry. See the Fuel & Energy Consumed section below for details on how this works per vehicle.

---

# Report Page

After configuring your settings, click **Generate Idling ROI Report** to create the report. A loading overlay will appear while the tool fetches and processes your fleet data.

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

## Monthly Activity Trend

This chart shows driving and idling hours over time. The chart automatically adjusts its bucketing based on the analysis period:

| Period Length | Bucketing |
|---------------|-----------|
| 1-2 days | Daily |
| 3-56 days | Weekly |
| 57+ days | Monthly |

- **Green line**: Driving hours
- **Red line**: Idling hours

## Trip Activity

Three stat cards summarise driving and idling behaviour:

| Card | Description |
|------|-------------|
| **Total Driving Duration** | Total hours vehicles were in motion |
| **Total Idle Duration** | Total hours engines were running with speed = 0 |
| **Idling %** | Idle hours as a percentage of total engine-on time |

## Idling Cost Overview

Four stat cards show the financial analysis:

### Fuel & Energy Consumed

The total fuel (litres) and energy (kWh) consumed while idling across your fleet.

**Per-Vehicle Calculation Logic:**

For each vehicle, the tool checks whether actual fuel telemetry is available:

1. **If `FuelAndEnergyUsed` records exist**: The tool uses the actual `TotalIdlingFuelUsedL` and `TotalIdlingEnergyUsedKwh` values from MyGeotab. This provides the most accurate measurement.

2. **If no fuel records exist**: The tool estimates consumption using `Idle Hours × Idle Rate` based on the vehicle's fuel type settings.

**Mixed Fleet Handling:**

In databases where some vehicles have fuel telemetry and others do not, the tool applies the appropriate method per vehicle:
- Vehicles with telemetry use actual consumption data
- Vehicles without telemetry use estimated consumption based on idle rates

The fleet totals shown in the report are the sum of all per-vehicle calculations, regardless of which method was used for each vehicle.

### Total Idle Cost

The cost of fuel/energy consumed during idling for the analysis period.

**Calculation**: `Idle Fuel (L) × Fuel Price ($/L)` or `Idle Energy (kWh) × Electricity Price ($/kWh)`

The sub-text shows the period length (e.g., "15-day period at configured prices").

### Savings at 25% Reduction

The projected **annual** savings if idling is reduced by 25%.

**Calculation**:
```
Annual Idle Cost = Period Idle Cost × (365 / Period Days)
Annual Savings = Annual Idle Cost × 0.25
```

The sub-text confirms this is annualized (e.g., "Annually based on 59 current vehicles").

### Scaled Annual Savings

If you entered an **Estimated Total Vehicles** value greater than your current fleet size, this card shows the projected savings scaled to that larger fleet.

**Calculation**:
```
Scale Factor = Estimated Vehicles / Current Vehicles
Scaled Savings = Annual Savings × Scale Factor
```

---

# Understanding the Calculations

## How Idling Cost is Calculated

The tool calculates idling cost per vehicle using the following logic:

1. **Fetch Trip Data**: For each vehicle, retrieve all trips in the analysis period using `Get<Trip>`
2. **Sum Idle Duration**: Add up the `idlingDuration` field from each trip
3. **Fetch Fuel Data**: Retrieve fuel consumption records using `Get<FuelAndEnergyUsed>`
4. **Calculate Fuel Used**:
   - If fuel records exist: Use `TotalIdlingFuelUsedL` and `TotalIdlingEnergyUsedKwh` from the records
   - If no fuel records: Estimate using `Idle Hours × Idle Rate`
5. **Calculate Cost**: Multiply fuel/energy by the configured price per unit

## How Annual Savings are Calculated

The tool annualizes the savings based on the analysis period length:

```
Period Days = (End Date - Start Date) + 1
Annualization Factor = 365 / Period Days
Annual Idle Cost = Total Period Idle Cost × Annualization Factor
Annual Savings at 25% = Annual Idle Cost × 0.25
```

**Example**: If a 15-day analysis shows $1,500 in idle cost:
- Annual idle cost = $1,500 × (365 / 15) = $36,500
- Annual savings at 25% = $36,500 × 0.25 = $9,125

## Data Sources and Variance

The Idling ROI Tool pulls data directly from the MyGeotab API. You may notice small variances (typically 1-2%) when comparing to MyGeotab's built-in reports. This is expected due to:

1. **Trip Boundary Handling**: The tool's `Get<Trip>` API call may include slightly more boundary trips than pre-built MyGeotab reports
2. **Archived Devices**: The tool filters to currently active devices by default

These variances are proportional across all vehicles and do not significantly impact ROI projections.

---

# Troubleshooting

## Common Issues

### "No vehicles with valid powertrain" error

**Cause**: None of your vehicles are assigned to a valid Powertrain and Fuel Type group in MyGeotab.

**Solution**: In MyGeotab, navigate to **Assets** > **Vehicles** and assign each vehicle to the appropriate group under the `Powertrain and Fuel Type` hierarchy.

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

**Solution**: Click "Sign In" to re-authenticate with your MyGeotab credentials.

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
| Note | Any flags (e.g., "no activity") |

Use this file to:
- Cross-check totals against MyGeotab's Trips Detail Report
- Identify outlier vehicles with unusually high or low idling
- Diagnose data discrepancies reported by customers

---

*Last Updated: May 2026*
