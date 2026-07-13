import os
import google.generativeai as genai

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash")


# ==========================================================
# Generate Interview Questions
# ==========================================================

def generate_questions(resume_text, job_description):

    prompt = f"""
You are an experienced technical interviewer.

Resume:
{resume_text}

Job Description:
{job_description}

Generate:

1. Five Technical Questions
2. Three HR Questions
3. Two Project-Based Questions

Instructions:
- Return ONLY the questions.
- Number each question.
- Do not provide answers.
"""

    response = model.generate_content(prompt)

    questions = []

    for line in response.text.split("\n"):

        line = line.strip()

        if not line:
            continue

        # Skip headings
        if "Technical Questions" in line:
            continue

        if "HR Questions" in line:
            continue

        if "Project-Based Questions" in line:
            continue

        if line[0].isdigit():
            questions.append(line)


    return questions


# ==========================================================
# Evaluate Candidate Answer
# ==========================================================

def evaluate_answer(question, answer):

    prompt = f"""
You are a Senior Technical Interviewer.

Interview Question:
{question}

Candidate Answer:
{answer}

Evaluate the answer.

Give your response in the following format ONLY.

# Score
Score: X/10

# Strengths
• Point 1
• Point 2

# Weaknesses
• Point 1
• Point 2

# Suggestions
• Point 1
• Point 2

# Ideal Answer
Write a perfect answer that would impress an interviewer.

Do NOT write anything outside this format.
"""

    from google.api_core.exceptions import ResourceExhausted

    try:
        response = model.generate_content(prompt)
        return response.text

    except ResourceExhausted:
        return """
    # Score
    Score: 0/10

    # Strengths
    Unable to evaluate.

    # Weaknesses
    The AI service has temporarily reached its usage limit.

    # Suggestions
    Please try again in a few minutes.

    # Ideal Answer
    Evaluation is temporarily unavailable because the AI service quota has been exceeded.
    """

    except Exception as e:
        return f"Error: {str(e)}"