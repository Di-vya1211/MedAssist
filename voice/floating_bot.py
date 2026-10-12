"""
MedAssist - Cute Floating 3D AI Health Companion Bot
Fixed bottom-right corner interactive companion that gently floats/bobs on the screen
with the user's 3D robot avatar and 'How may I help you? 👋' speech bubble.
Clicking the robot opens the intelligent medical dialogue where the bot assists
the patient with symptom checking, medication questions, and allergy safeguards.
"""

import os
import base64
import streamlit as st
from typing import Optional
from voice.voice_assistant import conversational_assistant

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AVATAR_PATH = os.path.join(BASE_DIR, "assets", "bot_avatar.png")


def get_bot_avatar_b64() -> str:
    """Returns base64 encoded string of the 3D robot image."""
    if os.path.exists(AVATAR_PATH):
        try:
            with open(AVATAR_PATH, "rb") as f:
                return base64.b64encode(f.read()).decode("utf-8")
        except Exception:
            pass
    return ""


def init_floating_bot_state():
    """Initializes session state for the floating bot dialogue matching active language."""
    user_lang = st.session_state.get("language", "en")
    is_hindi = (user_lang == "hi")
    greeting = (
        "नमस्ते! 👋 मैं आपका MedAssist AI साथी हूँ। मैं आज आपकी क्या सहायता कर सकता हूँ? "
        "आप मुझसे किसी भी बीमारी, दवा, लक्षण, या स्वास्थ्य संबंधी सवाल पूछ सकते हैं।"
        if is_hindi else
        "Hello! 👋 I'm your MedAssist AI Companion. How may I help you today? "
        "You can ask me about symptoms, medicines, side effects, precautions, or any health concern."
    )
    if "floating_bot_history" not in st.session_state or not st.session_state.floating_bot_history:
        st.session_state.floating_bot_history = [
            {
                "role": "assistant",
                "content": greeting,
                "audio_path": None,
                "allergy_recorded": None
            }
        ]
        st.session_state.floating_bot_lang = user_lang
    elif st.session_state.get("floating_bot_lang") != user_lang and len(st.session_state.floating_bot_history) <= 1:
        st.session_state.floating_bot_history[0]["content"] = greeting
        st.session_state.floating_bot_lang = user_lang


def on_floating_bot_dialog_dismiss():
    """Resets dialog open state when dismissed via X button or backdrop click."""
    st.session_state.floating_bot_dialog_open = False


