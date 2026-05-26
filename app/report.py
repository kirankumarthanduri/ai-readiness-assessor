import anthropic
import os
import sys
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(__file__))

load_dotenv()

def calculate_scores(answers: dict) -> dict:
    """Calculate scores per dimension and overall."""

    dimension_scores = {
        "Data Readiness": [],
        "Technology Infrastructure": [],
        "Talent & Skills": [],
        "Leadership & Strategy": [],
        "Governance & Ethics": []
    }

    from questions import questions

    for q in questions:
        q_id = str(q["id"])
        if q_id in answers:
            score = answers[q_id] + 1
            dimension_scores[q["dimension"]].append(score)

    dimension_percentages = {}
    for dimension, scores in dimension_scores.items():
        if scores:
            avg = sum(scores) / len(scores)
            percentage = round((avg / 4) * 100)
            dimension_percentages[dimension] = percentage

    all_scores = [s for scores in dimension_scores.values() for s in scores]
    overall = round((sum(all_scores) / (len(all_scores) * 4)) * 100) if all_scores else 0

    return {
        "overall": overall,
        "dimensions": dimension_percentages
    }


def get_maturity_level(score: int) -> str:
    """Return maturity label based on overall score."""
    if score < 25:
        return "🔴 Beginner"
    elif score < 50:
        return "🟡 Developing"
    elif score < 75:
        return "🟠 Advanced"
    else:
        return "🟢 Leader"


def _build_questions_text() -> str:
    from questions import questions
    lines = []
    for q in questions:
        lines.append(f"[{q['dimension']}] Q{q['id']}: {q['question']}")
        for i, opt in enumerate(q["options"]):
            lines.append(f"  {i+1}. {opt}")
    return "\n".join(lines)


# Static system prompt — cached on first call, reused on subsequent calls
_SYSTEM_PROMPT = f"""You are an expert Enterprise AI Transformation Consultant.

You administer a 20-question AI Readiness Assessment across five dimensions:
- Data Readiness
- Technology Infrastructure
- Talent & Skills
- Leadership & Strategy
- Governance & Ethics

Each question has four options scored 1 (lowest) to 4 (highest). Here is the full question bank:

{_build_questions_text()}

When given an organization's assessment results, generate a professional Enterprise AI Readiness Report with exactly these sections:

1. EXECUTIVE SUMMARY
   - 3-4 sentences summarizing the organization's AI readiness position

2. DIMENSION ANALYSIS
   - For each of the 5 dimensions, provide:
     * Current state (1-2 sentences)
     * Key observation (1 sentence)

3. TOP 3 STRENGTHS
   - List the 3 strongest areas with brief explanation

4. TOP 3 CRITICAL GAPS
   - List the 3 most important gaps that need immediate attention

5. RECOMMENDED 90-DAY ACTION PLAN
   - Month 1: Quick wins (3 actions)
   - Month 2: Foundation building (3 actions)
   - Month 3: Acceleration (3 actions)

6. CLOSING RECOMMENDATION
   - 2-3 sentences with strategic advice for leadership

Keep the tone professional, executive-level, and actionable. Use clear headings for each section.
"""


def generate_report(answers: dict, org_name: str) -> tuple:
    """Send answers to Claude and get full AI Readiness Report."""

    scores = calculate_scores(answers)
    overall = scores["overall"]
    dimensions = scores["dimensions"]
    maturity = get_maturity_level(overall)

    dimension_summary = "\n".join([
        f"- {dim}: {score}/100"
        for dim, score in dimensions.items()
    ])

    from questions import questions
    answers_summary = ""
    for q in questions:
        q_id = str(q["id"])
        if q_id in answers:
            selected_option = q["options"][answers[q_id]]
            answers_summary += f"\n[{q['dimension']}] Q{q['id']}: {selected_option}"

    user_message = f"""Organization: {org_name}

Overall AI Readiness Score: {overall}/100
Maturity Level: {maturity}

Dimension Scores:
{dimension_summary}

Selected Answers:
{answers_summary}

Please generate the Enterprise AI Readiness Report for this organization."""

    client = anthropic.Anthropic(
        api_key=os.getenv("ANTHROPIC_API_KEY")
    )

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2000,
        system=[
            {
                "type": "text",
                "text": _SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"}
            }
        ],
        messages=[
            {
                "role": "user",
                "content": user_message
            }
        ]
    )

    return message.content[0].text, scores
