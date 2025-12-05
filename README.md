
# 🩺 Physician Notetaker – AI Medical Conversation Analyzer

Live Demo: **[https://saik2026-demo.hf.space/physician-notetaker/](https://saik2026-demo.hf.space/physician-notetaker/)**

---

## 1. Project Overview

**Physician Notetaker** is an AI-powered web application that transforms raw physician–patient conversations into structured, clinically useful insights.

The system takes a medical conversation transcript as input and automatically:

- Extracts key medical entities (Symptoms, Treatment, Diagnosis, Prognosis)
- Analyzes patient sentiment and intent
- Generates a structured SOAP note (Subjective, Objective, Assessment, Plan)
- Presents everything in an intuitive, modern chat-style UI

This project showcases how **LLMs, LangChain, Groq, and Django** can be combined to build a practical, production-style medical NLP assistant suitable for clinics, medico-legal reporting, and healthcare analytics.

---

## 2. Problem Statement

Healthcare professionals spend a significant portion of their time on **documentation**, especially after patient consultations. Manual note-taking from conversations leads to:

- Lost time and reduced face-to-face patient interaction  
- Inconsistent documentation quality  
- Risk of missing important clinical details  
- Difficulty standardizing records for analytics, audits, or legal use  

At the same time, raw consultation transcripts are **unstructured** and **hard to use** directly in workflows.

**Physician Notetaker** addresses this by:

1. Converting free-form medical dialogue into:
   - Key clinical entities: Symptoms, treatments, diagnoses, prognosis
   - Sentiment and patient intent (e.g., anxious, reassured, seeking reassurance)
   - Structured SOAP notes ready for EMR systems or reports

2. Providing a **recruiter-friendly demo** UI where a user can:
   - Paste any physician–patient conversation
   - Get instant, AI-generated medical analysis and documentation
   - See NER, sentiment, and SOAP outputs clearly separated

This demonstrates a real-world, end-to-end **LLM + backend + UI** pipeline relevant to healthcare, data science, and applied NLP roles.

---

## 3. File Structure

Project root:

```
c:/Users/chskc/Desktop/no parking/physician-notetaker/
├── Dockerfile
├── requirements.txt
├── start.py
├── start.sh
└── physician-notetaker/
    ├── .env
    ├── manage.py
    ├── db.sqlite3
    ├── file.bat
    ├── main.py
    ├── output_results.json
    ├── README.md
    │
    ├── chatbot_project/         # Django project configuration
    │   ├── __init__.py
    │   ├── asgi.py              # ASGI entrypoint
    │   ├── wsgi.py              # WSGI entrypoint (used by gunicorn)
    │   ├── settings.py          # Django settings (INSTALLED_APPS, DB, static, etc.)
    │   └── urls.py              # Root URL routing, includes chat app URLs
    │
    ├── chat/                    # Django app for the chat UI & API
    │   ├── __init__.py
    │   ├── admin.py             # (Default) Django admin registration
    │   ├── apps.py              # App config
    │   ├── models.py            # (Currently unused) DB models placeholder
    │   ├── urls.py              # Chat app URLs (/chat/, /chat/api/, etc.)
    │   ├── views.py             # Core views: chat page + AI analysis API endpoints
    │   ├── tests.py
    │   ├── templates/
    │   │   └── chat/
    │   │       └── chat.html    # Tailwind-based medical chatbot UI
    │   └── __pycache__/         # Python bytecode cache (ignored in development)
    │
    ├── src/                     # AI / NLP logic (framework-agnostic)
    │   ├── __init__.py
    │   ├── config.py            # Loads GROQ_API_KEY, model name, temperature, etc.
    │   │
    │   ├── chains/              # LangChain-based chains for each task
    │   │   ├── __init__.py
    │   │   ├── ner_chain.py     # Multi-step NER pipeline (validation → extraction → correction)
    │   │   ├── sentiment_chain.py # Sentiment & intent analysis pipeline
    │   │   └── soap_chain.py    # SOAP note generation pipeline
    │   │
    │   ├── prompts/             # Prompt templates for LLMs
    │   │   ├── __init__.py
    │   │   ├── ner_prompts.py       # Prompts for medical NER & validation
    │   │   ├── sentiment_prompts.py # Prompts for sentiment & intent detection
    │   │   └── soap_prompts.py      # Prompts for SOAP note generation
    │   │
    │   ├── utils/
    │   │   ├── __init__.py
    │   │   └── validators.py    # (Optional) helper/validation utilities
    │   │
    │   └── __pycache__/         # Python bytecode cache
    │
    └── staticfiles/             # Collected static files (primarily Django admin)
        └── admin/
            ├── css/             # Admin CSS bundle
            ├── img/             # Admin icons and images
            └── js/              # Admin JavaScript bundle
```

### Key Components

- **`chat/templates/chat/chat.html`**  
  Fully designed, responsive UI for the medical chatbot using Tailwind, Font Awesome, and inline JS animations.

- **`chat/views.py`**  
  - `chat_view`: Renders the chat UI  
  - `chat_api`: Accepts a conversation, calls the LangChain + Groq pipelines, returns JSON with NER, sentiment, and SOAP note

- **`src/chains/*.py`**  
  - `ner_chain.py`: Uses `ChatGroq` + prompt templates + validation logic to extract:
    - Symptoms, Treatment, Diagnosis, Prognosis
  - `sentiment_chain.py`: Classifies patient sentiment and intent
  - `soap_chain.py`: Generates a structured SOAP note (Subjective, Objective, Assessment, Plan)

- **`src/config.py`**  
  Central configuration for:
  - Groq API key and model
  - Temperature settings
  - Timeout and other LLM parameters

- **`Dockerfile`**  
  Production-ready container configuration for running Django + Gunicorn on Hugging Face Spaces (port 7860).

- **`start.py` / `start.sh`**  
  Startup helpers to run Gunicorn/Django in the deployment environment.

---

## 4. Setup Instructions

### 4.1. Prerequisites

- Python 3.11+
- pip / venv
- A **Groq API key** (for LLM inference)
- Git (optional, if cloning from a repo)

### 4.2. Clone the Project

```
git clone <your-repo-url> physician-notetaker
cd physician-notetaker/physician-notetaker
```

### 4.3. Create and Activate Virtual Environment

```
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 4.4. Install Dependencies

From the project root (where `requirements.txt` is located):

```
pip install --upgrade pip
pip install -r ../requirements.txt
```

### 4.5. Configure Environment Variables

Create a `.env` file inside `physician-notetaker/`:

```
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.1-8b-instant
DJANGO_SECRET_KEY=your_django_secret_key_here
DJANGO_DEBUG=True
```

> On Hugging Face Spaces, set `GROQ_API_KEY` as a **secret** in the Space settings.

### 4.6. Run Database Migrations

```
cd physician-notetaker
python manage.py migrate
```

(Optional) Create a Django superuser:

```
python manage.py createsuperuser
```

### 4.7. Run Locally (Development)

```
python manage.py runserver
```

Then open:

- http://127.0.0.1:8000/chat/  
  or  
- http://127.0.0.1:8000/

### 4.8. Run via Gunicorn (Production-style)

```
gunicorn chatbot_project.wsgi:application --bind 0.0.0.0:7860
```

---

## 5. Usage / How to Use

### 5.1. Accessing the App

- **Local**:  
  `http://127.0.0.1:8000/chat/`
- **Deployed (Hugging Face Space)**:  
  `https://saik2026-demo.hf.space/physician-notetaker/`

### 5.2. Steps for a Typical User (Doctor / Reviewer)

1. **Open the web app**  
   Navigate to the URL and you’ll see a modern chat-style medical UI.

2. **Paste a conversation**  
   Copy any physician–patient dialogue (for example, the whiplash injury case) into the text area:
   - The conversation can include both physician and patient turns.
   - The UI shows live character and word counts.

3. **Click “Analyze” (or press Ctrl+Enter)**  
   The app:
   - Sends the conversation to the backend `/chat/api/`
   - LLM (via Groq + LangChain) runs:
     - Medical NER
     - Sentiment & intent analysis
     - SOAP note generation

4. **Review the results**  
   The bot reply includes three sections:

   - **NER Card**
     - Symptoms (e.g., neck pain, back pain, stiffness)
     - Treatment (e.g., physiotherapy, painkillers)
     - Diagnosis (e.g., whiplash injury)
     - Prognosis (e.g., full recovery expected within six months)

   - **Sentiment & Intent Card**
     - Overall sentiment: Anxious / Neutral / Reassured
     - Intents: Seeking reassurance, reporting symptoms, etc.
     - Confidence level and supporting patient quotes

   - **SOAP Note Card**
     - Subjective: Chief complaint & HPI
     - Objective: Physical exam findings
     - Assessment: Diagnosis & severity
     - Plan: Treatment, follow-up, prognosis

5. **Iterate & Experiment**
   - Use the “Try Sample” button to load a pre-defined conversation.
   - Modify or paste new transcripts to see how the model generalizes.
   - Use copy/export buttons (if implemented) to reuse the generated documentation.

---

## 6. Technology Stack

### Backend

- **Python 3.11**
- **Django 5.x** – Web framework for routing, views, and templates
- **Gunicorn** – WSGI server for production-style deployment
- **SQLite** – Default Django database for local storage

### AI / NLP

- **Groq + Llama models** – LLM inference via Groq API  
- **LangChain** – Orchestrating prompts and multi-step chains:
  - `langchain`
  - `langchain-groq`
- **Custom Prompt Engineering** for:
  - Medical NER
  - Sentiment & intent analysis
  - SOAP note generation

### Frontend

- **HTML5 / CSS3 / JavaScript**
- **Tailwind CSS** (CDN) – Utility-first styling
- **Font Awesome** – Icons
- **Anime.js** – Smooth animations/transitions
- Responsive, mobile-first layout (works on phones, tablets, laptops)

### Deployment

- **Dockerfile** – Containerized deployment
- **Gunicorn** – Production server
- **Hugging Face Spaces** – Hosting (live demo)

---

## 7. Features

### 7.1. End-to-End Medical NLP Pipeline

- **Named Entity Recognition (NER)**  
  Extracts:
  - `Symptoms` (e.g., neck pain, back pain, stiffness)
  - `Treatment` (e.g., painkillers, physiotherapy)
  - `Diagnosis` (e.g., whiplash injury)
  - `Prognosis` (e.g., full recovery expected within six months)

- **Sentiment & Intent Analysis**
  - Classifies patient sentiment as:
    - Anxious
    - Neutral
    - Reassured
  - Detects patient intent:
    - Seeking reassurance
    - Reporting symptoms
    - Expressing concern
    - Acknowledging improvement

- **SOAP Note Generation**
  - Converts raw dialogue into a structured SOAP note:
    - Subjective – Chief complaint, HPI
    - Objective – Exam findings
    - Assessment – Diagnosis & severity
    - Plan – Treatment, follow-up, prognosis

### 7.2. Modern Medical Chat UI

- Clean, **clinic-style UI** with:
  - Gradient header, glassmorphism cards
  - Clear sections for NER, sentiment, and SOAP results
- Fully **responsive**:
  - Optimized layouts for mobile, tablet, and desktop
- Interactive UX:
  - Typing indicator
  - Animated cards
  - Quick actions: “Try Sample”, “Help”, “Features”
  - Character counter and word count badges

### 7.3. Robust Backend Architecture

- Separation of concerns:
  - `chat/` handles web + API
  - `src/` encapsulates AI logic and prompts
- Multi-step LangChain chains:
  - Validator → Extractor → Corrector for NER
  - Dedicated chains for each task for clarity and maintainability
- Config-driven:
  - Centralized control of Groq model, temperature, and timeouts

### 7.4. Deployable & Extensible

- Ready to run on:
  - Local machine (Django dev server)
  - Dockerized environments
  - Hugging Face Spaces (public demo)
- Easy to extend:
  - Add more fields to NER (e.g., medications, allergies)
  - Plug in RAG (Retrieval-Augmented Generation) for guidelines
  - Integrate with EMR/clinical systems via APIs
