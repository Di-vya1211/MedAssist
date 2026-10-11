"""
MedAssist - Patient Integration Module
Drug safety checking, allergy warnings, and medical context from history
"""

import streamlit as st
from datetime import datetime
try:
    from .patient_db import PatientDatabase
except ImportError:
    from patient_db import PatientDatabase


def check_drug_allergy_with_warning(patient_id: int, drug_name: str, db: PatientDatabase) -> Dict:
    """
    Check if patient is allergic to drug and show warning
    Returns detailed warning info
    """
    is_allergic, allergy_data = db.check_drug_allergy(patient_id, drug_name)
    
    result = {
        'is_allergic': is_allergic,
        'drug_name': drug_name,
        'allergy_data': allergy_data,
        'warning_level': 'none'
    }
    
    if not is_allergic:
        return result
    
    # Determine warning level based on severity
    severity = allergy_data.get('severity', 'Moderate')
    
    if severity == 'Severe':
        result['warning_level'] = 'critical'
        
        st.error(f"""
        🚨 **CRITICAL ALLERGY WARNING!**
        
        ❌ **DO NOT USE: {drug_name.upper()}**
        
        **Generic Name:** {allergy_data.get('generic_name', 'N/A')}
        
        **Severity:** {severity}
        
        **Symptoms:** {allergy_data.get('symptoms', 'Not specified')}
        
        **Reaction Date:** {allergy_data.get('reaction_date', 'Unknown')}
        
        **Notes:** {allergy_data.get('notes', 'Consult doctor immediately')}
        
        ⚠️ **PLEASE CONSULT YOUR DOCTOR BEFORE USING THIS MEDICINE!**
        """)
    
    elif severity == 'Moderate':
        result['warning_level'] = 'warning'
        
        st.warning(f"""
        ⚠️ **ALLERGY WARNING**
        
        **Caution with:** {drug_name}
        
        **Generic Name:** {allergy_data.get('generic_name', 'N/A')}
        
        **Severity:** {severity}
        
        **Symptoms:** {allergy_data.get('symptoms', 'Not specified')}
        
        **Note:** {allergy_data.get('notes', 'Use with caution')}
        
        💡 **Consider alternative medicines - Consult your doctor**
        """)
    
    else:  # Mild
        result['warning_level'] = 'info'
        
        st.info(f"""
        ℹ️ **ALLERGY INFORMATION**
        
        **Medicine:** {drug_name}
        
        **Generic Name:** {allergy_data.get('generic_name', 'N/A')}
        
        **Severity:** {severity}
        
        **Possible Symptoms:** {allergy_data.get('symptoms', 'Mild reaction')}
        
        **Note:** {allergy_data.get('notes', 'Monitor for reactions')}
        
        🔍 **Monitor for any adverse reactions**
        """)
    
    return result


def get_patient_medical_context(patient_id: int, db: PatientDatabase) -> str:
    """
    Get patient's medical history context for LLM recommendations
    This helps LLM make better recommendations based on past conditions
    """
    context_parts = []
    
    # Get patient profile
    patient = db.get_patient(patient_id)
    if patient:
        context_parts.append(f"Patient: {patient.get('full_name', 'Unknown')}")
        context_parts.append(f"Age: {patient.get('age', 'Unknown')}")
        context_parts.append(f"Gender: {patient.get('gender', 'Unknown')}")
        context_parts.append(f"Blood Type: {patient.get('blood_type', 'Unknown')}")
        context_parts.append("")
    
    # Get allergies
    allergies = db.get_allergies(patient_id)
    if allergies:
        context_parts.append("Known Allergies:")
        for allergy in allergies:
            context_parts.append(f"- {allergy.get('medicine_name', 'Unknown')}: {allergy.get('severity', 'Unknown')} (Symptoms: {allergy.get('symptoms', 'Not specified')})")
        context_parts.append("")
    
    # Get medical history
    history = db.get_medical_history(patient_id)
    if history:
        context_parts.append("Medical History:")
        for h in history[:5]:  # Last 5 conditions
            context_parts.append(f"- {h.get('disease_name', 'Unknown')} ({h.get('diagnosis_date', 'Date unknown')[:10]}): {h.get('severity', 'Unknown')}")
            if h.get('treatment_given'):
                context_parts.append(f"  Treatment: {h.get('treatment_given')}")
        context_parts.append("")
    
    # Get recent reports
    reports = db.get_reports(patient_id, limit=3)
    if reports:
        context_parts.append("Recent Medical Reports:")
        for report in reports:
            context_parts.append(f"- {report.get('disease_diagnosed', 'Unknown')} ({report.get('created_at', 'Date unknown')[:10]})")
        context_parts.append("")
    
    return "\n".join(context_parts)


def show_patient_summary(patient_id: int, db: PatientDatabase):
    """Display patient health summary in sidebar"""
    patient = db.get_patient(patient_id)
    
    if not patient:
        return
    
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 👤 Patient Profile")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Age", patient.get('age', 'N/A'))
        with col2:
            st.metric("Blood Type", patient.get('blood_type', 'N/A'))
        
        # Quick stats
        allergies = db.get_allergies(patient_id)
        history = db.get_medical_history(patient_id)
        reports = db.get_reports(patient_id)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Allergies", len(allergies))
        with col2:
            st.metric("Conditions", len(history))
        with col3:
            st.metric("Reports", len(reports))
        
        # Show critical allergies
        critical_allergies = [a for a in allergies if a.get('severity') == 'Severe']
        if critical_allergies:
            st.error(f"🚨 {len(critical_allergies)} Critical Allerg{'y' if len(critical_allergies) == 1 else 'ies'}!")
            for allergy in critical_allergies:
                st.warning(f"⚠️ {allergy.get('medicine_name')}")


