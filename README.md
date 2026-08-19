# AI Interview Voice Agent

An AI-powered voice interview system built with **LiveKit Agents**, **Deepgram**, **Groq**, **MongoDB**, and **FastAPI**.

The system conducts technical interviews through real-time voice interaction. It collects candidate information, generates questions based on the candidate's role and experience, evaluates answers, asks follow-up questions when necessary, generates a final interview report, and stores the results in MongoDB.

---

## Features

- Real-time voice-based interviews
- Candidate name, role, and experience collection
- Experience-based interview difficulty
- AI-generated technical interview questions
- Prevention of repeated questions
- Candidate answer evaluation
- 1–10 answer scoring
- Follow-up questions for incomplete answers
- Question retry handling
- Interview progress tracking
- Final interview report generation
- MongoDB persistence
- FastAPI backend
- LiveKit Cloud deployment
- Docker-based production deployment
- Automatic interview session termination

---

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application |
| LiveKit Agents | Real-time voice agent |
| Deepgram | Speech-to-text and text-to-speech |
| Groq | LLM inference |
| Llama 3.3 70B | Question generation and answer evaluation |
| MongoDB | Interview and report storage |
| FastAPI | REST API backend |
| Pydantic | Data validation |
| Docker | Containerization |
| LiveKit Cloud | Agent deployment |
| uv | Python dependency management |

---

# Architecture

```text
                         ┌─────────────────────┐
                         │      Candidate      │
                         │      Voice Input    │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    LiveKit Cloud    │
                         │    Voice Session    │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    LiveKit Agent    │
                         │  livekit_worker.py  │
                         └──────────┬──────────┘
                                    │
                 ┌──────────────────┼──────────────────┐
                 │                  │                  │
                 ▼                  ▼                  ▼
          ┌────────────┐     ┌────────────┐     ┌────────────┐
          │  Deepgram  │     │    Groq    │     │  MongoDB   │
          │ STT / TTS  │     │ Llama 3.3  │     │  Database  │
          └────────────┘     └─────┬──────┘     └────────────┘
                                   │
                                   ▼
                         ┌─────────────────────┐
                         │  Interview Manager  │
                         │                     │
                         │  State Management   │
                         │  Questions          │
                         │  Answers            │
                         │  Retries            │
                         │  Scores             │
                         └─────────────────────┘

                         ┌─────────────────────┐
                         │       FastAPI       │
                         │    REST Backend     │
                         └─────────────────────┘
````

---

# Interview Flow

```text
Candidate joins
       │
       ▼
Ask candidate name
       │
       ▼
Ask target role
       │
       ▼
Ask experience
       │
       ▼
Determine experience level
       │
       ▼
Generate interview question
       │
       ▼
Candidate answers
       │
       ▼
Evaluate answer
       │
       ├─────────────── Strong answer
       │                       │
       │                       ▼
       │                 Next question
       │
       └─────────────── Incomplete / weak answer
                               │
                               ▼
                       Follow-up question
                               │
                               ▼
                       Evaluate response
                               │
                               ▼
                         Next question
                               │
                               ▼
                       Interview complete
                               │
                               ▼
                     Generate final report
                               │
                               ▼
                       Store in MongoDB
                               │
                               ▼
                     End interview session
```

---

# Experience Levels

The interview difficulty is adjusted according to the candidate's experience.

| Experience | Question Difficulty       |
| ---------- | ------------------------- |
| BEGINNER   | Very easy, basic concepts |
| JUNIOR     | Easy to medium            |
| MID        | Medium                    |
| SENIOR     | Medium to advanced        |

The interview focuses on conceptual questions.

The question generator avoids:

* Coding questions
* Mathematical questions
* System design questions
* Algorithm implementation questions
* Data structure implementation questions

---

# Answer Evaluation

Candidate answers are evaluated using the LLM.

The score is between **1 and 10**.

```text
1–3   Incorrect or irrelevant
4–5   Partially correct
6–7   Correct but basic
8–10  Strong answer
```

Each evaluation can contain:

* Score
* Strengths
* Weaknesses
* Improvements

Example:

```json
{
  "score": 8,
  "strengths": [
    "Correctly explained the core concept"
  ],
  "weaknesses": [],
  "improvements": [
    "Could provide a practical example"
  ]
}
```

---

# Follow-up Questions

If the candidate gives an incomplete or weak answer, the agent can ask a follow-up question instead of immediately moving to the next question.

Example:

```text
Agent:
What is machine learning?

