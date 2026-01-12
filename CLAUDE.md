# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Big Five Aspect Scale (BFAS) personality assessment application. Combines deterministic Python scoring with LLM-powered interpretation using RAG (Retrieval-Augmented Generation).

## Architecture

```
User Input (100 items, 1-5 Likert)
        │
        v
  bfas_scoring.py (deterministic)
   - Validate responses
   - Calculate raw scores (10 items/aspect)
   - Apply reverse coding (items 9-10 of each aspect)
   - Select norms (University <25, ESCS ≥25)
   - Apply gender adjustments (female: compassion, withdrawal, politeness)
   - Compute percentiles via z-score
   - Detect asymmetries (≥15 percentile diff within domain)
   - Flag clinical patterns
        │
        v
  BFASProfile object
        │
        v
  LLM Interpretation Layer
   - Input: profile + user context
   - RAG: BFAS_Complete_RAG_Knowledge_Base.md
   - Output: Natural language report (800-1200 words)
```

## Key Data Files

- `bfas_instrument.json` - 100 items in Swedish, aspect/dimension mapping, reverse-coding flags
- `bfas_scoring.py` - Scoring engine with embedded ESCS/University norms
- `test_profiles.json` - 10 test cases including clinical patterns (max_dysregulation, psychosis_prone, aggression_risk)
- `BFAS_Complete_RAG_Knowledge_Base.md` - 50+ study synthesis for LLM context

## Scoring Details

**Dimensions and Aspects:**
- Openness/Intellect: openness (1-10), intellect (11-20)
- Conscientiousness: industriousness (21-30), orderliness (31-40)
- Extraversion: enthusiasm (41-50), assertiveness (51-60)
- Agreeableness: compassion (61-70), politeness (71-80)
- Neuroticism: withdrawal (81-90), volatility (91-100)

**Reverse-coded items:** Last 2 items of each aspect (formula: 6 - response)

**Clinical flags detected:** max_dysregulation, aggression_risk, depression_suicide_risk, impulsive_selfharm, psychosis_proneness, hypomania_risk, perfectionism_paralysis

## Commands

```bash
# Run scoring test (Sara profile)
python exportedResearch/bfas_scoring.py

# Dependencies
pip install scipy
```

## Implementation Status

**Complete & Live** - Streamlit web app fully functional and deployed on Streamlit Cloud.

### Latest Session Enhancements (Jan 2026)
- Added "About the Developer" modal with bio and Buy Me a Coffee button (welcome page footer)
- Optimized interpretation quality: increased max_tokens (1500 → 2500), added conciseness directives
- Removed slow UI elements ("Take Again" button) that triggered st.rerun()
- Set app to production mode (DEV_MODE=0)
- Added privacy assurance in disclaimer
- Renamed button to "Start Anonymous Assessment"

### Known Limitations
- **Framework limitation:** Streamlit's `st.rerun()` causes noticeable latency on state changes
- **Architectural note:** Streamlit is appropriate for this internal-tool use case but would struggle with 100+ concurrent users
- See global CLAUDE.md for Technology Stack Assessment framework—use for future projects

## Language

- Instrument items: Swedish
- Code/documentation: English
- App copy available in `bfas_app_copy.md`
