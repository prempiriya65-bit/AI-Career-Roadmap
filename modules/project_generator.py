"""
Project Generator Module
Generates exactly three tailored portfolio project specifications (Beginner, Intermediate, Advanced)
relevant to the selected target career role using Gemini AI or domain project suites.
"""

import json
from typing import Dict, Any, List, Tuple, Optional
from modules.gemini_service import generate_structured_json, is_api_configured

ROLE_PROJECT_PRESETS = {
    "AI Engineer": [
        {
            "title": "Multimodal Document Intelligence & Semantic Q&A Agent",
            "difficulty_level": "Beginner",
            "problem_statement": "Organizations struggle to search and extract actionable insights from long PDF manuals, tables, and scanned reports without losing contextual accuracy.",
            "description": "An end-to-end Retrieval-Augmented Generation (RAG) assistant that parses multi-format documents, generates semantic embeddings, and answers complex user queries with cited source passages.",
            "technologies": ["Python", "FastAPI", "LangChain/LlamaIndex", "ChromaDB", "Google Gemini API / HuggingFace", "Streamlit"],
            "main_features": [
                "Automated PDF & Markdown document parsing with table extraction",
                "Recursive character text chunking and vector embedding generation",
                "Hybrid vector + keyword search retrieval pipeline",
                "Source citation verification and hallucination reduction guardrails",
                "Streamlit chat interface with confidence scoring"
            ],
            "implementation_steps": [
                "Step 1: Set up document ingestion pipeline with PyPDF and chunking logic.",
                "Step 2: Initialize ChromaDB vector store and index text chunks using modern embeddings.",
                "Step 3: Construct prompt template with context window injection and query formulation.",
                "Step 4: Connect Gemini API or local open LLM with citation grounding.",
                "Step 5: Build intuitive Streamlit chat UI with upload drawer and history."
            ],
            "expected_output": "A live web application where users upload PDFs and interact with an AI chatbot that answers questions with exact page references and quotes."
        },
        {
            "title": "Autonomous Code Review & Security Audit Agent",
            "difficulty_level": "Intermediate",
            "problem_statement": "Engineering teams spend hundreds of hours manually reviewing pull requests for style compliance, subtle logical bugs, and security vulnerabilities like OWASP Top 10.",
            "description": "An intelligent GitHub bot agent that automatically reviews incoming Pull Requests, detects code smells, flags security vulnerabilities, and proposes git patch diffs directly on GitHub.",
            "technologies": ["Python", "GitHub Webhooks API", "Docker", "Pytest", "Tree-sitter", "Gemini 2.5 Flash", "Redis"],
            "main_features": [
                "Automated webhook receiver listening to GitHub PR events",
                "Abstract Syntax Tree (AST) code parsing for syntax structure",
                "Vulnerability detection for SQL injection, secrets leaks, and buffer overflows",
                "Automated PR comment generator with markdown diff snippets",
                "Async task queue processing using Celery and Redis"
            ],
            "implementation_steps": [
                "Step 1: Build FastAPI webhook server to authenticate and receive GitHub pull request payloads.",
                "Step 2: Parse changed file patches using GitPython and AST tooling.",
                "Step 3: Engineer multi-stage LLM prompts evaluating security, complexity, and styling.",
                "Step 4: Use GitHub REST API to post inline line comments and review summaries.",
                "Step 5: Package inside a Docker container with rate-limiting and logging."
            ],
            "expected_output": "A working GitHub bot that comments actionable code reviews and security fixes on GitHub PRs within 15 seconds."
        },
        {
            "title": "Production-Grade Distributed Agentic Workflow Orchestrator",
            "difficulty_level": "Advanced",
            "problem_statement": "Complex enterprise tasks require multiple collaborative AI agents with memory, tool execution, human-in-the-loop approvals, and strict latency SLAs.",
            "description": "A distributed multi-agent system orchestrating specialized worker agents (Researcher, Coder, Verifier) coordinated by a supervisor model with persistent state memory and observability.",
            "technologies": ["Python", "LangGraph", "FastAPI", "PostgreSQL", "Docker Compose", "Prometheus", "OpenTelemetry", "Gemini API"],
            "main_features": [
                "Multi-agent supervisor graph managing parallel task delegations",
                "Tool registry allowing agents to run sandboxed code, search APIs, and query SQL",
                "Persistent state checkpoints and human-in-the-loop review interruptions",
                "Telemetry dashboard tracking token costs, latency, and step transitions",
                "High-concurrency async execution with failover and retry mechanics"
            ],
            "implementation_steps": [
                "Step 1: Define cyclic agent graph schema with state reducer functions.",
                "Step 2: Implement tool execution layer with sandbox isolation and timeouts.",
                "Step 3: Connect PostgreSQL for workflow state persistence and replayability.",
                "Step 4: Integrate OpenTelemetry instrumentation for distributed tracing.",
                "Step 5: Deploy full microservices stack using Docker Compose and write documentation."
            ],
            "expected_output": "A production microservice with REST and WebSocket APIs capable of executing complex multi-step workflows with real-time UI monitoring."
        }
    ],
    "Machine Learning Engineer": [
        {
            "title": "Customer Churn Prediction & Explainability Dashboard",
            "difficulty_level": "Beginner",
            "problem_statement": "Subscription businesses lose revenue due to customer churn without understanding the underlying risk factors.",
            "description": "A supervised machine learning classification pipeline predicting customer churn probability with SHAP model explainability and interactive scenario simulation.",
            "technologies": ["Python", "Scikit-Learn", "XGBoost", "SHAP", "Pandas", "Streamlit"],
            "main_features": [
                "Automated data preprocessing, outlier clipping, and one-hot encoding",
                "Trained XGBoost and LightGBM models evaluated with ROC-AUC and PR-AUC curves",
                "SHAP waterfall charts explaining individual prediction drivers",
                "Interactive 'What-If' simulator to test retention offers"
            ],
            "implementation_steps": [
                "Step 1: Clean and explore Kaggle Telco Churn dataset.",
                "Step 2: Build Scikit-Learn ColumnTransformer pipeline with Cross-Validation.",
                "Step 3: Tune XGBoost hyperparameters via Optuna.",
                "Step 4: Compute SHAP values for global and local interpretability.",
                "Step 5: Deploy interactive dashboard in Streamlit."
            ],
            "expected_output": "A deployed web app allowing marketing managers to input customer metrics and receive churn risk with feature explanations."
        },
        {
            "title": "Real-Time Fraud Detection Pipeline with Feature Store",
            "difficulty_level": "Intermediate",
            "problem_statement": "Financial transactions require millisecond-latency anomaly detection to prevent fraudulent credit card charges.",
            "description": "A streaming ML pipeline ingesting transaction streams, serving pre-computed features via Feast feature store, and flagging anomalous transactions in real time.",
            "technologies": ["Python", "FastAPI", "Feast", "Redis", "Kafka / Kafka-mock", "Scikit-Learn", "Docker"],
            "main_features": [
                "Event-driven transaction consumer with rolling aggregation features",
                "Sub-10ms model inference endpoint using ONNX runtime",
                "Online feature retrieval from Redis key-value store",
                "Automated drift detection alerts when transaction distributions shift"
            ],
            "implementation_steps": [
                "Step 1: Set up Feast feature store definitions for user transaction velocity.",
                "Step 2: Train Random Forest and Isolation Forest anomaly models.",
                "Step 3: Export trained model to ONNX format for rapid inference.",
                "Step 4: Create FastAPI prediction microservice with Redis caching.",
                "Step 5: Containerize and benchmark endpoint under simulated load."
            ],
            "expected_output": "A high-performance Dockerized prediction API processing simulated payment streams with sub-15ms response times."
        },
        {
            "title": "End-to-End MLOps Platform with Automated CI/CD & Model Registry",
            "difficulty_level": "Advanced",
            "problem_statement": "Machine learning models degrade over time without automated retraining pipelines, experiment tracking, and canary deployments.",
            "description": "A full-lifecycle MLOps infrastructure featuring automated data validation, DVC versioning, MLflow model registry, and GitHub Actions CI/CD deploying to Kubernetes.",
            "technologies": ["Python", "MLflow", "DVC", "Evidently AI", "GitHub Actions", "Docker", "Kubernetes", "AWS/GCP"],
            "main_features": [
                "Data version control with DVC tracking S3 storage buckets",
                "Automated retraining triggers upon detecting data drift via Evidently AI",
                "MLflow tracking server managing model staging and production tagging",
                "GitHub Actions pipeline running unit tests, data schema validation, and image builds",
                "Zero-downtime blue/green deployment rollout"
            ],
            "implementation_steps": [
                "Step 1: Configure MLflow server and DVC remote storage.",
                "Step 2: Build reproducible training pipeline with Hydra configuration.",
                "Step 3: Implement data quality test suite using Great Expectations.",
                "Step 4: Write GitHub Actions workflow building Docker image on git tag push.",
                "Step 5: Deploy deployment manifest with health checks to a Kubernetes cluster."
            ],
            "expected_output": "A battle-tested production MLOps repository demonstrating automated retraining, tracking, and canary deployment."
        }
    ],
    "Data Scientist": [
        {
            "title": "E-Commerce Market Basket & Recommendation Engine",
            "difficulty_level": "Beginner",
            "problem_statement": "Retail platforms fail to maximize average order value without personalized product recommendations.",
            "description": "A collaborative filtering and association rule mining engine that uncovers purchasing patterns and generates real-time cross-sell product suggestions.",
            "technologies": ["Python", "Pandas", "Scikit-Learn", "Surprise", "Plotly", "Streamlit"],
            "main_features": [
                "Apriori and FP-Growth association rule generation (Support, Confidence, Lift)",
                "Singular Value Decomposition (SVD) matrix factorization for user recommendations",
                "Interactive basket visualizer with network graphs",
                "Revenue uplift simulation calculator"
            ],
            "implementation_steps": [
                "Step 1: Perform exploratory analysis on retail transactional data.",
                "Step 2: Implement item-item collaborative filtering algorithms.",
                "Step 3: Evaluate models using RMSE and Mean Average Precision (MAP@K).",
                "Step 4: Build network relationship visualization with Plotly.",
                "Step 5: Package as a Streamlit business dashboard."
            ],
            "expected_output": "A business intelligence application demonstrating cross-sell recommendations with interactive graphs."
        },
        {
            "title": "Healthcare Clinical Outcome Prediction & Biomarker Analysis",
            "difficulty_level": "Intermediate",
            "problem_statement": "Early identification of patient risk factors in chronic conditions significantly improves patient survival rates.",
            "description": "A clinical data science system analyzing patient electronic health records to predict readmission risks and identify significant clinical biomarkers.",
            "technologies": ["Python", "Statsmodels", "XGBoost", "SciPy", "Pandas", "Seaborn"],
            "main_features": [
                "Multivariate survival analysis and Cox Proportional Hazards modeling",
                "Rigorous statistical hypothesis testing (ANOVA, Chi-square, Mann-Whitney)",
                "Propensity score matching to control for confounding variables",
                "Clinical risk score calculator with interactive calibration curves"
            ],
            "implementation_steps": [
                "Step 1: Clean clinical datasets and address missing value patterns.",
                "Step 2: Formulate statistical hypotheses and verify normality assumptions.",
                "Step 3: Train ensemble classifiers with strict cross-validation.",
                "Step 4: Measure calibration, Brier score, and decision curve analysis.",
                "Step 5: Author a reproducible academic research report with charts."
            ],
            "expected_output": "A research-grade analysis repository with validated statistical models and clinical decision curves."
        },
        {
            "title": "Enterprise Demand Forecasting & Inventory Optimization Suite",
            "difficulty_level": "Advanced",
            "problem_statement": "Supply chain miscalculations lead to millions in inventory holding costs and out-of-stock lost revenue.",
            "description": "A hierarchical time-series forecasting platform incorporating macro-economic trends, weather data, and promotional schedules to optimize warehouse replenishment.",
            "technologies": ["Python", "Prophet", "NeuralProphet", "Statsforecast", "PySpark", "Optuna", "FastAPI"],
            "main_features": [
                "Hierarchical reconciliation across SKU, store, and regional levels",
                "Automated changepoint and seasonality detection with exogenous regressors",
                "Dynamic safety stock and economic order quantity (EOQ) optimization",
                "Automated forecast evaluation pipeline measuring WAPE and MASE"
            ],
            "implementation_steps": [
                "Step 1: Ingest multi-year transactional time-series data with PySpark.",
                "Step 2: Benchmark statistical models (AutoARIMA, ETS) vs Deep Learning (N-BEATS).",
                "Step 3: Construct bottom-up and top-down hierarchical reconciliation.",
                "Step 4: Integrate cost optimization linear programming with PuLP.",
                "Step 5: Expose forecasting endpoints via FastAPI with automated weekly batch runs."
            ],
            "expected_output": "A complete enterprise forecasting engine delivering automated multi-horizon inventory recommendations."
        }
    ]
}


