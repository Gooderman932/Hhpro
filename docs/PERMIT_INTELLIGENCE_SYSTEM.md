# Permit Intelligence System
## Poor Dude Holdings LLC - Patent Pending

---

## Architecture

```
Raw Permits (paid + free sources)
        |
        v
  Normalization Layer (unified schema)
        |
        v
  Proprietary ML Enrichment
  - ProjectMatcherAI (fit scoring)
  - WinProbabilityModel (win chance)
  - Opportunity Score (weighted formula)
        |
        v
  Ranked, Actionable Opportunities
  (served via /api/permits/search)
```

## Data Sources

### Paid Sources (PERMIT_API_KEY required)
| Provider | Coverage | Env Var |
|----------|----------|---------|
| Shovels.ai | Nationwide, AI-cleaned | `PERMIT_API_KEY`, `PERMIT_API_PROVIDER=shovels` |
| BatchData | 125M+ permits, daily refresh | `PERMIT_API_KEY`, `PERMIT_API_PROVIDER=batchdata` |

### Free Sources (always available)
| Source | Coverage | Env Var |
|--------|----------|---------|
| NYC DOB Open Data | New York City permits | None required (optional `SOCRATA_APP_TOKEN`) |
| Census Bureau | Nationwide aggregate stats | `CENSUS_API_KEY` |
| FRED (already live) | Economic indicators | `FRED_API_KEY` |

## Tier Access

| Feature | Basic ($49) | Pro ($149) | Enterprise ($399) |
|---------|-------------|------------|-------------------|
| NYC Open Data | 25/search | Unlimited | Unlimited |
| Paid Permit Source | - | 100/search | 250/search |
| AI Opportunity Score | Yes | Yes | Yes |
| Win Probability | Yes | Yes | Yes |
| Match Score | Yes | Yes | Yes |
| Census Stats | Basic | Full | Full |

## API Endpoint

```
GET /api/permits/search?location=Austin&state=TX&limit=50
Authorization: Bearer <token>
```

Response includes `proprietary_analysis` per permit with:
- `opportunity_score` (0-100): Weighted composite of match, win probability, cost, recency
- `match_score` (0-100): How well the permit matches the user's trade/profile
- `win_probability` (0-100): Predicted chance of winning the bid
- `required_trades`: Detected trade specialties needed
- `estimated_timeline_months`: Project duration estimate
- `recommendation`: Actionable text (e.g., "Excellent opportunity - contact owner ASAP")

## Environment Setup

```bash
# Required for paid permits (pick one provider)
PERMIT_API_KEY=your_key_here
PERMIT_API_PROVIDER=shovels  # or batchdata

# Free data enrichment
CENSUS_API_KEY=your_census_key  # https://api.census.gov/data/key_signup.html
FRED_API_KEY=your_fred_key      # Already configured

# Optional
SOCRATA_APP_TOKEN=your_token    # Higher rate limits for NYC data
```
