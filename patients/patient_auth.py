"""
MedAssist - Patient Authentication Pages
Login and Registration UI for Streamlit
"""

import os
import re
import streamlit as st
from .patient_db import PatientDatabase, DEFAULT_DB_PATH

def init_auth_session():
    """Initialize authentication session state"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'patient_id' not in st.session_state:
        st.session_state.patient_id = None
    if 'patient_name' not in st.session_state:
        st.session_state.patient_name = None
    if 'auth_page' not in st.session_state:
        st.session_state.auth_page = "login"


def show_login_page(db: PatientDatabase):
    """Display login page"""
    st.markdown("""
    <style>
    /* High contrast dark buttons */
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
    .stButton > button[kind="primary"] p,
    .stButton > button[kind="primary"] span,
    .stButton > button[kind="primary"] div {
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
    }
    .stButton > button[kind="secondary"] p,
    .stButton > button[kind="secondary"] span,
    .stButton > button[kind="secondary"] div {
        color: #f1f5f9 !important;
    }
    </style>
    <div style='text-align: center; padding: 20px;'>
        <h1>🏥 MedAssist</h1>
        <h3>Rural Health Companion</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.subheader("Patient Login")
        
        username = st.text_input("Username", key="login_username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", key="login_password", placeholder="Enter your password")
        
        col_login, col_register = st.columns(2)
        
        with col_login:
            if st.button("🔓 Login", use_container_width=True, key="login_btn", type="primary"):
                if not username or not password:
                    st.error("⚠️ Please enter username and password!")
                else:
                    success, message, patient_id = db.login_patient(username, password)
                    
                    if success:
                        patient_data = db.get_patient(patient_id) or {}
                        st.session_state.authenticated = True
                        st.session_state.patient_id = patient_id
                        st.session_state.patient_username = username
                        st.session_state.patient_name = patient_data.get('full_name') or username
                        st.session_state.patient_profile = patient_data
                        pref_lang = patient_data.get('language_preference') or "English"
                        if pref_lang == "Hindi":
                            st.session_state.language = "hi"
                        else:
                            st.session_state.language = "en"
                        st.success(f"✅ {message}")
                        st.rerun()
                    else:
                        st.error(f"❌ {message}")
        
        with col_register:
            if st.button("📝 Register", use_container_width=True, key="register_btn"):
                st.session_state.auth_page = "register"
                st.rerun()
        
        st.markdown("---")
        st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
        if st.button("⚡ Quick Demo Login", use_container_width=True, key="quick_demo_btn"):
            demo_user = db.get_connection().execute("SELECT patient_id FROM patients WHERE username='demo'").fetchone()
            if demo_user:
                pid = demo_user[0]
                # Ensure demo user has persistent registration allergies
                if not db.get_allergies(pid):
                    db.add_allergy(pid, "Aspirin", "Severe", "Facial swelling, hives, breathing difficulty", generic_name="Acetylsalicylic acid", notes="Permanent registration record")
                    db.add_allergy(pid, "Sulfa antibiotics", "Moderate", "Skin rash, intense itching", generic_name="Sulfamethoxazole", notes="Permanent registration record")
                patient_data = db.get_patient(pid) or {}
                st.session_state.authenticated = True
                st.session_state.patient_id = pid
                st.session_state.patient_username = "demo"
                st.session_state.patient_name = patient_data.get('full_name') or "Demo Patient"
                st.session_state.patient_profile = patient_data
                st.session_state.language = "en"
                st.success("✅ Logged in as Demo Patient!")
                st.rerun()
            else:
                st.info("Demo user: demo / demo123")
        st.markdown("<p style='color:#9ca3af; font-size:0.85rem; text-align:center; margin-top:8px;'>Demo Credentials: <b>demo</b> / <b>demo123</b></p></div>", unsafe_allow_html=True)


