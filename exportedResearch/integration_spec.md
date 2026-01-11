# BFAS System Integration Specification

## Architecture Overview

```
┌─────────────┐
│ User Input  │
│ (100 items) │
└──────┬──────┘
       │
       v
┌─────────────────────────────┐
│  bfas_scoring.py            │
│  (Deterministic Pipeline)   │
│                             │
│  1. Validate responses      │
│  2. Calculate raw scores    │
│  3. Select norms            │
│  4. Compute percentiles     │
│  5. Detect asymmetries      │
│  6. Flag clinical patterns  │
└──────┬──────────────────────┘
       │
       v (BFASProfile object)
       │
┌──────┴──────────────────────┐
│  LLM Interpretation Layer   │
│  (Uses RAG knowledge base)  │
│                             │
│  Input: profile + context   │
│  RAG: BFAS_Complete_RAG...  │
│  Output: Natural language   │
└──────┬──────────────────────┘
       │
       v
┌─────────────┐
│ Final Report│
└─────────────┘
```

## Data Flow

### Input
```python
{
    "responses": [1-5, 1-5, ...],  # 100 integers
    "age": 29,
    "gender": "female",  # optional
    "context": {  # optional, for interpretation
        "occupation": "PhD student",
        "education": "graduate",
        "reason": "personal development"
    }
}
```

### Scoring Output
```python
{
    "metadata": {
        "age": 29,
        "gender": "female",
        "norm_set": "ESCS"
    },
    "aspect_scores": {
        "intellect": {
            "raw_score": 40,
            "mean_score": 4.0,
            "percentile": 84,
            "z_score": 1.01,
            "gender_adjusted": false
        },
        # ... 9 more aspects
    },
    "dimension_scores": {
        "openness_intellect": 73,
        # ... 4 more dimensions
    },
    "asymmetries": [
        {
            "domain": "openness_intellect",
            "higher_aspect": "intellect",
            "percentile_difference": 36,
            "aspects": ["intellect", "openness"]
        }
    ],
    "clinical_flags": []
}
```

### LLM Interpretation Prompt Template
```
You are Dr. Alexandra Svensson, BFAS expert psychologist.

TASK: Interpret this BFAS profile for personal development (not clinical diagnosis).

PROFILE DATA:
{scoring_output}

CONTEXT:
- Age: {age}
- Gender: {gender}
- Occupation: {occupation}
- Education: {education}

KNOWLEDGE BASE:
{BFAS_Complete_RAG_Knowledge_Base.md}

REQUIREMENTS:
1. Start with core profile summary (2-3 sentences)
2. Analyze significant asymmetries (percentile diff >= 15)
3. Address clinical flags IF present (with disclaimers)
4. Provide practical implications for their context
5. List strengths and development areas
6. Suggest optimal environments
7. Use natural language, avoid jargon
8. Be evidence-based but conversational

TONE: Professional but warm, like a mentor
LENGTH: 800-1200 words
```

## Implementation Phases

### Phase 1: Core Scoring (Week 1)
- [ ] Implement `bfas_scoring.py`
- [ ] Unit tests for all functions
- [ ] Validate against known profiles
- [ ] Test edge cases (all 1s, all 5s, clinical patterns)

### Phase 2: Integration Layer (Week 2)
- [ ] API endpoint or CLI wrapper
- [ ] Prompt template for LLM interpretation
- [ ] RAG retrieval integration
- [ ] Output formatting (PDF/markdown/JSON)

### Phase 3: User Interface (Week 3-4)
**Option A: Web App (Streamlit)**
```python
import streamlit as st
from bfas_scoring import calculate_all_scores

st.title("BFAS Personality Assessment")

# Collect demographics
age = st.number_input("Age", min_value=17, max_value=100)
gender = st.selectbox("Gender", ["Male", "Female", "Prefer not to say"])

# Collect 100 responses (use form with sections)
responses = []
for i in range(1, 101):
    responses.append(st.slider(f"Item {i}", 1, 5, 3))

if st.button("Generate Profile"):
    profile = calculate_all_scores(responses, age, gender)
    # Pass to LLM for interpretation
    interpretation = generate_interpretation(profile)
    st.write(interpretation)
```

**Option B: CLI Tool**
```bash
$ python bfas_assess.py --input responses.json --output report.pdf
$ python bfas_assess.py --interactive
```

**Option C: API Endpoint**
```python
from fastapi import FastAPI
from bfas_scoring import calculate_all_scores

app = FastAPI()

@app.post("/assess")
def assess(data: dict):
    profile = calculate_all_scores(
        data["responses"],
        data["age"],
        data.get("gender")
    )
    interpretation = generate_interpretation(profile)
    return {"profile": profile, "interpretation": interpretation}
```

## Testing Strategy

### Unit Tests
```python
def test_reverse_coding():
    assert reverse_code(1) == 5
    assert reverse_code(5) == 1

def test_aspect_scoring():
    # All 5s, no reverse items triggered
    responses = [5] * 100
    score = calculate_aspect_raw_score(responses, 'openness')
    assert score == 50  # 8*5 + 2*1 (reversed)

def test_gender_adjustment():
    norms_male, _ = select_norms(30, 'male')
    norms_female, _ = select_norms(30, 'female')
    assert norms_female['compassion']['mean'] > norms_male['compassion']['mean']

def test_clinical_flags():
    # Create max dysregulation profile
    responses = create_profile(volatility=45, withdrawal=45)
    profile = calculate_all_scores(responses, 25, None)
    assert any(f.pattern == 'max_dysregulation' for f in profile.clinical_flags)
```

### Integration Tests
- Sara profile (from our example)
- Edge case: All 1s
- Edge case: All 5s
- Clinical pattern: Max dysregulation
- Clinical pattern: Psychosis-proneness
- Asymmetry detection: High Intellect + Low Openness

## Deployment Considerations

### Dependencies
```
scipy>=1.11.0
python>=3.9
```

### Data Files Required
- `bfas_instrument.json` (100 items, metadata)
- `BFAS_Complete_RAG_Knowledge_Base.md` (for LLM context)

### Security
- No PHI/PII storage for production
- Responses should be anonymous
- Clinical flags trigger disclaimer, not diagnosis

### Disclaimers
```
This assessment is for personal development only.
Not a clinical diagnosis or substitute for professional evaluation.
If clinical flags are present, consult licensed mental health professional.
Results based on self-report and may not reflect others' perceptions.
```

## Next Steps

1. **Immediate:** Validate `bfas_scoring.py` works correctly
2. **This week:** Decide on UI (web/CLI/API)
3. **Next week:** Build interpretation prompt template
4. **Week 3:** Full integration + testing
5. **Week 4:** Production deployment

## Questions for Thomas

1. Preferred interface: Web app, CLI, or API?
2. Output format: PDF, markdown, interactive web?
3. Public or private deployment?
4. Need multi-language support (Swedish + English)?
