"""Generate Resume and Cover Letter PDFs using reportlab."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from pathlib import Path

OUT_DIR = Path(__file__).parent

# ── Colour palette ────────────────────────────────────────────────────────────
NAVY   = colors.HexColor("#1B2A4A")
ACCENT = colors.HexColor("#2E6DA4")
LIGHT  = colors.HexColor("#F4F6F9")
GRAY   = colors.HexColor("#555555")
BLACK  = colors.HexColor("#1A1A1A")


def base_styles():
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle("NameStyle",
        fontSize=22, textColor=NAVY, fontName="Helvetica-Bold",
        spaceAfter=2, alignment=TA_CENTER))

    styles.add(ParagraphStyle("ContactStyle",
        fontSize=9, textColor=GRAY, fontName="Helvetica",
        spaceAfter=6, alignment=TA_CENTER))

    styles.add(ParagraphStyle("SectionHeader",
        fontSize=10, textColor=ACCENT, fontName="Helvetica-Bold",
        spaceBefore=10, spaceAfter=3, alignment=TA_LEFT,
        textTransform="uppercase", letterSpacing=1))

    styles.add(ParagraphStyle("JobTitle",
        fontSize=10, textColor=NAVY, fontName="Helvetica-Bold",
        spaceBefore=6, spaceAfter=1))

    styles.add(ParagraphStyle("SubLine",
        fontSize=9, textColor=GRAY, fontName="Helvetica-Oblique",
        spaceAfter=3))

    styles.add(ParagraphStyle("BulletItem",
        fontSize=9, textColor=BLACK, fontName="Helvetica",
        leftIndent=12, spaceAfter=2, bulletIndent=0,
        leading=13))

    styles.add(ParagraphStyle("BodyText2",
        fontSize=9.5, textColor=BLACK, fontName="Helvetica",
        spaceAfter=6, leading=14, alignment=TA_JUSTIFY))

    styles.add(ParagraphStyle("ProjectTitle",
        fontSize=9.5, textColor=NAVY, fontName="Helvetica-Bold",
        spaceBefore=4, spaceAfter=2))

    styles.add(ParagraphStyle("ProjectBody",
        fontSize=9, textColor=BLACK, fontName="Helvetica",
        spaceAfter=4, leading=13))

    styles.add(ParagraphStyle("SkillLabel",
        fontSize=9, textColor=NAVY, fontName="Helvetica-Bold"))

    styles.add(ParagraphStyle("SkillValue",
        fontSize=9, textColor=BLACK, fontName="Helvetica"))

    styles.add(ParagraphStyle("CLName",
        fontSize=14, textColor=NAVY, fontName="Helvetica-Bold",
        spaceAfter=2))

    styles.add(ParagraphStyle("CLContact",
        fontSize=9.5, textColor=GRAY, fontName="Helvetica",
        spaceAfter=4))

    styles.add(ParagraphStyle("CLDate",
        fontSize=9.5, textColor=BLACK, fontName="Helvetica",
        spaceAfter=2))

    styles.add(ParagraphStyle("CLAddressee",
        fontSize=9.5, textColor=BLACK, fontName="Helvetica",
        spaceAfter=10))

    styles.add(ParagraphStyle("CLBody",
        fontSize=10, textColor=BLACK, fontName="Helvetica",
        spaceAfter=10, leading=15, alignment=TA_JUSTIFY))

    styles.add(ParagraphStyle("CLSign",
        fontSize=10, textColor=NAVY, fontName="Helvetica-Bold",
        spaceAfter=2))

    return styles


def divider(color=ACCENT, thickness=0.8):
    return HRFlowable(width="100%", thickness=thickness,
                      color=color, spaceAfter=4, spaceBefore=2)


# ── RESUME ────────────────────────────────────────────────────────────────────

def build_resume():
    path = OUT_DIR / "Sunday_Igbone_Resume.pdf"
    doc = SimpleDocTemplate(
        str(path), pagesize=A4,
        leftMargin=1.8*cm, rightMargin=1.8*cm,
        topMargin=1.6*cm, bottomMargin=1.6*cm
    )
    s = base_styles()
    story = []

    # ── Header ──
    story.append(Paragraph("SUNDAY MONDAY IGBONE", s["NameStyle"]))
    story.append(Paragraph(
        "otachesunday226@gmail.com &nbsp;|&nbsp; Edinburgh, UK", s["ContactStyle"]))
    story.append(divider(NAVY, 1.2))

    # ── Education ──
    story.append(Paragraph("Education", s["SectionHeader"]))
    story.append(divider())

    story.append(Paragraph(
        "Master of Science &mdash; Applied Mathematical Sciences", s["JobTitle"]))
    story.append(Paragraph("Heriot-Watt University &nbsp;|&nbsp; 2024 &ndash; 2026", s["SubLine"]))
    for b in [
        "Thesis: <i>Learning Dynamical Systems from Data using SINDy (Sparse Identification of Nonlinear Dynamics)</i>",
        "Relevant coursework: Machine Learning, Statistical Modelling, Numerical Methods, Data-Driven Modelling",
    ]:
        story.append(Paragraph(f"&bull; &nbsp;{b}", s["BulletItem"]))

    story.append(Spacer(1, 4))
    story.append(Paragraph("Bachelor of Science &mdash; Mathematics", s["JobTitle"]))
    story.append(Paragraph("Taraba State University &nbsp;|&nbsp; 2017 &ndash; 2021", s["SubLine"]))

    # ── Experience ──
    story.append(Spacer(1, 4))
    story.append(Paragraph("Experience", s["SectionHeader"]))
    story.append(divider())

    exp = [
        {
            "title": "Data Science Intern",
            "org": "Amdari",
            "date": "Jan 2026 &ndash; Present",
            "bullets": [
                "<b>Fraud Detection:</b> Achieved ROC-AUC of <b>0.982</b> and <b>96% accuracy</b> on 10,836 digital money transfer transactions by building and comparing four fraud classification models (Logistic Regression, Random Forest, XGBoost, LightGBM), using time-based train/test splitting to prevent data leakage.",
                "<b>Churn Prediction:</b> Reduced customer churn identification time across 10,000 customers by building an end-to-end ML pipeline trained on 200,000+ ride-hailing records, engineering 23 behavioural features across trips, sessions, and rider profiles.",
                "<b>Production Deployment:</b> Eliminated manual reporting by deploying a real-time scoring REST API (FastAPI) and interactive analytics dashboard (Streamlit + Plotly), enabling live customer risk assessment for business stakeholders.",
            ]
        },
        {
            "title": "Artificial Intelligence Intern",
            "org": "Pantech AI",
            "date": "Nov 2024 &ndash; Present",
            "bullets": [
                "Improved model iteration speed by training, evaluating, and testing deep learning models in Python (Scikit-learn, NumPy, Pandas) across multiple client AI projects, contributing to production-ready solutions.",
                "Strengthened data pipeline reliability by implementing structured data wrangling and pre-processing workflows, reducing preparation time across concurrent project tracks.",
                "Supported client communication by documenting research findings and presenting model results clearly in regular cross-functional stand-ups and planning sessions.",
            ]
        },
        {
            "title": "Mathematics Teacher &amp; Administrative Assistant",
            "org": "Solid Foundation Tutors",
            "date": "Jul 2023",
            "bullets": [
                "Improved student mathematics attainment by designing structured, individualised learning programmes, producing measurable grade improvements across tutored cohorts.",
            ]
        },
    ]

    for e in exp:
        story.append(Paragraph(
            f"{e['title']} &nbsp;&mdash;&nbsp; {e['org']} &nbsp;|&nbsp; {e['date']}",
            s["JobTitle"]))
        for b in e["bullets"]:
            story.append(Paragraph(f"&bull; &nbsp;{b}", s["BulletItem"]))
        story.append(Spacer(1, 2))

    # ── Research ──
    story.append(Paragraph("Research", s["SectionHeader"]))
    story.append(divider())

    story.append(Paragraph(
        "MSc Thesis: Learning Dynamical Systems from Data using SINDy", s["JobTitle"]))
    story.append(Paragraph("Heriot-Watt University &nbsp;|&nbsp; 2025 &ndash; 2026", s["SubLine"]))
    for b in [
        "Applying sparse regression techniques (SINDy framework) to identify governing equations of dynamical systems directly from time-series data, without prior knowledge of system structure.",
        "Implemented and benchmarked SINDy models in Python against classical numerical methods, evaluating robustness under noise and limited data regimes.",
        "Relevant to signal processing, Bayesian inference, and data-driven scientific modelling.",
    ]:
        story.append(Paragraph(f"&bull; &nbsp;{b}", s["BulletItem"]))

    # ── Projects ──
    story.append(Spacer(1, 4))
    story.append(Paragraph("Projects", s["SectionHeader"]))
    story.append(divider())

    story.append(Paragraph(
        "Fraudulent Transaction Detection &mdash; NovaPay Digital Payments &nbsp;|&nbsp; Amdari, 2026",
        s["ProjectTitle"]))
    story.append(Paragraph(
        "Trained and compared 4 fraud classifiers on 10,836 transactions (9.1% fraud rate). "
        "Applied time-based splitting to prevent leakage. Best model achieved <b>ROC-AUC = 0.982, PR-AUC = 0.969</b>; "
        "Random Forest hit <b>97% fraud precision</b> at 98% overall accuracy. "
        "Features: IP risk scores, device trust, transaction velocity, corridor risk, KYC tier.",
        s["ProjectBody"]))

    story.append(Paragraph(
        "Customer Churn Prediction &amp; Analytics System &nbsp;|&nbsp; Amdari, 2026",
        s["ProjectTitle"]))
    story.append(Paragraph(
        "End-to-end pipeline: 23-feature engineering, 3 classifiers, K-Means segmentation, "
        "FastAPI scoring API, Streamlit dashboard, drift monitoring &mdash; applied to 200K+ ride-hailing records.",
        s["ProjectBody"]))

    # ── Skills ──
    story.append(Paragraph("Skills", s["SectionHeader"]))
    story.append(divider())

    skill_data = [
        ["Languages", "Python (advanced), SQL"],
        ["ML / AI", "Scikit-learn, XGBoost, LightGBM, Random Forest, Logistic Regression"],
        ["Mathematical Methods", "Sparse regression (SINDy), dynamical systems, Bayesian statistics, numerical methods"],
        ["Deployment", "FastAPI, Streamlit, Plotly"],
        ["Dev Tools", "Git, Jupyter, VS Code"],
    ]

    for label, value in skill_data:
        row_data = [[
            Paragraph(f"<b>{label}</b>", s["SkillLabel"]),
            Paragraph(value, s["SkillValue"]),
        ]]
        t = Table(row_data, colWidths=[4.5*cm, 13*cm])
        t.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ("TOPPADDING", (0, 0), (-1, -1), 2),
        ]))
        story.append(t)

    doc.build(story)
    print(f"Resume saved: {path}")


# ── COVER LETTER ──────────────────────────────────────────────────────────────

def build_cover_letter():
    path = OUT_DIR / "Sunday_Igbone_CoverLetter_CambridgeConsultants.pdf"
    doc = SimpleDocTemplate(
        str(path), pagesize=A4,
        leftMargin=2.2*cm, rightMargin=2.2*cm,
        topMargin=2*cm, bottomMargin=2*cm
    )
    s = base_styles()
    story = []

    # ── Sender header ──
    story.append(Paragraph("Sunday Monday Igbone", s["CLName"]))
    story.append(Paragraph(
        "otachesunday226@gmail.com &nbsp;|&nbsp; Edinburgh, UK", s["CLContact"]))
    story.append(divider(NAVY, 0.8))
    story.append(Spacer(1, 6))

    story.append(Paragraph("30 June 2026", s["CLDate"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "Hiring Team &mdash; AI &amp; Algorithms<br/>"
        "Cambridge Consultants<br/>"
        "Cambridge, UK",
        s["CLAddressee"]))

    story.append(Paragraph("Dear Hiring Team,", s["CLBody"]))

    paragraphs = [
        "I am writing to apply for the <b>PhD AI Internship</b> at Cambridge Consultants. "
        "Your work in intelligent systems &mdash; from real-time AI-enhanced medical imaging to edge algorithms "
        "that help visually impaired people navigate &mdash; represents exactly the kind of research-driven, "
        "high-impact engineering I want to contribute to. I am currently completing my <b>MSc in Applied "
        "Mathematical Sciences at Heriot-Watt University</b> (graduating 2026), and I believe my combination "
        "of mathematical research, applied ML, and real-world deployment experience makes me a strong fit.",

        "My thesis sits at the intersection of data-driven modelling and dynamical systems. I am investigating "
        "<i>Learning Dynamical Systems from Data using SINDy (Sparse Identification of Nonlinear Dynamics)</i> "
        "&mdash; applying sparse regression to recover governing equations directly from time-series observations, "
        "without prior knowledge of system structure. This work has deepened my understanding of Bayesian "
        "statistical thinking, signal processing, and the challenge of learning structured models from noisy, "
        "limited data &mdash; areas directly relevant to several of Cambridge Consultants' research streams.",

        "Alongside my research, I have delivered production-grade AI systems with measurable results. At Amdari, "
        "I built a fraudulent transaction detection system for a digital payments platform (NovaPay): I trained "
        "and compared four classifiers &mdash; Logistic Regression, Random Forest, XGBoost, and LightGBM &mdash; "
        "on 10,836 transactions with a 9.1% fraud rate, applying time-based splitting to prevent data leakage "
        "and using features spanning IP risk scores, device trust signals, transaction velocity, and KYC tier. "
        "The best-performing model achieved a <b>ROC-AUC of 0.982</b> and <b>PR-AUC of 0.969</b>, with Random "
        "Forest reaching <b>97% precision on fraud cases</b> at 98% overall accuracy. I have also built a "
        "complete customer churn prediction and analytics system &mdash; engineering 23 features from 200,000+ "
        "ride-hailing records, deploying a real-time FastAPI scoring endpoint, and building a Streamlit analytics "
        "dashboard for business stakeholders. These projects reflect the full modelling, training, testing, and "
        "communication cycle your internship describes.",

        "At <b>Pantech AI</b>, I have continued developing model training and deployment skills across multiple "
        "client projects, attending stand-ups and contributing to planning sessions &mdash; exactly the "
        "mixed-discipline, client-oriented environment Cambridge Consultants values.",

        "What draws me specifically to Cambridge Consultants is that you do not just publish &mdash; you build "
        "things that work in the real world. The opportunity to contribute to internal R&amp;D, work on "
        "state-of-the-art AI problems across defence, healthcare, and biotech, and be supported by a team of "
        "deep technical experts is precisely the environment in which I want to grow. My mathematical background "
        "gives me the rigour for algorithmically complex problems, and my industry experience means I can "
        "contribute immediately.",

        "I am available for a <b>6 or 12-month placement</b> with a flexible start date and am fully prepared "
        "to undergo UK National Security Vetting as required. I would welcome the opportunity to discuss my "
        "application further.",

        "Yours sincerely,",
    ]

    for p in paragraphs:
        story.append(Paragraph(p, s["CLBody"]))

    story.append(Spacer(1, 16))
    story.append(Paragraph("Sunday Monday Igbone", s["CLSign"]))
    story.append(Paragraph("otachesunday226@gmail.com", s["CLContact"]))

    doc.build(story)
    print(f"Cover letter saved: {path}")


if __name__ == "__main__":
    build_resume()
    build_cover_letter()
    print("\nBoth PDFs generated successfully.")
