"""
Report Generator Module
Handles exporting full assessment reports as PDF, TXT, and CSV,
as well as persisting and retrieving analysis records in local storage (data/history.json).
"""

import json
import os
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
import pandas as pd
from fpdf import FPDF

HISTORY_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "history.json")


def _safe_pdf_text(text: Any) -> str:
    """Normalize text to Latin-1 safe characters for standard FPDF core fonts."""
    if text is None:
        return ""
    s = str(text)
    replacements = {
        "\u2014": "-",
        "\u2013": "-",
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2022": "*",
        "\u2192": "->",
        "\u2197": "",
        "\u2026": "...",
    }
    for src, dst in replacements.items():
        s = s.replace(src, dst)
    return s.encode("latin-1", errors="replace").decode("latin-1")


class PDFReport(FPDF):
    """Custom FPDF class with branded header and footer."""

    def __init__(self, student_name: str, target_role: str):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.student_name = student_name
        self.target_role = target_role
        self.set_auto_page_break(auto=True, margin=15)

    def header(self):
        # Top banner styling
        self.set_fill_color(30, 58, 138)  # Deep Navy #1E3A8A
        self.rect(0, 0, 210, 18, "F")
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(255, 255, 255)
        self.set_xy(10, 4)
        self.cell(0, 10, "AI CAREER ROADMAP & SKILL GAP FINDER", 0, 0, "L")
        self.set_font("Helvetica", "", 9)
        self.set_xy(10, 4)
        self.cell(190, 10, "Academic & Professional Career Report", 0, 0, "R")
        self.ln(18)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(100, 116, 139)
        page_str = f"Page {self.page_no()}/{{nb}} | Confidential Student Assessment"
        self.cell(0, 10, page_str, 0, 0, "C")

    def chapter_title(self, title: str):
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(15, 23, 42)  # #0F172A
        self.set_fill_color(239, 246, 255)  # Light Blue #EFF6FF
        self.cell(0, 8, f"  {title}", 0, 1, "L", fill=True)
        self.ln(2)