@st.dialog("🤖 MedAssist AI Companion", width="small", on_dismiss=on_floating_bot_dialog_dismiss)
def open_medassist_bot_dialog(patient_id: Optional[int] = None, patient_db = None):
    """
    Interactive clinical dialogue modal where the 3D robot greets the patient
    and answers whatever clinical or medical questions they ask.
    """
    init_floating_bot_state()
    b64 = get_bot_avatar_b64()
    is_hindi = st.session_state.get("language", "en") == "hi"

    # Header Card with the 3D Robot Image
    st.markdown(f"""
    <div style='display: flex; align-items: center; gap: 12px; background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(56, 189, 248, 0.3); border-radius: 14px; padding: 10px 14px; margin-bottom: 10px; box-shadow: 0 4px 16px rgba(0,0,0,0.3);'>
        <img src='data:image/png;base64,{b64}' style='width: 48px; height: 48px; border-radius: 50%; border: 2px solid #38bdf8; box-shadow: 0 4px 14px rgba(2, 132, 199, 0.5); object-fit: cover; background: #0b0f19;' />
        <div>
            <h3 style='margin: 0; color: #f8fafc; font-size: 1.15rem; font-weight: 700;'>MedAssist AI Companion</h3>
            <p style='margin: 2px 0 0 0; color: #10b981; font-size: 0.8rem; font-weight: 600;'>🟢 Online • Ready to help</p>
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
        <div style='background: rgba(239, 68, 68, 0.12); border: 1px solid rgba(239, 68, 68, 0.35); border-radius: 8px; padding: 6px 12px; margin-bottom: 10px; font-size: 0.78rem; color: #fca5a5;'>
            🛡️ <b>Active Allergy Guard:</b> Protecting you against {crit_str}
        </div>
        """, unsafe_allow_html=True)

    # Scrollable Chat History Container
    st.markdown("<div style='max-height: 250px; min-height: 140px; overflow-y: auto; padding-right: 4px; margin-bottom: 8px;'>", unsafe_allow_html=True)
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
        st.markdown("<p style='color: #94a3b8; font-size: 0.76rem; margin: 2px 0 6px 0; font-weight: 600;'>💡 Quick questions:</p>", unsafe_allow_html=True)
        chips = [
            ("🤒 Cold/Fever", "What medicines and remedies help with common cold and fever?"),
            ("💊 Paracetamol", "Is Paracetamol safe and what is the typical dosage?"),
            ("🛡️ Allergies", "What drug allergies do I have recorded in my profile?")
        ] if not is_hindi else [
            ("🤒 सर्दी-बुखार", "सर्दी और बुखार में क्या उपाय और दवाएं सुरक्षित हैं?"),
            ("💊 पैरासिटामोल", "पैरासिटामोल की सही खुराक और सावधानियां क्या हैं?"),
            ("🛡️ एलर्जी", "मेरी प्रोफाइल में कौन-कौन सी दवा एलर्जी दर्ज है?")
        ]
        q_cols = st.columns(3)
        for i, (label, query_text) in enumerate(chips):
            with q_cols[i]:
                if st.button(label, key=f"chip_dialog_{i}", use_container_width=True):
                    with st.spinner("🤖 Loading answer..." if not is_hindi else "🤖 उत्तर तैयार कर रहे हैं..."):
                        _process_bot_query(query_text, patient_id, patient_db)
                    st.rerun(scope="fragment")

    # In-dialog Voice Input: Direct Live Mic
    live_btn_text = "🎙️ Live Mic (लाइव बोलें)" if is_hindi else "🎙️ Live Mic (Speak Now)"
    if st.button(live_btn_text, key="dialog_live_mic_btn", use_container_width=True, type="primary"):
        user_active_lang = st.session_state.get("language", "en")
        prompt_lang = "बोलिए..." if is_hindi else "Speak now in English or Hindi..."
        with st.spinner(f"🔴 Live Mic Active... {prompt_lang}"):
            from voice.voice_service import voice_service
            ok, v_text, _ = voice_service.record_live_microphone(timeout=5, phrase_time_limit=8, hinted_lang=user_active_lang)
            if ok and v_text:
                with st.spinner("🤖 Thinking..." if not is_hindi else "🤖 विचार कर रहे हैं..."):
                    _process_bot_query(v_text, patient_id, patient_db)
                st.rerun(scope="fragment")
            else:
                st.warning("⚠️ No speech captured. Please speak closer to microphone and try again!")

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
        with st.spinner("🤖 MedAssist is thinking & verifying health guidelines..." if not is_hindi else "🤖 विचार कर रहे हैं..."):
            _process_bot_query(user_input.strip(), patient_id, patient_db)
        st.rerun(scope="fragment")

    # Reset Chat and Close Dialog Buttons
    col_clr, col_close = st.columns([1, 1])
    with col_clr:
        if st.button("🗑️ Reset Chat", key="clear_chat_dialog_btn", use_container_width=True):
            st.session_state.floating_bot_history = []
            init_floating_bot_state()
            st.rerun(scope="fragment")
    with col_close:
        if st.button("✕ Close / बंद करें", key="close_chat_dialog_btn", use_container_width=True):
            st.session_state.floating_bot_dialog_open = False
            st.rerun(scope="app")


