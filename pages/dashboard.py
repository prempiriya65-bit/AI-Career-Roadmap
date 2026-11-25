"""
Dashboard Page View - "My Career Analysis"
Executive overview displaying key metrics, skill readiness score with transparent formula explanation,
and four interactive Plotly visual charts.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from modules.report_generator import generate_pdf_report, generate_txt_report, generate_csv_report

LEVEL_NUM = {"none": 0, "beginner": 1, "intermediate": 2, "advanced": 3}


def render_dashboard_page():
    """Render executive metrics, Plotly visualizations, and export actions."""
    if not st.session_state.get("has_analysis", False):
        st.info("No active career analysis found. Please fill out the student intake form on the Home page first.")
        if st.button("Go to Home Form", type="primary"):
            st.session_state["active_page"] = "Home"
            st.rerun()
        return

    profile = st.session_state.get("profile", {})
    skill_analysis = st.session_state.get("skill_analysis", {})
    roadmap = st.session_state.get("roadmap", [])
    projects = st.session_state.get("projects", [])

    student_name = profile.get("student_name", "Student")
    target_role = profile.get("target_role", "AI Engineer")
    skills_table = skill_analysis.get("skills_table", [])
    possessed = skill_analysis.get("possessed_skills", [])
    improve = skill_analysis.get("improve_skills", [])
    missing = skill_analysis.get("missing_skills", [])
    readiness_score = skill_analysis.get("readiness_score", 0.0)

    # Header Card
    st.markdown(f"""
    <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px; padding: 1.25rem 1.5rem; margin-bottom: 1.5rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
            <div>
                <span style="font-size: 0.8rem; text-transform: uppercase; color: #64748B; font-weight: 700; letter-spacing: 0.05em;">Career Assessment Summary</span>
                <h2 style="margin: 0.2rem 0; color: #0F172A;">{student_name}</h2>
                <span style="color: #475569; font-size: 0.95rem;">Target Role: <strong style="color: #2563EB;">{target_role}</strong> | {profile.get('education_level', '')}</span>
            </div>
            <div style="text-align: right; margin-top: 0.5rem;">
                <span style="font-size: 0.8rem; color: #64748B; font-weight: 600;">Overall Syllabus Readiness</span>
                <div style="font-size: 2.2rem; font-weight: 800; color: #2563EB; line-height: 1;">{readiness_score}%</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 5 KPI Metric Cards
    m1, m2, m3, m4, m5 = st.columns(5)
    with m1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Entered Skills</div>
            <div class="metric-value">{len(profile.get('skills_with_levels', {}))}</div>
            <div class="metric-sub">Self-Reported</div>
        </div>
        """, unsafe_allow_html=True)

    with m2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Role Benchmark</div>
            <div class="metric-value">{len(skills_table)}</div>
            <div class="metric-sub">Required Skills</div>
        </div>
        """, unsafe_allow_html=True)

    with m3:
        st.markdown(f"""
        <div class="metric-card" style="border-top: 4px solid #10B981;">
            <div class="metric-title" style="color: #059669;">Possessed</div>
            <div class="metric-value" style="color: #059669;">{len(possessed)}</div>
            <div class="metric-sub">Meets Requirement</div>
        </div>
        """, unsafe_allow_html=True)

    with m4:
        st.markdown(f"""
        <div class="metric-card" style="border-top: 4px solid #F59E0B;">
            <div class="metric-title" style="color: #D97706;">To Improve</div>
            <div class="metric-value" style="color: #D97706;">{len(improve)}</div>
            <div class="metric-sub">Partial Proficiency</div>
        </div>
        """, unsafe_allow_html=True)

    with m5:
        st.markdown(f"""
        <div class="metric-card" style="border-top: 4px solid #EF4444;">
            <div class="metric-title" style="color: #DC2626;">Missing</div>
            <div class="metric-value" style="color: #DC2626;">{len(missing)}</div>
            <div class="metric-sub">Need To Learn</div>
        </div>
        """, unsafe_allow_html=True)

    # Readiness Score Explanation Callout (Requirement: Explain its calculation if included)
    st.markdown(f"""
    <div class="custom-alert custom-alert-info" style="margin-top: 1.25rem;">
        <strong>Readiness Score Calculation:</strong> {skill_analysis.get('score_explanation', '')}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Interactive Visualizations & Analytics")

    # Plotly Charts Row 1
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("##### 1. Current vs. Required Competency Levels")
        # Prepare data for grouped bar chart
        chart_data = []
        for s in skills_table:
            skill_name = s.get("skill", "")
            student_lvl = LEVEL_NUM.get(s.get("student_level", "None").lower(), 0)
            required_lvl = LEVEL_NUM.get(s.get("required_level", "Intermediate").lower(), 2)
            chart_data.append({"Skill": skill_name[:24], "Level": student_lvl, "Type": "Your Current Level"})
            chart_data.append({"Skill": skill_name[:24], "Level": required_lvl, "Type": "Required Benchmark"})

        df_levels = pd.DataFrame(chart_data)
        fig_bar = px.bar(
            df_levels,
            x="Skill",
            y="Level",
            color="Type",
            barmode="group",
            color_discrete_map={"Your Current Level": "#2563EB", "Required Benchmark": "#94A3B8"},
            category_orders={"Level": [0, 1, 2, 3]}
        )
        fig_bar.update_layout(
            yaxis=dict(
                tickvals=[0, 1, 2, 3],
                ticktext=["None (0)", "Beginner (1)", "Intermediate (2)", "Advanced (3)"],
                range=[0, 3.5]
            ),
            xaxis_tickangle=-45,
            margin=dict(l=20, r=20, t=20, b=80),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=360
        )
        fig_bar.update_xaxes(showgrid=False)
        fig_bar.update_yaxes(showgrid=True, gridcolor="#E2E8F0")
        st.plotly_chart(fig_bar, width="stretch")

    with c2:
        st.markdown("##### 2. Skill Gap Status Distribution")
        status_counts = pd.DataFrame([
            {"Status": "Possessed (Ready)", "Count": len(possessed), "Color": "#10B981"},
            {"Status": "Needs Improvement", "Count": len(improve), "Color": "#F59E0B"},
            {"Status": "Missing (To Learn)", "Count": len(missing), "Color": "#EF4444"}
        ])
        fig_donut = px.pie(
            status_counts,
            values="Count",
            names="Status",
            hole=0.55,
            color="Status",
            color_discrete_map={
                "Possessed (Ready)": "#10B981",
                "Needs Improvement": "#F59E0B",
                "Missing (To Learn)": "#EF4444"
            }
        )
        fig_donut.update_layout(
            margin=dict(l=20, r=20, t=20, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5),
            height=360
        )
        st.plotly_chart(fig_donut, width="stretch")

    # Plotly Charts Row 2
    c3, c4 = st.columns(2)

    with c3:
        st.markdown("##### 3. Missing & Improvement Priority Breakdown")
        pri_counts = {"High": 0, "Medium": 0, "Low": 0}
        for s in (missing + improve):
            p = s.get("priority", "Medium").capitalize()
            if p in pri_counts:
                pri_counts[p] += 1
            else:
                pri_counts["Medium"] += 1

        df_pri = pd.DataFrame([
            {"Priority": "High Priority", "Skills": pri_counts["High"], "Color": "#EF4444"},
            {"Priority": "Medium Priority", "Skills": pri_counts["Medium"], "Color": "#F59E0B"},
            {"Priority": "Low Priority", "Skills": pri_counts["Low"], "Color": "#3B82F6"}
        ])

        fig_pri = px.bar(
            df_pri,
            x="Priority",
            y="Skills",
            color="Priority",
            color_discrete_map={
                "High Priority": "#EF4444",
                "Medium Priority": "#F59E0B",
                "Low Priority": "#3B82F6"
            },
            text="Skills"
        )
        fig_pri.update_layout(
            margin=dict(l=20, r=20, t=20, b=40),
            showlegend=False,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=320
        )
        fig_pri.update_yaxes(showgrid=True, gridcolor="#E2E8F0")
        st.plotly_chart(fig_pri, width="stretch")

    with c4:
        st.markdown("##### 4. 8-Week Cumulative Study Hours Plan")
        if roadmap:
            weeks = [f"W{w.get('week_number', i+1)}" for i, w in enumerate(roadmap)]
            hrs = [w.get("estimated_hours", 10) for w in roadmap]
            cum_hrs = []
            cur = 0
            for h in hrs:
                cur += h
                cum_hrs.append(cur)

            fig_roadmap = go.Figure()
            fig_roadmap.add_trace(go.Bar(
                x=weeks,
                y=hrs,
                name="Weekly Hours",
                marker_color="#93C5FD"
            ))
            fig_roadmap.add_trace(go.Scatter(
                x=weeks,
                y=cum_hrs,
                name="Cumulative Hours",
                mode="lines+markers",
                line=dict(color="#1E3A8A", width=3),
                marker=dict(size=8, color="#2563EB")
            ))
            fig_roadmap.update_layout(
                margin=dict(l=20, r=20, t=20, b=40),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=320
            )
            fig_roadmap.update_yaxes(showgrid=True, gridcolor="#E2E8F0")
            st.plotly_chart(fig_roadmap, width="stretch")

    st.markdown("---")
    st.markdown("### Export & Action Center")

    d1, d2, d3, d4, d5 = st.columns([1.5, 1.5, 1.5, 1.5, 1.5])

    # 1. Download PDF
    with d1:
        pdf_bytes = generate_pdf_report(profile, skill_analysis, roadmap, projects)
        st.download_button(
            label="Download PDF Report",
            data=pdf_bytes,
            file_name=f"{student_name.replace(' ', '_')}_{target_role.replace(' ', '_')}_Report.pdf",
            mime="application/pdf",
            width="stretch"
        )

    # 2. Download TXT
    with d2:
        txt_content = generate_txt_report(profile, skill_analysis, roadmap, projects)
        st.download_button(
            label="Download TXT Report",
            data=txt_content,
            file_name=f"{student_name.replace(' ', '_')}_Report.txt",
            mime="text/plain",
            width="stretch"
        )

    # 3. Download CSV
    with d3:
        csv_data = generate_csv_report(skill_analysis)
        st.download_button(
            label="Download Gap CSV",
            data=csv_data,
            file_name=f"{student_name.replace(' ', '_')}_Skill_Gap.csv",
            mime="text/csv",
            width="stretch"
        )

    # 4. Jump to Roadmap
    with d4:
        if st.button("Open 8-Week Roadmap", width="stretch"):
            st.session_state["active_page"] = "8-Week Roadmap"
            st.rerun()

    # 5. Jump to Projects
    with d5:
        if st.button("View Portfolio Projects", width="stretch"):
            st.session_state["active_page"] = "Portfolio Projects"
            st.rerun()
