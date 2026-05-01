"""
╔══════════════════════════════════════════════════════════════════════╗
║  Clinical Neurology — Chapter 1  ·  Full Learning Module            ║
║  Source: Clinical Neurology, 10th Edition (Aminoff et al.)          ║
║  Tabs: 📖 Study Guide  |  📝 Quiz  |  📊 Analytics                  ║
║  Run : streamlit run app.py                                          ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

# ─────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Clinical Neurology Ch.1 — Learning Module",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────────────
# GLOBAL CSS
# ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  html, body, [class*="css"] { font-family: "Segoe UI", sans-serif; }
  .main-header {
    background: linear-gradient(135deg, #0d1b2a 0%, #1b3a5c 60%, #0f3460 100%);
    color: white; padding: 2rem 2.5rem; border-radius: 16px;
    margin-bottom: 1.5rem; box-shadow: 0 8px 32px rgba(0,0,0,0.3);
  }
  .main-header h1 { margin:0; font-size:2rem; letter-spacing:.5px; }
  .main-header p  { margin:.4rem 0 0; opacity:.75; font-size:.95rem; }
  .q-card {
    background:#fff; border-radius:14px; padding:1.8rem;
    box-shadow: 0 2px 16px rgba(0,0,0,.07); margin-bottom:1.2rem;
    border:1px solid #f0f0f0;
  }
  .q-concept {
    display:inline-block; background:#e8f4fd; color:#1565c0;
    font-size:.72rem; font-weight:700; padding:.25rem .75rem;
    border-radius:20px; text-transform:uppercase; letter-spacing:.5px;
    margin-bottom:.9rem;
  }
  .q-text { font-size:1.15rem; font-weight:600; color:#1a1a2e; line-height:1.6; }
  .fb-ok  { background:#e8f5e9; border-left:5px solid #2e7d32;
            padding:1rem 1.2rem; border-radius:8px; margin-top:1rem; color:#1b5e20; }
  .fb-err { background:#fce4ec; border-left:5px solid #c62828;
            padding:1rem 1.2rem; border-radius:8px; margin-top:1rem; color:#b71c1c; }
  .grade-box { text-align:center; padding:2rem; border-radius:16px; margin-bottom:1.5rem; }
  .grade-num { font-size:4rem; font-weight:800; line-height:1; }
  .grade-pass  { background:#e8f5e9; color:#2e7d32; }
  .grade-merit { background:#e3f2fd; color:#1565c0; }
  .grade-fail  { background:#fce4ec; color:#c62828; }
  .admin-hdr {
    background: linear-gradient(90deg,#0f3460,#533483);
    color:white; padding:1rem 1.5rem; border-radius:10px; margin-bottom:1.2rem;
  }
  .prog-lbl { font-size:.82rem; color:#666; margin-bottom:.25rem; }
  [data-testid="metric-container"] {
    background:#f8faff; border:1px solid #e0e7ff; border-radius:12px; padding:.9rem;
  }
  .sg-tbl { width:100%; border-collapse:collapse; font-size:.88rem; margin:.4rem 0 1rem; }
  .sg-tbl th { background:#0f3460; color:white; padding:.5rem .8rem; text-align:left; }
  .sg-tbl td { padding:.45rem .8rem; border-bottom:1px solid #e8eaf6; vertical-align:top; }
  .sg-tbl tr:nth-child(even) td { background:#f5f7ff; }
  .sg-tbl tr:hover td { background:#e8f0fe; }
</style>
""", unsafe_allow_html=True)

CSV_FILE = "quiz_results.csv"

