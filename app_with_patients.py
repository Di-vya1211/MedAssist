"""
MedAssist — Rural Health Companion (WITH PATIENT MANAGEMENT)
Complete app with login, patient tracking, allergy checking, and voice interface
"""

import os
import sys
import streamlit as st
from datetime import datetime

# ========== IMPORT PATIENT MANAGEMENT MODULES ==========
from patient_db import PatientDatabase
from patient_auth import render_auth, get_patient_db, show_patient_header
from patient_integration import (
    check_drug_allergy_with_warning,
    get_patient_medical_context,
    show_patient_summary,
    show_allergy_warnings_banner,
    save_llm_recommendation,
    show_patient_allergies_ui,
    show_medical_history_ui,
    show_reports_ui
)
from patient_voice import (
    render_voice_input_ui,
    render_voice_symptom_checker,
    render_voice_history,
    VoiceManager
)

# ========== YOUR EXISTING IMPORTS ==========
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

try:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from disease_info_module_complete.disease_info import DiseaseInfoRetriever, format_disease_info
    DISEASE_MODULE_OK = True
except:
    DISEASE_MODULE_OK = False

try:
    from agents.rag_retriever import RAGRetriever
    RAG_MODULE_OK = True
except:
    RAG_MODULE_OK = False

try:
    from agents.drug_info_agent import DrugInfoAgent
    DRUG_MODULE_OK = True
except:
    DRUG_MODULE_OK = False

