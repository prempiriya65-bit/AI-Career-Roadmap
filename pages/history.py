"""
Analysis History Page View
View, inspect, load, and manage previously saved student assessments and career roadmaps.
"""

import streamlit as st
import pandas as pd
from modules.report_generator import load_history, delete_history_item


def render_history_page():
    """Render historical assessments table with load and delete actions."""
    st.markdown("## Analysis History")
    st.markdown("Review and reload past career roadmap assessments stored locally on your machine.")

    history_records = load_history()

    if not history_records:
        st.info("No saved assessment history found yet. Generate an assessment from the Home page to start building your record history!")
        if st.button("Go to Home Page", type="primary"):
            st.session_state["active_page"] = "Home"
            st.rerun()
        return

    st.markdown(f"**Total Records Saved:** `{len(history_records)}`")

    # Display history table overview
    overview_data = []
    for r in history_records:
        overview_data.append({
            "Assessment ID": r.get("id", "")[:8],
            "Date": r.get("formatted_date", ""),
            "Student Name": r.get("student_name", "Anonymous"),
            "Target Career": r.get("target_role", ""),
            "Readiness": f"{r.get('readiness_score', 0)}%"
        })

    df_hist = pd.DataFrame(overview_data)
    st.dataframe(df_hist, width="stretch", hide_index=True)

    st.markdown("---")
    st.markdown("### Inspect & Load Saved Assessment")

    # Selection dropdown to view or restore
    options = {f"{r.get('formatted_date', '')} — {r.get('student_name', '')} ({r.get('target_role', '')})": r for r in history_records}
    selected_label = st.selectbox("Select Assessment to Load:", list(options.keys()))

    if selected_label:
        selected_record = options[selected_label]
        payload = selected_record.get("payload", {})

        col_load, col_del, _ = st.columns([1.5, 1.5, 3])

        with col_load:
            if st.button("Load This Assessment", type="primary", width="stretch"):
                st.session_state["profile"] = payload.get("profile", {})
                st.session_state["skill_analysis"] = payload.get("skill_analysis", {})
                st.session_state["roadmap"] = payload.get("roadmap", [])
                st.session_state["projects"] = payload.get("projects", [])
                st.session_state["completed_weeks"] = []
                st.session_state["has_analysis"] = True
                st.session_state["active_page"] = "My Career Analysis"
                st.success("Loaded assessment! Redirecting to Dashboard...")
                st.rerun()

        with col_del:
            if st.button("Delete This Record", width="stretch"):
                item_id = selected_record.get("id")
                if delete_history_item(item_id):
                    st.success("Record deleted successfully!")
                    st.rerun()
                else:
                    st.error("Failed to delete record.")

        # Quick summary card of the selected item
        with st.expander("Preview Assessment Payload Details", expanded=False):
            st.json({
                "Student Name": selected_record.get("student_name"),
                "Target Role": selected_record.get("target_role"),
                "Readiness Score": selected_record.get("readiness_score"),
                "Skills Entered": len(payload.get("profile", {}).get("skills_with_levels", {})),
                "Missing Skills Count": len(payload.get("skill_analysis", {}).get("missing_skills", [])),
                "Roadmap Weeks": len(payload.get("roadmap", [])),
                "Projects Count": len(payload.get("projects", []))
            })