Candidate:
It is related to computers learning.

Agent:
Could you explain how computers learn from data?
```

The system can retry a question a limited number of times before moving forward.

---

# Question Management

The interview manager maintains a list of previously asked questions.

This allows the question generator to avoid repeating questions during the same interview.

The interview manager also tracks:

* Current interview state
* Candidate name
* Candidate role
* Candidate experience
* Current question
* Question count
* Retry count
* Current answer
* Interview responses
* Evaluation results

---

# Project Structure

```text
ai-interview-agent/
│
├── .env.example
├── .gitignore
├── Dockerfile
├── livekit.toml
├── pyproject.toml
├── README.md
├── uv.lock
│
├── src/
│   │
│   ├── agent/
│   │   ├── __init__.py
│   │   └── livekit_worker.py
│   │
│   └── backend/
│       ├── __init__.py
│       │
│       ├── api/
│       │   ├── __init__.py
│       │   └── interview_routes.py
│       │
│       ├── models/
│       │   ├── __init__.py
│       │   └── interview.py
│       │
│       ├── schemas/
│       │   ├── __init__.py
│       │   └── interview_schema.py
│       │
│       ├── services/
│       │   ├── __init__.py
│       │   ├── interview_agent.py
│       │   ├── interview_manager.py
│       │   └── interviewer.py
│       │
│       └── db.py
│
└── tests/
```

---

# Core Components

## `livekit_worker.py`

The main LiveKit worker.

Responsible for:

* Connecting to LiveKit
* Starting the voice session
* Receiving candidate speech
* Sending audio responses
* Managing the interview flow
* Calling the interview services
* Ending the interview session

---

## `interview_manager.py`

Manages the interview state and candidate information.

Responsible for:

* Candidate name
* Candidate role
* Candidate experience
* Current question
* Question count
* Retry count
* Interview state
* Current answer
* Interview data

---

## `interviewer.py`

Contains the LLM-powered interview functionality.

Main functions include:

```python
generate_question()
generate_followup_question()
evaluate_answer()
generate_final_report()
```

---

## `db.py`

Handles the MongoDB connection and collections.

The application uses MongoDB to persist completed interview reports.

---

## `interview_routes.py`

Contains FastAPI endpoints for interacting with the interview backend.

---

## `interview_schema.py`

Contains Pydantic schemas used for validation and structured interview data.

---

# MongoDB

The application stores completed interview reports in MongoDB.

A report can contain:

* Candidate name
* Target role
* Experience level
* Interview questions
* Candidate answers
* Individual evaluations
* Scores
* Strengths
* Weaknesses
* Improvements
* Final recommendation
* Interview timestamp

Example document:

```json
{
  "candidate_name": "Candidate Name",
  "role": "AI Engineer",
  "experience": "JUNIOR",
  "interview_data": [
    {
      "question": "What is machine learning?",
      "answer": "Candidate response...",
      "evaluation": {
        "score": 8,
        "strengths": [
          "Correctly explained the basic concept"
        ],
        "weaknesses": [],
        "improvements": [
          "Could provide a practical example"
        ]
      }
    }
  ],
  "final_report": {
    "overall_score": 8,
    "strengths": [],
    "weaknesses": [],
    "improvements": [],
    "recommendation": "..."
  }
}
```

---

# Environment Variables

Create a `.env.local` file containing your credentials:

```env
LIVEKIT_URL=
LIVEKIT_API_KEY=
LIVEKIT_API_SECRET=

DEEPGRAM_API_KEY=

GROQ_API_KEY=

MONGO_URI=
```

A `.env.example` file should be committed to the repository without real credentials.

Example:

```env
LIVEKIT_URL=
LIVEKIT_API_KEY=
LIVEKIT_API_SECRET=

DEEPGRAM_API_KEY=

GROQ_API_KEY=

