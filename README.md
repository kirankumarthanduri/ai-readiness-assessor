# Enterprise AI Readiness Assessor

A Streamlit web app that evaluates an organization's readiness for AI transformation across 5 key dimensions and generates a professional executive report using Claude AI.
https://avgs928mfw4qfc5w9pqjmp.streamlit.app/
<img width="1193" height="805" alt="image" src="https://github.com/user-attachments/assets/c44d762a-4b25-43bf-b62d-e632014c0632" />

## Demo

Answer 20 questions → get scored across 5 dimensions → receive a Claude-generated AI readiness report with a 90-day action plan.

## Features

- 20-question assessment across 5 AI readiness dimensions
- Real-time progress tracking
- Automated scoring with maturity level classification
- AI-generated executive report via Claude claude-sonnet-4-5
- Downloadable TXT report

## Assessment Dimensions

| Dimension | What It Covers |
|---|---|
| Data Readiness | Data quality, governance, accessibility, privacy |
| Technology Infrastructure | Cloud adoption, APIs, MLOps, scalability |
| Talent & Skills | AI literacy, dedicated talent, training programs |
| Leadership & Strategy | AI strategy, executive sponsorship, budget alignment |
| Governance & Ethics | AI governance, bias handling, risk management |

## Maturity Levels

| Score | Level |
|---|---|
| 0–24 | Beginner |
| 25–49 | Developing |
| 50–74 | Advanced |
| 75–100 | Leader |

## Project Structure

```
ai-readiness-assessor/
├── app/
│   ├── main.py          # Streamlit UI and page router
│   ├── questions.py     # 20 assessment questions
│   └── report.py        # Scoring logic + Claude API report generation
├── requirements.txt
├── .env                 # Not committed — add your API key here
└── .gitignore
```

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/your-username/ai-readiness-assessor.git
cd ai-readiness-assessor
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Add your Anthropic API key**

Create a `.env` file in the project root:
```
ANTHROPIC_API_KEY=your_api_key_here
```

Get your API key at [console.anthropic.com](https://console.anthropic.com).

**4. Run the app**
```bash
streamlit run app/main.py
```

The app opens at `http://localhost:8501`.

## How It Works

1. User enters their organization name on the welcome screen
2. Answers 20 radio-button questions grouped by dimension
3. On submission, scores are calculated locally (each option scores 1–4)
4. Scores + all answers are sent to Claude claude-sonnet-4-5 via the Anthropic SDK
5. Claude returns a structured executive report covering strengths, gaps, and a 90-day action plan
6. User can view scores, read the report, and download it as a `.txt` file

## Requirements

- Python 3.8+
- Anthropic API key
- `streamlit`, `anthropic`, `python-dotenv`
