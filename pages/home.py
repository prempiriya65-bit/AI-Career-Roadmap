"""
Home Page View
Student intake form with input validation, skill level matrix, career role selection,
and triggers for roadmap generation.
"""

import streamlit as st
from modules.gemini_service import is_api_configured
from modules.skill_analyzer import analyze_skill_gaps
from modules.roadmap_generator import generate_learning_roadmap
from modules.project_generator import generate_portfolio_projects
from modules.report_generator import save_analysis_to_history

STANDARD_ROLES = [
    "AI Engineer",
    "Machine Learning Engineer",
    "Data Scientist",
    "Data Analyst",
    "Python Developer",
    "Full Stack Developer",
    "Web Developer",
    "Cloud Engineer",
    "Cybersecurity Engineer",
    "Other (custom job role)"
]

PROGRAMMING_SKILLS_OPTIONS = [
    "Python", "JavaScript", "TypeScript", "SQL", "C++", "Java", "C", "R", "Go", "Rust", "Bash / Shell", "HTML/CSS"
]

TECHNICAL_SKILLS_OPTIONS = [
    "Machine Learning (Scikit-Learn)", "Deep Learning (PyTorch)", "Deep Learning (TensorFlow)",
    "Natural Language Processing (NLP)", "Large Language Models (LLMs / RAG)", "Computer Vision (OpenCV)",
    "Data Analysis (Pandas & NumPy)", "Data Visualization (Plotly / Seaborn)", "SQL Databases (PostgreSQL / MySQL)",
    "NoSQL Databases (MongoDB / Redis)", "RESTful APIs (FastAPI / Flask / Express)", "Docker & Containerization",
    "Kubernetes & Orchestration", "Git & GitHub Version Control", "CI/CD Pipelines (GitHub Actions)",
    "Cloud Computing (AWS)", "Cloud Computing (Google Cloud Platform)", "Cloud Computing (Azure)",
    "Linux Systems Administration", "Network Security & Protocols", "React / Next.js", "Tableau / Power BI"
]


