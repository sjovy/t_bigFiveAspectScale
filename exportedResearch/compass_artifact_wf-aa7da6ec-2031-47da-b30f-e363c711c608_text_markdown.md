# BFAS Normative Data for AI Personality Assessment

The Big Five Aspect Scale provides robust psychometric data for converting raw scores to standardized interpretations, though **no official percentile tables exist**. The best normative reference comes from the Swiss PERCIVAL study (N=4,457 representative adults), while the original DeYoung et al. (2007) study remains the foundational source with complete descriptive statistics for all 10 aspects. Raw-to-percentile conversion requires computing z-scores from published means and SDs, then applying normal distribution assumptions given the scale's well-established normality.

---

## Complete normative statistics from the original validation

The definitive BFAS norms come from DeYoung, Quilty, & Peterson (2007) published in the *Journal of Personality and Social Psychology*. Two samples provide complementary reference data: the Eugene-Springfield Community Sample (ESCS) with **N=481** adults aged 20-85 (M=52.51, SD=12.63) represents general adult populations, while the University Sample with **N=480** students aged 17-61 (M=19.32, SD=3.33) provides norms for younger populations.

### Community sample descriptive statistics (ESCS, N=481)

| Aspect | Mean | SD | Cronbach's α |
|--------|------|-----|--------------|
| **Volatility** | 2.48 | 0.70 | .85 |
| **Withdrawal** | 2.45 | 0.71 | .84 |
| **Compassion** | 4.11 | 0.54 | .84 |
| **Politeness** | 4.10 | 0.53 | .75 |
| **Industriousness** | 3.80 | 0.61 | .81 |
| **Orderliness** | 3.73 | 0.62 | .80 |
| **Enthusiasm** | 3.59 | 0.72 | .81 |
| **Assertiveness** | 3.36 | 0.70 | .85 |
| **Intellect** | 3.70 | 0.68 | .84 |
| **Openness** | 3.74 | 0.61 | .78 |

Domain-level reliability ranges from α=.84 to α=.89. The ESCS sample was 97% White, with approximately equal years of post-secondary education. For general adult norms, this community sample is recommended over the university sample due to its broader age range and non-student composition.

### University sample shows systematic differences from adults

| Aspect | Mean | SD | α | Test-Retest r |
|--------|------|-----|---|---------------|
| **Volatility** | 2.72 | 0.82 | .87 | .85 |
| **Withdrawal** | 2.92 | 0.75 | .81 | .81 |
| **Compassion** | 3.87 | 0.65 | .84 | .79 |
| **Politeness** | 3.52 | 0.67 | .76 | .74 |
| **Industriousness** | 2.84 | 0.70 | .79 | .82 |
| **Orderliness** | 3.28 | 0.64 | .72 | .79 |
| **Enthusiasm** | 3.52 | 0.73 | .81 | .73 |
| **Assertiveness** | 3.21 | 0.71 | .84 | .86 |
| **Intellect** | 3.39 | 0.67 | .79 | .86 |
| **Openness** | 3.52 | 0.64 | .72 | .79 |

Students score **higher on Neuroticism aspects** (Volatility: +0.24, Withdrawal: +0.47) and **lower on Conscientiousness aspects** (Industriousness: −0.96, Orderliness: −0.45) compared to community adults. This reflects established developmental patterns where conscientiousness increases and neuroticism decreases with age. Test-retest reliability averages **r=.81** over 38 days.

---

## Inter-aspect correlations reveal the BFAS structure

Understanding correlations between aspects is essential for interpreting profile patterns. Within-domain aspect correlations range from **r=.51 to r=.64**, confirming aspects are related but distinct constructs.

| Aspect Pair (Same Domain) | Correlation |
|---------------------------|-------------|
| Volatility–Withdrawal | .64 |
| Compassion–Politeness | .54 |
| Industriousness–Orderliness | .64 |
| Enthusiasm–Assertiveness | .53 |
| Intellect–Openness | .51 |

Cross-domain correlations reveal meaningful patterns: **Assertiveness correlates negatively with Politeness (r=−.37)**, reflecting the confidence-deference tradeoff. **Withdrawal shows moderate negative correlations with Assertiveness (r=−.46), Intellect (r=−.36), and Enthusiasm (r=−.40)**, consistent with withdrawal's association with social avoidance. Compassion and Enthusiasm correlate at **r=.59**, linking warmth-related traits across domains.

