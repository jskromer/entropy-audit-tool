# Baseline Model Structure: How Entropy Arises

## Overview

This document describes how entropy arises in M&V (Measurement & Verification) systems by comparing actual building performance against a baseline EnergyPlus simulation model. The entropy audit tool quantifies degradation across multiple pathways that cause deviations from the baseline.

---

## The Baseline: EnergyPlus Simulation Model

### What is the Baseline?

The **baseline** is an EnergyPlus building energy simulation that represents the expected performance of a facility under controlled, known conditions. It serves as the counterfactual "ground truth" for M&V analysis.

### EnergyPlus Model Components

A baseline EnergyPlus model includes:

1. **Building Geometry**
   - Zones (thermal regions)
   - Surfaces (walls, roofs, windows, floors)
   - Materials (thermal properties, R-values)

2. **HVAC Systems**
   - Equipment topology (chillers, boilers, AHUs, VAVs)
   - Control sequences and setpoints
   - Design flow rates and capacities

3. **Internal Loads**
   - Occupancy schedules
   - Lighting power density
   - Equipment loads (plug loads)

4. **Environmental Inputs**
   - Weather data (TMY3 or AMY files)
   - Outdoor air requirements
   - Infiltration rates

5. **Operational Schedules**
   - Operating hours
   - Temperature setpoints
   - Ventilation rates

### Baseline Simulation Output

The EnergyPlus model produces time-series predictions:
- **Energy consumption** (electricity, gas) at 15-min to hourly intervals
- **Zone temperatures** and humidity levels
- **HVAC equipment performance** (COP, efficiency)
- **Demand profiles** (peak power, ramp rates)

---

## How Entropy Arises: Six Degradation Pathways

Entropy represents the **divergence between baseline predictions and measured reality**. This divergence accumulates through six categories of noise factors:

### 1. Measurement Factors (31% weight)

**Mechanism**: Sensors and data collection introduce errors that obscure true performance.

| Factor | How Entropy Arises | EnergyPlus Link |
|--------|-------------------|-----------------|
| **Sensor Drift** | Calibration degrades over time; readings deviate from true values | Measured kWh ≠ True kWh |
| **Data Completeness** | Missing data points create gaps in comparison | Cannot compare 15% of timesteps |
| **Sampling Frequency** | Coarse sampling misses peak events | 1-hour intervals miss 15-min peaks in EnergyPlus |
| **Measurement Error** | Instrument precision limits (±2% accuracy) | Uncertainty bands around measured values |

**Example**: A power meter drifts +3% over 18 months. If EnergyPlus predicts 1,000 kWh, the meter reads 1,030 kWh—but is this real drift or measurement error?

---

### 2. Model Factors (46% weight)

**Mechanism**: The EnergyPlus model itself has structural limitations and uncertainties.

| Factor | How Entropy Arises | EnergyPlus Link |
|--------|-------------------|-----------------|
| **Model Misspecification** | Wrong building geometry or HVAC topology | Simulated 10 zones vs. actual 12 zones |
| **Parameter Uncertainty** | Unknown true R-values, infiltration rates | U-value = 0.35 ± 0.10 W/m²K |
| **Omitted Variables** | Missing confounders (e.g., process loads) | EnergyPlus doesn't model loading dock activity |
| **Calibration Staleness** | Model hasn't been updated with new data | Baseline from 2023, now 2025 |
| **Extrapolation Risk** | Operating outside design conditions | Summer peak 42°C vs. design 38°C |

**Example**: The EnergyPlus model was calibrated to 2022 utility bills. In 2024, a kitchen renovation added equipment loads not in the simulation, causing systematic under-prediction.

---

### 3. Environmental Factors (15% weight)

**Mechanism**: Actual weather and indoor conditions deviate from baseline assumptions.

| Factor | How Entropy Arises | EnergyPlus Link |
|--------|-------------------|-----------------|
| **Temperature Deviation** | Setpoints change (72°F → 70°F) | Measured zone T ≠ EnergyPlus setpoint schedule |
| **Humidity Control** | RH drifts due to faulty humidifiers | Latent loads differ from baseline |
| **Lighting Standards** | Task lighting added (not in model) | Actual illumination > EnergyPlus lighting schedule |
| **Air Quality Drift** | Ventilation rates increased for IAQ | OA flow > design minimum in EnergyPlus |
| **Pressure Control** | Building envelope leaks worsen | Infiltration 1.2 ACH vs. 0.8 ACH in model |