def generate_pdf_report(
    profile: Dict[str, Any],
    skill_analysis: Dict[str, Any],
    roadmap: List[Dict[str, Any]],
    projects: List[Dict[str, Any]],
    resources: Optional[List[Dict[str, Any]]] = None
) -> bytes:
    """Generate a clean, professional multi-page PDF career report."""
    student_name = profile.get("student_name", "Student")
    target_role = profile.get("target_role", "AI Engineer")

    pdf = PDFReport(student_name=student_name, target_role=target_role)
    pdf.alias_nb_pages()
    pdf.add_page()

    # Title Card
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(37, 99, 235)  # #2563EB
    pdf.cell(0, 10, _safe_pdf_text(f"Career Assessment: {target_role}"), 0, 1, "L")

    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(71, 85, 105)
    gen_time = datetime.now().strftime("%B %d, %Y - %I:%M %p")
    pdf.cell(0, 6, _safe_pdf_text(f"Generated for: {student_name} | Date: {gen_time}"), 0, 1, "L")
    pdf.ln(4)

    # Student Summary Box
    pdf.set_fill_color(248, 250, 252)
    pdf.set_draw_color(226, 232, 240)
    pdf.rect(10, pdf.get_y(), 190, 24, "FD")
    pdf.set_xy(12, pdf.get_y() + 2)

    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(45, 5, "Education Level:", 0, 0)
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(50, 5, _safe_pdf_text(profile.get("education_level", "N/A"))[:28], 0, 0)

    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(45, 5, "University/College:", 0, 0)
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(50, 5, _safe_pdf_text(profile.get("university") or "Not Specified")[:28], 0, 1)

    pdf.set_xy(12, pdf.get_y() + 1)
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(45, 5, "Weekly Commitment:", 0, 0)
    pdf.set_font("Helvetica", "", 9)
    hours_str = f"{profile.get('study_hours_per_day', 2)} hrs/day x {profile.get('study_days_per_week', 5)} days/wk"
    pdf.cell(50, 5, _safe_pdf_text(hours_str), 0, 0)

    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(45, 5, "Readiness Score:", 0, 0)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(37, 99, 235)
    pdf.cell(50, 5, f"{skill_analysis.get('readiness_score', 0)}%", 0, 1)

    pdf.set_text_color(15, 23, 42)
    pdf.ln(8)

    # Section 1: Executive Summary & Calculation
    pdf.chapter_title("1. Executive Summary & Readiness Calculation")
    pdf.set_font("Helvetica", "", 9)
    summary_text = _safe_pdf_text(skill_analysis.get("overall_summary", "Evaluation completed successfully."))
    pdf.multi_cell(190, 5, summary_text)
    pdf.ln(2)

    score_expl = _safe_pdf_text(skill_analysis.get("score_explanation", ""))
    if score_expl:
        pdf.set_font("Helvetica", "I", 8)
        pdf.set_text_color(100, 116, 139)
        pdf.multi_cell(190, 4, f"Note: {score_expl}")
        pdf.set_text_color(15, 23, 42)
    pdf.ln(4)

    # Section 2: Skill Gap Analysis Table
    pdf.chapter_title("2. Role Competency & Skill Gap Analysis")
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_fill_color(226, 232, 240)

    # Table Header
    col_w = [55, 26, 26, 28, 20, 35]
    headers = ["Required Skill", "Your Level", "Target", "Status", "Priority", "Recommended Topics"]
    for w, h in zip(col_w, headers):
        pdf.cell(w, 7, h, 1, 0, "C", fill=True)
    pdf.ln(7)

    pdf.set_font("Helvetica", "", 7.5)
    skills_table = skill_analysis.get("skills_table", [])
    for row in skills_table:
        pdf.cell(col_w[0], 6, _safe_pdf_text(row.get("skill", ""))[:32], 1, 0, "L")
        pdf.cell(col_w[1], 6, _safe_pdf_text(row.get("student_level", "None")), 1, 0, "C")
        pdf.cell(col_w[2], 6, _safe_pdf_text(row.get("required_level", "")), 1, 0, "C")

        status = _safe_pdf_text(row.get("status", "Missing"))
        pdf.cell(col_w[3], 6, status, 1, 0, "C")
        pdf.cell(col_w[4], 6, _safe_pdf_text(row.get("priority", "Medium")), 1, 0, "C")
        raw_topics = _safe_pdf_text(row.get("recommended_topics", ""))
        topics = raw_topics[:25] + "..." if len(raw_topics) > 25 else raw_topics
        pdf.cell(col_w[5], 6, topics, 1, 1, "L")

    pdf.ln(6)

    # Section 3: 8-Week Personalized Roadmap
    pdf.add_page()
    pdf.chapter_title("3. Personalized 8-Week Learning Roadmap")

    for week in roadmap:
        w_num = week.get("week_number", 1)
        w_theme = _safe_pdf_text(week.get("theme", f"Week {w_num}"))
        w_hours = week.get("estimated_hours", 10)
        diff = _safe_pdf_text(week.get("difficulty", "Intermediate"))

        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(30, 58, 138)
        pdf.cell(0, 6, f"{w_theme}  [{diff} | {w_hours} hrs]", 0, 1, "L")
        pdf.set_text_color(15, 23, 42)

        pdf.set_font("Helvetica", "B", 8)
        pdf.cell(25, 5, "Skills to Learn:", 0, 0)
        pdf.set_font("Helvetica", "", 8)
        skills_str = _safe_pdf_text(", ".join(week.get("skills_to_develop", [])))
        pdf.multi_cell(165, 5, skills_str)

        pdf.set_font("Helvetica", "B", 8)
        pdf.cell(25, 5, "Weekly Project:", 0, 0)
        pdf.set_font("Helvetica", "", 8)
        pdf.multi_cell(165, 5, _safe_pdf_text(week.get("weekly_project", "Mini project")))

        pdf.set_font("Helvetica", "B", 8)
        pdf.cell(25, 5, "Outcome:", 0, 0)
        pdf.set_font("Helvetica", "I", 8)
        pdf.multi_cell(165, 4, _safe_pdf_text(week.get("expected_outcome", "Core mastery achieved.")))
        pdf.ln(2)

    pdf.ln(4)

    # Section 4: Recommended Portfolio Projects
    pdf.add_page()
    pdf.chapter_title("4. Recommended Portfolio Projects (3 Tiers)")

    for p in projects:
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(37, 99, 235)
        pdf.cell(0, 6, _safe_pdf_text(f"{p.get('title', 'Project')}  [{p.get('difficulty_level', 'Beginner')}]"), 0, 1, "L")
        pdf.set_text_color(15, 23, 42)

        pdf.set_font("Helvetica", "B", 8.5)
        pdf.cell(30, 5, "Problem Statement:", 0, 0)
        pdf.set_font("Helvetica", "", 8.5)
        pdf.multi_cell(160, 4.5, _safe_pdf_text(p.get("problem_statement", "")))

        pdf.set_font("Helvetica", "B", 8.5)
        pdf.cell(30, 5, "Technologies:", 0, 0)
        pdf.set_font("Helvetica", "", 8.5)
        pdf.multi_cell(160, 5, _safe_pdf_text(", ".join(p.get("technologies", []))))

        pdf.set_font("Helvetica", "B", 8.5)
        pdf.cell(30, 5, "Expected Output:", 0, 0)
        pdf.set_font("Helvetica", "", 8.5)
        pdf.multi_cell(160, 4.5, _safe_pdf_text(p.get("expected_output", "")))
        pdf.ln(4)

    # Section 5: Learning Resources (if provided)
    if resources:
        pdf.chapter_title("5. Recommended Verified Learning Resources")
        for res in resources[:6]:
            pdf.set_font("Helvetica", "B", 8.5)
            pdf.cell(50, 5, _safe_pdf_text(res.get("title", "Resource"))[:28], 0, 0)
            pdf.set_font("Helvetica", "", 8)
            pdf.set_text_color(37, 99, 235)
            pdf.cell(0, 5, _safe_pdf_text(res.get("url", "")), 0, 1)
            pdf.set_text_color(15, 23, 42)

    return bytes(pdf.output())


