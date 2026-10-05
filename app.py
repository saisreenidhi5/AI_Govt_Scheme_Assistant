import streamlit as st
import requests


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="IN Scheme Assistant",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# APPLICATION TITLE
# ============================================================

st.title("🇮🇳 IN Scheme Assistant")

st.caption(
    "🤖 AI-powered Government Scheme Discovery Assistant"
)

st.divider()


# ============================================================
# OLLAMA CONFIGURATION
# ============================================================

OLLAMA_URL = "http://localhost:11434"


def get_ollama_models():
    """
    Get all models installed in Ollama.
    """

    try:
        response = requests.get(
            f"{OLLAMA_URL}/api/tags",
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()

            models = data.get("models", [])

            return [
                model.get("name")
                for model in models
                if model.get("name")
            ]

        return []

    except requests.exceptions.RequestException:
        return []


def ask_ollama(prompt, model_name):
    """
    Send a prompt to Ollama.
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
                "No response received from Ollama."
            )

        return (
            f"❌ Ollama returned error {response.status_code}\n\n"
            f"Details: {response.text}"
        )

    except requests.exceptions.ConnectionError:

        return (
            "❌ Cannot connect to Ollama.\n\n"
            "Please make sure Ollama is running."
        )

    except requests.exceptions.Timeout:

        return (
            "⏳ Ollama took too long to respond.\n\n"
            "Please try again."
        )

    except Exception as e:

        return f"❌ Unexpected error: {str(e)}"


# ============================================================
# GOVERNMENT SCHEME DATA
# ============================================================

SCHEMES = [

    {
        "name": "PM Scholarship Scheme",
        "category": "Education",
        "description": "Scholarship support for eligible students.",
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
        "description": "Income support scheme for eligible farmer families.",
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
        "description": "Health coverage support for eligible families.",
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
        "description": "Credit support for eligible micro and small businesses.",
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
        "description": "Housing assistance for eligible beneficiaries.",
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
        "description": "Support for eligible street vendors.",
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
        "description": "Skill development and training opportunities.",
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
        "description": "Bank loans for eligible entrepreneurs.",
        "keywords": [
            "business",
            "entrepreneur",
            "startup",
            "loan"
        ]
    }

]


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
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("👤 Your Profile")

    st.caption(
        "Tell us a little about yourself to get more relevant recommendations."
    )

    age_group = st.selectbox(
        "🎂 Age Group",
        [
            "Below 18",
            "18–25",
            "26–40",
            "41–60",
            "Above 60"
        ]
    )

    occupation = st.selectbox(
        "💼 Occupation",
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
        "📍 State / Union Territory",
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
        "💰 Income Range",
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
        "🎯 Main Purpose",
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

    category = st.selectbox(
        "🏷️ Scheme Category",
        [
            "All Categories",
            "Education",
            "Agriculture",
            "Healthcare",
            "Business",
            "Housing",
            "Skill Development"
        ]
    )


# ============================================================
# DASHBOARD METRICS
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "📋 Schemes",
        len(SCHEMES)
    )

with col2:
    categories = len(
        set(scheme["category"] for scheme in SCHEMES)
    )

    st.metric(
        "🏷️ Categories",
        categories
    )

with col3:
    models = get_ollama_models()

    if models:
        ollama_status = "Online"
    else:
        ollama_status = "Offline"

    st.metric(
        "🤖 Ollama",
        ollama_status
    )

with col4:
    st.metric(
        "🇮🇳 Coverage",
        "India"
    )


st.divider()


# ============================================================
# PROFILE SUMMARY
# ============================================================

st.subheader("👤 Your Profile")

p1, p2, p3, p4 = st.columns(4)

with p1:
    st.info(f"🎂 **Age**\n\n{age_group}")

with p2:
    st.info(f"💼 **Occupation**\n\n{occupation}")

with p3:
    st.info(f"📍 **State**\n\n{state}")

with p4:
    st.info(f"🎯 **Purpose**\n\n{purpose}")


# ============================================================
# QUICK QUESTIONS
# ============================================================

st.subheader("💡 Quick Questions")

q1, q2, q3, q4 = st.columns(4)

with q1:
    if st.button(
        "🎓 Schemes for students",
        use_container_width=True
    ):
        st.session_state.question = (
            "What government schemes are available for students?"
        )

with q2:
    if st.button(
        "🌾 Schemes for farmers",
        use_container_width=True
    ):
        st.session_state.question = (
            "What government schemes are available for farmers?"
        )

with q3:
    if st.button(
        "🏥 Healthcare schemes",
        use_container_width=True
    ):
        st.session_state.question = (
            "What healthcare government schemes are available?"
        )

with q4:
    if st.button(
        "💼 Small business schemes",
        use_container_width=True
    ):
        st.session_state.question = (
            "What government schemes support small businesses?"
        )


# ============================================================
# QUESTION INPUT
# ============================================================

st.subheader("🔎 Ask Your Question")

question = st.text_area(
    "What would you like to know?",
    value=st.session_state.question,
    height=120,
    placeholder=(
        "Example: What government schemes can help me "
        "with education?"
    )
)


# ============================================================
# SEARCH BUTTON
# ============================================================

search = st.button(
    "🔍 Find Government Schemes",
    type="primary",
    use_container_width=True
)


# ============================================================
# SEARCH / AI PROCESSING
# ============================================================

if search:

    if not question.strip():

        st.warning(
            "⚠️ Please enter a question first."
        )

    else:

        st.session_state.question = question
        st.session_state.searched = True

        # ----------------------------------------------------
        # FIND OLLAMA MODELS
        # ----------------------------------------------------

        models = get_ollama_models()

        if not models:

            st.error(
                "❌ No Ollama model was found."
            )

            st.info(
                "Make sure Ollama is running and that a model "
                "is installed."
            )

        else:

            # Use first installed model automatically
            model_name = models[0]

            # ------------------------------------------------
            # FIND RELEVANT LOCAL SCHEMES
            # ------------------------------------------------

            search_text = (
                question.lower()
                + " "
                + purpose.lower()
                + " "
                + occupation.lower()
                + " "
                + category.lower()
            )

            relevant_schemes = []

            for scheme in SCHEMES:

                score = 0

                for keyword in scheme["keywords"]:

                    if keyword.lower() in search_text:
                        score += 1

                if (
                    category == "All Categories"
                    or scheme["category"] == category
                ):
                    score += 1

                if score > 0:
                    relevant_schemes.append(
                        (score, scheme)
                    )

            relevant_schemes.sort(
                key=lambda x: x[0],
                reverse=True
            )

            selected_schemes = [
                scheme
                for score, scheme in relevant_schemes[:5]
            ]

            # ------------------------------------------------
            # CREATE AI PROMPT
            # ------------------------------------------------

            scheme_context = "\n".join(
                [
                    f"- {scheme['name']} "
                    f"({scheme['category']}): "
                    f"{scheme['description']}"
                    for scheme in selected_schemes
                ]
            )

            if not scheme_context:

                scheme_context = (
                    "No locally matched schemes were found. "
                    "Use your knowledge carefully and clearly "
                    "state when information should be verified."
                )

            prompt = f"""
You are an AI assistant that helps people discover
Indian government schemes.

IMPORTANT:
Do not invent eligibility requirements, benefit amounts,
application links, deadlines, or government rules.

Use simple language.

USER PROFILE
------------
Age Group: {age_group}
Occupation: {occupation}
State: {state}
Income Range: {income}
Main Purpose: {purpose}

USER QUESTION
-------------
{question}

POTENTIALLY RELEVANT SCHEMES
-----------------------------
{scheme_context}

TASK
----
Answer the user's question clearly.

For every relevant scheme, explain:

1. Scheme name
2. What it is for
3. Who may be eligible
4. Main benefits
5. Important documents
6. How to apply
7. Any important conditions

If exact eligibility or benefit information is uncertain,
tell the user to verify it on the official government
portal.

End with:

"⚠️ Please verify the latest eligibility and application
details on the official government website before applying."
"""

            # ------------------------------------------------
            # CALL OLLAMA
            # ------------------------------------------------

            with st.spinner(
                f"🤖 {model_name} is analyzing your question..."
            ):

                answer = ask_ollama(
                    prompt,
                    model_name
                )

            st.session_state.answer = answer

            # ------------------------------------------------
            # AI RESULT
            # ------------------------------------------------

            st.divider()

            st.subheader("🤖 AI Recommendation")

            st.write(answer)

            # ------------------------------------------------
            # RELEVANT SCHEMES
            # ------------------------------------------------

            st.divider()

            st.subheader("📋 Relevant Schemes")

            if selected_schemes:

                for scheme in selected_schemes:

                    with st.expander(
                        f"📌 {scheme['name']}  •  "
                        f"{scheme['category']}"
                    ):

                        st.write(
                            scheme["description"]
                        )

                        st.write(
                            "🔎 **Why it may be relevant:** "
                            "It matches your question, "
                            "profile, or selected category."
                        )

            else:

                st.info(
                    "No matching schemes were found in the "
                    "current scheme database. Try a different "
                    "question or category."
                )


# ============================================================
# OLLAMA STATUS
# ============================================================

st.divider()

with st.expander("🤖 Ollama Connection Status"):

    current_models = get_ollama_models()

    if current_models:

        st.success(
            "✅ Ollama is connected and available."
        )

        st.write("**Installed model(s):**")

        for model in current_models:
            st.write(f"• `{model}`")

    else:

        st.error(
            "❌ Ollama is not available."
        )

        st.write(
            "Make sure Ollama is running on "
            "`http://localhost:11434`."
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🇮🇳 IN Scheme Assistant • AI-powered government scheme discovery"
)

st.caption(
    "⚠️ This application provides informational assistance. "
    "Always verify the latest scheme details with the relevant "
    "official government department or portal."
)