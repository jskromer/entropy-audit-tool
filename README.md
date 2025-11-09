# 🎯 Entropy Audit Tool

**Interactive M&V Baseline Risk Assessment Dashboard**

A comprehensive framework for quantifying baseline degradation through weighted entropy scoring across 6 factor categories and 30+ individual noise sources.

🌐 **[Launch Dashboard](https://jskromer.github.io/entropy-audit-tool/)**

---

## Overview

The Entropy Audit Tool helps M&V professionals assess baseline reliability by calculating a weighted sum of noisy factors that impact value. Higher entropy scores indicate greater degradation and trigger escalating governance protocols.

### Key Features

- 🎛️ **Interactive Dashboard** - Real-time entropy calculation with 30+ factor sliders
- 📊 **Visual Indicators** - Color-coded bulb (green → yellow → red blinking) based on risk level
- 📈 **Category Breakdown** - Contribution analysis across 6 major categories
- 🎯 **Scenario Testing** - Pre-loaded low/moderate/high risk scenarios
- ⚡ **Action Recommendations** - Automatic governance protocols by entropy zone

---

## Entropy Zones

| Score | Zone | Status | Action | Update Frequency |
|-------|------|--------|--------|------------------|
| 0-15 | 🟢 Green | LOW | Continue standard M&V | Annual |
| 16-50 | 🟡 Yellow | MODERATE | Enhanced monitoring, recalibration | Quarterly |
| 51-75 | 🔴 Red | HIGH | Urgent redesign, adaptive baseline | Monthly |
| 76-100 | 🔴 Critical | FORCE MAJEURE | Suspend M&V, crisis management | Real-time |

---

## Factor Categories

### 1. Measurement Factors (31%)
- Sensor Drift
- Data Completeness
- Sampling Frequency
- Measurement Error

### 2. Model Factors (46%)
- Model Misspecification
- Parameter Uncertainty
- Omitted Variables
- Calibration Staleness
- Extrapolation Risk

### 3. Environmental Factors (15%)
- Temperature Deviation
- Humidity Control
- Lighting Standards
- Air Quality Drift
- Pressure Control

### 4. Operational Factors (23%)
- **Energy Drift** ⚠️
- Equipment Degradation
- Maintenance Variance
- Operating Hours Drift

### 5. Economic/Regulatory Factors (35%)
- **Tariff Changes** ⚠️
- Demand Charges
- **Regulatory Changes** ⚠️
- Legal Requirements
- Market Shifts

### 6. System Factors (23%)
- Occupancy Changes
- External Shocks (e.g., COVID-19)
- Behavioral Adaptation
- Technology Changes

---

## Quick Start

1. **Open the Dashboard**: [index.html](https://jskromer.github.io/entropy-audit-tool/)
2. **Adjust Sliders**: Set noise levels (0-100%) for each factor
3. **View Results**: Watch entropy score, bulb color, and recommended actions update in real-time
4. **Test Scenarios**: Click pre-loaded scenario buttons to see typical cases

---

## Calculation Formula

```
Entropy Score = Σ (Factor_i × Weight_i × Noise_i) × 100
                i=1 to 30+

Where:
- Factor_i: Individual noise source
- Weight_i: Category/factor importance (see tables)
- Noise_i: Current noise level (0-1 normalized)
```

---

## Example: High Entropy Scenario

**Scenario**: Office building M&V in Year 2, post-COVID with new tariff structure

**Key Drivers**:
- Energy drift: +16% efficiency loss → 6.40 points
- Tariff changes: +25% rate increase → 4.50 points
- Regulatory changes: New ventilation code → 4.80 points
- External shocks: COVID hybrid work → 6.40 points
- Occupancy changes: 30% WFH → 4.50 points

**Total Entropy Score: 60** (Red Zone - High Risk)

**Recommended Action**: Urgent baseline redesign with adaptive protocols and monthly updates

---

## Integration with M&V Framework

### Maps to 3D Uncertainty Model

| Entropy Range | Aleatory | Epistemic | Ontological | Cynefin Domain |
|---------------|----------|-----------|-------------|----------------|
| 0-15 | HIGH | LOW | MINIMAL | Clear/Simple |
| 16-50 | MODERATE | MODERATE | LOW | Complicated |
| 51-75 | MODERATE | HIGH | MODERATE | Complex |
| 76-100 | LOW | LOW | DOMINANT | Chaotic |

### Governance Protocols

- **Green Zone**: Routine adjustments only, project manager authority
- **Yellow Zone**: Enhanced monitoring, technical review committee
- **Red Zone**: Dynamic baseline, stakeholder steering committee
- **Critical Zone**: Force majeure, executive decision + independent verification

---

## Files

- **index.html** - Main interactive dashboard
- **Sliderandbulb.html** - Simple entropy indicator visualization
- **EntropyAudit_QuickReference.md** - One-page summary
- **README.md** - This file

---

## Theoretical Foundation

Based on the **Counterfactual Design Paradigm** which organizes M&V uncertainty into three dimensions:

1. **Aleatory Uncertainty** - Inherent randomness (statistical treatment)
2. **Epistemic Uncertainty** - Incomplete knowledge (Bayesian updating)
3. **Ontological Uncertainty** - Regime changes & unknown unknowns (governance protocols)

The entropy audit provides a single composite metric that maps to these dimensions and triggers appropriate inference strategies.

---

## Use Cases

✅ **Baseline Establishment** - Assess initial system complexity
✅ **Quarterly Reviews** - Monitor entropy drift over time
✅ **Contract Disputes** - Quantify force majeure triggers
✅ **Portfolio Management** - Compare entropy across sites
✅ **Training** - Teach M&V professionals about baseline risks
✅ **Stakeholder Communication** - Visual representation of system health

---

## Citation

If you use this tool in your work, please reference:

> Kromer, J.S. (2025). Entropy Audit: A Dimensional Framework for M&V Baseline Risk Assessment.
> https://github.com/jskromer/entropy-audit-tool

---

## License

MIT License - Free to use, modify, and distribute with attribution

---

## Contact

For questions, feedback, or collaboration:
- GitHub: [@jskromer](https://github.com/jskromer)
- Web: [Launch Tool](https://jskromer.github.io/entropy-audit-tool/)

---

**Version**: 1.0
**Last Updated**: January 2025
**Status**: Production Ready

---

## Acknowledgments

Built on principles from:
- Counterfactual Design Paradigm
- Cynefin Complexity Framework
- Stacey Matrix
- IPMVP (International Performance Measurement & Verification Protocol)
- Information Theory (Shannon Entropy)
