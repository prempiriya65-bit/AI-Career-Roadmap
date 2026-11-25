"""
Learning Resources Page View
Verified, high-quality documentation, interactive courses, free platforms,
and coding practice hubs organized by skill domains.
"""

import streamlit as st

VERIFIED_RESOURCE_CATALOG = {
    "python": [
        {"title": "Official Python 3 Documentation", "type": "Documentation", "url": "https://docs.python.org/3/", "desc": "Comprehensive standard library and language tutorial."},
        {"title": "Real Python Tutorials", "type": "Tutorials", "url": "https://realpython.com/", "desc": "Practical, step-by-step Python development articles."},
        {"title": "Exercism Python Track", "type": "Practice", "url": "https://exercism.org/tracks/python", "desc": "Hands-on coding exercises with free mentor feedback."}
    ],
    "machine learning": [
        {"title": "Scikit-Learn Official User Guide", "type": "Documentation", "url": "https://scikit-learn.org/stable/user_guide.html", "desc": "Industry-standard machine learning library reference."},
        {"title": "Kaggle Learn - Machine Learning", "type": "Free Platform", "url": "https://www.kaggle.com/learn", "desc": "Micro-courses with interactive hands-on Jupyter environments."},
        {"title": "Google Machine Learning Crash Course", "type": "Course", "url": "https://developers.google.com/machine-learning/crash-course", "desc": "Fast-paced, practical introduction to ML fundamentals."}
    ],
    "deep learning": [
        {"title": "PyTorch Official Tutorials", "type": "Documentation", "url": "https://pytorch.org/tutorials/", "desc": "From beginner tensors to custom autograd and production deployment."},
        {"title": "DeepLearning.AI Courses", "type": "Course", "url": "https://www.deeplearning.ai/", "desc": "Specializations by Andrew Ng covering deep learning and neural networks."},
        {"title": "Fast.ai - Practical Deep Learning for Coders", "type": "Free Platform", "url": "https://course.fast.ai/", "desc": "Top-down hands-on deep learning curriculum."}
    ],
    "transformers & llms": [
        {"title": "Hugging Face Transformers Documentation", "type": "Documentation", "url": "https://huggingface.co/docs/transformers/index", "desc": "State-of-the-art transformer architectures and pipelines."},
        {"title": "Google AI Studio & Gemini Documentation", "type": "Documentation", "url": "https://ai.google.dev/docs", "desc": "Official developer guides and API reference for Gemini models."},
        {"title": "Hugging Face NLP Course", "type": "Course", "url": "https://huggingface.co/learn/nlp-course", "desc": "Free in-depth training on modern NLP models and tokenizers."}
    ],
    "sql & databases": [
        {"title": "PostgreSQL Official Documentation", "type": "Documentation", "url": "https://www.postgresql.org/docs/", "desc": "Definitive guide to advanced SQL, window functions, and indexing."},
        {"title": "Mode Analytics SQL Tutorial", "type": "Tutorials", "url": "https://mode.com/sql-tutorial/", "desc": "Interactive SQL for data analysis and business intelligence."},
        {"title": "SQLZoo Interactive Exercises", "type": "Practice", "url": "https://sqlzoo.net/", "desc": "In-browser SQL practice with real-time feedback."}
    ],
    "docker & cloud": [
        {"title": "Docker Official Documentation", "type": "Documentation", "url": "https://docs.docker.com/get-started/", "desc": "Comprehensive guides to containerization and Docker Compose."},
        {"title": "Kubernetes Official Documentation", "type": "Documentation", "url": "https://kubernetes.io/docs/home/", "desc": "Core concepts, architecture, and production cluster operations."},
        {"title": "AWS Skill Builder", "type": "Free Platform", "url": "https://explore.skillbuilder.aws/", "desc": "Free digital training on AWS cloud fundamentals."}
    ],
    "git & software engineering": [
        {"title": "Pro Git Book (Free Online)", "type": "Documentation", "url": "https://git-scm.com/book/en/v2", "desc": "The complete reference guide to Git version control."},
        {"title": "GitHub Skills Interactive Labs", "type": "Practice", "url": "https://skills.github.com/", "desc": "Learn GitHub workflows by interacting directly with repositories."},
        {"title": "LeetCode Practice Hub", "type": "Practice", "url": "https://leetcode.com/", "desc": "Algorithmic and data structure problem solving."}
    ]
}