def render_home_page():
    """Render hero header, student intake form, and generation handlers."""
    # Hero Card
    st.markdown("""
    <div class="hero-card">
        <h1>AI Career Roadmap & Skill Gap Finder</h1>
        <p>
            Bridge the gap between where you are and where you want to be in tech.
            Powered by Google Gemini AI, our intelligent career architect analyzes your current competencies,
            identifies missing skills, and creates a realistic 8-week personalized learning curriculum.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # API Key status callout if not configured
    if not is_api_configured():
        st.markdown("""
        <div class="custom-alert custom-alert-warning">
            <strong>Google Gemini API Key Not Configured:</strong>
            To enable real-time Gemini AI generation, please add your key to <code>.streamlit/secrets.toml</code>
            or enter it in the sidebar setup panel. You can also explore the application using our
            <strong>Pre-Computed Demo Profile</strong>.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### Student Profile & Career Goals")
    st.markdown("Fill out your academic and technical background to generate a personalized career roadmap.")

    with st.form("student_intake_form", clear_on_submit=False):
        col1, col2 = st.columns(2)

        with col1:
            student_name = st.text_input(
                "1. Full Name *",
                value=st.session_state.get("input_name", ""),
                placeholder="e.g. Alex Johnson",
                help="Your name will appear on all generated assessment reports and certificates."
            )

            education_level = st.selectbox(
                "2. Current Education Level *",
                options=[
                    "Undergraduate (B.Tech / B.E. / B.Sc / BCA)",
                    "Postgraduate (M.Tech / M.Sc / MCA / MS)",
                    "High School / Diploma",
                    "Self-Taught / Career Switcher",
                    "Working Professional"
                ],
                index=0
            )

            university_name = st.text_input(
                "3. College or University Name (Optional)",
                value=st.session_state.get("input_university", ""),
                placeholder="e.g. National Institute of Technology"
            )

            role_choice = st.selectbox(
                "4. Target Job Role *",
                options=STANDARD_ROLES,
                index=0,
                help="Select the tech role you are aiming for."
            )

            custom_role = ""
            if role_choice == "Other (custom job role)":
                custom_role = st.text_input(
                    "Enter Custom Role Title *",
                    placeholder="e.g. MLOps Engineer, Quantum Computing Researcher"
                )

        with col2:
            study_hours = st.slider(
                "5. Available Study Hours Per Day *",
                min_value=1,
                max_value=12,
                value=int(st.session_state.get("input_hours", 3)),
                help="Realistic hours you can dedicate daily without burnout."
            )

            study_days = st.slider(
                "6. Available Study Days Per Week *",
                min_value=1,
                max_value=7,
                value=int(st.session_state.get("input_days", 5)),
                help="Number of days per week you will follow the study plan."
            )

            weekly_total = study_hours * study_days
            st.info(f"Total Weekly Study Budget: **{weekly_total} hours / week**")

            learning_style = st.selectbox(
                "7. Preferred Learning Style *",
                options=["Practical Projects", "Videos & Interactive Demos", "Documentation & Books", "Mixed (Balanced)"],
                index=3,
                help="Roadmap tasks and resources will be weighted according to your preference."
            )

        st.markdown("---")
        st.markdown("#### Technical Competencies & Experience Levels")

        selected_prog = st.multiselect(
            "8. Current Programming Languages (Select all you have written code in) *",
            options=PROGRAMMING_SKILLS_OPTIONS,
            default=st.session_state.get("input_prog_skills", ["Python"]),
            help="Select languages you have practical experience with."
        )

        selected_tech = st.multiselect(
            "9. Current Technical Frameworks, Libraries & Tools *",
            options=TECHNICAL_SKILLS_OPTIONS,
            default=st.session_state.get("input_tech_skills", ["Data Analysis (Pandas & NumPy)", "Git & GitHub Version Control"]),
            help="Select frameworks, databases, or libraries you know."
        )

        # Experience levels for each selected skill
        all_selected = list(dict.fromkeys(selected_prog + selected_tech))
        skills_with_levels = {}

        if all_selected:
            st.markdown("##### 10. Specify Your Experience Level for Each Selected Skill:")
            st.caption("Be honest about your current level. Do not inflate skills—Gemini uses this to customize your roadmap!")

            # Display skills in a neat 2-column grid
            skill_cols = st.columns(2)
            for idx, skill in enumerate(all_selected):
                with skill_cols[idx % 2]:
                    saved_level = st.session_state.get("skill_levels", {}).get(skill, "Beginner")
                    level_idx = 0 if saved_level == "Beginner" else (1 if saved_level == "Intermediate" else 2)
                    lvl = st.radio(
                        f"**{skill}**",
                        options=["Beginner", "Intermediate", "Advanced"],
                        index=level_idx,
                        key=f"lvl_{skill}",
                        horizontal=True
                    )
                    skills_with_levels[skill] = lvl
        else:
            st.warning("Please select at least one programming language or technical skill to proceed.")

        st.markdown("---")
        btn_col1, btn_col2, btn_col3 = st.columns([2, 1, 1])

        with btn_col1:
            submitted = st.form_submit_button(
                "Generate My Career Roadmap",
                type="primary",
                width="stretch"
            )

        with btn_col2:
            reset_clicked = st.form_submit_button(
                "Reset Form",
                width="stretch"
            )

        with btn_col3:
            demo_clicked = st.form_submit_button(
                "Load Demo Profile",
                width="stretch"
            )

    # Handle Form Actions
    if reset_clicked:
        for k in ["profile", "skill_analysis", "roadmap", "projects", "has_analysis", "skill_levels", "completed_weeks"]:
            if k in st.session_state:
                del st.session_state[k]
        st.success("Form inputs and analysis session reset successfully!")
        st.rerun()

    if demo_clicked:
        load_demo_profile()
        st.rerun()

    if submitted:
        # Validate inputs
        final_role = custom_role.strip() if role_choice == "Other (custom job role)" else role_choice

        if not student_name.strip():
            st.error("Validation Error: Please enter your Full Name.")
            return

        if not final_role:
            st.error("Validation Error: Please specify your target job role.")
            return

        if not skills_with_levels:
            st.error("Validation Error: Please select at least one programming or technical skill.")
            return

        profile = {
            "student_name": student_name.strip(),
            "education_level": education_level,
            "university": university_name.strip(),
            "target_role": final_role,
            "study_hours_per_day": study_hours,
            "study_days_per_week": study_days,
            "learning_style": learning_style,
            "skills_with_levels": skills_with_levels
        }

        # Cache inputs in session state
        st.session_state["profile"] = profile
        st.session_state["input_name"] = student_name.strip()
        st.session_state["input_university"] = university_name.strip()
        st.session_state["input_hours"] = study_hours
        st.session_state["input_days"] = study_days
        st.session_state["input_prog_skills"] = selected_prog
        st.session_state["input_tech_skills"] = selected_tech
        st.session_state["skill_levels"] = skills_with_levels

        # Execute Generation with loading animations
        with st.spinner("Analyzing skill gaps against industry benchmarks..."):
            success_gap, analysis_data, msg_gap = analyze_skill_gaps(profile)

        with st.spinner(f"Generating personalized 8-week learning plan for {final_role}..."):
            success_road, roadmap_data, msg_road = generate_learning_roadmap(profile, analysis_data)

        with st.spinner("Curating high-impact portfolio projects..."):
            success_proj, projects_data, msg_proj = generate_portfolio_projects(profile, analysis_data)

        # Store in session state
        st.session_state["skill_analysis"] = analysis_data
        st.session_state["roadmap"] = roadmap_data
        st.session_state["projects"] = projects_data
        st.session_state["completed_weeks"] = []
        st.session_state["has_analysis"] = True

        # Save to local history
        save_analysis_to_history({
            "profile": profile,
            "skill_analysis": analysis_data,
            "roadmap": roadmap_data,
            "projects": projects_data
        })

        st.success("Career roadmap generated successfully! Redirecting to Dashboard...")
        st.session_state["active_page"] = "My Career Analysis"
        st.rerun()


def load_demo_profile():
    """Load a realistic sample profile for academic testing."""
    profile = {
        "student_name": "Rohan Sharma",
        "education_level": "Undergraduate (B.Tech / B.E. / B.Sc / BCA)",
        "university": "Apex Institute of Technology",
        "target_role": "AI Engineer",
        "study_hours_per_day": 3,
        "study_days_per_week": 5,
        "learning_style": "Mixed (Balanced)",
        "skills_with_levels": {
            "Python": "Intermediate",
            "Data Analysis (Pandas & NumPy)": "Intermediate",
            "Git & GitHub Version Control": "Beginner",
            "SQL": "Beginner"
        }
    }

    _, analysis_data, _ = analyze_skill_gaps(profile)
    _, roadmap_data, _ = generate_learning_roadmap(profile, analysis_data)
    _, projects_data, _ = generate_portfolio_projects(profile, analysis_data)

    st.session_state["profile"] = profile
    st.session_state["skill_analysis"] = analysis_data
    st.session_state["roadmap"] = roadmap_data
    st.session_state["projects"] = projects_data
    st.session_state["completed_weeks"] = []
    st.session_state["has_analysis"] = True
    st.session_state["active_page"] = "My Career Analysis"
    st.toast("Loaded sample student profile for demonstration!", icon="🚀")
