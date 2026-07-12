import pandas as pd
import streamlit as st
import re

from resume_parser import extract_resume_text
from interview_ai import generate_questions, evaluate_answer
from pdf_generator import generate_pdf

# =====================================================
# Page Configuration
# =====================================================

st.set_page_config(
    page_title="AI Interview Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================================================
# Custom CSS
# ======================================================

st.markdown("""
<style>

/* Background */
.stApp{
    background-color:#F6F8FC;
}

/* Main title */
h1{
    color:#1F3C88;
    text-align:center;
}

/* Section headings */
h2,h3{
    color:#163172;
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background:#EAF2FF;
}

/* Buttons */
.stButton>button{
    width:100%;
    background:#2563EB;
    color:white;
    border-radius:10px;
    border:none;
    height:45px;
    font-size:17px;
    font-weight:bold;
}

.stButton>button:hover{
    background:#1D4ED8;
}

/* Text Area */
textarea{
    border-radius:12px !important;
}

/* Metric Cards */
div[data-testid="metric-container"]{
    background:white;
    padding:15px;
    border-radius:12px;
    box-shadow:0px 3px 8px rgba(0,0,0,.10);
    text-align:center;
}

/* Progress Bar */
.stProgress>div>div>div{
    background:#2563EB;
}

</style>
""", unsafe_allow_html=True)



# =====================================================
# Session State
# =====================================================

if "questions" not in st.session_state:
    st.session_state.questions = []

if "current_question" not in st.session_state:
    st.session_state.current_question = 0

if "interview_started" not in st.session_state:
    st.session_state.interview_started = False

if "interview_completed" not in st.session_state:
    st.session_state.interview_completed = False

if "feedback" not in st.session_state:
    st.session_state.feedback = ""

# Store candidate answers
if "answers" not in st.session_state:
    st.session_state.answers = {}

# Store AI feedback
if "feedbacks" not in st.session_state:
    st.session_state.feedbacks = {}

# Store question scores
if "scores" not in st.session_state:
    st.session_state.scores = {}

# Resume text
if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

# Job description
if "job_description" not in st.session_state:
    st.session_state.job_description = ""

# =====================================================
# Title
# =====================================================
st.title("🤖 AI Interview Assistant")

st.caption(
    "Practice AI-powered interviews with your Resume and Job Description."
)

# =====================================================
# Dashboard Cards
# =====================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "📄 Resume",
        "Ready" if st.session_state.resume_text else "Pending"
    )

with col2:
    st.metric(
        "💼 Job Description",
        "Ready" if st.session_state.job_description else "Pending"
    )

with col3:
    status = (
        "Started"
        if st.session_state.interview_started
        else "Not Started"
    )

    st.metric(
        "🎯 Interview",
        status
    )

st.divider()


# =====================================================
# Sidebar
# =====================================================

with st.sidebar:

    st.header("📌 About")

    st.markdown("""
### This application allows you to:

✅ Upload Resume

✅ Paste Job Description

✅ Generate AI Interview Questions

✅ Evaluate Answers

✅ View Interview Statistics

✅ Get Hiring Recommendation

✅ Download Interview Report
""")

    st.divider()

    st.header("📊 Interview Status")

    if st.session_state.interview_started:

        st.success("Interview Started")

        st.write(
            f"Current Question: "
            f"{st.session_state.current_question + 1}"
        )

    else:

        st.info("Waiting to start interview...")
# =====================================================
# Resume Upload
# =====================================================

st.header("📄 Upload Resume")

uploaded_resume = st.file_uploader(
    "Choose your Resume (PDF)",
    type=["pdf"]
)

# =====================================================
# Job Description
# =====================================================

st.header("💼 Job Description")

job_description = st.text_area(
    "Paste the Job Description here",
    height=220,
    placeholder="Paste the complete job description..."
)

st.divider()

# =====================================================
# Generate Questions
# =====================================================

generate = st.button(
    "🚀 Generate Interview Questions",
    use_container_width=True
)

