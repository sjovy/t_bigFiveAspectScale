"""
BFAS Personality Assessment - Streamlit App
AI-powered Big Five Aspect Scale assessment with LLM interpretation.
"""

import streamlit as st
import json
import os
from dotenv import load_dotenv
from anthropic import Anthropic

# Import scoring engine
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'exportedResearch'))
from bfas_scoring import calculate_all_scores, format_profile_summary

# Load environment
load_dotenv()

# Page config
st.set_page_config(
    page_title="BFAS Personality Assessment",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .disclaimer-box {
        background-color: #fff3cd;
        border: 1px solid #ffc107;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .results-card {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    .aspect-score {
        display: flex;
        justify-content: space-between;
        padding: 0.5rem 0;
        border-bottom: 1px solid #eee;
    }
    .clinical-warning {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .stProgress > div > div > div > div {
        background-color: #4CAF50;
    }
</style>
""", unsafe_allow_html=True)


# Load instrument
@st.cache_data
def load_instrument():
    with open('exportedResearch/bfas_instrument.json', 'r', encoding='utf-8') as f:
        return json.load(f)


# Load RAG knowledge base
@st.cache_data
def load_knowledge_base():
    with open('exportedResearch/BFAS_Complete_RAG_Knowledge_Base.md', 'r', encoding='utf-8') as f:
        return f.read()


@st.dialog("About the Developer")
def about_modal():
    """Display About modal with developer bio and coffee link."""
    st.markdown("""
    63 years of age. Unemployed and totally age discriminated on the Swedish job market (look it up, I dare you). Somehow still very young at heart and love to stay ahead of the crowd regarding everything AI. Using AI for programming and sometimes with embedded AI capabilities inside apps. 100% autodidact. Broke as a biatch, so hopefully one of these apps will land me a job someday. Meanwhile, if you enjoy my work, please buy me a coffee to help me stay afloat.
    """)

    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown("""
        <a href="https://www.buymeacoffee.com/thomassjovy" target="_blank">
        <img src="https://cdn.buymeacoffee.com/buttons/v2/default-green.png" alt="Buy Me A Coffee" style="height: 40px !important;width: 150px !important;" />
        </a>
        """, unsafe_allow_html=True)


def generate_interpretation(profile_summary: dict, knowledge_base: str) -> str:
    """Generate natural language interpretation using Claude."""
    client = Anthropic()

    prompt = f"""You are an expert personality psychologist interpreting BFAS (Big Five Aspect Scale) results.

KNOWLEDGE BASE:
{knowledge_base}

PROFILE DATA:
{json.dumps(profile_summary, indent=2)}

Generate a personalized, engaging interpretation (800-1200 words) that:

1. Opens with a brief overview of what makes this profile distinctive
2. Covers each of the 5 dimensions, highlighting:
   - The person's percentile scores for both aspects
   - What these scores mean behaviorally (use specific examples)
   - Any significant asymmetries between aspects within a dimension
3. Identifies 2-3 key strengths from the profile
4. Notes 1-2 potential growth areas (phrased constructively)
5. If clinical flags are present, mention them sensitively with appropriate disclaimers

IMPORTANT GUIDELINES:
- Use second person ("you") throughout
- Be warm but scientifically grounded
- Avoid clinical/diagnostic language unless flags are present
- Highlight the unique pattern of aspects, not just domain scores
- Use the knowledge base for evidence-based interpretations
- End with an empowering reflection

Do NOT include:
- Rigid structure with headers for each dimension
- Repetitive percentile listings
- Generic personality descriptions
- Medical advice

Write in flowing paragraphs that feel personalized and insightful."""

    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text


def render_welcome():
    """Render welcome/landing page."""
    st.markdown('<p class="main-header">Discover Your Personality in 10 Dimensions</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">A modern AI-powered personality assessment using the Big Five Aspect Scale</p>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Welcome image
        st.image("ai-generated-9556075_1280.png", use_container_width=True)

        st.markdown("""
        ### Welcome!

        Hi, and welcome to this personality assessment tool. Whether you're here out of curiosity
        about yourself or exploring how AI can assist in psychological assessment, you've come to the right place.

        ### Why BFAS?

        The **Big Five Aspect Scale** is one of the few personality instruments recognized by
        research psychologists as having genuine scientific validity. Unlike popular online tests,
        BFAS is grounded in decades of peer-reviewed research and measures personality across
        **5 major dimensions** and **10 specific aspects** — providing insights that generic tests simply cannot.

        **The 10 Aspects:**
        - **Openness/Intellect**: Openness (aesthetic) + Intellect (abstract thinking)
        - **Conscientiousness**: Industriousness (drive) + Orderliness (organization)
        - **Extraversion**: Enthusiasm (warmth) + Assertiveness (leadership)
        - **Agreeableness**: Compassion (empathy) + Politeness (respect)
        - **Neuroticism**: Withdrawal (anxiety) + Volatility (reactivity)

        ### AI-Powered Interpretation

        Your results are interpreted by an AI trained on the scientific literature behind BFAS.
        While this doesn't replace a professional consultation, AI-assisted interpretation can
        provide valuable preliminary insights — and is increasingly used as a support tool
        even by professionals in the field.
        """)

        st.markdown("""
        <div class="disclaimer-box">
        <strong>⚠️ Important Disclaimer</strong><br>
        This is an <strong>educational demonstration</strong> of AI and programming capabilities.
        It is NOT a clinical diagnostic tool or substitute for professional psychological evaluation.
        For clinical concerns, always consult a licensed professional. <strong>We do not keep any data that can be traced back to you.</strong>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Start Anonymous Assessment (15-20 min)", type="primary", use_container_width=True):
            st.session_state.page = 'demographics'
            st.rerun()

        # Dev mode: skip to results with test profile
        if os.getenv('DEV_MODE') == '1':
            st.markdown("---")
            st.markdown("**🛠 Dev Mode**")
            with open('exportedResearch/test_profiles.json', 'r') as f:
                test_profiles = json.load(f)
            profile_name = st.selectbox("Load test profile:", list(test_profiles.keys()))
            if st.button("Skip to Results", type="secondary"):
                profile = test_profiles[profile_name]
                st.session_state.responses = {i+1: profile['responses'][i] for i in range(100)}
                st.session_state.age = profile.get('age', 30)
                st.session_state.gender = profile.get('gender')
                st.session_state.page = 'results'
                st.rerun()

        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #999; font-size: 0.85em;">
        Developed in partnership with Claude Code  |
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("About the Developer", key="about_btn", use_container_width=True):
                about_modal()


def render_demographics():
    """Collect demographic info before assessment."""
    st.markdown("### Before We Begin")
    st.markdown("We need a few details to compare your scores to appropriate reference groups.")

    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("Age", min_value=17, max_value=100, value=30)

    with col2:
        gender = st.selectbox("Gender (optional)",
                             options=["Prefer not to say", "Male", "Female"],
                             index=0)

    st.markdown("""
    **Tips for accurate results:**
    - Answer how you **actually are**, not how you wish to be
    - Go with your first instinct
    - Consider your general patterns, not just recent behavior
    """)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Begin Assessment", type="primary", use_container_width=True):
            st.session_state.age = age
            st.session_state.gender = None if gender == "Prefer not to say" else gender.lower()
            st.session_state.page = 'assessment'
            st.session_state.responses = {}
            st.session_state.current_item = 0
            st.rerun()


def render_assessment():
    """Render the questionnaire."""
    instrument = load_instrument()
    items = instrument['items']
    scale_labels = instrument['instrument']['scale']['labels']

    # Initialize responses if needed
    if 'responses' not in st.session_state:
        st.session_state.responses = {}

    # Progress bar
    progress = len(st.session_state.responses) / 100
    st.progress(progress)
    st.markdown(f"**Question {len(st.session_state.responses) + 1} of 100** | "
                f"~{max(1, int((100 - len(st.session_state.responses)) * 0.15))} minutes remaining")

    # Display items in batches of 10 (one aspect at a time)
    current_aspect_start = (len(st.session_state.responses) // 10) * 10
    current_items = items[current_aspect_start:current_aspect_start + 10]

    if current_items:
        aspect_name = current_items[0]['aspect'].replace('_', ' ').title()
        dimension_name = current_items[0]['dimension'].replace('_', ' ').title()
        st.markdown(f"### {dimension_name} - {aspect_name}")

        with st.form(key=f"aspect_form_{current_aspect_start}"):
            responses_batch = {}

            for item in current_items:
                item_id = item['id']

                # Skip if already answered
                if item_id in st.session_state.responses:
                    continue

                st.markdown(f"**{item_id}.** {item['text']}")

                response = st.radio(
                    f"item_{item_id}",
                    options=[1, 2, 3, 4, 5],
                    format_func=lambda x: scale_labels[str(x)],
                    horizontal=True,
                    key=f"radio_{item_id}",
                    label_visibility="collapsed"
                )
                responses_batch[item_id] = response
                st.markdown("---")

            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.form_submit_button("Continue", type="primary", use_container_width=True):
                    st.session_state.responses.update(responses_batch)

                    # Check if complete
                    if len(st.session_state.responses) >= 100:
                        st.session_state.page = 'results'
                    st.rerun()
    else:
        # Should not happen, but safety
        st.session_state.page = 'results'
        st.rerun()


def render_results():
    """Render results page with scores and interpretation."""
    st.markdown('<p class="main-header">Your BFAS Personality Profile</p>', unsafe_allow_html=True)

    # Convert responses dict to ordered list
    responses_list = [st.session_state.responses[i] for i in range(1, 101)]

    # Calculate scores
    with st.spinner("Calculating your scores..."):
        profile = calculate_all_scores(
            responses_list,
            st.session_state.age,
            st.session_state.gender
        )
        summary = format_profile_summary(profile)

    # Store for potential reuse
    st.session_state.profile_summary = summary

    # Display scores visualization
    st.markdown("### Your Scores at a Glance")

    # Create two columns for the chart
    col1, col2 = st.columns([2, 1])

    with col1:
        # Aspect scores chart
        import plotly.graph_objects as go

        aspects = list(summary['aspect_scores'].keys())
        percentiles = [summary['aspect_scores'][a]['percentile'] for a in aspects]

        # Color by dimension
        dimension_colors = {
            'openness': '#9C27B0', 'intellect': '#9C27B0',
            'industriousness': '#2196F3', 'orderliness': '#2196F3',
            'enthusiasm': '#FF9800', 'assertiveness': '#FF9800',
            'compassion': '#4CAF50', 'politeness': '#4CAF50',
            'withdrawal': '#F44336', 'volatility': '#F44336'
        }
        colors = [dimension_colors[a] for a in aspects]

        fig = go.Figure(data=[
            go.Bar(
                x=percentiles,
                y=[a.replace('_', ' ').title() for a in aspects],
                orientation='h',
                marker_color=colors,
                text=[f"{p}%" for p in percentiles],
                textposition='outside'
            )
        ])

        fig.update_layout(
            title="Percentile Scores by Aspect",
            xaxis_title="Percentile",
            xaxis=dict(range=[0, 105]),
            height=500,
            margin=dict(l=20, r=20, t=40, b=20)
        )

        # Add reference lines
        fig.add_vline(x=25, line_dash="dash", line_color="gray", opacity=0.5)
        fig.add_vline(x=50, line_dash="dash", line_color="gray", opacity=0.5)
        fig.add_vline(x=75, line_dash="dash", line_color="gray", opacity=0.5)

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("""
        **Reading Your Scores:**

        - **1-25%**: Lower than most
        - **25-75%**: About average
        - **75-99%**: Higher than most

        **Color Legend:**
        - 🟣 Openness/Intellect
        - 🔵 Conscientiousness
        - 🟠 Extraversion
        - 🟢 Agreeableness
        - 🔴 Neuroticism
        """)

        st.markdown(f"""
        **Your Profile Info:**
        - Age: {summary['metadata']['age']}
        - Norms: {summary['metadata']['norm_set']}
        """)

    # Clinical flags warning
    if summary['clinical_flags']:
        st.markdown("""
        <div class="clinical-warning">
        <strong>⚠️ Patterns Detected</strong><br>
        Your profile shows patterns that research associates with certain tendencies.
        This is <strong>informational only</strong> - not a diagnosis.
        If you have concerns about your mental health, please consult a licensed professional.
        </div>
        """, unsafe_allow_html=True)

        for flag in summary['clinical_flags']:
            with st.expander(f"Pattern: {flag['pattern'].replace('_', ' ').title()}"):
                st.write(f"**Severity:** {flag['severity']}")
                st.write(f"**Aspects involved:** {', '.join(flag['aspects'])}")
                st.write(f"**Note:** {flag['message']}")

    # Asymmetries
    if summary['asymmetries']:
        st.markdown("### Notable Patterns in Your Profile")
        for asym in summary['asymmetries']:
            st.info(f"**{asym['domain'].replace('_', ' ').title()}:** "
                   f"Your {asym['higher_aspect'].replace('_', ' ')} is notably higher than "
                   f"your {[a for a in asym['aspects'] if a != asym['higher_aspect']][0].replace('_', ' ')} "
                   f"({asym['percentile_difference']} percentile points difference)")

    # AI Interpretation
    st.markdown("---")
    st.markdown("### Your Personalized Interpretation")

    with st.spinner("Generating your personalized profile interpretation... (30-60 seconds)"):
        try:
            knowledge_base = load_knowledge_base()
            interpretation = generate_interpretation(summary, knowledge_base)
            st.session_state.interpretation = interpretation
        except Exception as e:
            interpretation = f"Unable to generate interpretation: {str(e)}"
            st.error(interpretation)

    st.markdown(interpretation)

    # Actions
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        # Download results as JSON
        results_json = json.dumps({
            'scores': summary,
            'interpretation': st.session_state.get('interpretation', '')
        }, indent=2)
        st.download_button(
            "Download Results (JSON)",
            data=results_json,
            file_name="bfas_results.json",
            mime="application/json",
            use_container_width=True
        )

    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #999; font-size: 0.85em;">
    Interpretation generated by Claude Haiku 4.5
    </div>
    """, unsafe_allow_html=True)


def main():
    """Main app entry point."""
    # Initialize session state
    if 'page' not in st.session_state:
        st.session_state.page = 'welcome'

    # Route to appropriate page
    if st.session_state.page == 'welcome':
        render_welcome()
    elif st.session_state.page == 'demographics':
        render_demographics()
    elif st.session_state.page == 'assessment':
        render_assessment()
    elif st.session_state.page == 'results':
        render_results()


if __name__ == "__main__":
    main()
