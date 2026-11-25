"""
Skill Analyzer Module
Performs skill gap analysis by contrasting student skills and levels against industry benchmarks
and role requirements using Gemini AI with structured schema validation.
"""

import json
from typing import Dict, Any, List, Tuple
from modules.gemini_service import generate_structured_json, is_api_configured

# Benchmark definitions for standard industry roles
ROLE_BENCHMARKS = {
    "AI Engineer": [
        {"skill": "Python Programming", "required_level": "Advanced", "priority": "High", "topics": "OOP, Type hints, AsyncIO, Memory optimization, Python C-extensions"},
        {"skill": "Deep Learning Frameworks (PyTorch/TensorFlow)", "required_level": "Advanced", "priority": "High", "topics": "Tensors, Autograd, Custom layers, Distributed training, Model quantization"},
        {"skill": "Large Language Models & Transformers", "required_level": "Intermediate", "priority": "High", "topics": "Attention mechanism, Hugging Face, Fine-tuning (LoRA/QLoRA), Prompt engineering"},
        {"skill": "Vector Databases & RAG Architecture", "required_level": "Intermediate", "priority": "High", "topics": "FAISS, ChromaDB, Chunking strategies, Embedding models, Hybrid search"},
        {"skill": "AI Model Deployment & APIs (FastAPI)", "required_level": "Intermediate", "priority": "High", "topics": "FastAPI, Docker containerization, REST/gRPC endpoints, ONNX runtime"},
        {"skill": "Mathematics for AI (Linear Algebra, Calculus, Probability)", "required_level": "Intermediate", "priority": "Medium", "topics": "Matrix decompositions, Gradient descent, Bayes theorem, Distribution functions"},
        {"skill": "MLOps & Experiment Tracking", "required_level": "Beginner", "priority": "Medium", "topics": "MLflow, Weights & Biases, CI/CD for ML, DVC data versioning"},
        {"skill": "Cloud AI Services (GCP/AWS/Azure)", "required_level": "Beginner", "priority": "Low", "topics": "Cloud run, Vertex AI, S3/GCS storage, IAM authentication"}
    ],
    "Machine Learning Engineer": [
        {"skill": "Python & Data Science Stack (NumPy, Pandas)", "required_level": "Advanced", "priority": "High", "topics": "Vectorized computations, Data cleaning, Feature engineering, Memory efficient DataFrames"},
        {"skill": "Classical Machine Learning (Scikit-Learn)", "required_level": "Advanced", "priority": "High", "topics": "Ensembles, XGBoost, LightGBM, Cross-validation, Hyperparameter tuning"},
        {"skill": "Deep Learning (PyTorch)", "required_level": "Intermediate", "priority": "High", "topics": "CNNs, RNNs/LSTMs, Transformers, Transfer learning, Tensorboard"},
        {"skill": "Model Serving & Pipeline Architecture", "required_level": "Intermediate", "priority": "High", "topics": "BentoML, FastAPI, Docker, Batch vs Real-time inference"},
        {"skill": "Feature Stores & Data Pipelines", "required_level": "Intermediate", "priority": "Medium", "topics": "SQL, Apache Spark basics, Data validation, Feast feature store"},
        {"skill": "Statistics & Applied Probability", "required_level": "Intermediate", "priority": "Medium", "topics": "Hypothesis testing, A/B testing, Confidence intervals, Regression analysis"},
        {"skill": "MLOps & CI/CD", "required_level": "Intermediate", "priority": "Medium", "topics": "GitHub Actions, Model registry, Automated testing for data pipelines"},
        {"skill": "Cloud Infrastructure", "required_level": "Beginner", "priority": "Low", "topics": "AWS SageMaker or GCP Vertex AI, EC2/Compute Engine, S3 buckets"}
    ],
    "Data Scientist": [
        {"skill": "Python & R for Data Science", "required_level": "Advanced", "priority": "High", "topics": "Pandas, NumPy, Scipy, Functional programming, Jupyter workflows"},
        {"skill": "Statistical Modeling & Hypothesis Testing", "required_level": "Advanced", "priority": "High", "topics": "P-values, ANOVA, Regression analysis, Non-parametric tests, Experimental design"},
        {"skill": "Data Wrangling & Exploratory Analysis", "required_level": "Advanced", "priority": "High", "topics": "Missing value imputation, Outlier detection, Correlation analysis, Feature transformation"},
        {"skill": "SQL & Relational Databases", "required_level": "Advanced", "priority": "High", "topics": "Window functions, Complex joins, Subqueries, CTEs, Query performance optimization"},
        {"skill": "Machine Learning Algorithms", "required_level": "Intermediate", "priority": "High", "topics": "Supervised/Unsupervised learning, Random Forests, Gradient Boosting, Clustering"},
        {"skill": "Data Visualization & Storytelling", "required_level": "Intermediate", "priority": "Medium", "topics": "Plotly, Seaborn, Tableau/PowerBI, Stakeholder communication"},
        {"skill": "Big Data Fundamentals", "required_level": "Beginner", "priority": "Medium", "topics": "PySpark, Distributed computing basics, Hive/Athena"},
        {"skill": "Business Acumen & Metric Design", "required_level": "Intermediate", "priority": "Low", "topics": "KPI definition, Conversion funnels, Retention cohorts, LTV modeling"}
    ],
    "Data Analyst": [
        {"skill": "SQL & Data Extraction", "required_level": "Advanced", "priority": "High", "topics": "Aggregations, Window functions, Joins, Group By, Filtering, CTEs"},
        {"skill": "Business Intelligence (Power BI / Tableau)", "required_level": "Advanced", "priority": "High", "topics": "Interactive dashboards, DAX / calculated fields, Data modeling, Drill-down reports"},
        {"skill": "Excel & Advanced Spreadsheets", "required_level": "Advanced", "priority": "High", "topics": "XLOOKUP, Pivot tables, Power Query, What-if analysis, Conditional formatting"},
        {"skill": "Python for Data Analysis", "required_level": "Intermediate", "priority": "High", "topics": "Pandas data wrangling, Matplotlib/Seaborn visualization, Basic automation"},
        {"skill": "Descriptive Statistics", "required_level": "Intermediate", "priority": "Medium", "topics": "Mean, Median, Standard deviation, Percentiles, Correlation, Distributions"},
        {"skill": "Data Cleaning & Quality Assurance", "required_level": "Intermediate", "priority": "Medium", "topics": "Deduplication, Normalization, Schema validation, Anomaly detection"},
        {"skill": "Executive Presentation & Storytelling", "required_level": "Intermediate", "priority": "Medium", "topics": "Insight summarization, Dashboard design principles, Slide decks"},
        {"skill": "Basic Git & Version Control", "required_level": "Beginner", "priority": "Low", "topics": "Git clone, Commit, Push, Branching, GitHub collaboration"}
    ],
    "Python Developer": [
        {"skill": "Advanced Python & Software Architecture", "required_level": "Advanced", "priority": "High", "topics": "OOP, Metaclasses, Context managers, Generators, Design patterns, Concurrency"},
        {"skill": "Backend Web Frameworks (Django / FastAPI)", "required_level": "Advanced", "priority": "High", "topics": "Routing, ORM, Middleware, Authentication, RESTful APIs, Dependency injection"},
        {"skill": "Relational & NoSQL Databases", "required_level": "Intermediate", "priority": "High", "topics": "PostgreSQL, SQLAlchemy, Redis caching, Migrations, Indexing"},
        {"skill": "Unit Testing & Code Quality", "required_level": "Intermediate", "priority": "High", "topics": "Pytest, Mocking, Test-Driven Development (TDD), Flake8, Black, MyPy"},
        {"skill": "Git & CI/CD Pipelines", "required_level": "Intermediate", "priority": "Medium", "topics": "Branching strategies, GitHub Actions, Pull request reviews, Semantic versioning"},
        {"skill": "Docker & Containerization", "required_level": "Intermediate", "priority": "Medium", "topics": "Dockerfile, Docker Compose, Multi-stage builds, Container security"},
        {"skill": "Asynchronous Programming (AsyncIO, Celery)", "required_level": "Intermediate", "priority": "Medium", "topics": "Event loops, Async tasks, Background workers, Message queues (RabbitMQ/Redis)"},
        {"skill": "Cloud & Linux Server Deployment", "required_level": "Beginner", "priority": "Low", "topics": "Nginx reverse proxy, Systemd services, Linux shell, AWS EC2 / Render"}
    ],
    "Full Stack Developer": [
        {"skill": "JavaScript & TypeScript", "required_level": "Advanced", "priority": "High", "topics": "ES6+, Async/Await, Strict type safety, Interfaces, Generics, DOM manipulation"},
        {"skill": "Frontend Frameworks (React / Next.js)", "required_level": "Advanced", "priority": "High", "topics": "Hooks, State management (Redux/Zustand), SSR/SSG, Component lifecycle, Tailwind CSS"},
        {"skill": "Backend Development (Node.js/Express or Python/FastAPI)", "required_level": "Advanced", "priority": "High", "topics": "REST APIs, GraphQL, Authentication (JWT/OAuth), Middleware, WebSockets"},
        {"skill": "Databases & ORM", "required_level": "Intermediate", "priority": "High", "topics": "PostgreSQL, MongoDB, Prisma/Drizzle/SQLAlchemy, Schema migrations"},
        {"skill": "Git & Version Control", "required_level": "Intermediate", "priority": "Medium", "topics": "Git branching, Merge conflicts, PR workflows, Git rebase"},
        {"skill": "Docker & Container Basics", "required_level": "Intermediate", "priority": "Medium", "topics": "Local containerization, Environment variables, Docker Compose"},
        {"skill": "Web Security & Authentication", "required_level": "Intermediate", "priority": "Medium", "topics": "CORS, XSS, CSRF prevention, Rate limiting, HTTPS, Secret management"},
        {"skill": "Cloud Hosting & Deployment (Vercel, AWS)", "required_level": "Beginner", "priority": "Low", "topics": "Serverless functions, S3 bucket static hosting, CI/CD auto-deploys"}
    ],
    "Web Developer": [
        {"skill": "HTML5, CSS3 & Responsive Design", "required_level": "Advanced", "priority": "High", "topics": "Semantic HTML, Flexbox, CSS Grid, Media queries, Accessibility (WCAG)"},
        {"skill": "JavaScript (Modern ES6+)", "required_level": "Advanced", "priority": "High", "topics": "Closures, Promises, Fetch API, Event bubbling, LocalStorage, Modules"},
        {"skill": "Frontend Frameworks (React or Vue)", "required_level": "Intermediate", "priority": "High", "topics": "Component architecture, State & props, Virtual DOM, React Router"},
        {"skill": "CSS Frameworks (Tailwind CSS / Bootstrap)", "required_level": "Intermediate", "priority": "Medium", "topics": "Utility-first design, Custom theming, Responsive UI layouts"},
        {"skill": "Web Performance & SEO", "required_level": "Intermediate", "priority": "Medium", "topics": "Lighthouse optimization, Asset compression, Lazy loading, Meta tags"},
        {"skill": "Version Control (Git & GitHub)", "required_level": "Intermediate", "priority": "Medium", "topics": "Repository management, Pull requests, GitHub Pages"},
        {"skill": "API Integration (REST / JSON)", "required_level": "Intermediate", "priority": "Medium", "topics": "Consuming 3rd party APIs, Handling asynchronous errors, Loading states"},
        {"skill": "Basic Backend / CMS (Node.js or Headless CMS)", "required_level": "Beginner", "priority": "Low", "topics": "Simple endpoints, Strapi / Sanity CMS integration, Form submissions"}
    ],
    "Cloud Engineer": [
        {"skill": "Cloud Provider Core (AWS / GCP / Azure)", "required_level": "Advanced", "priority": "High", "topics": "IAM roles, VPC networking, EC2/Compute, S3/Cloud Storage, Load balancers"},
        {"skill": "Infrastructure as Code (Terraform)", "required_level": "Intermediate", "priority": "High", "topics": "HCL syntax, State management, Modules, Provider configurations, Plan & Apply"},
        {"skill": "Linux Systems Administration & Bash", "required_level": "Advanced", "priority": "High", "topics": "Bash scripting, Permissions, Cron jobs, SSH keys, System monitoring, Network tools"},
        {"skill": "Containerization & Kubernetes (Docker & K8s)", "required_level": "Intermediate", "priority": "High", "topics": "Pod creation, Deployments, Services, ConfigMaps, Ingress, Helm charts"},
        {"skill": "CI/CD & DevOps Automation", "required_level": "Intermediate", "priority": "Medium", "topics": "GitHub Actions, GitLab CI, Pipeline security, Automated testing and deployment"},
        {"skill": "Cloud Security & Compliance", "required_level": "Intermediate", "priority": "Medium", "topics": "Least privilege principle, Encryption at rest & transit, Security groups, KMS"},
        {"skill": "Monitoring, Logging & Observability", "required_level": "Intermediate", "priority": "Medium", "topics": "Prometheus, Grafana, CloudWatch, Datadog, Distributed tracing"},
        {"skill": "Python for Cloud Automation", "required_level": "Intermediate", "priority": "Low", "topics": "Boto3 SDK, Lambda serverless triggers, Cloud script automation"}
    ],
    "Cybersecurity Engineer": [
        {"skill": "Network Security & Protocols", "required_level": "Advanced", "priority": "High", "topics": "TCP/IP, DNS, OSI model, Firewalls, VPNs, Wireshark packet analysis, Subnetting"},
        {"skill": "Vulnerability Assessment & Penetration Testing", "required_level": "Intermediate", "priority": "High", "topics": "OWASP Top 10, Nmap, Burp Suite, Metasploit, Common Vulnerabilities and Exposures (CVE)"},
        {"skill": "Operating System Security (Linux & Windows)", "required_level": "Advanced", "priority": "High", "topics": "Privilege escalation, Hardening, Active Directory, PAM, Log analysis"},
        {"skill": "Security Information & Event Management (SIEM)", "required_level": "Intermediate", "priority": "High", "topics": "Splunk, ELK stack, Incident response triage, Log correlation, Alerting rules"},
        {"skill": "Cryptography & PKI", "required_level": "Intermediate", "priority": "Medium", "topics": "Symmetric vs Asymmetric, TLS/SSL certificates, Hashing algorithms, Digital signatures"},
        {"skill": "Python / Bash Scripting for Security", "required_level": "Intermediate", "priority": "Medium", "topics": "Network scanners, Automated brute-force detection, Log parsing scripts"},
        {"skill": "Identity & Access Management (IAM)", "required_level": "Intermediate", "priority": "Medium", "topics": "MFA, OAuth2, SAML, Zero Trust architecture, Role-based access control"},
        {"skill": "Cloud Security Architecture", "required_level": "Beginner", "priority": "Low", "topics": "Cloud security posture, GuardDuty, AWS Config, CloudTrail audits"}
    ]
}