def show_allergy_warnings_banner(patient_id: int, db: PatientDatabase):
    """Show banner with critical allergies at top of page"""
    allergies = db.get_allergies(patient_id)
    critical = [a for a in allergies if a.get('severity') == 'Severe']
    
    if critical:
        st.markdown(f"""
        <div style='background-color: #ff4444; color: white; padding: 15px; border-radius: 5px; margin-bottom: 10px;'>
            <h3>🚨 CRITICAL ALLERGIES: {', '.join([a.get('medicine_name') for a in critical])}</h3>
            <p>⚠️ Please inform your healthcare provider before accepting any medication.</p>
        </div>
        """, unsafe_allow_html=True)


def save_llm_recommendation(patient_id: int, disease: str, symptoms: str,
                           tests: List[str], drugs: List[str], precautions: str,
                           llm_response: str, confidence: float, db: PatientDatabase) -> Tuple[bool, str]:
    """
    Save LLM recommendation as medical report
    """
    try:
        success, message = db.add_report(
            patient_id=patient_id,
            disease_diagnosed=disease,
            symptoms=symptoms,
            tests=",".join(tests) if tests else "",
            drugs=",".join(drugs) if drugs else "",
            precautions=precautions,
            llm_response=llm_response,
            confidence=confidence
        )
        
        if success:
            st.success(f"✅ Report saved! {message}")
            return True, message
        else:
            st.error(f"❌ {message}")
            return False, message
    
    except Exception as e:
        error_msg = f"Failed to save report: {str(e)}"
        st.error(f"❌ {error_msg}")
        return False, error_msg


def show_patient_allergies_ui(patient_id: int, db: PatientDatabase):
    """UI for managing patient allergies"""
    st.markdown("### 💊 My Allergies")
    
    allergies = db.get_allergies(patient_id)
    
    if allergies:
        # Display allergies in a table format
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("**Medicine**")
        with col2:
            st.markdown("**Severity**")
        with col3:
            st.markdown("**Symptoms**")
        with col4:
            st.markdown("**Date**")
        
        for allergy in allergies:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.text(allergy.get('medicine_name', 'Unknown'))
            
            with col2:
                severity = allergy.get('severity', 'Unknown')
                if severity == 'Severe':
                    st.error(severity)
                elif severity == 'Moderate':
                    st.warning(severity)
                else:
                    st.info(severity)
            
            with col3:
                st.text(allergy.get('symptoms', 'Not specified')[:30])
            
            with col4:
                date_str = str(allergy.get('reaction_date', 'Unknown'))[:10]
                st.text(date_str)
    
    else:
        st.info("No allergies recorded yet")
    
    # Add new allergy
    with st.expander("➕ Add New Allergy"):
        col1, col2 = st.columns(2)
        
        with col1:
            medicine = st.text_input("Medicine Name", key="allergy_medicine")
            generic = st.text_input("Generic Name (Optional)", key="allergy_generic")
        
        with col2:
            severity = st.selectbox("Severity", ["Mild", "Moderate", "Severe"], key="allergy_severity")
            symptoms = st.text_input("Symptoms", key="allergy_symptoms")
        
        notes = st.text_area("Additional Notes", key="allergy_notes", height=50)
        
        if st.button("Save Allergy", use_container_width=True):
            if medicine and severity:
                success, message = db.add_allergy(
                    patient_id=patient_id,
                    medicine_name=medicine,
                    generic_name=generic,
                    severity=severity,
                    symptoms=symptoms,
                    notes=notes
                )
                
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
            else:
                st.error("Please fill required fields")


def show_medical_history_ui(patient_id: int, db: PatientDatabase):
    """UI for medical history"""
    st.markdown("### 📋 Medical History")
    
    history = db.get_medical_history(patient_id)
    
    if history:
        for h in history:
            with st.expander(f"📌 {h.get('disease_name')} - {str(h.get('diagnosis_date', 'Date'))[:10]}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Severity:** {h.get('severity', 'Unknown')}")
                    st.markdown(f"**Date:** {h.get('diagnosis_date', 'Unknown')}")
                
                with col2:
                    st.markdown(f"**Symptoms:** {h.get('symptoms', 'Not specified')}")
                
                if h.get('treatment_given'):
                    st.markdown(f"**Treatment:** {h.get('treatment_given')}")
                
                if h.get('doctor_notes'):
                    st.markdown(f"**Doctor Notes:** {h.get('doctor_notes')}")
    else:
        st.info("No medical history recorded yet")


def show_reports_ui(patient_id: int, db: PatientDatabase):
    """UI for medical reports"""
    st.markdown("### 📄 Medical Reports")
    
    reports = db.get_reports(patient_id)
    
    if reports:
        for report in reports:
            with st.expander(f"📋 {report.get('disease_diagnosed')} - {str(report.get('created_at', 'Date'))[:10]}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Confidence:** {report.get('confidence_score', 0):.1%}")
                    
                    if report.get('tests_recommended'):
                        st.markdown(f"**Tests:** {report.get('tests_recommended')}")
                
                with col2:
                    if report.get('drugs_prescribed'):
                        st.markdown(f"**Drugs:** {report.get('drugs_prescribed')}")
                    
                    if report.get('precautions'):
                        st.markdown(f"**Precautions:** {report.get('precautions')}")
                
                if report.get('llm_response'):
                    st.info(f"**Report:** {report.get('llm_response')[:200]}...")