# ========== PAGE CONFIG ==========
st.set_page_config(
    page_title="MedAssist — Rural Health Companion",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ========== CUSTOM CSS ==========
st.markdown("""
<style>
    .main { padding: 0rem 0.5rem; }
    .stTabs [data-baseweb="tab-list"] { gap: 2px; }
    h1 { color: #2E86AB; }
    h2 { color: #A23B72; }
</style>
""", unsafe_allow_html=True)

# ========== AUTHENTICATION ==========
def main():
    """Main app with authentication"""
    
    # Check authentication
    authenticated, patient_id = render_auth()
    
    if not authenticated:
        st.stop()  # Stop if not authenticated
    
    # Get database instance
    db = get_patient_db()
    
    # Show patient header with logout
    show_patient_header()
    
    # Show critical allergies banner
    show_allergy_warnings_banner(patient_id, db)
    
    # Show patient summary in sidebar
    show_patient_summary(patient_id, db)
    
    # ========== MAIN NAVIGATION ==========
    st.markdown("---")
    
    # Create main navigation tabs
    main_tabs = st.tabs([
        "🏠 Dashboard",
        "🔍 Symptom Checker",
        "💊 Drug Information",
        "🩺 Disease Information",
        "📊 Medical Reports",
        "👤 My Profile",
        "🎤 Voice Assistant"
    ])
    
    # ========== TAB 1: DASHBOARD ==========
    with main_tabs[0]:
        st.markdown("### Welcome to MedAssist!")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info("📋 **Quick Actions**")
            if st.button("Check Symptoms", use_container_width=True):
                st.session_state.selected_tab = 1
                st.rerun()
        
        with col2:
            st.info("💊 **Drug Info**")
            if st.button("Search Drug", use_container_width=True):
                st.session_state.selected_tab = 2
                st.rerun()
        
        with col3:
            st.info("🏥 **Disease Info**")
            if st.button("Search Disease", use_container_width=True):
                st.session_state.selected_tab = 3
                st.rerun()
        
        st.markdown("---")
        st.markdown("### 📈 Your Health Overview")
        
        patient = db.get_patient(patient_id)
        allergies = db.get_allergies(patient_id)
        history = db.get_medical_history(patient_id)
        reports = db.get_reports(patient_id)
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Age", patient.get('age', 'N/A'))
        col2.metric("Blood Type", patient.get('blood_type', 'N/A'))
        col3.metric("Total Allergies", len(allergies))
        col4.metric("Medical Conditions", len(history))
        
        # Recent activity
        st.markdown("### 📅 Recent Activity")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Recent Reports**")
            if reports:
                for report in reports[:3]:
                    st.info(f"📋 {report.get('disease_diagnosed')} - {str(report.get('created_at'))[:10]}")
            else:
                st.info("No reports yet")
        
        with col2:
            st.markdown("**Recent Conditions**")
            if history:
                for h in history[:3]:
                    st.info(f"🔴 {h.get('disease_name')} - {str(h.get('diagnosis_date'))[:10]}")
            else:
                st.info("No medical history yet")
    
    # ========== TAB 2: SYMPTOM CHECKER (WITH VOICE) ==========
    with main_tabs[1]:
        st.markdown("### 🔍 Symptom Checker")
        
        # Voice or text input
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🎤 Voice Input**")
            if st.button("Record Symptoms"):
                symptom_voice = render_voice_symptom_checker(patient_id, db)
                if symptom_voice:
                    st.session_state.symptom_input = symptom_voice
        
        with col2:
            st.markdown("**📝 Text Input**")
        
        # Text area
        symptoms = st.text_area(
            "Describe your symptoms:",
            value=st.session_state.get('symptom_input', ''),
            height=120,
            key="symptom_text"
        )
        
        if st.button("🔍 Analyze Symptoms", use_container_width=True):
            if not symptoms:
                st.error("Please describe your symptoms")
            else:
                st.info("🔄 Processing... Using AI to analyze symptoms")
                
                if RAG_MODULE_OK:
                    # Your existing RAG retriever code
                    try:
                        st.markdown("**Analysis Results:**")
                        st.info("Integration with your RAG module would go here")
                        
                        # Save to database
                        save_llm_recommendation(
                            patient_id=patient_id,
                            disease="Based on symptoms",
                            symptoms=symptoms,
                            tests=[],
                            drugs=[],
                            precautions="Consult doctor",
                            llm_response="Analysis complete",
                            confidence=0.75,
                            db=db
                        )
                    except Exception as e:
                        st.error(f"Error: {e}")
                else:
                    st.error("RAG module not available")
        
        st.markdown("---")
        st.markdown("### 📜 Voice History")
        render_voice_history(patient_id, db)
    
    # ========== TAB 3: DRUG INFORMATION ==========
    with main_tabs[2]:
        st.markdown("### 💊 Drug Information")
        
        drug_name = st.text_input("Enter drug name:", placeholder="e.g., Aspirin, Amoxicillin")
        
        if drug_name and st.button("Search Drug"):
            # Check for allergy FIRST
            st.info("🔍 Checking for allergies...")
            allergy_result = check_drug_allergy_with_warning(patient_id, drug_name, db)
            
            if allergy_result['is_allergic']:
                st.warning("⚠️ You have a known allergy to this drug!")
            
            # Then show drug info if your module is available
            if DRUG_MODULE_OK:
                try:
                    st.markdown("---")
                    st.markdown("**Drug Information:**")
                    st.info("Integration with your drug_info_agent would go here")
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.error("Drug module not available")
    
    # ========== TAB 4: DISEASE INFORMATION ==========
    with main_tabs[3]:
        st.markdown("### 🩺 Disease Information")
        
        disease_name = st.text_input("Enter disease name:", placeholder="e.g., Diabetes, Asthma")
        
        if disease_name and st.button("Search Disease"):
            if DISEASE_MODULE_OK:
                try:
                    st.info("🔄 Fetching disease information...")
                    st.markdown("**Disease Information:**")
                    st.info("Integration with your disease_info module would go here")
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.error("Disease module not available")
    
    # ========== TAB 5: MEDICAL REPORTS ==========
    with main_tabs[4]:
        st.markdown("### 📊 Medical Reports")
        show_reports_ui(patient_id, db)
    
    # ========== TAB 6: MY PROFILE ==========
    with main_tabs[5]:
        st.markdown("### 👤 My Profile")
        
        patient = db.get_patient(patient_id)
        
        if patient:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Personal Information**")
                st.text(f"Name: {patient.get('full_name')}")
                st.text(f"Age: {patient.get('age')}")
                st.text(f"Gender: {patient.get('gender')}")
                st.text(f"Phone: {patient.get('phone_number')}")
            
            with col2:
                st.markdown("**Medical Information**")
                st.text(f"Blood Type: {patient.get('blood_type')}")
                st.text(f"Height: {patient.get('height_cm')} cm")
                st.text(f"Weight: {patient.get('weight_kg')} kg")
                st.text(f"Doctor: {patient.get('doctor_name', 'N/A')}")
            
            st.markdown("---")
            st.markdown("### 💊 Allergies Management")
            show_patient_allergies_ui(patient_id, db)
            
            st.markdown("---")
            st.markdown("### 📋 Medical History")
            show_medical_history_ui(patient_id, db)
    
    # ========== TAB 7: VOICE ASSISTANT ==========
    with main_tabs[6]:
        st.markdown("### 🎤 Voice Assistant")
        
        patient = db.get_patient(patient_id)
        language = patient.get('language_preference', 'Hindi') if patient else 'Hindi'
        
        st.info(f"Speaking in: {language}")
        
        # Voice input options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🎤 Record Symptoms", use_container_width=True):
                success, text = render_voice_input_ui(patient_id, db)
                if success:
                    st.session_state.voice_symptom = text
                    st.rerun()
        
        with col2:
            if st.button("🎤 Record Medical History", use_container_width=True):
                success, text = render_voice_input_ui(patient_id, db)
                if success:
                    st.session_state.voice_history = text
                    st.rerun()
        
        with col3:
            if st.button("🎤 General Query", use_container_width=True):
                success, text = render_voice_input_ui(patient_id, db)
                if success:
                    st.session_state.voice_query = text
                    st.rerun()
        
        st.markdown("---")
        st.markdown("### 📜 Recent Interactions")
        render_voice_history(patient_id, db)


if __name__ == "__main__":
    main()