LEVEL_SCORES = {
    "none": 0,
    "beginner": 1,
    "intermediate": 2,
    "advanced": 3
}

PRIORITY_WEIGHTS = {
    "high": 3,
    "medium": 2,
    "low": 1
}


def normalize_level(level: str) -> str:
    """Normalize skill proficiency level strings."""
    lvl = (level or "").strip().capitalize()
    if lvl in ["Beginner", "Intermediate", "Advanced"]:
        return lvl
    return "Beginner"


def calculate_readiness_score(skills_table: List[Dict[str, Any]]) -> Tuple[float, str]:
    """
    Calculate an objective, mathematically transparent readiness score.
    Formula:
    Score = [ Sum( min(StudentLevelScore, RequiredLevelScore) * PriorityWeight ) /
              Sum( RequiredLevelScore * PriorityWeight ) ] * 100
    """
    total_max_weighted = 0
    total_attained_weighted = 0

    for item in skills_table:
        student_lvl = item.get("student_level", "None").lower()
        required_lvl = item.get("required_level", "Intermediate").lower()
        priority = item.get("priority", "Medium").lower()

        s_score = LEVEL_SCORES.get(student_lvl, 0)
        r_score = LEVEL_SCORES.get(required_lvl, 2)
        weight = PRIORITY_WEIGHTS.get(priority, 2)

        # Attained cannot exceed required for this metric
        attained = min(s_score, r_score)

        total_attained_weighted += (attained * weight)
        total_max_weighted += (r_score * weight)

    if total_max_weighted == 0:
        return 0.0, "No benchmark skills available."

    pct = round((total_attained_weighted / total_max_weighted) * 100, 1)

    formula_explanation = (
        f"Readiness Score: {pct}% | Calculated via weighted proficiency score "
        f"({total_attained_weighted} attained out of {total_max_weighted} benchmark points). "
        f"Skill weighting: High Priority = 3x, Medium Priority = 2x, Low Priority = 1x. "
        f"This score measures syllabus coverage against standard role benchmarks, not an arbitrary guarantee of employability."
    )

    return pct, formula_explanation