if generate:

    # Validation
    if uploaded_resume is None:
        st.error("⚠ Please upload your resume.")
        st.stop()

    if job_description.strip() == "":
        st.error("⚠ Please paste the Job Description.")
        st.stop()

    # Resume Parsing
    with st.spinner("📄 Reading Resume..."):

        resume_text = extract_resume_text(uploaded_resume)
        st.write("Resume Text:")
        st.write(resume_text)

    st.session_state.resume_text = resume_text
    st.session_state.job_description = job_description

    # Generate Questions
    with st.spinner("🤖 Generating Interview Questions..."):

        questions = generate_questions(
            resume_text,
            job_description
        )

    # Save Session Data
    st.session_state.questions = questions
    st.session_state.current_question = 0
    st.session_state.interview_started = True

    # Reset Previous Interview Data
    st.session_state.feedback = ""
    st.session_state.answers = {}
    st.session_state.feedbacks = {}
    st.session_state.scores = {}

    st.success("✅ Interview Questions Generated Successfully!")

    st.rerun()
# =====================================================
# Interview Screen
# =====================================================

if st.session_state.interview_started:

    questions = st.session_state.questions

    if len(questions) == 0:
        st.error("No questions generated.")
        st.stop()

    current_index = st.session_state.current_question

    # Safety Check
    if current_index >= len(questions):
        current_index = len(questions) - 1
        st.session_state.current_question = current_index

    current_question = questions[current_index]

    total_questions = len(questions)

    st.divider()

    # ==========================================
    # Progress
    # ==========================================

    st.subheader("📈 Interview Progress")

    progress = (current_index + 1) / total_questions

    st.progress(progress)

    st.write(
        f"### Question {current_index + 1} of {total_questions}"
    )
    remaining = total_questions - current_index - 1

    st.info(
        f"📌 Remaining Questions: {remaining}"
    )
# =====================================================
# Live Interview Dashboard
# =====================================================

    col1, col2, col3 = st.columns(3)

    # Card 1
    with col1:
        st.metric(
            "📍 Current Question",
            f"{current_index + 1}/{total_questions}"
        )

    # Card 2
    with col2:
        st.metric(
            "✅ Answered",
            len(st.session_state.answers)
        )

    # Card 3
    with col3:
        if st.session_state.scores:

            avg_score = (
                sum(st.session_state.scores.values())
                / len(st.session_state.scores)
            )

        else:
            avg_score = 0

        st.metric(
            "⭐ Average Score",
            f"{avg_score:.1f}/10"
        )

    st.divider()

    # ==========================================
    # Current Question
    # ==========================================

    st.subheader("🎤 Current Question")

    st.info(current_question)

    # ==========================================
    # Answer Box
    # ==========================================

    previous_answer = st.session_state.answers.get(current_index, "")

    answer = st.text_area(
        "✍️ Your Answer",
        value=previous_answer,
        height=220,
        key=f"answer_{current_index}"
    )

    # ==========================================
    # Submit Answer
    # ==========================================

    if st.button(
        "✅ Submit Answer",
        key=f"submit_{current_index}"
    ):

        if answer.strip() == "":

            st.warning("Please write your answer.")

        else:

            with st.spinner("🤖 AI is evaluating your answer..."):

                feedback = evaluate_answer(
                    current_question,
                    answer
                )

            # Save Answer
            st.session_state.answers[current_index] = answer

            # Save Feedback
            st.session_state.feedbacks[current_index] = feedback

            # Current Feedback
            st.session_state.feedback = feedback

            # Extract Score
            match = re.search(
                r"Score:\s*(\d+(\.\d+)?)/10",
                feedback
            )

            if match:
                score = float(match.group(1))
            else:
                score = 0

            st.session_state.scores[current_index] = score

            st.rerun()
# ======================================================
# Show AI Feedback
# ======================================================

