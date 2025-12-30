import streamlit as st
import time
import matplotlib.pyplot as plt

from resume_parser import extract_text_from_pdf
from model import calculate_match, extract_skills
from skills import SKILLS


# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="AI Resume Screening System",
    page_icon="📄",
    layout="centered"
)

st.title("📄 AI Resume Screening System")
st.write("Upload a resume and compare it with a job description using Machine Learning & NLP.")

st.divider()

# -------------------- INPUT SECTION --------------------
resume_file = st.file_uploader(
    "Upload Resume (PDF only)",
    type=["pdf"]
)

jd_text = st.text_area(
    "Paste Job Description here",
    height=200
)

# -------------------- PROCESSING --------------------
if resume_file and jd_text:

    with st.spinner("🔍 Analyzing resume..."):
        time.sleep(1)

        # Extract resume text
        resume_text = extract_text_from_pdf(resume_file)

        # Skill extraction
        matched_skills = extract_skills(resume_text, SKILLS)
        missing_skills = list(set(SKILLS) - set(matched_skills))

        # Match score
        score = calculate_match(resume_text, jd_text)

    st.divider()

    # -------------------- RESULTS --------------------
    st.metric(
        label="Resume Match Score",
        value=f"{score} %",
        delta="Based on Job Description similarity"
    )

    if score >= 70:
        st.success("✅ Candidate Shortlisted")
    else:
        st.warning("❌ Candidate Not Shortlisted")

    st.divider()

    # -------------------- SKILLS DISPLAY --------------------
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("✅ Matched Skills")
        if matched_skills:
            st.success(", ".join(matched_skills))
        else:
            st.info("No matching skills found")

    with col2:
        st.subheader("❌ Missing Skills")
        if missing_skills:
            st.error(", ".join(missing_skills))
        else:
            st.success("No missing skills")

    st.divider()

    # -------------------- VISUALIZATION --------------------
    labels = ["Matched Skills", "Missing Skills"]
    sizes = [len(matched_skills), len(missing_skills)]

    fig, ax = plt.subplots()
    ax.pie(
        sizes,
        labels=labels,
        autopct="%1.1f%%",
        startangle=90
    )
    ax.axis("equal")

    st.subheader("📊 Skill Match Distribution")
    st.pyplot(fig)

    st.divider()

    # -------------------- DISCLAIMER --------------------
    st.caption(
        "⚠️ This tool is for educational purposes only and is intended to assist recruiters, not replace human judgment."
    )

else:
    st.info("⬆️ Please upload a resume and paste a job description to start analysis.")
