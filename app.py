import streamlit as st
import pandas as pd

from candidate import Candidate
from parser import ResumeParser
from skill_extractor import SkillExtractor
from ats_scorer import ATSScorer
from db import Database
from heap_ranking import HeapRanking


st.set_page_config(
    page_title="AI Powered Resume Screener",
    layout="wide"
)

st.title("🤖 AI Powered Resume Screener")
st.write("Upload resumes and compare them with the Job Description.")

jd = st.text_area(
    "Enter Job Description"
)

files = st.file_uploader(
    "Upload Resumes",
    type=["pdf"],
    accept_multiple_files=True
)


if st.button("Analyze"):

    if jd == "":
        st.warning("Please enter a Job Description")
        st.stop()

    if not files:
        st.warning("Please upload at least one resume")
        st.stop()

    parser = ResumeParser()
    extractor = SkillExtractor()
    scorer = ATSScorer()
    db = Database()

    candidates = []

    jd_skills = extractor.extract(jd)

    for file in files:

        text = parser.extract_text(file)

        skills = extractor.extract(text)

        score = scorer.calculate_score(
            jd,
            text
        )

        candidate = Candidate(
            file.name,
            file.name,
            skills
        )

        candidate.set_score(score)

        candidates.append(candidate)

        candidate_id = db.save_candidate(candidate)

        db.save_skills(
            candidate_id,
            skills
        )

    top_candidates = HeapRanking.top_candidates(
        candidates,
        10
    )

    st.success(f"Total Resumes Uploaded : {len(files)}")

    best = top_candidates[0]

    st.success(
        f"🏆 Best Candidate : {best.name} "
        f"({best.score:.2f}%)"
    )

    st.subheader("📊 Candidate Ranking")

    result = []

    rank = 1

    for candidate in top_candidates:

        missing_skills = []

        for skill in jd_skills:

            if skill not in candidate.skills:
                missing_skills.append(skill)

        if len(jd_skills) > 0:

            match = (
                (len(jd_skills) - len(missing_skills))
                / len(jd_skills)
            ) * 100

        else:
            match = 0

        result.append({

            "Rank": rank,

            "Name": candidate.name,

            "ATS Score (%)":
            round(candidate.score, 2),

            "Skill Match (%)":
            round(match, 2),

            "Skills":
            ", ".join(candidate.skills),

            "Missing Skills":
            ", ".join(missing_skills)

        })

        rank += 1

    df = pd.DataFrame(result)

    st.dataframe(
        df,
        use_container_width=True
    )

    st.subheader("📈 ATS Score Comparison")

    chart = df.set_index("Name")

    st.bar_chart(
        chart["ATS Score (%)"]
    )

    csv = df.to_csv(index=False)

    st.download_button(

        label="⬇ Download Results CSV",

        data=csv,

        file_name="ats_results.csv",

        mime="text/csv"
    )