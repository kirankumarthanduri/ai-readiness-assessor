import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from questions import questions
from report import generate_report, get_maturity_level

# Page config
st.set_page_config(
    page_title="Enterprise AI Readiness Assessor",
    page_icon="🤖",
    layout="centered"
)

# Custom CSS
st.markdown("""
    <style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1a1a2e;
        text-align: center;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        font-size: 1rem;
        color: #555;
        text-align: center;
        margin-bottom: 2rem;
    }
    .dimension-header {
        font-size: 1.2rem;
        font-weight: 600;
        color: #16213e;
        background-color: #f0f4ff;
        padding: 0.5rem 1rem;
        border-left: 4px solid #4361ee;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    .score-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .report-box {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 2rem;
        margin-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)


def show_welcome():
    """Show welcome screen."""
    st.markdown('<div class="main-title">🤖 Enterprise AI Readiness Assessor</div>', 
                unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Assess your organization\'s readiness for AI transformation</div>', 
                unsafe_allow_html=True)

    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Questions", "20")
    with col2:
        st.metric("Dimensions", "5")
    with col3:
        st.metric("Time Required", "~5 mins")

    st.markdown("---")

    st.markdown("### 📋 What This Assessment Covers")
    st.markdown("""
    - 📊 **Data Readiness** — Data quality, governance, accessibility
    - 🏗️ **Technology Infrastructure** — Cloud, APIs, MLOps
    - 👥 **Talent & Skills** — AI literacy, expertise, training
    - 🎯 **Leadership & Strategy** — AI vision, budget, sponsorship
    - ⚖️ **Governance & Ethics** — Policies, compliance, responsible AI
    """)

    st.markdown("---")
    st.markdown("### 🏢 Tell Us About Your Organization")

    org_name = st.text_input(
        "Organization Name",
        placeholder="Enter your organization name..."
    )

    if st.button("🚀 Start Assessment", use_container_width=True):
        if org_name.strip() == "":
            st.error("Please enter your organization name to continue.")
        else:
            st.session_state.org_name = org_name
            st.session_state.page = "assessment"
            st.session_state.answers = {}
            st.rerun()


def show_assessment():
    """Show assessment questions."""
    st.markdown('<div class="main-title">🤖 AI Readiness Assessment</div>', 
                unsafe_allow_html=True)
    st.markdown(f'<div class="subtitle">Organization: {st.session_state.org_name}</div>', 
                unsafe_allow_html=True)

    # Progress
    answered = len(st.session_state.answers)
    progress = answered / len(questions)
    st.progress(progress)
    st.caption(f"Progress: {answered}/{len(questions)} questions answered")

    st.markdown("---")

    # Group questions by dimension
    dimensions = {}
    for q in questions:
        dim = q["dimension"]
        if dim not in dimensions:
            dimensions[dim] = []
        dimensions[dim].append(q)

    # Dimension icons
    icons = {
        "Data Readiness": "📊",
        "Technology Infrastructure": "🏗️",
        "Talent & Skills": "👥",
        "Leadership & Strategy": "🎯",
        "Governance & Ethics": "⚖️"
    }

    # Render questions
    for dimension, qs in dimensions.items():
        st.markdown(
            f'<div class="dimension-header">{icons.get(dimension, "📌")} {dimension}</div>',
            unsafe_allow_html=True
        )
        for q in qs:
            q_id = str(q["id"])
            current = st.session_state.answers.get(q_id, None)

            selected = st.radio(
                f"**Q{q['id']}.** {q['question']}",
                options=q["options"],
                index=current if current is not None else None,
                key=f"q_{q_id}"
            )

            if selected is not None:
                st.session_state.answers[q_id] = q["options"].index(selected)

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("⬅️ Back to Start", use_container_width=True):
            st.session_state.page = "welcome"
            st.rerun()

    with col2:
        answered_count = len(st.session_state.answers)
        if st.button(
            f"📊 Generate Report ({answered_count}/{len(questions)} answered)",
            use_container_width=True,
            disabled=answered_count < len(questions)
        ):
            st.session_state.page = "report"
            st.rerun()

    if answered_count < len(questions):
        st.warning(f"⚠️ Please answer all {len(questions)} questions to generate your report.")


def show_report():
    """Generate and show the AI Readiness Report."""
    st.markdown('<div class="main-title">📊 Your AI Readiness Report</div>', 
                unsafe_allow_html=True)
    st.markdown(f'<div class="subtitle">Organization: {st.session_state.org_name}</div>', 
                unsafe_allow_html=True)

    with st.spinner("🤖 Claude is analyzing your responses and generating your report..."):
        report_text, scores = generate_report(
            st.session_state.answers,
            st.session_state.org_name
        )

    overall = scores["overall"]
    maturity = get_maturity_level(overall)
    dimensions = scores["dimensions"]

    st.markdown("---")

    # Overall score
    st.markdown("### 🎯 Overall AI Readiness Score")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Overall Score", f"{overall}/100")
    with col2:
        st.metric("Maturity Level", maturity)

    st.progress(overall / 100)

    st.markdown("---")

    # Dimension scores
    st.markdown("### 📊 Dimension Breakdown")
    cols = st.columns(len(dimensions))
    icons = {
        "Data Readiness": "📊",
        "Technology Infrastructure": "🏗️",
        "Talent & Skills": "👥",
        "Leadership & Strategy": "🎯",
        "Governance & Ethics": "⚖️"
    }

    for i, (dim, score) in enumerate(dimensions.items()):
        with cols[i]:
            st.metric(
                f"{icons.get(dim, '📌')} {dim.split()[0]}",
                f"{score}%"
            )
            st.progress(score / 100)

    st.markdown("---")

    # Full report
    st.markdown("### 📋 Full Assessment Report")
    st.markdown(
        f'<div class="report-box">{report_text.replace(chr(10), "<br>")}</div>',
        unsafe_allow_html=True
    )

    st.markdown("---")

    # Download report
    download_content = f"""
ENTERPRISE AI READINESS REPORT
Organization: {st.session_state.org_name}

OVERALL SCORE: {overall}/100
MATURITY LEVEL: {maturity}

DIMENSION SCORES:
{chr(10).join([f"- {dim}: {score}/100" for dim, score in dimensions.items()])}

---

{report_text}
"""

    st.download_button(
        label="⬇️ Download Report as TXT",
        data=download_content,
        file_name=f"AI_Readiness_Report_{st.session_state.org_name}.txt",
        mime="text/plain",
        use_container_width=True
    )

    if st.button("🔄 Start New Assessment", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()


# App router
def main():
    if "page" not in st.session_state:
        st.session_state.page = "welcome"

    if st.session_state.page == "welcome":
        show_welcome()
    elif st.session_state.page == "assessment":
        show_assessment()
    elif st.session_state.page == "report":
        show_report()


if __name__ == "__main__":
    main()