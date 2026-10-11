"""
MedAssist - Cute Floating 3D AI Health Companion Bot
Displays a small floating 3D robot avatar on the bottom-right corner that
gently bobs up and down with a 'How may I help you? 👋' speech bubble.
When clicked, opens an intelligent clinical dialogue where the bot greets the user
and answers all their health, symptom, and medication questions with allergy safeguards.
"""

import os
import base64
import streamlit as st
from typing import Optional
from voice.voice_assistant import conversational_assistant

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AVATAR_PATH = os.path.join(BASE_DIR, "assets", "bot_avatar.png")


def get_bot_avatar_b64() -> str:
    """Returns base64 encoded string of the user-provided 3D robot image."""
    if os.path.exists(AVATAR_PATH):
        try:
            with open(AVATAR_PATH, "rb") as f:
                return base64.b64encode(f.read()).decode("utf-8")
        except Exception:
            pass
    return ""


def init_floating_bot_state():
    """Initializes session state for the floating bot."""
    if "floating_bot_history" not in st.session_state:
        is_hindi = st.session_state.get("language", "en") == "hi"
        greeting = (
            "नमस्ते! 👋 मैं आपका MedAssist AI साथी हूँ। मैं आज आपकी क्या सहायता कर सकता हूँ? "
            "आप मुझसे किसी भी बीमारी, दवा, लक्षण, या स्वास्थ्य संबंधी सवाल पूछ सकते हैं।"
            if is_hindi else
            "Hello! 👋 I'm your MedAssist AI Companion. How may I help you today? "
            "You can ask me about symptoms, medicines, side effects, precautions, or any health concern."
        )
        st.session_state.floating_bot_history = [
            {
                "role": "assistant",
                "content": greeting,
                "audio_path": None,
                "allergy_recorded": None
            }
        ]


