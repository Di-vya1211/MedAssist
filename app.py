"""
MedAssist — Rural Health Companion & Intelligent Patient Management System
Features:
- Clear, modern healthcare UI with patient dashboard & registration records (Weight, Height, BMI, Blood Group)
- Intelligent patient allergy & adverse reaction tracking across all modules
- Cross-module allergy safeguards (Drug Info, Disease Info, Medical Report, Symptom Checker)
- Full voice input in ALL modules with automatic language detection (Hindi / English / Indian languages)
- Multilingual responses matching the user's spoken language with Text-to-Speech (TTS)
"""

import os
import sys
import json
import re
import traceback
import uuid
from datetime import datetime
from PIL import Image

# Ensure project directories are in sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
for sub in ["agents", "core", "patients", "reports", "voice", "disease_info_module_complete"]:
    p = os.path.join(BASE_DIR, sub)
    if p not in sys.path:
        sys.path.insert(0, p)

from dotenv import load_dotenv
load_dotenv(os.path.join(BASE_DIR, 'config', '.env'))

import streamlit as st

# Patient Authentication & Database
from patients.patient_auth import render_auth, get_patient_db, show_patient_header
from patients.patient_db import PatientDatabase
from patients.patient_profile_ui import render_patient_dashboard_tab, calculate_bmi

# Voice Service & Reusable Voice UI
import importlib
import voice.voice_service
import voice.voice_ui
import voice.voice_assistant
import voice.floating_bot
importlib.reload(voice.voice_service)
importlib.reload(voice.voice_ui)
importlib.reload(voice.voice_assistant)
importlib.reload(voice.floating_bot)
from voice.voice_service import voice_service
from voice.voice_ui import render_voice_input_widget
from voice.voice_assistant import conversational_assistant
from voice.floating_bot import render_floating_bot

# ---------------------------------------------------------------------------
# Module imports with graceful degradation
# ---------------------------------------------------------------------------
import_errors = []

# Disease Info
try:
    from disease_info_module_complete.disease_info import DiseaseInfoRetriever, format_disease_info
    DISEASE_MODULE_OK = True
except Exception as e:
    import_errors.append(f"disease_info: {str(e)}")
    DISEASE_MODULE_OK = False

# Drug Info
try:
    from agents.drug_info_agent import DrugInfoAgent 
    DRUG_MODULE_OK = True
except Exception as e:
    import_errors.append(f"drug_info_agent: {str(e)}")
    DRUG_MODULE_OK = False

# Translation
try:
    from agents.translation_agent import translate_text as agent_translate
    TRANSLATION_OK = True
except Exception as e:
    import_errors.append(f"translation_agent: {str(e)}")
    TRANSLATION_OK = False

# Voice Output (TTS)
try:
    from voice.voice_output_agent import VoiceOutputAgent
    TTS_AVAILABLE = True
except Exception as e:
    TTS_AVAILABLE = False
    print(f"[TTS] Not available: {e}")

# ═══════════════════════════════════════════════════════════════════════════
# MEDICAL TESTS DATABASE
# ═══════════════════════════════════════════════════════════════════════════
@st.cache_data
def load_medical_tests():
    """Load scraped medical test data from JSON files."""
    possible_paths = [
        os.path.join(BASE_DIR, "data", "medical_tests.json"),
        os.path.join(BASE_DIR, "scrapers", "medlineplus_medical_tests.json"),
        os.path.join(BASE_DIR, "scrapers", "medical_tests.json"),
    ]

    for path in possible_paths:
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                if isinstance(data, dict) and "tests" in data:
                    tests_list = data["tests"]
                    return {t.get("name", "").lower(): t for t in tests_list if t.get("name")}
                elif isinstance(data, list):
                    return {t.get("name", "").lower(): t for t in data if isinstance(t, dict) and t.get("name")}
                elif isinstance(data, dict):
                    return {k.lower(): v for k, v in data.items() if isinstance(v, dict)}

            except Exception as e:
                print(f"[MedicalTests] Error loading {path}: {e}")

    return {}

medical_tests_db = load_medical_tests()


def get_fallback_tests(disease_name: str, medical_tests_db: dict, min_tests: int = 8):
    """Find related tests by keyword matching if LLM returns too few."""
    if not medical_tests_db or not disease_name:
        return []

    disease_lower = disease_name.lower()
    keywords = [w for w in disease_lower.split() if len(w) > 2]
    expanded_keywords = set(keywords)
    common_medical = ['blood', 'urine', 'x-ray', 'test', 'scan', 'culture', 
                      'panel', 'count', 'function', 'level', 'screening', 'exam']
    expanded_keywords.update(common_medical)

    if 'diabetes' in disease_lower:
        expanded_keywords.update(['glucose', 'a1c', 'hba1c', 'sugar', 'insulin', 'lipid', 'kidney'])
    elif 'asthma' in disease_lower or 'lung' in disease_lower:
        expanded_keywords.update(['spirometry', 'lung', 'breath', 'pulmonary', 'peak flow', 'chest', 'x-ray'])
    elif 'heart' in disease_lower or 'cardiac' in disease_lower:
        expanded_keywords.update(['cholesterol', 'ecg', 'troponin', 'echo', 'stress', 'lipid'])
    elif 'kidney' in disease_lower or 'renal' in disease_lower:
        expanded_keywords.update(['creatinine', 'bun', 'urinalysis', 'gfr', 'protein', 'albumin'])
    elif 'liver' in disease_lower or 'hepat' in disease_lower:
        expanded_keywords.update(['bilirubin', 'alt', 'ast', 'hepatitis', 'prothrombin'])
    elif 'thyroid' in disease_lower:
        expanded_keywords.update(['tsh', 't3', 't4', 'thyroxine', 'antibody'])
    elif 'cancer' in disease_lower or 'tumor' in disease_lower:
        expanded_keywords.update(['biopsy', 'marker', 'mammography', 'colonoscopy', 'psa', 'cea'])
    elif 'blood' in disease_lower:
        expanded_keywords.update(['cbc', 'hemoglobin', 'hematocrit', 'platelet', 'wbc', 'rbc'])
    elif 'pneumonia' in disease_lower or 'chest' in disease_lower:
        expanded_keywords.update(['chest', 'x-ray', 'sputum', 'culture', 'blood', 'oxygen'])
    elif 'arthritis' in disease_lower or 'joint' in disease_lower:
        expanded_keywords.update(['rheumatoid', 'anti-ccp', 'crp', 'esr', 'ana', 'uric', 'x-ray'])

    scored_tests = []
    for test_name, test_data in medical_tests_db.items():
        score = 0
        test_text = (test_name + ' ' + 
                    str(test_data.get('description', '')) + ' ' + 
                    str(test_data.get('why_done', ''))).lower()

        for kw in expanded_keywords:
            if kw in test_text:
                score += 3

        if score > 0:
            scored_tests.append((score, test_name))

    scored_tests.sort(reverse=True)
    return [name for _, name in scored_tests[:min_tests]]


def normalize_name(s: str) -> str:
    """Normalize test name for fuzzy matching."""
    s = s.lower()
    s = re.sub(r'[()\[\]{}]', '', s)
    s = re.sub(r'[^a-z0-9]', '', s)
    return s


# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="MedAssist — Rural Health Companion",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Handle query params for test selection
query_params = st.query_params
if "selected_test" in query_params:
    raw_key = query_params["selected_test"]
    if raw_key in medical_tests_db:
        st.session_state.selected_medical_test = raw_key
    else:
        matched = False
        norm_raw = normalize_name(raw_key)
        for db_name in medical_tests_db.keys():
            norm_db = normalize_name(db_name)
            if norm_raw == norm_db or norm_raw in norm_db or norm_db in norm_raw:
                st.session_state.selected_medical_test = db_name
                matched = True
                break
        if not matched:
            st.session_state.selected_medical_test = raw_key
    del st.query_params["selected_test"]
    st.rerun()


