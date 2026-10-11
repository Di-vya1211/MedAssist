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

# Automatically sync Streamlit Cloud Secrets into os.environ for cloud deployments
try:
    if hasattr(st, "secrets"):
        for _sec_key, _sec_val in st.secrets.items():
            if isinstance(_sec_val, str) and _sec_key not in os.environ:
                os.environ[_sec_key] = _sec_val
except Exception:
    pass

# Patient Authentication & Database
from patients.patient_auth import render_auth, get_patient_db, show_patient_header
from patients.patient_db import PatientDatabase
from patients.patient_profile_ui import render_patient_dashboard_tab, calculate_bmi

# Voice Service & Reusable Voice UI
import importlib
for _mod_name in [
    "core.llm", "core.drug_qa_backend", "agents.drug_info_agent",
    "reports.report_analyzer", "agents.translation_agent",
    "disease_info_module_complete.disease_info",
    "voice.voice_service", "voice.voice_ui", "voice.voice_assistant",
    "voice.floating_bot"
]:
    try:
        _m = importlib.import_module(_mod_name)
        importlib.reload(_m)
    except Exception as _e:
        print(f"[app] Module reload notice for {_mod_name}: {_e}")
from voice.voice_service import voice_service
from voice.voice_ui import render_voice_input_widget, render_read_aloud_widget
from voice.voice_assistant import conversational_assistant
from voice.floating_bot import render_floating_bot

# ---------------------------------------------------------------------------
# Module imports with graceful degradation
# ---------------------------------------------------------------------------
import_errors = []

# Disease Info
try:
    from disease_info_module_complete.disease_info import DiseaseInfoRetriever, format_disease_info, normalize_disease_query
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

# Wellness Hub
try:
    from wellness.wellness_ui import render_wellness_hub_tab
    WELLNESS_MODULE_OK = True
except Exception as e:
    import_errors.append(f"wellness_ui: {str(e)}")
    WELLNESS_MODULE_OK = False

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
    if not disease_name:
        return []

    norm_name = normalize_disease_query(disease_name) if 'normalize_disease_query' in globals() else disease_name
    disease_lower = f"{disease_name} {norm_name}".lower()
    keywords = [w for w in disease_lower.split() if len(w) > 2]
    expanded_keywords = set(keywords)
    common_medical = ['blood', 'urine', 'x-ray', 'test', 'scan', 'culture', 
                      'panel', 'count', 'function', 'level', 'screening', 'exam']
    expanded_keywords.update(common_medical)

    if any(k in disease_lower for k in ['diabetes', 'sugar', 'डायबिटीज', 'मधुमेह', 'glucose']):
        expanded_keywords.update(['glucose', 'a1c', 'hba1c', 'sugar', 'insulin', 'lipid', 'kidney', 'urinalysis'])
    elif any(k in disease_lower for k in ['asthma', 'lung', 'अस्थमा', 'दमा', 'respiratory']):
        expanded_keywords.update(['spirometry', 'lung', 'breath', 'pulmonary', 'peak flow', 'chest', 'x-ray'])
    elif any(k in disease_lower for k in ['heart', 'cardiac', 'कार्डियक', 'दिल']):
        expanded_keywords.update(['cholesterol', 'ecg', 'troponin', 'echo', 'stress', 'lipid'])
    elif any(k in disease_lower for k in ['kidney', 'renal', 'गुर्दा', 'किडनी']):
        expanded_keywords.update(['creatinine', 'bun', 'urinalysis', 'gfr', 'protein', 'albumin'])
    elif any(k in disease_lower for k in ['liver', 'hepat', 'लीवर', 'लिवर', 'पीलिया', 'jaundice']):
        expanded_keywords.update(['bilirubin', 'alt', 'ast', 'hepatitis', 'prothrombin', 'lft'])
    elif any(k in disease_lower for k in ['malaria', 'मलेरिया']):
        expanded_keywords.update(['malaria', 'smear', 'blood', 'platelet', 'cbc', 'parasite'])
    elif any(k in disease_lower for k in ['dengue', 'डेंगू']):
        expanded_keywords.update(['dengue', 'ns1', 'platelet', 'hematocrit', 'cbc', 'elisa'])
    elif any(k in disease_lower for k in ['typhoid', 'टाइफाइड']):
        expanded_keywords.update(['widal', 'typhidot', 'culture', 'cbc'])
    elif any(k in disease_lower for k in ['tuberculosis', 'tb', 'टीबी']):
        expanded_keywords.update(['mantoux', 'afb', 'sputum', 'x-ray', 'genexpert', 'chest'])
    elif any(k in disease_lower for k in ['anemia', 'एनीमिया', 'खून की कमी']):
        expanded_keywords.update(['hemoglobin', 'ferritin', 'iron', 'cbc', 'tibc', 'smear'])
    elif any(k in disease_lower for k in ['hypertension', 'blood pressure', 'bp', 'हाई बीपी']):
        expanded_keywords.update(['blood pressure', 'ecg', 'lipid', 'creatinine', 'urinalysis'])
    elif any(k in disease_lower for k in ['pneumonia', 'निमोनिया', 'chest']):
        expanded_keywords.update(['chest', 'x-ray', 'sputum', 'culture', 'blood', 'oxygen', 'wbc'])
    elif any(k in disease_lower for k in ['arthritis', 'गठिया', 'joint']):
        expanded_keywords.update(['rheumatoid', 'anti-ccp', 'crp', 'esr', 'ana', 'uric', 'x-ray'])
    elif any(k in disease_lower for k in ['thyroid', 'थायराइड']):
        expanded_keywords.update(['tsh', 't3', 't4', 'thyroxine', 'antibody'])
    elif any(k in disease_lower for k in ['cancer', 'tumor', 'कैंसर']):
        expanded_keywords.update(['biopsy', 'marker', 'mammography', 'colonoscopy', 'psa', 'cea'])
    elif any(k in disease_lower for k in ['blood', 'रक्त']):
        expanded_keywords.update(['cbc', 'hemoglobin', 'hematocrit', 'platelet', 'wbc', 'rbc'])

    scored_tests = []
    if medical_tests_db:
        for test_name, test_data in medical_tests_db.items():
            score = 0
            test_text = (test_name + ' ' + 
                        str(test_data.get('description', '')) + ' ' + 
                        str(test_data.get('why_done', ''))).lower()

            for kw in expanded_keywords:
                if kw in test_text:
                    score += 3

            if score > 0:
                scored_tests.append((score, test_name.title()))

    scored_tests.sort(reverse=True)
    tests = [name for _, name in scored_tests[:min_tests]]

    # Curated backup tests if database match had fewer items
    if len(tests) < min_tests:
        default_map = {
            "diabetes": ["A1C Hemoglobin Test", "Fasting Blood Glucose Test", "Oral Glucose Tolerance Test (OGTT)", "Random Plasma Glucose Test", "Urinalysis for Ketones", "Lipid Panel", "Serum Creatinine Test", "Microalbuminuria Test"],
            "asthma": ["Spirometry Test", "Peak Expiratory Flow (PEF) Test", "Fractional Exhaled Nitric Oxide (FeNO) Test", "Methacholine Challenge Test", "Chest X-Ray", "Allergy Skin Prick Testing", "Complete Blood Count", "Pulse Oximetry"],
            "pneumonia": ["Chest X-Ray", "Pulse Oximetry", "Complete Blood Count", "Blood Cultures", "Sputum Culture and Gram Stain", "CT Scan of Chest", "Arterial Blood Gas (ABG) Test", "Pleural Fluid Culture"],
            "arthritis": ["Joint X-Rays", "Rheumatoid Factor (RF) Blood Test", "Anti-CCP Antibody Test", "Erythrocyte Sedimentation Rate (ESR)", "C-Reactive Protein (CRP)", "Joint Fluid Analysis", "MRI of Joints", "Complete Blood Count"],
            "malaria": ["Malaria Rapid Diagnostic Test (RDT)", "Peripheral Blood Smear", "Complete Blood Count", "Quantitative Buffy Coat (QBC) Test", "Liver Function Tests", "Serum Bilirubin Test"],
            "dengue": ["Dengue NS1 Antigen Test", "Dengue IgM/IgG Antibody ELISA", "Complete Blood Count (Platelets)", "Liver Function Tests", "Serum Electrolyte Panel"],
            "typhoid": ["Widal Test", "Blood Culture for Salmonella", "Stool Culture and Examination", "Typhidot Rapid IgM Test", "Complete Blood Count"],
            "tuberculosis": ["Mantoux Tuberculin Skin Test (TST)", "Interferon-Gamma Release Assay (IGRA)", "Sputum Smear Microscopy (AFB)", "GeneXpert MTB/RIF Assay", "Chest X-Ray"],
            "jaundice": ["Serum Bilirubin Test (Total and Direct)", "Liver Function Tests (ALT/AST)", "Viral Hepatitis Panel", "Abdominal Ultrasound", "Complete Blood Count"],
            "anemia": ["Complete Blood Count (CBC with Hb)", "Peripheral Blood Smear", "Serum Ferritin Level", "Total Iron-Binding Capacity (TIBC)", "Vitamin B12 and Folate Levels"],
            "hypertension": ["Ambulatory Blood Pressure Monitoring (ABPM)", "Electrocardiogram (ECG)", "Echocardiogram", "Lipid Panel", "Fasting Blood Glucose", "Serum Creatinine Test"]
        }
        fallback_list = default_map.get(norm_name.lower(), [
            "Complete Blood Count (CBC)", "Comprehensive Metabolic Panel (CMP)", "Erythrocyte Sedimentation Rate (ESR)",
            "C-Reactive Protein (CRP)", "Urinalysis", "Serum Electrolyte Panel", "Diagnostic Ultrasound", "Chest X-Ray"
        ])
        for t in fallback_list:
            if t not in tests and len(tests) < min_tests:
                tests.append(t)

    return tests


