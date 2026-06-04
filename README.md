# Idling ROI Tool

A browser-based tool that connects to a MyGeotab database to analyse vehicle idling behaviour and calculate the financial impact of reducing idle time across a fleet.

Built for fleet managers and sales professionals to quantify and present idling ROI — no installation required.

Available in two forms:
- **Web version** — hosted on GitHub Pages, requires manual login
- **Add-in version** — installed into MyGeotab via ZIP, credentials passed automatically

---

## Project Structure

```
idling-roi-tool/
├── index.html                        # Web version — single-file app, no build step
├── addin/
│   ├── index.html                    # Add-in version — same app, no login screen,
│   │                                 #   add-in bootstrap, external CSS/fonts
│   ├── icon.svg                      # Speedometer SVG used as add-in icon
│   ├── build_zip.py                  # Build script — downloads assets, patches HTML,
│   │                                 #   bundles into MyGeotab ZIP format
│   └── releases/
│       └── idling-roi-tool.zip       # Pre-built add-in ZIP (committed to git)
├── geotab-logo(full-colour-rgb).png  # Geotab logo used in report footer
├── USER_GUIDE.md                     # End-user guide — web version
├── USER_GUIDE_ADDIN.md               # End-user guide — add-in version
└── README.md                         # This file
```

---

## Architecture

### Single-File HTML Application

Both versions are vanilla JavaScript with no framework and no bundler. All logic lives in a single `<script>` block inside `index.html`. The web version loads IBM Plex Sans/Mono and Material Symbols from Google Fonts CDN and Chart.js from jsDelivr CDN. The add-in version bundles all assets locally (see Build Process below).

The UI is a multi-screen single-page app driven by `showScreen(name)`:

| Screen | ID | Purpose |
|--------|----|---------|
| Login | `screen-login` | Credential entry (web version only) |
| Dashboard | `screen-dashboard` | Fleet summary, settings, generate button |
| Generating | `screen-generating` | Progress steps while data is fetched |
| Report | `screen-report` | Rendered report with charts and export actions |

Screen transitions call `renderReport()` and `renderCharts()` when switching to the report screen.

---

### Key Global State

| Variable | Type | Purpose |
|----------|------|---------|
| `api.session` | Object | Active session: `userName`, `database`, `sessionId`, `serverPath`, `password`, `timeZoneId`, `displayCurrency` |
| `configuredVehicles` | Array | All devices with resolved fuel type — populated by `loadDashboardFromApi()` |
| `groupAncestryMap` | Object | Precomputed map of groupId → Set of ancestor groupIds — built by `buildGroupAncestryMap()` |
| `reportData` | Object | Output of `computeReport()` — drives all report rendering |
| `fleetLoaded` | Boolean | Guard to prevent `loadDashboardFromApi()` from refetching on repeated dashboard visits |

---

### MyGeotab API Layer

The `api` object (`index.html:2020`) wraps all MyGeotab JSON-RPC calls to `https://{serverPath}.geotab.com/apiv1`.

**`api.call(method, params)`** — single authenticated POST. Injects `credentials: { sessionId, userName, database }` automatically from `api.session`. Throws `ApiError` on non-2xx or JSON error response.

**`api.callWithRetry(method, params, retries=3)`** — wraps `api.call` with:
- Session expiry re-authentication (re-calls `api.authenticate` and retries)
- Rate limit backoff (`OverLimitException` → exponential backoff: 1s, 2s, 4s)

**`api.authenticate({ userName, database, password })`** — calls `Authenticate`, stores the returned session and server path into `api.session`.

**Pagination** — `apiPaginate(method, params)` is an async generator that pages through results using `resultsLimit: 5000` and advancing by record offset until an empty page is returned.

**Add-in override** — in `addin/index.html`, `api.call` is replaced at bootstrap time with a Promise wrapper around `addinApi.call(method, params, successCb, errorCb)`. All existing `await api.call()` / `callWithRetry` code continues to work unchanged.

---

### API Calls Made

| Call | When | Key Params |
|------|------|-----------|
| `Authenticate` | Login (web only) | `userName`, `database`, `password` |
| `Get<User>` | Post-login / add-in bootstrap | `search: { name: userName }`, `resultsLimit: 1` — reads `timeZoneId`, `displayCurrency` |
| `Get<Device>` | Dashboard load + report generation | `search: { fromDate: now }` — returns only active (non-archived) devices |
| `Get<DeviceStatusInfo>` | Dashboard load + report generation | No search filter — provides each device's last-contact timestamp via `dateTime` |
| `Get<Group>` | Dashboard load + report generation | No search filter — returns all groups for ancestry walk |
| `Get<Trip>` | Report generation, per device | `search: { fromDate, toDate, deviceSearch: { id } }`, `resultsLimit: 10000` — batched 50 devices at a time |
| `Get<FuelAndEnergyUsed>` | Report generation, per device | `search: { fromDate, toDate, deviceSearch: { id } }`, `resultsLimit: 10000` — batched 50 devices at a time |
| `Logout` | Sign out (web only) | No params |