def perform_benchmark_gap_analysis(
    target_role: str,
    student_skills: Dict[str, str]
) -> List[Dict[str, Any]]:
    """
    Produce a deterministic, industry-grade baseline gap analysis
    using established role benchmarks.
    """
    benchmark = ROLE_BENCHMARKS.get(target_role)
    if not benchmark:
        # Generic role fallback
        benchmark = [
            {"skill": "Core Programming & Syntax", "required_level": "Advanced", "priority": "High", "topics": "Core language constructs, Data structures, Algorithms"},
            {"skill": "Frameworks & Standard Libraries", "required_level": "Intermediate", "priority": "High", "topics": "Primary framework conventions, Package management, Modularity"},
            {"skill": "Database & Storage Systems", "required_level": "Intermediate", "priority": "High", "topics": "CRUD operations, Query optimization, Data modeling"},
            {"skill": "System Architecture & APIs", "required_level": "Intermediate", "priority": "Medium", "topics": "REST/gRPC interfaces, Microservices vs Monoliths, Authentication"},
            {"skill": "Testing, Git & Version Control", "required_level": "Intermediate", "priority": "Medium", "topics": "Git workflows, Unit & integration testing, CI pipelines"},
            {"skill": "Deployment & Cloud Basics", "required_level": "Beginner", "priority": "Low", "topics": "Containerization, Cloud host deployment, Environment variables"}
        ]

    # Normalize student skills dictionary for case-insensitive lookup
    student_lookup = {k.strip().lower(): v for k, v in student_skills.items()}

    analysis_table = []

    for req in benchmark:
        req_skill = req["skill"]
        req_level = req["required_level"]
        priority = req["priority"]
        topics = req["topics"]

        # Check if student possesses this skill or similar
        matched_level = "None"
        req_lower = req_skill.lower()

        for s_name, s_lvl in student_lookup.items():
            # Check for keyword overlap
            keywords = [w for w in req_lower.replace("/", " ").replace("(", " ").replace(")", " ").split() if len(w) > 3]
            if s_name in req_lower or any(kw in s_name for kw in keywords):
                matched_level = normalize_level(s_lvl)
                break

        s_score = LEVEL_SCORES.get(matched_level.lower(), 0)
        r_score = LEVEL_SCORES.get(req_level.lower(), 2)

        if s_score >= r_score:
            status = "Possessed"
            gap_desc = f"Meets role requirement ({matched_level})"
        elif s_score > 0:
            status = "Needs Improvement"
            gap_desc = f"Partial proficiency: {matched_level} vs {req_level} needed"
        else:
            status = "Missing"
            gap_desc = f"Not found in profile: needs comprehensive training up to {req_level}"

        analysis_table.append({
            "skill": req_skill,
            "student_level": matched_level,
            "required_level": req_level,
            "status": status,
            "skill_gap": gap_desc,
            "priority": priority,
            "recommended_topics": topics
        })

    return analysis_table


