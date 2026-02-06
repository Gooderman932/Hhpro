# TRADE SECRETS DOCUMENTATION
## Poor Dude Holdings LLC - Confidential

### Document Classification: CONFIDENTIAL
### Last Updated: February 2025

---

## DEFINITION

The following algorithms, methodologies, formulas, weights, thresholds, and implementation 
details constitute **Trade Secrets** of Poor Dude Holdings LLC under the:
- Defend Trade Secrets Act (DTSA)
- Uniform Trade Secrets Act (UTSA)

---

## PROTECTED TRADE SECRETS

### 1. Win Probability Model Trade Secrets

| Element | Description | File Location |
|---------|-------------|---------------|
| Weight Configuration | Factor weighting for probability calculation | `_WEIGHTS` in win_probability_model.py |
| Threshold Values | Probability classification thresholds | `_THRESHOLDS` in win_probability_model.py |
| Calibration Formula | User-specific prediction calibration | `_calculate_calibration()` |
| Project Fit Algorithm | Multi-factor project-contractor fit scoring | `_score_project_fit()` |
| Competitive Pressure Formula | Bidder competition impact calculation | `_score_competitive_pressure()` |
| Market Conditions Scoring | Economic and sector adjustment methodology | `_score_market_conditions()` |

### 2. Demand Forecasting Engine Trade Secrets

| Element | Description | File Location |
|---------|-------------|---------------|
| Seasonality Factors | Month-by-month demand adjustments | `_SEASONALITY` in demand_forecast_model.py |
| Regional Growth Factors | State-level market growth multipliers | `_REGIONAL_FACTORS` |
| Sector Multipliers | Industry-specific growth rates | `_SECTOR_MULTIPLIERS` |
| Market Momentum Algorithm | Proprietary momentum score calculation | `calculate_market_momentum()` |
| Economic Impact Formula | Integration of economic indicators | `_calculate_economic_impact()` |
| Confidence Interval Methodology | Prediction uncertainty estimation | `_calculate_confidence_interval()` |

### 3. Competitive Intelligence Scorer Trade Secrets

| Element | Description | File Location |
|---------|-------------|---------------|
| Threat Weights | Factor weighting for threat calculation | `_THREAT_WEIGHTS` in competitive_intelligence.py |
| Threat Thresholds | Classification boundaries | `_THREAT_THRESHOLDS` |
| Market Share Threat Formula | Non-linear share-to-threat conversion | `_calculate_market_share_threat()` |
| Competitive Advantage Index | Overall competitive positioning algorithm | `calculate_competitive_advantage_index()` |

### 4. Project Matcher AI Trade Secrets

| Element | Description | File Location |
|---------|-------------|---------------|
| Trade Keywords | Domain-specific keyword embeddings | `_TRADE_KEYWORDS` in project_matcher.py |
| Sector Profiles | Complexity/regulation characteristics | `_SECTOR_PROFILES` |
| Text Similarity Algorithm | Semantic matching methodology | `_calculate_text_similarity()` |
| Value Fit Optimization | Optimal value range calculation | `_calculate_value_fit()` |
| Feedback Learning Algorithm | Adaptive preference learning | `_learn_from_feedback()` |

---

## SECURITY MEASURES

### Access Control
- All ML code resides in `/app/backend/app/ml/proprietary/`
- Source code access restricted to authorized personnel only
- Git repository access requires signed NDA

### Code Protection
- All files contain copyright headers
- Model outputs include proprietary watermarks
- Usage tracked via model instance IDs

### Employee Obligations
- All employees sign confidentiality agreements
- Trade secret training required annually
- Exit interviews include trade secret reminders

---

## MISAPPROPRIATION PREVENTION

### Monitoring
- Code access logging enabled
- Unusual access patterns flagged
- Model API calls monitored

### Legal Protection
- Non-disclosure agreements with all partners
- Non-compete clauses where applicable
- Clear IP assignment in employment contracts

---

## ENFORCEMENT PROCEDURES

In case of suspected misappropriation:

1. **Documentation**: Preserve all evidence of unauthorized access or use
2. **Legal Consultation**: Contact legal@poorduceholdings.com immediately
3. **Cease and Desist**: Issue formal notice to suspected parties
4. **Litigation**: Pursue legal remedies under DTSA/UTSA if necessary

---

## CONTACT

**Legal Department**: legal@poorduceholdings.com
**Security Team**: security@poorduceholdings.com

---

**© 2025 Poor Dude Holdings LLC. All Rights Reserved.**

This document itself constitutes confidential information.
