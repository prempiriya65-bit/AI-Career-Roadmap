"""
Skill Gap Finder Page View
Detailed competency comparison matrix separating possessed, improvement, and missing skills
with priority indicators, recommended subtopics, and CSV export.
"""

import streamlit as st
import pandas as pd
from modules.report_generator import generate_csv_report


def render_skill_gap_page():
    """Render segmented tables for possessed, improvement, and missing skills."""
    if not st.session_state.get("has_analysis", False):
        st.info("No active career analysis found. Please generate an assessment on the Home page first.")
        if st.button("Go to Home Form", type="primary"):
            st.session_state["active_page"] = "Home"
            st.rerun()
        return

    profile = st.session_state.get("profile", {})
    skill_analysis = st.session_state.get("skill_analysis", {})
    target_role = profile.get("target_role", "AI Engineer")
    skills_table = skill_analysis.get("skills_table", [])
    possessed = skill_analysis.get("possessed_skills", [])
    improve = skill_analysis.get("improve_skills", [])
    missing = skill_analysis.get("missing_skills", [])

    st.markdown(f"## Skill Gap Finder: {target_role}")
    st.markdown("Detailed breakdown of your competencies contrasted against standard industry role expectations.")

    # Action row: quick search and CSV export
    col_search, col_filter, col_csv = st.columns([2, 1.5, 1.5])
    with col_search:
        search_query = st.text_input("Filter skills by name or topic", placeholder="e.g. Python, SQL, Docker...")

    with col_filter:
        priority_filter = st.selectbox("Filter by Priority", ["All Priorities", "High", "Medium", "Low"])

    with col_csv:
        csv_data = generate_csv_report(skill_analysis)
        st.download_button(
            label="Download Table CSV",
            data=csv_data,
            file_name=f"{target_role.replace(' ', '_')}_Skill_Gap_Matrix.csv",
            mime="text/csv",
            width="stretch"
        )

    # Filter logic
    def filter_skills(skills_list):
        res = []
        for s in skills_list:
            # Query match
            q_match = True
            if search_query.strip():
                q = search_query.strip().lower()
                q_match = (
                    q in s.get("skill", "").lower() or
                    q in s.get("recommended_topics", "").lower() or
                    q in s.get("skill_gap", "").lower()
                )

            # Priority match
            p_match = True
            if priority_filter != "All Priorities":
                p_match = s.get("priority", "").lower() == priority_filter.lower()

            if q_match and p_match:
                res.append(s)
        return res

    # Segmented Tabs
    tab_all, tab_possessed, tab_improve, tab_missing = st.tabs([
        f"All Skills ({len(skills_table)})",
        f"Possessed ({len(possessed)})",
        f"Needs Improvement ({len(improve)})",
        f"Missing Skills ({len(missing)})"
    ])

    with tab_all:
        filtered = filter_skills(skills_table)
        st.markdown(f"Showing **{len(filtered)}** skills matching filters.")
        display_skills_table(filtered)

    with tab_possessed:
        filtered = filter_skills(possessed)
        st.success(f"You have satisfied **{len(possessed)}** requirement(s) for the {target_role} role benchmark!")
        if filtered:
            display_skills_table(filtered)
        else:
            st.info("No possessed skills match the current search filters.")

    with tab_improve:
        filtered = filter_skills(improve)
        st.warning(f"You have **{len(improve)}** skill(s) where you possess baseline knowledge, but the target role requires a higher proficiency level.")
        if filtered:
            display_skills_table(filtered)
        else:
            st.info("No improvement skills match the current search filters.")

    with tab_missing:
        filtered = filter_skills(missing)
        st.error(f"You have **{len(missing)}** skill(s) that were not identified in your profile. Prioritize these in your 8-week roadmap.")
        if filtered:
            display_skills_table(filtered)
        else:
            st.info("No missing skills match the current search filters.")


def display_skills_table(skills_list):
    """Render an attractive interactive dataframe table."""
    if not skills_list:
        st.write("No matching skills to display.")
        return

    # Convert to presentation DataFrame
    df = pd.DataFrame(skills_list)
    cols_order = ["skill", "student_level", "required_level", "status", "priority", "skill_gap", "recommended_topics"]
    available_cols = [c for c in cols_order if c in df.columns]
    df = df[available_cols]

    df = df.rename(columns={
        "skill": "Required Skill",
        "student_level": "Your Level",
        "required_level": "Target Level",
        "status": "Gap Status",
        "priority": "Priority",
        "skill_gap": "Gap Assessment",
        "recommended_topics": "Key Topics to Study"
    })

    st.dataframe(
        df,
        width="stretch",
        hide_index=True,
        column_config={
            "Required Skill": st.column_config.TextColumn("Required Skill", width="medium"),
            "Your Level": st.column_config.TextColumn("Your Level", width="small"),
            "Target Level": st.column_config.TextColumn("Target Level", width="small"),
            "Gap Status": st.column_config.TextColumn("Gap Status", width="small"),
            "Priority": st.column_config.TextColumn("Priority", width="small"),
            "Gap Assessment": st.column_config.TextColumn("Gap Assessment", width="medium"),
            "Key Topics to Study": st.column_config.TextColumn("Key Topics to Study", width="large")
        }
    )
