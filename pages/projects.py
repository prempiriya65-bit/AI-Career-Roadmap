"""
Portfolio Projects Page View
Curated portfolio project specifications (Beginner, Intermediate, Advanced)
with problem statements, architecture, tech stack pills, step-by-step guides, and expected deliverables.
"""

import streamlit as st
from modules.project_generator import generate_portfolio_projects


def render_projects_page():
    """Render exactly 3 tiered portfolio project blueprints."""
    if not st.session_state.get("has_analysis", False):
        st.info("No active career analysis found. Please generate an assessment on the Home page first.")
        if st.button("Go to Home Form", type="primary"):
            st.session_state["active_page"] = "Home"
            st.rerun()
        return

    profile = st.session_state.get("profile", {})
    skill_analysis = st.session_state.get("skill_analysis", {})
    projects = st.session_state.get("projects", [])
    target_role = profile.get("target_role", "AI Engineer")

    # Header
    col_h1, col_h2 = st.columns([3, 1])
    with col_h1:
        st.markdown(f"## Recommended Portfolio Projects: {target_role}")
        st.markdown("Three real-world project blueprints designed to demonstrate progressive industry competency to recruiters.")

    with col_h2:
        if st.button("Regenerate Projects", width="stretch"):
            with st.spinner("Regenerating portfolio project blueprints..."):
                _, new_projects, _ = generate_portfolio_projects(profile, skill_analysis)
                st.session_state["projects"] = new_projects
                st.success("Refreshed portfolio project ideas!")
                st.rerun()

    # Render each project
    diff_colors = {
        "Beginner": ("#DCFCE7", "#166534", "Foundation Tier"),
        "Intermediate": ("#FEF3C7", "#92400E", "Production Tier"),
        "Advanced": ("#DBEAFE", "#1E40AF", "Capstone / Distributed Tier")
    }

    for idx, p in enumerate(projects, start=1):
        diff = p.get("difficulty_level", "Intermediate")
        bg_col, txt_col, tier_label = diff_colors.get(diff, ("#F1F5F9", "#334155", "Standard Tier"))

        with st.container():
            st.markdown(f"""
            <div class="project-card">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.75rem;">
                    <div>
                        <span style="background-color: {bg_col}; color: {txt_col}; font-size: 0.75rem; font-weight: 700; padding: 0.25rem 0.65rem; border-radius: 9999px;">
                            {diff.upper()} • {tier_label}
                        </span>
                        <h3 style="margin-top: 0.5rem; margin-bottom: 0.25rem; color: #0F172A;">
                            Project {idx}: {p.get('title', 'Portfolio Project')}
                        </h3>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Details inside structured layout
            col_left, col_right = st.columns([1.8, 1.2])

            with col_left:
                st.markdown("**Problem Statement:**")
                st.write(p.get("problem_statement", "No problem statement provided."))

                st.markdown("**Project Description:**")
                st.write(p.get("description", "No description provided."))

                st.markdown("**Expected Deliverable / Output:**")
                st.success(p.get("expected_output", "A working, tested portfolio repository."))

            with col_right:
                st.markdown("**Required Technologies:**")
                techs = p.get("technologies", [])
                tags_html = "".join([f'<span class="tech-tag">{t}</span>' for t in techs])
                st.markdown(tags_html, unsafe_allow_html=True)

                st.markdown("**Key Features:**")
                features = p.get("main_features", [])
                for f in features:
                    st.markdown(f"- {f}")

            with st.expander("View Chronological Implementation Steps", expanded=False):
                steps = p.get("implementation_steps", [])
                for s in steps:
                    st.markdown(f"- {s}")

            st.markdown("<br>", unsafe_allow_html=True)
