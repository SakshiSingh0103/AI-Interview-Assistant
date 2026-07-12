from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.colors import darkblue

def generate_pdf(scores, feedbacks):
    
    print("REPORTLAB PDF IS RUNNING")

    doc = SimpleDocTemplate("Interview_Report.pdf")

    styles = getSampleStyleSheet()

    title_style = styles["Heading1"]
    title_style.alignment = TA_CENTER
    title_style.textColor = darkblue

    heading_style = styles["Heading2"]

    normal_style = styles["BodyText"]

    story = []
    # ============================
    # Title
    # ============================
    story.append(
        Paragraph("AI Interview Report", title_style)
    )

    story.append(Spacer(1, 20))
    # ============================
    # Average Score
    # ============================
    average = (
        sum(scores.values()) / len(scores)
        if scores
        else 0
    )
    story.append(
        Paragraph(
            f"<b>Average Score:</b> {average:.1f}/10",
            heading_style,
        )
    )
    story.append(Spacer(1, 20))
    # ============================
    # Feedback
    # ============================
    for question in scores:

        story.append(
            Paragraph(
                f"<b>Question {question+1}</b>",
                heading_style,
            )
        )

        feedback = feedbacks.get(question, "")
        # Replace unsupported symbols
        feedback = (
            feedback
            .replace("•", "-")
            .replace("✅", "")
            .replace("⭐", "")
            .replace("➡", "->")
            .replace("📌", "")
            .replace("📊", "")
            .replace("🎯", "")
            .replace("\n", "<br/>")
        )

        story.append(
            Paragraph(
                feedback,
                normal_style,
            )
        )

        story.append(Spacer(1, 15))

    doc.build(story)