def render_resources_page():
    """Render categorized resources tailored to missing and improve skills."""
    if not st.session_state.get("has_analysis", False):
        st.info("No active career analysis found. Please generate an assessment on the Home page first.")
        if st.button("Go to Home Form", type="primary"):
            st.session_state["active_page"] = "Home"
            st.rerun()
        return

    profile = st.session_state.get("profile", {})
    skill_analysis = st.session_state.get("skill_analysis", {})
    target_role = profile.get("target_role", "AI Engineer")
    missing = skill_analysis.get("missing_skills", [])
    improve = skill_analysis.get("improve_skills", [])

    st.markdown(f"## Curated Learning Resources: {target_role}")
    st.markdown("Verified, authoritative references and learning hubs targeted at your identified skill gaps.")

    # Show missing skills cards
    focus_skills = missing + improve
    if not focus_skills:
        st.success("Your profile currently matches all required benchmark competencies! Explore advanced masterclasses below.")
        focus_skills = skill_analysis.get("skills_table", [])

    # Filter / Search
    search = st.text_input("Search resources by topic or technology", placeholder="e.g. PyTorch, SQL, Docker...")

    if search.strip():
        q = search.strip().lower()
        filtered_skills = []
        for s in focus_skills:
            matched_links = match_resources_for_skill(s.get("skill", ""))
            links_match = any(
                q in r.get("title", "").lower() or q in r.get("desc", "").lower()
                for r in matched_links
            )
            if (
                q in s.get("skill", "").lower()
                or q in s.get("recommended_topics", "").lower()
                or q in s.get("skill_gap", "").lower()
                or links_match
            ):
                filtered_skills.append(s)
    else:
        filtered_skills = focus_skills

    st.markdown("### Targeted Skill Gap Resources")
    if not filtered_skills:
        st.info("No learning resources match your search query. Try another keyword or clear the search box.")
    for s in filtered_skills[:8]:
        s_name = s.get("skill", "")
        pri = s.get("priority", "Medium")
        status = s.get("status", "Missing")
        badge_style = "badge-missing" if status == "Missing" else "badge-improve"

        with st.expander(f"**{s_name}** — ({status} | Priority: {pri})", expanded=True):
            st.markdown(f"**Recommended Topics to Master:** `{s.get('recommended_topics', '')}`")
            st.markdown(f"**Gap Diagnosis:** *{s.get('skill_gap', '')}*")

            # Match with verified catalog
            matched = match_resources_for_skill(s_name)
            st.markdown("##### Verified Learning Links:")
            r_cols = st.columns(len(matched)) if matched else [st.container()]
            for idx, r in enumerate(matched):
                with r_cols[idx % len(r_cols)]:
                    st.markdown(f"""
                    <div class="resource-box">
                        <span style="font-size: 0.7rem; font-weight: 700; color: #2563EB; text-transform: uppercase;">
                            {r['type']}
                        </span>
                        <div style="font-size: 0.95rem; font-weight: 700; margin: 0.25rem 0;">
                            <a href="{r['url']}" target="_blank">{r['title']} ↗</a>
                        </div>
                        <div style="font-size: 0.8rem; color: #64748B;">{r['desc']}</div>
                    </div>
                    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Universal Tech Career Platforms")
    u1, u2, u3, u4 = st.columns(4)
    with u1:
        st.markdown("""
        <div class="metric-card">
            <h4>Kaggle</h4>
            <p style="font-size: 0.8rem;">Hands-on ML datasets and notebook competitions.</p>
            <a href="https://www.kaggle.com" target="_blank" style="color: #2563EB; font-weight: 600;">Visit Kaggle ↗</a>
        </div>
        """, unsafe_allow_html=True)

    with u2:
        st.markdown("""
        <div class="metric-card">
            <h4>FreeCodeCamp</h4>
            <p style="font-size: 0.8rem;">Free full-stack, data analysis, and Python certs.</p>
            <a href="https://www.freecodecamp.org" target="_blank" style="color: #2563EB; font-weight: 600;">Visit FreeCodeCamp ↗</a>
        </div>
        """, unsafe_allow_html=True)

    with u3:
        st.markdown("""
        <div class="metric-card">
            <h4>Roadmap.sh</h4>
            <p style="font-size: 0.8rem;">Community-driven developer roadmaps.</p>
            <a href="https://roadmap.sh" target="_blank" style="color: #2563EB; font-weight: 600;">Visit Roadmap.sh ↗</a>
        </div>
        """, unsafe_allow_html=True)

    with u4:
        st.markdown("""
        <div class="metric-card">
            <h4>Exercism</h4>
            <p style="font-size: 0.8rem;">Code practice with mentor feedback in 60+ languages.</p>
            <a href="https://exercism.org" target="_blank" style="color: #2563EB; font-weight: 600;">Visit Exercism ↗</a>
        </div>
        """, unsafe_allow_html=True)


def match_resources_for_skill(skill_name: str):
    """Match skill name to verified resource catalog."""
    sn = skill_name.lower()
    if "python" in sn:
        return VERIFIED_RESOURCE_CATALOG["python"]
    elif "deep learning" in sn or "pytorch" in sn or "tensorflow" in sn:
        return VERIFIED_RESOURCE_CATALOG["deep learning"]
    elif "transformer" in sn or "llm" in sn or "rag" in sn:
        return VERIFIED_RESOURCE_CATALOG["transformers & llms"]
    elif "sql" in sn or "database" in sn:
        return VERIFIED_RESOURCE_CATALOG["sql & databases"]
    elif "docker" in sn or "cloud" in sn or "kubernetes" in sn:
        return VERIFIED_RESOURCE_CATALOG["docker & cloud"]
    elif "machine learning" in sn or "data" in sn:
        return VERIFIED_RESOURCE_CATALOG["machine learning"]
    else:
        return VERIFIED_RESOURCE_CATALOG["git & software engineering"]