# ─────────────────────────────────────────────────────────────────────
# QUIZ DATA
# ─────────────────────────────────────────────────────────────────────
QUESTIONS = [
    {
        "id": 1, "concept": "Chief Complaint – Dizziness",
        "question": (
            "According to Chapter 1, dizziness as a neurological chief complaint can represent "
            "three distinct clinical entities. Which pairing is CORRECT?"
        ),
        "options": [
            "Vertigo — light-headedness resulting from cerebral hypoperfusion",
            "Presyncope — the illusion of movement of oneself or the environment",
            "Imbalance — unsteadiness due to extrapyramidal, vestibular, cerebellar, or sensory deficits",
            "Ataxia — loss of power from disorders affecting motor pathways",
        ],
        "answer": "Imbalance — unsteadiness due to extrapyramidal, vestibular, cerebellar, or sensory deficits",
        "explanation": (
            "Chapter 1 defines dizziness as three phenomena: (1) Vertigo — illusion of movement of "
            "oneself or the environment; (2) Imbalance — unsteadiness due to extrapyramidal, vestibular, "
            "cerebellar, or sensory deficits; (3) Presyncope — light-headedness from cerebral hypoperfusion. "
            "Option A swaps vertigo with presyncope; Option B swaps presyncope with vertigo; "
            "Option D (ataxia) is not listed as one of the three meanings of dizziness."
        ),
    },
    {
        "id": 2, "concept": "Vital Signs – Orthostatic Hypotension",
        "question": (
            "Which blood pressure change upon moving from recumbent to upright posture defines "
            "orthostatic hypotension according to Chapter 1?"
        ),
        "options": [
            "Systolic drop >= 10 mm Hg OR diastolic drop >= 5 mm Hg",
            "Systolic drop >= 20 mm Hg OR diastolic drop >= 10 mm Hg",
            "Systolic drop >= 30 mm Hg OR diastolic drop >= 15 mm Hg",
            "Any systolic drop accompanied by a compensatory rise in heart rate",
        ],
        "answer": "Systolic drop >= 20 mm Hg OR diastolic drop >= 10 mm Hg",
        "explanation": (
            "Chapter 1: orthostatic hypotension = drop of >= 20 mm Hg (systolic) OR >= 10 mm Hg "
            "(diastolic) on standing. A compensatory heart-rate rise implies intact sympathetic reflexes "
            "(likely hypovolemia); absent compensation suggests autonomic dysfunction or sympatholytic drugs."
        ),
    },
    {
        "id": 3, "concept": "UMN vs LMN Lesions",
        "question": (
            "A patient has hyperactive tendon reflexes, increased muscle tone, and a Babinski sign. "
            "Which localisation best explains this picture?"
        ),
        "options": [
            "Lower motor neuron (anterior horn cell or peripheral nerve) lesion",
            "Neuromuscular junction disorder",
            "Upper motor neuron (central nervous system) lesion",
            "Primary myopathy",
        ],
        "answer": "Upper motor neuron (central nervous system) lesion",
        "explanation": (
            "Chapter 1: UMN lesions cause increased tone, hyperreflexia, and Babinski sign. "
            "LMN lesions cause decreased tone, hyporeflexia, atrophy, and fasciculations. "
            "UMN lesions affect the brain or spinal cord above the anterior horn cell."
        ),
    },
    {
        "id": 4, "concept": "Aphasia Syndromes",
        "question": (
            "A patient produces fluent but meaningless speech with paraphasic errors, cannot understand "
            "language, and cannot repeat phrases. According to Table 1-1 in Chapter 1, this is:"
        ),
        "options": [
            "Expressive (Broca) aphasia",
            "Receptive (Wernicke) aphasia",
            "Conduction aphasia",
            "Anomic aphasia",
        ],
        "answer": "Receptive (Wernicke) aphasia",
        "explanation": (
            "Table 1-1: Receptive (Wernicke) aphasia = Fluency PRESERVED, Comprehension IMPAIRED, "
            "Repetition IMPAIRED. Speech is voluminous but meaningless with paraphasias and neologisms. "
            "Broca = non-fluent + intact comprehension. Conduction = intact fluency and comprehension "
            "but impaired repetition. Anomic = all three preserved except naming."
        ),
    },
    {
        "id": 5, "concept": "Muscle Strength Grading (0–5 Scale)",
        "question": "On the standard muscle-strength grading scale in Chapter 1, grade 3 means:",
        "options": [
            "Decreased strength but can move against gravity plus added resistance",
            "Able to move against gravity but not against added resistance",
            "Able to move only with gravity eliminated (horizontal plane only)",
            "Flicker of movement with no joint motion",
        ],
        "answer": "Able to move against gravity but not against added resistance",
        "explanation": (
            "Scale: 5 = normal; 4 = moves vs gravity + resistance; 3 = moves vs gravity only; "
            "2 = horizontal movement (gravity eliminated); 1 = flicker; 0 = no contraction. "
            "Grade 3 means the limb lifts against gravity but is overcome by any examiner resistance."
        ),
    },
    {
        "id": 6, "concept": "Meningeal Signs",
        "question": (
            "Passive neck flexion causes involuntary hip and knee flexion in a supine patient. "
            "This classic meningeal sign is called:"
        ),
        "options": ["Kernig sign", "Lasegue sign", "Brudzinski sign", "Babinski sign"],
        "answer": "Brudzinski sign",
        "explanation": (
            "Chapter 1 (Fig 1-5): Brudzinski sign = involuntary hip/knee flexion on passive neck flexion, "
            "indicating meningeal irritation from meningitis or subarachnoid haemorrhage. "
            "Kernig = resistance to knee extension with hip flexed. Lasegue = radicular pain on "
            "straight-leg raise. Babinski = extensor plantar response (UMN sign)."
        ),
    },
    {
        "id": 7, "concept": "Papilledema",
        "question": "Which statement about papilledema is CORRECT according to Chapter 1?",
        "options": [
            "Typically unilateral; causes significant early visual acuity loss",
            "Results from optic nerve atrophy; associated with multiple sclerosis",
            "Almost always bilateral; does not impair vision except for blind-spot enlargement; not painful",
            "In fully developed papilledema, venous pulsations are readily visible and disk margins are sharp",
        ],
        "answer": "Almost always bilateral; does not impair vision except for blind-spot enlargement; not painful",
        "explanation": (
            "Chapter 1: Papilledema is almost always bilateral, does not typically impair vision except "
            "for enlargement of the blind spot, and is not painful. It results from raised ICP transmitted "
            "to the optic nerve sheath. Optic disk pallor is the sign of optic nerve atrophy in MS."
        ),
    },
    {
        "id": 8, "concept": "Classic Gait Abnormalities",
        "question": "Which description correctly matches the hemiplegic gait in Chapter 1?",
        "options": [
            "Wide-based, staggering gait resembling drunkenness — cerebellar disease",
            "Slow scissoring gait with legs crossing — bilateral pyramidal disease",
            "High-stepping with foot slap — foot drop from peroneal nerve lesion",
            "Leg extended and internally rotated, foot inverted/plantar-flexed, circumduction at hip",
        ],
        "answer": "Leg extended and internally rotated, foot inverted/plantar-flexed, circumduction at hip",
        "explanation": (
            "Chapter 1 (Fig 1-25): Hemiplegic gait — affected leg extended and internally rotated, "
            "foot inverted and plantar-flexed, swinging in a semicircle (circumduction) at the hip. "
            "Seen after unilateral hemispheric stroke. Option A = cerebellar; Option B = paraplegic; "
            "Option C = steppage gait from foot drop."
        ),
    },
    {
        "id": 9, "concept": "Time Course as Etiologic Clue",
        "question": (
            "According to the diagnostic formulation in Chapter 1, which disease category "
            "typically causes neurologic symptoms evolving within minutes?"
        ),
        "options": [
            "Neoplastic and degenerative disorders",
            "Inflammatory and metabolic disorders",
            "Ischemia, seizure, or syncope",
            "Infectious and autoimmune disorders",
        ],
        "answer": "Ischemia, seizure, or syncope",
        "explanation": (
            "Chapter 1: Only a few processes produce neurologic symptoms that evolve within minutes — "
            "typically ischemia, seizure, or syncope. Neoplastic/degenerative = progressive unremitting. "
            "Inflammatory/metabolic = may wax and wane. MS = relapses and remissions."
        ),
    },
    {
        "id": 10, "concept": "Sensory Pathway Localisation",
        "question": (
            "Chapter 1 states that which sensory modalities are carried specifically by the "
            "large-fibre pathway in the posterior columns and medial lemniscus?"
        ),
        "options": [
            "Pain and temperature",
            "Vibration and position (joint) sense",
            "Light touch only",
            "Pain, temperature, and crude touch",
        ],
        "answer": "Vibration and position (joint) sense",
        "explanation": (
            "Chapter 1: Large fibres in posterior columns/medial lemniscus carry vibration + position sense. "
            "Small fibres in spinothalamic tracts carry pain + temperature. "
            "Light touch is conveyed by BOTH pathways. Posterior column lesion (e.g., B12 deficiency) "
            "spares pain/temperature; spinothalamic lesion spares vibration/proprioception."
        ),
    },
]

