import streamlit as st
import requests
# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="🇮🇳 Scheme Assistant",
    layout="wide",
    initial_sidebar_state="expanded"
)
# ============================================================
# CUSTOM COLOR THEME
# ============================================================
st.markdown(
 """<style>
    /* --------------------------------------------------------
       MAIN APPLICATION
    -------------------------------------------------------- */
    .stApp {
        background: linear-gradient(
            135deg,
            #f8fbff 0%,
            #eef6ff 50%,
            #f3fff8 100%
        );
        color: #17324d;
    }
    /* --------------------------------------------------------
       HEADINGS
    -------------------------------------------------------- */
    h1 {
        color: #0b3d91 !important;
        font-weight: 800 !important;
    }
    h2,
    h3 {
        color: #14532d !important;
        font-weight: 700 !important;
    }
    /* --------------------------------------------------------
       CAPTIONS
    -------------------------------------------------------- */
    [data-testid="stCaptionContainer"] {
        color: #52677a;
    }
    /* --------------------------------------------------------
       SIDEBAR
    -------------------------------------------------------- */
    section[data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #e8f3ff 0%,
            #f5fbff 50%,
            #effcf5 100%
        );
        border-right: 2px solid #c7def5;
    }
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #0b3d91 !important;
    }
    /* --------------------------------------------------------
       METRIC CARDS
    -------------------------------------------------------- */
    [data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #cfe2f3;
        border-radius: 14px;
        padding: 14px;
        box-shadow:
            0 3px 12px rgba(11, 61, 145, 0.08);
    }
    [data-testid="stMetricLabel"] {
        color: #42627d !important;
    }
    [data-testid="stMetricValue"] {
        color: #0b3d91 !important;
        font-weight: 800 !important;
    }
    /* --------------------------------------------------------
       BUTTONS
    -------------------------------------------------------- */
    .stButton > button {
        background: #0b5ed7;
        color: white;
        border: 1px solid #084298;
        border-radius: 10px;
        font-weight: 600;
        transition: 0.2s ease;
    }
    .stButton > button:hover {
        background: #084298;
        color: white;
        border-color: #052c65;
    }
    /* MAIN SEARCH BUTTON */
    .stButton > button[kind="primary"] {
        background: linear-gradient(
            90deg,
            #0b5ed7,
            #198754
        );
        color: white;
        border: none;
        font-size: 1.05rem;
        padding: 0.65rem 1rem;
        font-weight: 700;
    }
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(
            90deg,
            #084298,
            #146c43
        );
        color: white;
    }
    /* --------------------------------------------------------
       TEXT AREA AND SELECT BOXES
    -------------------------------------------------------- */
    .stTextArea textarea,
    .stSelectbox div[data-baseweb="select"] > div {
        border: 1px solid #b9d4ec !important;
        border-radius: 10px !important;
        background-color: #ffffff !important;
    }
    .stTextArea textarea:focus {
        border-color: #0b5ed7 !important;
        box-shadow:
            0 0 0 2px rgba(11, 94, 215, 0.12) !important;
    }
    /* --------------------------------------------------------
       ALERTS
    -------------------------------------------------------- */
    div[data-testid="stAlert"] {
        border-radius: 12px;
        border-left-width: 5px;
    }
    /* --------------------------------------------------------
       EXPANDERS
    -------------------------------------------------------- */
    details {
        background: #ffffff;
        border: 1px solid #cfe2f3;
        border-radius: 12px;
        margin-bottom: 8px;
    }
    details summary {
        color: #0b3d91 !important;
        font-weight: 650 !important;
    }
    /* --------------------------------------------------------
       DIVIDERS
    -------------------------------------------------------- */
    hr {
        border-color: #cfe2f3 !important;
    }
    /* --------------------------------------------------------
       FOOTER
    -------------------------------------------------------- */
    footer {
        visibility: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# ============================================================
# APPLICATION HEADER
# ============================================================
st.title("🇮🇳 Scheme Assistant")
st.caption(
    "🤖 AI-powered Government Scheme Discovery Assistant"
)
st.divider()
# ==========================================================
# OLLAMA CONFIGURATION
# ============================================================
OLLAMA_URL = "http://localhost:11434"
def get_ollama_models():
    """
    Get the list of locally installed Ollama models.
    """
    try:
        response = requests.get(
            f"{OLLAMA_URL}/api/tags",
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            models = [
                model.get("name")
                for model in data.get("models", [])
                if model.get("name")
            ]
            return models
        return []
    except requests.exceptions.ConnectionError:
        return []
    except requests.exceptions.Timeout:
        return []
    except Exception:
        return []
def ask_ollama(prompt, model_name):
    """
    Send a prompt to Ollama and return the generated response.
    """
    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": model_name,
                "prompt": prompt,
                "stream": False
            },
            timeout=180
        )
        if response.status_code == 200:
            data = response.json()
            return data.get(
                "response",
                "No response was generated."
            )
        return (
            f"Ollama returned an error "
            f"(status code {response.status_code})."
        )
    except requests.exceptions.ConnectionError:
        return (
            "Unable to connect to Ollama. "
            "Please make sure Ollama is running."
        )
    except requests.exceptions.Timeout:
        return (
            "The AI request timed out. "
            "Please try again."
        )
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"
# ============================================================
# GOVERNMENT SCHEMES DATA
# ============================================================
SCHEMES = [
    {
        "name": "PM Scholarship Scheme",
        "category": "Education",
        "description": (
            "Scholarship support for eligible students."
        ),
        "keywords": [
            "student",
            "education",
            "scholarship",
            "college",
            "study"
        ]
    },
    {
        "name": "PM-KISAN",
        "category": "Agriculture",
        "description": (
            "Income support scheme for eligible farmer families."
        ),
        "keywords": [
            "farmer",
            "agriculture",
            "farming",
            "crop",
            "kisan"
        ]
    },
    {
        "name": "Ayushman Bharat PM-JAY",
        "category": "Healthcare",
        "description": (
            "Health coverage support for eligible families."
        ),
        "keywords": [
            "health",
            "hospital",
            "medical",
            "healthcare",
            "treatment"
        ]
    },
    {
        "name": "PM Mudra Yojana",
        "category": "Business",
        "description": (
            "Credit support for eligible micro and small businesses."
        ),
        "keywords": [
            "business",
            "startup",
            "loan",
            "entrepreneur",
            "shop",
            "small business"
        ]
    },
    {
        "name": "Pradhan Mantri Awas Yojana",
        "category": "Housing",
        "description": (
            "Housing assistance for eligible beneficiaries."
        ),
        "keywords": [
            "house",
            "home",
            "housing",
            "rent",
            "construction"
        ]
    },
    {
        "name": "PM SVANidhi",
        "category": "Business",
        "description": (
            "Support for eligible street vendors."
        ),
        "keywords": [
            "street vendor",
            "vendor",
            "business",
            "loan",
            "shop"
        ]
    },
    {
        "name": "Skill India",
        "category": "Skill Development",
        "description": (
            "Skill development and training opportunities."
        ),
        "keywords": [
            "skill",
            "training",
            "job",
            "employment",
            "career"
        ]
    },
    {
        "name": "Stand-Up India",
        "category": "Business",
        "description": (
            "Bank loans for eligible entrepreneurs."
        ),
        "keywords": [
            "business",
            "entrepreneur",
            "startup",
            "loan"
        ] }]
# ============================================================
# SESSION STATE
# ============================================================
if "question" not in st.session_state:
    st.session_state.question = ""
if "answer" not in st.session_state:
    st.session_state.answer = ""
if "searched" not in st.session_state:
    st.session_state.searched = False
# ============================================================
# SIDEBAR - USER PROFILE
# ============================================================
with st.sidebar:
    st.header("👤 Your Profile")
    st.caption(
        "Provide your details to get more relevant scheme suggestions."
    )
    age_group = st.selectbox(
        "Age Group",
        [
            "Below 18",
            "18–25",
            "26–40",
            "41–60",
            "Above 60"
        ]
    )
    occupation = st.selectbox(
        "Occupation",
        [
            "Student",
            "Farmer",
            "Self-employed",
            "Business Owner",
            "Employee",
            "Job Seeker",
            "Homemaker",
            "Senior Citizen",
            "Other"
        ]
    )
    state = st.selectbox(
        "State / UT",
        [
            "All India",
            "Andhra Pradesh",
            "Telangana",
            "Karnataka",
            "Tamil Nadu",
            "Kerala",
            "Maharashtra",
            "Delhi",
            "Gujarat",
            "Rajasthan",
            "West Bengal",
            "Uttar Pradesh",
            "Other"
        ]
    )
    income = st.selectbox(
        "Income Range",
        [
            "Prefer not to say",
            "Below ₹1 Lakh",
            "₹1–3 Lakhs",
            "₹3–5 Lakhs",
            "₹5–10 Lakhs",
            "Above ₹10 Lakhs"
        ]
    )
    purpose = st.selectbox(
        "Main Purpose",
        [
            "Education",
            "Employment",
            "Agriculture",
            "Healthcare",
            "Business",
            "Housing",
            "Skill Development",
            "Financial Assistance",
            "Other"
        ]
    )
    st.divider()
    st.subheader("⚙️ Search Settings")
    category_filter = st.selectbox(
        "Scheme Category",
        [
            "All Categories",
            "Education",
            "Agriculture",
            "Healthcare",
            "Business",
            "Housing",
            "Skill Development"
        ])
# ============================================================
# DASHBOARD
# ============================================================
st.subheader("📊 Scheme Dashboard")
models = get_ollama_models()
if models:
    ollama_status = "Online"
else:
    ollama_status = "Offline"
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(
        "📚 Schemes",
        len(SCHEMES)
    )
with col2:
    st.metric(
        "🗂️ Categories",
        len(
            set(
                scheme["category"]
                for scheme in SCHEMES
            )
        )
    )
with col3:
    st.metric(
        "🤖 Ollama",
        ollama_status
    )
with col4:
    st.metric(
        "🇮🇳 Coverage",
        "India"
    )
# ============================================================
# PROFILE SUMMARY
# ============================================================
st.subheader("👤 Your Profile Summary")
profile_col1, profile_col2, profile_col3, profile_col4 = st.columns(4)
with profile_col1:
    st.info(
        f"**Age Group**\n\n{age_group}"
    )
with profile_col2:
    st.info(
        f"**Occupation**\n\n{occupation}"
    )
with profile_col3:
    st.info(
        f"**State / UT**\n\n{state}"
    )
with profile_col4:
    st.info(
        f"**Purpose**\n\n{purpose}"
    )
# ============================================================
# QUICK QUESTIONS
# ============================================================
st.subheader("⚡ Quick Questions")
quick_col1, quick_col2, quick_col3, quick_col4 = st.columns(4)
with quick_col1:
    if st.button(
        "🎓 Schemes for students",
        use_container_width=True
    ):
        st.session_state.question = (
            "What government schemes are available for students?"
        )
        st.session_state.searched = False
        st.rerun()
with quick_col2:
    if st.button(
        "🌾 Schemes for farmers",
        use_container_width=True
    ):
        st.session_state.question = (
            "What government schemes are available for farmers?"
        )
        st.session_state.searched = False
        st.rerun()
with quick_col3:
    if st.button(
        "🏥 Healthcare schemes",
        use_container_width=True
    ):
        st.session_state.question = (
            "What healthcare government schemes are available?"
        )
        st.session_state.searched = False
        st.rerun()
with quick_col4:
    if st.button(
        "💼 Small business schemes",
        use_container_width=True
    ):
        st.session_state.question = (
            "What government schemes support small businesses?"
        )
        st.session_state.searched = False
        st.rerun()
# ============================================================
# USER QUESTION
# ============================================================
st.subheader("🔍 Ask About Government Schemes")
question = st.text_area(
    "Enter your question",
    value=st.session_state.question,
    height=120,
    placeholder=(
        "Example: What government schemes can help "
        "me with education?"
    )
)
# ============================================================
# SEARCH BUTTON
# ============================================================
search_button = st.button(
    "🔍 Find Government Schemes",
    type="primary",
    use_container_width=True
)
# ============================================================
# SEARCH PROCESS
# ============================================================
if search_button:
    if not question.strip():
        st.warning(
            "⚠️ Please enter a question before searching."
        )
    else:
        st.session_state.question = question
        # ----------------------------------------------------
        # CHECK OLLAMA
        # ----------------------------------------------------
        models = get_ollama_models()
        if not models:
            st.error(
                "❌ Ollama is not available.\n\n"
                "Please make sure Ollama is installed "
                "and running on your computer."
            )
        else:
            # ------------------------------------------------
            # SELECT FIRST AVAILABLE MODEL
            # ------------------------------------------------
            model_name = models[0]
            # ------------------------------------------------
            # SEARCH TEXT
            # ------------------------------------------------
            search_text = " ".join(
                [
                    question,
                    purpose,
                    occupation,
                    category_filter
                ]
            ).lower()
            # ------------------------------------------------
            # SCORE SCHEMES
            # ------------------------------------------------
            scored_schemes = []
            for scheme in SCHEMES:
                score = 0
                # Keyword matching
                for keyword in scheme["keywords"]:
                    if keyword.lower() in search_text:
                        score += 2
                # Category matching
                if (
                    category_filter != "All Categories"
                    and scheme["category"]
                    == category_filter
                ):
                    score += 5
                # Purpose matching
                if (
                    purpose.lower()
                    == scheme["category"].lower()
                ):
                    score += 4
                # Occupation matching
                occupation_lower = occupation.lower()
                if (
                    occupation_lower
                    in " ".join(
                        scheme["keywords"]
                    ).lower()
                ):
                    score += 3
                scored_schemes.append(
                    {
                        "scheme": scheme,
                        "score": score
                    }
                )
            # ------------------------------------------------
            # SORT SCHEMES
            # ------------------------------------------------
            scored_schemes.sort(
                key=lambda x: x["score"],
                reverse=True
            )
            # ------------------------------------------------
            # SELECT TOP 5
            # ------------------------------------------------
            top_schemes = [
                item["scheme"]
                for item in scored_schemes[:5]
            ]
            # ------------------------------------------------
            # BUILD SCHEME CONTEXT
            # ------------------------------------------------
            scheme_context = ""
            for scheme in top_schemes:
                scheme_context += (
                    f"\nScheme Name: "
                    f"{scheme['name']}\n"
                )
                scheme_context += (
                    f"Category: "
                    f"{scheme['category']}\n"
                )
                scheme_context += (
                    f"Description: "
                    f"{scheme['description']}\n"
                )
                scheme_context += "\n"
            # ------------------------------------------------
            # AI PROMPT
            # ------------------------------------------------
            prompt = f"""
You are an AI Government Scheme Assistant for India.
Your job is to help users understand government schemes
using ONLY the scheme information provided below.
USER PROFILE:
Age Group:
{age_group}
Occupation:
{occupation}
State / UT:
{state}
Income Range:
{income}
Main Purpose:
{purpose}
USER QUESTION:
{question}
RELEVANT SCHEMES:
{scheme_context}
INSTRUCTIONS:

1. Answer the user's question clearly.
2. Use simple and easy-to-understand language.
3. Recommend the most relevant schemes from the provided list.
4. Explain why each recommended scheme may be relevant.
5. Mention the scheme name.
6. Mention its purpose.
7. Explain who may potentially benefit.
8. Explain possible benefits only when supported by the
   provided information.
9. Do not invent eligibility requirements.
10. Do not invent benefit amounts.
11. Do not invent application deadlines.
12. Do not invent government websites or links.
13. Do not claim that the user is definitely eligible.
14. Clearly mention that eligibility should be verified
    using the official government portal.
15. If the provided information is insufficient,
    say so honestly.
16. Keep the answer structured and useful.
For each scheme, use this style:
### Scheme Name
**Why it may be relevant:**  
Explain briefly.
**Purpose:**  
Explain the purpose.
**Who may benefit:**  
Give a general explanation based only on
the provided information.
**Important:**  
Eligibility and application details should be
verified through the official government portal.
At the end, provide a short recommendation about
which schemes the user should investigate first.
"""
            # ------------------------------------------------
            # CALL OLLAMA
            # ------------------------------------------------
            with st.spinner(
                "🤖 AI is analyzing your profile and finding relevant schemes..."
            ):
                answer = ask_ollama(
                    prompt,
                    model_name
                )
            st.session_state.answer = answer
            st.session_state.searched = True
# ============================================================
# AI RECOMMENDATION
# ============================================================
if st.session_state.searched:
    st.divider()
    st.subheader("🤖 AI Recommendation")
    st.write(
        st.session_state.answer
    )
    # ========================================================
    # RELEVANT SCHEMES
    # ========================================================
    st.subheader("📚 Relevant Schemes")
    search_text = " ".join(
        [
            st.session_state.question,
            purpose,
            occupation,
            category_filter
        ]
    ).lower()
    scored_schemes = []
    for scheme in SCHEMES:
        score = 0
        for keyword in scheme["keywords"]:
            if keyword.lower() in search_text:
                score += 2
        if (
            category_filter != "All Categories"
            and scheme["category"]
            == category_filter
        ):
            score += 5
        if (
            purpose.lower()
            == scheme["category"].lower()
        ):
            score += 4
        occupation_lower = occupation.lower()
        if (
            occupation_lower
            in " ".join(
                scheme["keywords"]
            ).lower()
        ):
            score += 3
        scored_schemes.append(
            {
                "scheme": scheme,
                "score": score
            }
        )
    scored_schemes.sort(
        key=lambda x: x["score"],
        reverse=True
    )
    top_schemes = scored_schemes[:5]
    for item in top_schemes:
        scheme = item["scheme"]
        score = item["score"]
        with st.expander(
            f"📌 {scheme['name']} — {scheme['category']}"
        ):
            st.write(
                f"**Description:** "
                f"{scheme['description']}"
            )
            if score > 0:
                st.success(
                    f"⭐ Relevance score: {score}"
                )
            else:
                st.info(
                    "This scheme is included as "
                    "a general recommendation."
                )
# ============================================================
# OLLAMA CONNECTION STATUS
# ============================================================
st.divider()
with st.expander("🛠️ Ollama Connection Status"):
    current_models = get_ollama_models()
    if current_models:
        st.success(
            "🟢 Ollama is connected and ready."
        )
        st.write("Installed models:")
        for model in current_models:
            st.write(
                f"• {model}"
            )
    else:
        st.error(
            "🔴 Ollama is not currently available."
        )
        st.write(
            "Make sure Ollama is running and try again."
        )
# ============================================================
# FOOTER
# ============================================================
st.divider()
st.caption(
    "IN Scheme Assistant • "
    "AI-powered Government Scheme Discovery"
)
st.caption(
    "⚠️ Please verify scheme eligibility, benefits, "
    "and application details on official government portals."
)