**Example**: Post-COVID, the facility increases outdoor air ventilation by 50%. EnergyPlus baseline uses pre-COVID ventilation rates, so cooling energy is now systematically under-predicted.

---

### 4. Operational Factors (23% weight)

**Mechanism**: Equipment performance degrades and operational practices change.

| Factor | How Entropy Arises | EnergyPlus Link |
|--------|-------------------|-----------------|
| **Energy Drift** | Chiller COP degrades (5.2 → 4.6) | Measured kW/ton > EnergyPlus COP curve |
| **Equipment Degradation** | Fouling, wear reduce efficiency | Fan power increases due to dirty filters |
| **Maintenance Variance** | Deferred PMs accumulate inefficiencies | Belts slip, heat exchangers foul |
| **Operating Hours Drift** | Schedule changes (8am-5pm → 7am-7pm) | Actual occupancy ≠ baseline schedule |

**Example**: The EnergyPlus model assumes a chiller COP of 5.2 (design spec). After 3 years, fouling reduces actual COP to 4.7. Measured cooling energy exceeds baseline by 11%.

---

### 5. Economic/Regulatory Factors (35% weight)

**Mechanism**: External changes invalidate baseline economic and compliance assumptions.

| Factor | How Entropy Arises | EnergyPlus Link |
|--------|-------------------|-----------------|
| **Tariff Changes** | New rate structure changes cost optimization | Demand charges shift load profiles |
| **Demand Charges** | Time-of-use peaks penalized | Baseline didn't model TOU strategies |
| **Regulatory Changes** | New ASHRAE 90.1 requirements | Ventilation, lighting codes change |
| **Legal Requirements** | ADA, fire code trigger modifications | Door usage, elevator loads change |
| **Market Shifts** | Energy price volatility changes behavior | Occupants react to price signals |

**Example**: A utility introduces time-of-use pricing. The facility shifts cooling loads to off-peak hours. EnergyPlus baseline assumed flat rates, so temporal load patterns now differ fundamentally.

---

### 6. System Factors (23% weight)

**Mechanism**: Macro-level shocks and adaptations render the baseline obsolete.

| Factor | How Entropy Arises | EnergyPlus Link |
|--------|-------------------|-----------------|
| **Occupancy Changes** | Remote work reduces density 30% | Measured occupancy < baseline people schedule |
| **External Shocks** | Pandemic, natural disasters | COVID-19 hybrid work not in 2019 baseline |
| **Behavioral Adaptation** | Occupants game the system | Manual overrides defeat EnergyPlus control logic |
| **Technology Changes** | LED retrofit, VFD upgrades | Lighting/fan power < baseline equipment objects |

**Example**: COVID-19 shifts an office building to 60% remote work. The EnergyPlus baseline assumed 100% occupancy 8am-6pm. Now internal loads, plug loads, and HVAC schedules are fundamentally different.

---

## The Entropy Calculation

### Formula

```
Entropy Score = Σ (Noise_i × Weight_i) × 100
                i=1 to 30+ factors

Where:
- Noise_i = Current deviation for factor i (0-100%)
- Weight_i = Category and factor importance (sums to 1.0)
```

### Interpretation

| Entropy Score | Meaning | Baseline Status |
|---------------|---------|-----------------|
| **0-15** | Low entropy | Baseline still valid, minor calibration needed |
| **16-50** | Moderate entropy | Baseline degrading, recalibration recommended |
| **51-75** | High entropy | Baseline substantially invalid, redesign needed |
| **76-100** | Critical entropy | Baseline obsolete, force majeure condition |

---

## Integration with EnergyPlus MCP Server

### Workflow