MONGO_URI=
```

### Security

Never commit:

```text
.env
.env.local
```

or any file containing API keys, passwords, or database credentials.

---

# Local Development

## 1. Clone the repository

```bash
git clone git@github.com:siya0066/ai-interview-voice-agent.git
```

Enter the project:

```bash
cd ai-interview-voice-agent
```

---

## 2. Install dependencies

This project uses `uv`.

Install dependencies:

```bash
uv sync
```

---

## 3. Configure environment variables

Create `.env.local`:

```bash
cp .env.example .env.local
```

Then add your:

* LiveKit credentials
* Deepgram API key
* Groq API key
* MongoDB URI

---

# Running the Voice Agent

For local development:

```bash
uv run python src/agent/livekit_worker.py dev
```

The worker will connect to LiveKit Cloud and wait for an interview session.

---

# Running the FastAPI Backend

Start the FastAPI server:

```bash
uv run uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

FastAPI Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

# LiveKit Cloud

The voice agent is deployed using LiveKit Cloud.

Authenticate the LiveKit CLI:

```bash
lk cloud auth
```

Check the configured project:

```bash
lk project list
```

Check the agent deployment:

```bash
lk agent status
```

View deployment logs:

```bash
lk agent logs
```

Deploy updated code:

```bash
lk agent deploy
```

The production deployment uses the project's:

```text
Dockerfile
livekit.toml
```

---

# Docker

The project includes a Dockerfile for production deployment.

Build the Docker image:

```bash
docker build -t ai-interview-agent .
```

Run the container:

```bash
docker run ai-interview-agent
```

For production deployment, configure the required environment variables through the deployment platform rather than committing secrets to the repository.

---

# Testing

The project contains a test suite under:

```text
tests/
```

Run the tests using:

```bash
uv run pytest
```

---

# API

The FastAPI backend provides endpoints for managing interviews and reports.

Current API structure:

```text
GET     /
GET     /health

POST    /interview/start

GET     /reports

GET     /reports/{candidate_name}

DELETE  /reports/{candidate_name}
```

Interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

---

# Interview Data

Each completed interview contains information about:

```text
Candidate
    ├── Name
    ├── Role
    └── Experience

Interview
    ├── Questions
    ├── Answers
    ├── Scores
    ├── Strengths
    ├── Weaknesses
    └── Improvements

Final Report
    ├── Overall Score
    ├── Strengths
    ├── Weaknesses
    ├── Improvements
    └── Recommendation
```

---

# Future Improvements

Potential future improvements include:

* Candidate authentication
* Recruiter authentication
* Interview scheduling
* Resume-based interviews
* Resume parsing
* Behavioral interviews
* HR interviews
* Role-specific evaluation criteria
* Candidate dashboard
* Recruiter dashboard
* Interview analytics
* Real-time transcription display
* Interview history
* Candidate comparison
* Advanced scoring
* Web frontend
* Interview scheduling
* Email notifications
* Multi-tenant organizations
* Role-based access control

---

# Development Roadmap

```text
[x] LiveKit voice agent setup
[x] LiveKit Cloud deployment
[x] Deepgram STT/TTS integration
[x] Groq LLM integration
[x] MongoDB integration
[ ] Interview state management
[ ] Dynamic question generation
[ ] Follow-up question handling
[ ] Answer evaluation
[ ] Final report generation
[ ] FastAPI interview APIs
[ ] Automatic session termination
[ ] Automated tests
[ ] Frontend
```

---

# Deployment

The application is designed to run as a LiveKit Agent in LiveKit Cloud.

The production deployment consists of:

```text
Git Repository
      │
      ▼
Docker Build
      │
      ▼
LiveKit Cloud
      │
      ▼
AI Interview Agent
      │
      ├── Deepgram
      ├── Groq
      └── MongoDB
```

---

# Security Considerations

The application handles candidate interview data and API credentials.

Important security practices include:

* Never commit API keys
* Never commit MongoDB credentials
* Keep `.env` and `.env.local` out of Git
* Validate API input with Pydantic
* Validate candidate data before storing it
* Restrict MongoDB network access
* Use HTTPS/WSS in production
* Implement authentication before exposing production APIs
* Implement authorization for interview reports
* Avoid exposing internal error details through APIs
* Use environment variables or a secret manager for production credentials

---

# License

This project is licensed under the MIT License.

```

**One correction before you commit this README:** your current repository is the LiveKit starter repository, and your actual files are currently under `src/`. The README above reflects that structure. If we later move `main.py` into `src/` or change the backend layout, we should update the tree and commands at that point rather than leaving the README lying about the architecture.
```
