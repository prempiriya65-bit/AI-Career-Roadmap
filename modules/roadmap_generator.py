"""
Roadmap Generator Module
Generates a structured, personalized 8-Week Learning Roadmap tailored to the student's
skill gaps, available study hours, weekly days, and learning style using Gemini AI.
"""

import json
from typing import Dict, Any, List, Tuple, Optional
from modules.gemini_service import generate_structured_json, is_api_configured


def build_default_roadmap(
    target_role: str,
    missing_skills: List[str],
    improve_skills: List[str],
    daily_hours: int,
    weekly_days: int,
    learning_style: str
) -> List[Dict[str, Any]]:
    """
    Generate an 8-week curriculum adhering strictly to student time budget and role requirements.
    """
    weekly_hours = daily_hours * weekly_days
    skills_to_cover = (missing_skills + improve_skills) if (missing_skills or improve_skills) else [
        "Core Technical Fundamentals", "Advanced Data Structures & Algorithms", "Framework Architecture",
        "API Integration & Services", "Database Optimization", "Production Deployment", "Testing & MLOps", "Capstone Polish"
    ]

    roadmap = []
    milestone_themes = [
        ("Week 1: Core Fundamentals & Prerequisite Foundations", "Foundations", "Beginner"),
        ("Week 2: Advanced Syntax, Modular Design & Core Tooling", "Core Syntax", "Beginner"),
        ("Week 3: Essential Frameworks & Data Manipulation", "Frameworks", "Intermediate"),
        ("Week 4: Applied Problem Solving & Production Architecture", "Architecture", "Intermediate"),
        ("Week 5: System Integration, Performance & Security", "Integration", "Intermediate"),
        ("Week 6: Advanced Specialized Techniques & Testing", "Advanced Topics", "Advanced"),
        ("Week 7: End-to-End Capstone Project Development", "Capstone Part 1", "Advanced"),
        ("Week 8: Optimization, Deployment, Portfolio & Interview Prep", "Capstone Part 2 & Polish", "Advanced")
    ]

    for week_idx, (theme, focus, diff) in enumerate(milestone_themes, start=1):
        # Pick primary skills for this week
        primary_skill = skills_to_cover[(week_idx - 1) % len(skills_to_cover)]
        secondary_skill = skills_to_cover[week_idx % len(skills_to_cover)]

        # Generate realistic daily tasks based on study days
        daily_tasks = []
        for day in range(1, weekly_days + 1):
            if day == 1:
                daily_tasks.append(f"Day 1: Comprehensive conceptual review of {primary_skill} theory via {learning_style.lower()} resources.")
            elif day == 2:
                daily_tasks.append(f"Day 2: Hands-on code walkthrough and interactive notebook exercises for {primary_skill}.")
            elif day == weekly_days:
                daily_tasks.append(f"Day {day}: Complete and document weekly mini-project, push to GitHub repository.")
            else:
                daily_tasks.append(f"Day {day}: Implement practical coding tasks and edge-case testing for {secondary_skill}.")

        practical_exercises = [
            f"Exercise 1: Code an end-to-end module implementing core {primary_skill} operations.",
            f"Exercise 2: Debug and refactor an unoptimized sample pipeline focusing on performance.",
            f"Exercise 3: Write comprehensive unit test suites covering edge cases."
        ]

        weekly_project = (
            f"Milestone Mini-Project {week_idx}: Build a functional '{primary_skill.split()[0]} Showcase Utility' "
            f"with clean code architecture, configuration files, and GitHub documentation."
        )

        expected_outcome = (
            f"Demonstrated operational competency in {primary_skill} and {secondary_skill}. "
            f"Complete code artifact committed to your portfolio repository."
        )

        roadmap.append({
            "week_number": week_idx,
            "theme": theme,
            "skills_to_develop": [primary_skill, secondary_skill],
            "learning_topics": [
                f"{primary_skill} Core Mechanics",
                f"{secondary_skill} Architecture & Best Practices",
                "Error Handling & Unit Testing",
                "Clean Code Documentation"
            ],
            "daily_tasks": daily_tasks,
            "practical_exercises": practical_exercises,
            "weekly_project": weekly_project,
            "expected_outcome": expected_outcome,
            "estimated_hours": weekly_hours,
            "difficulty": diff
        })

    return roadmap