def build_fallback_projects(target_role: str) -> List[Dict[str, Any]]:
    """Return verified domain portfolio projects for the role."""
    if target_role in ROLE_PROJECT_PRESETS:
        return ROLE_PROJECT_PRESETS[target_role]

    # Clean generic tech project suite for other roles
    return [
        {
            "title": f"Foundation {target_role} Core Utility Application",
            "difficulty_level": "Beginner",
            "problem_statement": f"Junior practitioners need a reliable portfolio project demonstrating core design patterns and automated testing in {target_role}.",
            "description": f"A modular, well-tested core system applying industry standard practices, clean code separation, and comprehensive documentation for {target_role}.",
            "technologies": ["Python", "Git", "Pytest", "FastAPI / SQLite", "Docker"],
            "main_features": [
                "Modular architecture separating business logic from interfaces",
                "Unit and integration test suite with >85% code coverage",
                "Comprehensive logging, configuration management, and input validation",
                "Interactive demonstration interface"
            ],
            "implementation_steps": [
                "Step 1: Set up modular repository layout with poetry or venv.",
                "Step 2: Implement core business logic classes with type annotations.",
                "Step 3: Write Pytest test suites covering normal and edge cases.",
                "Step 4: Add configuration via environment variables and .env.",
                "Step 5: Create README with architecture diagrams and setup steps."
            ],
            "expected_output": "A clean, production-standard GitHub repository demonstrating foundational software craftsmanship."
        },
        {
            "title": f"Full-Stack {target_role} Service with Cloud Integration",
            "difficulty_level": "Intermediate",
            "problem_statement": f"Real-world {target_role} applications must handle asynchronous data flows, user authentication, and secure database persistence.",
            "description": f"An asynchronous full-stack microservice with database persistence, JWT authentication, and RESTful API endpoints tailored to {target_role}.",
            "technologies": ["Python", "PostgreSQL", "Docker Compose", "Redis", "FastAPI"],
            "main_features": [
                "Secure user authentication with JWT and bcrypt password hashing",
                "Relational schema migrations using Alembic",
                "Caching layer using Redis for high read performance",
                "Containerized local development with Docker Compose"
            ],
            "implementation_steps": [
                "Step 1: Design database schema and ER diagrams.",
                "Step 2: Build RESTful API endpoints with Pydantic request/response schemas.",
                "Step 3: Implement security, token verification, and rate limiting.",
                "Step 4: Write Docker Compose file for service and database dependencies.",
                "Step 5: Write API documentation with Swagger/OpenAPI."
            ],
            "expected_output": "A containerized microservice repository with Swagger API documentation and reproducible docker-compose setup."
        },
        {
            "title": f"Enterprise-Grade Distributed {target_role} Platform",
            "difficulty_level": "Advanced",
            "problem_statement": f"Large organizations require high-availability, distributed scalability, and observability for mission-critical {target_role} workloads.",
            "description": f"An enterprise distributed platform featuring CI/CD automated deployment, metrics monitoring, resilience patterns, and cloud scalability for {target_role}.",
            "technologies": ["Python", "Kubernetes", "Prometheus", "Grafana", "GitHub Actions", "Cloud Provider"],
            "main_features": [
                "Asynchronous message queuing and background task workers",
                "Prometheus metrics scraping and Grafana dashboard visualization",
                "Automated CI/CD deployment pipeline with staging/production promotion",
                "Zero-downtime health probes and circuit-breaker failure isolation"
            ],
            "implementation_steps": [
                "Step 1: Build core distributed worker architecture.",
                "Step 2: Instrument application with Prometheus metrics counters and histograms.",
                "Step 3: Configure GitHub Actions CI workflow running linting, security, and tests.",
                "Step 4: Write Helm charts or Kubernetes manifests with Horizontal Pod Autoscaler.",
                "Step 5: Publish deployment guide and live demonstration link."
            ],
            "expected_output": "A battle-ready cloud-native architecture demonstrating senior-level system design and deployment skills."
        }
    ]