---

## Gender norms require separate percentile calculations

Weisberg, DeYoung & Hirsh (2011) provides the definitive gender difference data from **N=2,643** adults (892 male, 1,751 female; ages 17-85). Effect sizes (Cohen's d) indicate where separate gender norms are warranted:

| Aspect | Direction | Cohen's d | Interpretation |
|--------|-----------|-----------|----------------|
| **Compassion** | Women higher | 0.45 | Medium effect |
| **Withdrawal** | Women higher | 0.40 | Small-medium |
| **Politeness** | Women higher | 0.36 | Small-medium |
| **Volatility** | Women higher | 0.30 | Small |
| **Openness** | Women higher | 0.27 | Small |
| **Enthusiasm** | Women higher | 0.23 | Small |
| **Intellect** | Men higher | 0.22 | Small |
| **Orderliness** | Women higher | 0.18 | Negligible-small |
| **Assertiveness** | Men higher | 0.09 | Negligible |
| **Industriousness** | — | 0.06 | Negligible |

For an AI assessment tool, **gender-specific norms are recommended for Compassion, Withdrawal, and Politeness** given their medium effect sizes. A woman scoring at the 50th percentile for Compassion using combined norms would actually fall around the 33rd percentile compared to other women. The domain-level differences are smaller (Agreeableness d=0.48, Neuroticism d=0.39) because aspects within domains often show opposite-direction gender differences that cancel out.

---

## Large-scale validation studies provide supplementary norms

### Swiss PERCIVAL study offers the most representative modern norms

The Swiss validation (Haehner et al., 2025) with **N=4,457** nationally representative adults across German, French, and Italian provides the largest and most methodologically rigorous normative sample. Key findings:

- Internal consistency: α=.62–.91 for aspects (Politeness consistently lowest at α≈.70)
- McDonald's ω: all ≥.67
- Six-month test-retest: all correlations ≥.62
- Measurement invariance: partial weak invariance achieved across all three languages
- **Data availability**: OSF repository at osf.io/8sv9k/

### Additional validation samples with reported statistics

| Study | N | Population | Country | Key Finding |
|-------|---|------------|---------|-------------|
| DeYoung et al. (2016) | 870 combined | Community/MTurk | USA | α=.76–.92 across aspects |
| German BFAS-G | 662 | Adults (81% female) | Germany | α=.71–.91; NEO-FFI r=.66–.85 |
| Libyan Arabic | 1,136 | Young adults | Libya | CFA confirmed 10-factor structure |
| MTurk Well-being | 706 | MTurk workers | USA | M age=36; 54% female |

The DeYoung et al. (2016) study found slightly different means in MTurk/community samples: Industriousness M=3.43–3.58, Assertiveness M=3.26–3.67, reflecting sample composition effects.

---

## Converting raw scores to percentiles

Since no official percentile tables exist, conversion requires computing z-scores using the formula: **z = (raw score − M) / SD**, then converting to percentiles via normal distribution. The BFAS shows approximately normal distributions, making this approach valid.

### Percentile conversion reference (using ESCS community norms)

| Percentile | Standard Score | Volatility | Withdrawal | Compassion | Politeness | Industriousness |
|------------|----------------|------------|------------|------------|------------|-----------------|
| 5th | −1.645 | 1.33 | 1.28 | 3.22 | 3.23 | 2.80 |
| 16th | −1.00 | 1.78 | 1.74 | 3.57 | 3.57 | 3.19 |
| 50th | 0.00 | 2.48 | 2.45 | 4.11 | 4.10 | 3.80 |
| 84th | +1.00 | 3.18 | 3.16 | 4.65 | 4.63 | 4.41 |
| 95th | +1.645 | 3.63 | 3.62 | 5.00* | 4.97 | 4.80 |

*Capped at scale maximum of 5.0

| Percentile | Orderliness | Enthusiasm | Assertiveness | Intellect | Openness |
|------------|-------------|------------|---------------|-----------|----------|
| 5th | 2.71 | 2.41 | 2.21 | 2.58 | 2.74 |
| 16th | 3.11 | 2.87 | 2.66 | 3.02 | 3.13 |
| 50th | 3.73 | 3.59 | 3.36 | 3.70 | 3.74 |
| 84th | 4.35 | 4.31 | 4.06 | 4.38 | 4.35 |
| 95th | 4.75 | 4.77 | 4.51 | 4.82 | 4.74 |

---

## Open data sources for computing custom norms

### Direct BFAS resources (all public domain)

1. **IPIP BFAS Scoring Keys** (ipip.ori.org/BFASKeys.htm): Complete 100-item scale with scoring keys and reliability data. This is the official public domain source for BFAS items.

2. **DeYoung Personality Lab** (deyoung.psych.umn.edu/research): Self-rating and peer-rating questionnaire forms in Google Doc format; NEO PI-R to BFAS scoring key for mapping NEO facets to aspects.

3. **Swiss Validation OSF Repository** (osf.io/8sv9k/): N=4,457 dataset with full BFAS responses, analysis scripts, and supplementary materials.

### Large datasets requiring BFAS item mapping

The BFAS uses IPIP items, enabling computation from existing IPIP datasets:

- **Johnson's IPIP-NEO Repository** (osf.io/tbmh5/): **926,463 records** (307K from 300-item version + 619K from 120-item). Raw item responses can be mapped to BFAS aspects using published scoring keys.

- **Open Psychometrics IPIP-BFFM** (openpsychometrics.org/_rawdata/): **1,015,342 records** with raw Big Five responses, demographics (gender, age, country). Excellent for computing population-specific norms.

These massive datasets enable computation of age-specific, country-specific, or demographic-specific percentile tables not available elsewhere.

---

## Reliability benchmarks for quality assessment

Across all validation studies, reliability follows consistent patterns:

| Reliability Type | Typical Range | Benchmark |
|------------------|---------------|-----------|
| Domain α | .84–.89 | Excellent |
| Aspect α | .72–.91 | Good to excellent |
| Politeness α | .62–.76 | Acceptable (consistently lowest) |
| Test-retest (1 month) | .73–.86 | Good |
| Test-retest (6 months) | .62–.70 | Moderate |
| Correlation with factor scores | .87–.91 | Excellent |

Politeness consistently shows the lowest reliability (α≈.70–.75), likely due to its narrower conceptual scope compared to other aspects. For an AI tool, this suggests treating Politeness scores with somewhat wider confidence intervals.

---

## Practical recommendations for implementation

**For general adult assessment**: Use the ESCS community sample norms (M age=52.5) as the primary reference. These provide more representative adult population values than university samples.

**For young adult populations**: Use the university sample norms (M age=19.3), which better reflect the higher neuroticism and lower conscientiousness typical of this age group.

**For gender-specific percentiles**: Apply separate norms for Compassion (d=0.45), Withdrawal (d=0.40), and Politeness (d=0.36). For other aspects, combined norms are acceptable given small effect sizes.

**For cross-cultural use**: The Swiss validation confirms BFAS functions similarly across German, French, and Italian. The Arabic (Libyan) validation suggests the 10-aspect structure holds in collectivist cultures, though absolute score levels may differ. Exercise caution applying English norms to non-Western populations.

**For score interpretation**: Standard error of measurement averages approximately **0.15–0.20** scale points for aspect scores. Differences smaller than 0.3 points (roughly 0.5 SD) should not be over-interpreted.

### Data sources summary

| Source | Sample Size | Access | Best For |
|--------|-------------|--------|----------|
| DeYoung et al. (2007) | 961 | Open access PDF | Original norms, reliability |
| Swiss PERCIVAL | 4,457 | OSF (osf.io/8sv9k/) | Representative adult norms |
| Johnson IPIP-NEO | 926,463 | Open (osf.io/tbmh5/) | Computing custom percentiles |
| Weisberg et al. (2011) | 2,643 | Open access | Gender difference norms |
| Open Psychometrics | 1,015,342 | Open download | Large-scale norm computation |
| IPIP.org | N/A | Public domain | Scoring keys, items |

The BFAS itself is **public domain** and freely available. The primary gap is the absence of published percentile tables, which must be computed from the published means and SDs or derived from the large open datasets available through OSF and Open Psychometrics.