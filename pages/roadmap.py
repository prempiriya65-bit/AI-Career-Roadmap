"""
8-Week Roadmap Page View
Interactive 8-week personalized learning curriculum with daily tasks, practical exercises,
weekly milestone projects, progress tracking, and roadmap regeneration.
"""

import streamlit as st
from modules.roadmap_generator import generate_learning_roadmap


def render_roadmap_page():
    """Render the 8-week curriculum timeline with interactive collapsible modules."""
    if not st.session_state.get("has_analysis", False):
        st.info("No active career analysis found. Please generate an assessment on the Home page first.")
        if st.button("Go to Home Form", type="primary"):
            st.session_state["active_page"] = "Home"
            st.rerun()
        return

    profile = st.session_state.get("profile", {})
    skill_analysis = st.session_state.get("skill_analysis", {})
    roadmap = st.session_state.get("roadmap", [])
    target_role = profile.get("target_role", "AI Engineer")

    daily_h = profile.get("study_hours_per_day", 2)
    days_w = profile.get("study_days_per_week", 5)
    weekly_h = daily_h * days_w
    learning_style = profile.get("learning_style", "Mixed")

    # Header section with regeneration button
    h_col1, h_col2 = st.columns([3, 1])
    with h_col1:
        st.markdown(f"## Personalized 8-Week Roadmap: {target_role}")
        st.markdown(
            f"Tailored to your schedule: **{daily_h} hours/day** across **{days_w} days/week** "
            f"(Total: **{weekly_h} hours/week**). Style: **{learning_style}**."
        )

    with h_col2:
        if st.button("Regenerate Roadmap", type="secondary", width="stretch"):
            with st.spinner("Regenerating 8-week learning curriculum..."):
                _, new_roadmap, _ = generate_learning_roadmap(profile, skill_analysis)
                st.session_state["roadmap"] = new_roadmap
                st.success("Roadmap refreshed!")
                st.rerun()

    # Learning Progress Tracker
    completed_weeks = st.session_state.get("completed_weeks", [])
    progress_val = len(completed_weeks) / 8.0
    st.progress(progress_val, text=f"Curriculum Progress: {len(completed_weeks)} / 8 Weeks Completed ({int(progress_val * 100)}%)")

    # Display 8 Weeks in Expandable Cards
    for week in roadmap:
        w_num = week.get("week_number", 1)
        w_theme = week.get("theme", f"Week {w_num}")
        w_hours = week.get("estimated_hours", weekly_h)
        diff = week.get("difficulty", "Intermediate")
        is_done = w_num in completed_weeks

        status_tag = "Completed" if is_done else f"{diff} • {w_hours} Hours"

        with st.expander(f"**Week {w_num}: {w_theme}** — ({status_tag})", expanded=(w_num == 1 or w_num == 2)):
            # Mark complete checkbox
            col_check, col_diff = st.columns([1, 4])
            with col_check:
                marked = st.checkbox(f"Mark Week {w_num} Done", value=is_done, key=f"check_week_{w_num}")
                if marked and w_num not in completed_weeks:
                    completed_weeks.append(w_num)
                    st.session_state["completed_weeks"] = completed_weeks
                    st.rerun()
                elif not marked and w_num in completed_weeks:
                    completed_weeks.remove(w_num)
                    st.session_state["completed_weeks"] = completed_weeks
                    st.rerun()

            with col_diff:
                st.markdown(
                    f"**Difficulty Level:** `{diff}` | "
                    f"**Estimated Time Commitment:** `{w_hours} Hours`"
                )

            st.markdown("---")

            # Skills & Topics
            col_sk, col_top = st.columns(2)
            with col_sk:
                st.markdown("**Core Skills to Develop:**")
                skills = week.get("skills_to_develop", [])
                for s in skills:
                    st.markdown(f"- `{s}`")

            with col_top:
                st.markdown("**Learning Topics:**")
                topics = week.get("learning_topics", [])
                for t in topics:
                    st.markdown(f"- {t}")

            st.markdown("---")

            # Daily Schedule
            st.markdown("##### Daily Study Plan")
            daily_tasks = week.get("daily_tasks", [])
            for task in daily_tasks:
                st.markdown(f"- {task}")

            st.markdown("---")

            # Practical Exercises & Weekly Project
            col_ex, col_proj = st.columns(2)
            with col_ex:
                st.markdown("##### Practical Exercises")
                exercises = week.get("practical_exercises", [])
                for ex in exercises:
                    st.markdown(f"- {ex}")

            with col_proj:
                st.markdown("##### Weekly Milestone Assignment")
                st.info(week.get("weekly_project", "Milestone implementation project."))

            st.markdown("---")
            st.markdown(f"**Expected Learning Outcome:** *{week.get('expected_outcome', 'Competency acquired.')}*")