def analyze_skill_gaps(
    student_profile: Dict[str, Any]
) -> Tuple[bool, Dict[str, Any], Optional[str]]:
    """
    Main function to analyze skill gaps using Gemini AI when configured,
    or accurate benchmark knowledge when API key is missing or calls fail.
    Returns (success, analysis_data_dict, error_or_info_message)
    """
    target_role = student_profile.get("target_role", "AI Engineer")
    student_skills = student_profile.get("skills_with_levels", {})

    # If Gemini API is configured, use LLM for deep contextual gap analysis
    if is_api_configured():
        prompt = f"""
You are an expert AI Career Coach and Tech Hiring Architect.
Analyze the following student profile against the industry requirements for the role of '{target_role}'.

Student Profile:
- Name: {student_profile.get('student_name', 'Student')}
- Education: {student_profile.get('education_level', 'Not specified')}
- College/University: {student_profile.get('university', 'Not specified')}
- Current Skills & Levels: {json.dumps(student_skills)}
- Target Role: {target_role}
- Available Study Time: {student_profile.get('study_hours_per_day', 2)} hours/day, {student_profile.get('study_days_per_week', 5)} days/week
- Learning Style: {student_profile.get('learning_style', 'Mixed')}

Strict Evaluation Guidelines:
1. Do not assume a skill is mastered if the student has not provided evidence of it.
2. If the student has not listed a skill, mark student_level as "None".
3. Contrast student's current proficiency with standard production-grade requirements.
4. Categorize each skill strictly into:
   - "Possessed": Student current level meets or exceeds required level.
   - "Needs Improvement": Student has beginner/intermediate skill, but target role requires higher.
   - "Missing": Student does not currently have this required skill.
5. Provide 7 to 9 relevant industry skills.
6. Provide specific, actionable learning topics for each skill.

Return your response in STRICT JSON format with the following structure:
{{
    "skills_analysis": [
        {{
            "skill": "Skill Name",
            "student_level": "None" | "Beginner" | "Intermediate" | "Advanced",
            "required_level": "Beginner" | "Intermediate" | "Advanced",
            "status": "Possessed" | "Needs Improvement" | "Missing",
            "skill_gap": "Clear descriptive statement of the gap",
            "priority": "High" | "Medium" | "Low",
            "recommended_topics": "Key subtopics and competencies to master"
        }}
    ],
    "overall_summary": "A 2-3 sentence personalized evaluation of the student's current standing."
}}
"""
        success, response_data, error_msg = generate_structured_json(
            prompt=prompt,
            system_instruction="You are a senior tech career coach. Provide objective, accurate, actionable skill assessments in valid JSON format."
        )

        if success and response_data and "skills_analysis" in response_data:
            table = response_data["skills_analysis"]
            score, explanation = calculate_readiness_score(table)

            # Separate into categories
            possessed = [s for s in table if s.get("status") == "Possessed"]
            improve = [s for s in table if s.get("status") == "Needs Improvement"]
            missing = [s for s in table if s.get("status") == "Missing"]

            result = {
                "skills_table": table,
                "possessed_skills": possessed,
                "improve_skills": improve,
                "missing_skills": missing,
                "readiness_score": score,
                "score_explanation": explanation,
                "overall_summary": response_data.get("overall_summary", ""),
                "is_ai_generated": True
            }
            return True, result, None

    # Fallback to benchmark-based deterministic analysis
    table = perform_benchmark_gap_analysis(target_role, student_skills)
    score, explanation = calculate_readiness_score(table)

    possessed = [s for s in table if s.get("status") == "Possessed"]
    improve = [s for s in table if s.get("status") == "Needs Improvement"]
    missing = [s for s in table if s.get("status") == "Missing"]

    summary = (
        f"Based on established technical benchmarks for {target_role}, you currently have "
        f"{len(possessed)} requirement(s) satisfied, {len(improve)} skill(s) requiring elevation to production proficiency, "
        f"and {len(missing)} core competency area(s) to acquire."
    )

    result = {
        "skills_table": table,
        "possessed_skills": possessed,
        "improve_skills": improve,
        "missing_skills": missing,
        "readiness_score": score,
        "score_explanation": explanation,
        "overall_summary": summary,
        "is_ai_generated": False
    }

    if not is_api_configured():
        return True, result, "API key not configured. Generated using industry benchmark evaluation."
    return True, result, "Gemini generation fallback used standard role benchmark dataset."