def _process_bot_query(query: str, patient_id: Optional[int], patient_db):
    """Processes the query with the conversational assistant and updates history."""
    if not query:
        return

    st.session_state.floating_bot_dialog_open = True

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
    Renders the small 3D robot avatar on the bottom-right corner.
    Floats continuously with a gentle bobbing animation and 'How may I help you? 👋' tooltip.
    Clicking it opens the conversational AI health assistant dialogue natively.
    """
    init_floating_bot_state()
    b64 = get_bot_avatar_b64()
    is_hindi = st.session_state.get("language", "en") == "hi"
    speech_text = "How may I help you? 👋" if not is_hindi else "मैं आपकी क्या सहायता करूँ? 👋"

    # Floating CSS for both the 3D robot visual, invisible native button layer, and side card dialog
    st.html(f"""
    <style>
    /* Fixed Floating Bot Widget (Bottom-Right Corner) */
    #medassist-bot-container {{
        position: fixed !important;
        bottom: 25px !important;
        right: 25px !important;
        z-index: 100000005 !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: flex-end !important;
        gap: 8px !important;
        pointer-events: none !important;
    }}

    /* Tooltip Speech Bubble Floating Above the Bot */
    .bot-speech-bubble {{
        background: #1e293b;
        color: #f8fafc;
        border: 1.5px solid #38bdf8;
        border-radius: 14px;
        padding: 6px 14px;
        font-size: 0.82rem;
        font-weight: 700;
        box-shadow: 0 4px 18px rgba(0, 0, 0, 0.5), 0 0 10px rgba(56, 189, 248, 0.25);
        animation: botFloatingBob 3s ease-in-out infinite;
        white-space: nowrap;
        position: relative;
        cursor: pointer;
        user-select: none;
    }}
    .bot-speech-bubble::after {{
        content: '';
        position: absolute;
        bottom: -6px;
        right: 24px;
        width: 10px;
        height: 10px;
        background: #1e293b;
        border-right: 1.5px solid #38bdf8;
        border-bottom: 1.5px solid #38bdf8;
        transform: rotate(45deg);
    }}

    /* Hide speech bubble when chat dialog card is open so they don't overlap */
    body:has(div[data-testid="stDialog"]) .bot-speech-bubble,
    body:has(div.stDialog) .bot-speech-bubble,
    body:has(div[role="dialog"]) .bot-speech-bubble {{
        display: none !important;
    }}

    /* 3D Robot Head Circular Visual */
    .bot-avatar-circle {{
        width: 72px;
        height: 72px;
        border-radius: 50%;
        background-color: #0b0f19;
        border: 3px solid #38bdf8;
        box-shadow: 0 8px 24px rgba(2, 132, 199, 0.6), 0 0 16px rgba(56, 189, 248, 0.4);
        cursor: pointer;
        animation: botFloatingBob 3s ease-in-out infinite;
        overflow: hidden;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: transform 0.25s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.25s ease;
        user-select: none;
        pointer-events: none !important;
    }}

    .bot-avatar-circle img {{
        width: 100%;
        height: 100%;
        object-fit: cover;
        pointer-events: none;
    }}

    .bot-avatar-circle:hover {{
        transform: scale(1.12) translateY(-2px);
        box-shadow: 0 14px 35px rgba(56, 189, 248, 0.85), 0 0 25px rgba(56, 189, 248, 0.6);
        border-color: #ffffff;
    }}

    /* Visual glow indication when chat dialog is open */
    body:has(div[data-testid="stDialog"]) .bot-avatar-circle,
    body:has(div.stDialog) .bot-avatar-circle,
    body:has(div[role="dialog"]) .bot-avatar-circle {{
        border-color: #38bdf8 !important;
        box-shadow: 0 0 25px rgba(56, 189, 248, 0.9), 0 0 15px rgba(244, 63, 94, 0.5) !important;
    }}

    /* Gentle Floating Bobbing Keyframes */
    @keyframes botFloatingBob {{
        0% {{
            transform: translateY(0px);
        }}
        50% {{
            transform: translateY(-8px);
        }}
        100% {{
            transform: translateY(0px);
        }}
    }}

    /* Position the native Streamlit button layer right on top of the 72px robot */
    div[data-testid="stElementContainer"]:has(#medassist-native-btn-marker) + div[data-testid="stElementContainer"] {{
        position: fixed !important;
        bottom: 25px !important;
        right: 25px !important;
        width: 76px !important;
        height: 76px !important;
        z-index: 100000050 !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow: hidden !important;
        border-radius: 50% !important;
        animation: botFloatingBob 3s ease-in-out infinite !important;
    }}

    body:has(div[data-testid="stDialog"]) div[data-testid="stElementContainer"]:has(#medassist-native-btn-marker) + div[data-testid="stElementContainer"],
    body:has(div.stDialog) div[data-testid="stElementContainer"]:has(#medassist-native-btn-marker) + div[data-testid="stElementContainer"],
    body:has(div[role="dialog"]) div[data-testid="stElementContainer"]:has(#medassist-native-btn-marker) + div[data-testid="stElementContainer"] {{
        display: none !important;
    }}

    div[data-testid="stElementContainer"]:has(#medassist-native-btn-marker) + div[data-testid="stElementContainer"] button {{
        width: 76px !important;
        height: 76px !important;
        min-width: 76px !important;
        min-height: 76px !important;
        border-radius: 50% !important;
        opacity: 0 !important;
        cursor: pointer !important;
        border: none !important;
        background: transparent !important;
        padding: 0 !important;
        margin: 0 !important;
        pointer-events: auto !important;
    }}

    /* ========================================================
       FLOATING AI BOT DIALOG AS SIDE SQUARE CARD (BOTTOM-RIGHT)
       ======================================================== */
    /* 1. Backdrop / Outer Flex Container: Fullscreen, transparent, aligns content to bottom-right */
    div[data-baseweb="modal"],
    div[data-baseweb="modal"] > div,
    div[data-testid="stDialog"],
    div.stDialog,
    .e1mymz5c0 {{
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
    }}

    /* 2. Inner Dialog Card: Fixed at bottom-right corner directly above the 3D bot */
    div[data-testid="stDialog"] > div,
    div.stDialog > div,
    div[role="dialog"],
    .e1mymz5c1 {{
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
    }}

    /* Pop out directly from the bottom-right 3D bot */
    @keyframes botPopupFromBot {{
        0% {{
            opacity: 0;
            transform: scale(0.12) translateY(80px) translateX(40px);
        }}
        70% {{
            opacity: 1;
            transform: scale(1.03) translateY(-4px) translateX(-2px);
        }}
        100% {{
            opacity: 1;
            transform: scale(1) translateY(0) translateX(0);
        }}
    }}

    div[data-testid="stDialog"] h2,
    div.stDialog h2,
    div[role="dialog"] h2 {{
        font-size: 1.05rem !important;
        margin: 0 !important;
        padding: 0 !important;
        color: #f8fafc !important;
        font-weight: 700 !important;
    }}

    div[data-testid="stDialog"] button[aria-label="Close"],
    div.stDialog button[aria-label="Close"],
    div[role="dialog"] button[aria-label="Close"],
    .e1mymz5c3 {{
        color: #94a3b8 !important;
        top: 14px !important;
        right: 14px !important;
        font-size: 1.2rem !important;
        border-radius: 8px !important;
        transition: all 0.2s ease !important;
    }}
    div[data-testid="stDialog"] button[aria-label="Close"]:hover,
    div.stDialog button[aria-label="Close"]:hover,
    div[role="dialog"] button[aria-label="Close"]:hover,
    .e1mymz5c3:hover {{
        color: #f43f5e !important;
        background: rgba(244, 63, 94, 0.15) !important;
        transform: scale(1.1) !important;
    }}

    div[data-testid="stDialog"] > div::-webkit-scrollbar,
    div.stDialog > div::-webkit-scrollbar,
    div[role="dialog"]::-webkit-scrollbar,
    .e1mymz5c1::-webkit-scrollbar {{
        width: 6px !important;
    }}
    div[data-testid="stDialog"] > div::-webkit-scrollbar-thumb,
    div.stDialog > div::-webkit-scrollbar-thumb,
    div[role="dialog"]::-webkit-scrollbar-thumb,
    .e1mymz5c1::-webkit-scrollbar-thumb {{
        background: rgba(56, 189, 248, 0.3) !important;
        border-radius: 10px !important;
    }}
    </style>

    <div id="medassist-bot-container" onclick="medassistClickBotToggle()">
        <div class="bot-speech-bubble" onclick="medassistClickBotToggle(); event.stopPropagation();">
            {speech_text}
        </div>
        <div class="bot-avatar-circle" title="Click to chat with MedAssist AI / चैट खोलने या बंद करने के लिए क्लिक करें" onclick="medassistClickBotToggle(); event.stopPropagation();">
            <img src="data:image/png;base64,{b64}" alt="MedAssist AI Bot" />
        </div>
    </div>

    <script>
    function medassistClickBotToggle() {{
        var targets = [document];
        if (window.parent && window.parent.document) {{
            targets.push(window.parent.document);
        }}
        if (window.top && window.top.document) {{
            targets.push(window.top.document);
        }}
        for (var i = 0; i < targets.length; i++) {{
            try {{
                var btns = Array.from(targets[i].querySelectorAll('button'));
                var b = btns.find(function(x) {{
                    return x.textContent && x.textContent.indexOf('MEDASSIST_BOT_CLICK_ACTION') !== -1;
                }});
                if (b) {{
                    b.click();
                    return;
                }}
            }} catch(e) {{}}
        }}
    }}
    </script>
    """)

    # Native Streamlit clickable button anchor and button (Handles pure-python open/close toggle)
    st.markdown('<div id="medassist-native-btn-marker" style="display:none;"></div>', unsafe_allow_html=True)
    if st.button("MEDASSIST_BOT_CLICK_ACTION", key="medassist_native_floating_btn"):
        st.session_state.floating_bot_dialog_open = not st.session_state.get("floating_bot_dialog_open", False)
        st.rerun()

    if st.session_state.get("floating_bot_dialog_open", False):
        open_medassist_bot_dialog(patient_id, patient_db)