Dates passed to Trip and FuelAndEnergyUsed are converted to UTC boundary timestamps by `getDateInUTC(dateStr, timeZoneId, endOfDay)` — start of day at `00:00:00Z`, end of day at `23:59:59.999Z`, shifted by the user's MyGeotab timezone offset.

---

### Powertrain Resolution

MyGeotab organises powertrain/fuel type as a group hierarchy under `GroupPowertrainAndFuelTypeId`. Devices are members of leaf groups (e.g. `GroupDieselId`). The tool resolves fuel type via a two-step process:

**Step 1 — Build ancestry map** (`buildGroupAncestryMap`, `index.html:2393`)

Recursively walks each group's `parent.id` chain and caches the result:
```
groupAncestryMap[groupId] = Set { groupId, parentId, grandparentId, ... }
```

**Step 2 — Resolve per device** (`resolveFuelType`, `index.html:2417`)

For each device, iterates over its `groups[]`, expands each to ancestors via the map, and checks against `POWERTRAIN_GROUP_MAP`:

```javascript
const POWERTRAIN_GROUP_MAP = {
  'GroupBatteryElectricVehicleId':         'BEV',
  'GroupPluginHybridElectricVehicleId':    'PHEV',
  'GroupFuelCellElectricVehicleId':        'FCEV',
  'GroupGasolinePetrolId':                 'Petrol',
  'GroupDieselId':                         'Diesel',
  'GroupBiodieselId':                      'Biodiesel',
  'GroupEthanolId':                        'Ethanol',
  'GroupCompressedNaturalGasId':           'CNG',
  'GroupPropaneLiquifiedPetroleumGasId':   'LPG',
  'GroupManuallyClassifiedPowertrainId':   'Manual',
  'GroupOtherFuelId':                      'OtherFuel'
}
```

A device with both `Manual` and a valid fuel type (common when powertrain was manually set in MyGeotab) is resolved to the valid fuel type — `Manual` is filtered out in favour of the specific fuel.

Devices that resolve to `None`, `Manual`, or `OtherFuel` are stored in `INVALID_FUEL_TYPES` and excluded from cost calculations; they appear in the Unassigned Vehicles section.

---

### Report Calculation Engine

`computeReport(devices, trips, fuelRecords, settings)` (`index.html:2650`) accepts:
- `devices` — filtered `configuredVehicles` (valid fuel types only)
- `trips` — all `Get<Trip>` results for the period
- `fuelRecords` — all `Get<FuelAndEnergyUsed>` results for the period
- `settings` — from `getSelectedSettings()`: dates, currency, per-fuel price and idle rate

**Per-vehicle calculation:**

1. Sum `idlingDuration` (ISO 8601 duration string) across all trips for the device via `parseDuration()`
2. Look up `FuelAndEnergyUsed` records for the device
3. **If fuel records exist**: use `totalIdlingFuelUsedL` + `totalIdlingEnergyUsedKwh` from the records
4. **If no fuel records**: estimate as `idleHours × idleRate` from settings
5. Multiply fuel/energy by configured price per unit → idle cost

**Fleet-level aggregation:**

```
periodDays            = (endDate − startDate) + 1
annualFactor          = 365 / periodDays
annualIdleCost        = totalIdleCost × annualFactor
savings25Period       = totalIdleCost × 0.25
savings25             = annualIdleCost × 0.25
scaleFactor           = max(1, estimatedVehicles / activeVehicles)
scaledTotalIdleCost   = totalIdleCost × scaleFactor
scaledAnnualIdleCost  = annualIdleCost × scaleFactor
scaledSavings25Period = savings25Period × scaleFactor
scaledSavings25       = savings25 × scaleFactor
idlingPct             = totalIdleHours / (totalDrivingHours + totalIdleHours) × 100
idealSavings          = annualIdleCost × (1 − 10 / idlingPct)   [only when idlingPct > 10]
scaledIdealSavings    = idealSavings × scaleFactor
```

Both the selected-period and annualised figures are computed (and, when an estimated fleet size is set, their scaled variants) so the report can show them side by side without recomputation.

**Report layout** — the financial results render as two sections, each a 2×2 matrix (rows: Existing Fleet / Projected Fleet; columns: Selected period / Annual):

| Section | Cards | Strip below |
|---------|-------|-------------|
| **Idling Cost Overview** (baseline) | Total Idle Cost + Scaled Total Idle Cost, each period & annual | Fleet Idling Benchmark |
| **Saving Opportunity Overview** (25% reduction) | Saving at 25% + Scaled Saving at 25%, each period & annual | Stretch goal — reach the 10% benchmark, or Top Quartile recognition |

