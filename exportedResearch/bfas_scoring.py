"""
BFAS Scoring Engine
Deterministic calculation of raw scores, percentiles, and pattern detection.
No LLM dependencies - pure Python logic.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from scipy.stats import norm
import json


# ============================================================================
# CONSTANTS
# ============================================================================

REVERSE_ITEMS = {
    'openness': [9, 10],
    'intellect': [19, 20],
    'industriousness': [29, 30],
    'orderliness': [39, 40],
    'enthusiasm': [49, 50],
    'assertiveness': [59, 60],
    'compassion': [69, 70],
    'politeness': [79, 80],
    'withdrawal': [89, 90],
    'volatility': [99, 100]
}

# ESCS Community Norms (N=481, ages 20-85, M=52.5)
ESCS_NORMS = {
    'volatility': {'mean': 2.48, 'sd': 0.70},
    'withdrawal': {'mean': 2.45, 'sd': 0.71},
    'compassion': {'mean': 4.11, 'sd': 0.54},
    'politeness': {'mean': 4.10, 'sd': 0.53},
    'industriousness': {'mean': 3.80, 'sd': 0.61},
    'orderliness': {'mean': 3.73, 'sd': 0.62},
    'enthusiasm': {'mean': 3.59, 'sd': 0.72},
    'assertiveness': {'mean': 3.36, 'sd': 0.70},
    'intellect': {'mean': 3.70, 'sd': 0.68},
    'openness': {'mean': 3.74, 'sd': 0.61}
}

# University Norms (N=480, ages 17-61, M=19.3)
UNIVERSITY_NORMS = {
    'volatility': {'mean': 2.72, 'sd': 0.82},
    'withdrawal': {'mean': 2.92, 'sd': 0.75},
    'compassion': {'mean': 3.87, 'sd': 0.65},
    'politeness': {'mean': 3.52, 'sd': 0.67},
    'industriousness': {'mean': 2.84, 'sd': 0.70},
    'orderliness': {'mean': 3.28, 'sd': 0.64},
    'enthusiasm': {'mean': 3.52, 'sd': 0.73},
    'assertiveness': {'mean': 3.21, 'sd': 0.71},
    'intellect': {'mean': 3.39, 'sd': 0.67},
    'openness': {'mean': 3.52, 'sd': 0.64}
}

# Gender adjustments (Cohen's d from Weisberg et al. 2011)
# Only applied for female respondents on these aspects
FEMALE_ADJUSTMENTS = {
    'compassion': 0.24,    # d=0.45 → ~0.24 mean difference
    'withdrawal': 0.28,    # d=0.40 → ~0.28 mean difference
    'politeness': 0.19     # d=0.36 → ~0.19 mean difference
}

ASPECT_TO_DIMENSION = {
    'openness': 'openness_intellect',
    'intellect': 'openness_intellect',
    'industriousness': 'conscientiousness',
    'orderliness': 'conscientiousness',
    'enthusiasm': 'extraversion',
    'assertiveness': 'extraversion',
    'compassion': 'agreeableness',
    'politeness': 'agreeableness',
    'withdrawal': 'neuroticism',
    'volatility': 'neuroticism'
}

ASPECT_RANGES = {
    'openness': (1, 10),
    'intellect': (11, 20),
    'industriousness': (21, 30),
    'orderliness': (31, 40),
    'enthusiasm': (41, 50),
    'assertiveness': (51, 60),
    'compassion': (61, 70),
    'politeness': (71, 80),
    'withdrawal': (81, 90),
    'volatility': (91, 100)
}


# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class AspectScore:
    aspect: str
    raw_score: int
    mean_score: float
    percentile: int
    z_score: float
    gender_adjusted: bool = False


@dataclass
class Asymmetry:
    domain: str
    aspect1: str
    aspect2: str
    percentile_diff: int
    higher_aspect: str
    clinical_significance: bool  # True if diff >= 15 percentile points


@dataclass
class ClinicalFlag:
    pattern: str
    severity: str  # 'low', 'medium', 'high'
    aspects_involved: List[str]
    message: str
    recommendation: str


@dataclass
class BFASProfile:
    aspect_scores: Dict[str, AspectScore]
    dimension_scores: Dict[str, int]
    asymmetries: List[Asymmetry]
    clinical_flags: List[ClinicalFlag]
    age: int
    gender: Optional[str]
    norm_set: str  # 'ESCS' or 'University'


# ============================================================================
# VALIDATION
# ============================================================================

def validate_responses(responses: List[int]) -> None:
    """Validate raw response array."""
    if len(responses) != 100:
        raise ValueError(f"Expected 100 responses, got {len(responses)}")
    
    for i, response in enumerate(responses, 1):
        if not isinstance(response, int):
            raise TypeError(f"Item {i}: response must be integer, got {type(response)}")
        if not 1 <= response <= 5:
            raise ValueError(f"Item {i}: response {response} out of range [1-5]")


def validate_demographics(age: int, gender: Optional[str]) -> None:
    """Validate demographic inputs."""
    if not isinstance(age, int) or age < 17 or age > 100:
        raise ValueError(f"Age must be integer 17-100, got {age}")
    
    if gender is not None:
        valid_genders = ['male', 'female', 'man', 'woman', 'kvinna', 'kvinnlig', 'manlig']
        if gender.lower() not in valid_genders:
            raise ValueError(f"Gender must be one of {valid_genders} or None")


# ============================================================================
# SCORING FUNCTIONS
# ============================================================================

def reverse_code(response: int) -> int:
    """Apply reverse coding formula: 6 - response."""
    return 6 - response


def calculate_aspect_raw_score(responses: List[int], aspect: str) -> int:
    """Calculate raw score for a single aspect (10 items)."""
    start, end = ASPECT_RANGES[aspect]
    aspect_responses = responses[start-1:end]  # Convert to 0-indexed
    
    # Apply reverse coding to last 2 items
    reverse_items = REVERSE_ITEMS[aspect]
    score = 0
    
    for i, response in enumerate(aspect_responses, start=start):
        if i in reverse_items:
            score += reverse_code(response)
        else:
            score += response
    
    return score


def select_norms(age: int, gender: Optional[str]) -> tuple:
    """Select appropriate normative dataset based on age and gender."""
    # Age-based norm selection
    if age < 25:
        base_norms = UNIVERSITY_NORMS.copy()
        norm_set = 'University'
    else:
        base_norms = ESCS_NORMS.copy()
        norm_set = 'ESCS'
    
    # Deep copy to avoid modifying constants
    norms = {}
    for aspect, values in base_norms.items():
        norms[aspect] = values.copy()
    
    # Gender adjustment for females
    if gender and gender.lower() in ['female', 'woman', 'kvinna', 'kvinnlig']:
        for aspect in FEMALE_ADJUSTMENTS:
            norms[aspect]['mean'] += FEMALE_ADJUSTMENTS[aspect]
    
    return norms, norm_set


def calculate_percentile(mean_score: float, norm_mean: float, norm_sd: float) -> int:
    """Convert mean item score to percentile using z-score."""
    z_score = (mean_score - norm_mean) / norm_sd
    percentile = norm.cdf(z_score) * 100
    return round(percentile)


def calculate_all_scores(
    responses: List[int],
    age: int,
    gender: Optional[str] = None
) -> BFASProfile:
    """
    Main scoring function. Returns complete BFAS profile.
    
    Args:
        responses: List of 100 integers (1-5)
        age: Integer 17-100
        gender: Optional str ('male', 'female', etc.)
    
    Returns:
        BFASProfile with all scores, asymmetries, and clinical flags
    """
    validate_responses(responses)
    validate_demographics(age, gender)
    
    norms, norm_set = select_norms(age, gender)
    aspect_scores = {}
    dimension_scores = {}
    
    # Calculate aspect scores
    for aspect in ASPECT_RANGES.keys():
        raw_score = calculate_aspect_raw_score(responses, aspect)
        mean_score = raw_score / 10  # BFAS uses mean item scores
        
        norm = norms[aspect]
        percentile = calculate_percentile(mean_score, norm['mean'], norm['sd'])
        z_score = (mean_score - norm['mean']) / norm['sd']
        
        gender_adjusted = (
            gender and 
            gender.lower() in ['female', 'woman', 'kvinna', 'kvinnlig'] and
            aspect in FEMALE_ADJUSTMENTS
        )
        
        aspect_scores[aspect] = AspectScore(
            aspect=aspect,
            raw_score=raw_score,
            mean_score=mean_score,
            percentile=percentile,
            z_score=z_score,
            gender_adjusted=gender_adjusted
        )
    
    # Calculate dimension scores
    dimension_pairs = {
        'openness_intellect': ['openness', 'intellect'],
        'conscientiousness': ['industriousness', 'orderliness'],
        'extraversion': ['enthusiasm', 'assertiveness'],
        'agreeableness': ['compassion', 'politeness'],
        'neuroticism': ['withdrawal', 'volatility']
    }
    
    for dimension, aspects in dimension_pairs.items():
        dimension_scores[dimension] = sum(
            aspect_scores[asp].raw_score for asp in aspects
        )
    
    # Detect asymmetries
    asymmetries = detect_asymmetries(aspect_scores)
    
    # Clinical pattern detection
    clinical_flags = detect_clinical_patterns(aspect_scores)
    
    return BFASProfile(
        aspect_scores=aspect_scores,
        dimension_scores=dimension_scores,
        asymmetries=asymmetries,
        clinical_flags=clinical_flags,
        age=age,
        gender=gender,
        norm_set=norm_set
    )


# ============================================================================
# PATTERN DETECTION
# ============================================================================

def detect_asymmetries(aspect_scores: Dict[str, AspectScore]) -> List[Asymmetry]:
    """Detect clinically significant within-domain asymmetries."""
    asymmetries = []
    
    pairs = [
        ('openness_intellect', 'intellect', 'openness'),
        ('conscientiousness', 'industriousness', 'orderliness'),
        ('extraversion', 'enthusiasm', 'assertiveness'),
        ('agreeableness', 'compassion', 'politeness'),
        ('neuroticism', 'withdrawal', 'volatility')
    ]
    
    for domain, aspect1, aspect2 in pairs:
        pct1 = aspect_scores[aspect1].percentile
        pct2 = aspect_scores[aspect2].percentile
        diff = abs(pct1 - pct2)
        
        # Significant if >= 15 percentile points
        if diff >= 15:
            higher = aspect1 if pct1 > pct2 else aspect2
            asymmetries.append(Asymmetry(
                domain=domain,
                aspect1=aspect1,
                aspect2=aspect2,
                percentile_diff=diff,
                higher_aspect=higher,
                clinical_significance=True
            ))
    
    return asymmetries


def detect_clinical_patterns(aspect_scores: Dict[str, AspectScore]) -> List[ClinicalFlag]:
    """Detect high-risk clinical patterns from research literature."""
    flags = []
    
    # Get percentiles for easier access
    p = {asp: score.percentile for asp, score in aspect_scores.items()}
    
    # Pattern 1: Maximum Dysregulation
    if p['volatility'] >= 75 and p['withdrawal'] >= 75:
        flags.append(ClinicalFlag(
            pattern='max_dysregulation',
            severity='high',
            aspects_involved=['volatility', 'withdrawal'],
            message='Combined internalizing and externalizing distress pattern',
            recommendation='Priority for clinical evaluation. Highest psychopathology risk.'
        ))
    
    # Pattern 2: Violence/Aggression Risk
    if p['volatility'] >= 75 and p['politeness'] <= 25 and p['compassion'] <= 25:
        flags.append(ClinicalFlag(
            pattern='aggression_risk',
            severity='high',
            aspects_involved=['volatility', 'politeness', 'compassion'],
            message='Reactive aggression combined with antagonism',
            recommendation='Screen for ASPD/NPD. Consider anger management.'
        ))
    
    # Pattern 3: Severe Depression/Suicide Risk
    if p['withdrawal'] >= 75 and p['enthusiasm'] <= 25 and p['assertiveness'] <= 25:
        flags.append(ClinicalFlag(
            pattern='depression_suicide_risk',
            severity='high',
            aspects_involved=['withdrawal', 'enthusiasm', 'assertiveness'],
            message='Passive avoidance + anhedonia + low agency pattern',
            recommendation='Depression screening and safety planning indicated.'
        ))
    
    # Pattern 4: Impulsive Self-Harm
    if (p['industriousness'] <= 25 and p['orderliness'] <= 25 and 
        p['volatility'] >= 75):
        flags.append(ClinicalFlag(
            pattern='impulsive_selfharm',
            severity='high',
            aspects_involved=['industriousness', 'orderliness', 'volatility'],
            message='Impulsivity combined with emotional dysregulation',
            recommendation='Safety planning priority. Consider DBT.'
        ))
    
    # Pattern 5: Psychosis-Proneness
    if p['openness'] >= 75 and p['intellect'] <= 25 and p['volatility'] >= 75:
        flags.append(ClinicalFlag(
            pattern='psychosis_proneness',
            severity='medium',
            aspects_involved=['openness', 'intellect', 'volatility'],
            message='Pattern detection without critical evaluation plus dysregulation',
            recommendation='Screen for schizotypal features. Not diagnostic.'
        ))
    
    # Pattern 6: Hypomania Risk
    if p['assertiveness'] >= 75 and p['volatility'] >= 75 and p['withdrawal'] <= 25:
        flags.append(ClinicalFlag(
            pattern='hypomania_risk',
            severity='medium',
            aspects_involved=['assertiveness', 'volatility', 'withdrawal'],
            message='Elevated hypomania risk pattern',
            recommendation='Consider bipolar spectrum screening.'
        ))
    
    # Pattern 7: Perfectionism Paralysis (common, lower severity)
    if p['orderliness'] >= 75 and p['industriousness'] <= 40:
        flags.append(ClinicalFlag(
            pattern='perfectionism_paralysis',
            severity='low',
            aspects_involved=['orderliness', 'industriousness'],
            message='High organization without matching drive',
            recommendation='May indicate anxiety-driven perfectionism. Explore barriers to sustained effort.'
        ))
    
    return flags


# ============================================================================
# OUTPUT FORMATTING
# ============================================================================

def format_profile_summary(profile: BFASProfile) -> Dict:
    """Format profile for JSON export or LLM consumption."""
    return {
        'metadata': {
            'age': profile.age,
            'gender': profile.gender,
            'norm_set': profile.norm_set
        },
        'aspect_scores': {
            aspect: {
                'raw_score': score.raw_score,
                'mean_score': round(score.mean_score, 2),
                'percentile': score.percentile,
                'z_score': round(score.z_score, 2),
                'gender_adjusted': score.gender_adjusted
            }
            for aspect, score in profile.aspect_scores.items()
        },
        'dimension_scores': profile.dimension_scores,
        'asymmetries': [
            {
                'domain': asym.domain,
                'higher_aspect': asym.higher_aspect,
                'percentile_difference': asym.percentile_diff,
                'aspects': [asym.aspect1, asym.aspect2]
            }
            for asym in profile.asymmetries
        ],
        'clinical_flags': [
            {
                'pattern': flag.pattern,
                'severity': flag.severity,
                'aspects': flag.aspects_involved,
                'message': flag.message,
                'recommendation': flag.recommendation
            }
            for flag in profile.clinical_flags
        ]
    }


# ============================================================================
# TESTING
# ============================================================================

if __name__ == '__main__':
    # Test case: Sara (29F, PhD)
    test_responses = [
        4, 3, 4, 3, 3, 3, 4, 3, 3, 3,  # Openness
        4, 5, 4, 4, 4, 5, 4, 4, 3, 3,  # Intellect
        5, 4, 5, 4, 4, 4, 5, 4, 3, 3,  # Industriousness
        3, 4, 3, 3, 3, 4, 3, 3, 3, 3,  # Orderliness
        3, 2, 3, 3, 2, 3, 3, 2, 3, 3,  # Enthusiasm
        3, 3, 4, 3, 3, 3, 3, 3, 3, 4,  # Assertiveness
        4, 4, 4, 4, 3, 4, 5, 4, 3, 3,  # Compassion
        4, 3, 4, 3, 4, 3, 4, 3, 3, 3,  # Politeness
        4, 3, 3, 3, 3, 3, 3, 4, 3, 3,  # Withdrawal
        3, 2, 3, 2, 2, 3, 2, 3, 3, 3   # Volatility
    ]
    
    profile = calculate_all_scores(test_responses, age=29, gender='female')
    summary = format_profile_summary(profile)
    
    print(json.dumps(summary, indent=2))