def normalize_name(s: str) -> str:
    """Normalize test name for fuzzy matching."""
    s = s.lower()
    s = re.sub(r'[()\[\]{}]', '', s)
    s = re.sub(r'[^a-z0-9]', '', s)
    return s


def fetch_medical_test_details(test_name: str, disease_name: str = "") -> dict:
    """
    Fetches rich clinical details for any diagnostic test.
    Checks medical_tests_db first, then session cache, then LLM, then clinical heuristics.
    Guarantees test_data is NEVER empty.
    """
    clean_name = test_name.strip()

    # Handle non-ASCII / Hindi test names (e.g. translated badge clicks)
    lookup_name = clean_name
    if any(ord(c) > 127 for c in clean_name):
        h_map = {
            "ग्लूकोज": "glucose", "शुगर": "sugar", "ए1सी": "a1c", "फास्टिंग": "fasting",
            "रक्त": "blood", "खून": "blood", "मूत्र": "urine", "यूरिन": "urine",
            "सीबीसी": "cbc", "लिपिड": "lipid", "कोलेस्ट्रॉल": "cholesterol",
            "एक्स-रे": "x-ray", "सीटी": "ct scan", "एमआरआई": "mri",
            "अल्ट्रासाउंड": "ultrasound", "किडनी": "kidney", "क्रीटिनिन": "creatinine",
            "लीवर": "liver", "लिवर": "liver", "बिलीरुबिन": "bilirubin",
            "थायराइड": "thyroid", "ईसीजी": "ecg", "इलेक्ट्रोलाइट": "electrolyte",
            "मलेरिया": "malaria", "डेंगू": "dengue", "टाइफाइड": "typhoid", "विडाल": "widal",
            "स्पाइरोमेट्री": "spirometry", "बायोप्सी": "biopsy"
        }
        for hk, en in h_map.items():
            if hk in lookup_name:
                lookup_name = f"{lookup_name} {en}"
        if TRANSLATION_OK:
            try:
                en_trans = agent_translate(clean_name, target_lang="en")
                if en_trans and en_trans.strip():
                    lookup_name = f"{lookup_name} {en_trans.strip()}"
            except Exception:
                pass

    norm_key = normalize_name(lookup_name)

    # 1. Check medical_tests_db
    matched_data = None
    if medical_tests_db:
        if clean_name.lower() in medical_tests_db:
            matched_data = medical_tests_db[clean_name.lower()]
        elif norm_key in medical_tests_db:
            matched_data = medical_tests_db[norm_key]
        else:
            for db_name, db_data in medical_tests_db.items():
                if norm_key in normalize_name(db_name) or normalize_name(db_name) in norm_key:
                    matched_data = db_data
                    break

    if matched_data and matched_data.get("description") and matched_data.get("why_done"):
        return {
            "name": matched_data.get("name", clean_name.title()),
            "description": matched_data.get("description", "A standard diagnostic test used in medical evaluation."),
            "why_done": matched_data.get("why_done", f"Performed to assess clinical status and diagnose conditions related to {disease_name or 'the patient\'s symptoms'}."),
            "how_you_prepare": matched_data.get("how_you_prepare", "Follow all specific clinic instructions. Fasting may be necessary for blood draws."),
            "normal_values": matched_data.get("normal_values", "Results should be interpreted by your healthcare provider alongside clinical signs."),
            "procedure": matched_data.get("what_happens") or matched_data.get("procedure") or "A certified phlebotomist or clinical specialist performs the sample collection or scan following clinical guidelines.",
            "risks": matched_data.get("risks_complications") or matched_data.get("risks") or "Minimal risks: minor soreness, slight bruising, or temporary tenderness at the test site."
        }

    # 2. Check session cache
    cache_key = f"_cached_test_{normalize_name(clean_name)}"
    if cache_key in st.session_state:
        return st.session_state[cache_key]

    # 3. Query LLMClient for structured test details
    llm_test_data = None
    try:
        from core.llm import LLMClient
        llm = LLMClient()
        prompt = f"""You are a clinical laboratory medicine expert. Provide structured medical test details for:
Test Name: "{clean_name}" (Clinical concept: "{lookup_name}")
Associated Condition: "{disease_name}"

Return ONLY a valid JSON object with these exact keys:
{{
  "name": "{clean_name.title()}",
  "description": "2-3 clear sentences describing what this test evaluates and measures.",
  "why_done": "Why physicians recommend this test and what abnormalities it identifies.",
  "procedure": "Clear step-by-step description of what happens during the test procedure.",
  "how_you_prepare": "Patient preparation rules (e.g. fasting hours, water intake, medications to avoid, timing).",
  "normal_values": "Typical reference values and clinical meaning of abnormal readings.",
  "risks": "Potential risks, side effects, or minor complications associated with this test."
}}"""
        resp_text = llm.generate(prompt)
        match = re.search(r'\{.*\}', resp_text, re.DOTALL)
        if match:
            parsed = json.loads(match.group(0))
            if parsed.get("description") and parsed.get("why_done"):
                llm_test_data = parsed
    except Exception as e:
        print(f"[MedicalTest] LLM detail generation notice: {e}")

    if llm_test_data:
        st.session_state[cache_key] = llm_test_data
        return llm_test_data

    # 4. Domain-specific clinical heuristics fallback
    t_low = clean_name.lower()
    if any(k in t_low for k in ["glucose", "ogtt", "sugar", "tolerance", "a1c", "hba1c"]):
        heuristic_data = {
            "name": clean_name.title(),
            "description": "The Oral Glucose Tolerance Test (OGTT) and glucose assays evaluate how efficiently your body clears sugar from the bloodstream after fasting and glucose ingestion. It assesses pancreatic beta-cell function and insulin sensitivity.",
            "why_done": f"Diagnoses Type 2 Diabetes, Prediabetes, and Gestational Diabetes, and monitors glycemic control in patients with {disease_name or 'metabolic disorders'}.",
            "procedure": "A fasting blood sample is drawn first. You then drink a measured glucose drink (usually 75g in water), and blood samples are drawn at 1-hour and 2-hour intervals to track blood sugar levels.",
            "how_you_prepare": "Fast overnight for at least 8 to 12 hours prior to the test (water is permitted). Maintain normal carbohydrate intake for 3 days prior. Avoid strenuous exercise or smoking before the test.",
            "normal_values": "Fasting: Under 100 mg/dL (Normal). 2 Hours post-glucose: Less than 140 mg/dL (Normal); 140 to 199 mg/dL indicates Prediabetes (Impaired Glucose Tolerance); 200 mg/dL or higher indicates Diabetes.",
            "risks": "Very safe test: occasional mild nausea or stomach upset from the sweet drink, and slight bruising at the needle puncture site."
        }
    elif any(k in t_low for k in ["lipid", "cholesterol", "triglyceride", "ldl", "hdl"]):
        heuristic_data = {
            "name": clean_name.title(),
            "description": "A comprehensive lipid profile measures circulating blood fats including Total Cholesterol, High-Density Lipoprotein (HDL), Low-Density Lipoprotein (LDL), and Triglycerides.",
            "why_done": f"Evaluates cardiovascular risk, arterial plaque formation, and monitors response to statin therapy or dietary interventions for {disease_name or 'cardiac health'}.",
            "procedure": "A phlebotomist applies an elastic tourniquet around your upper arm, swabs the area with alcohol, and collects a small blood sample from a vein into a vacuum vial.",
            "how_you_prepare": "Fast for 9 to 12 hours before the blood draw (water only). Avoid alcohol for 24 hours prior. Take regular morning medications unless instructed otherwise.",
            "normal_values": "Total Cholesterol: < 200 mg/dL; LDL (Bad): < 100 mg/dL; HDL (Good): > 40 mg/dL (men), > 50 mg/dL (women); Triglycerides: < 150 mg/dL.",
            "risks": "Extremely minimal: slight pinch during needle insertion, minor localized bruising, or temporary faintness."
        }
    elif any(k in t_low for k in ["blood", "cbc", "hemoglobin", "tlc", "wbc", "platelet"]):
        heuristic_data = {
            "name": clean_name.title(),
            "description": "A Complete Blood Count (CBC) examines cellular components of the blood: red blood cells (erythrocytes), white blood cells (leukocytes), and platelets (thrombocytes).",
            "why_done": f"Screens for anemia, acute or chronic infections, systemic inflammation, bleeding disorders, and immune system status in connection with {disease_name or 'systemic illness'}.",
            "procedure": "A standard venipuncture is performed on your inner arm using a small sterile needle to draw a small vial of blood for automated hematology analyzer assessment.",
            "how_you_prepare": "Usually requires no special fasting unless performed alongside a fasting metabolic or lipid panel. Drink adequate water beforehand.",
            "normal_values": "Hemoglobin: 12.0-16.5 g/dL; WBC Count: 4,000-11,000 cells/mcL; Platelets: 150,000-450,000 cells/mcL; Hematocrit: 36%-50%.",
            "risks": "Virtually risk-free: brief stinging sensation and minor temporary bruising where the needle entered."
        }
    elif any(k in t_low for k in ["kidney", "renal", "creatinine", "bun", "urea", "gfr"]):
        heuristic_data = {
            "name": clean_name.title(),
            "description": "Renal function testing evaluates blood urea nitrogen (BUN), serum creatinine, and estimated glomerular filtration rate (eGFR) to assess kidney filtration efficacy.",
            "why_done": f"Detects acute or chronic kidney impairment, dehydration, and drug toxicity related to {disease_name or 'renal health'}.",
            "procedure": "A healthcare worker draws a routine blood sample from your arm vein. In some cases, a 24-hour urine collection sample may also be requested.",
            "how_you_prepare": "Avoid eating large portions of cooked red meat for 24 hours prior, as it can temporarily elevate creatinine levels. Stay well hydrated.",
            "normal_values": "Serum Creatinine: 0.7 to 1.3 mg/dL; Blood Urea Nitrogen (BUN): 7 to 20 mg/dL; eGFR: 90 mL/min/1.73m² or higher (Normal).",
            "risks": "Minimal: brief discomfort during blood collection and minor hematoma or soreness that fades within a day."
        }
    else:
        heuristic_data = {
            "name": clean_name.title(),
            "description": f"Standard clinical diagnostic procedure recommended to evaluate physiological status, detect abnormalities, and monitor response to treatment for {disease_name or 'the condition'}.",
            "why_done": f"Provides objective quantitative and qualitative clinical data to confirm diagnosis and optimize clinical care for {disease_name or 'the patient'}.",
            "procedure": "Carried out by certified clinical technicians following standardized aseptic hospital protocols.",
            "how_you_prepare": "Follow all preparatory instructions given by your clinic. If blood work is involved, 8-hour fasting is frequently advisable unless instructed otherwise.",
            "normal_values": "Clinical reference intervals vary by laboratory equipment and methodology. Your physician will review abnormal values in context of your overall health.",
            "risks": "Low risk under standard clinical care. Inform your physician if you have bleeding disorders or allergy to antiseptics."
        }

    st.session_state[cache_key] = heuristic_data
    return heuristic_data


# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="MedAssist — Rural Health Companion",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Handle query params for test selection and live speech input
query_params = st.query_params
if "live_voice_text" in query_params:
    import urllib.parse
    raw_v = query_params["live_voice_text"]
    v_text = urllib.parse.unquote(raw_v).strip()
    v_mod = query_params.get("live_voice_module", "disease")
    if v_text:
        if v_mod == "disease":
            st.session_state.disease_input = v_text
            st.session_state.disease_text_field = v_text
            st.session_state._trigger_disease = True
        elif v_mod == "drug":
            st.session_state.drug_search = v_text
            st.session_state.drug_text_input = v_text
            st.session_state._trigger_drug = True
        elif v_mod == "symptoms":
            st.session_state.symptom_input = v_text
            st.session_state.symp_area = v_text
            st.session_state._trigger_symptom = True
    del st.query_params["live_voice_text"]
    if "live_voice_module" in st.query_params:
        del st.query_params["live_voice_module"]
    st.rerun()

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
       FLOATING AI BOT DIALOG AS SIDE SQUARE CARD (BOTTOM-RIGHT)
       ======================================================== */
    /* 1. Backdrop / Outer Flex Container: Fullscreen, transparent, aligns content to bottom-right */
    div[data-baseweb="modal"],
    div[data-baseweb="modal"] > div,
    div[data-testid="stDialog"],
    div.stDialog,
    .e1mymz5c0 {
        position: fixed !important;
        inset: 0 !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        bottom: 0 !important;
        width: 100vw !important;
        height: 100vh !important;
        background: transparent !important;
        background-color: transparent !important;
        display: flex !important;
        align-items: flex-end !important;
        justify-content: flex-end !important;
        padding: 0 !important;
        margin: 0 !important;
        z-index: 99999999 !important;
    }

    /* 2. Inner Dialog Card: Fixed at bottom-right corner directly above the 3D bot */
    div[data-testid="stDialog"] > div,
    div.stDialog > div,
    div[role="dialog"],
    .e1mymz5c1 {
        position: fixed !important;
        bottom: 105px !important;
        right: 25px !important;
        inset: auto !important;
        top: auto !important;
        left: auto !important;
        margin: 0 !important;
        width: 410px !important;
        max-width: calc(100vw - 35px) !important;
        height: 550px !important;
        max-height: calc(100vh - 125px) !important;
        background: #0b1120 !important;
        background-color: #0b1120 !important;
        border: 2px solid #38bdf8 !important;
        border-radius: 20px !important;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.95), 0 0 30px rgba(56, 189, 248, 0.4) !important;
        overflow-y: auto !important;
        padding: 1.15rem 1.3rem !important;
        display: flex !important;
        flex-direction: column !important;
        pointer-events: auto !important;
        transform-origin: bottom right !important;
        animation: botPopupFromBot 0.35s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
    }

    /* Pop out directly from the bottom-right 3D bot */
    @keyframes botPopupFromBot {
        0% {
            opacity: 0;
            transform: scale(0.12) translateY(80px) translateX(40px);
        }
        70% {
            opacity: 1;
            transform: scale(1.03) translateY(-4px) translateX(-2px);
        }
        100% {
            opacity: 1;
            transform: scale(1) translateY(0) translateX(0);
        }
    }

    /* 3. Hide floating speech bubble when dialog is open so they do not overlap */
    body:has(div[data-testid="stDialog"]) .bot-speech-bubble,
    body:has(div.stDialog) .bot-speech-bubble,
    body:has(div[role="dialog"]) .bot-speech-bubble {
        display: none !important;
    }

    /* 4. Compact dialog header & stylish close button */
    div[data-testid="stDialog"] h2,
    div.stDialog h2,
    div[role="dialog"] h2 {
        font-size: 1.05rem !important;
        margin: 0 !important;
        padding: 0 !important;
        color: #f8fafc !important;
        font-weight: 700 !important;
    }

    div[data-testid="stDialog"] button[aria-label="Close"],
    div.stDialog button[aria-label="Close"],
    div[role="dialog"] button[aria-label="Close"],
    .e1mymz5c3 {
        color: #94a3b8 !important;
        top: 14px !important;
        right: 14px !important;
        font-size: 1.2rem !important;
        border-radius: 8px !important;
        transition: all 0.2s ease !important;
    }

    div[data-testid="stDialog"] button[aria-label="Close"]:hover,
    div.stDialog button[aria-label="Close"]:hover,
    div[role="dialog"] button[aria-label="Close"]:hover,
    .e1mymz5c3:hover {
        color: #f43f5e !important;
        background: rgba(244, 63, 94, 0.15) !important;
        transform: scale(1.1) !important;
    }

    /* 5. Custom scrollbar for the dialog card */
    div[data-testid="stDialog"] > div::-webkit-scrollbar,
    div.stDialog > div::-webkit-scrollbar,
    div[role="dialog"]::-webkit-scrollbar,
    .e1mymz5c1::-webkit-scrollbar {
        width: 6px !important;
    }
    div[data-testid="stDialog"] > div::-webkit-scrollbar-thumb,
    div.stDialog > div::-webkit-scrollbar-thumb,
    div[role="dialog"]::-webkit-scrollbar-thumb,
    .e1mymz5c1::-webkit-scrollbar-thumb {
        background: rgba(56, 189, 248, 0.3) !important;
        border-radius: 10px !important;
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
        st.stop()

    db = get_patient_db()

    # Load patient profile
    patient = db.get_patient(patient_id)
    if not patient:
        st.error("Patient account not found. Please log in again.")
        st.stop()

    st.session_state.patient_profile = patient
    patient_name = patient.get("full_name") or st.session_state.get("patient_name") or "Patient"

    # Synchronize language preference with patient registration profile
    if "language" not in st.session_state:
        pref = (patient.get("language_preference") or "English").lower()
        st.session_state.language = "hi" if "hindi" in pref else "en"

    # Fetch recorded allergies for cross-module active safeguards
    patient_allergies = db.get_allergies(patient_id)
    critical_allergies = [a for a in patient_allergies if a.get("severity") == "Severe"]

    # ═══════════════════════════════════════════════════════════════════════════
    # TOP HEADER & CONTROLS
    # ═══════════════════════════════════════════════════════════════════════════
    top_col1, top_col2, top_col_bot, top_col3, top_col4 = st.columns([3.5, 2, 1.8, 1.5, 1.2])

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
            if "floating_bot_history" in st.session_state:
                del st.session_state.floating_bot_history
            st.rerun()

    with top_col_bot:
        if st.button("🤖 AI Companion", use_container_width=True, type="primary"):
            st.session_state.floating_bot_dialog_open = True
            st.rerun()

    with top_col3:
        if st.button("🚨 EMERGENCY", use_container_width=True, type="secondary"):
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
    tab_profile, tab_disease, tab_drug, tab_report, tab_symptom, tab_wellness = st.tabs([
        "🏠 Dashboard & Profile",
        "🔍 Disease Info",
        "💊 Drug Information",
        "📄 Medical Report",
        "🩺 Symptom Checker",
        "🌿 Wellness Hub"
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
        if "disease_text_field" not in st.session_state:
            st.session_state.disease_text_field = st.session_state.get("disease_input", "")

        disease_name = st.text_input(
            "Enter disease name:",
            placeholder="e.g., Diabetes, Asthma, Pneumonia, Arthritis, Malaria...",
            key="disease_text_field"
        )
        st.session_state.disease_input = disease_name

        col_search, _ = st.columns([1, 4])
        with col_search:
            disease_search_clicked = st.button("🔍 Search Disease", use_container_width=True, type="primary")

        # Quick Examples Callback (runs before widget instantiation)
        def _set_disease_example(ex_name):
            st.session_state.disease_text_field = ex_name
            st.session_state.disease_input = ex_name
            st.session_state._trigger_disease = True

        st.markdown('<p style="color:#64748b; font-size:0.85rem; margin-top:8px;">Quick examples:</p>', unsafe_allow_html=True)
        ex_cols = st.columns(5)
        disease_examples = ["Diabetes", "Asthma", "Pneumonia", "Arthritis", "Coronavirus"]
        for i, ex in enumerate(disease_examples):
            with ex_cols[i]:
                st.button(ex, key=f"dis_ex_{ex}", on_click=_set_disease_example, args=(ex,), use_container_width=True)

        # Handle Search Execution
        should_search_disease = disease_search_clicked or st.session_state.get("_trigger_disease", False)
        effective_disease = (disease_name or st.session_state.get("disease_input", "")).strip()
        if should_search_disease and effective_disease:
            if "_trigger_disease" in st.session_state:
                del st.session_state._trigger_disease

            if detect_emergency(effective_disease):
                st.error("🚨 EMERGENCY KEYWORDS DETECTED: If experiencing severe symptoms, call 108 immediately!")

            if not DISEASE_MODULE_OK:
                st.error("❌ Disease Info module is unavailable.")
            else:
                if "disease_retriever" not in st.session_state:
                    st.session_state.disease_retriever = DiseaseInfoRetriever(top_k=5)
                retriever = st.session_state.disease_retriever

                with st.spinner(f"🔍 Searching clinical records for **{effective_disease}**..."):
                    try:
                        info = retriever.get_structured_info(effective_disease)
                        result = format_disease_info(info)

                        # Enrich diagnostic tests if too few or contains stubs
                        tests = [t for t in result.get("diagnostic_tests", []) if t and "consult" not in t.lower() and "see source" not in t.lower()]
                        if len(tests) < 6:
                            norm_dis = normalize_disease_query(effective_disease) if 'normalize_disease_query' in globals() else effective_disease
                            more_tests = get_fallback_tests(norm_dis, medical_tests_db, min_tests=8)
                            for mt in more_tests:
                                if mt.title() not in tests and mt.lower() not in [t.lower() for t in tests]:
                                    tests.append(mt.title())
                        if tests:
                            result["diagnostic_tests"] = tests

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
                test_data = fetch_medical_test_details(test_key, data.get('disease_name', ''))

                # Translate into Hindi if active language is 'hi'
                if st.session_state.language == "hi" and TRANSLATION_OK:
                    for field in ["name", "description", "why_done", "procedure", "how_you_prepare", "normal_values", "risks"]:
                        if test_data.get(field):
                            test_data[field] = translate_content(test_data[field], target_lang="hi")

                st.markdown("---")
                b_col, t_col = st.columns([1, 4])
                with b_col:
                    if st.button("← Back to Disease", key="back_to_dis_btn", use_container_width=True):
                        del st.session_state.selected_medical_test
                        st.rerun()
                with t_col:
                    disp_name = test_data.get('name', test_key.title())
                    st.markdown(f"<h3 style='color:#38bdf8; margin:0;'>🔬 {disp_name}</h3>", unsafe_allow_html=True)

                td1, td2 = st.columns(2)
                with td1:
                    st.markdown(f"""
                    <div class="info-card" style="border-left-color: #38bdf8;">
                        <h4 style="color:#38bdf8; margin:0 0 6px 0;">📝 About Test</h4>
                        <p style="margin:0; line-height:1.6;">{test_data.get('description', 'Information not available.')}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    if test_data.get('why_done'):
                        st.markdown(f"""
                        <div class="info-card" style="border-left-color: #10b981;">
                            <h4 style="color:#10b981; margin:0 0 6px 0;">🎯 Why It's Done</h4>
                            <p style="margin:0; line-height:1.6;">{test_data.get('why_done')}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    if test_data.get('procedure'):
                        st.markdown(f"""
                        <div class="info-card" style="border-left-color: #06b6d4;">
                            <h4 style="color:#06b6d4; margin:0 0 6px 0;">📋 Procedure / प्रक्रिया</h4>
                            <p style="margin:0; line-height:1.6;">{test_data.get('procedure')}</p>
                        </div>
                        """, unsafe_allow_html=True)
                with td2:
                    if test_data.get('how_you_prepare'):
                        st.markdown(f"""
                        <div class="info-card" style="border-left-color: #f59e0b;">
                            <h4 style="color:#f59e0b; margin:0 0 6px 0;">⚠️ Preparation</h4>
                            <p style="margin:0; line-height:1.6;">{test_data.get('how_you_prepare')}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    if test_data.get('normal_values'):
                        st.markdown(f"""
                        <div class="info-card" style="border-left-color: #a855f7;">
                            <h4 style="color:#a855f7; margin:0 0 6px 0;">✅ Normal Range & Interpretation</h4>
                            <p style="margin:0; line-height:1.6;">{test_data.get('normal_values')}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    if test_data.get('risks'):
                        st.markdown(f"""
                        <div class="info-card" style="border-left-color: #ef4444;">
                            <h4 style="color:#ef4444; margin:0 0 6px 0;">🚨 Risks & Complications / जोखिम</h4>
                            <p style="margin:0; line-height:1.6;">{test_data.get('risks')}</p>
                        </div>
                        """, unsafe_allow_html=True)

                # Test Read Aloud
                test_speech = f"{disp_name}. {test_data.get('description', '')}. Why done: {test_data.get('why_done', '')}. Procedure: {test_data.get('procedure', '')}. Preparation: {test_data.get('how_you_prepare', '')}. Normal range: {test_data.get('normal_values', '')}. Risks: {test_data.get('risks', '')}."
                render_read_aloud_widget(
                    test_speech,
                    widget_key=f"test_{normalize_name(test_key)[:12]}",
                    label="🔊 Listen to Test Details / टेस्ट की जानकारी सुनें"
                )

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
                # Read Aloud (TTS)
                dis_speech = f"{data.get('disease_name')}. {data.get('description')}. Precautions: {'. '.join(data.get('precautions', [])[:2])}."
                render_read_aloud_widget(
                    dis_speech,
                    widget_key=f"dis_{data.get('disease_name', 'overview')[:10]}",
                    label="🔊 Read Aloud Disease Overview / बीमारी की जानकारी सुनें"
                )

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

        if "drug_text_input" not in st.session_state:
            st.session_state.drug_text_input = st.session_state.get("drug_search", "")

        drug_query = st.text_input(
            "Enter drug name or health question:",
            placeholder="e.g. Paracetamol, Ibuprofen, 'What medicine helps with hypertension?'...",
            key="drug_text_input"
        )
        st.session_state.drug_search = drug_query

        # Quick Examples Callback (runs before widget instantiation)
        def _set_drug_example(ex_name):
            st.session_state.drug_text_input = ex_name
            st.session_state.drug_search = ex_name
            st.session_state._trigger_drug = True

        st.markdown('<p style="color:#64748b; font-size:0.85rem;">Quick examples:</p>', unsafe_allow_html=True)
        dex_cols = st.columns(5)
        drug_examples = ["Paracetamol", "Ibuprofen", "Aspirin", "Metformin", "Amoxicillin"]
        for idx, ex in enumerate(drug_examples):
            with dex_cols[idx]:
                st.button(ex, key=f"dex_{idx}", on_click=_set_drug_example, args=(ex,), use_container_width=True)

        col_drug_btn, _ = st.columns([1, 4])
        with col_drug_btn:
            drug_search_btn = st.button("🔍 Search Drug", key="drug_search_action_btn", use_container_width=True, type="primary")

        should_search_drug = drug_search_btn or st.session_state.get("_trigger_drug", False)
        effective_drug_query = (drug_query or st.session_state.get("drug_search", "")).strip()

        if should_search_drug and effective_drug_query:
            if "_trigger_drug" in st.session_state:
                del st.session_state._trigger_drug

            if not DRUG_MODULE_OK:
                st.error("❌ Drug Info module is not available.")
            else:
                # Check if drug_query reports an adverse reaction or allergy
                try:
                    is_allg, allg_data = conversational_assistant.check_and_record_allergy_from_text(
                        effective_drug_query, patient_id=patient_id, patient_db=db
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

                drug_agent = DrugInfoAgent()
                st.session_state.drug_agent = drug_agent

                with st.spinner(f"Analyzing drug database for '{effective_drug_query}'..."):
                    try:
                        # Pass updated patient allergies into drug agent!
                        drug_res = drug_agent.answer(effective_drug_query, patient_allergies=patient_allergies)
                        st.session_state.drug_results = drug_res
                    except Exception as e:
                        st.error(f"Error fetching drug info: {e}")

        # Display Drug Result
        if st.session_state.get("drug_results"):
            res = st.session_state.drug_results
            active_drug_str = (drug_query or st.session_state.get("drug_search", "")).strip()
            is_query_a_question = is_question_query(active_drug_str)
            candidate_drugs = extract_candidate_drugs(res, active_drug_str) if is_query_a_question else []

            # Allergy Cross-Checking:
            if not is_query_a_question:
                # Specific drug searched (e.g. "Paracetamol", "Aspirin")
                is_allg, allg_data = db.check_drug_allergy(patient_id, active_drug_str)
                if is_allg and allg_data:
                    sev = allg_data.get("severity", "Moderate")
                    sym = allg_data.get("symptoms", "Adverse reaction")
                    st.markdown(f"""
                    <div class="critical-card" style="margin-top: 16px;">
                        <h3 style="color:#ef4444 !important; margin:0 0 6px 0;">🚨 CRITICAL ALLERGY ALERT FOR {active_drug_str.upper()}</h3>
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

            ans_text = res.get("answer", "")
            # Ensure clinical cards are ALWAYS present and accurate
            is_direct_lookup = (res.get("type") == "direct" or not is_question_query(drug_query))
            if not ans_text or "Based on standard" in ans_text or len(ans_text) < 40 or "indicated for the treatment of " + drug_query.lower() in ans_text.lower():
                candidate_cards = res.get("drugs", [])
                if candidate_cards:
                    if is_direct_lookup:
                        card = candidate_cards[0]
                        c_name = card.get('name', drug_query)
                        c_ind = card.get('indications', 'Prescribed medication for clinical symptom relief.')
                        c_dose = card.get('dosage', 'Take as directed by doctor or package instructions.')
                        c_warn = card.get('warnings', 'Follow prescribed dosage. Consult doctor before taking.')
                        ans_text = (
                            f"**{c_name.upper()}**\n\n"
                            f"**What it's used for:** {c_ind}\n\n"
                            f"**Dosage:** {c_dose}\n\n"
                            f"**Warnings & Precautions:** {c_warn}\n\n"
                            f"⚠️ For any personal decisions regarding medication, always consult with a doctor or pharmacist."
                        )
                    else:
                        lines = [f"The following medications are indicated for {drug_query}:\n"]
                        for d in candidate_cards[:5]:
                            d_name = d.get('name', 'Medication')
                            d_ind = d.get('indications', f'Prescribed for {drug_query}')
                            d_warn = d.get('warnings', 'Follow prescribed dosage. Consult doctor before taking.')
                            lines.append(f"**{d_name.upper()}**")
                            lines.append(f"What it's used for: {d_name} – {d_ind[:250]}")
                            if d_warn:
                                lines.append(f"Warnings: {d_warn[:200]}")
                            lines.append("")
                        lines.append("⚠️ For any personal decisions regarding medication, always consult with a doctor or pharmacist.")
                        ans_text = "\n".join(lines)
                else:
                    ans_text = f"Consult your physician for prescription treatment regarding '{drug_query}'."

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
            valid_src_names = []
            if sources:
                valid_src_names = [s.get("drug_name") for s in sources if s.get("drug_name") and s.get("drug_name").lower() != drug_query.lower()]
            if not valid_src_names:
                valid_src_names = [d.get("name") for d in res.get("drugs", []) if d.get("name")]
            if valid_src_names:
                st.markdown("<p style='color:#64748b; font-size:0.85rem;'>📚 FDA Sources: " + ", ".join(valid_src_names[:5]) + "</p>", unsafe_allow_html=True)
            else:
                st.markdown("<p style='color:#64748b; font-size:0.85rem;'>📚 FDA Sources: openFDA Drug Database & National Library of Medicine</p>", unsafe_allow_html=True)

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
            render_read_aloud_widget(
                ans_text,
                widget_key="drug_summary",
                label="🔊 Read Aloud Drug Summary / दवा की जानकारी सुनें"
            )

    # ========================== TAB 4: MEDICAL REPORT ==========================
    with tab_report:
        st.markdown("<h2 style='color:#f8fafc;'>📄 Medical Report Analyzer</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color:#94a3b8;'>Upload your blood test, pathology, or discharge report (PDF or Image). We extract values, explain them simply in Hindi or English, and check for any medicine allergy conflicts.</p>", unsafe_allow_html=True)

        uploaded_report = st.file_uploader("Upload Medical Report (PDF, JPG, PNG, WEBP)", type=["pdf", "png", "jpg", "jpeg", "webp"])

        # Quick Sample Reports
        st.markdown("<p style='color:#64748b; font-size:0.85rem; margin-top:6px;'>Or test instantly with verified sample reports:</p>", unsafe_allow_html=True)
        r_cols = st.columns(3)
        sample_reports_data = [
            ("📋 Sample CBC Report", "cbc", "COMPLETE BLOOD COUNT (CBC) REPORT\nPatient: Ramesh Kumar, Age: 42, Gender: Male\nTest Date: 10-Oct-2026\n\nTEST PARAMETERS:\n- Hemoglobin: 10.2 g/dL (Normal: 13.0 - 17.0 g/dL) [LOW - Mild Anemia]\n- Total Leukocyte Count (WBC): 12,500 /mcL (Normal: 4,000 - 11,000 /mcL) [HIGH - Mild Infection]\n- Platelet Count: 180,000 /mcL (Normal: 150,000 - 450,000 /mcL) [Normal]\n- Hematocrit (PCV): 32.1 % (Normal: 40 - 50 %) [LOW]\n- ESR: 28 mm/hr (Normal: 0 - 15 mm/hr) [HIGH - Inflammation]\n\nImpression: Mild microcytic hypochromic anemia with mild leukocytosis. Clinical correlation advised."),
            ("📋 Sample Diabetes & Lipid Panel", "lipid", "METABOLIC & LIPID PROFILE REPORT\nPatient: Sunita Devi, Age: 55, Gender: Female\nTest Date: 10-Oct-2026\n\nTEST PARAMETERS:\n- Fasting Blood Sugar (FBS): 168 mg/dL (Normal: 70 - 100 mg/dL) [HIGH - Diabetic Range]\n- HbA1c: 8.4 % (Normal: < 5.7 %, Diabetic: >= 6.5 %) [HIGH]\n- Total Cholesterol: 245 mg/dL (Normal: < 200 mg/dL) [HIGH]\n- LDL Cholesterol: 162 mg/dL (Normal: < 100 mg/dL) [HIGH - Plaque Risk]\n- HDL Cholesterol: 38 mg/dL (Normal: > 50 mg/dL) [LOW]\n- Triglycerides: 220 mg/dL (Normal: < 150 mg/dL) [HIGH]\n\nImpression: Uncontrolled Type 2 Diabetes Mellitus with mixed dyslipidemia. Lifestyle modification and physician review required."),
            ("📋 Sample Renal & Liver Panel", "renal", "RENAL & LIVER FUNCTION REPORT\nPatient: Amit Verma, Age: 48, Gender: Male\nTest Date: 10-Oct-2026\n\nTEST PARAMETERS:\n- Serum Creatinine: 1.8 mg/dL (Normal: 0.7 - 1.3 mg/dL) [HIGH - Impaired Clearance]\n- Blood Urea Nitrogen (BUN): 28 mg/dL (Normal: 7 - 20 mg/dL) [HIGH]\n- Total Bilirubin: 0.9 mg/dL (Normal: 0.2 - 1.2 mg/dL) [Normal]\n- SGPT (ALT): 68 U/L (Normal: < 45 U/L) [MILD ELEVATION]\n- SGOT (AST): 54 U/L (Normal: < 40 U/L) [MILD ELEVATION]\n- Serum Uric Acid: 7.8 mg/dL (Normal: 3.5 - 7.2 mg/dL) [HIGH]\n\nImpression: Mild elevation in renal parameters (Creatinine/BUN) and transaminases. Nephrology/Physician follow-up recommended. Avoid nephrotoxic NSAIDs.")
        ]
        def _set_sample_report(r_text, label):
            st.session_state.active_report_text = r_text
            st.session_state.active_report_name = label

        for idx, (label, key_suffix, r_text) in enumerate(sample_reports_data):
            with r_cols[idx]:
                st.button(label, key=f"sample_rep_btn_{key_suffix}", on_click=_set_sample_report, args=(r_text, label), use_container_width=True)

        raw_report_text = None
        temp_path = None

        if uploaded_report is not None:
            temp_path = os.path.join(BASE_DIR, f"temp_{uploaded_report.name}")
            with open(temp_path, "wb") as f:
                f.write(uploaded_report.getbuffer())
            try:
                from reports.report_analyzer import extract_from_pdf, extract_from_image
                if uploaded_report.name.lower().endswith(".pdf"):
                    raw_report_text = extract_from_pdf(temp_path)
                else:
                    raw_report_text = extract_from_image(temp_path)
            except Exception as ex:
                raw_report_text = f"Extraction error: {ex}"
        elif st.session_state.get("active_report_text"):
            raw_report_text = st.session_state.active_report_text
            st.info(f"Showing analysis for: **{st.session_state.get('active_report_name', 'Sample Medical Report')}**")

        if raw_report_text:
            with st.spinner("📖 Extracting text and analyzing report..."):
                try:
                    from reports.report_analyzer import get_structured_analysis

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

                        # Ironclad verification of all sections
                        vals = analysis.get("values_found", {})
                        if not vals:
                            from reports.report_analyzer import extract_values
                            vals = extract_values(raw_report_text)
                            analysis["values_found"] = vals

                        probs = analysis.get("problems", [])
                        recs = analysis.get("recommendations", [])
                        diet = analysis.get("diet_lifestyle", [])
                        doc_text = analysis.get("when_to_see_doctor", "")
                        summ = analysis.get("summary", "")

                        needs_fallback = (
                            not probs
                            or not recs
                            or not diet
                            or not doc_text
                            or not summ
                            or "Based on standard" in summ
                            or len(summ.strip()) < 20
                        )

                        if needs_fallback:
                            from reports.report_analyzer import generate_clinical_findings
                            clin = generate_clinical_findings(vals, raw_report_text)
                            if not probs:
                                probs = clin.get("problems", [])
                                analysis["problems"] = probs
                            if not recs:
                                recs = clin.get("recommendations", [])
                                analysis["recommendations"] = recs
                            if not diet:
                                diet = clin.get("diet_lifestyle", [])
                                analysis["diet_lifestyle"] = diet
                            if not doc_text:
                                doc_text = clin.get("when_to_see_doctor", "")
                                analysis["when_to_see_doctor"] = doc_text
                            if not summ or "Based on standard" in summ or len(summ.strip()) < 20:
                                summ = clin.get("summary", "")
                                analysis["summary"] = summ

                            # Translate if target language is not English
                            if st.session_state.language != "en" and TRANSLATION_OK:
                                try:
                                    analysis["summary"] = translate_content(analysis["summary"], target_lang=st.session_state.language)
                                    analysis["when_to_see_doctor"] = translate_content(analysis["when_to_see_doctor"], target_lang=st.session_state.language)
                                    analysis["problems"] = [translate_content(p, target_lang=st.session_state.language) for p in analysis["problems"]]
                                    analysis["recommendations"] = [translate_content(r, target_lang=st.session_state.language) for r in analysis["recommendations"]]
                                    analysis["diet_lifestyle"] = [translate_content(d, target_lang=st.session_state.language) for d in analysis["diet_lifestyle"]]
                                except Exception as terr:
                                    print(f"[ReportUI] Fallback translation notice: {terr}")

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
                        speech_rep = f"Report summary. {analysis.get('summary', '')}. Key problems: {', '.join(probs[:3])}."
                        render_read_aloud_widget(speech_rep, widget_key="report_analysis_tts", label="🔊 Read Aloud Report Analysis / रिपोर्ट की जानकारी सुनें")

                except Exception as e:
                    st.error(f"Error analyzing report: {e}")
                    st.code(traceback.format_exc())
                finally:
                    if temp_path and os.path.exists(temp_path):
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

        if "symp_area" not in st.session_state:
            st.session_state.symp_area = st.session_state.get("symptom_input", "")

        symp_text = st.text_area(
            "Describe your symptoms:",
            placeholder="e.g., I have had fever, dry cough, and vomiting for 2 days...",
            height=100,
            key="symp_area"
        )
        st.session_state.symptom_input = symp_text

        # Quick Add Pills / Examples Callback (runs before widget instantiation)
        def _set_symptom_example(s_val):
            st.session_state.symp_area = s_val
            st.session_state.symptom_input = s_val
            st.session_state._trigger_symptoms = True

        st.markdown("<p style='color:#64748b; font-size:0.85rem;'>Quick examples (Click to analyze):</p>", unsafe_allow_html=True)
        q_cols = st.columns(5)
        sample_symptom_combos = [
            ("Fever & Cough", "fever, cough, body ache"),
            ("Headache", "severe headache, nausea"),
            ("Stomach Pain", "stomach pain, vomiting"),
            ("Breathing Issue", "shortness of breath, chest tightness"),
            ("Joint Pain", "joint pain, morning stiffness")
        ]
        for idx, (label, s_text) in enumerate(sample_symptom_combos):
            with q_cols[idx]:
                st.button(label, key=f"qsym_{idx}", on_click=_set_symptom_example, args=(s_text,), use_container_width=True)

        col_chk_btn, _ = st.columns([1, 4])
        with col_chk_btn:
            check_symp_btn = st.button("🔍 Check Symptoms", key="chk_symp_action_btn", use_container_width=True, type="primary")

        should_check_symptoms = check_symp_btn or st.session_state.get("_trigger_symptoms", False)
        effective_symp_text = (symp_text or st.session_state.get("symptom_input", "")).strip()

        if should_check_symptoms and effective_symp_text:
            if "_trigger_symptoms" in st.session_state:
                del st.session_state._trigger_symptoms

            with st.spinner("Analyzing symptoms and cross-referencing disease patterns..."):
                try:
                    if "symptom_checker" not in st.session_state:
                        from agents.symptom_checker_agent import SymptomCheckerAgent
                        st.session_state.symptom_checker = SymptomCheckerAgent()

                    res_sym = st.session_state.symptom_checker.predict(effective_symp_text, language=st.session_state.language)

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
                        top_dis = res_sym['predictions'][0]['disease'] if res_sym.get('predictions') else 'condition'
                        top_c = res_sym['predictions'][0]['confidence'] if res_sym.get('predictions') else 50
                        speech_sym = f"Symptom analysis results. Top possibility is {top_dis} with {top_c} percent confidence. Matched symptoms: {', '.join(res_sym.get('symptoms', []))}."
                        render_read_aloud_widget(speech_sym, widget_key="symptom_prediction_tts", label="🔊 Read Aloud Prediction / लक्षण विश्लेषण सुनें")

                except Exception as e:
                    st.error(f"Error checking symptoms: {e}")

    # ========================== TAB 6: WELLNESS HUB ==========================
    with tab_wellness:
        if WELLNESS_MODULE_OK:
            render_wellness_hub_tab(patient_id=patient_id, patient_db=db)
        else:
            st.error("Wellness Hub module is currently unavailable.")

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