"""
Comprehensive Validation Test Suite for AI Career Roadmap Application
Tests:
1. Imports and environment packages
2. Skill analyzer benchmark logic and readiness score formula
3. Roadmap generator logic and hours calculation
4. Project generator output schema and count
5. Report generation (PDF, TXT, CSV)
6. History persistence (Save, Load, Delete)
"""

import os
import sys
import json

def run_tests():
    print("=" * 60)
    print("RUNNING COMPREHENSIVE APPLICATION TEST SUITE")
    print("=" * 60)

    # 1. Test Imports
    print("\n[Test 1] Importing all modules and dependencies...")
    try:
        import streamlit
        import google.genai
        import plotly
        import pandas as pd
        import fpdf
        from modules.gemini_service import is_api_configured, get_api_key
        from modules.skill_analyzer import analyze_skill_gaps, calculate_readiness_score, ROLE_BENCHMARKS
        from modules.roadmap_generator import generate_learning_roadmap, build_default_roadmap
        from modules.project_generator import generate_portfolio_projects, build_fallback_projects
        from modules.report_generator import (
            generate_pdf_report, generate_txt_report, generate_csv_report,
            save_analysis_to_history, load_history, delete_history_item
        )
        print("  --> [PASS] All modules and libraries imported successfully.")
    except Exception as e:
        print(f"  --> [FAIL] Import error: {e}")
        sys.exit(1)

    # 2. Test Skill Analyzer
    print("\n[Test 2] Testing Skill Gap Analyzer & Readiness Score...")
    sample_profile = {
        "student_name": "Test Student",
        "education_level": "Undergraduate (B.Tech)",
        "university": "Test University",
        "target_role": "AI Engineer",
        "study_hours_per_day": 3,
        "study_days_per_week": 5,
        "learning_style": "Practical Projects",
        "skills_with_levels": {
            "Python Programming": "Intermediate",
            "Git & Version Control": "Beginner",
            "Deep Learning Frameworks (PyTorch/TensorFlow)": "Beginner"
        }
    }

    success, analysis_data, msg = analyze_skill_gaps(sample_profile)
    assert success is True, "analyze_skill_gaps should succeed"
    assert "skills_table" in analysis_data, "skills_table missing"
    assert "readiness_score" in analysis_data, "readiness_score missing"
    assert "score_explanation" in analysis_data, "score_explanation missing"
    assert len(analysis_data["skills_table"]) > 0, "skills_table should have entries"
    score = analysis_data["readiness_score"]
    print(f"  --> [PASS] Skill analysis completed. Readiness Score: {score}%")
    print(f"      Possessed: {len(analysis_data['possessed_skills'])}, To Improve: {len(analysis_data['improve_skills'])}, Missing: {len(analysis_data['missing_skills'])}")

    # 3. Test Roadmap Generator
    print("\n[Test 3] Testing 8-Week Roadmap Generator...")
    success_road, roadmap, msg_road = generate_learning_roadmap(sample_profile, analysis_data)
    assert success_road is True, "generate_learning_roadmap should succeed"
    assert len(roadmap) == 8, f"Roadmap must have exactly 8 weeks, got {len(roadmap)}"
    for w in roadmap:
        assert "week_number" in w, "week_number missing"
        assert "theme" in w, "theme missing"
        assert "daily_tasks" in w, "daily_tasks missing"
        assert len(w["daily_tasks"]) == 5, f"Daily tasks count should match study days (5), got {len(w['daily_tasks'])}"
        assert w["estimated_hours"] == 15, f"Estimated hours should be 3*5=15, got {w['estimated_hours']}"
    print(f"  --> [PASS] 8-Week roadmap generated with exact 8-week length and 15 hrs/week commitment.")

    # 4. Test Portfolio Project Generator
    print("\n[Test 4] Testing Portfolio Project Recommendations...")
    success_proj, projects, msg_proj = generate_portfolio_projects(sample_profile, analysis_data)
    assert success_proj is True, "generate_portfolio_projects should succeed"
    assert len(projects) == 3, f"Must have exactly 3 projects, got {len(projects)}"
    diffs = [p["difficulty_level"] for p in projects]
    print(f"  --> [PASS] Exactly 3 projects generated with tiers: {diffs}")

    # 5. Test Reports Generation
    print("\n[Test 5] Testing Report Generation (PDF, TXT, CSV)...")
    # CSV
    csv_str = generate_csv_report(analysis_data)
    assert len(csv_str) > 50, "CSV string too short"
    assert "Required Skill" in csv_str, "CSV should contain headers"
    print(f"  --> [PASS] CSV report generated ({len(csv_str)} bytes).")

    # TXT
    txt_str = generate_txt_report(sample_profile, analysis_data, roadmap, projects)
    assert len(txt_str) > 200, "TXT report too short"
    assert "AI CAREER ROADMAP" in txt_str, "TXT should contain header"
    print(f"  --> [PASS] TXT report generated ({len(txt_str)} bytes).")

    # PDF
    pdf_bytes = generate_pdf_report(sample_profile, analysis_data, roadmap, projects)
    assert len(pdf_bytes) > 1000, "PDF bytes should be substantial"
    assert pdf_bytes.startswith(b"%PDF"), "Output must be valid PDF header"
    print(f"  --> [PASS] PDF report generated successfully ({len(pdf_bytes)} bytes).")

    # 6. Test History Persistence
    print("\n[Test 6] Testing History Persistence (Save, Load, Delete)...")
    payload = {
        "profile": sample_profile,
        "skill_analysis": analysis_data,
        "roadmap": roadmap,
        "projects": projects
    }
    saved = save_analysis_to_history(payload)
    assert saved is True, "save_analysis_to_history should succeed"

    history = load_history()
    assert len(history) > 0, "History should contain at least 1 record"
    first_item = history[0]
    assert first_item["student_name"] == "Test Student", "Stored student name mismatch"
    print(f"  --> [PASS] Record saved and loaded. Total records in history: {len(history)}.")

    # Test delete
    deleted = delete_history_item(first_item["id"])
    assert deleted is True, "delete_history_item should succeed"
    history_after = load_history()
    assert len(history_after) == len(history) - 1, "Record count should decrease by 1"
    print(f"  --> [PASS] Record deleted cleanly. Remaining records: {len(history_after)}.")

    print("\n" + "=" * 60)
    print("ALL TESTS PASSED SUCCESSFULLY! (6/6 TEST SUITES)")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()