The Projected Fleet rows are hidden when no estimated fleet size is set (`scaleFactor <= 1`). Each card carries a `stat-card-sub` line built in `renderReport` that states the calculation basis (period length, price basis, scaling, and the idling-rate change for savings cards).

**Chart bucketing** (`renderCharts`, `index.html:3574`):

| Period length | Bucket | Label format |
|---------------|--------|-------------|
| 1–14 days | Daily | `D MMM` |
| 15–90 days | Weekly | `Week N - Mon YYYY` (keyed to Monday of the week) |
| 91+ days | Monthly | `Mon YYYY` |

---

### FUEL_TYPES Registry

`FUEL_TYPES` (`index.html:1964`) is the single source of truth for fuel metadata:

```javascript
FUEL_TYPES[key] = {
  label:      string,   // display name, e.g. "Diesel"
  powertrain: string,   // "ICE" | "Electric" | "Plug-in" | "Fuel Cell"
  unit:       string,   // "L" | "kWh" | "kg" | "kWh+L" (PHEV dual)
  idleRate:   number,   // default idle consumption rate
  badge:      string    // CSS class for the fuel badge chip
}
```

Default idle rates (EPA/DOE/industry estimates):

| Fuel | Default rate | Source |
|------|-------------|--------|
| Petrol | 0.6 L/hr | EPA/DOE Fact #861 |
| Diesel | 3.0 L/hr | Argonne/DOE heavy-duty data |
| BEV | 3.0 kWh/hr | DOE Vehicle Technologies Office |
| PHEV | 1.5 kWh/hr + 0.3 L/hr | Combined estimate |
| FCEV | 0.3 kg/hr | Industry estimate |
| Biodiesel / Ethanol / CNG / LPG | ~1.5 L/hr or similar | Industry estimates |

---

### CSS / Design System

The tool uses a custom design system called "Arkivleet" defined in CSS custom properties at `:root`. Key tokens:

| Token group | Examples |
|------------|---------|
| Colors | `--color-primary: #25457B`, `--color-accent: #00B8FF`, `--color-error: #FE4A3F` |
| Typography | `--font-sans: 'IBM Plex Sans'`, `--font-mono: 'IBM Plex Mono'` |
| Spacing | `--space-3` (0.25rem) through `--space-15` (3rem) |
| Radii | `--radius-xs`, `--radius-sm`, `--radius-md`, `--radius-full` |
| Shadows | `--shadow-sm`, `--shadow-md`, `--shadow-lg` |

Key component classes: `.ig` (input group wrapper), `.if` (input field with icon + unit), `.if-sm` (compact input), `.fbadge` (fuel type chip), `.stat-card`, `.gen-overlay` (generating spinner overlay), `.notif-overlay` (notification modal overlay).

---

## Add-In Version

`addin/index.html` is a modified copy of the web `index.html` with these differences:

| Aspect | Web version | Add-in version |
|--------|-------------|----------------|
| Login screen | Present | Removed |
| Authentication | User enters credentials | MyGeotab passes session via `addinApi` |
| Initial screen | `screen-login` | `screen-dashboard` |
| CSS loading | Inline `<style>` block | External `main.css` (CSP requirement) |
| Fonts | Google Fonts CDN | Bundled woff2 files |
| Chart.js | jsDelivr CDN | Bundled `chart.js` |
| Sign-out | Dropdown with logout button | Removed |
| `api.call` | `fetch` to MyGeotab JSON-RPC | Promise wrapper around `addinApi.call` |
| Root container | `<body>` | `<div id="Idling ROI Tool">` (required by MyGeotab) |
| Modal scoping | `position: fixed` vs viewport | `transform: translateZ(0)` on root — scopes fixed children |

### Add-In Registration

The registration name in `geotab.addin["Idling ROI Tool"]` must exactly match the `"name"` field in `configuration.json`. MyGeotab uses this string as the lookup key to call `initialize()`.

### Add-In Bootstrap (`_bootAddin`)

```javascript
geotab.addin["Idling ROI Tool"] = function() {
  return {
    initialize(addinApi, state, callback) {
      // 1. Override api.call to use addinApi's pre-authenticated session
      api.call = (method, params) =>
        new Promise((resolve, reject) =>
          addinApi.call(method, params, resolve, reject));

      // 2. Derive database from state.database or URL path
      api.session = { database, sessionId: 'addin', serverPath: 'my', ... };

      // 3. Try addinApi.getSession() for actual logged-in user's name
      // 4. Follow up with Get<User> for timeZoneId + displayCurrency
      // 5. Call _bootAddin() then callback()
    },
    focus(addinApi, state) { show root div },
    blur()               { hide root div }
  };
};
```

