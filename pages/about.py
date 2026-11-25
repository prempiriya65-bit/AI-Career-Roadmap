"""
About Project Page View
Academic and architectural documentation of the AI Career Roadmap & Skill Gap Finder,
covering methodology, architecture, scoring mechanics, and tech stack.
"""

import streamlit as st


def render_about_page():
    """Render project architecture, methodology, and academic details."""
    st.markdown("## About the Project")
    st.markdown("### AI Career Roadmap & Skill Gap Finder Web Application")

    st.markdown("""
    <div class="saas-card">
        <h4 style="color: #2563EB; margin-bottom: 0.5rem;">Academic & Industry Motivation</h4>
        <p>
            Computer Science and engineering students frequently know their target career (e.g. AI Engineer,
            Machine Learning Engineer, Data Scientist) but face significant ambiguity regarding:
        </p>
        <ul>
            <li>Which foundational and specialized skills are strictly expected in production environments.</li>
            <li>Which competencies they already possess at junior vs production levels.</li>
            <li>The priority order and time commitments required to bridge those gaps.</li>
            <li>What realistic, non-trivial portfolio projects demonstrate proof of skill to recruiters.</li>
        </ul>
        <p>
            This application leverages the <strong>Google Gemini API (via the official <code>google-genai</code> SDK)</strong>
            combined with rigorous software engineering benchmarks to generate personalized, time-bounded learning roadmaps.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Technology Stack")
        st.markdown("""
        - **Frontend Framework:** Streamlit (v1.50+)
        - **Programming Language:** Python 3.10+
        - **Generative AI SDK:** `google-genai` (Official Google GenAI SDK)
        - **AI Foundation Models:** Gemini 2.5 Flash / Gemini 2.0 Flash / Gemini 1.5 Flash
        - **Data Visualizations:** Plotly Interactive Graphs & Gauges
        - **Data Processing:** Pandas & NumPy
        - **PDF Generation Engine:** FPDF2 (Clean A4 PDF Export)
        - **Security & Configuration:** Streamlit Secrets (`secrets.toml`)
        - **Storage:** Local JSON History Persistence (`data/history.json`)
        """)

    with col2:
        st.markdown("### Mathematical Readiness Formula")
        st.markdown("""
        Rather than displaying an arbitrary percentage, the **Overall Skill Readiness Score**
        is calculated using a transparent weighted scoring algorithm:

        $$\\text{Readiness Score} = \\left( \\frac{\\sum \\min(S_i, R_i) \\times W_i}{\\sum R_i \\times W_i} \\right) \\times 100$$

        Where:
        - $S_i$: Student's attained level for skill $i$ (None=0, Beg=1, Int=2, Adv=3)
        - $R_i$: Target role requirement for skill $i$ (Beg=1, Int=2, Adv=3)
        - $W_i$: Priority weight of skill $i$ (High=3, Medium=2, Low=1)
        """)

    st.markdown("---")
    st.markdown("### Architectural Pipeline")
    st.markdown("""
    1. **Intake & Profile Parsing:** Student inputs education, target role, time budget, and self-assessed skill levels.
    2. **Grounding & Benchmark Lookup:** Role benchmarks provide target competencies and priority weightings.
    3. **LLM Gap Analysis:** Gemini API generates structured JSON evaluating current vs required competency, gap status, and actionable subtopics.
    4. **Roadmap Synthesis:** An 8-week progressive curriculum is generated respecting the exact daily/weekly hours budget and learning style.
    5. **Portfolio Project Generation:** Exactly 3 tailored projects (Beginner, Intermediate, Capstone) are formulated with problem statements and implementation steps.
    6. **Visualization & Report Export:** Plotly charts render metrics; users can export reports in PDF, TXT, or CSV.
    """)

    st.markdown("---")
    st.markdown("### Project Demonstration Checklist for Evaluators")
    st.markdown("""
    - [x] Responsive, modern UI with white background and navy/blue accents.
    - [x] All 10 job role options supported including custom role input.
    - [x] Interactive skill experience selection (Beginner, Intermediate, Advanced).
    - [x] Separation of Possessed, Needs Improvement, and Missing skills.
    - [x] Complete 8-week roadmap respecting weekly hours with daily tasks and exercises.
    - [x] Exactly 3 portfolio project ideas with implementation steps.
    - [x] Verified, working learning resource links.
    - [x] 4 distinct Plotly charts (Current vs Required, Donut Distribution, Priority Bar, 8-Week Hours).
    - [x] PDF, TXT, and CSV download capabilities.
    - [x] Local assessment history persistence and reload.
    - [x] Secure API key handling via `.streamlit/secrets.toml`.
    """)