# ─────────────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "active_tab": "study",
        "name": "", "student_id": "",
        "logged_in": False,
        "current_q": 0, "answers": [],
        "submitted": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ─────────────────────────────────────────────────────────────────────
# CSV HELPERS
# ─────────────────────────────────────────────────────────────────────
def save_result(name, sid, answers):
    score = sum(1 for i, q in enumerate(QUESTIONS)
                if i < len(answers) and answers[i] == q["answer"])
    grade = round(score / len(QUESTIONS) * 100)
    row = {"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
           "name": name, "student_id": sid, "score": score, "grade": grade}
    for i, q in enumerate(QUESTIONS):
        row[f"q{i+1}_correct"] = 1 if (i < len(answers) and answers[i] == q["answer"]) else 0
    df_new = pd.DataFrame([row])
    if os.path.exists(CSV_FILE):
        df_new.to_csv(CSV_FILE, mode="a", header=False, index=False)
    else:
        df_new.to_csv(CSV_FILE, mode="w", header=True, index=False)

def load_results():
    if not os.path.exists(CSV_FILE):
        return None
    try:
        df = pd.read_csv(CSV_FILE)
        return df if not df.empty else None
    except Exception:
        return None

def build_report(name, sid, answers):
    score = sum(1 for i, q in enumerate(QUESTIONS)
                if i < len(answers) and answers[i] == q["answer"])
    grade = round(score / len(QUESTIONS) * 100)
    lines = ["=" * 65,
             "  CLINICAL NEUROLOGY -- CHAPTER 1 QUIZ RESULT",
             "=" * 65,
             f"  Student : {name}",
             f"  ID      : {sid}",
             f"  Date    : {datetime.now().strftime('%Y-%m-%d %H:%M')}",
             f"  Score   : {score} / {len(QUESTIONS)}  |  Grade : {grade} / 100",
             "=" * 65, ""]
    for i, q in enumerate(QUESTIONS):
        ua = answers[i] if i < len(answers) else "--"
        ok = ua == q["answer"]
        lines += [f"Q{i+1}. [{q[chr(99)+chr(111)+chr(110)+chr(99)+chr(101)+chr(112)+chr(116)]}]",
                  f"   {q['question']}",
                  f"   Your Answer    : {ua}",
                  f"   Correct Answer : {q['answer']}",
                  f"   Result         : {chr(10003)+' CORRECT' if ok else chr(10007)+' INCORRECT'}",
                  f"   Explanation    : {q['explanation']}", ""]
    lines += ["=" * 65, "  End of Report", "=" * 65]
    return "\n".join(lines)

