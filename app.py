
import streamlit as st
import anthropic
import os
from datetime import datetime
import base64


st.set_page_config(
    page_title="Dr. Sajjad Math Tutor",
    page_icon="🎓",
    layout="wide"
)

# Dark/Light mode
st.sidebar.title("⚙️ Settings")
dark_mode = st.sidebar.toggle("🌙 Dark Mode", value=True)

if dark_mode:
    bg_color = "#0D1B2A"
    text_color = "#FFFFFF"
else:
    bg_color = "#FFFFFF"
    text_color = "#000000"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg_color}; color: {text_color}; }}
    </style>
    <h1 style="text-align: center; color: #00C9B1;">🎓 Math Tutor</h1>
    <p style="text-align: center; color: gray;">
    Your Smart Math Tutor | Grade 1 to PhD |Houston TX
    </p>
    <hr>
""", unsafe_allow_html=True)

# Level Selection
st.sidebar.markdown("---")
st.sidebar.title("📚 Select Level")
level = st.sidebar.selectbox(
    "Choose your class:",
    [
        # Primary
        "Grade 1",
        "Grade 2",
        "Grade 3",
        "Grade 4",
        "Grade 5",
        # Middle School
        "Grade 6",
        "Grade 7",
        "Grade 8",
        # High School
        "Grade 9",
        "Grade 10",
        "Grade 11",
        "Grade 12",
        # University Core
        "University — Calculus 1",
        "University — Calculus 2",
        "University — Linear Algebra",
        "University — Differential Equations",
        "University — Real Analysis",
        "University — Abstract Algebra",
        "University — Complex Analysis",
        "University — Numerical Methods",
        "University — Topology",
        "University — Probability Theory",
        "University — Mathematical Statistics",
        "University — Discrete Mathematics",
        "University — Graph Theory",
        "University — Number Theory",
        "University — Optimization",
        "University — Mathematical Logic",
        # Applied Math
        "Applied — Financial Mathematics",
        "Applied — Mathematical Physics",
        "Applied — Operations Research",
        "Applied — Game Theory",
        "Applied — Cryptography & Math",
        # PhD Level
        "PhD — Functional Analysis",
        "PhD — Algebraic Topology",
        "PhD — Differential Geometry",
        "PhD — Advanced Number Theory",
        "PhD — Measure Theory",
        "PhD — Advanced Statistics",
        "PhD — Machine Learning Math",
        "PhD — Advanced Math (General)",
    ]
)

st.sidebar.markdown("*Your Teacher:*")
st.sidebar.markdown("👨‍🏫 Dr. Sajjad Shaukat")
st.sidebar.markdown("🎓 PhD Mathematics")
st.sidebar.markdown("🏛️ Texas Southern University")
st.sidebar.markdown("📍 Houston TX")

# All prompts
prompts = {
    "Grade 1": "You are a very friendly fun teacher for Grade 1 children aged 6-7. Use simple words, emojis and exciting examples. Cover ALL Grade 1 topics: counting, addition, subtraction, shapes, patterns.",
    "Grade 2": "You are a fun teacher for Grade 2 children aged 7-8. Cover ALL Grade 2 topics: addition, subtraction, place values, measurement, basic geometry.",
    "Grade 3": "You are a patient teacher for Grade 3 aged 8-9. Cover ALL Grade 3 topics: multiplication, division, fractions, time, measurement.",
    "Grade 4": "You are an encouraging teacher for Grade 4 aged 9-10. Cover ALL Grade 4 topics: fractions, decimals, geometry, measurement, factors, multiples.",
    "Grade 5": "You are a supportive teacher for Grade 5 aged 10-11. Cover ALL Grade 5 topics: decimals, percentages, fractions, basic algebra, geometry.",
    "Grade 6": "You are a friendly math teacher for Grade 6. Cover ALL Grade 6 topics: ratios, percentages, negative numbers, geometry, statistics.",
    "Grade 7": "You are a patient math teacher for Grade 7. Cover ALL Grade 7 topics: algebra basics, ratios, percentages, geometry, probability.",
    "Grade 8": "You are an algebra teacher for Grade 8. Cover ALL Grade 8 topics: linear equations, inequalities, graphing, geometry, statistics.",
    "Grade 9": "You are a geometry teacher for Grade 9. Cover ALL Grade 9 topics: geometry, algebra 1, statistics, basic trigonometry.",
    "Grade 10": "You are a math teacher for Grade 10. Cover ALL Grade 10 topics: trigonometry, algebra 2, statistics, geometry.",
    "Grade 11": "You are a pre-calculus teacher for Grade 11. Cover ALL Grade 11 topics: functions, limits introduction, exponentials, logarithms, sequences.",
    "Grade 12": "You are a math teacher for Grade 12. Cover ALL Grade 12 topics: calculus introduction, statistics, probability, discrete math.",
    "University — Calculus 1": "You are a Calculus 1 professor. Topics: limits, derivatives, basic integration.",
    "University — Calculus 2": "You are a Calculus 2 professor. Topics: advanced integration, sequences, series.",
    "University — Linear Algebra": "You are a Linear Algebra professor. Topics: vectors, matrices, eigenvalues, vector spaces.",
    "University — Differential Equations": "You are a Differential Equations professor. Topics: ODEs, PDEs, Laplace transforms.",
    "University — Real Analysis": "You are a Real Analysis professor. Topics: rigorous proofs, continuity, convergence.",
    "University — Abstract Algebra": "You are an Abstract Algebra professor. Topics: groups, rings, fields, homomorphisms.",
    "University — Complex Analysis": "You are a Complex Analysis professor. Topics: complex numbers, analytic functions, contour integration.",
    "University — Numerical Methods": "You are a Numerical Methods professor. Topics: numerical integration, solving equations, approximation.",
    "University — Topology": "You are a Topology professor. Topics: open sets, continuity, compactness, connectedness.",
    "University — Probability Theory": "You are a Probability Theory professor. Topics: probability spaces, random variables, distributions.",
    "University — Mathematical Statistics": "You are a Mathematical Statistics professor. Topics: estimation, hypothesis testing, regression.",
    "University — Discrete Mathematics": "You are a Discrete Math professor. Topics: logic, sets, combinatorics, graph theory.",
    "University — Graph Theory": "You are a Graph Theory professor. Topics: graphs, trees, paths, coloring, network flows.",
    "University — Number Theory": "You are a Number Theory professor. Topics: primes, divisibility, modular arithmetic.",
    "University — Optimization": "You are an Optimization professor. Topics: linear programming, convex optimization.",
    "University — Mathematical Logic": "You are a Mathematical Logic professor. Topics: propositional logic, predicate logic, proof theory.",
    "Applied — Financial Mathematics": "You are a Financial Mathematics tutor. Topics: interest rates, derivatives pricing, stochastic calculus.",
    "Applied — Mathematical Physics": "You are a Mathematical Physics tutor. Topics: classical mechanics, quantum mechanics mathematics.",
    "Applied — Operations Research": "You are an Operations Research tutor. Topics: linear programming, queuing theory, simulation.",
    "Applied — Game Theory": "You are a Game Theory tutor. Topics: Nash equilibrium, cooperative games, strategic thinking.",
    "Applied — Cryptography & Math": "You are a Cryptography tutor. Topics: number theory, RSA, elliptic curves, hash functions.",
    "PhD — Functional Analysis": "You are a Functional Analysis expert. Topics: Banach spaces, Hilbert spaces, operators, spectral theory.",
    "PhD — Algebraic Topology": "You are an Algebraic Topology expert. Topics: homotopy, homology, cohomology.",
    "PhD — Differential Geometry": "You are a Differential Geometry expert. Topics: manifolds, curvature, geodesics.",
    "PhD — Advanced Number Theory": "You are an Advanced Number Theory expert. Topics: analytic number theory, L-functions.",
    "PhD — Measure Theory": "You are a Measure Theory expert. Topics: sigma algebras, Lebesgue measure, integration.",
    "PhD — Advanced Statistics": "You are an Advanced Statistics expert. Topics: asymptotic theory, robust statistics.",
    "PhD — Machine Learning Math": "You are a Machine Learning Mathematics expert. Topics: optimization, probability, linear algebra in ML.",
    "PhD — Advanced Math (General)": "You are an expert mathematician helping a PhD student with any advanced topic.",
}

system_prompt = prompts[level] + " Always use plain text. No LaTeX or dollar signs. Be encouraging, clear and precise."

# Show level
st.markdown(f"*📖 Current Level:* {level}")
st.markdown("---")

# Initialize client
client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY", "YOUR_KEY_HERE")
)

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "history" not in st.session_state:
    st.session_state.history = []
if "current_level" not in st.session_state:
    st.session_state.current_level = level

# Reset when level changes
if st.session_state.current_level != level:
    st.session_state.messages = []
    st.session_state.current_level = level
    st.rerun()

# Search history in sidebar
st.sidebar.markdown("---")
st.sidebar.title("📜 Search History")
if st.session_state.history:
    for item in reversed(st.session_state.history[-10:]):
        st.sidebar.markdown(f"• {item}")
else:
    st.sidebar.markdown("No history yet")

if st.sidebar.button("🗑️ Clear History"):
    st.session_state.history = []
    st.session_state.messages = []
    st.rerun()

# Show chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Input
if prompt := st.chat_input(f"Ask your {level} question..."):
    timestamp = datetime.now().strftime("%H:%M")
    st.session_state.history.append(f"[{timestamp}] {prompt[:35]}...")

    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = client.messages.create(
                model="claude-haiku-4-5",
                max_tokens=1024,
                system=system_prompt,
                messages=st.session_state.messages
            )
            reply = response.content[0].text
            st.write(reply)
            
            # Audio player
            from gtts import gTTS
            import base64
            tts = gTTS(text=reply, lang='en', tld='com')
            tts.save("response.mp3")
            with open("response.mp3", "rb") as f:
                audio_bytes = f.read()
            audio_b64 = base64.b64encode(audio_bytes).decode()
            st.markdown(
                f'<audio controls src="data:audio/mp3;base64,{audio_b64}"></audio>',
                unsafe_allow_html=True
            )

    st.session_state.messages.append({
        "role": "assistant", 
        "content": reply
    })
