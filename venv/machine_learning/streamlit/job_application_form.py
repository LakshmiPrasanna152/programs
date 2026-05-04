import streamlit as st
from datetime import date, datetime
import time

# ─── Page Configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Job Application Portal",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Custom CSS  (Light Blue Theme) ───────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=Playfair+Display:wght@700&display=swap');

    /* ── Base ── */
    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        color: #1a2a3a !important;
    }

    /* ── Page Background : soft sky-blue gradient ── */
    .stApp {
        background: linear-gradient(160deg, #e8f4fd 0%, #d0eaf8 40%, #bfe0f5 100%) !important;
        min-height: 100vh;
    }

    /* Force Streamlit's main block background transparent */
    .block-container {
        background: transparent !important;
        padding-top: 2rem !important;
    }

    /* ── Hero Banner ── */
    .hero-banner {
        background: linear-gradient(90deg, #1a73e8, #0ea5e9);
        border-radius: 18px;
        padding: 40px 48px;
        margin-bottom: 32px;
        box-shadow: 0 16px 48px rgba(26,115,232,0.25);
    }
    .hero-banner h1 {
        font-family: 'Playfair Display', serif;
        color: #ffffff;
        font-size: 2.6rem;
        margin: 0 0 6px 0;
        letter-spacing: -0.5px;
    }
    .hero-banner p {
        color: rgba(255,255,255,0.92);
        font-size: 1.05rem;
        margin: 0;
    }
    .hero-badge {
        display: inline-block;
        background: rgba(255,255,255,0.22);
        color: #ffffff;
        border-radius: 30px;
        padding: 4px 14px;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 1.4px;
        text-transform: uppercase;
        margin-bottom: 14px;
    }

    /* ── Section Card ── */
    .section-card {
        background: #ffffff;
        border: 1.5px solid #c8e0f4;
        border-radius: 16px;
        padding: 28px 32px 20px;
        margin-bottom: 24px;
        box-shadow: 0 4px 20px rgba(26,115,232,0.08);
    }
    .section-title {
        font-size: 1.0rem;
        font-weight: 700;
        color: #1a73e8;
        letter-spacing: 0.9px;
        text-transform: uppercase;
        margin-bottom: 18px;
        display: flex;
        align-items: center;
        gap: 8px;
        border-bottom: 2px solid #e3f0fc;
        padding-bottom: 10px;
    }

    /* ── Labels — dark & fully visible ── */
    label,
    .stTextInput label, .stNumberInput label,
    .stSelectbox label, .stMultiSelect label,
    .stRadio label, .stCheckbox label,
    .stSlider label, .stDateInput label,
    .stTextArea label, .stFileUploader label,
    .stTimeInput label,
    p, span, div {
        color: #1a2a3a !important;
        font-weight: 500 !important;
    }

    /* ── Input fields ── */
    input, textarea {
        background: #f0f7fe !important;
        color: #1a2a3a !important;
        border: 1.5px solid #93c5e8 !important;
        border-radius: 10px !important;
    }
    input:focus, textarea:focus {
        border-color: #1a73e8 !important;
        box-shadow: 0 0 0 3px rgba(26,115,232,0.15) !important;
        background: #ffffff !important;
    }
    input::placeholder, textarea::placeholder {
        color: #7aabcc !important;
    }

    /* Selectbox dropdowns */
    [data-baseweb="select"] > div {
        background: #f0f7fe !important;
        border: 1.5px solid #93c5e8 !important;
        border-radius: 10px !important;
        color: #1a2a3a !important;
    }
    [data-baseweb="select"] * {
        color: #1a2a3a !important;
    }

    /* ── Slider track ── */
    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, #1a73e8, #0ea5e9) !important;
    }

    /* ── Radio & Checkbox text ── */
    .stRadio > div label,
    .stCheckbox > div label {
        color: #1a2a3a !important;
        font-weight: 500 !important;
    }

    /* ── Multiselect tags ── */
    .stMultiSelect span[data-baseweb="tag"] {
        background: #1a73e8 !important;
        color: #fff !important;
        border-radius: 20px !important;
    }
    .stMultiSelect span[data-baseweb="tag"] span {
        color: #fff !important;
    }

    /* ── Submit Button ── */
    .stButton > button {
        background: linear-gradient(90deg, #1a73e8, #0ea5e9) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 14px 42px !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.5px !important;
        transition: all 0.25s ease !important;
        box-shadow: 0 8px 28px rgba(26,115,232,0.30) !important;
        width: 100% !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 14px 36px rgba(26,115,232,0.45) !important;
    }

    /* ── Progress bar ── */
    .stProgress > div > div {
        background: linear-gradient(90deg, #1a73e8, #0ea5e9) !important;
        border-radius: 10px !important;
    }
    .stProgress > div {
        background: #c8dff5 !important;
        border-radius: 10px !important;
    }

    /* ── Divider ── */
    hr { border-color: #c8e0f4 !important; }

    /* ── Metric boxes ── */
    [data-testid="stMetric"] {
        background: #ffffff !important;
        border: 1.5px solid #c8e0f4 !important;
        border-radius: 12px !important;
        padding: 16px !important;
        box-shadow: 0 2px 10px rgba(26,115,232,0.08) !important;
    }
    [data-testid="stMetricLabel"] {
        color: #4a7fa8 !important;
        font-weight: 600 !important;
    }
    [data-testid="stMetricValue"] {
        color: #1a2a3a !important;
        font-weight: 700 !important;
    }

    /* ── File uploader ── */
    [data-testid="stFileUploader"] {
        background: #f0f7fe !important;
        border: 2px dashed #5aabdf !important;
        border-radius: 12px !important;
    }
    [data-testid="stFileUploader"] * {
        color: #1a2a3a !important;
    }

    /* ── Alert / notification boxes ── */
    .stAlert { border-radius: 12px !important; }
    [data-testid="stNotification"] { color: #1a2a3a !important; }

    /* ── Expander ── */
    .streamlit-expanderHeader {
        background: #e8f4fd !important;
        color: #1a2a3a !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
    }

    /* ── JSON viewer ── */
    .element-container pre {
        background: #f0f7fe !important;
        color: #1a2a3a !important;
        border: 1px solid #c8e0f4 !important;
        border-radius: 10px !important;
    }

    /* ── Markdown headings ── */
    h1, h2, h3, h4 {
        color: #1a2a3a !important;
    }
</style>
""", unsafe_allow_html=True)


# ─── Hero Banner ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <div class="hero-badge">✦ Now Hiring</div>
    <h1>Job Application Portal</h1>
    <p>Complete the form below carefully. All fields marked with <b>*</b> are required.</p>
</div>
""", unsafe_allow_html=True)


# ─── Progress tracker ─────────────────────────────────────────────────────────
if "submitted" not in st.session_state:
    st.session_state.submitted = False

col_p1, col_p2 = st.columns([3, 1])
with col_p1:
    progress_val = st.session_state.get("progress", 10)
    st.progress(progress_val / 100)
with col_p2:
    st.metric("Form Progress", f"{progress_val}%")

st.markdown("<br>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 1 — Personal Information
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">👤 Personal Information</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    first_name = st.text_input("First Name *", placeholder="e.g. Priya")
with col2:
    last_name = st.text_input("Last Name *", placeholder="e.g. Sharma")
with col3:
    gender = st.selectbox("Gender *", ["— Select —", "Male", "Female", "Non-binary", "Prefer not to say"])

col4, col5 = st.columns(2)
with col4:
    dob = st.date_input(
        "Date of Birth *",
        value=date(1995, 1, 1),
        min_value=date(1950, 1, 1),
        max_value=date(2005, 12, 31),
    )
with col5:
    nationality = st.selectbox(
        "Nationality *",
        ["— Select —", "Indian", "American", "British", "Canadian", "Australian", "German", "Other"],
    )

phone = st.text_input("Phone Number *", placeholder="+91 98765 43210")
email = st.text_input("Email Address *", placeholder="yourname@example.com")
address = st.text_area("Residential Address", placeholder="Street, City, State, PIN", height=80)

st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 2 — Role & Availability
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🎯 Role & Availability</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    job_role = st.selectbox(
        "Applying for Position *",
        [
            "— Select Role —",
            "Software Engineer",
            "Data Scientist",
            "Product Manager",
            "UX/UI Designer",
            "DevOps Engineer",
            "Business Analyst",
            "Marketing Specialist",
        ],
    )
with col2:
    job_type = st.radio(
        "Employment Type *",
        ["Full-Time", "Part-Time", "Contract", "Internship"],
        horizontal=True,
    )

col3, col4 = st.columns(2)
with col3:
    work_mode = st.radio(
        "Work Preference *",
        ["On-site", "Remote", "Hybrid"],
        horizontal=True,
    )
with col4:
    joining_date = st.date_input(
        "Earliest Joining Date *",
        value=date.today(),
        min_value=date.today(),
    )

available_time = st.time_input("Preferred Interview Time", value=datetime.strptime("10:00", "%H:%M").time())
relocate = st.checkbox("✈️  I am open to relocation if required")

st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 3 — Education & Experience
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🎓 Education & Experience</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    highest_edu = st.selectbox(
        "Highest Education *",
        ["— Select —", "High School", "Diploma", "Bachelor's", "Master's", "MBA", "PhD", "Other"],
    )
with col2:
    field_of_study = st.text_input("Field of Study *", placeholder="e.g. Computer Science")

col3, col4 = st.columns(2)
with col3:
    graduation_year = st.number_input(
        "Graduation Year *", min_value=1980, max_value=2030, value=2020, step=1
    )
with col4:
    gpa = st.slider("CGPA / Percentage *", min_value=0.0, max_value=10.0, value=7.5, step=0.1)

experience_yrs = st.slider(
    "Total Years of Experience *",
    min_value=0,
    max_value=30,
    value=3,
    step=1,
    format="%d yrs",
)
current_ctc = st.number_input(
    "Current CTC (₹ LPA) — leave 0 if fresher", min_value=0.0, max_value=200.0, value=0.0, step=0.5
)
expected_ctc = st.number_input(
    "Expected CTC (₹ LPA) *", min_value=0.0, max_value=300.0, value=6.0, step=0.5
)

st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 4 — Skills & Tech Stack
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🛠️ Skills & Tech Stack</div>', unsafe_allow_html=True)

tech_skills = st.multiselect(
    "Technical Skills *",
    [
        "Python", "JavaScript", "TypeScript", "Java", "C++", "Go", "Rust",
        "React", "Vue", "Angular", "Node.js", "Django", "FastAPI", "Flask",
        "SQL", "PostgreSQL", "MongoDB", "Redis", "Docker", "Kubernetes",
        "AWS", "GCP", "Azure", "Terraform", "CI/CD", "Machine Learning",
        "Deep Learning", "NLP", "Data Analysis", "Tableau", "Power BI",
    ],
    default=["Python", "SQL"],
)

soft_skills = st.multiselect(
    "Soft Skills",
    [
        "Leadership", "Communication", "Team Collaboration", "Problem Solving",
        "Critical Thinking", "Adaptability", "Time Management", "Creativity",
        "Conflict Resolution", "Presentation", "Mentoring",
    ],
    default=["Communication", "Problem Solving"],
)

proficiency = st.select_slider(
    "Overall Proficiency Level *",
    options=["Beginner", "Intermediate", "Advanced", "Expert"],
    value="Intermediate",
)

languages = st.multiselect(
    "Languages Known",
    ["English", "Hindi", "Telugu", "Tamil", "Kannada", "Malayalam", "Bengali", "Marathi",
     "Spanish", "French", "German", "Japanese", "Mandarin"],
    default=["English", "Telugu"],
)

st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 5 — Documents & Links
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📎 Documents & Links</div>', unsafe_allow_html=True)

resume_file = st.file_uploader(
    "Upload Resume (PDF / DOCX) *",
    type=["pdf", "docx"],
    help="Max file size: 5 MB",
)

photo_file = st.file_uploader(
    "Upload Passport Photo (JPG / PNG)",
    type=["jpg", "jpeg", "png"],
)

col1, col2 = st.columns(2)
with col1:
    linkedin = st.text_input("LinkedIn Profile URL", placeholder="https://linkedin.com/in/yourname")
with col2:
    portfolio = st.text_input("Portfolio / GitHub URL", placeholder="https://github.com/yourname")

how_heard = st.selectbox(
    "How did you hear about us?",
    ["— Select —", "LinkedIn", "Naukri", "Indeed", "Referral", "Company Website", "Job Fair", "Other"],
)

st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 6 — Additional Questions
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">💬 Additional Questions</div>', unsafe_allow_html=True)

motivation = st.text_area(
    "Why do you want to join our company? *",
    placeholder="Describe your motivation in 100–200 words…",
    height=120,
)

achievement = st.text_area(
    "Describe your biggest professional achievement *",
    placeholder="Situation → Task → Action → Result…",
    height=100,
)

rating = st.slider(
    "How would you rate your communication skills? (1 = Poor, 10 = Excellent)",
    min_value=1, max_value=10, value=7,
)

notice_period = st.select_slider(
    "Notice Period *",
    options=["Immediate", "15 Days", "1 Month", "2 Months", "3 Months"],
    value="1 Month",
)

has_disability = st.radio(
    "Do you have any disability requiring accommodation?",
    ["No", "Yes"],
    horizontal=True,
)

disability_detail = ""
if has_disability == "Yes":
    disability_detail = st.text_input("Please specify (optional)", placeholder="Brief description…")

col1, col2 = st.columns(2)
with col1:
    background_check = st.checkbox("✅  I consent to a background verification check")
with col2:
    terms_agree = st.checkbox("✅  I agree to the Terms & Privacy Policy *")

st.markdown('</div>', unsafe_allow_html=True)


# ─── Submit Button ─────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
submit = st.button("🚀  Submit Application")


# ─── Validation & Submission ──────────────────────────────────────────────────
if submit:
    errors = []
    if not first_name.strip():
        errors.append("First Name is required.")
    if not last_name.strip():
        errors.append("Last Name is required.")
    if gender == "— Select —":
        errors.append("Please select your gender.")
    if not phone.strip():
        errors.append("Phone number is required.")
    if not email.strip() or "@" not in email:
        errors.append("A valid email address is required.")
    if job_role == "— Select Role —":
        errors.append("Please select a job role.")
    if highest_edu == "— Select —":
        errors.append("Please select your highest education.")
    if not field_of_study.strip():
        errors.append("Field of study is required.")
    if not tech_skills:
        errors.append("Please select at least one technical skill.")
    if resume_file is None:
        errors.append("Resume upload is required.")
    if not motivation.strip():
        errors.append("Motivation field cannot be empty.")
    if not achievement.strip():
        errors.append("Achievement field cannot be empty.")
    if not terms_agree:
        errors.append("You must agree to the Terms & Privacy Policy.")

    if errors:
        st.error("⚠️  Please fix the following errors before submitting:")
        for e in errors:
            st.markdown(f"- ❌ {e}")
        st.session_state["progress"] = 40
    else:
        # Show success flow
        with st.spinner("Submitting your application…"):
            time.sleep(1.8)

        st.session_state["progress"] = 100
        st.session_state["submitted"] = True
        st.success("🎉  Application submitted successfully! We'll get back to you within 5–7 business days.")

        st.balloons()

        # Summary
        st.markdown("---")
        st.markdown("### 📋 Application Summary")

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Applicant", f"{first_name} {last_name}")
        c2.metric("Role Applied", job_role)
        c3.metric("Experience", f"{experience_yrs} yrs")
        c4.metric("Expected CTC", f"₹{expected_ctc} LPA")

        with st.expander("View Full Details", expanded=False):
            st.json({
                "Personal": {
                    "Name": f"{first_name} {last_name}",
                    "Gender": gender,
                    "DOB": str(dob),
                    "Nationality": nationality,
                    "Phone": phone,
                    "Email": email,
                    "Address": address,
                },
                "Role": {
                    "Position": job_role,
                    "Type": job_type,
                    "Work Mode": work_mode,
                    "Joining Date": str(joining_date),
                    "Preferred Interview Time": str(available_time),
                    "Open to Relocation": relocate,
                    "Notice Period": notice_period,
                },
                "Education": {
                    "Highest Education": highest_edu,
                    "Field of Study": field_of_study,
                    "Graduation Year": graduation_year,
                    "CGPA": gpa,
                },
                "Experience": {
                    "Years": experience_yrs,
                    "Current CTC (LPA)": current_ctc,
                    "Expected CTC (LPA)": expected_ctc,
                },
                "Skills": {
                    "Technical": tech_skills,
                    "Soft Skills": soft_skills,
                    "Proficiency": proficiency,
                    "Languages": languages,
                    "Communication Rating": rating,
                },
                "Links": {
                    "LinkedIn": linkedin,
                    "Portfolio": portfolio,
                    "How Heard": how_heard,
                },
                "Additional": {
                    "Motivation": motivation,
                    "Achievement": achievement,
                    "Disability Accommodation": has_disability,
                    "Disability Detail": disability_detail,
                    "Background Check Consent": background_check,
                },
            })