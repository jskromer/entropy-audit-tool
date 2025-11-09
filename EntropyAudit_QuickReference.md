# Entropy Audit - Quick Reference Guide
## Weighted Sum of Noisy Factors Impacting M&V Baseline Value

---

## Visual Indicator

**Interactive Tool:** [Sliderandbulb.html](Sliderandbulb.html)

- 🟢 **Green (0-15)**: Low entropy - stable, predictable system
- 🟡 **Yellow (16-50)**: Moderate entropy - manageable noise levels
- 🔴 **Red Blinking (51-100)**: High entropy - critical intervention needed

**Blink rate increases with entropy** = urgency escalates

---

## Six Factor Categories

### 1. Measurement Factors (Weight: 0.31)
*Aleatory uncertainty - random variability*

| Factor | Weight | Example |
|--------|--------|---------|
| Sensor Drift | 0.08 | 240 days since calibration |
| Data Completeness | 0.10 | 3% missing data |
| Sampling Frequency | 0.06 | 15-min vs 5-min ideal |
| Measurement Error | 0.07 | Instrument precision ±2% |

### 2. Model Factors (Weight: 0.46)
*Epistemic uncertainty - incomplete knowledge*

| Factor | Weight | Example |
|--------|--------|---------|
| Model Misspecification | 0.12 | Wrong functional form |
| Parameter Uncertainty | 0.09 | Large confidence intervals |
| Omitted Variables | 0.10 | Missing confounders |
| Calibration Staleness | 0.08 | 18 months since update |
| Extrapolation Risk | 0.07 | Operating outside range |

### 3. Environmental Factors (Weight: 0.15)
*Epistemic/Ontological - operating conditions*

| Factor | Weight | Example |
|--------|--------|---------|
| Temperature Deviation | 0.04 | +3°F from baseline setpoint |
| Humidity Control | 0.03 | ±5% RH drift |
| Lighting Standards | 0.03 | Illumination changes |
| Air Quality Drift | 0.03 | -15% ventilation rate |
| Pressure Control | 0.02 | Building envelope changes |

### 4. Operational Factors (Weight: 0.23)
*Epistemic/Ontological - performance degradation*

| Factor | Weight | Example |
|--------|--------|---------|
| **Energy Drift** | **0.08** | **+16% efficiency loss** |
| Equipment Degradation | 0.06 | 8yr / 15yr expected life |
| Maintenance Variance | 0.04 | 2 missed PMs / 12 total |
| Operating Hours Drift | 0.05 | +20% runtime vs baseline |

### 5. Economic/Regulatory Factors (Weight: 0.35)
*Ontological - external forces changing value proposition*

| Factor | Weight | Example |
|--------|--------|---------|
| **Tariff Changes** | **0.09** | **+25% rate increase** |
| Demand Charges | 0.06 | +15% peak pricing |
| **Regulatory Changes** | **0.08** | **New ventilation code** |
| **Legal Requirements** | **0.07** | **Energy disclosure law** |
| Market Shifts | 0.05 | Energy price volatility |

### 6. System Factors (Weight: 0.23)
*Ontological - regime changes and unknown unknowns*

| Factor | Weight | Example |
|--------|--------|---------|
| Occupancy Changes | 0.06 | 30% work-from-home |
| External Shocks | 0.08 | COVID-19 pandemic |
| Behavioral Adaptation | 0.04 | Gaming/equation effects |
| Technology Changes | 0.05 | Equipment replacement |

---

## Quick Calculation

```
Entropy Score = Σ (Factor_i × Weight_i × Noise_i) × 100

Where:
- Factor_i: Individual noise source
- Weight_i: Importance (see tables above)
- Noise_i: Normalized 0-1 (0=ideal, 1=worst)
```

**Example:**
- Energy drift: 16% → 0.80 noise × 0.08 weight = 6.4 points
- Tariff change: 25% → 0.50 noise × 0.09 weight = 4.5 points
- Sensor drift: 240/365 days → 0.66 noise × 0.08 weight = 5.3 points
- **Total: ~60 points → RED ZONE**

---

## Action Matrix

