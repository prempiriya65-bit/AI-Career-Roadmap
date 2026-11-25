# AI Career Roadmap & Skill Gap Finder

[![Python 3.10+](https://img.shields.io/badge/python-3.10--3.12-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.50+-FF4B4B.svg)](https://streamlit.io/)
[![Google Gemini API](https://img.shields.io/badge/Google%20GenAI-Gemini%202.5%20Flash-4285F4.svg)](https://ai.google.dev/)

A clean, lightweight Streamlit web application designed to help students and aspiring tech professionals eliminate career ambiguity. Powered by the **Google Gemini API** (`google-genai`), **Streamlit**, and **Plotly**, the app evaluates current programming and technical skills against industry role benchmarks, calculates a transparent readiness score, and builds a personalized **8-Week Learning Roadmap** plus **Three Tiered Portfolio Projects** with fallback support when offline or without an API key.

---

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [API Key Configuration](#api-key-configuration)
- [How to Run the Application](#how-to-run-the-application)
- [Running Tests](#running-tests)
- [Upload to GitHub](#upload-to-github)
- [Deploy on Streamlit Community Cloud](#deploy-on-streamlit-community-cloud)
- [Skill Readiness Scoring Methodology](#skill-readiness-scoring-methodology)

---

## Features

1. **Intelligent Student Profiling:**
   - Captures education level, college/university, daily and weekly study budget, and preferred learning style (`Practical Projects`, `Videos & Interactive Demos`, `Documentation & Books`, `Mixed (Balanced)`).
   - Dynamic proficiency matrix (`Beginner`, `Intermediate`, `Advanced`) for selected programming languages and technical tools.
   - Supports 9 standard tech roles (`AI Engineer`, `Machine Learning Engineer`, `Data Scientist`, `Data Analyst`, `Python Developer`, `Full Stack Developer`, `Web Developer`, `Cloud Engineer`, `Cybersecurity Engineer`) plus `Other (custom job role)`.
   - Includes a one-click **Load Demo Profile** for instant exploration.

2. **Skill Gap Finder:**
   - Categorizes competencies into **Possessed**, **Needs Improvement**, and **Missing Skills**.
   - Priority badges (`High`, `Medium`, `Low`), gap details, recommended subtopics, search/priority filtering, and CSV download.

3. **8-Week Personalized Learning Roadmap:**
   - Strictly adapts to your daily hours x weekly study days budget.
   - Provides weekly themes, target skills, daily tasks, hands-on exercises, milestone assignments, expected outcomes, interactive completion tracking, and roadmap regeneration.

4. **Three Tiered Portfolio Projects:**
   - Generates **Beginner**, **Intermediate**, and **Advanced** project blueprints with problem statements, tech stacks, key features, implementation steps, and expected deliverables.

5. **Interactive Analytics Dashboard & Exports:**
   - 4 Plotly charts (Competency Comparison, Gap Status Distribution, Priority Breakdown, and 8-Week Cumulative Study Hours).
   - Export full reports as **PDF** (`fpdf2`), **TXT**, or **CSV**.
   - Local assessment history saved in `data/history.json` with reload and delete controls.

6. **Curated Learning Resources:**
   - Searchable, verified documentation and course links mapped to missing and improvement skills.

---

## Technologies Used

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Web Framework** | Streamlit (`>=1.50.0`) | Multi-view reactive UI & session state |
| **Language** | Python `3.10 - 3.12` (recommended) | Core application runtime |
| **AI SDK** | `google-genai` (`>=1.0.0`) | Official Google Gemini GenAI SDK |
| **AI Models** | Gemini 2.5 Flash / 2.0 Flash / 1.5 Flash | Structured JSON gap & roadmap generation |
| **Visualizations** | Plotly (`>=5.20.0`) | Interactive charts and progress curves |
| **Data Processing** | Pandas (`>=2.2.0`) | Tabular skill matrices & CSV export |
| **PDF Export** | FPDF2 (`>=2.8.0`) | Branded multi-page A4 PDF reports |

---

## Project Structure

```text
AI-Career-Roadmap/
├── app.py                          # Main Streamlit entrypoint & sidebar router
├── requirements.txt                # Production Python dependencies
├── README.md                       # Project documentation & deployment guide
├── test_app.py                     # Automated module & export test suite
├── .gitignore                      # Excludes .venv, __pycache__, secrets.toml, .env
│
├── .streamlit/
│   ├── config.toml                 # Theme colors, server settings & nav config
│   └── secrets.toml.example        # Template for Google Gemini API key
│
├── modules/
│   ├── __init__.py
│   ├── gemini_service.py           # Google GenAI client, fallback & JSON parser
│   ├── skill_analyzer.py           # Benchmark gap engine & readiness calculator
│   ├── roadmap_generator.py        # 8-week curriculum generator
│   ├── project_generator.py        # 3-tier portfolio project generator
│   └── report_generator.py         # PDF, TXT, CSV exports & history persistence
│
├── pages/
│   ├── __init__.py
│   ├── home.py                     # Intake form, validation & demo loader
│   ├── dashboard.py                # KPI summary, Plotly charts & exports
│   ├── skill_gap.py                # Segmented skill tables & filters
│   ├── roadmap.py                  # Interactive 8-week curriculum tracker
│   ├── projects.py                 # 3 portfolio project blueprints
│   ├── resources.py                # Searchable verified learning resources
│   ├── history.py                  # Saved assessment history manager
│   └── about.py                    # Methodology & architecture overview
│
├── assets/
│   └── style.css                   # Custom SaaS styling & status badges
│
└── data/
    └── history.json                # Local JSON persistence for assessments
```

---

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/<your-username>/AI-Career-Roadmap.git
   cd AI-Career-Roadmap
   ```

2. **Create and activate a Python virtual environment:**
   - **Windows (PowerShell):**
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```
   - **macOS / Linux:**
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## API Key Configuration

This application uses the **Google Gemini API** via the `GEMINI_API_KEY` secret (it also checks the `GOOGLE_API_KEY` environment variable as a fallback).

> **Note:** An API key is **recommended** for live AI-tailored generation, but **not strictly required** to explore the app. Without a key, the app automatically falls back to built-in industry role benchmarks and deterministic templates.

### Option 1: Local Streamlit Secrets (Recommended for Local Development)

1. Get a free API key from [Google AI Studio](https://aistudio.google.com/).
2. Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml`:
   - **Windows (PowerShell):**
     ```powershell
     Copy-Item .streamlit\secrets.toml.example .streamlit\secrets.toml
     ```
   - **macOS / Linux:**
     ```bash
     cp .streamlit/secrets.toml.example .streamlit/secrets.toml
     ```
3. Replace `YOUR_GEMINI_API_KEY` inside `.streamlit/secrets.toml`:
   ```toml
   GEMINI_API_KEY = "your-actual-gemini-api-key"
   ```
   *(`.streamlit/secrets.toml` is listed in `.gitignore` so it will never be committed to GitHub.)*

### Option 2: Environment Variable

```powershell
# Windows PowerShell
$env:GEMINI_API_KEY="your-actual-gemini-api-key"
```
```bash
# macOS / Linux
export GEMINI_API_KEY="your-actual-gemini-api-key"
```

### Option 3: In-App Sidebar Input

When the app is running, open **Gemini AI Connection -> Setup Gemini API Key** in the sidebar to store your key in the current browser session only.

---

## How to Run the Application

From the project root directory (with your virtual environment activated):

```bash
streamlit run app.py
```

Open your browser to `http://localhost:8501`.

---

## Running Tests

Run the included validation suite from the project root:

```bash
python test_app.py
```

Expected output: `ALL TESTS PASSED SUCCESSFULLY! (6/6 TEST SUITES)`

---

## Upload to GitHub

1. **Verify sensitive/local files are ignored** (`.venv/`, `__pycache__/`, `.streamlit/secrets.toml`, `.env` must NOT appear):
   ```bash
   git status
   ```
2. **Stage and commit your cleaned project:**
   ```bash
   git add .
   git commit -m "Prepare clean AI Career Roadmap project for GitHub and Streamlit Cloud"
   ```
3. **Create a new repository on GitHub** (e.g., `AI-Career-Roadmap`) without initializing an extra README or `.gitignore`.
4. **Add the remote and push:**
   ```bash
   git remote add origin https://github.com/<your-username>/AI-Career-Roadmap.git
   git branch -M main
   git push -u origin main
   ```

---

## Deploy on Streamlit Community Cloud

1. Push your repository to GitHub (see steps above).
2. Sign in to [share.streamlit.io](https://share.streamlit.io/) with your GitHub account.
3. Click **Create app** -> **Yup, I have an app** (or **Deploy a public app from GitHub**).
4. Configure deployment settings:
   - **Repository:** `<your-username>/AI-Career-Roadmap`
   - **Branch:** `main`
   - **Main file path:** `app.py`
   - **Advanced settings -> Python version:** Select `3.11` or `3.12` (recommended for maximum wheel compatibility).
5. **Configure Secrets** (before or right after clicking Deploy):
   - Open **App settings -> Secrets** in Streamlit Community Cloud.
   - Paste:
     ```toml
     GEMINI_API_KEY = "your-actual-gemini-api-key"
     ```
   - Click **Save**.
6. Wait for dependencies from `requirements.txt` to install and your app will go live!

---

## Skill Readiness Scoring Methodology

The **Overall Skill Readiness Score** uses a transparent weighted curriculum coverage formula:

$$\text{Readiness Score} = \left( \frac{\sum_{i=1}^{N} \min(S_i, R_i) \times W_i}{\sum_{i=1}^{N} R_i \times W_i} \right) \times 100$$

Where:
- $S_i \in \{0, 1, 2, 3\}$: Student proficiency (`None=0`, `Beginner=1`, `Intermediate=2`, `Advanced=3`)
- $R_i \in \{1, 2, 3\}$: Target role requirement
- $W_i \in \{1, 2, 3\}$: Skill priority weight (`High=3`, `Medium=2`, `Low=1`)