def generate_learning_roadmap(
    student_profile: Dict[str, Any],
    skill_analysis: Dict[str, Any]
) -> Tuple[bool, List[Dict[str, Any]], Optional[str]]:
    """
    Generate an 8-week personalized learning roadmap using Gemini API or default curriculum.
    """
    target_role = student_profile.get("target_role", "AI Engineer")
    daily_hours = student_profile.get("study_hours_per_day", 2)
    weekly_days = student_profile.get("study_days_per_week", 5)
    learning_style = student_profile.get("learning_style", "Mixed")
    weekly_hours = daily_hours * weekly_days

    missing = [s["skill"] for s in skill_analysis.get("missing_skills", [])]
    improve = [s["skill"] for s in skill_analysis.get("improve_skills", [])]
    possessed = [s["skill"] for s in skill_analysis.get("possessed_skills", [])]

    if is_api_configured():
        prompt = f"""
You are an expert technical curriculum designer and senior software engineering mentor.
Create an exact, personalized 8-Week Learning Roadmap for a student preparing for the role of '{target_role}'.

Student Details:
- Target Role: {target_role}
- Available Study Hours: {daily_hours} hours per day
- Available Study Days: {weekly_days} days per week (Total: {weekly_hours} hours/week)
- Preferred Learning Style: {learning_style}
- Missing Skills (Highest Priority to Learn): {json.dumps(missing)}
- Skills Needing Improvement: {json.dumps(improve)}
- Already Possessed Skills: {json.dumps(possessed)}

Requirements:
1. Exactly 8 weeks of progressively challenging learning (Weeks 1-2: Foundations of missing topics, Weeks 3-5: Core specialization, Weeks 6-8: Advanced production engineering, Capstone, and Deployment).
2. For EACH week, provide:
   - week_number (integer 1 to 8)
   - theme (concise title summarizing the week's objective)
   - skills_to_develop (list of 2-3 target skills)
   - learning_topics (list of 3-4 specific topics)
   - daily_tasks (list of EXACTLY {weekly_days} strings, one for each available day: 'Day 1: ...', 'Day 2: ...')
   - practical_exercises (list of 2-3 hands-on programming tasks)
   - weekly_project (one tangible mini-project or milestone assignment)
   - expected_outcome (concrete, verifiable learning outcome)
   - estimated_hours (must equal {weekly_hours})
   - difficulty ("Beginner", "Intermediate", or "Advanced")
3. Respect the student's study time budget strictly ({weekly_hours} hours per week).
4. Emphasize their preferred learning style: {learning_style}.

Return strictly a JSON object with a single key "roadmap" containing the array of 8 week objects:
{{
    "roadmap": [
        {{
            "week_number": 1,
            "theme": "...",
            "skills_to_develop": ["..."],
            "learning_topics": ["..."],
            "daily_tasks": ["Day 1: ...", ...],
            "practical_exercises": ["..."],
            "weekly_project": "...",
            "expected_outcome": "...",
            "estimated_hours": {weekly_hours},
            "difficulty": "Beginner"
        }}
    ]
}}
"""
        success, response_data, error_msg = generate_structured_json(
            prompt=prompt,
            system_instruction="You are an expert tech educator. Output only valid JSON adhering to the specified schema."
        )

        if success and response_data and "roadmap" in response_data:
            roadmap = response_data["roadmap"]
            if isinstance(roadmap, list) and len(roadmap) == 8:
                return True, roadmap, None

    # Fallback to high-quality benchmark curriculum
    default_roadmap = build_default_roadmap(
        target_role=target_role,
        missing_skills=missing,
        improve_skills=improve,
        daily_hours=daily_hours,
        weekly_days=weekly_days,
        learning_style=learning_style
    )

    if not is_api_configured():
        return True, default_roadmap, "API key not configured. Generated 8-week curriculum via role milestone framework."
    return True, default_roadmap, "Generated curriculum using structured role template."
