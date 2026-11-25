"""
AI Career Roadmap & Skill Gap Finder
Main Application Entrypoint

A comprehensive Streamlit web application providing AI-powered skill gap analysis,
personalized 8-week learning roadmaps, portfolio project blueprints, and career analytics.
"""

import os
import streamlit as st
from modules.gemini_service import is_api_configured, test_api_connection, get_api_key

# Page Configuration
st.set_page_config(
    page_title="AI Career Roadmap & Skill Gap Finder",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS Stylesheet
def load_css():
    css_path = os.path.join(os.path.dirname(__file__), "assets", "style.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# Import Page Views
from pages.home import render_home_page
from pages.dashboard import render_dashboard_page
from pages.skill_gap import render_skill_gap_page
from pages.roadmap import render_roadmap_page
from pages.projects import render_projects_page
from pages.resources import render_resources_page
from pages.history import render_history_page
from pages.about import render_about_page

# Navigation options
NAVIGATION_SECTIONS = [
    "Home",
    "My Career Analysis",
    "Skill Gap Finder",
    "8-Week Roadmap",
    "Portfolio Projects",
    "Learning Resources",
    "Analysis History",
    "About Project"
]

# Initialize Session State
if "active_page" not in st.session_state:
    st.session_state["active_page"] = "Home"

if "has_analysis" not in st.session_state:
    st.session_state["has_analysis"] = False


def render_sidebar():
    """Render professional SaaS sidebar with navigation, API status, and quick links."""
    with st.sidebar:
        # App Branding Header
        st.markdown("""
        <div style="padding: 1rem 0 1.25rem 0; border-bottom: 1px solid #1E293B; margin-bottom: 1rem;">
            <div style="font-size: 1.3rem; font-weight: 800; color: #FFFFFF; display: flex; align-items: center; gap: 8px;">
                <span>🎯</span> <span>Career Compass AI</span>
            </div>
            <div style="font-size: 0.75rem; color: #94A3B8; margin-top: 4px;">
                Skill Gap Finder & 8-Week Roadmap
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Active Student Badge (if analysis exists)
        if st.session_state.get("has_analysis", False):
            profile = st.session_state.get("profile", {})
            st.markdown(f"""
            <div style="background-color: #1E293B; border-radius: 8px; padding: 0.75rem; margin-bottom: 1.25rem; border: 1px solid #334155;">
                <div style="font-size: 0.7rem; color: #94A3B8; text-transform: uppercase; font-weight: 700;">Active Student</div>
                <div style="font-size: 0.95rem; font-weight: 700; color: #FFFFFF; margin-top: 2px;">{profile.get('student_name', 'Student')}</div>
                <div style="font-size: 0.8rem; color: #60A5FA;">Target: {profile.get('target_role', 'Tech Role')}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; color: #94A3B8; font-weight: 700; margin-bottom: 0.5rem;'>Navigation</div>", unsafe_allow_html=True)

        # Navigation Selector
        current_idx = 0
        if st.session_state["active_page"] in NAVIGATION_SECTIONS:
            current_idx = NAVIGATION_SECTIONS.index(st.session_state["active_page"])

        selected_page = st.radio(
            "Go to section:",
            NAVIGATION_SECTIONS,
            index=current_idx,
            label_visibility="collapsed"
        )

        if selected_page != st.session_state["active_page"]:
            st.session_state["active_page"] = selected_page
            st.rerun()

        st.markdown("---")

        # Gemini API Key Status / Configuration Panel
        st.markdown("<div style='font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; color: #94A3B8; font-weight: 700; margin-bottom: 0.5rem;'>Gemini AI Connection</div>", unsafe_allow_html=True)

        if is_api_configured():
            st.markdown("""
            <div style="background-color: #064E3B; border: 1px solid #059669; border-radius: 6px; padding: 0.5rem 0.75rem; font-size: 0.8rem; color: #A7F3D0; margin-bottom: 0.75rem;">
                ✓ Gemini API Configured
            </div>
            """, unsafe_allow_html=True)
            if st.button("Test Connection", width="stretch"):
                with st.spinner("Connecting to Google Gemini API..."):
                    connected, msg = test_api_connection()
                    if connected:
                        st.success(msg)
                    else:
                        st.error(msg)
        else:
            st.markdown("""
            <div style="background-color: #451A03; border: 1px solid #B45309; border-radius: 6px; padding: 0.5rem 0.75rem; font-size: 0.8rem; color: #FDE68A; margin-bottom: 0.75rem;">
                ⚠ API Key Not Set
            </div>
            """, unsafe_allow_html=True)

            with st.expander("Setup Gemini API Key", expanded=False):
                temp_key = st.text_input("Enter Gemini API Key:", type="password", help="Obtain key from https://aistudio.google.com/")
                if st.button("Apply Key"):
                    if temp_key.strip():
                        st.session_state["custom_gemini_api_key"] = temp_key.strip()
                        st.success("API key stored for this session!")
                        st.rerun()
                    else:
                        st.error("Please enter a valid key string.")
                st.caption("Permanent setup: Add `GEMINI_API_KEY = 'YOUR_KEY'` to `.streamlit/secrets.toml`")

        st.markdown("---")

        # Quick Actions
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("New Plan", width="stretch"):
                st.session_state["active_page"] = "Home"
                st.rerun()
        with col_btn2:
            if st.button("History", width="stretch"):
                st.session_state["active_page"] = "Analysis History"
                st.rerun()

        # Sidebar Footer
        st.markdown("""
        <div style="margin-top: 2rem; font-size: 0.7rem; color: #64748B; text-align: center;">
            AI Career Roadmap v1.0<br>
            Powered by Google Gemini 2.5 Flash
        </div>
        """, unsafe_allow_html=True)


def main():
    """Main application router."""
    render_sidebar()

    current_page = st.session_state.get("active_page", "Home")

    if current_page == "Home":
        render_home_page()
    elif current_page == "My Career Analysis":
        render_dashboard_page()
    elif current_page == "Skill Gap Finder":
        render_skill_gap_page()
    elif current_page == "8-Week Roadmap":
        render_roadmap_page()
    elif current_page == "Portfolio Projects":
        render_projects_page()
    elif current_page == "Learning Resources":
        render_resources_page()
    elif current_page == "Analysis History":
        render_history_page()
    elif current_page == "About Project":
        render_about_page()
    else:
        render_home_page()


if __name__ == "__main__":
    main()
