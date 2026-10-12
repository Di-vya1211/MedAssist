"""
MedAssist - Patient Profile & Health Dashboard UI
Renders the complete patient profile with registration records (Weight, Height, Blood Type, BMI),
interactive profile editing, and comprehensive allergy/adverse reaction tracking.
"""

import streamlit as st
from datetime import datetime
from typing import Dict, Any, Optional

def calculate_bmi(weight_kg: Optional[float], height_cm: Optional[float]) -> Dict[str, Any]:
    """Calculates BMI and returns value, status label, and color."""
    if not weight_kg or not height_cm or height_cm <= 0:
        return {"value": "N/A", "label": "Not Recorded", "color": "#94a3b8", "bg": "rgba(148, 163, 184, 0.1)"}
    
    height_m = height_cm / 100.0
    bmi = weight_kg / (height_m * height_m)
    bmi_val = round(bmi, 1)

    if bmi < 18.5:
        return {"value": f"{bmi_val}", "label": "Underweight", "color": "#38bdf8", "bg": "rgba(56, 189, 248, 0.15)"}
    elif 18.5 <= bmi < 25.0:
        return {"value": f"{bmi_val}", "label": "Healthy (Normal)", "color": "#10b981", "bg": "rgba(16, 185, 129, 0.15)"}
    elif 25.0 <= bmi < 30.0:
        return {"value": f"{bmi_val}", "label": "Overweight", "color": "#f59e0b", "bg": "rgba(245, 158, 11, 0.15)"}
    else:
        return {"value": f"{bmi_val}", "label": "Obese", "color": "#ef4444", "bg": "rgba(239, 68, 68, 0.15)"}


