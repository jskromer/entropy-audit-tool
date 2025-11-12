# EnergyPlus MCP Server Integration Guide

## Overview

This guide shows how to use the [EnergyPlus MCP Server](https://github.com/jskromer/energyplus-mcp) to generate baseline predictions and calculate entropy scores for the Entropy Audit Tool.

---

## Prerequisites

### 1. Install EnergyPlus MCP Server

Follow the installation instructions at https://github.com/jskromer/energyplus-mcp

**Quick Start (Docker)**:
```bash
# Clone the repository
git clone https://github.com/jskromer/energyplus-mcp.git
cd energyplus-mcp

# Build Docker image
docker build -t energyplus-mcp .

# Run the server
docker run -p 8000:8000 -v $(pwd)/examples:/workspace energyplus-mcp
```

### 2. Prepare Your Baseline Model

You need:
- **IDF File**: EnergyPlus building model (.idf)
- **Weather File**: EPW file matching your location (.epw)
- **Utility Data**: Actual measured energy consumption (CSV/Excel)

---

## Workflow: From EnergyPlus to Entropy Score

### Step 1: Load and Validate Baseline Model

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Connect to MCP server
server_params = StdioServerParameters(
    command="docker",
    args=["run", "-i", "energyplus-mcp"]
)

async with stdio_client(server_params) as (read, write):
    async with ClientSession(read, write) as session:
        # Initialize
        await session.initialize()

        # Load baseline IDF
        result = await session.call_tool(
            "load_idf_file",
            arguments={"file_path": "/workspace/baseline_2023.idf"}
        )
        print("✅ Baseline model loaded")

        # Validate model
        validation = await session.call_tool(
            "validate_idf_file",
            arguments={}
        )
        print(f"Validation: {validation}")
```

### Step 2: Inspect Model Components

```python
# Get building zones
zones = await session.call_tool("list_zones", arguments={})
print(f"Zones: {zones}")

# Get HVAC topology
hvac = await session.call_tool("get_hvac_topology", arguments={})
print(f"HVAC Systems: {hvac}")

# Get schedules
schedules = await session.call_tool("list_schedules", arguments={})
print(f"Schedules: {schedules}")
```

**Output Example**:
```json
{
  "zones": [
    {"name": "Floor1_Office", "area": 5000, "volume": 45000},
    {"name": "Floor2_Office", "area": 5000, "volume": 45000},
    {"name": "Floor3_Office", "area": 5000, "volume": 45000}
  ],
  "hvac": {
    "chiller": "WaterCooled_500Ton",
    "air_handlers": ["AHU1", "AHU2", "AHU3"],
    "vav_boxes": 24
  }
}
```

### Step 3: Run Baseline Simulation

```python
# Run simulation with actual weather
result = await session.call_tool(
    "run_simulation",
    arguments={
        "weather_file": "/workspace/actual_2024.epw",
        "output_directory": "/workspace/outputs",
        "run_period": {
            "begin_month": 1,
            "begin_day": 1,
            "end_month": 12,
            "end_day": 31
        }
    }
)

print(f"Simulation status: {result['status']}")
print(f"Errors: {result['errors']}")
print(f"Warnings: {result['warnings']}")
```

### Step 4: Extract Baseline Predictions

```python
# Get electricity consumption (baseline prediction)
baseline_data = await session.call_tool(
    "get_meter_data",
    arguments={
        "meter_name": "Electricity:Facility",
        "reporting_frequency": "Monthly"
    }
)

# Example output
baseline_kwh = {
    "Jan": 125000,
    "Feb": 110000,
    "Mar": 95000,
    "Apr": 85000,
    "May": 90000,
    "Jun": 110000,
    "Jul": 130000,
    "Aug": 135000,
    "Sep": 115000,
    "Oct": 95000,
    "Nov": 105000,
    "Dec": 120000
}
```

### Step 5: Compare to Measured Data

```python
import pandas as pd

# Load actual utility bills
measured_data = pd.read_csv("utility_bills_2024.csv")

# Calculate deviations
deviations = {}
for month in baseline_kwh.keys():
    baseline = baseline_kwh[month]
    measured = measured_data[measured_data['month'] == month]['kwh'].values[0]

    deviation_pct = ((measured - baseline) / baseline) * 100
    deviations[month] = {
        "baseline_kwh": baseline,
        "measured_kwh": measured,
        "deviation_pct": deviation_pct,
        "deviation_kwh": measured - baseline
    }

# Summary statistics
avg_deviation = sum(d['deviation_pct'] for d in deviations.values()) / 12
max_deviation = max(d['deviation_pct'] for d in deviations.values())

print(f"Average deviation: {avg_deviation:.1f}%")
print(f"Maximum deviation: {max_deviation:.1f}%")
```

**Example Output**:
```
Average deviation: 12.3%
Maximum deviation: 18.5% (August)
```

### Step 6: Map Deviations to Entropy Factors

```python
def calculate_entropy_factors(deviations, model_age_months, occupancy_change_pct):
    """
    Map observed deviations to entropy factor noise levels (0-100)
    """
    entropy_factors = {}

    # 1. Energy Drift (Operational category, 8% weight)
    avg_drift = sum(d['deviation_pct'] for d in deviations.values()) / 12
    if avg_drift > 0:
        # Positive drift suggests efficiency loss
        energy_drift_noise = min(abs(avg_drift) * 5, 100)  # Scale to 0-100
        entropy_factors['Operational-Energy-Drift'] = energy_drift_noise

    # 2. Calibration Staleness (Model category, 8% weight)
    # Assume 1% per month of staleness
    calibration_noise = min(model_age_months, 100)
    entropy_factors['Model-Calibration-Staleness'] = calibration_noise

    # 3. Occupancy Changes (System category, 6% weight)
    if occupancy_change_pct > 0:
        occupancy_noise = min(occupancy_change_pct, 100)
        entropy_factors['System-Occupancy-Changes'] = occupancy_noise

    # 4. Equipment Degradation (Operational category, 6% weight)
    # Infer from peak month deviations
    max_drift = max(d['deviation_pct'] for d in deviations.values())
    if max_drift > 10:
        equipment_noise = min((max_drift - 10) * 3, 100)
        entropy_factors['Operational-Equipment-Degradation'] = equipment_noise

    # 5. Measurement factors (if data quality issues detected)
    missing_data_pct = 5  # Example: 5% of data missing
    entropy_factors['Measurement-Data-Completeness'] = missing_data_pct

    return entropy_factors

# Example usage
entropy_factors = calculate_entropy_factors(
    deviations=deviations,
    model_age_months=18,  # Model is 18 months old
    occupancy_change_pct=25  # 25% reduction in occupancy
)

print("Entropy Factor Contributions:")
for factor, noise in entropy_factors.items():
    print(f"  {factor}: {noise}% noise")
```

**Output**:
```
Entropy Factor Contributions:
  Operational-Energy-Drift: 61% noise → 4.88 points
  Model-Calibration-Staleness: 18% noise → 1.44 points
  System-Occupancy-Changes: 25% noise → 1.50 points
  Operational-Equipment-Degradation: 25% noise → 1.50 points
  Measurement-Data-Completeness: 5% noise → 0.50 points
```

### Step 7: Calculate Total Entropy Score

```python
# Load factor weights from the dashboard
factor_weights = {
    'Operational-Energy-Drift': 0.08,
    'Model-Calibration-Staleness': 0.08,
    'System-Occupancy-Changes': 0.06,
    'Operational-Equipment-Degradation': 0.06,
    'Measurement-Data-Completeness': 0.10
}

def calculate_entropy_score(entropy_factors, factor_weights):
    """
    Calculate weighted entropy score (0-100)
    """
    total_entropy = 0

    for factor_id, noise_pct in entropy_factors.items():
        weight = factor_weights.get(factor_id, 0)
        contribution = (noise_pct / 100) * weight * 100
        total_entropy += contribution
        print(f"  {factor_id}: {noise_pct}% × {weight} = {contribution:.2f} points")

    return total_entropy

entropy_score = calculate_entropy_score(entropy_factors, factor_weights)
print(f"\n🎯 Total Entropy Score: {entropy_score:.1f}")

# Interpret
if entropy_score <= 15:
    zone = "🟢 GREEN - Low Impact"
    action = "Continue standard M&V"
elif entropy_score <= 50:
    zone = "🟡 YELLOW - Moderate Impact"
    action = "Enhanced monitoring, quarterly recalibration"
elif entropy_score <= 75:
    zone = "🔴 RED - High Impact"
    action = "Urgent baseline redesign, monthly updates"
else:
    zone = "🔴 CRITICAL - Force Majeure"
    action = "Suspend M&V, crisis management"

print(f"Zone: {zone}")
print(f"Recommended Action: {action}")
```

**Output**:
```
  Operational-Energy-Drift: 61% × 0.08 = 4.88 points
  Model-Calibration-Staleness: 18% × 0.08 = 1.44 points
  System-Occupancy-Changes: 25% × 0.06 = 1.50 points
  Operational-Equipment-Degradation: 25% × 0.06 = 1.50 points
  Measurement-Data-Completeness: 5% × 0.10 = 0.50 points

🎯 Total Entropy Score: 9.8
Zone: 🟢 GREEN - Low Impact
Action: Continue standard M&V
```

---

## Step 8: Export to Dashboard

Generate a JSON file that can be imported into the entropy audit dashboard:

```python
import json

dashboard_export = {
    "metadata": {
        "baseline_model": "baseline_2023.idf",
        "analysis_date": "2025-01-15",
        "model_age_months": 18,
        "avg_deviation": f"{avg_deviation:.1f}%"
    },
    "entropy_factors": entropy_factors,
    "entropy_score": entropy_score,
    "zone": zone,
    "recommended_action": action,
    "deviations_by_month": deviations
}

with open("entropy_audit_results.json", "w") as f:
    json.dump(dashboard_export, f, indent=2)

print("✅ Exported to entropy_audit_results.json")
```

**Manual Dashboard Update**:

1. Open `index.html` in a browser
2. Manually adjust sliders to match `entropy_factors`:
   - Operational → Energy Drift: 61%
   - Model → Calibration Staleness: 18%
   - System → Occupancy Changes: 25%
   - Operational → Equipment Degradation: 25%
   - Measurement → Data Completeness: 5%
3. Observe the entropy score and bulb color update automatically

---

## Advanced: Automated Entropy Audits

### Monthly Scheduled Audit

```python
import schedule
import time

def monthly_entropy_audit():
    """
    Automated monthly entropy audit workflow
    """
    print("🔄 Running monthly entropy audit...")

    # 1. Run EnergyPlus simulation with latest weather
    # 2. Fetch latest utility bills
    # 3. Calculate deviations
    # 4. Map to entropy factors
    # 5. Calculate entropy score
    # 6. Send alert if score > 50 (Yellow Zone)

    if entropy_score > 50:
        send_alert(f"⚠️ Entropy score: {entropy_score:.1f} - Action required!")

# Schedule monthly on 1st of month at 9am
schedule.every().month.at("09:00").do(monthly_entropy_audit)

while True:
    schedule.run_pending()
    time.sleep(3600)  # Check every hour
```

### Portfolio-Wide Analysis

```python
buildings = [
    {"name": "Building A", "idf": "bldg_a.idf", "utility_csv": "bldg_a_bills.csv"},
    {"name": "Building B", "idf": "bldg_b.idf", "utility_csv": "bldg_b_bills.csv"},
    {"name": "Building C", "idf": "bldg_c.idf", "utility_csv": "bldg_c_bills.csv"}
]

portfolio_results = []

for building in buildings:
    print(f"\n📊 Analyzing {building['name']}...")

    # Run entropy audit for each building
    entropy_score = run_entropy_audit(building['idf'], building['utility_csv'])

    portfolio_results.append({
        "building": building['name'],
        "entropy_score": entropy_score,
        "priority": "HIGH" if entropy_score > 50 else "NORMAL"
    })

# Sort by entropy score (highest risk first)
portfolio_results.sort(key=lambda x: x['entropy_score'], reverse=True)

print("\n📈 Portfolio Entropy Summary:")
for result in portfolio_results:
    print(f"  {result['building']}: {result['entropy_score']:.1f} ({result['priority']})")
```

---

## Troubleshooting

### Issue: Simulation Fails

```python
# Check for common issues
diagnostics = await session.call_tool("get_error_logs", arguments={})
print(diagnostics)

# Common fixes:
# 1. Weather file mismatch (location, design days)
# 2. Missing HVAC components
# 3. Invalid schedules
# 4. Convergence issues (reduce timestep)
```

### Issue: Large Deviations (>30%)

Possible causes:
1. **Baseline is wrong**: Model geometry doesn't match actual building
2. **Major change occurred**: Equipment retrofit, occupancy shift
3. **Measurement error**: Meter malfunction, billing error
4. **Weather anomaly**: Extreme heat wave not captured in TMY

**Action**: Use MCP inspection tools to verify model accuracy:
```python
# Verify zones match actual building
zones = await session.call_tool("list_zones", arguments={})

# Check HVAC topology
hvac = await session.call_tool("get_hvac_topology", arguments={})

# Review internal loads
loads = await session.call_tool("get_internal_loads", arguments={})
```

---

## Best Practices

### 1. Model Calibration

Before using EnergyPlus for entropy audits, calibrate to ASHRAE Guideline 14:
- **Monthly**: CV(RMSE) < 15%, NMBE < 5%
- **Hourly**: CV(RMSE) < 30%, NMBE < 10%

### 2. Weather Data

Use **Actual Meteorological Year (AMY)** files, not TMY:
- TMY = Typical year (synthetic average)
- AMY = Actual observed weather for the audit period

### 3. Update Frequency

| Entropy Zone | Update Baseline | Run Audit |
|--------------|----------------|-----------|
| Green (0-15) | Annually | Quarterly |
| Yellow (16-50) | Quarterly | Monthly |
| Red (51-75) | Monthly | Weekly |
| Critical (76-100) | Real-time | Daily |

### 4. Version Control

Track baseline models in Git:
```bash
git init energyplus-baselines
git add baseline_2023.idf
git commit -m "Initial baseline - post-commissioning"

# After recalibration
git add baseline_2024_updated.idf
git commit -m "Updated for occupancy changes (25% WFH)"
```

---

## Example: Complete Workflow Script

```python
async def full_entropy_audit(idf_path, weather_path, utility_csv, model_age_months):
    """
    Complete entropy audit from EnergyPlus to dashboard
    """
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # 1. Load model
            print("📂 Loading baseline model...")
            await session.call_tool("load_idf_file", {"file_path": idf_path})

            # 2. Run simulation
            print("⚙️ Running EnergyPlus simulation...")
            await session.call_tool("run_simulation", {
                "weather_file": weather_path,
                "output_directory": "./outputs"
            })

            # 3. Extract predictions
            print("📊 Extracting baseline predictions...")
            baseline = await session.call_tool("get_meter_data", {
                "meter_name": "Electricity:Facility",
                "reporting_frequency": "Monthly"
            })

            # 4. Load measured data
            measured = pd.read_csv(utility_csv)

            # 5. Calculate deviations
            deviations = calculate_deviations(baseline, measured)

            # 6. Map to entropy factors
            entropy_factors = calculate_entropy_factors(
                deviations,
                model_age_months,
                occupancy_change_pct=25
            )

            # 7. Calculate entropy score
            entropy_score = calculate_entropy_score(entropy_factors, factor_weights)

            # 8. Export results
            export_to_dashboard(entropy_factors, entropy_score)

            print(f"✅ Entropy audit complete. Score: {entropy_score:.1f}")
            return entropy_score

# Run it
import asyncio
score = asyncio.run(full_entropy_audit(
    idf_path="./models/baseline_2023.idf",
    weather_path="./weather/actual_2024.epw",
    utility_csv="./data/utility_bills_2024.csv",
    model_age_months=18
))
```

---

## Resources

- **EnergyPlus MCP Server**: https://github.com/jskromer/energyplus-mcp
- **EnergyPlus Documentation**: https://energyplus.net/documentation
- **ASHRAE Guideline 14**: Measurement of Energy, Demand, and Water Savings
- **IPMVP**: International Performance Measurement & Verification Protocol
- **Model Context Protocol**: https://modelcontextprotocol.io

---

## Support

For issues with the EnergyPlus MCP Server, open an issue at:
https://github.com/jskromer/energyplus-mcp/issues

For entropy audit questions, see:
- `README.md` - Overview and features
- `BaselineModel_Structure.md` - Theoretical foundation
- `EntropyAudit_QuickReference.md` - One-page summary

---

**Version**: 1.0
**Last Updated**: January 2025
**Author**: J.S. Kromer
