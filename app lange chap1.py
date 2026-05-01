"""
╔══════════════════════════════════════════════════════════════════╗
║  Clinical Neurology — Chapter 1 Interactive Quiz & Analytics    ║
║  Source: Clinical Neurology, 10th Edition (Aminoff et al.)      ║
║  Run: streamlit run app.py                                       ║
╚══════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from datetime import datetime

# ─────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Clinical Neurology – Chapter 1 Quiz",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────────
# GLOBAL STYLE
# ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* ── Base typography ── */
    html, body, [class*="css"] { font-family: 'Segoe UI', sans-serif; }

    /* ── Header banner ── */
    .quiz-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        color: white;
        padding: 2rem 2.5rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }
    .quiz-header h1 { margin: 0; font-size: 2rem; letter-spacing: 0.5px; }
    .quiz-header p  { margin: 0.4rem 0 0; opacity: 0.75; font-size: 1rem; }

    /* ── Card containers ── */
    .card {
        background: #ffffff;
        border-radius: 14px;
        padding: 1.8rem;
        box-shadow: 0 2px 16px rgba(0,0,0,0.07);
        margin-bottom: 1.5rem;
        border: 1px solid #f0f0f0;
    }

    /* ── Question text ── */
    .question-text {
        font-size: 1.2rem;
        font-weight: 600;
        color: #1a1a2e;
        line-height: 1.6;
        margin-bottom: 1.2rem;
    }

    /* ── Concept badge ── */
    .concept-badge {
        display: inline-block;
        background: #e8f4fd;
        color: #1565c0;
        font-size: 0.75rem;
        font-weight: 700;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 1rem;
    }

    /* ── Feedback boxes ── */
    .feedback-correct {
        background: #e8f5e9;
        border-left: 5px solid #2e7d32;
        padding: 1rem 1.2rem;
        border-radius: 8px;
        margin-top: 1rem;
        color: #1b5e20;
    }
    .feedback-incorrect {
        background: #fce4ec;
        border-left: 5px solid #c62828;
        padding: 1rem 1.2rem;
        border-radius: 8px;
        margin-top: 1rem;
        color: #b71c1c;
    }

    /* ── Results summary table ── */
    .results-table th {
        background: #0f3460;
        color: white;
    }

    /* ── Metric card override ── */
    [data-testid="metric-container"] {
        background: #f8faff;
        border: 1px solid #e0e7ff;
        border-radius: 12px;
        padding: 1rem;
    }

    /* ── Admin section ── */
    .admin-header {
        background: linear-gradient(90deg, #0f3460, #533483);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
    }

    /* ── Progress labels ── */
    .progress-label {
        font-size: 0.85rem;
        color: #666;
        margin-bottom: 0.3rem;
    }

    /* ── Grade display ── */
    .grade-display {
        text-align: center;
        padding: 2rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
    }
    .grade-display .grade-number {
        font-size: 4rem;
        font-weight: 800;
        line-height: 1;
    }
    .grade-pass  { background: #e8f5e9; color: #2e7d32; }
    .grade-merit { background: #e3f2fd; color: #1565c0; }
    .grade-fail  { background: #fce4ec; color: #c62828; }

    /* ── Login form ── */
    .login-card {
        max-width: 520px;
        margin: 3rem auto;
        background: white;
        border-radius: 18px;
        padding: 2.5rem;
        box-shadow: 0 4px 30px rgba(0,0,0,0.1);
        border: 1px solid #e8eaf6;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────
# QUIZ DATA — 10 Questions from Chapter 1: Neurologic History & Exam
# Source: Clinical Neurology, 10th Ed. (Aminoff, Greenberg, Simon)
# ─────────────────────────────────────────────────────────────────
QUESTIONS = [
    {
        "id": 1,
        "concept": "Chief Complaint – Dizziness",
        "question": (
            "According to Chapter 1, 'dizziness' as a neurological chief complaint can mean "
            "three distinct clinical entities. Which of the following correctly pairs one of these "
            "entities with its definition?"
        ),
        "options": [
            "Vertigo — light-headedness resulting from cerebral hypoperfusion",
            "Presyncope — the illusion of movement of oneself or the environment",
            "Imbalance — unsteadiness due to extrapyramidal, vestibular, cerebellar, or sensory deficits",
            "Ataxia — loss of power from disorders affecting motor pathways",
        ],
        "answer": "Imbalance — unsteadiness due to extrapyramidal, vestibular, cerebellar, or sensory deficits",
        "explanation": (
            "Chapter 1 defines dizziness as encompassing three distinct phenomena: "
            "(1) Vertigo — the illusion of movement of oneself or the environment; "
            "(2) Imbalance — unsteadiness due to extrapyramidal, vestibular, cerebellar, or sensory deficits; "
            "(3) Presyncope — light-headedness resulting from cerebral hypoperfusion. "
            "Option A incorrectly defines vertigo; Option B confuses presyncope and vertigo; "
            "Option D (ataxia) is not listed as one of the three meanings of dizziness in Chapter 1."
        ),
    },
    {
        "id": 2,
        "concept": "Vital Signs – Orthostatic Hypotension",
        "question": (
            "When testing for orthostatic hypotension, which of the following blood pressure "
            "changes upon moving from recumbent to upright posture is considered diagnostic, "
            "according to Chapter 1?"
        ),
        "options": [
            "Systolic drop ≥ 10 mm Hg OR diastolic drop ≥ 5 mm Hg",
            "Systolic drop ≥ 20 mm Hg OR diastolic drop ≥ 10 mm Hg",
            "Systolic drop ≥ 30 mm Hg OR diastolic drop ≥ 15 mm Hg",
            "Any drop in systolic BP accompanied by a rise in heart rate",
        ],
        "answer": "Systolic drop ≥ 20 mm Hg OR diastolic drop ≥ 10 mm Hg",
        "explanation": (
            "Chapter 1 states that orthostatic hypotension is defined as a blood pressure drop of "
            "≥ 20 mm Hg (systolic) OR ≥ 10 mm Hg (diastolic) when a patient switches from recumbent "
            "to upright posture. Additionally, the chapter notes that if this drop is accompanied by a "
            "compensatory increase in pulse rate, sympathetic autonomic reflexes are intact and the cause "
            "is likely hypovolemia. Absence of a compensatory heart rate rise suggests autonomic dysfunction "
            "(e.g., multisystem atrophy, polyneuropathy) or sympatholytic drug effect."
        ),
    },
    {
        "id": 3,
        "concept": "Upper vs. Lower Motor Neuron Lesions",
        "question": (
            "A patient presents with hyperactive tendon reflexes, increased muscle tone, and an extensor "
            "plantar response (Babinski sign). Which localisation best explains this clinical picture "
            "according to Chapter 1?"
        ),
        "options": [
            "Lower motor neuron (anterior horn cell or peripheral nerve) lesion",
            "Neuromuscular junction disorder",
            "Upper motor neuron (central nervous system) lesion",
            "Primary muscle (myopathy) disorder",
        ],
        "answer": "Upper motor neuron (central nervous system) lesion",
        "explanation": (
            "Chapter 1 clearly distinguishes UMN from LMN lesions: Upper motor neuron (UMN) lesions "
            "cause increased muscle tone, hyperactive tendon reflexes, and Babinski signs (extensor plantar "
            "response). In contrast, lower motor neuron (LMN) lesions produce decreased muscle tone, "
            "hypoactive reflexes, muscle atrophy, and fasciculations. This distinction is fundamental to "
            "neuroanatomic localisation — UMN lesions affect the central nervous system (brain or spinal cord "
            "above the anterior horn cell), whereas LMN lesions affect the anterior horn cell, nerve root, "
            "or peripheral nerve."
        ),
    },
    {
        "id": 4,
        "concept": "Aphasia Syndromes",
        "question": (
            "A patient produces fluent speech but cannot understand spoken language and cannot repeat "
            "phrases. Their comprehension of written language is also impaired. According to Chapter 1's "
            "aphasia classification table, which aphasia syndrome does this describe?"
        ),
        "options": [
            "Expressive (Broca) aphasia",
            "Receptive (Wernicke) aphasia",
            "Conduction aphasia",
            "Anomic aphasia",
        ],
        "answer": "Receptive (Wernicke) aphasia",
        "explanation": (
            "Chapter 1 (Table 1-1) classifies aphasia syndromes by three key features: fluency, "
            "comprehension, and repetition. Receptive (Wernicke) aphasia is characterised by: fluency PRESERVED, "
            "comprehension IMPAIRED, repetition IMPAIRED. The chapter notes that 'language expression is preserved "
            "but comprehension and repetition are impaired,' with paraphasic errors and neologisms, and that these "
            "patients are often unaware of their deficit. Broca aphasia has impaired fluency but preserved "
            "comprehension. Conduction aphasia has intact fluency and comprehension but impaired repetition. "
            "Anomic aphasia has all three preserved except naming."
        ),
    },
    {
        "id": 5,
        "concept": "Muscle Strength Grading Scale",
        "question": (
            "When grading muscle strength according to the standard scale described in Chapter 1, "
            "what does a grade of '3' indicate?"
        ),
        "options": [
            "Decreased strength but can move against gravity plus added resistance",
            "Able to move against gravity but not against added resistance",
            "Able to move only with gravity eliminated (horizontal plane only)",
            "Flicker of muscle movement with no joint motion",
        ],
        "answer": "Able to move against gravity but not against added resistance",
        "explanation": (
            "Chapter 1 describes the standard 0–5 muscle strength grading scale: "
            "5 = normal strength; "
            "4 = decreased strength but can still move against gravity PLUS added resistance; "
            "3 = able to move against gravity but NOT against added resistance; "
            "2 = able to move only with gravity eliminated (horizontal movement); "
            "1 = flicker of movement; "
            "0 = no visible muscle contraction. "
            "Grade 3 therefore means the patient can lift against gravity alone but is overcome by any "
            "additional examiner resistance — a critically important distinction in neurological assessment."
        ),
    },
    {
        "id": 6,
        "concept": "Meningeal Signs",
        "question": (
            "A patient presents with neck stiffness, fever, and headache. On examination, passive flexion "
            "of the neck causes involuntary flexion of both hips and knees. This finding is called:"
        ),
        "options": [
            "Kernig sign",
            "Lasègue sign",
            "Brudzinski sign",
            "Babinski sign",
        ],
        "answer": "Brudzinski sign",
        "explanation": (
            "Chapter 1 defines meningeal signs as follows (Figure 1-5): "
            "Brudzinski sign — thigh and knee flexion in response to passive flexion of the neck; this indicates "
            "meningeal irritation, as seen in meningitis and subarachnoid haemorrhage. "
            "Kernig sign — resistance to passive extension at the knee with the hip flexed (described in the "
            "Extremities & Back section of Chapter 1). "
            "Lasègue sign — straight leg raising that reproduces radicular pain in L4–S2 distribution. "
            "Babinski sign — an extensor plantar response indicating an UMN lesion."
        ),
    },
    {
        "id": 7,
        "concept": "Papilledema",
        "question": (
            "According to Chapter 1, which of the following statements about papilledema is CORRECT?"
        ),
        "options": [
            "Papilledema is typically unilateral and causes significant reduction in visual acuity early in its course",
            "Papilledema results from atrophy of the optic nerve and is associated with multiple sclerosis",
            "Papilledema is almost always bilateral, usually does not impair vision except for enlarging the blind spot, and is not painful",
            "In fully developed papilledema, spontaneous venous pulsations are readily visible and the disk margins are sharp",
        ],
        "answer": "Papilledema is almost always bilateral, usually does not impair vision except for enlarging the blind spot, and is not painful",
        "explanation": (
            "Chapter 1 states explicitly: 'Papilledema is almost always bilateral, does not typically impair "
            "vision except for enlargement of the blind spot, and is not painful.' It is caused by increased "
            "intracranial pressure transmitted to the optic nerve sheath. Early signs include engorged retinal "
            "veins, absent spontaneous venous pulsations, and disk hyperaemia. Fully developed papilledema shows "
            "disk elevation above the retinal plane with obscured vessels. Optic disk pallor (not papilledema) "
            "results from optic nerve atrophy and is associated with MS."
        ),
    },
    {
        "id": 8,
        "concept": "Gait Abnormalities",
        "question": (
            "Chapter 1 describes several classic gait abnormalities. Which description correctly matches "
            "the 'hemiplegic gait'?"
        ),
        "options": [
            "Wide-based, staggering gait possibly associated with nystagmus, due to cerebellar disease",
            "Slow, stiff gait with legs crossing in front of each other (scissoring), seen in bilateral pyramidal disease",
            "High-stepping gait with the foot slapping the floor, due to foot drop from peroneal nerve or L4-L5 lesion",
            "The affected leg is held extended and internally rotated, the foot is inverted and plantar flexed, and the leg swings in a semicircle (circumduction)",
        ],
        "answer": "The affected leg is held extended and internally rotated, the foot is inverted and plantar flexed, and the leg swings in a semicircle (circumduction)",
        "explanation": (
            "Chapter 1 (Figure 1-25) describes the hemiplegic gait as: the affected leg held extended and "
            "internally rotated, with the foot inverted and plantar flexed, and the leg moving in a circular "
            "direction at the hip (circumduction). This results from unilateral UMN (corticospinal tract) damage, "
            "as seen after a hemispheric stroke. Option A describes cerebellar ataxic gait; Option B is paraplegic "
            "(scissoring) gait from bilateral pyramidal involvement; Option C describes steppage gait from foot "
            "drop (peroneal nerve or L4-L5 lesion)."
        ),
    },
    {
        "id": 9,
        "concept": "Time Course as a Diagnostic Clue",
        "question": (
            "According to the diagnostic formulation principles in Chapter 1, which disease category "
            "typically produces neurologic symptoms that evolve within minutes?"
        ),
        "options": [
            "Neoplastic and degenerative disorders",
            "Inflammatory and metabolic disorders",
            "Ischemia, seizure, or syncope",
            "Infectious and autoimmune disorders",
        ],
        "answer": "Ischemia, seizure, or syncope",
        "explanation": (
            "Chapter 1 states: 'Only a few processes produce neurologic symptoms that evolve within minutes — "
            "typically ischemia, seizure, or syncope.' The chapter presents time course as a critical clue to "
            "aetiology (Figure 1-1). Neoplastic and degenerative processes give rise to progressive, unremitting "
            "symptoms. Inflammatory and metabolic processes may cause subacute onset over hours to days. "
            "Multiple sclerosis is characterised by episodes of exacerbation and remission. Understanding this "
            "temporal pattern is fundamental to neurologic differential diagnosis."
        ),
    },
    {
        "id": 10,
        "concept": "Sensory Pathway Localisation",
        "question": (
            "In Chapter 1, which sensory modalities are specifically stated to be conveyed by the "
            "large-fibre pathway travelling in the posterior columns of the spinal cord and brainstem "
            "medial lemniscus?"
        ),
        "options": [
            "Pain and temperature sensation",
            "Vibration and position (joint) sense",
            "Light touch only",
            "Pain, temperature, and crude touch",
        ],
        "answer": "Vibration and position (joint) sense",
        "explanation": (
            "Chapter 1 describes two major somatosensory pathways: "
            "(1) Large sensory fibres travelling in the posterior columns/medial lemniscus carry vibration "
            "sense and position (proprioceptive) sense. "
            "(2) Small sensory fibres travelling in the spinothalamic tracts carry pain and temperature sense. "
            "(3) Light touch is conveyed by BOTH pathways. "
            "This anatomical distinction is diagnostically important: a posterior column lesion (e.g., vitamin B12 "
            "deficiency, tabes dorsalis) causes loss of vibration and proprioception with preserved pain/temperature, "
            "whereas a spinothalamic lesion causes the opposite dissociation."
        ),
    },
]

CSV_FILE = "quiz_results.csv"

# ─────────────────────────────────────────────────────────────────
# SESSION STATE INITIALISATION
# ─────────────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "page": "login",          # login | quiz | results
        "name": "",
        "student_id": "",
        "current_q": 0,
        "answers": [],            # list of chosen option strings
        "submitted": False,       # whether current question was submitted
        "selected": None,         # currently selected radio value
        "start_time": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ─────────────────────────────────────────────────────────────────
# CSV HELPERS
# ─────────────────────────────────────────────────────────────────
def save_result(name: str, sid: str, answers: list) -> None:
    score = sum(
        1 for i, q in enumerate(QUESTIONS)
        if i < len(answers) and answers[i] == q["answer"]
    )
    grade = round(score / len(QUESTIONS) * 100)

    row = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "name": name,
        "student_id": sid,
        "score": score,
        "grade": grade,
    }
    # Per-question correct flags
    for i, q in enumerate(QUESTIONS):
        row[f"q{i+1}_correct"] = 1 if (i < len(answers) and answers[i] == q["answer"]) else 0

    df_new = pd.DataFrame([row])
    if os.path.exists(CSV_FILE):
        df_new.to_csv(CSV_FILE, mode="a", header=False, index=False)
    else:
        df_new.to_csv(CSV_FILE, mode="w", header=True, index=False)


def load_results() -> pd.DataFrame | None:
    if not os.path.exists(CSV_FILE):
        return None
    try:
        df = pd.read_csv(CSV_FILE)
        return df if not df.empty else None
    except Exception:
        return None


# ─────────────────────────────────────────────────────────────────
# DOWNLOAD TEXT BUILDER
# ─────────────────────────────────────────────────────────────────
def build_download_text(name: str, sid: str, answers: list) -> str:
    score = sum(1 for i, q in enumerate(QUESTIONS) if i < len(answers) and answers[i] == q["answer"])
    grade = round(score / len(QUESTIONS) * 100)
    lines = [
        "=" * 65,
        "  CLINICAL NEUROLOGY – CHAPTER 1 QUIZ RESULT",
        "=" * 65,
        f"  Student Name : {name}",
        f"  Student ID   : {sid}",
        f"  Date         : {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"  Score        : {score} / {len(QUESTIONS)}",
        f"  Grade        : {grade} / 100",
        "=" * 65,
        "",
    ]
    for i, q in enumerate(QUESTIONS):
        user_ans = answers[i] if i < len(answers) else "Not answered"
        correct = user_ans == q["answer"]
        lines += [
            f"Q{i+1}. [{q['concept']}]",
            f"   {q['question']}",
            f"   Your Answer   : {user_ans}",
            f"   Correct Answer: {q['answer']}",
            f"   Result        : {'✓ CORRECT' if correct else '✗ INCORRECT'}",
            f"   Explanation   : {q['explanation']}",
            "",
        ]
    lines += ["=" * 65, "  End of Report", "=" * 65]
    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────
# ██ PAGE 1 — LOGIN
# ─────────────────────────────────────────────────────────────────
def page_login():
    st.markdown("""
    <div class="quiz-header">
        <h1>🧠 Clinical Neurology — Chapter 1</h1>
        <p>Neurologic History & Examination · Interactive Assessment Module</p>
    </div>
    """, unsafe_allow_html=True)

    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown("### 👤 Student Identification")
        st.markdown("Please enter your details to begin the 10-question quiz.")
        st.divider()

        name = st.text_input("Full Name", placeholder="e.g., Sarah Johnson", key="login_name")
        sid  = st.text_input("Student ID", placeholder="e.g., MED-2024-0042", key="login_sid")

        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"📋 **{len(QUESTIONS)} Questions**")
        with col2:
            st.info("⏱️ **No Time Limit**")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 Start Quiz", use_container_width=True, type="primary"):
            if not name.strip():
                st.error("Please enter your full name.")
            elif not sid.strip():
                st.error("Please enter your Student ID.")
            else:
                st.session_state.name = name.strip()
                st.session_state.student_id = sid.strip()
                st.session_state.page = "quiz"
                st.session_state.current_q = 0
                st.session_state.answers = []
                st.session_state.submitted = False
                st.session_state.selected = None
                st.session_state.start_time = datetime.now()
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Admin dashboard (always accessible below login) ──
    st.markdown("<br>", unsafe_allow_html=True)
    render_admin_dashboard()


# ─────────────────────────────────────────────────────────────────
# ██ PAGE 2 — QUIZ ENGINE
# ─────────────────────────────────────────────────────────────────
def page_quiz():
    qi = st.session_state.current_q
    q  = QUESTIONS[qi]
    total = len(QUESTIONS)

    # ── Header ──
    st.markdown("""
    <div class="quiz-header">
        <h1>🧠 Clinical Neurology — Chapter 1 Quiz</h1>
        <p>Neurologic History & Examination · Aminoff, Greenberg & Simon, 10th Edition</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Top bar: name + progress ──
    col_info, col_prog = st.columns([1, 2])
    with col_info:
        st.markdown(f"**Student:** {st.session_state.name}  \n**ID:** {st.session_state.student_id}")
    with col_prog:
        progress_pct = qi / total
        st.markdown(f'<div class="progress-label">Question {qi + 1} of {total}</div>', unsafe_allow_html=True)
        st.progress(progress_pct)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Question Card ──
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f'<span class="concept-badge">📖 Concept: {q["concept"]}</span>', unsafe_allow_html=True)
    st.markdown(f'<div class="question-text">Q{qi + 1}. {q["question"]}</div>', unsafe_allow_html=True)

    # Radio — preserve selection via session_state key
    radio_key = f"radio_q{qi}"
    if radio_key not in st.session_state:
        st.session_state[radio_key] = None

    selected = st.radio(
        "Choose your answer:",
        options=q["options"],
        key=radio_key,
        index=None if st.session_state[radio_key] is None
              else (q["options"].index(st.session_state[radio_key])
                    if st.session_state[radio_key] in q["options"] else None),
    )

    st.markdown('</div>', unsafe_allow_html=True)

    # ── Feedback after submit ──
    if st.session_state.submitted:
        user_ans = st.session_state.answers[qi] if qi < len(st.session_state.answers) else None
        if user_ans == q["answer"]:
            st.markdown(f"""
            <div class="feedback-correct">
                <strong>✅ Correct!</strong><br>
                <strong>Explanation:</strong> {q['explanation']}
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="feedback-incorrect">
                <strong>❌ Incorrect.</strong>
                The correct answer is: <em>{q['answer']}</em><br><br>
                <strong>Explanation:</strong> {q['explanation']}
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        # Navigation button
        is_last = qi == total - 1
        btn_label = "📊 View My Results" if is_last else "Next Question ➜"
        if st.button(btn_label, use_container_width=True, type="primary"):
            if is_last:
                save_result(
                    st.session_state.name,
                    st.session_state.student_id,
                    st.session_state.answers,
                )
                st.session_state.page = "results"
            else:
                st.session_state.current_q += 1
                st.session_state.submitted = False
            st.rerun()

    else:
        # Submit button
        if st.button("Submit Answer ✔", use_container_width=True, type="primary"):
            if selected is None:
                st.warning("⚠️ Please select an answer before submitting.")
            else:
                # Record answer
                if len(st.session_state.answers) <= qi:
                    st.session_state.answers.append(selected)
                else:
                    st.session_state.answers[qi] = selected
                st.session_state.submitted = True
                st.rerun()

    # ── Live score tracker in sidebar ──
    with st.sidebar:
        st.markdown("### 📈 Progress Tracker")
        answered = len(st.session_state.answers)
        correct_so_far = sum(
            1 for i, a in enumerate(st.session_state.answers)
            if i < len(QUESTIONS) and a == QUESTIONS[i]["answer"]
        )
        st.metric("Questions Answered", f"{answered} / {total}")
        st.metric("Correct So Far", correct_so_far)
        if answered > 0:
            pct = round(correct_so_far / answered * 100)
            st.metric("Running %", f"{pct}%")
        st.divider()
        st.caption(f"Student: {st.session_state.name}")
        st.caption(f"ID: {st.session_state.student_id}")


# ─────────────────────────────────────────────────────────────────
# ██ PAGE 3 — RESULTS
# ─────────────────────────────────────────────────────────────────
def page_results():
    answers = st.session_state.answers
    score   = sum(1 for i, q in enumerate(QUESTIONS) if i < len(answers) and answers[i] == q["answer"])
    grade   = round(score / len(QUESTIONS) * 100)

    # Grade classification
    if grade >= 80:
        grade_class, grade_label, grade_emoji = "grade-pass",  "Distinction", "🏆"
    elif grade >= 60:
        grade_class, grade_label, grade_emoji = "grade-merit", "Pass",        "✅"
    else:
        grade_class, grade_label, grade_emoji = "grade-fail",  "Needs Review","📚"

    st.markdown("""
    <div class="quiz-header">
        <h1>📊 Quiz Results</h1>
        <p>Clinical Neurology · Chapter 1 · Neurologic History & Examination</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Grade Display ──
    col_g, col_m = st.columns([1, 2])
    with col_g:
        st.markdown(f"""
        <div class="grade-display {grade_class}">
            <div class="grade-number">{grade_emoji} {grade}</div>
            <div style="font-size:1.2rem; font-weight:600; margin-top:0.5rem">{grade_label}</div>
            <div style="opacity:0.75; font-size:0.9rem">out of 100</div>
        </div>""", unsafe_allow_html=True)

    with col_m:
        st.markdown("### 📋 Summary")
        c1, c2, c3 = st.columns(3)
        c1.metric("Score", f"{score} / {len(QUESTIONS)}")
        c2.metric("Grade", f"{grade}%")
        c3.metric("Status", grade_label)
        st.markdown(f"""
        **Student:** {st.session_state.name}  
        **Student ID:** {st.session_state.student_id}  
        **Completed:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
        """)

    # ── Download Button ──
    report_text = build_download_text(
        st.session_state.name, st.session_state.student_id, answers
    )
    st.download_button(
        label="📥 Download My Full Report (.txt)",
        data=report_text,
        file_name=f"neurology_ch1_{st.session_state.student_id}_{datetime.now().strftime('%Y%m%d')}.txt",
        mime="text/plain",
        use_container_width=True,
    )

    st.markdown("---")

    # ── Detailed Results Table ──
    st.markdown("### 📝 Detailed Question Review")

    table_data = []
    for i, q in enumerate(QUESTIONS):
        user_ans = answers[i] if i < len(answers) else "Not answered"
        correct  = user_ans == q["answer"]
        table_data.append({
            "Q#"          : f"Q{i+1}",
            "Concept"     : q["concept"],
            "Your Answer" : user_ans,
            "Correct Answer": q["answer"],
            "Result"      : "✅ Correct" if correct else "❌ Incorrect",
            "Explanation" : q["explanation"],
        })

    df_results = pd.DataFrame(table_data)

    # Colour rows by result
    def colour_row(row):
        if "✅" in row["Result"]:
            return ["background-color: #e8f5e9"] * len(row)
        else:
            return ["background-color: #fce4ec"] * len(row)

    styled = df_results.style.apply(colour_row, axis=1)
    st.dataframe(styled, use_container_width=True, hide_index=True, height=420)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Retake Quiz", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

    st.markdown("---")
    render_admin_dashboard()


# ─────────────────────────────────────────────────────────────────
# ██ ADMIN ANALYTICS DASHBOARD
# ─────────────────────────────────────────────────────────────────
def render_admin_dashboard():
    with st.expander("🔐 Admin Analytics Dashboard", expanded=False):
        st.markdown("""
        <div class="admin-header">
            <strong>📊 Class Performance Analytics</strong> — Chapter 1: Neurologic History & Examination
        </div>
        """, unsafe_allow_html=True)

        df = load_results()

        if df is None:
            st.info("📭 No quiz results yet. Data will appear here after students complete the quiz.")
            return

        # ── Ensure q_correct columns exist ──
        q_cols = [f"q{i+1}_correct" for i in range(len(QUESTIONS))]
        for col in q_cols:
            if col not in df.columns:
                df[col] = 0

        total_students = len(df)
        avg_grade      = round(df["grade"].mean(), 1)
        high_grade     = int(df["grade"].max())
        low_grade      = int(df["grade"].min())
        pass_rate      = round((df["grade"] >= 60).sum() / total_students * 100, 1)

        # ── Class Metrics ──
        st.markdown("#### 🎓 Class Metrics")
        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("👥 Total Students", total_students)
        m2.metric("📈 Average Grade", f"{avg_grade}%")
        m3.metric("🏆 Highest Grade", f"{high_grade}%")
        m4.metric("📉 Lowest Grade", f"{low_grade}%")
        m5.metric("✅ Pass Rate (≥60%)", f"{pass_rate}%")

        st.markdown("<br>", unsafe_allow_html=True)

        col_hist, col_bar = st.columns(2)

        # ── Score Distribution Histogram ──
        with col_hist:
            st.markdown("#### 📊 Score Distribution")
            fig_hist = px.histogram(
                df, x="grade",
                nbins=10,
                range_x=[0, 100],
                color_discrete_sequence=["#0f3460"],
                labels={"grade": "Grade (%)", "count": "Number of Students"},
                template="plotly_white",
            )
            fig_hist.add_vline(
                x=avg_grade, line_dash="dash", line_color="#e94560",
                annotation_text=f"Avg: {avg_grade}%",
                annotation_position="top right",
            )
            fig_hist.update_layout(
                bargap=0.1,
                plot_bgcolor="white",
                paper_bgcolor="white",
                xaxis=dict(showgrid=False),
                yaxis=dict(gridcolor="#f0f0f0"),
                margin=dict(t=20, b=10),
            )
            st.plotly_chart(fig_hist, use_container_width=True)

        # ── Concept Mastery Bar Chart ──
        with col_bar:
            st.markdown("#### 🎯 Concept Mastery (% Correct per Question)")
            concept_data = []
            for i, q in enumerate(QUESTIONS):
                col = f"q{i+1}_correct"
                pct = round(df[col].mean() * 100, 1) if col in df.columns else 0
                concept_data.append({
                    "Question": f"Q{i+1}",
                    "Concept": q["concept"],
                    "% Correct": pct,
                })
            df_concepts = pd.DataFrame(concept_data)

            fig_bar = px.bar(
                df_concepts,
                x="Question", y="% Correct",
                hover_data=["Concept"],
                color="% Correct",
                color_continuous_scale=["#c62828", "#f9a825", "#2e7d32"],
                range_color=[0, 100],
                labels={"% Correct": "% Correct"},
                template="plotly_white",
            )
            fig_bar.add_hline(
                y=60, line_dash="dash", line_color="#c62828",
                annotation_text="60% threshold",
                annotation_position="top left",
            )
            fig_bar.update_layout(
                plot_bgcolor="white",
                paper_bgcolor="white",
                yaxis=dict(range=[0, 105], gridcolor="#f0f0f0"),
                xaxis=dict(showgrid=False),
                coloraxis_showscale=False,
                margin=dict(t=20, b=10),
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        # ── Concepts needing more teaching ──
        st.markdown("#### ⚠️ Topics Requiring Additional Teaching (< 60% correct)")
        weak = df_concepts[df_concepts["% Correct"] < 60].sort_values("% Correct")
        if weak.empty:
            st.success("🎉 All concepts are above the 60% threshold — great class performance!")
        else:
            for _, row in weak.iterrows():
                st.warning(
                    f"**{row['Question']} — {row['Concept']}** → "
                    f"Only **{row['% Correct']}%** of students answered correctly."
                )

        # ── Raw Data Table ──
        st.markdown("#### 📋 Individual Student Results")
        display_cols = ["timestamp", "name", "student_id", "score", "grade"]
        st.dataframe(df[display_cols].sort_values("timestamp", ascending=False),
                     use_container_width=True, hide_index=True)

        # ── CSV Download ──
        csv_bytes = df.to_csv(index=False).encode()
        st.download_button(
            "📥 Export Full Results CSV",
            data=csv_bytes,
            file_name="quiz_results_export.csv",
            mime="text/csv",
        )


# ─────────────────────────────────────────────────────────────────
# ██ ROUTER
# ─────────────────────────────────────────────────────────────────
if st.session_state.page == "login":
    page_login()
elif st.session_state.page == "quiz":
    page_quiz()
elif st.session_state.page == "results":
    page_results()