@st.dialog("🤖 MedAssist AI Companion", width="medium")
def open_medassist_bot_dialog(patient_id: Optional[int] = None, patient_db = None):
    """
    Interactive modal dialog where the 3D bot greets the user
    and answers whatever clinical or medical questions they ask.
    """
    init_floating_bot_state()
    b64 = get_bot_avatar_b64()
    is_hindi = st.session_state.get("language", "en") == "hi"

    # Header Card with 3D Robot Image
    st.markdown(f"""
    <div style='display: flex; align-items: center; gap: 14px; background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(56, 189, 248, 0.3); border-radius: 14px; padding: 12px 16px; margin-bottom: 14px; box-shadow: 0 4px 16px rgba(0,0,0,0.3);'>
        <img src='data:image/png;base64,{b64}' style='width: 56px; height: 56px; border-radius: 50%; border: 2.5px solid #38bdf8; box-shadow: 0 4px 14px rgba(2, 132, 199, 0.5); object-fit: cover; background: #0b0f19;' />
        <div>
            <h3 style='margin: 0; color: #f8fafc; font-size: 1.25rem; font-weight: 700;'>MedAssist AI Assistant</h3>
            <p style='margin: 2px 0 0 0; color: #10b981; font-size: 0.82rem; font-weight: 600;'>🟢 Online • How may I help you today?</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Active Patient Allergies Safeguard Banner
    allergies = []
    if patient_db and patient_id:
        try:
            allergies = patient_db.get_allergies(patient_id)
        except Exception:
            pass
    if allergies:
        crit_str = ", ".join([a.get("medicine_name", "") for a in allergies[:3] if a.get("medicine_name")])
        st.markdown(f"""
        <div style='background: rgba(239, 68, 68, 0.12); border: 1px solid rgba(239, 68, 68, 0.35); border-radius: 8px; padding: 6px 12px; margin-bottom: 12px; font-size: 0.8rem; color: #fca5a5;'>
            🛡️ <b>Active Allergy Guard:</b> Protecting you against {crit_str}
        </div>
        """, unsafe_allow_html=True)

    # Scrollable Chat History Container
    st.markdown("<div style='max-height: 330px; overflow-y: auto; padding-right: 4px; margin-bottom: 10px;'>", unsafe_allow_html=True)
    for msg in st.session_state.floating_bot_history:
        role = msg.get("role", "assistant")
        content = msg.get("content", "")
        audio_path = msg.get("audio_path")
        allergy_rec = msg.get("allergy_recorded")

        avatar_img = f"data:image/png;base64,{b64}" if role == "assistant" else "🧑‍⚕️"
        with st.chat_message(role, avatar=avatar_img):
            st.write(content)
            if allergy_rec:
                st.warning(f"🚨 **Allergy Recorded:** Successfully saved '{allergy_rec}' into your permanent health profile!")
            if audio_path and os.path.exists(audio_path):
                st.audio(audio_path, format="audio/mp3")
    st.markdown("</div>", unsafe_allow_html=True)

    # Quick Suggestion Chips (Available for instant 1-click answers)
    if len(st.session_state.floating_bot_history) <= 3:
        st.markdown("<p style='color: #94a3b8; font-size: 0.78rem; margin: 4px 0 6px 0;'>Quick suggestions:</p>", unsafe_allow_html=True)
        chips = [
            ("🤒 Cold & Fever", "What medicines and remedies help with common cold and fever?"),
            ("💊 Paracetamol", "Is Paracetamol safe and what is the typical dosage?"),
            ("🛡️ My Allergies", "What drug allergies do I have recorded in my profile?")
        ] if not is_hindi else [
            ("🤒 सर्दी-बुखार", "सर्दी और बुखार में क्या उपाय और दवाएं सुरक्षित हैं?"),
            ("💊 पैरासिटामोल", "पैरासिटामोल की सही खुराक और सावधानियां क्या हैं?"),
            ("🛡️ मेरी एलर्जी", "मेरी प्रोफाइल में कौन-कौन सी दवा एलर्जी दर्ज है?")
        ]
        q_cols = st.columns(3)
        for i, (label, query_text) in enumerate(chips):
            with q_cols[i]:
                if st.button(label, key=f"chip_dialog_{i}", use_container_width=True):
                    _process_bot_query(query_text, patient_id, patient_db)
                    st.rerun()

    # Question Input Form
    placeholder = "अपना सवाल यहाँ लिखें..." if is_hindi else "Ask any medical or health question..."
    with st.form("dialog_bot_input_form", clear_on_submit=True):
        col_in, col_btn = st.columns([4, 1])
        with col_in:
            user_input = st.text_input(
                "Your Question",
                placeholder=placeholder,
                label_visibility="collapsed",
                key="dialog_bot_text_input"
            )
        with col_btn:
            ask_submitted = st.form_submit_button("Ask ➤", type="primary", use_container_width=True)

    if ask_submitted and user_input and user_input.strip():
        _process_bot_query(user_input.strip(), patient_id, patient_db)
        st.rerun()

    # Clear chat / Reset Button
    col_clr, _ = st.columns([1.5, 3])
    with col_clr:
        if st.button("🗑️ Reset Chat", key="clear_chat_dialog_btn", use_container_width=True):
            st.session_state.floating_bot_history = []
            init_floating_bot_state()
            st.rerun()


def _process_bot_query(query: str, patient_id: Optional[int], patient_db):
    """Processes the query with the conversational assistant and updates history."""
    if not query:
        return

    # Add user message to history
    st.session_state.floating_bot_history.append({
        "role": "user",
        "content": query,
        "audio_path": None,
        "allergy_recorded": None
    })

    patient_profile = st.session_state.get("patient_profile")
    active_lang = st.session_state.get("language")

    # Get clinical response from ConversationalVoiceAssistant
    result = conversational_assistant.process_message(
        user_message=query,
        patient_id=patient_id,
        patient_db=patient_db,
        patient_profile=patient_profile,
        force_language=active_lang
    )

    response_text = result.get("response_text", "I am here to help you. Please ask any health question.")
    audio_path = result.get("audio_path")
    allergy_detected = result.get("allergy_detected", False)
    allergy_info = result.get("allergy_info") or {}
    med_name = allergy_info.get("medicine_name") if allergy_detected else None

    # Add bot response to history
    st.session_state.floating_bot_history.append({
        "role": "assistant",
        "content": response_text,
        "audio_path": audio_path,
        "allergy_recorded": med_name
    })


def render_floating_bot(patient_id: Optional[int] = None, patient_db = None):
    """
    Renders the small 3D robot avatar (Image 2) on the bottom-right corner.
    Floats continuously with a bobbing animation and 'How may I help you? 👋' tooltip.
    Clicking it opens the conversational AI health assistant dialogue.
    """
    init_floating_bot_state()
    b64 = get_bot_avatar_b64()
    is_hindi = st.session_state.get("language", "en") == "hi"
    speech_text = "How may I help you? 👋" if not is_hindi else "मैं आपकी क्या सहायता करूँ? 👋"

    # Inject Floating Bot CSS
    st.markdown(f"""
    <style>
    /* Fixed Floating Bot Container at Bottom-Right */
    div[data-testid="stVerticalBlock"]:has(> div #floating-bot-marker),
    div[data-testid="stElementContainer"]:has(> div #floating-bot-marker) {{
        position: fixed !important;
        bottom: 24px !important;
        right: 24px !important;
        z-index: 9999999 !important;
        width: 76px !important;
        height: 76px !important;
        max-width: 76px !important;
        max-height: 76px !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow: visible !important;
    }}

    /* Tooltip Speech Bubble Floating Above the Bot */
    .floating-bot-speech-bubble {{
        position: fixed;
        bottom: 110px;
        right: 20px;
        background: #1e293b;
        color: #f8fafc;
        border: 1.5px solid #38bdf8;
        border-radius: 14px;
        padding: 6px 14px;
        font-size: 0.82rem;
        font-weight: 700;
        box-shadow: 0 4px 18px rgba(0, 0, 0, 0.5), 0 0 10px rgba(56, 189, 248, 0.2);
        z-index: 9999999;
        animation: botFloatingBob 3s ease-in-out infinite;
        pointer-events: none;
        white-space: nowrap;
    }}
    .floating-bot-speech-bubble::after {{
        content: '';
        position: absolute;
        bottom: -6px;
        right: 28px;
        width: 10px;
        height: 10px;
        background: #1e293b;
        border-right: 1.5px solid #38bdf8;
        border-bottom: 1.5px solid #38bdf8;
        transform: rotate(45deg);
    }}

    /* 3D Robot Head Circular Floating Button */
    div[data-testid="stVerticalBlock"]:has(> div #floating-bot-marker) button,
    div[data-testid="stElementContainer"]:has(> div #floating-bot-marker) button {{
        width: 72px !important;
        height: 72px !important;
        min-width: 72px !important;
        min-height: 72px !important;
        max-width: 72px !important;
        max-height: 72px !important;
        border-radius: 50% !important;
        background-image: url('data:image/png;base64,{b64}') !important;
        background-size: 90% !important;
        background-position: center !important;
        background-repeat: no-repeat !important;
        background-color: #0b0f19 !important;
        border: 3px solid #38bdf8 !important;
        box-shadow: 0 8px 24px rgba(2, 132, 199, 0.6), 0 0 16px rgba(56, 189, 248, 0.4) !important;
        cursor: pointer !important;
        animation: botFloatingBob 3s ease-in-out infinite !important;
        padding: 0 !important;
        margin: 0 !important;
        color: transparent !important;
        overflow: hidden !important;
        transition: transform 0.25s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.25s ease !important;
    }}

    div[data-testid="stVerticalBlock"]:has(> div #floating-bot-marker) button:hover,
    div[data-testid="stElementContainer"]:has(> div #floating-bot-marker) button:hover {{
        transform: scale(1.12) translateY(-2px) !important;
        box-shadow: 0 14px 35px rgba(56, 189, 248, 0.85), 0 0 25px rgba(56, 189, 248, 0.6) !important;
        border-color: #ffffff !important;
    }}

    /* Hide button text so only the 3D robot face is shown */
    div[data-testid="stVerticalBlock"]:has(> div #floating-bot-marker) button *,
    div[data-testid="stElementContainer"]:has(> div #floating-bot-marker) button * {{
        display: none !important;
    }}

    /* Gentle Floating Bobbing Keyframes */
    @keyframes botFloatingBob {{
        0% {{
            transform: translateY(0px);
        }}
        50% {{
            transform: translateY(-9px);
        }}
        100% {{
            transform: translateY(0px);
        }}
    }}
    </style>
    <div class="floating-bot-speech-bubble">{speech_text}</div>
    <div id="floating-bot-marker"></div>
    """, unsafe_allow_html=True)

    # Clickable Floating Bot Button
    if st.button("🤖", key="floating_bot_circle_btn", help="Click to chat with MedAssist AI"):
        open_medassist_bot_dialog(patient_id, patient_db)