# ─────────────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────────────
def render_header():
    st.markdown("""
    <div class="main-header">
      <h1>&#129504; Clinical Neurology &#8212; Chapter 1</h1>
      <p>Neurologic History &amp; Examination &nbsp;&middot;&nbsp;
         Aminoff, Greenberg &amp; Simon, 10th Edition &nbsp;&middot;&nbsp;
         Full Learning Module</p>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────
# STUDY GUIDE
# ─────────────────────────────────────────────────────────────────────
def tab_study_guide():
    st.markdown("## &#128218; Study Guide &#8212; Chapter 1: Neurologic History & Examination")
    st.caption("Source: *Clinical Neurology*, 10th Edition, Aminoff, Greenberg & Simon. Content extracted directly from Chapter 1.")
    st.info("&#128161; **How to use:** Work through each topic, then switch to the **Quiz** tab to test yourself. You can return here at any time.", icon="&#8505;")
    st.markdown("---")

    # ── 1. History ──────────────────────────────────────────────
    with st.expander("&#128218;  1. NEUROLOGIC HISTORY — Structure & Key Complaints", expanded=True):
        st.markdown("#### History-Taking Framework")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
**History of Present Illness must cover:**
- **Quality & Severity** — character, ranking vs past problems
- **Location** — precise localisation guides anatomic diagnosis
- **Time Course** — abrupt vs insidious; improving / worsening / relapsing
- **Precipitating & Alleviating Factors**
- **Associated Symptoms** — neck pain + leg weakness → cervical myelopathy
""")
        with col2:
            st.markdown("""
**Past Medical History red flags:**
- HTN, diabetes, heart disease, cancer, HIV → neurologic complications
- Open-heart surgery → stroke or confusional state
- Pregnancy → worsens epilepsy; predisposes to pseudotumor cerebri, eclampsia
- Medications → confusion, ataxia, neuropathy, seizures
- Vitamins: B₁ deficiency → Wernicke–Korsakoff; B₁₂ → combined systems disease; B₃ → pellagra
""")
        st.markdown("#### Common Neurologic Chief Complaints — Differential Meanings")
        st.markdown("""
| Patient Word | Neurologic Meanings | Key Clarification |
|---|---|---|
| **Dizziness** | Vertigo · Imbalance · Presyncope | Ask what exactly they mean |
| **Weakness** | True motor loss | Patients may mean fatigue or sensory disturbance |
| **Numbness** | Hypesthesia · Hyperesthesia · Paraesthesia | Occasionally used to mean weakness |
| **Shaking** | Tremor · Chorea · Athetosis · Myoclonus · Fasciculation | Ask patient to demonstrate |
| **Blurred vision** | Diplopia · Oscillopsia · Reduced acuity · Visual field cut | Monocular vs binocular? |
| **Spells** | Epilepsy · Syncope | Duration, triggers, post-ictal state |
| **Confusion** | Memory impairment · Language disorder · Personality change | Seek specific examples |
""")
        st.markdown("#### Dizziness — 3 Subtypes (Critical Table)")
        st.markdown("""
| Type | Definition | Key Causes |
|---|---|---|
| **Vertigo** | Illusion of movement of oneself or the environment | Vestibular (BPPV, labyrinthitis), brainstem/cerebellar lesion |
| **Imbalance** | Unsteadiness due to extrapyramidal, vestibular, cerebellar, or sensory deficits | Parkinson, cerebellar ataxia, posterior column disease |
| **Presyncope** | Light-headedness from cerebral hypoperfusion | Orthostatic hypotension, cardiac arrhythmia, vasovagal |
""")

    # ── 2. Vital Signs ──────────────────────────────────────────
    with st.expander("&#129657;  2. VITAL SIGNS — Neurologic Significance"):
        st.markdown("""
| Vital Sign | Abnormality | Neurologic Implication |
|---|---|---|
| **Blood Pressure ↑** | Hypertension | Risk for stroke; hypertensive encephalopathy; ICH; SAH |
| **BP drop on standing** | Orthostatic hypotension (**>=20 mmHg systolic OR >=10 mmHg diastolic**) | With ↑HR → hypovolemia (intact autonomics). Without ↑HR → autonomic failure (MSA, polyneuropathy) or sympatholytic drugs |
| **Pulse irregular** | Atrial fibrillation | Cardiac cause of stroke or syncope |
| **Respiratory rate ↑** | Tachypnea | Hepatic encephalopathy, sepsis, salicylate intoxication, neuromuscular disease |
| **Cheyne-Stokes breathing** | Alternating hyperpnea & apnea | Metabolic disorders or hemispheric lesions |
| **Apneustic / Ataxic breathing** | Irregular pattern | Brainstem disorder |
| **Temperature ↑** | Fever | Meningitis, encephalitis, myelitis |
| **Temperature ↓** | Hypothermia | Ethanol/sedative intox, hypoglycemia, Wernicke encephalopathy, hypothyroidism |
""")

    # ── 3. Mental Status ─────────────────────────────────────────
    with st.expander("&#129335;  3. MENTAL STATUS EXAMINATION"):
        st.markdown("#### Level of Consciousness")
        st.markdown("""
- **Normal**: Awake + Alert (responds to visual/verbal cues) + Oriented (person, place, approximate date/time)
- **Abnormal spectrum**: Drowsiness → Delirium/Confusional state → Stupor → **Coma** (unarousable)
""")
        st.markdown("#### Memory Testing")
        st.markdown("""
| Memory Type | How Tested | Impaired In |
|---|---|---|
| **Immediate recall** | Repeat digit strings (normal = 5–7 digits) | Confusional states |
| **Recent memory** | Recall object list after 3–5 min | Amnesia (predominant involvement) |
| **Remote memory** | Personal history, historic events | Preserved until late stages of dementia |
""")
        st.markdown("#### Aphasia Syndromes (Table 1-1) — High-Yield")
        st.markdown("""
| Type | Fluency | Comprehension | Repetition | Location | Patient Insight |
|---|---|---|---|---|---|
| **Expressive (Broca)** | ❌ Impaired | ✅ Intact | ❌ Impaired | Left premotor frontal | Aware & frustrated |
| **Receptive (Wernicke)** | ✅ Preserved | ❌ Impaired | ❌ Impaired | Left posterior temporal | Usually **unaware** |
| **Global** | ❌ Impaired | ❌ Impaired | ❌ Impaired | Large left hemisphere | Variable |
| **Conduction** | ✅ Preserved | ✅ Intact | ❌ Impaired | Arcuate fasciculus | Aware |
| **Transcortical Expressive** | ❌ Impaired | ✅ Intact | ✅ **Intact** | Anterior border zone | Aware |
| **Transcortical Receptive** | ✅ Preserved | ❌ Impaired | ✅ **Intact** | Posterior border zone | Unaware |
| **Anomic** | ✅ Preserved | ✅ Intact | ✅ Intact | Variable | Aware |
""")
        st.info("**Memory tip:** Broca = Broken output (non-fluent). Wernicke = Wordy but Wrong (fluent, meaningless).", icon="&#128161;")

        st.markdown("#### Parietal Lobe Sensory Integration Signs")
        st.markdown("""
| Sign | Definition |
|---|---|
| **Astereognosis** | Cannot identify object by touch (coin, key, pin) |
| **Agraphesthesia** | Cannot identify number written on palm |
| **Extinction** | Fails to perceive bilateral simultaneous stimuli (perceived unilaterally) |
| **Neglect** | Fails to attend to one side of space or body |
| **Anosognosia** | Unaware of own neurologic deficit |
| **Constructional apraxia** | Cannot draw clock face or copy geometric figures |
""")

    # ── 4. Cranial Nerves ────────────────────────────────────────
    with st.expander("&#128065;  4. CRANIAL NERVES — Examination & Key Abnormalities"):
        st.markdown("""
| CN | Name | How to Test | Key Abnormality |
|---|---|---|---|
| **I** | Olfactory | Identify coffee/vanilla (each nostril; no alcohol) | Anosmia: frontal lesion, head trauma, neurodegeneration |
| **II** | Optic | Ophthalmoscopy · Snellen chart · Confrontation fields | Papilledema: bilateral, painless, ↑ICP. Optic pallor: atrophy (MS). Bitemporal hemianopia: pituitary. |
| **III** | Oculomotor | Pupils · Eyelids · Eye movements | CN III palsy: dilated unreactive pupil + ptosis + "down & out" eye |
| **IV** | Trochlear | Downward/inward gaze | Superior oblique weakness → diplopia on downward gaze (trouble reading/stairs) |
| **V** | Trigeminal | Touch/temp on V1/V2/V3 · Corneal reflex | Corneal reflex: afferent = V1, efferent = VII |
| **VI** | Abducens | Lateral gaze | Lateral rectus weakness → convergent squint; diplopia on lateral gaze |
| **VII** | Facial | Wrinkle forehead · Close eyes · Smile | Peripheral: whole hemiface weak (including forehead). Central: **forehead spared** |
| **VIII** | Vestibulocochlear | Rinne test · Weber test · Dix–Hallpike | Rinne: conductive = bone>air. Weber: lateralises to affected ear (conductive) or normal ear (sensorineural) |
| **IX/X** | Glossopharyngeal/Vagus | Say "ah" → palate elevation · Gag reflex | Palate deviates away from lesion |
| **XI** | Spinal Accessory | Head rotation (SCM) · Shoulder shrug (trapezius) | SCM weakness → impaired head rotation away from weak side |
| **XII** | Hypoglossal | Push tongue into cheek | Tongue deviates toward weak side; denervation → atrophy + fasciculations |
""")
        st.markdown("#### Pupillary Abnormalities (Table 1-2)")
        st.markdown("""
| Syndrome | Appearance | Light Reaction | Accommodation | Lesion Site |
|---|---|---|---|---|
| **Adie (tonic) pupil** | Unilateral large | Sluggish | Normal | Ciliary ganglion |
| **Argyll Robertson** | Bilateral small, irregular | **Absent** | **Normal** ("accommodates but won't react") | Midbrain (syphilis) |
| **Horner syndrome** | Unilateral miosis + ptosis | Normal | Normal | Sympathetic pathway |
| **Marcus Gunn (RAPD)** | Normal | Consensual > direct | Normal | Optic nerve |
| **CN III compression** | Dilated (~7mm), unreactive | Absent | Absent | CN III (compressive) |
""")

    # ── 5. Motor Function ────────────────────────────────────────
    with st.expander("&#128170;  5. MOTOR FUNCTION — Strength, Tone & UMN vs LMN"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### MRC Muscle Strength Scale (0–5)")
            st.markdown("""
| Grade | Description |
|---|---|
| **5** | Normal strength — full range vs full resistance |
| **4** | Moves against gravity + added resistance (reduced) |
| **3** | Moves against gravity ONLY — no added resistance |
| **2** | Moves only horizontally (gravity eliminated) |
| **1** | Flicker of contraction — no joint movement |
| **0** | No visible or palpable contraction |
""")
        with col2:
            st.markdown("#### UMN vs LMN Lesion Comparison")
            st.markdown("""
| Feature | UMN Lesion | LMN Lesion |
|---|---|---|
| **Tone** | Increased (spasticity/rigidity) | Decreased (flaccidity) |
| **Reflexes** | Hyperreflexia | Hyporeflexia / areflexia |
| **Plantar** | Babinski (extensor) | Flexor (normal) |
| **Atrophy** | Minimal / late | Early, prominent |
| **Fasciculations** | Absent | Present |
| **Location** | Brain / spinal cord | Ant. horn / nerve root / peripheral nerve |
""")
        st.markdown("#### Tone Patterns")
        st.markdown("""
- **Spasticity** — velocity-dependent increase → corticospinal tract disease
- **Rigidity** — constant through full ROM → **basal ganglia** disease (Parkinson)
- **Hypotonia** — decreased tone → muscle, LMN, or cerebellar disorders
- **Pyramidal weakness pattern**: UL = extensors + abductors weak; LL = flexors weak
- **Pronator drift**: arms outstretched, palms up, eyes closed → affected arm falls and pronates
""")

    # ── 6. Sensory Function ──────────────────────────────────────
    with st.expander("&#128075;  6. SENSORY FUNCTION — Pathways & Dissociated Loss"):
        st.markdown("#### Two Major Spinal Sensory Pathways")
        st.markdown("""
| Pathway | Fibre Type | Spinal Tract | Modalities | Classic Lesion |
|---|---|---|---|---|
| **Posterior columns / Medial lemniscus** | Large | Dorsal columns | **Vibration + Joint position (proprioception)** | B₁₂ deficiency, tabes dorsalis, Friedreich ataxia |
| **Spinothalamic tract** | Small | Anterolateral columns | **Pain + Temperature** | Syringomyelia, Brown-Sequard, Wallenberg syndrome |
| Both | Mixed | Both | **Light touch** | — |
""")
        st.warning("**Key concept:** Dissociated sensory loss = lesion restricted to ONE pathway. "
                   "Loss of vibration/proprioception with intact pain/temp = posterior column lesion. "
                   "Loss of pain/temp with intact vibration/proprioception = spinothalamic lesion.", icon="⚠️")
        st.markdown("#### Sensory Testing Principles")
        st.markdown("""
- Always **start distally** (toes/fingers) → proceed proximally to find upper border of deficit
- **Compare both sides** to detect lateralised deficits
- **128-Hz tuning fork** for vibration (placed on bony prominences)
- **Position sense**: displace distal phalanx up/down; patient detects with eyes closed
""")

    # ── 7. Reflexes ──────────────────────────────────────────────
    with st.expander("&#9889;  7. REFLEXES — Grading, Nerve Roots & Primitive Reflexes"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Tendon Reflex Grading (0–4)")
            st.markdown("""
| Grade | Response |
|---|---|
| **4** | Very brisk; clonus (rhythmic contractions) |
| **3** | Brisk but normal |
| **2** | Normal |
| **1** | Minimal / reduced |
| **0** | Absent |
""")
            st.markdown("#### Tendon Reflex Nerve Roots")
            st.markdown("""
| Reflex | Root |
|---|---|
| Biceps / Brachioradialis | C5–C6 |
| Triceps | C7–C8 |
| Quadriceps (patellar) | L3–L4 |
| Achilles | S1–S2 |
""")
        with col2:
            st.markdown("#### Babinski Sign (Extensor Plantar Response)")
            st.markdown("""
- **Stimulus**: firm stroke along lateral sole from heel toward great toe
- **Normal**: plantar FLEXION of toes
- **Babinski (abnormal)**: great toe **dorsiflexes** (extends) + toe fanning
- **Significance**: unequivocal sign of **corticospinal (UMN) tract** dysfunction
""")
            st.markdown("#### Primitive / Frontal Release Reflexes")
            st.markdown("""
Present in infancy → normally disappear → reappear with aging or **frontal lobe disease**:

| Reflex | Stimulus | Response |
|---|---|---|
| **Palmar grasp** | Stroke palm | Fingers grasp examiner |
| **Palmomental** | Scratch palm | Ipsilateral chin contraction |
| **Suck / Snout** | Touch/tap lips | Sucking movements / lip protrusion |
| **Glabellar (Myerson)** | Tap forehead | Persistent blinking (abnormal) |
""")

    # ── 8. Gait ──────────────────────────────────────────────────
    with st.expander("&#128694;  8. GAIT ABNORMALITIES — 10 Classic Patterns"):
        st.markdown("""
| # | Gait Type | Key Features | Cause / Lesion |
|---|---|---|---|
| 1 | **Hemiplegic** | Leg extended + internally rotated, foot inverted/plantar-flexed, circumduction | Unilateral UMN lesion (stroke) |
| 2 | **Paraplegic (Scissoring)** | Slow, stiff; legs cross in front of each other | Bilateral corticospinal disease |
| 3 | **Cerebellar Ataxic** | Wide-based, staggering, "drunk" — no worsening with eye closure | Cerebellar disease |
| 4 | **Sensory Ataxic** | Wide-based, feet slapped; patient watches feet; **Romberg positive** | Posterior column disease |
| 5 | **Steppage** | Exaggerated hip/knee lift; foot slap | Foot drop — peroneal nerve or L4–L5 |
| 6 | **Dystrophic (Waddling)** | Lordotic, waddling | Proximal myopathy |
| 7 | **Parkinsonian** | Flexed posture, small shuffling steps, reduced arm swing, festination | Basal ganglia (Parkinson) |
| 8 | **Choreic** | Jerky, lurching; few falls | Basal ganglia (Huntington, Sydenham) |
| 9 | **Apraxic** | Difficulty initiating ("glued to floor"); once started — slow shuffling; normal when lying | Frontal lobe (NPH) |
| 10 | **Antalgic** | Favours one limb to avoid weight-bearing pain | Painful leg condition |
""")
        st.info("**Romberg sign** = instability with eyes CLOSED but not OPEN → sensory (posterior column) ataxia. "
                "Cerebellar ataxia is wide-based and unsteady with eyes OPEN.", icon="ℹ️")

    # ── 9. Meningeal Signs ───────────────────────────────────────
    with st.expander("&#128308;  9. MENINGEAL SIGNS, HEAD TRAUMA SIGNS & SKIN FINDINGS"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Meningeal Irritation Signs")
            st.markdown("""
| Sign | How to Elicit | Positive Finding | Significance |
|---|---|---|---|
| **Brudzinski** | Passive neck flexion (supine) | Involuntary hip + knee flexion | Meningitis, SAH |
| **Kernig** | Hip flexed 90°, extend knee | Resistance / pain | Meningeal irritation |
| **Neck stiffness** | Passive neck flexion | Rigidity | Meningitis, SAH, cervical spondylosis |
| **Lasegue (SLR)** | Raise extended leg, supine | Radicular pain L4–S2 | Sciatic nerve / nerve root irritation |
""")
        with col2:
            st.markdown("#### Signs of Basal Skull Fracture")
            st.markdown("""
| Sign | Description |
|---|---|
| **Battle sign** | Postauricular (behind-ear) haematoma |
| **Raccoon eyes** | Bilateral periorbital haematoma |
| **Haemotympanum** | Blood behind tympanic membrane |
| **CSF otorrhoea/rhinorrhoea** | CSF leaking from ear or nose |
""")
            st.markdown("#### Key Skin Findings with Neurologic Significance")
            st.markdown("""
| Finding | Association |
|---|---|
| Petechiae | Meningococcal meningitis |
| Osler nodes / Janeway lesions | Bacterial endocarditis → stroke |
| Kayser-Fleischer rings | Wilson disease (copper deposits) |
| Jaundice | Hepatic encephalopathy |
| Hot dry skin | Anticholinergic drug intoxication |
""")

    # ── 10. Diagnostic Formulation ───────────────────────────────
    with st.expander("&#128300;  10. DIAGNOSTIC FORMULATION — Anatomic & Etiologic Diagnosis"):
        st.info("**Occam's Razor**: Always seek the single, unifying diagnosis that explains all features.", icon="&#9881;")
        st.markdown("#### Step 1 — Anatomic Diagnosis: Where Is the Lesion?")
        st.markdown("""
| Anatomic Site | Characteristic Pattern |
|---|---|
| **Cerebral hemisphere** | Contralateral motor + sensory deficits (face + arm + leg); cognitive deficits; visual field defects |
| **Brainstem** | **Crossed deficits**: ipsilateral CN palsy + contralateral limb deficits |
| **Spinal cord** | Deficits BELOW lesion level; face spared (except high cervical) |
| **Polyneuropathy** | Distal symmetric sensory loss + weakness; lower > upper limbs; areflexia |
| **Myopathy** | Proximal weakness; no sensory loss; may affect face/trunk |
""")
        st.markdown("#### Step 2 — Etiologic Diagnosis: What Is the Lesion? (Table 1-3)")
        st.markdown("""
| Category | Examples | Time Course |
|---|---|---|
| **Vascular** | Ischaemic stroke, ICH, SAH | Seconds → minutes |
| **Epileptic / Syncopal** | Seizure, vasovagal syncope | Seconds → minutes |
| **Infectious** | Bacterial meningitis, encephalitis, HIV dementia | Hours → days |
| **Inflammatory / Immune** | Multiple sclerosis, Guillain-Barre, myasthenia gravis | Days → weeks (relapsing-remitting) |
| **Metabolic** | Hypoglycaemia, hepatic encephalopathy, Wernicke | Hours → days; waxes & wanes |
| **Neoplastic** | Glioma, metastases, paraneoplastic | Weeks → months (progressive unremitting) |
| **Degenerative** | Alzheimer, Parkinson, ALS, Huntington | Months → years |
| **Toxic** | Alcohol-related, drug side effects | Variable |
| **Traumatic** | Subdural/epidural haematoma, entrapment neuropathy | Immediately post-injury |
| **Nutritional** | Wernicke (B1), combined systems disease (B12), pellagra (B3) | Subacute |
""")

    st.markdown("---")
    st.success("✅ All 10 topics reviewed! Switch to the **Quiz** tab to test your knowledge.")

# ─────────────────────────────────────────────────────────────────────
# QUIZ TAB
# ─────────────────────────────────────────────────────────────────────
def tab_quiz():
    if not st.session_state.logged_in:
        st.markdown("### &#128100; Student Identification")
        st.markdown("Enter your details below to begin the quiz. Study the material in the **Study Guide** tab first if you wish.")
        name = st.text_input("Full Name", placeholder="e.g., Sarah Johnson", key="inp_name")
        sid  = st.text_input("Student ID", placeholder="e.g., MED-2024-0042", key="inp_sid")
        c1, c2 = st.columns(2)
        c1.info(f"&#128203; **{len(QUESTIONS)} Questions**")
        c2.info("&#9200;&#65039; **No Time Limit**")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("&#128640; Begin Quiz", use_container_width=True, type="primary"):
            if not name.strip():
                st.error("Please enter your full name.")
            elif not sid.strip():
                st.error("Please enter your Student ID.")
            else:
                st.session_state.name       = name.strip()
                st.session_state.student_id = sid.strip()
                st.session_state.logged_in  = True
                st.session_state.current_q  = 0
                st.session_state.answers    = []
                st.session_state.submitted  = False
                st.session_state.active_tab = "quiz"
                st.rerun()
        return

    if st.session_state.active_tab == "results":
        render_results()
        return

    qi    = st.session_state.current_q
    q     = QUESTIONS[qi]
    total = len(QUESTIONS)

    st.markdown(f'<div class="prog-lbl">Question {qi + 1} of {total} &nbsp;&middot;&nbsp; '
                f'Student: <b>{st.session_state.name}</b></div>', unsafe_allow_html=True)
    st.progress(qi / total)

    st.markdown('<div class="q-card">', unsafe_allow_html=True)
    st.markdown(f'<span class="q-concept">&#128218; {q["concept"]}</span>', unsafe_allow_html=True)
    st.markdown(f'<div class="q-text">Q{qi + 1}. {q["question"]}</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    radio_key = f"radio_{qi}"
    if radio_key not in st.session_state:
        st.session_state[radio_key] = None

    idx = None
    if st.session_state[radio_key] and st.session_state[radio_key] in q["options"]:
        idx = q["options"].index(st.session_state[radio_key])

    selected = st.radio("Choose your answer:", options=q["options"],
                        key=radio_key, index=idx)

    if st.session_state.submitted:
        user_ans = st.session_state.answers[qi] if qi < len(st.session_state.answers) else None
        if user_ans == q["answer"]:
            st.markdown(f'<div class="fb-ok">&#9989; <b>Correct!</b><br><br>'
                        f'<b>Explanation:</b> {q["explanation"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="fb-err">&#10060; <b>Incorrect.</b> '
                        f'Correct answer: <em>{q["answer"]}</em><br><br>'
                        f'<b>Explanation:</b> {q["explanation"]}</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        is_last = qi == total - 1
        btn_lbl = "&#128202; View My Results" if is_last else "Next Question &#10145;"
        if st.button(btn_lbl, use_container_width=True, type="primary"):
            if is_last:
                save_result(st.session_state.name, st.session_state.student_id, st.session_state.answers)
                st.session_state.active_tab = "results"
            else:
                st.session_state.current_q += 1
                st.session_state.submitted  = False
            st.rerun()
    else:
        if st.button("Submit Answer &#10004;", use_container_width=True, type="primary"):
            if selected is None:
                st.warning("Please select an answer before submitting.")
            else:
                if len(st.session_state.answers) <= qi:
                    st.session_state.answers.append(selected)
                else:
                    st.session_state.answers[qi] = selected
                st.session_state.submitted = True
                st.rerun()

    with st.sidebar:
        st.markdown("### &#128202; Progress")
        answered = len(st.session_state.answers)
        correct  = sum(1 for i, a in enumerate(st.session_state.answers)
                       if i < len(QUESTIONS) and a == QUESTIONS[i]["answer"])
        st.metric("Answered", f"{answered} / {total}")
        st.metric("Correct",  correct)
        if answered > 0:
            st.metric("Running %", f"{round(correct/answered*100)}%")
        st.divider()
        st.caption(f"&#128100; {st.session_state.name}")
        st.caption(f"&#128266; {st.session_state.student_id}")
        st.divider()
        st.markdown("**Tip:** Switch to the Study Guide tab to review material at any time.")

# ─────────────────────────────────────────────────────────────────────
# RESULTS
# ─────────────────────────────────────────────────────────────────────
def render_results():
    answers = st.session_state.answers
    score   = sum(1 for i, q in enumerate(QUESTIONS)
                  if i < len(answers) and answers[i] == q["answer"])
    grade   = round(score / len(QUESTIONS) * 100)

    if grade >= 80:
        gc, gl, ge = "grade-pass",  "Distinction", "&#127942;"
    elif grade >= 60:
        gc, gl, ge = "grade-merit", "Pass",        "&#9989;"
    else:
        gc, gl, ge = "grade-fail",  "Needs Review","&#128218;"

    st.markdown("## &#128202; Your Quiz Results")
    col_g, col_m = st.columns([1, 2])
    with col_g:
        st.markdown(f"""
        <div class="grade-box {gc}">
          <div class="grade-num">{ge} {grade}</div>
          <div style="font-size:1.2rem;font-weight:600;margin-top:.5rem">{gl}</div>
          <div style="opacity:.7;font-size:.9rem">out of 100</div>
        </div>""", unsafe_allow_html=True)
    with col_m:
        st.markdown("### Summary")
        c1, c2, c3 = st.columns(3)
        c1.metric("Score",  f"{score} / {len(QUESTIONS)}")
        c2.metric("Grade",  f"{grade}%")
        c3.metric("Status", gl)
        date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        st.markdown(f"**Student:** {st.session_state.name}  \n"
                    f"**ID:** {st.session_state.student_id}  \n"
                    f"**Date:** {date_str}")

    report = build_report(st.session_state.name, st.session_state.student_id, answers)
    st.download_button("&#128229; Download Full Report (.txt)", data=report,
                       file_name=f"neuro_ch1_{st.session_state.student_id}.txt",
                       mime="text/plain", use_container_width=True)
    st.markdown("---")
    st.markdown("### &#128221; Detailed Question Review")
    rows = []
    for i, q in enumerate(QUESTIONS):
        ua = answers[i] if i < len(answers) else "—"
        ok = ua == q["answer"]
        rows.append({"Q#": f"Q{i+1}", "Concept": q["concept"],
                     "Your Answer": ua, "Correct Answer": q["answer"],
                     "Result": "Correct" if ok else "Incorrect",
                     "Explanation": q["explanation"]})
    df_r = pd.DataFrame(rows)
    def colour_row(row):
        c = "#e8f5e9" if row["Result"] == "Correct" else "#fce4ec"
        return [f"background-color:{c}"] * len(row)
    st.dataframe(df_r.style.apply(colour_row, axis=1),
                 use_container_width=True, hide_index=True, height=420)
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("&#128260; Retake Quiz", use_container_width=True):
            for k in ["current_q","answers","submitted","active_tab","logged_in","name","student_id"]:
                if k in st.session_state: del st.session_state[k]
            for i in range(len(QUESTIONS)):
                if f"radio_{i}" in st.session_state: del st.session_state[f"radio_{i}"]
            st.rerun()
    with col2:
        if st.button("&#128218; Return to Study Guide", use_container_width=True):
            st.session_state.active_tab = "study"
            st.rerun()

# ─────────────────────────────────────────────────────────────────────
# ANALYTICS TAB
# ─────────────────────────────────────────────────────────────────────
def tab_analytics():
    st.markdown("""
    <div class="admin-hdr">
      <b>&#128202; Admin Analytics Dashboard</b> — Chapter 1: Neurologic History & Examination
    </div>
    """, unsafe_allow_html=True)

    df = load_results()
    if df is None:
        st.info("No quiz results yet. Data will appear here after students complete the quiz.")
        return

    for i in range(len(QUESTIONS)):
        col = f"q{i+1}_correct"
        if col not in df.columns:
            df[col] = 0

    total_s   = len(df)
    avg_grade = round(df["grade"].mean(), 1)
    high      = int(df["grade"].max())
    low       = int(df["grade"].min())
    pass_rate = round((df["grade"] >= 60).sum() / total_s * 100, 1)

    st.markdown("#### &#127891; Class Metrics")
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Students Tested", total_s)
    m2.metric("Average Grade",   f"{avg_grade}%")
    m3.metric("Highest Grade",   f"{high}%")
    m4.metric("Lowest Grade",    f"{low}%")
    m5.metric("Pass Rate (>=60%)", f"{pass_rate}%")

    st.markdown("<br>", unsafe_allow_html=True)
    col_h, col_b = st.columns(2)

    with col_h:
        st.markdown("#### Score Distribution")
        fig_hist = px.histogram(df, x="grade", nbins=10, range_x=[0,100],
                                color_discrete_sequence=["#0f3460"],
                                labels={"grade":"Grade (%)"}, template="plotly_white")
        fig_hist.add_vline(x=avg_grade, line_dash="dash", line_color="#e94560",
                           annotation_text=f"Avg: {avg_grade}%", annotation_position="top right")
        fig_hist.update_layout(bargap=0.1, xaxis=dict(showgrid=False),
                               yaxis=dict(gridcolor="#f0f0f0"), margin=dict(t=20,b=10))
        st.plotly_chart(fig_hist, use_container_width=True)

    with col_b:
        st.markdown("#### Concept Mastery (% Correct per Question)")
        concept_data = [{"Q": f"Q{i+1}", "Concept": QUESTIONS[i]["concept"],
                         "% Correct": round(df[f"q{i+1}_correct"].mean()*100, 1)
                         if f"q{i+1}_correct" in df.columns else 0}
                        for i in range(len(QUESTIONS))]
        df_c = pd.DataFrame(concept_data)
        fig_bar = px.bar(df_c, x="Q", y="% Correct", hover_data=["Concept"],
                         color="% Correct",
                         color_continuous_scale=["#c62828","#f9a825","#2e7d32"],
                         range_color=[0,100], template="plotly_white")
        fig_bar.add_hline(y=60, line_dash="dash", line_color="#c62828",
                          annotation_text="60% pass", annotation_position="top left")
        fig_bar.update_layout(coloraxis_showscale=False,
                              yaxis=dict(range=[0,105], gridcolor="#f0f0f0"),
                              xaxis=dict(showgrid=False), margin=dict(t=20,b=10))
        st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("#### Topics Requiring Additional Teaching (< 60% correct)")
    weak = df_c[df_c["% Correct"] < 60].sort_values("% Correct")
    if weak.empty:
        st.success("All concepts above 60% — excellent performance!")
    else:
        for _, row in weak.iterrows():
            st.warning(f"**{row['Q']} — {row['Concept']}** → Only **{row['% Correct']}%** answered correctly.")

    st.markdown("---")
    st.markdown("#### Individual Student Results")
    show_cols = ["timestamp","name","student_id","score","grade"]
    st.dataframe(df[show_cols].sort_values("timestamp", ascending=False),
                 use_container_width=True, hide_index=True)
    csv_bytes = df.to_csv(index=False).encode()
    st.download_button("&#128229; Export Full Results CSV", data=csv_bytes,
                       file_name="quiz_results_export.csv", mime="text/csv")

# ─────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────
render_header()

tab_sg, tab_qz, tab_an = st.tabs([
    "&#128218;  Study Guide",
    "&#128221;  Quiz",
    "&#128202;  Admin Analytics",
])

with tab_sg:
    tab_study_guide()

with tab_qz:
    tab_quiz()

with tab_an:
    tab_analytics()