def render_patient_dashboard_tab(patient_id: int, db):
    """
    Renders the complete dashboard & profile tab.
    """
    # Refresh patient data
    patient = db.get_patient(patient_id)
    if not patient:
        st.error("Patient profile not found. Please log in again.")
        return

    st.session_state.patient_profile = patient
    full_name = patient.get("full_name") or st.session_state.get("patient_name") or "Patient"
    username = patient.get("username", "user")
    age = patient.get("age", "N/A")
    gender = patient.get("gender", "N/A")
    phone = patient.get("phone_number", "N/A")
    email = patient.get("email", "N/A")
    blood_type = patient.get("blood_type") or "Not set"
    height_cm = patient.get("height_cm") or 0.0
    weight_kg = patient.get("weight_kg") or 0.0
    emergency_name = patient.get("emergency_contact_name") or "Not provided"
    emergency_phone = patient.get("emergency_contact_phone") or "Not provided"
    doctor_name = patient.get("doctor_name") or "Not assigned"
    doctor_phone = patient.get("doctor_phone") or "N/A"
    active_code = st.session_state.get("language", "en")
    lang_pref = "English" if active_code == "en" else ("Hindi" if active_code == "hi" else (patient.get("language_preference") or "English"))
    reg_date = str(patient.get("created_at") or "")[:10]

    bmi_info = calculate_bmi(weight_kg if weight_kg > 0 else None, height_cm if height_cm > 0 else None)
    allergies = db.get_allergies(patient_id)

    # ═════════════════════════════════════════════════════════════════
    # 1. WELCOME & PATIENT IDENTITY BANNER
    # ═════════════════════════════════════════════════════════════════
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, rgba(30, 58, 138, 0.35) 0%, rgba(15, 23, 42, 0.8) 100%);
                border: 1px solid rgba(56, 189, 248, 0.25); border-radius: 16px; padding: 22px 26px; margin-bottom: 24px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);'>
        <div style='display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;'>
            <div>
                <span style='background: rgba(56, 189, 248, 0.15); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.3);
                             padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 600;'>
                    PATIENT ID #{patient_id}
                </span>
                <h2 style='color: #ffffff; margin: 8px 0 4px 0; font-size: 1.8rem; font-weight: 700;'>
                    👤 {full_name}
                </h2>
                <p style='color: #94a3b8; margin: 0; font-size: 0.95rem;'>
                    @{username} • {email} • 📞 {phone} • Registered: {reg_date}
                </p>
            </div>
            <div style='text-align: right;'>
                <span style='background: {bmi_info["bg"]}; color: {bmi_info["color"]}; border: 1px solid {bmi_info["color"]};
                             padding: 6px 14px; border-radius: 12px; font-size: 0.9rem; font-weight: 600;'>
                    BMI: {bmi_info["value"]} ({bmi_info["label"]})
                </span>
                <p style='color: #cbd5e1; font-size: 0.85rem; margin: 8px 0 0 0;'>
                    Preferred Language: <b style='color:#38bdf8;'>{lang_pref}</b>
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ═════════════════════════════════════════════════════════════════
    # 2. VITAL REGISTRATION RECORDS GRID
    # ═════════════════════════════════════════════════════════════════
    st.markdown("<h3 style='color: #f8fafc; font-size: 1.25rem; margin-bottom: 14px;'>📊 Patient Registration & Vital Records</h3>", unsafe_allow_html=True)

    v1, v2, v3, v4, v5 = st.columns(5)

    with v1:
        st.markdown(f"""
        <div style='background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(56, 189, 248, 0.2); border-radius: 12px; padding: 16px; text-align: center;'>
            <p style='color: #94a3b8; font-size: 0.8rem; text-transform: uppercase; margin: 0 0 4px 0; font-weight: 600;'>⚖️ Weight</p>
            <p style='color: #38bdf8; font-size: 1.6rem; font-weight: 700; margin: 0;'>{weight_kg} <span style='font-size: 0.9rem; font-weight: 400;'>kg</span></p>
        </div>
        """, unsafe_allow_html=True)

    with v2:
        st.markdown(f"""
        <div style='background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(56, 189, 248, 0.2); border-radius: 12px; padding: 16px; text-align: center;'>
            <p style='color: #94a3b8; font-size: 0.8rem; text-transform: uppercase; margin: 0 0 4px 0; font-weight: 600;'>📏 Height</p>
            <p style='color: #38bdf8; font-size: 1.6rem; font-weight: 700; margin: 0;'>{height_cm} <span style='font-size: 0.9rem; font-weight: 400;'>cm</span></p>
        </div>
        """, unsafe_allow_html=True)

    with v3:
        st.markdown(f"""
        <div style='background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(239, 68, 68, 0.25); border-radius: 12px; padding: 16px; text-align: center;'>
            <p style='color: #94a3b8; font-size: 0.8rem; text-transform: uppercase; margin: 0 0 4px 0; font-weight: 600;'>🩸 Blood Group</p>
            <p style='color: #ef4444; font-size: 1.6rem; font-weight: 700; margin: 0;'>{blood_type}</p>
        </div>
        """, unsafe_allow_html=True)

    with v4:
        st.markdown(f"""
        <div style='background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(16, 185, 129, 0.2); border-radius: 12px; padding: 16px; text-align: center;'>
            <p style='color: #94a3b8; font-size: 0.8rem; text-transform: uppercase; margin: 0 0 4px 0; font-weight: 600;'>🎂 Age & Sex</p>
            <p style='color: #10b981; font-size: 1.4rem; font-weight: 700; margin: 0;'>{age} <span style='font-size: 0.9rem; font-weight: 400;'>yrs • {gender}</span></p>
        </div>
        """, unsafe_allow_html=True)

    with v5:
        allergy_color = "#ef4444" if allergies else "#10b981"
        st.markdown(f"""
        <div style='background: rgba(15, 23, 42, 0.7); border: 1px solid {allergy_color}33; border-radius: 12px; padding: 16px; text-align: center;'>
            <p style='color: #94a3b8; font-size: 0.8rem; text-transform: uppercase; margin: 0 0 4px 0; font-weight: 600;'>🛡️ Known Allergies</p>
            <p style='color: {allergy_color}; font-size: 1.6rem; font-weight: 700; margin: 0;'>{len(allergies)} <span style='font-size: 0.9rem; font-weight: 400;'>drugs</span></p>
        </div>
        """, unsafe_allow_html=True)

    # Secondary Contacts Card
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div style='background: rgba(15, 23, 42, 0.5); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 14px 18px;'>
            <h5 style='color: #f59e0b; margin: 0 0 6px 0;'>🚨 Emergency Contact</h5>
            <p style='color: #cbd5e1; margin: 0; font-size: 0.9rem;'>
                <b>{emergency_name}</b> • Phone: <span style='color:#38bdf8;'>{emergency_phone}</span>
            </p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div style='background: rgba(15, 23, 42, 0.5); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 14px 18px;'>
            <h5 style='color: #38bdf8; margin: 0 0 6px 0;'>👨‍⚕️ Assigned Doctor</h5>
            <p style='color: #cbd5e1; margin: 0; font-size: 0.9rem;'>
                <b>{doctor_name}</b> • Phone: <span style='color:#38bdf8;'>{doctor_phone}</span>
            </p>
        </div>
        """, unsafe_allow_html=True)

    # ═════════════════════════════════════════════════════════════════
    # 3. EDIT PROFILE & VITALS EXPANDER
    # ═════════════════════════════════════════════════════════════════
    with st.expander("✏️ Update Registration Vitals (Weight, Height, Contacts)", expanded=False):
        st.markdown("<p style='color:#94a3b8; font-size:0.85rem;'>Keep your registration vitals up-to-date so MedAssist calculates dosages and risk factors accurately.</p>", unsafe_allow_html=True)

        up1, up2, up3 = st.columns(3)
        with up1:
            new_weight = st.number_input("Weight (kg)", min_value=5.0, max_value=300.0, value=float(weight_kg) if weight_kg > 0 else 65.0, step=0.5, key="edit_weight")
            new_phone = st.text_input("Phone Number", value=phone if phone != "N/A" else "", key="edit_phone")
        with up2:
            new_height = st.number_input("Height (cm)", min_value=40.0, max_value=250.0, value=float(height_cm) if height_cm > 0 else 165.0, step=0.5, key="edit_height")
            new_blood = st.selectbox("Blood Group", ["O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-"], index=max(0, ["O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-"].index(blood_type)) if blood_type in ["O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-"] else 0, key="edit_blood")
        with up3:
            new_em_name = st.text_input("Emergency Contact Person", value=emergency_name if emergency_name != "Not provided" else "", key="edit_em_name")
            new_em_phone = st.text_input("Emergency Phone", value=emergency_phone if emergency_phone != "Not provided" else "", key="edit_em_phone")

        up3_1, up3_2 = st.columns([1, 1])
        with up3_1:
            lang_choices = ["English", "Hindi", "Bengali", "Tamil", "Telugu", "Marathi"]
            curr_choice_idx = lang_choices.index(lang_pref) if lang_pref in lang_choices else 0
            new_lang = st.selectbox("Preferred Language (पसंदीदा भाषा)", lang_choices, index=curr_choice_idx, key="edit_lang_choice")

        col_save, _ = st.columns([1, 4])
        with col_save:
            if st.button("💾 Save Changes", key="save_profile_vitals_btn", use_container_width=True, type="primary"):
                success, msg = db.update_patient(
                    patient_id,
                    weight_kg=new_weight,
                    height_cm=new_height,
                    blood_type=new_blood,
                    phone_number=new_phone,
                    emergency_contact_name=new_em_name,
                    emergency_contact_phone=new_em_phone,
                    language_preference=new_lang
                )
                if success:
                    st.session_state.language = "hi" if new_lang == "Hindi" else "en"
                    if "floating_bot_history" in st.session_state:
                        del st.session_state.floating_bot_history
                    st.success("✅ Profile records updated successfully!")
                    st.rerun()
                else:
                    st.error(f"Failed to update: {msg}")

    # ═════════════════════════════════════════════════════════════════
    # 4. PATIENT ALLERGIES & ADVERSE DRUG REACTION RECORDS
    # ═════════════════════════════════════════════════════════════════
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom: 12px;'>
        <div>
            <h3 style='color: #f8fafc; font-size: 1.3rem; margin: 0;'>🛡️ Patient Drug Allergy & Adverse Reaction Records</h3>
            <p style='color: #94a3b8; font-size: 0.85rem; margin: 4px 0 0 0;'>
                MedAssist strictly protects you by avoiding all recorded allergic drugs in recommendations across all modules.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not allergies:
        st.markdown("""
        <div style='background: rgba(16, 185, 129, 0.08); border: 1px dashed rgba(16, 185, 129, 0.3); border-radius: 12px; padding: 20px; text-align: center;'>
            <p style='color: #10b981; font-size: 1rem; margin: 0; font-weight: 600;'>✅ No Drug Allergies Recorded</p>
            <p style='color: #94a3b8; font-size: 0.85rem; margin: 6px 0 0 0;'>
                If you ever face an allergy, rash, or side effect after taking any medicine, record it below so our model will remember it and protect you in the future.
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        for idx, item in enumerate(allergies):
            med_name = item.get("medicine_name", "Unknown Medicine")
            severity = item.get("severity", "Moderate")
            symptoms = item.get("symptoms", "Not specified")
            notes = item.get("notes", "")
            date_str = str(item.get("reaction_date") or item.get("created_at") or "")[:10]
            allergy_id = item.get("allergy_id")

            if severity == "Severe":
                sev_color = "#ef4444"
                sev_bg = "rgba(239, 68, 68, 0.15)"
                sev_emoji = "🚨"
            elif severity == "Moderate":
                sev_color = "#f59e0b"
                sev_bg = "rgba(245, 158, 11, 0.15)"
                sev_emoji = "⚠️"
            else:
                sev_color = "#38bdf8"
                sev_bg = "rgba(56, 189, 248, 0.15)"
                sev_emoji = "ℹ️"

            col_allg, col_del = st.columns([5, 1])

            with col_allg:
                st.markdown(f"""
                <div style='background: rgba(15, 23, 42, 0.7); border-left: 4px solid {sev_color}; border-radius: 8px; padding: 12px 16px; margin-bottom: 8px;'>
                    <div style='display:flex; justify-content:space-between; align-items:center;'>
                        <h4 style='color:#f8fafc; margin:0; font-size:1.05rem;'>{sev_emoji} <b>{med_name}</b></h4>
                        <span style='background:{sev_bg}; color:{sev_color}; padding:2px 10px; border-radius:12px; font-size:0.75rem; font-weight:700;'>
                            {severity.upper()} REACTION
                        </span>
                    </div>
                    <p style='color:#cbd5e1; font-size:0.85rem; margin:6px 0 2px 0;'>
                        <b>Symptoms Faced:</b> {symptoms}
                    </p>
                    {f"<p style='color:#94a3b8; font-size:0.8rem; margin:0;'><b>Notes:</b> {notes}</p>" if notes else ""}
                    <p style='color:#64748b; font-size:0.75rem; margin:4px 0 0 0;'>Reported on: {date_str}</p>
                </div>
                """, unsafe_allow_html=True)

            with col_del:
                if st.button("🗑️ Remove", key=f"del_allg_{allergy_id}_{idx}", use_container_width=True):
                    db.delete_allergy(patient_id, allergy_id)
                    st.success(f"Removed record for {med_name}")
                    st.rerun()

    # ═════════════════════════════════════════════════════════════════
    # 5. ADD / REPORT NEW ALLERGY FORM
    # ═════════════════════════════════════════════════════════════════
    with st.expander("➕ Report / Add New Medicine Allergy or Reaction", expanded=False):
        st.markdown("<p style='color:#94a3b8; font-size:0.85rem;'>If you experienced an allergy, vomiting, rash, or side effect from any medicine, record it here.</p>", unsafe_allow_html=True)

        a_col1, a_col2 = st.columns(2)
        with a_col1:
            allg_med = st.text_input("Medicine / Drug Name *", placeholder="e.g. Paracetamol, Ibuprofen, Amoxicillin, Aspirin...", key="new_allg_med")
            allg_sev = st.selectbox("Severity of Reaction *", ["Severe", "Moderate", "Mild"], index=1, key="new_allg_sev")

        with a_col2:
            allg_symp = st.text_input("Symptoms Experienced", placeholder="e.g. Skin rash, facial swelling, vomiting, itching, nausea...", key="new_allg_symp")
            allg_gen = st.text_input("Generic / Salt Name (Optional)", placeholder="e.g. Acetaminophen, NSAID...", key="new_allg_gen")

        allg_notes = st.text_area("Additional Notes / Reaction Details", placeholder="What happened after taking this medicine? How long after did the reaction start?", height=65, key="new_allg_notes")

        if st.button("🛡️ Save to My Allergy Records", key="save_new_allg_btn", use_container_width=True, type="primary"):
            if not allg_med or not allg_med.strip():
                st.error("Please enter the medicine name.")
            else:
                success, msg = db.add_allergy(
                    patient_id=patient_id,
                    medicine_name=allg_med.strip(),
                    severity=allg_sev,
                    symptoms=allg_symp.strip() or "Allergic reaction",
                    generic_name=allg_gen.strip(),
                    notes=allg_notes.strip()
                )
                if success:
                    st.success(f"✅ Allergy to **{allg_med}** recorded! MedAssist will strictly avoid recommending this drug.")
                    st.rerun()
                else:
                    st.error(f"Failed to record allergy: {msg}")