if (
    st.session_state.interview_started
    and current_index in st.session_state.feedbacks
):

    st.divider()

    st.subheader("📊 AI Evaluation")

    feedback = st.session_state.feedbacks[current_index]
    score = st.session_state.scores.get(current_index, 0)

    # ==============================
    # Score
    # ==============================
    st.markdown(
        f"""
        <h1 style='text-align:center;'>Score</h1>
        <h2 style='text-align:center;color:#2563EB;font-size:48px;'>
            {score}/10
        </h2>
        """,
        unsafe_allow_html=True
    )
    # Remove score section
    feedback = re.sub(
        r"# Score\s*Score:\s*\d+(?:\.\d+)?/10",
        "",
        feedback,
        flags=re.IGNORECASE
    )

    # Split by markdown headings
    parts = re.split(
        r"# (Strengths|Weaknesses|Suggestions|Ideal Answer)",
        feedback
    )

    data = {}

    for i in range(1, len(parts), 2):
        heading = parts[i].strip()
        content = parts[i + 1].strip()
        data[heading] = content


    # ==============================
    # Strengths
    # ==============================
    if "Strengths" in data:
        st.success("### ✅ Strengths")
        st.markdown(data["Strengths"])

    # ==============================
    # Weaknesses
    # ==============================
    if "Weaknesses" in data:
        st.error("### ❌ Weaknesses")
        st.markdown(data["Weaknesses"])

    # ==============================
    # Suggestions
    # ==============================
    if "Suggestions" in data:
        st.warning("### 💡 Suggestions")
        st.markdown(data["Suggestions"])

    # ==============================
    # Ideal Answer
    # ==============================
    if "Ideal Answer" in data:
        st.info("### 📝 Ideal Answer")
        st.markdown(data["Ideal Answer"])
# =====================================================
# Statistics
# =====================================================

if st.session_state.interview_started:

    st.divider()

    answered = len(st.session_state.answers)

    total = len(st.session_state.questions)

    scores = list(st.session_state.scores.values())

    average = sum(scores) / len(scores) if scores else 0

    highest = max(scores) if scores else 0

    col1, col2, col3 = st.columns(3)

    col1.metric("Questions Answered", answered)

    col2.metric("Average Score", f"{average:.1f}/10")

    col3.metric("Highest Score", f"{highest:.1f}/10")
# =====================================================
# Navigation
# =====================================================

if st.session_state.interview_started:

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "⬅ Previous",
            disabled=st.session_state.current_question == 0,
            key="previous_button"
        ):

            st.session_state.current_question -= 1
            st.rerun()

    with col2:

        if st.button(
            "Next ➡",
            key="next_button"
        ):

            if st.session_state.current_question < len(st.session_state.questions)-1:

                st.session_state.current_question += 1

                st.rerun()

            else:

                st.session_state.interview_started = False

                st.session_state.interview_completed = True

                st.rerun()
# =====================================================
# Final Summary & Dashboard
# =====================================================