def show_registration_page(db: PatientDatabase):
    """Display registration page"""
    st.markdown("""
    <style>
    /* High contrast dark buttons */
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
    }
    .stButton > button[kind="secondary"],
    .stButton > button[data-testid="stBaseButton-secondary"] {
        background: #1e293b !important;
        color: #f1f5f9 !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
    }
    .stButton > button[kind="secondary"] p,
    .stButton > button[kind="secondary"] span,
    .stButton > button[kind="secondary"] div {
        color: #f1f5f9 !important;
    }
    </style>
    <div style='text-align: center; padding: 20px;'>
        <h1>🏥 MedAssist</h1>
        <h3>Patient Registration</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.subheader("Create New Patient Account")
        
        # Basic Information
        st.markdown("### Basic Information")
        col1, col2 = st.columns(2)
        
        with col1:
            full_name = st.text_input("Full Name *", placeholder="Your full name")
            username = st.text_input("Username *", placeholder="Choose a username")
            email = st.text_input("Email *", placeholder="your@email.com")
        
        with col2:
            age = st.number_input("Age", min_value=0, max_value=120, value=30)
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            phone = st.text_input("Phone Number", placeholder="98765-43210")
        
        # Medical Information
        st.markdown("### Medical Information")
        col1, col2 = st.columns(2)
        
        with col1:
            blood_type = st.selectbox("Blood Type", ["", "O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-"])
            height = st.number_input("Height (cm)", min_value=50.0, max_value=250.0, value=170.0, step=0.5)
        
        with col2:
            weight = st.number_input("Weight (kg)", min_value=10.0, max_value=300.0, value=70.0, step=0.5)
            language = st.selectbox("Preferred Language", ["English", "Hindi", "Bengali", "Tamil", "Telugu", "Marathi"], index=0)
        
        # Known Drug Allergies (Permanent Record)
        st.markdown("### Known Drug Allergies (पूर्व दवा एलर्जी)")
        col_allg1, col_allg2 = st.columns([3, 1])
        with col_allg1:
            reg_allergies = st.text_input(
                "Known Allergies to Medicines (दवा एलर्जी, यदि कोई हो)",
                placeholder="e.g. Aspirin, Penicillin, Paracetamol, Sulfa (or leave blank if none)",
                key="reg_allg_input"
            )
        with col_allg2:
            reg_allergy_sev = st.selectbox("Allergy Severity", ["Severe", "Moderate", "Mild"], index=0, key="reg_allg_sev")

        # Emergency Contact
        st.markdown("### Emergency Contact")
        col1, col2 = st.columns(2)
        
        with col1:
            emergency_name = st.text_input("Emergency Contact Name", placeholder="Contact person name")
        
        with col2:
            emergency_phone = st.text_input("Emergency Contact Phone", placeholder="98765-43211")
        
        # Doctor Information
        st.markdown("### Your Doctor")
        col1, col2 = st.columns(2)
        
        with col1:
            doctor_name = st.text_input("Doctor's Name (Optional)", placeholder="Dr. Name")
        
        with col2:
            doctor_phone = st.text_input("Doctor's Phone (Optional)", placeholder="Doctor's phone")
        
        # Password
        st.markdown("### Set Password")
        col1, col2 = st.columns(2)
        
        with col1:
            password = st.text_input("Password *", type="password", placeholder="Min 6 characters")
        
        with col2:
            confirm_password = st.text_input("Confirm Password *", type="password", placeholder="Re-enter password")
        
        # Buttons
        col_register, col_back = st.columns(2)
        
        with col_register:
            if st.button("✅ Register", use_container_width=True, key="register_confirm", type="primary"):
                # Validation
                if not all([full_name, username, email, password, confirm_password]):
                    st.error("⚠️ Please fill all required fields (*)")
                elif password != confirm_password:
                    st.error("⚠️ Passwords do not match!")
                elif len(password) < 6:
                    st.error("⚠️ Password must be at least 6 characters!")
                else:
                    # Register
                    success, message, patient_id = db.register_patient(
                        username=username,
                        email=email,
                        password=password,
                        full_name=full_name,
                        age=int(age) if age else None,
                        gender=gender,
                        phone=phone,
                        blood_type=blood_type if blood_type else None
                    )
                    
                    if success:
                        st.success(f"✅ {message}")
                        st.info(f"Your Patient ID: {patient_id}")
                        
                        # Update patient with additional info
                        db.update_patient(
                            patient_id,
                            height_cm=height,
                            weight_kg=weight,
                            language_preference=language,
                            emergency_contact_name=emergency_name,
                            emergency_contact_phone=emergency_phone,
                            doctor_name=doctor_name,
                            doctor_phone=doctor_phone
                        )
                        
                        # Save any declared allergies directly with the registration record
                        if reg_allergies and reg_allergies.strip():
                            drug_list = [d.strip() for d in re.split(r'[,;]+', reg_allergies) if d.strip()]
                            for drug_item in drug_list:
                                db.add_allergy(
                                    patient_id=patient_id,
                                    medicine_name=drug_item,
                                    severity=reg_allergy_sev,
                                    symptoms="Declared during patient registration",
                                    notes="Permanent registration record"
                                )

                        st.success("🎉 Account created successfully! Logging you in...")
                        patient_data = db.get_patient(patient_id) or {}
                        st.session_state.authenticated = True
                        st.session_state.patient_id = patient_id
                        st.session_state.patient_username = username
                        st.session_state.patient_name = full_name
                        st.session_state.patient_profile = patient_data
                        st.session_state.language = "hi" if language == "Hindi" else "en"
                        st.rerun()
                    else:
                        st.error(f"❌ {message}")
        
        with col_back:
            if st.button("← Back to Login", use_container_width=True, key="back_to_login"):
                st.session_state.auth_page = "login"
                st.rerun()


def render_auth(db_path: str = DEFAULT_DB_PATH):
    """
    Main authentication handler
    Returns: (authenticated, patient_id)
    """
    init_auth_session()
    
    db = PatientDatabase(db_path)
    
    if not st.session_state.authenticated:
        if st.session_state.auth_page == "login":
            show_login_page(db)
        else:
            show_registration_page(db)
        
        return False, None
    
    return True, st.session_state.patient_id


def show_patient_header():
    """Show patient dashboard header"""
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        st.markdown(f"### 👤 Welcome, {st.session_state.patient_name}!")
    
    with col3:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.patient_id = None
            st.session_state.patient_name = None
            st.session_state.auth_page = "login"
            st.rerun()


def get_patient_db(db_path: str = DEFAULT_DB_PATH) -> PatientDatabase:
    """Get patient database instance"""
    if 'patient_db' not in st.session_state:
        st.session_state.patient_db = PatientDatabase(db_path)
    return st.session_state.patient_db