The [EnergyPlus MCP Server](https://github.com/jskromer/energyplus-mcp) enables programmatic interaction with baseline models:

1. **Load Baseline IDF**: Use `load_idf_file` to load the baseline building model
2. **Inspect Model**: Extract zones, HVAC topology, schedules with inspection tools
3. **Run Baseline Simulation**: Execute with historical weather using `run_simulation`
4. **Extract Predictions**: Get time-series energy consumption outputs
5. **Compare to Measured Data**: Calculate deviations (measured - predicted)
6. **Quantify Factor Contributions**: Map deviations to entropy factors
7. **Calculate Entropy Score**: Weighted sum across all factors

### Example: Detecting Energy Drift

```python
# 1. Load baseline model
mcp_client.load_idf_file("baseline_2023.idf")

# 2. Run simulation with actual weather
mcp_client.run_simulation(weather_file="actual_2024.epw")

# 3. Get baseline prediction
baseline_kwh = mcp_client.get_meter_data("Electricity:Facility")

# 4. Compare to measured data
measured_kwh = utility_data.get_consumption()

# 5. Calculate deviation
drift_percent = (measured_kwh - baseline_kwh) / baseline_kwh * 100

# 6. Map to entropy factor
if drift_percent > 10:
    entropy_factors["Operational-Energy-Drift"] = min(drift_percent, 100)
```

### MCP Tools for Entropy Analysis

| MCP Tool Category | Entropy Use Case |
|-------------------|------------------|
| **Model Inspection** | Verify baseline matches current building (zones, HVAC) |
| **Modification Tools** | Update baseline with known changes (schedules, loads) |
| **Simulation** | Generate predictions for comparison |
| **Visualization** | Plot baseline vs. actual consumption |

---

## Practical Example: Office Building Entropy Analysis

### Baseline Setup (Year 0)

- **Building**: 50,000 sq ft office, 3 floors, VAV system
- **EnergyPlus Model**: Calibrated to 2023 utility bills (CV-RMSE < 15%)
- **Initial Entropy Score**: 8 (Low - Green Zone)

### Year 1 Audit

**Observed Changes**:
- Utility bills 12% higher than baseline prediction
- Occupancy surveys show 25% WFH adoption
- Chiller maintenance logs show COP degradation

**Entropy Contribution**:
- Energy Drift: 12% → 12 points
- Occupancy Changes: 25% → 6 points
- Equipment Degradation: 15% → 4 points
- **Total Entropy**: 22 (Moderate - Yellow Zone)

**Action**: Quarterly recalibration, update occupancy schedules in EnergyPlus

### Year 2 Audit

**Observed Changes**:
- COVID-19 pandemic → hybrid work policy (40% WFH)
- New utility rate structure with demand charges
- Deferred maintenance due to budget cuts

**Entropy Contribution**:
- External Shocks: 80% → 20 points
- Occupancy Changes: 40% → 10 points
- Tariff Changes: 60% → 14 points
- Equipment Degradation: 25% → 6 points
- Maintenance Variance: 50% → 5 points
- **Total Entropy**: 55 (High - Red Zone)

**Action**: Urgent baseline redesign with adaptive protocols, consider force majeure

---

## Key Insights

### 1. Entropy is Multi-Dimensional

The 30+ factors span measurement, model, environmental, operational, economic, and system domains. High entropy can result from:
- **Many small deviations** (death by 1000 cuts)
- **One catastrophic change** (COVID-19, equipment failure)

### 2. EnergyPlus Provides the Counterfactual

Without a simulation baseline, you cannot distinguish:
- **Real efficiency improvements** (entropy factor)
- **Measurement errors** (entropy factor)
- **Weather-driven variation** (accounted for in EnergyPlus)

### 3. Entropy Triggers Governance

| Zone | Action | EnergyPlus Role |
|------|--------|-----------------|
| **Green** | Monitor | Run annual baseline with updated weather |
| **Yellow** | Recalibrate | Update schedules, loads, and re-run |
| **Red** | Redesign | Build new model with current conditions |
| **Critical** | Force Majeure | Baseline invalid, suspend M&V |

---

## Conclusion

The entropy audit framework quantifies how **real-world divergence from a baseline EnergyPlus model** accumulates across multiple pathways. By systematically tracking 30+ noise factors, M&V professionals can:

1. **Diagnose** which factors drive baseline degradation
2. **Prioritize** recalibration efforts (highest-contribution factors)
3. **Trigger** governance protocols before contracts break down
4. **Communicate** system health to non-technical stakeholders

The EnergyPlus MCP server enables programmatic baseline management, making entropy audits scalable across large building portfolios.

---

## References

- **EnergyPlus MCP Server**: https://github.com/jskromer/energyplus-mcp
- **EnergyPlus Documentation**: https://energyplus.net/documentation
- **IPMVP**: International Performance Measurement & Verification Protocol
- **ASHRAE Guideline 14**: Measurement of Energy, Demand, and Water Savings

---

**Version**: 1.0
**Last Updated**: January 2025
**Author**: J.S. Kromer