def generate_txt_report(
    profile: Dict[str, Any],
    skill_analysis: Dict[str, Any],
    roadmap: List[Dict[str, Any]],
    projects: List[Dict[str, Any]],
    resources: Optional[List[Dict[str, Any]]] = None
) -> str:
    """Generate a clean ASCII-formatted text report."""
    lines = []
    lines.append("=" * 75)
    lines.append("AI CAREER ROADMAP & SKILL GAP FINDER - COMPREHENSIVE REPORT")
    lines.append("=" * 75)
    lines.append(f"Generated Date  : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"Student Name    : {profile.get('student_name', 'Student')}")
    lines.append(f"Education Level : {profile.get('education_level', 'N/A')}")
    lines.append(f"College/Uni     : {profile.get('university') or 'Not Specified'}")
    lines.append(f"Target Career   : {profile.get('target_role', 'AI Engineer')}")
    lines.append(f"Study Schedule  : {profile.get('study_hours_per_day', 2)} hrs/day, {profile.get('study_days_per_week', 5)} days/week")
    lines.append(f"Readiness Score : {skill_analysis.get('readiness_score', 0)}%")
    lines.append("-" * 75)
    lines.append("EXECUTIVE SUMMARY:")
    lines.append(skill_analysis.get("overall_summary", "Evaluation complete."))
    lines.append("")
    lines.append("SCORE CALCULATION:")
    lines.append(skill_analysis.get("score_explanation", ""))
    lines.append("=" * 75)
    lines.append("SKILL GAP ANALYSIS TABLE:")
    lines.append(f"{'Skill':<35} | {'Current':<12} | {'Required':<12} | {'Status':<16} | {'Priority':<8}")
    lines.append("-" * 75)

    for row in skill_analysis.get("skills_table", []):
        s_name = row.get("skill", "")[:34]
        c_lvl = row.get("student_level", "None")[:11]
        r_lvl = row.get("required_level", "")[:11]
        stat = row.get("status", "")[:15]
        pri = row.get("priority", "")[:7]
        lines.append(f"{s_name:<35} | {c_lvl:<12} | {r_lvl:<12} | {stat:<16} | {pri:<8}")

    lines.append("=" * 75)
    lines.append("PERSONALIZED 8-WEEK LEARNING ROADMAP:")
    lines.append("-" * 75)

    for week in roadmap:
        lines.append(f"\n>> {week.get('theme', 'Week')} (Est. Hours: {week.get('estimated_hours', 10)})")
        lines.append(f"   Skills to Develop: {', '.join(week.get('skills_to_develop', []))}")
        lines.append(f"   Weekly Project   : {week.get('weekly_project', '')}")
        lines.append(f"   Expected Outcome : {week.get('expected_outcome', '')}")
        lines.append("   Daily Schedule:")
        for t in week.get("daily_tasks", []):
            lines.append(f"     * {t}")

    lines.append("\n" + "=" * 75)
    lines.append("PORTFOLIO PROJECT RECOMMENDATIONS (3 TIERS):")
    lines.append("-" * 75)

    for idx, p in enumerate(projects, start=1):
        lines.append(f"\n[Project {idx}] {p.get('title', '')} ({p.get('difficulty_level', '')})")
        lines.append(f"Problem Statement: {p.get('problem_statement', '')}")
        lines.append(f"Technologies     : {', '.join(p.get('technologies', []))}")
        lines.append(f"Expected Output  : {p.get('expected_output', '')}")
        lines.append("Implementation Steps:")
        for s in p.get("implementation_steps", []):
            lines.append(f"  - {s}")

    if resources:
        lines.append("\n" + "=" * 75)
        lines.append("RECOMMENDED LEARNING RESOURCES:")
        lines.append("-" * 75)
        for r in resources:
            lines.append(f"- {r.get('title', '')} [{r.get('type', 'Doc')}]: {r.get('url', '')}")

    lines.append("\n" + "=" * 75)
    lines.append("END OF REPORT - AI Career Roadmap & Skill Gap Finder")
    lines.append("=" * 75)

    return "\n".join(lines)


def generate_csv_report(skill_analysis: Dict[str, Any]) -> str:
    """Generate CSV string of the skill gap analysis table."""
    table = skill_analysis.get("skills_table", [])
    df = pd.DataFrame(table)
    if not df.empty:
        # Reorder and rename for professional display
        expected_cols = ["skill", "student_level", "required_level", "status", "skill_gap", "priority", "recommended_topics"]
        actual_cols = [c for c in expected_cols if c in df.columns]
        df = df[actual_cols]
        rename_map = {
            "skill": "Required Skill",
            "student_level": "Student Current Level",
            "required_level": "Required Level",
            "status": "Gap Status",
            "skill_gap": "Skill Gap Detail",
            "priority": "Priority",
            "recommended_topics": "Recommended Learning Topics"
        }
        df = df.rename(columns=rename_map)
    return df.to_csv(index=False)


def save_analysis_to_history(payload: Dict[str, Any]) -> bool:
    """Save analysis record to local JSON history file."""
    try:
        os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
        history = load_history()

        record = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),
            "formatted_date": datetime.now().strftime("%b %d, %Y - %I:%M %p"),
            "student_name": payload.get("profile", {}).get("student_name", "Anonymous"),
            "target_role": payload.get("profile", {}).get("target_role", "AI Engineer"),
            "readiness_score": payload.get("skill_analysis", {}).get("readiness_score", 0),
            "payload": payload
        }

        # Keep latest at the top
        history.insert(0, record)

        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)

        return True
    except Exception as e:
        return False


def load_history() -> List[Dict[str, Any]]:
    """Load analysis history list from disk."""
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except Exception:
        return []


def delete_history_item(item_id: str) -> bool:
    """Delete a record by ID from history.json."""
    try:
        history = load_history()
        updated = [h for h in history if h.get("id") != item_id]
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(updated, f, indent=2, ensure_ascii=False)
        return True
    except Exception:
        return False