if st.session_state.interview_completed:

    st.balloons()

    st.header("🎉 Interview Completed")

    scores = list(st.session_state.scores.values())

    total = len(st.session_state.questions)
    answered = len(st.session_state.answers)

    average = sum(scores) / len(scores) if scores else 0
    highest = max(scores) if scores else 0
    lowest = min(scores) if scores else 0

    progress = answered / total if total > 0 else 0

    # ==============================
    # Hiring Recommendation
    # ==============================

    if average >= 8:

        recommendation = "Highly Recommended"
        grade = "A"

        st.success("⭐⭐⭐⭐⭐ Excellent Performance")

    elif average >= 6:

        recommendation = "Recommended"
        grade = "B"

        st.info("⭐⭐⭐⭐ Good Performance")

    else:

        recommendation = "Needs More Practice"
        grade = "C"

        st.warning("⭐⭐ Needs Improvement")

    st.subheader("🤖 AI Hiring Recommendation")

    st.success(recommendation)

    st.divider()

    # ==============================
    # Interview Summary
    # ==============================

    st.header("🏆 Interview Summary")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "⭐ Average Score",
            f"{average:.1f}/10"
        )

    with col2:
        st.metric(
            "🔥 Highest Score",
            f"{highest:.1f}/10"
        )

    with col3:
        st.metric(
            "📉 Lowest Score",
            f"{lowest:.1f}/10"
        )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Questions Answered",
            f"{answered}/{total}"
        )

    with col2:

        st.metric(
            "Grade",
            grade
        )

        st.progress(progress)
    # =====================================================
    # Performance Analytics
    # =====================================================

    st.divider()

    st.header("📈 Performance Analytics")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "⭐ Average",
            f"{average:.1f}/10"
        )

    with col2:
        st.metric(
            "🔥 Highest",
            f"{highest:.1f}/10"
        )

    with col3:
        st.metric(
            "📉 Lowest",
            f"{lowest:.1f}/10"
        )

    # -----------------------------------------
    # Question-wise Score Chart
    # -----------------------------------------

    if st.session_state.scores:

        chart_data = pd.DataFrame({

            "Question": [
                f"Q{i+1}"
                for i in st.session_state.scores.keys()
            ],

            "Score": list(
                st.session_state.scores.values()
            )

        })

        st.subheader("📊 Question-wise Scores")

        st.bar_chart(
            chart_data.set_index("Question")
        )

        st.subheader("📈 Score Trend")

        st.line_chart(
            chart_data.set_index("Question")
        )

        # =========================================
        # Performance Insights
        # =========================================

        best_question = max(
            st.session_state.scores,
            key=st.session_state.scores.get
        )

        worst_question = min(
            st.session_state.scores,
            key=st.session_state.scores.get
        )

        col1, col2 = st.columns(2)

        with col1:

            st.success(
                f"""
🏅 Best Performance

Question {best_question + 1}

Score: {st.session_state.scores[best_question]}/10
"""
            )

        with col2:

            st.warning(
                f"""
📉 Needs Improvement

Question {worst_question + 1}

Score: {st.session_state.scores[worst_question]}/10
"""
            )

    # =========================================
    # Interview Statistics
    # =========================================

    st.divider()

    st.subheader("📋 Interview Statistics")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Questions",
            total
        )

    with col2:
        st.metric(
            "Answered",
            answered
        )

    with col3:
        st.metric(
            "Completion",
            f"{progress*100:.0f}%"
        )

    # =========================================
    # Overall Performance
    # =========================================

    st.subheader("🎯 Overall Performance")

    if average >= 9:

        st.success("🌟 Outstanding Performance")

    elif average >= 8:

        st.success("🚀 Excellent Performance")

    elif average >= 7:

        st.info("👍 Good Performance")

    elif average >= 6:

        st.warning("📘 Fair Performance")

    else:

        st.error("📚 Needs More Practice")
    # =========================================
    # Congratulations
    # =========================================

    if average >= 8:

        st.balloons()

        st.success(
            """
🎉 Congratulations!

You performed exceptionally well in this interview.

Keep practicing and you're ready for real interviews!
"""
        )

    # =========================================
    # Download PDF
    # =========================================

    st.divider()

    st.subheader("📄 Download Interview Report")

    if st.button(
        "📄 Generate PDF Report",
        key="generate_pdf"
    ):

        generate_pdf(
            st.session_state.scores,
            st.session_state.feedbacks
        )

        with open(
            "Interview_Report.pdf",
            "rb"
        ) as pdf:

            st.download_button(
                "⬇ Download Report",
                pdf,
                file_name="Interview_Report.pdf",
                mime="application/pdf",
                key="download_pdf"
            )

    # =========================================
    # Restart Interview
    # =========================================

    st.divider()

    if st.button(
        "🔄 Restart Interview",
        key="restart_interview"
    ):

        st.session_state.questions = []

        st.session_state.answers = {}

        st.session_state.feedbacks = {}

        st.session_state.scores = {}

        st.session_state.feedback = ""

        st.session_state.current_question = 0

        st.session_state.interview_started = False

        st.session_state.interview_completed = False

        st.session_state.resume_text = ""

        st.session_state.job_description = ""

        st.rerun()