| Score | Zone | Status | Action | Update Frequency |
|-------|------|--------|--------|------------------|
| 0-15 | 🟢 Green | LOW | Continue standard M&V | Annual |
| 16-50 | 🟡 Yellow | MODERATE | Enhanced monitoring, consider recalibration | Quarterly |
| 51-75 | 🔴 Red | HIGH | Urgent redesign, adaptive baseline | Monthly |
| 76-100 | 🔴 Blinking | CRITICAL | Force majeure, suspend M&V | Real-time |

---

## Mapping to Uncertainty Dimensions

| Entropy Range | Aleatory | Epistemic | Ontological | Cynefin Domain |
|---------------|----------|-----------|-------------|----------------|
| 0-15 | HIGH | LOW | MINIMAL | Clear/Simple |
| 16-50 | MODERATE | MODERATE | LOW | Complicated |
| 51-75 | MODERATE | HIGH | MODERATE | Complex |
| 76-100 | LOW | LOW | DOMINANT | Chaotic |

---

## Key Factor Interactions

### Cascade Effect Example

**Tariff change (4.5) → Energy drift (6.4) → Temperature deviation (3.0) → Occupancy change (4.5) → Sensor drift (5.3) = 23.7 total**

🎯 **Lesson:** External economic/regulatory factors trigger cascades that amplify entropy exponentially.

---

## Decision Framework

```
Calculate Entropy Score
        ↓
Identify Top 3 Contributing Factors
        ↓
Determine Dominant Category
        ↓
┌────────┬────────────┬──────────────┐
│Measure-│   Model    │ Economic/    │
│ment    │            │ System       │
├────────┼────────────┼──────────────┤
│Improve │ Recalibrate│ Adaptive     │
│data    │ or respec- │ baseline or  │
│quality │ ify model  │ force majeure│
└────────┴────────────┴──────────────┘
        ↓
Select Governance Protocol
        ↓
Implement Continuous Monitoring
```

---

## Governance by Zone

### 🟢 Green (0-15): Routine Operations
- Standard adjustments (weather, occupancy)
- Project manager authority
- Annual reports

### 🟡 Yellow (16-50): Enhanced Monitoring
- Routine + recalibration
- Technical review committee
- Quarterly entropy audits
- Escalate if trending to red

### 🔴 Red (51-75): Adaptive Baseline
- Dynamic updates, scenario analysis
- Stakeholder steering committee
- Monthly tracking + risk register
- Auto-escalate if >75 or sustained >60

### 🔴 Critical (76-100): Force Majeure
- Baseline suspended
- Executive + independent verification
- Formal force majeure declaration
- Immediate contract renegotiation

---

## Common Pitfalls

❌ **Ignoring cascade effects** - factors compound nonlinearly
❌ **Treating all factors equally** - use proper weights
❌ **Static assessment** - entropy evolves over time
❌ **Focusing only on measurement** - economic/system factors often dominate
❌ **No governance protocols** - high entropy without response = contract disputes

---

## Best Practices

✅ Run entropy audit at baseline establishment
✅ Schedule periodic re-audits based on initial score
✅ Monitor for threshold crossings (especially 50→51 and 75→76)
✅ Document factor contributions over time
✅ Link entropy scores to contractual force majeure clauses
✅ Use visual indicator ([Sliderandbulb.html](Sliderandbulb.html)) in stakeholder reports
✅ Train M&V team on interpretation and escalation procedures

---

## Related Documents

- **[EntropyAudit_Framework.md](EntropyAudit_Framework.md)** - Full framework with examples
- **[Counterfactual_Design_Paradigm.md](Counterfactual_Design_Paradigm.md)** - Conceptual foundation
- **[Sliderandbulb.html](Sliderandbulb.html)** - Interactive visualization

---

## Summary

**Entropy Audit = Quantitative measure of baseline degradation**

- **Weighted sum** of noisy factors across 6 categories
- **Score 0-100** with color-coded zones
- **Triggers governance protocols** from routine to force majeure
- **Maps to 3D uncertainty** (aleatory, epistemic, ontological)
- **Enables proactive management** of M&V risks

**The higher the entropy, the less reliable the baseline, the wider the uncertainty bounds, the more urgent the intervention.**

---

**Version:** 1.0
**Last Updated:** 2025-01-XX
**Status:** Active