`sessionId: 'addin'` is a truthy sentinel — the real auth is managed by MyGeotab. The guard `if (!api.session?.sessionId) return` in `loadDashboardFromApi()` needs a truthy value to proceed.

### Add-In CSP Constraints

MyGeotab's add-in context enforces a Content Security Policy that:
- **Blocks** inline `<style>` tags — CSS must be in an external file linked via `<link rel="stylesheet">`
- **Blocks** Google Fonts and jsDelivr CDN requests — all fonts and libraries must be bundled locally
- **Allows** `<script src="...">` from local relative paths

---

## Add-In Build Process

`addin/build_zip.py` (run from the `addin/` directory):

```
python build_zip.py
```

Steps performed:
1. Reads `addin/icon.svg` → base64 encodes it for `configuration.json`
2. Downloads `Chart.js` from jsDelivr (~200 KB)
3. Downloads Material Symbols CSS from Google Fonts → extracts the woff2 URL → downloads the woff2 (~359 KB)
4. Downloads IBM Plex Sans/Mono CSS from Google Fonts → extracts all woff2 URLs → downloads each (~414 KB, 22 files)
5. Reads `addin/index.html` and patches it via `patch_html()`:
   - Strips `<link rel="preconnect">` hints
   - Strips Google Fonts `<link>` tags
   - Replaces CDN Chart.js `<script>` with `<script src="chart.js">`
   - Extracts the inline `<style>` block → stores as `css_out`, replaces with `<link rel="stylesheet" href="main.css">`
6. Appends IBM Plex and Material Symbols `@font-face` CSS to `css_out` → written as `main.css`
7. Assembles ZIP:

```
configuration.json
Idling ROI Tool/
  index.html
  main.css
  chart.js
  material-symbols-rounded.woff2
  ibm-plex-0.woff2 … ibm-plex-21.woff2
  geotab-logo(full-colour-rgb).png
```

**Critical ordering in `patch_html()`**: The `re.search` for the `<style>` block must run *after* all `re.sub` calls that modify the HTML string — otherwise the saved match positions become stale and the splice will be applied to the wrong character positions.

---

## Features

| Feature | Description |
|---------|-------------|
| Powertrain auto-detection | Resolves fuel type from MyGeotab group hierarchy — no manual tagging |
| Fuel & energy telemetry | Uses `FuelAndEnergyUsed.totalIdlingFuelUsedL/totalIdlingEnergyUsedKwh` when available; falls back to idle rate estimate |
| Multi-powertrain support | ICE Petrol, ICE Diesel, BEV, PHEV, FCEV, Biodiesel, Ethanol, CNG, LPG |
| Activity trend chart | Stacked bar (driving vs idle) auto-bucketed daily / weekly / monthly |
| Fleet savings scenarios | 25% reduction and "reach 10% benchmark" — annualised and scaled to estimated fleet |
| Fleet benchmark strip | Positions the fleet against 10% (top quartile) and ~20% (industry average) |
| Fleet scaling | Projects savings to an estimated total fleet size |
| Export: Print as PDF | Browser print dialog |
| Export: Download HTML | Standalone report HTML file |
| Export: Diagnostic CSV | Per-vehicle breakdown for cross-checking against MyGeotab reports |
| Currency detection | Auto-detected from user's MyGeotab `displayCurrency` preference |
| Unassigned vehicles | Lists devices with missing/invalid fuel type with direct link to edit in MyGeotab |

---

## Known Limitations

- **Trip boundary variance** — `Get<Trip>` may include slightly more boundary trips than MyGeotab's built-in reports, resulting in ~1–2% variance. Use Diagnostic CSV to investigate.
- **PHEV telemetry** — MyGeotab does not split PHEV fuel consumption into electric and combustion components. The tool uses a combined idle rate estimate for PHEVs without telemetry.
- **Rate limiting** — large fleets or long periods generate many per-device API calls and can hit `OverLimitException`. The `callWithRetry` layer handles this with exponential backoff, but very large fleets will be slow.
- **Idle rate fallback** — configured idle rates are only used for vehicles without `FuelAndEnergyUsed` telemetry. Vehicles with telemetry always use recorded values.

---

## Development Notes

- The standalone `index.html` is the source of truth. Never edit `addin/index.html` directly without also checking whether the same change needs to propagate — or whether it should only live in the add-in.
- After editing `addin/index.html`, always run `python build_zip.py` and commit the new ZIP alongside the source so partners can download it directly from GitHub.
- The add-in version does not have a login screen — any changes touching `showLoginModal`, `api.authenticate`, or `bootstrapSession` in the web version will not apply to the add-in.
- Chart.js is pinned to `4.4.0` in `build_zip.py` and in the `<script>` tag of `index.html`. Keep these in sync.

---

*For feedback or issues, contact Revenue Generation International — SEA*