# ---------------------------------------------------------------------------
# High-Clarity Modern Healthcare CSS Theme
# ---------------------------------------------------------------------------
st.markdown("""
<style>
    /* Main Layout & Dark Canvas */
    .stApp {
        background-color: #0b0f19;
        color: #f1f5f9;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Sleek Typography */
    h1, h2, h3, h4, h5 {
        color: #f8fafc !important;
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    p, li, span, label {
        color: #cbd5e1 !important;
    }

    /* Modern Card Styles */
    .info-card {
        background: rgba(22, 31, 51, 0.75);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 20px;
        border-radius: 14px;
        border-left: 4px solid #38bdf8;
        margin-bottom: 16px;
        backdrop-filter: blur(8px);
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.25);
    }
    .warning-card {
        background: rgba(30, 25, 20, 0.8);
        border: 1px solid rgba(245, 158, 11, 0.3);
        padding: 16px;
        border-radius: 12px;
        border-left: 4px solid #f59e0b;
        margin-bottom: 14px;
    }
    .critical-card {
        background: rgba(40, 20, 25, 0.85);
        border: 1px solid rgba(239, 68, 68, 0.4);
        padding: 18px;
        border-radius: 14px;
        border-left: 5px solid #ef4444;
        margin-bottom: 16px;
    }
    .success-card {
        background: rgba(16, 35, 25, 0.75);
        border: 1px solid rgba(16, 185, 129, 0.3);
        padding: 16px;
        border-radius: 12px;
        border-left: 4px solid #10b981;
        margin-bottom: 14px;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(15, 23, 42, 0.65);
        padding: 6px 10px;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
    .stTabs [data-baseweb="tab"], .stTabs button[role="tab"] {
        background-color: transparent !important;
        color: #94a3b8 !important;
        border-radius: 12px !important;
        padding: 8px 18px !important;
        font-weight: 600;
        font-size: 0.92rem;
        transition: all 0.25s ease-in-out;
        border: none !important;
        outline: none !important;
    }
    .stTabs [data-baseweb="tab"]:hover, .stTabs button[role="tab"]:hover {
        background-color: rgba(255, 255, 255, 0.06) !important;
        color: #f1f5f9 !important;
        border-radius: 12px !important;
    }
    .stTabs [aria-selected="true"], .stTabs button[role="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #0284c7 0%, #2563eb 100%) !important;
        color: #ffffff !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35) !important;
        border: none !important;
        outline: none !important;
    }
    .stTabs [data-baseweb="tab-highlight"],
    .stTabs [data-baseweb="tab-border"] {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
    }

    /* High-contrast Inputs */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        background-color: #131b2e !important;
        color: #f8fafc !important;
        border: 1px solid rgba(56, 189, 248, 0.25) !important;
        border-radius: 10px !important;
        padding: 12px 14px !important;
        font-size: 1rem !important;
    }
    .stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.25) !important;
    }
    .stSelectbox > div > div {
        background-color: #131b2e !important;
        color: #f8fafc !important;
        border-radius: 10px !important;
        border: 1px solid rgba(56, 189, 248, 0.25) !important;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 10px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
        padding: 8px 18px !important;
        background: #1e293b !important;
        color: #f8fafc !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2) !important;
    }
    .stButton > button:hover {
        background: #334155 !important;
        color: #38bdf8 !important;
        border-color: #38bdf8 !important;
        box-shadow: 0 4px 14px rgba(56, 189, 248, 0.25) !important;
    }
    .stButton > button p, 
    .stButton > button span, 
    .stButton > button div {
        color: inherit !important;
        font-weight: 600 !important;
    }
    .stButton > button[kind="primary"],
    .stButton > button[data-testid="stBaseButton-primary"] {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important;
        color: #ffffff !important;
        border: 1px solid #38bdf8 !important;
        box-shadow: 0 4px 14px rgba(2, 132, 199, 0.35) !important;
    }
    .stButton > button[kind="primary"]:hover,
    .stButton > button[data-testid="stBaseButton-primary"]:hover {
        background: linear-gradient(135deg, #38bdf8 0%, #0284c7 100%) !important;
        color: #ffffff !important;
        border-color: #7dd3fc !important;
        box-shadow: 0 4px 18px rgba(56, 189, 248, 0.45) !important;
    }
    .stButton > button[kind="primary"] p,
    .stButton > button[kind="primary"] span,
    .stButton > button[kind="primary"] div,
    .stButton > button[data-testid="stBaseButton-primary"] p,
    .stButton > button[data-testid="stBaseButton-primary"] span,
    .stButton > button[data-testid="stBaseButton-primary"] div {
        color: #ffffff !important;
    }
    .stButton > button[kind="secondary"],
    .stButton > button[data-testid="stBaseButton-secondary"] {
        background: #1e293b !important;
        color: #f1f5f9 !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
    }
    .stButton > button[kind="secondary"]:hover,
    .stButton > button[data-testid="stBaseButton-secondary"]:hover {
        background: #334155 !important;
        color: #38bdf8 !important;
        border-color: #38bdf8 !important;
        box-shadow: 0 4px 12px rgba(56, 189, 248, 0.25) !important;
    }
    .stButton > button[kind="secondary"] p,
    .stButton > button[kind="secondary"] span,
    .stButton > button[kind="secondary"] div,
    .stButton > button[data-testid="stBaseButton-secondary"] p,
    .stButton > button[data-testid="stBaseButton-secondary"] span,
    .stButton > button[data-testid="stBaseButton-secondary"] div {
        color: #f1f5f9 !important;
    }
    .stButton > button[kind="secondary"]:hover p,
    .stButton > button[kind="secondary"]:hover span,
    .stButton > button[kind="secondary"]:hover div,
    .stButton > button[data-testid="stBaseButton-secondary"]:hover p,
    .stButton > button[data-testid="stBaseButton-secondary"]:hover span,
    .stButton > button[data-testid="stBaseButton-secondary"]:hover div {
        color: #38bdf8 !important;
    }

    /* Expanders */
    .streamlit-expanderHeader {
        background-color: rgba(22, 31, 51, 0.6) !important;
        border-radius: 10px !important;
        color: #f8fafc !important;
        font-weight: 600 !important;
    }

    /* ========================================================
       FLOATING AI HEALTH BOT (BOTTOM-RIGHT CORNER)
       ======================================================== */
    div[data-testid="stPopover"] {
        position: fixed !important;
        bottom: 24px !important;
        right: 24px !important;
        z-index: 999999 !important;
    }
    div[data-testid="stPopover"] > button {
        display: inline-flex !important;
        align-items: center !important;
        gap: 8px !important;
        background: linear-gradient(135deg, #0284c7 0%, #2563eb 100%) !important;
        color: #ffffff !important;
        border: 2px solid #38bdf8 !important;
        border-radius: 40px !important;
        padding: 10px 20px !important;
        font-size: 0.95rem !important;
        font-weight: 700 !important;
        box-shadow: 0 8px 24px rgba(2, 132, 199, 0.45) !important;
        cursor: pointer !important;
        transition: all 0.25s ease-in-out !important;
        animation: bot-glow-pulse 2.8s infinite !important;
    }
    div[data-testid="stPopover"] > button:hover {
        background: linear-gradient(135deg, #38bdf8 0%, #0284c7 100%) !important;
        box-shadow: 0 10px 32px rgba(56, 189, 248, 0.7) !important;
        transform: translateY(-2px) scale(1.02) !important;
        border-color: #ffffff !important;
    }
    div[data-testid="stPopover"] > button p,
    div[data-testid="stPopover"] > button span,
    div[data-testid="stPopover"] > button div {
        color: #ffffff !important;
        font-weight: 700 !important;
    }
    @keyframes bot-glow-pulse {
        0% { box-shadow: 0 4px 15px rgba(2, 132, 199, 0.4); }
        50% { box-shadow: 0 8px 28px rgba(56, 189, 248, 0.75), 0 0 14px rgba(56, 189, 248, 0.5); }
        100% { box-shadow: 0 4px 15px rgba(2, 132, 199, 0.4); }
    }
    div[data-testid="stPopoverBody"] {
        width: 390px !important;
        max-width: calc(100vw - 32px) !important;
        max-height: 560px !important;
        background: #0f172a !important;
        border: 1px solid rgba(56, 189, 248, 0.4) !important;
        border-radius: 18px !important;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.8), 0 0 20px rgba(2, 132, 199, 0.25) !important;
        padding: 14px 16px !important;
    }
    div[data-testid="stPopoverBody"] .stChatMessage {
        background-color: rgba(30, 41, 59, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 12px !important;
        margin-bottom: 8px !important;
        padding: 8px 12px !important;
    }
    div[data-testid="stPopoverBody"] .stChatMessage[data-testid="chat-message-user"] {
        background-color: rgba(2, 132, 199, 0.15) !important;
        border-color: rgba(56, 189, 248, 0.3) !important;
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Session state initialization
# ---------------------------------------------------------------------------
def init_session_state():
    defaults = {
        "messages": [],
        "language": "en",  # Default to English
        "emergency_alert": False,
        "disease_input": "",
        "drug_search": "",
        "symptom_input": "",
        "disease_result": None,
        "drug_results": None,
        "drug_audio_path": None,
        "voice_chat_history": [],
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_session_state()

# ---------------------------------------------------------------------------
# Language Options
# ---------------------------------------------------------------------------
LANGUAGE_OPTIONS = [
    ("English", "en"),
    ("हिन्दी (Hindi)", "hi"),
    ("বাংলা (Bengali)", "bn"),
    ("தமிழ் (Tamil)", "ta"),
    ("తెలుగు (Telugu)", "te"),
    ("मराठी (Marathi)", "mr"),
    ("ગુજરાતી (Gujarati)", "gu"),
    ("ਪੰਜਾਬੀ (Punjabi)", "pa"),
    ("ಕನ್ನಡ (Kannada)", "kn"),
    ("മലയാളം (Malayalam)", "ml"),
    ("ଓଡ଼ିଆ (Odia)", "or"),
    ("اردو (Urdu)", "ur"),
]

def translate_content(text: str, target_lang: str = None) -> str:
    if not text:
        return text
    if not target_lang:
        target_lang = st.session_state.get("language", "en")
    if target_lang == "en" or not TRANSLATION_OK:
        return text
    try:
        return agent_translate(text, target_lang=target_lang)
    except Exception as e:
        print(f"[Translate] Error: {e}")
        return text


# ---------------------------------------------------------------------------
# Emergency detection
# ---------------------------------------------------------------------------
EMERGENCY_KEYWORDS = [
    "chest pain", "can't breathe", "cant breathe", "difficulty breathing",
    "severe bleeding", "unconscious", "unconsciousness", "heart attack",
    "stroke", "suicide", "suicidal", "poisoning", "poisoned",
    "seizure", "convulsions", "not breathing", "choking",
    "severe burn", "electrocuted", "drowning", "anaphylaxis",
    "सांस नहीं आ रही", "सीने में दर्द", "बेहोश", "खून बह रहा"
]

def detect_emergency(text: str) -> bool:
    if not text:
        return False
    text_lower = text.lower()
    return any(kw in text_lower for kw in EMERGENCY_KEYWORDS)


def is_question_query(q: str) -> bool:
    """Detect if query is a health question / sentence rather than a specific drug name."""
    if not q:
        return False
    q_lower = q.lower().strip()
    if "?" in q_lower:
        return True
    question_indicators = [
        "what", "which", "how", "why", "when", "who", "where", "can i", "should i",
        "medicine for", "medication for", "drug for", "tablets for", "tablet for", "syrup for", "pills for",
        "helps with", "used for", "treatment for", "remedy for", "cure for", "prescribed for",
        "kya", "kaun", "kaunsi", "kaun si", "dawa", "dawain", "ki dawa", "ke liye", "batao", "bataiye", "upchar", "ilaj"
    ]
    if any(ind in q_lower for ind in question_indicators):
        return True
    tokens = q_lower.split()
    if len(tokens) >= 4 and any(w in tokens for w in ["for", "with", "in", "to", "and", "is", "of", "hai", "me", "ko"]):
        return True
    return False


def extract_candidate_drugs(res: dict, query: str = "") -> list:
    """Extract distinct medicine names from FDA sources and response text."""
    drugs = []
    sources = res.get("sources", []) if isinstance(res, dict) else []
    for s in sources:
        name = s.get("drug_name", "").strip() if isinstance(s, dict) else ""
        if name:
            parts = re.split(r'\s+(?:and|&|\/|\+)\s+|,', name)
            for p in parts:
                cleaned = re.sub(r'[^a-zA-Z0-9\s\-]', '', p).strip()
                if cleaned and len(cleaned) > 2 and cleaned.lower() not in [d.lower() for d in drugs]:
                    drugs.append(cleaned.title())

    ans = res.get("answer", "") if isinstance(res, dict) else ""
    if len(drugs) < 2 and ans:
        words = re.findall(r'\b[A-Z][a-z]{3,}(?:ol|il|in|ine|an|ide|cin|zole|pam|pine|statin|pril|sartan)\b', ans)
        for w in words:
            if w.lower() not in [d.lower() for d in drugs] and w.lower() not in ["medicine", "prescription", "condition", "aspirin", "protein", "hypertension", "patient"]:
                drugs.append(w.title())

    return drugs


# ═══════════════════════════════════════════════════════════════════════════
# MAIN APP EXECUTION
# ═══════════════════════════════════════════════════════════════════════════
def main():
    # ========== 1. AUTHENTICATION ==========
    authenticated, patient_id = render_auth()
    if not authenticated:
        render_floating_bot()
        st.stop()

    db = get_patient_db()

    # Load patient profile
    patient = db.get_patient(patient_id)
    if not patient:
        st.error("Patient account not found. Please log in again.")
        st.stop()

    st.session_state.patient_profile = patient
    patient_name = patient.get("full_name") or st.session_state.get("patient_name") or "Patient"

    # Fetch recorded allergies for cross-module active safeguards
    patient_allergies = db.get_allergies(patient_id)
    critical_allergies = [a for a in patient_allergies if a.get("severity") == "Severe"]

    # ═══════════════════════════════════════════════════════════════════════════
    # TOP HEADER & CONTROLS
    # ═══════════════════════════════════════════════════════════════════════════
    top_col1, top_col2, top_col3, top_col4 = st.columns([4, 2, 1.5, 1.2])

    with top_col1:
        st.markdown(f"""
        <div style='display: flex; align-items: center; gap: 12px;'>
            <span style='font-size: 2.2rem;'>🏥</span>
            <div>
                <h2 style='margin: 0; color: #38bdf8 !important; font-size: 1.6rem;'>MedAssist</h2>
                <p style='margin: 0; color: #94a3b8; font-size: 0.85rem;'>Rural Health Companion & Allergy Protection System</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with top_col2:
        # Language Selector
        lang_idx = 0
        for i, opt in enumerate(LANGUAGE_OPTIONS):
            if opt[1] == st.session_state.get("language", "en"):
                lang_idx = i
                break
        selected_lang = st.selectbox(
            "🌐 Active Language",
            options=LANGUAGE_OPTIONS,
            format_func=lambda x: x[0],
            index=lang_idx,
            label_visibility="collapsed"
        )
        if selected_lang[1] != st.session_state.language:
            st.session_state.language = selected_lang[1]
            st.rerun()

    with top_col3:
        if st.button("🚨 EMERGENCY (108)", use_container_width=True, type="secondary"):
            st.error("🚨 EMERGENCY: Call 108 (Ambulance) or 102 immediately!")

    with top_col4:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.patient_id = None
            st.session_state.patient_name = None
            st.rerun()

    # CRITICAL ALLERGY BANNER (If severe allergies exist)
    if critical_allergies:
        crit_names = ", ".join([a.get('medicine_name') for a in critical_allergies])
        st.markdown(f"""
        <div class="critical-card" style="margin-top: 14px;">
            <div style="display:flex; align-items:center; gap: 10px;">
                <span style="font-size:1.5rem;">🚨</span>
                <div>
                    <h4 style="color:#ef4444 !important; margin:0; font-size:1rem;">ACTIVE ALLERGY SAFEGUARD: {crit_names}</h4>
                    <p style="color:#cbd5e1; margin:2px 0 0 0; font-size:0.85rem;">
                        MedAssist is actively guarding your recommendations to prevent accidental exposure to these medications.
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color: rgba(255,255,255,0.08); margin: 12px 0 18px 0;'>", unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════════════════════
    # MAIN APP TABS
    # ═══════════════════════════════════════════════════════════════════════════
    tab_profile, tab_disease, tab_drug, tab_report, tab_symptom = st.tabs([
        "🏠 Dashboard & Profile",
        "🔍 Disease Info",
        "💊 Drug Information",
        "📄 Medical Report",
        "🩺 Symptom Checker"
    ])

    # ========================== TAB 1: DASHBOARD & PROFILE ==========================
    with tab_profile:
        render_patient_dashboard_tab(patient_id, db)

    # ========================== TAB 2: DISEASE INFO ==========================
    with tab_disease:
        st.markdown("<h2 style='color:#f8fafc;'>🔍 Disease Information</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color:#94a3b8;'>Search for any disease or health condition. Learn about causes, precautions, diagnostic tests, and treatments.</p>", unsafe_allow_html=True)

        # Voice Input for Disease
        render_voice_input_widget(
            module_key="disease",
            target_state_key="disease_input",
            trigger_state_key="_trigger_disease",
            help_text="Speak disease name in Hindi or English (e.g., 'मुझे मलेरिया के बारे में बताओ' or 'Asthma')"
        )

        # Disease Search Field
        default_disease = st.session_state.get("disease_input", "")
        disease_name = st.text_input(
            "Enter disease name:",
            value=default_disease,
            placeholder="e.g., Diabetes, Asthma, Pneumonia, Arthritis, Malaria...",
            key="disease_text_field"
        )
        st.session_state.disease_input = disease_name

        col_search, _ = st.columns([1, 4])
        with col_search:
            disease_search_clicked = st.button("🔍 Search Disease", use_container_width=True, type="primary")

        # Quick Examples
        st.markdown('<p style="color:#64748b; font-size:0.85rem; margin-top:8px;">Quick examples:</p>', unsafe_allow_html=True)
        ex_cols = st.columns(5)
        disease_examples = ["Diabetes", "Asthma", "Pneumonia", "Arthritis", "Coronavirus"]
        for i, ex in enumerate(disease_examples):
            with ex_cols[i]:
                if st.button(ex, key=f"dis_ex_{ex}", use_container_width=True):
                    st.session_state.disease_input = ex
                    st.session_state._trigger_disease = True
                    st.rerun()

        # Handle Search Execution
        should_search_disease = disease_search_clicked or st.session_state.get("_trigger_disease", False)
        if should_search_disease and disease_name and disease_name.strip():
            if "_trigger_disease" in st.session_state:
                del st.session_state._trigger_disease

            if detect_emergency(disease_name):
                st.error("🚨 EMERGENCY KEYWORDS DETECTED: If experiencing severe symptoms, call 108 immediately!")

            if not DISEASE_MODULE_OK:
                st.error("❌ Disease Info module is unavailable.")
            else:
                if "disease_retriever" not in st.session_state:
                    st.session_state.disease_retriever = DiseaseInfoRetriever(top_k=5)
                retriever = st.session_state.disease_retriever

                with st.spinner(f"🔍 Searching clinical records for **{disease_name}**..."):
                    try:
                        info = retriever.get_structured_info(disease_name.strip())
                        result = format_disease_info(info)
                        st.session_state.disease_result = result
                        if "selected_medical_test" in st.session_state:
                            del st.session_state.selected_medical_test
                    except Exception as e:
                        st.error(f"Error fetching disease info: {e}")

        # Display Disease Result
        if st.session_state.get("disease_result"):
            data = st.session_state.disease_result

            # Check if disease treatment conflicts with recorded allergies!
            treatments = data.get("treatment", [])
            treatment_text = " ".join(treatments) if isinstance(treatments, list) else str(treatments)
            allergic_conflicts = []
            for allg in patient_allergies:
                m_name = (allg.get("medicine_name") or "").lower().strip()
                if m_name and m_name in treatment_text.lower():
                    allergic_conflicts.append(allg)

            if allergic_conflicts:
                for conf in allergic_conflicts:
                    st.markdown(f"""
                    <div class="critical-card">
                        <h4 style="color:#ef4444; margin:0;">⚠️ PATIENT ALLERGY WARNING FOR THIS CONDITION</h4>
                        <p style="color:#cbd5e1; margin:4px 0 0 0; font-size:0.9rem;">
                            Common treatments for {data.get('disease_name')} include <b>{conf.get('medicine_name')}</b>, but you have a recorded 
                            <b>{conf.get('severity')}</b> reaction to this drug (Symptoms: {conf.get('symptoms')}). 
                            <b>DO NOT TAKE {conf.get('medicine_name')} without consulting your doctor for an alternative!</b>
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

            # Translation if target language is not English
            if st.session_state.language != "en" and TRANSLATION_OK:
                try:
                    for key in ["description", "when_to_see_doctor"]:
                        if data.get(key) and isinstance(data[key], str):
                            data[key] = translate_content(data[key], target_lang=st.session_state.language)
                    for key in ["symptoms", "diagnostic_tests", "precautions", "treatment", "risk_factors"]:
                        if data.get(key) and isinstance(data[key], list):
                            data[key] = [translate_content(item, target_lang=st.session_state.language) for item in data[key] if isinstance(item, str)]
                except Exception as e:
                    print(f"[App] Disease translation error: {e}")

            st.markdown(f"<h3 style='color:#38bdf8; margin-top:20px;'>{data['disease_name']}</h3>", unsafe_allow_html=True)
            st.markdown(f"<p style='color:#f59e0b; font-size:0.85rem;'>Confidence: {data.get('confidence', 'HIGH').upper()}</p>", unsafe_allow_html=True)

            # Display Test Detail View if selected
            if st.session_state.get("selected_medical_test"):
                test_key = st.session_state.selected_medical_test
                test_data = medical_tests_db.get(test_key, {})

                if not test_data:
                    norm_key = normalize_name(test_key)
                    for db_name, db_data in medical_tests_db.items():
                        if norm_key in normalize_name(db_name):
                            test_data = db_data
                            test_key = db_name
                            break

                st.markdown("---")
                b_col, t_col = st.columns([1, 4])
                with b_col:
                    if st.button("← Back to Disease", key="back_to_dis_btn", use_container_width=True):
                        del st.session_state.selected_medical_test
                        st.rerun()
                with t_col:
                    disp_name = test_data.get('name', test_key.title()) if test_data else test_key.title()
                    st.markdown(f"<h3 style='color:#38bdf8; margin:0;'>🔬 {disp_name}</h3>", unsafe_allow_html=True)

                if test_data:
                    td1, td2 = st.columns(2)
                    with td1:
                        st.markdown(f"""
                        <div class="info-card" style="border-left-color: #38bdf8;">
                            <h4 style="color:#38bdf8; margin:0 0 6px 0;">📝 About Test</h4>
                            <p style="margin:0;">{test_data.get('description', 'Information not available.')}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        if test_data.get('why_done'):
                            st.markdown(f"""
                            <div class="info-card" style="border-left-color: #10b981;">
                                <h4 style="color:#10b981; margin:0 0 6px 0;">🎯 Why It's Done</h4>
                                <p style="margin:0;">{test_data.get('why_done')}</p>
                            </div>
                            """, unsafe_allow_html=True)
                    with td2:
                        if test_data.get('how_you_prepare'):
                            st.markdown(f"""
                            <div class="info-card" style="border-left-color: #f59e0b;">
                                <h4 style="color:#f59e0b; margin:0 0 6px 0;">⚠️ Preparation</h4>
                                <p style="margin:0;">{test_data.get('how_you_prepare')}</p>
                            </div>
                            """, unsafe_allow_html=True)
                        if test_data.get('normal_values'):
                            st.markdown(f"""
                            <div class="info-card" style="border-left-color: #a855f7;">
                                <h4 style="color:#a855f7; margin:0 0 6px 0;">✅ Normal Range</h4>
                                <p style="margin:0;">{test_data.get('normal_values')}</p>
                            </div>
                            """, unsafe_allow_html=True)

            # Display Disease Content Cards
            if not st.session_state.get("selected_medical_test"):
                card_configs = [
                    ("📖 Description", data.get('description', ''), "#38bdf8"),
                    ("🛡️ Precautions", data.get('precautions', []), "#10b981"),
                    ("🤒 Symptoms", data.get('symptoms', []), "#f43f5e"),
                    ("💊 Treatment Options", data.get('treatment', []), "#f59e0b"),
                    ("🩺 When to See a Doctor", data.get('when_to_see_doctor', ''), "#a855f7"),
                ]

                for i in range(0, len(card_configs), 2):
                    c1, c2 = st.columns(2)
                    title, content, color = card_configs[i]
                    with c1:
                        if isinstance(content, list):
                            content_html = "".join([f"<li style='margin-bottom:6px;'>{item}</li>" for item in content])
                            content_html = f"<ul style='margin:0;padding-left:18px;'>{content_html}</ul>"
                        else:
                            content_html = f"<p style='margin:0;'>{content}</p>"
                        st.markdown(f"""
                        <div class="info-card" style="border-left-color: {color};">
                            <h4 style="color:{color};margin:0 0 10px 0;font-size:1.1rem;">{title}</h4>
                            <div style="color:#cbd5e1;">{content_html}</div>
                        </div>
                        """, unsafe_allow_html=True)

                    if i + 1 < len(card_configs):
                        title, content, color = card_configs[i + 1]
                        with c2:
                            if isinstance(content, list):
                                content_html = "".join([f"<li style='margin-bottom:6px;'>{item}</li>" for item in content])
                                content_html = f"<ul style='margin:0;padding-left:18px;'>{content_html}</ul>"
                            else:
                                content_html = f"<p style='margin:0;'>{content}</p>"
                            st.markdown(f"""
                            <div class="info-card" style="border-left-color: {color};">
                                <h4 style="color:{color};margin:0 0 10px 0;font-size:1.1rem;">{title}</h4>
                                <div style="color:#cbd5e1;">{content_html}</div>
                            </div>
                            """, unsafe_allow_html=True)

                # Diagnostic Tests Clickable Badges
                diag_tests = data.get("diagnostic_tests", [])
                if isinstance(diag_tests, list) and diag_tests:
                    st.markdown("""
                    <div class="info-card" style="border-left-color: #6366f1; padding-bottom: 10px;">
                        <h4 style="color: #818cf8; margin: 0 0 8px 0;">🔬 Diagnostic Medical Tests</h4>
                        <p style="color: #94a3b8; font-size: 0.85rem; margin: 0;">Click any test to inspect preparation, normal ranges, and procedure:</p>
                    </div>
                    """, unsafe_allow_html=True)

                    test_cols = st.columns(2)
                    for idx, test_item in enumerate(diag_tests[:10]):
                        with test_cols[idx % 2]:
                            if st.button(f"🔬 {test_item}", key=f"diag_btn_{idx}_{test_item[:10]}", use_container_width=True):
                                st.session_state.selected_medical_test = test_item.lower().strip()
                                st.rerun()

                # Read Aloud (TTS)
                st.markdown("---")
                st.markdown("<h4 style='color:#38bdf8;'>🔊 Read Aloud / सुनकर समझें</h4>", unsafe_allow_html=True)
                if st.button("🔊 Listen to Disease Overview", key="tts_dis_btn"):
                    with st.spinner("Generating audio..."):
                        speech = f"{data.get('disease_name')}. {data.get('description')}. Precautions: {'. '.join(data.get('precautions', [])[:2])}."
                        ap = voice_service.text_to_speech(speech, lang_code=st.session_state.language, output_path="voice_disease.mp3")
                        if ap and os.path.exists(ap):
                            st.audio(ap, format="audio/mp3")

    # ========================== TAB 3: DRUG INFORMATION ==========================
    with tab_drug:
        st.markdown("<h2 style='color:#f8fafc;'>💊 Drug Information & Allergy Protection</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color:#94a3b8;'>Search medications by brand or generic name, or ask what medicine helps with symptoms. All searches are automatically cross-checked against your recorded allergies.</p>", unsafe_allow_html=True)

        # Voice Input for Drug
        render_voice_input_widget(
            module_key="drug",
            target_state_key="drug_search",
            trigger_state_key="_trigger_drug",
            help_text="Speak medicine name or report adverse reaction in Hindi or English (e.g. 'पेरासिटामोल के बारे में बताओ' or 'मुझे एस्पिरिन से एलर्जी है')",
            patient_id=patient_id,
            patient_db=db
        )

        drug_query = st.text_input(
            "Enter drug name or health question:",
            value=st.session_state.get("drug_search", ""),
            placeholder="e.g. Paracetamol, Ibuprofen, 'What medicine helps with hypertension?'...",
            key="drug_text_input"
        )
        st.session_state.drug_search = drug_query

        # Quick Examples
        st.markdown('<p style="color:#64748b; font-size:0.85rem;">Quick examples:</p>', unsafe_allow_html=True)
        dex_cols = st.columns(5)
        drug_examples = ["Paracetamol", "Ibuprofen", "Aspirin", "Metformin", "Amoxicillin"]
        for idx, ex in enumerate(drug_examples):
            with dex_cols[idx]:
                if st.button(ex, key=f"dex_{idx}", use_container_width=True):
                    st.session_state.drug_search = ex
                    st.session_state._trigger_drug = True
                    st.rerun()

        col_drug_btn, _ = st.columns([1, 4])
        with col_drug_btn:
            drug_search_btn = st.button("🔍 Search Drug", key="drug_search_action_btn", use_container_width=True, type="primary")

        should_search_drug = drug_search_btn or st.session_state.get("_trigger_drug", False)

        if should_search_drug and drug_query and drug_query.strip():
            if "_trigger_drug" in st.session_state:
                del st.session_state._trigger_drug

            if not DRUG_MODULE_OK:
                st.error("❌ Drug Info module is not available.")
            else:
                # Check if drug_query reports an adverse reaction or allergy
                try:
                    is_allg, allg_data = conversational_assistant.check_and_record_allergy_from_text(
                        drug_query, patient_id=patient_id, patient_db=db
                    )
                    if is_allg and allg_data:
                        st.markdown(f"""
                        <div style='background:rgba(239,68,68,0.15); border:1px solid #ef4444; border-radius:10px; padding:12px 16px; margin-bottom:14px;'>
                            <h4 style='color:#ef4444; margin:0;'>🛡️ ALLERGY RECORDED & SAVED: {allg_data.get('medicine_name')}</h4>
                            <p style='color:#cbd5e1; margin:4px 0 0 0; font-size:0.9rem;'>
                                Severity: <b>{allg_data.get('severity')}</b> | Symptoms: <b>{allg_data.get('symptoms')}</b>.<br>
                                MedAssist has permanently stored this reaction in your health profile and will strictly avoid this drug in future recommendations.
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                        patient_allergies = db.get_allergies(patient_id)
                except Exception as e:
                    print(f"[DrugTab] Allergy check notice: {e}")

                if "drug_agent" not in st.session_state:
                    st.session_state.drug_agent = DrugInfoAgent()

                with st.spinner(f"Analyzing drug database for '{drug_query}'..."):
                    try:
                        # Pass updated patient allergies into drug agent!
                        drug_res = st.session_state.drug_agent.answer(drug_query, patient_allergies=patient_allergies)
                        st.session_state.drug_results = drug_res
                    except Exception as e:
                        st.error(f"Error fetching drug info: {e}")

        # Display Drug Result
        if st.session_state.get("drug_results"):
            res = st.session_state.drug_results
            is_query_a_question = is_question_query(drug_query)
            candidate_drugs = extract_candidate_drugs(res, drug_query) if is_query_a_question else []

            # Allergy Cross-Checking:
            if not is_query_a_question:
                # Specific drug searched (e.g. "Paracetamol", "Aspirin")
                is_allg, allg_data = db.check_drug_allergy(patient_id, drug_query)
                if is_allg and allg_data:
                    sev = allg_data.get("severity", "Moderate")
                    sym = allg_data.get("symptoms", "Adverse reaction")
                    st.markdown(f"""
                    <div class="critical-card" style="margin-top: 16px;">
                        <h3 style="color:#ef4444 !important; margin:0 0 6px 0;">🚨 CRITICAL ALLERGY ALERT FOR {drug_query.upper()}</h3>
                        <p style="color:#ffffff; font-size:1.05rem; margin:0 0 6px 0; font-weight:600;">
                            {patient_name}, you have a documented <u>{sev.upper()}</u> allergy/adverse reaction to this medication!
                        </p>
                        <p style="color:#cbd5e1; margin:0; font-size:0.9rem;">
                            <b>Reported Symptoms:</b> {sym} • <b>Recorded on:</b> {str(allg_data.get('reaction_date', ''))[:10]}
                        </p>
                        <p style="color:#fca5a5; margin:6px 0 0 0; font-size:0.85rem;">
                            ⚠️ <b>DO NOT TAKE THIS MEDICINE.</b> Please consult your doctor to prescribe an alternative treatment.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                # Question asked (e.g. "What medicine helps with hypertension?")
                # Cross-check each recommended candidate drug against patient's allergies!
                flagged_conflicts = []
                for cand in candidate_drugs:
                    is_cand_allg, cand_data = db.check_drug_allergy(patient_id, cand)
                    if is_cand_allg and cand_data:
                        flagged_conflicts.append((cand, cand_data))

                if flagged_conflicts:
                    for cand_name, cand_info in flagged_conflicts:
                        sev = cand_info.get("severity", "Moderate")
                        sym = cand_info.get("symptoms", "Adverse reaction")
                        st.markdown(f"""
                        <div class="critical-card" style="margin-top: 16px;">
                            <h3 style="color:#ef4444 !important; margin:0 0 6px 0;">🚨 ALLERGY ALERT: RECOMMENDED MEDICINE '{cand_name.upper()}' IS CONTRAINDICATED</h3>
                            <p style="color:#ffffff; font-size:1.02rem; margin:0 0 4px 0; font-weight:600;">
                                {patient_name}, one of the medications recommended above (<b>{cand_name}</b>) is in your recorded allergy profile!
                            </p>
                            <p style="color:#cbd5e1; margin:0; font-size:0.9rem;">
                                <b>Severity:</b> {sev.upper()} • <b>Reported Symptoms:</b> {sym}
                            </p>
                            <p style="color:#fca5a5; margin:6px 0 0 0; font-size:0.85rem;">
                                ⚠️ <b>DO NOT TAKE {cand_name.upper()}.</b> Please ask your doctor for a non-allergic alternative.
                            </p>
                        </div>
                        """, unsafe_allow_html=True)

            ans_text = res.get("answer", "No details found.")
            if st.session_state.language != "en" and TRANSLATION_OK:
                ans_text = translate_content(ans_text, target_lang=st.session_state.language)

            st.session_state.drug_answer_text = ans_text

            st.markdown(f"""
            <div class="info-card" style="border-left-color: #38bdf8; margin-top: 16px;">
                <h4 style="color:#38bdf8; margin:0 0 10px 0;">📋 Medication Summary</h4>
                <p style="line-height:1.7; margin:0; white-space:pre-wrap;">{ans_text}</p>
            </div>
            """, unsafe_allow_html=True)

            # Sources
            sources = res.get("sources", [])
            if sources:
                st.markdown("<p style='color:#64748b; font-size:0.85rem;'>📚 FDA Sources: " + ", ".join([s.get("drug_name", "FDA") for s in sources[:5]]) + "</p>", unsafe_allow_html=True)

            # ═════════════════════════════════════════════════════════════════
            # REPORT ADVERSE REACTION / ALLERGY AFTER TAKING THIS MEDICINE
            # ═════════════════════════════════════════════════════════════════
            st.markdown("---")
            expander_title = (
                "⚡ Faced an allergy or side effect from any of these recommended medicines? Record it here"
                if is_query_a_question else
                f"⚡ Faced an allergy or side effect from {drug_query}? Record it here to safeguard future recommendations"
            )

            with st.expander(expander_title, expanded=False):
                if is_query_a_question:
                    st.markdown("""
                    <p style='color:#94a3b8; font-size:0.85rem;'>
                        If you took one of the medicines recommended above and experienced an allergy, rash, or side effect, 
                        select the specific medicine below so MedAssist remembers it and avoids it in all future recommendations.
                    </p>
                    """, unsafe_allow_html=True)

                    drug_options = candidate_drugs + ["Other (Type custom drug name)..."] if candidate_drugs else ["Type drug name below..."]
                    selected_opt = st.selectbox(
                        "Which medicine caused you an allergy / side effect?",
                        options=drug_options,
                        key="adv_drug_select"
                    )

                    if "Other" in selected_opt or "Type drug name" in selected_opt:
                        chosen_drug_name = st.text_input("Enter the exact medicine name:", placeholder="e.g. Lisinopril, Amlodipine...", key="adv_custom_drug").strip()
                    else:
                        chosen_drug_name = selected_opt.strip()
                else:
                    st.markdown(f"<p style='color:#94a3b8; font-size:0.85rem;'>If you took <b>{drug_query}</b> and faced any allergy, rash, vomiting, or adverse reaction, save it here. MedAssist will remember it forever and alert you in all future searches and reports.</p>", unsafe_allow_html=True)
                    chosen_drug_name = drug_query.strip()

                rf1, rf2 = st.columns(2)
                with rf1:
                    adv_sev = st.selectbox("Reaction Severity", ["Severe", "Moderate", "Mild"], index=1, key="adv_sev_select_box")
                    adv_type = st.selectbox("Type of Reaction", ["Allergy", "Side Effect", "Toxic Reaction", "Ineffective"], key="adv_type_select_box")
                with rf2:
                    adv_symp = st.text_input("Symptoms Faced", placeholder="e.g. Skin rash, facial swelling, nausea, breathing difficulty...", key="adv_sym_input_box")
                    adv_onset = st.number_input("Onset Time (Hours after taking)", min_value=0, max_value=72, value=1, key="adv_time_number_box")

                adv_desc = st.text_area("Detailed Experience / Notes", placeholder="Describe how you felt, if you required emergency care, etc.", key="adv_desc_text_area")

                btn_label = f"🛡️ Save Allergy Record for {chosen_drug_name}" if chosen_drug_name else "🛡️ Save Allergy Record"
                if st.button(btn_label, key="save_adv_btn_action", type="primary"):
                    if not chosen_drug_name:
                        st.warning("Please specify or select the medicine name that caused the allergy.")
                    else:
                        ok, save_msg = db.add_allergy(
                            patient_id=patient_id,
                            medicine_name=chosen_drug_name.strip(),
                            severity=adv_sev,
                            symptoms=adv_symp.strip() or "Allergic adverse reaction",
                            notes=adv_desc.strip() or f"Reported {adv_type} reaction"
                        )
                        if ok:
                            st.success(f"✅ Record saved! MedAssist will now keep in mind your allergy to **{chosen_drug_name}** and recommend alternatives in the future.")
                            st.rerun()
                        else:
                            st.error(f"Failed to save: {save_msg}")

            # Read Aloud
            st.markdown("<h4 style='color:#38bdf8;'>🔊 Read Aloud</h4>", unsafe_allow_html=True)
            if st.button("🔊 Listen to Drug Summary", key="tts_drug_btn"):
                with st.spinner("Generating speech..."):
                    ap = voice_service.text_to_speech(ans_text[:350], lang_code=st.session_state.language, output_path="voice_drug.mp3")
                    if ap and os.path.exists(ap):
                        st.audio(ap, format="audio/mp3")

    # ========================== TAB 4: MEDICAL REPORT ==========================
    with tab_report:
        st.markdown("<h2 style='color:#f8fafc;'>📄 Medical Report Analyzer</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color:#94a3b8;'>Upload your blood test, pathology, or discharge report (PDF or Image). We extract values, explain them simply in Hindi or English, and check for any medicine allergy conflicts.</p>", unsafe_allow_html=True)

        # Voice input for report questions
        render_voice_input_widget(
            module_key="report",
            target_state_key="report_voice_query",
            help_text="Speak any question about your report in Hindi or English"
        )

        uploaded_report = st.file_uploader("Upload Medical Report (PDF, JPG, PNG, WEBP)", type=["pdf", "png", "jpg", "jpeg", "webp"])

        if uploaded_report is not None:
            temp_path = os.path.join(BASE_DIR, f"temp_{uploaded_report.name}")
            with open(temp_path, "wb") as f:
                f.write(uploaded_report.getbuffer())

            with st.spinner("📖 Extracting text and analyzing report..."):
                try:
                    from reports.report_analyzer import extract_from_pdf, extract_from_image, get_structured_analysis

                    if uploaded_report.name.lower().endswith(".pdf"):
                        raw_report_text = extract_from_pdf(temp_path)
                    else:
                        raw_report_text = extract_from_image(temp_path)

                    if raw_report_text.startswith("PDF extraction error") or raw_report_text.startswith("OCR error"):
                        st.error(raw_report_text)
                    elif len(raw_report_text) < 20:
                        st.warning("Could not clearly read text from the file. Please upload a clearer image or document.")
                    else:
                        # Analyze with patient profile & allergies injected!
                        analysis = get_structured_analysis(
                            raw_report_text,
                            language=st.session_state.language,
                            patient_allergies=patient_allergies,
                            patient_profile=patient
                        )

                        # Check if any recommendations mention allergic drugs
                        rec_str = " ".join(analysis.get("recommendations", []))
                        report_allergy_matches = []
                        for allg in patient_allergies:
                            m_name = (allg.get("medicine_name") or "").lower().strip()
                            if m_name and m_name in rec_str.lower():
                                report_allergy_matches.append(allg)

                        if report_allergy_matches:
                            for c in report_allergy_matches:
                                st.markdown(f"""
                                <div class="critical-card">
                                    <h4 style="color:#ef4444; margin:0;">⚠️ ALLERGY ALERT IN REPORT RECOMMENDATIONS</h4>
                                    <p style="color:#cbd5e1; margin:4px 0 0 0; font-size:0.9rem;">
                                        Common medications for findings in this report include <b>{c.get('medicine_name')}</b>, but you have a recorded 
                                        <b>{c.get('severity')}</b> allergy to it! Inform your doctor to prescribe a safe alternative.
                                    </p>
                                </div>
                                """, unsafe_allow_html=True)

                        # Summary
                        st.markdown(f"""
                        <div class="info-card" style="border-left-color: #38bdf8;">
                            <h4 style="color:#38bdf8; margin:0 0 8px 0;">📝 Report Summary</h4>
                            <p style="margin:0; font-size:1.05rem; line-height:1.6;">{analysis.get('summary', 'Report analyzed.')}</p>
                        </div>
                        """, unsafe_allow_html=True)

                        # Extracted Values
                        vals = analysis.get("values_found", {})
                        if vals:
                            st.markdown("<h4 style='color:#f8fafc;'>📊 Extracted Test Values</h4>", unsafe_allow_html=True)
                            v_cols = st.columns(min(4, len(vals)))
                            for i, (k, v) in enumerate(vals.items()):
                                with v_cols[i % len(v_cols)]:
                                    st.markdown(f"""
                                    <div style='background:#161f33; padding:12px; border-radius:10px; border:1px solid rgba(255,255,255,0.08); text-align:center; margin-bottom:10px;'>
                                        <p style='color:#94a3b8; font-size:0.75rem; margin:0; text-transform:uppercase;'>{k}</p>
                                        <p style='color:#38bdf8; font-size:1.25rem; font-weight:700; margin:2px 0 0 0;'>{v}</p>
                                    </div>
                                    """, unsafe_allow_html=True)

                        # Problems Found
                        probs = analysis.get("problems", [])
                        if probs:
                            st.markdown("<h4 style='color:#f8fafc;'>⚠️ Key Health Findings</h4>", unsafe_allow_html=True)
                            for p in probs:
                                st.markdown(f"""
                                <div class="warning-card">
                                    <p style="color:#f59e0b; margin:0; font-weight:600;">• {p}</p>
                                </div>
                                """, unsafe_allow_html=True)

                        # Recommendations & Diet
                        col_rec, col_diet = st.columns(2)
                        with col_rec:
                            recs = analysis.get("recommendations", [])
                            if recs:
                                st.markdown(f"""
                                <div class="info-card" style="border-left-color:#10b981;">
                                    <h4 style="color:#10b981; margin:0 0 10px 0;">✅ Recommended Actions</h4>
                                    <ul style="margin:0; padding-left:18px;">
                                        {''.join([f'<li style=\"margin-bottom:6px;\">{r}</li>' for r in recs])}
                                    </ul>
                                </div>
                                """, unsafe_allow_html=True)
                        with col_diet:
                            diet = analysis.get("diet_lifestyle", [])
                            if diet:
                                st.markdown(f"""
                                <div class="info-card" style="border-left-color:#f59e0b;">
                                    <h4 style="color:#f59e0b; margin:0 0 10px 0;">🥗 Diet & Lifestyle</h4>
                                    <ul style="margin:0; padding-left:18px;">
                                        {''.join([f'<li style=\"margin-bottom:6px;\">{d}</li>' for d in diet])}
                                    </ul>
                                </div>
                                """, unsafe_allow_html=True)

                        # When to see doctor
                        doc_text = analysis.get("when_to_see_doctor", "")
                        if doc_text:
                            st.markdown(f"""
                            <div class="info-card" style="border-left-color:#a855f7;">
                                <h4 style="color:#a855f7; margin:0 0 6px 0;">🩺 When to Consult a Doctor</h4>
                                <p style="margin:0;">{doc_text}</p>
                            </div>
                            """, unsafe_allow_html=True)

                        # Read Aloud
                        st.markdown("<h4 style='color:#38bdf8;'>🔊 Read Aloud</h4>", unsafe_allow_html=True)
                        if st.button("🔊 Listen to Report Analysis", key="tts_report_btn"):
                            with st.spinner("Generating speech..."):
                                speech_rep = f"Report summary. {analysis.get('summary', '')}. Key problems: {', '.join(probs[:2])}."
                                ap_rep = voice_service.text_to_speech(speech_rep[:350], lang_code=st.session_state.language, output_path="voice_rep.mp3")
                                if ap_rep and os.path.exists(ap_rep):
                                    st.audio(ap_rep, format="audio/mp3")

                except Exception as e:
                    st.error(f"Error analyzing report: {e}")
                    st.code(traceback.format_exc())
                finally:
                    if os.path.exists(temp_path):
                        os.remove(temp_path)

    # ========================== TAB 5: SYMPTOM CHECKER ==========================
    with tab_symptom:
        st.markdown("<h2 style='color:#f8fafc;'>🩺 Symptom Checker</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color:#94a3b8;'>Describe what symptoms you are experiencing in Hindi or English. Our model predicts possible conditions, matching confidence scores, and recommended tests while safeguarding against your drug allergies.</p>", unsafe_allow_html=True)

        # Voice Input for Symptoms
        render_voice_input_widget(
            module_key="symptoms",
            target_state_key="symptom_input",
            trigger_state_key="_trigger_symptoms",
            help_text="Speak symptoms in Hindi or English (e.g. 'मुझे 3 दिन से तेज बुखार और सिरदर्द है')"
        )

        symp_text = st.text_area(
            "Describe your symptoms:",
            value=st.session_state.get("symptom_input", ""),
            placeholder="e.g., I have had fever, dry cough, and vomiting for 2 days...",
            height=100,
            key="symp_area"
        )
        st.session_state.symptom_input = symp_text

        # Quick Add Pills
        st.markdown("<p style='color:#64748b; font-size:0.85rem;'>Quick add symptoms:</p>", unsafe_allow_html=True)
        q_cols = st.columns(5)
        for idx, sym in enumerate(["Fever", "Cough", "Headache", "Vomiting", "Stomach Pain"]):
            with q_cols[idx]:
                if st.button(sym, key=f"qsym_{idx}", use_container_width=True):
                    current = st.session_state.get("symptom_input", "")
                    st.session_state.symptom_input = f"{current}, {sym}".strip(", ")
                    st.rerun()

        col_chk_btn, _ = st.columns([1, 4])
        with col_chk_btn:
            check_symp_btn = st.button("🔍 Check Symptoms", key="chk_symp_action_btn", use_container_width=True, type="primary")

        should_check_symptoms = check_symp_btn or st.session_state.get("_trigger_symptoms", False)

        if should_check_symptoms and symp_text and symp_text.strip():
            if "_trigger_symptoms" in st.session_state:
                del st.session_state._trigger_symptoms

            with st.spinner("Analyzing symptoms and cross-referencing disease patterns..."):
                try:
                    if "symptom_checker" not in st.session_state:
                        from agents.symptom_checker_agent import SymptomCheckerAgent
                        st.session_state.symptom_checker = SymptomCheckerAgent()

                    res_sym = st.session_state.symptom_checker.predict(symp_text, language=st.session_state.language)

                    if res_sym["type"] == "emergency":
                        st.error(res_sym["message"])
                    elif res_sym["type"] == "error":
                        st.warning(res_sym["message"])
                    else:
                        st.markdown(f"""
                        <div style='background:rgba(56,189,248,0.1); border-radius:10px; padding:12px 16px; margin-bottom:16px;'>
                            <p style='color:#38bdf8; margin:0;'>
                                <b>Detected Symptoms:</b> {', '.join(res_sym.get('symptoms', []))} &nbsp;•&nbsp; 
                                <b>Duration:</b> {res_sym.get('duration', 'N/A')} days
                            </p>
                        </div>
                        """, unsafe_allow_html=True)

                        st.markdown("<h4 style='color:#f8fafc;'>📊 Possible Health Conditions</h4>", unsafe_allow_html=True)
                        for i, pred in enumerate(res_sym.get("predictions", [])[:3], 1):
                            conf = pred.get("confidence", 50)
                            color = "#ef4444" if conf >= 70 else ("#f59e0b" if conf >= 40 else "#38bdf8")

                            st.markdown(f"""
                            <div style='background:rgba(22,31,51,0.8); border:1px solid rgba(255,255,255,0.08); border-radius:12px; padding:16px; margin-bottom:12px;'>
                                <div style='display:flex; justify-content:space-between; align-items:center;'>
                                    <h5 style='color:{color}; margin:0; font-size:1.15rem;'>{i}. {pred['disease']}</h5>
                                    <span style='color:{color}; font-weight:700; font-size:1.2rem;'>{conf}%</span>
                                </div>
                                <div style='background:rgba(255,255,255,0.1); border-radius:6px; height:8px; overflow:hidden; margin:8px 0;'>
                                    <div style='background:{color}; width:{conf}%; height:100%;'></div>
                                </div>
                                <p style='color:#94a3b8; font-size:0.85rem; margin:0;'>
                                    <b>Matched:</b> {', '.join(pred.get('matched_symptoms', []))} &nbsp;•&nbsp; 
                                    <b>Urgency:</b> {pred.get('urgency', 'normal').upper()}
                                </p>
                            </div>
                            """, unsafe_allow_html=True)

                        # Read Aloud
                        st.markdown("<h4 style='color:#38bdf8;'>🔊 Read Aloud</h4>", unsafe_allow_html=True)
                        if st.button("🔊 Listen to Symptom Prediction", key="tts_sym_btn"):
                            with st.spinner("Generating speech..."):
                                top_dis = res_sym['predictions'][0]['disease'] if res_sym.get('predictions') else 'condition'
                                top_c = res_sym['predictions'][0]['confidence'] if res_sym.get('predictions') else 50
                                speech_sym = f"Symptom analysis results. Top possibility is {top_dis} with {top_c} percent confidence."
                                ap_s = voice_service.text_to_speech(speech_sym, lang_code=st.session_state.language, output_path="voice_sym.mp3")
                                if ap_s and os.path.exists(ap_s):
                                    st.audio(ap_s, format="audio/mp3")

                except Exception as e:
                    st.error(f"Error checking symptoms: {e}")

    # ═══════════════════════════════════════════════════════════════════════════
    # FOOTER
    # ═══════════════════════════════════════════════════════════════════════════
    st.markdown("<hr style='border-color: rgba(255,255,255,0.08); margin: 30px 0 16px 0;'>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: center; color: #64748b; font-size: 0.85rem;'>
        🏥 <b>MedAssist</b> — AI-powered Rural Health Companion & Adverse Reaction Safeguard © 2026<br>
        <i>Disclaimer: For informational and clinical decision support purposes only. Not a replacement for emergency healthcare or licensed physician advice.</i>
    </div>
    """, unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════════════════════
    # FLOATING AI HEALTH BOT (BOTTOM-RIGHT CORNER)
    # ═══════════════════════════════════════════════════════════════════════════
    render_floating_bot(patient_id=patient_id, patient_db=db)


if __name__ == "__main__":
    main()