def generate_portfolio_projects(
    student_profile: Dict[str, Any],
    skill_analysis: Dict[str, Any]
) -> Tuple[bool, List[Dict[str, Any]], Optional[str]]:
    """
    Generate exactly three tailored portfolio project specifications using Gemini AI or domain presets.
    """
    target_role = student_profile.get("target_role", "AI Engineer")
    missing = [s["skill"] for s in skill_analysis.get("missing_skills", [])]
    improve = [s["skill"] for s in skill_analysis.get("improve_skills", [])]

    if is_api_configured():
        prompt = f"""
You are an expert tech career advisor and software engineering portfolio evaluator.
Generate EXACTLY THREE impressive, real-world portfolio project ideas for a student targeting the role of '{target_role}'.

Context:
- Target Role: {target_role}
- Education: {student_profile.get('education_level', 'College')}
- Missing Skills to Showcase: {json.dumps(missing)}
- Skills Needing Improvement: {json.dumps(improve)}

Requirements:
1. Provide EXACTLY 3 projects with three distinct levels of difficulty:
   - Project 1: "Beginner" (Solid foundation, clean structure, builds confidence)
   - Project 2: "Intermediate" (Production patterns, database/API integration, testing)
   - Project 3: "Advanced" (Distributed systems / End-to-end cloud deployment / MLOps or Enterprise grade)
2. For EACH project, include:
   - title (Professional, attractive name)
   - difficulty_level ("Beginner", "Intermediate", or "Advanced")
   - problem_statement (Real-world business or engineering problem solved)
   - description (Clear 2-3 sentence overview)
   - technologies (Array of 5-7 specific tech/libraries)
   - main_features (Array of 4-5 bullet features)
   - implementation_steps (Array of 5 chronological implementation steps)
   - expected_output (Tangible final deliverable)

Return strictly a JSON object with a single key "projects" containing the array of 3 projects:
{{
    "projects": [
        {{
            "title": "...",
            "difficulty_level": "Beginner",
            "problem_statement": "...",
            "description": "...",
            "technologies": ["..."],
            "main_features": ["..."],
            "implementation_steps": ["Step 1: ...", "Step 2: ...", ...],
            "expected_output": "..."
        }}
    ]
}}
"""
        success, response_data, error_msg = generate_structured_json(
            prompt=prompt,
            system_instruction="You are a senior tech hiring manager. Return valid JSON containing exactly three project specifications."
        )

        if success and response_data and "projects" in response_data:
            projects = response_data["projects"]
            if isinstance(projects, list) and len(projects) == 3:
                return True, projects, None

    # Fallback to high quality role presets
    presets = build_fallback_projects(target_role)
    if not is_api_configured():
        return True, presets, "API key not configured. Provided verified portfolio project blueprints."
    return True, presets, "Generated portfolio projects using standard industry blueprints."
