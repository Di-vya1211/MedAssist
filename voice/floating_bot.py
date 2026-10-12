"""
MedAssist - Tactical High-Tech AI Health Companion HUD Dock
Fixed bottom-right corner tactical AI health companion pill dock.
High-density clinical aesthetic with telemetry status indicators, zero cartoon bobbing,
sharp hairline borders, and instant conversational health support with allergy safeguards.
"""

import os
import base64
import streamlit as st
from typing import Optional
from voice.voice_assistant import conversational_assistant
from core.instant_cache import get_instant_drug, get_instant_disease

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AVATAR_PATH = os.path.join(BASE_DIR, "assets", "bot_avatar.png")


def get_bot_avatar_b64() -> str:
    """Returns base64 encoded string of the avatar image."""
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
        "नमस्ते! 👋 मैं आपका MedAssist AI क्लीनिकल साथी हूँ। "
        "आप मुझसे किसी भी बीमारी, दवा, लक्षण, एलर्जी सुरक्षा, या रिपोर्ट के बारे में पूछ सकते हैं।"
        if is_hindi else
        "Hello! 👋 I am MedAssist AI Clinical Companion. "
        "You can query disease protocols, drug dosages, adverse interactions, or report findings with active allergy protection."
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


@st.dialog("⚡ MedAssist AI Clinical HUD", width="small", on_dismiss=on_floating_bot_dialog_dismiss)
def open_medassist_bot_dialog(patient_id: Optional[int] = None, patient_db = None):
    """
    Interactive clinical dialogue modal styled in high-density tactical dark theme.
    """
    init_floating_bot_state()
    b64 = get_bot_avatar_b64()
    is_hindi = st.session_state.get("language", "en") == "hi"

    # Clinical Telemetry Header Card with Bot Avatar
    st.markdown(f"""
    <div style='background: #080e1e; border: 1px solid rgba(56, 189, 248, 0.4); border-radius: 10px; padding: 10px 14px; margin-bottom: 12px; box-shadow: 0 4px 16px rgba(0,0,0,0.4); display: flex; align-items: center; gap: 12px;'>
        <img src="data:image/png;base64,{b64}" style="width: 44px; height: 44px; border-radius: 50%; border: 2px solid #38bdf8; object-fit: cover; flex-shrink: 0;" alt="Bot Avatar" />
        <div style='flex: 1;'>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <span style='font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 0.92rem; color: #38bdf8; font-weight: 700; letter-spacing: 0.02em;'>MedAssist AI Clinical Companion</span>
                <span style='font-family: monospace; font-size: 0.70rem; color: #10b981; background: rgba(16,185,129,0.1); border: 1px solid #10b981; padding: 1px 6px; border-radius: 4px;'>● ONLINE</span>
            </div>
            <p style='margin: 3px 0 0 0; color: #cbd5e1; font-size: 0.76rem;'>
                Clinical Decision Support • Active Allergy Safeguard Armed
            </p>
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
        <div style='background: rgba(239, 68, 68, 0.12); border: 1px solid rgba(239, 68, 68, 0.4); border-radius: 6px; padding: 6px 12px; margin-bottom: 10px; font-size: 0.78rem; color: #fca5a5;'>
            🛡️ <b>ALLERGY SHIELD ACTIVE:</b> Guarding against {crit_str}
        </div>
        """, unsafe_allow_html=True)

    # Scrollable Chat History Container
    st.markdown("<div style='max-height: 250px; min-height: 140px; overflow-y: auto; padding-right: 4px; margin-bottom: 8px;'>", unsafe_allow_html=True)
    for msg in st.session_state.floating_bot_history:
        role = msg.get("role", "assistant")
        content = msg.get("content", "")
        audio_path = msg.get("audio_path")
        allergy_rec = msg.get("allergy_recorded")

        avatar_img = "⚡" if role == "assistant" else "🧑‍⚕️"
        with st.chat_message(role, avatar=avatar_img):
            st.write(content)
            if allergy_rec:
                st.warning(f"🚨 **Allergy Recorded:** Stored '{allergy_rec}' in your health profile!")
            if audio_path and os.path.exists(audio_path):
                st.audio(audio_path, format="audio/mp3")
    st.markdown("</div>", unsafe_allow_html=True)

    # Quick Suggestion Chips (Available for instant 1-click answers)
    if len(st.session_state.floating_bot_history) <= 3:
        st.markdown("<p style='color: #64748b; font-size: 0.76rem; margin: 2px 0 6px 0; font-family: monospace; font-weight: 600;'>[QUICK JUMP PROTOCOLS]</p>", unsafe_allow_html=True)
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
    """Processes the query with fast instant cache or conversational assistant and updates history."""
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
    active_lang = st.session_state.get("language", "en")
    q_lower = query.lower().strip()

    # 1. Instant check for Profile Allergies query
    if any(k in q_lower for k in ["allergy", "allergies", "एलर्जी"]) and any(k in q_lower for k in ["profile", "my", "meri", "record", "दर्ज"]):
        allergies = patient_db.get_allergies(patient_id) if patient_db and patient_id else []
        if allergies:
            items = [f"• **{a.get('medicine_name')}** ({a.get('severity')} severity - {a.get('symptoms')})" for a in allergies]
            resp = "Here are your documented drug allergies:\n\n" + "\n".join(items) if active_lang != "hi" else "आपकी प्रोफाइल में दर्ज दवा एलर्जी निम्न हैं:\n\n" + "\n".join(items)
        else:
            resp = "You currently have no documented drug allergies in your profile. You can record any allergy anytime!" if active_lang != "hi" else "आपकी प्रोफाइल में कोई दवा एलर्जी दर्ज नहीं है। आप किसी भी दवा से रिएक्शन होने पर यहाँ दर्ज करा सकते हैं।"

        st.session_state.floating_bot_history.append({
            "role": "assistant",
            "content": resp,
            "audio_path": None,
            "allergy_recorded": None
        })
        return

    # 2. Instant check for Paracetamol query
    if "paracetamol" in q_lower or "पैरासिटामोल" in q_lower or "crocin" in q_lower or "dolo" in q_lower:
        d_res = get_instant_drug("paracetamol", target_lang=active_lang)
        if d_res and d_res.get("answer"):
            st.session_state.floating_bot_history.append({
                "role": "assistant",
                "content": d_res["answer"],
                "audio_path": None,
                "allergy_recorded": None
            })
            return

    # 3. Instant check for Cold/Fever query
    if "cold" in q_lower or "fever" in q_lower or "सर्दी" in q_lower or "जुकाम" in q_lower or "बुखार" in q_lower:
        dis_res = get_instant_disease("common cold", target_lang=active_lang)
        if dis_res:
            prec = "\n• " + "\n• ".join(dis_res.get("precautions", [])[:3])
            treat = "\n• " + "\n• ".join(dis_res.get("treatment", [])[:3])
            ans = f"**{dis_res['disease_name']}**\n\n{dis_res['description']}\n\n**Recommended Measures:**{prec}\n\n**Common Supportive Care:**{treat}"
            st.session_state.floating_bot_history.append({
                "role": "assistant",
                "content": ans,
                "audio_path": None,
                "allergy_recorded": None
            })
            return

    # 4. Fallback to conversational assistant with active language and allergies
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
    Renders the floating AI health companion robot avatar in the bottom-right corner.
    Crisp circular avatar with the 3D robot head image from assets/bot_avatar.png,
    speech bubble, subtle glowing ring, and instant dialog trigger.
    """
    init_floating_bot_state()
    b64 = get_bot_avatar_b64()
    is_hindi = st.session_state.get("language", "en") == "hi"
    speech_text = "Ask Me! 💬" if not is_hindi else "पूछिए! 💬"

    st.html(f"""
    <style>
    /* Fixed Bot Avatar Container */
    #medassist-bot-container {{
        position: fixed !important;
        bottom: 25px !important;
        right: 25px !important;
        z-index: 100000005 !important;
        display: flex !important;
        align-items: center !important;
        gap: 12px !important;
        cursor: pointer !important;
        pointer-events: auto !important;
    }}

    /* Floating Speech Bubble */
    .bot-speech-bubble {{
        background: #080e1e;
        color: #38bdf8;
        border: 1px solid #38bdf8;
        padding: 6px 14px;
        border-radius: 14px;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        font-size: 0.82rem;
        font-weight: 700;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.6);
        position: relative;
        white-space: nowrap;
        pointer-events: none;
        user-select: none;
        letter-spacing: 0.02em;
    }}

    .bot-speech-bubble::after {{
        content: '';
        position: absolute;
        right: -6px;
        top: calc(50% - 5px);
        width: 10px;
        height: 10px;
        background: #080e1e;
        border-right: 1px solid #38bdf8;
        border-bottom: 1px solid #38bdf8;
        transform: rotate(-45deg);
    }}

    /* Hide speech bubble when dialog is open so they don't overlap */
    body:has(div[data-testid="stDialog"]) .bot-speech-bubble,
    body:has(div.stDialog) .bot-speech-bubble,
    body:has(div[role="dialog"]) .bot-speech-bubble {{
        display: none !important;
    }}

    /* 3D Robot Head Circular Avatar Visual */
    .bot-avatar-circle {{
        width: 72px;
        height: 72px;
        border-radius: 50%;
        background-color: #080e1e;
        border: 2.5px solid #38bdf8;
        box-shadow: 0 8px 24px rgba(2, 132, 199, 0.6), 0 0 16px rgba(56, 189, 248, 0.4);
        cursor: pointer;
        overflow: hidden;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
        user-select: none;
    }}

    .bot-avatar-circle img {{
        width: 100%;
        height: 100%;
        object-fit: cover;
        pointer-events: none;
    }}

    .bot-avatar-circle:hover {{
        transform: scale(1.08) translateY(-2px);
        box-shadow: 0 12px 32px rgba(56, 189, 248, 0.8), 0 0 22px rgba(56, 189, 248, 0.6);
        border-color: #ffffff;
    }}

    /* Glowing indicator when dialog is active */
    body:has(div[data-testid="stDialog"]) .bot-avatar-circle,
    body:has(div.stDialog) .bot-avatar-circle,
    body:has(div[role="dialog"]) .bot-avatar-circle {{
        border-color: #38bdf8 !important;
        box-shadow: 0 0 25px rgba(56, 189, 248, 0.9) !important;
    }}

    /* Position the native Streamlit button layer right on top of the 72px robot */
    div[data-testid="stElementContainer"]:has(#medassist-native-btn-marker) + div[data-testid="stElementContainer"] {{
        position: fixed !important;
        bottom: 25px !important;
        right: 25px !important;
        width: 72px !important;
        height: 72px !important;
        z-index: 100000050 !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow: hidden !important;
        border-radius: 50% !important;
    }}

    body:has(div[data-testid="stDialog"]) div[data-testid="stElementContainer"]:has(#medassist-native-btn-marker) + div[data-testid="stElementContainer"],
    body:has(div.stDialog) div[data-testid="stElementContainer"]:has(#medassist-native-btn-marker) + div[data-testid="stElementContainer"],
    body:has(div[role="dialog"]) div[data-testid="stElementContainer"]:has(#medassist-native-btn-marker) + div[data-testid="stElementContainer"] {{
        display: none !important;
    }}

    div[data-testid="stElementContainer"]:has(#medassist-native-btn-marker) + div[data-testid="stElementContainer"] button {{
        width: 72px !important;
        height: 72px !important;
        min-width: 72px !important;
        min-height: 72px !important;
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
       FLOATING AI BOT DIALOG AS SIDE CARD (BOTTOM-RIGHT)
       ======================================================== */
    /* 1. Backdrop */
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
        height: 560px !important;
        max-height: calc(100vh - 125px) !important;
        background: #0b1120 !important;
        background-color: #0b1120 !important;
        border: 2px solid #38bdf8 !important;
        border-radius: 16px !important;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.95), 0 0 30px rgba(56, 189, 248, 0.35) !important;
        overflow-y: auto !important;
        padding: 1.1rem 1.25rem !important;
        display: flex !important;
        flex-direction: column !important;
        pointer-events: auto !important;
        transform-origin: bottom right !important;
        animation: botPopupFromBot 0.25s ease-out !important;
    }}

    @keyframes botPopupFromBot {{
        0% {{
            opacity: 0;
            transform: scale(0.3) translateY(60px);
        }}
        100% {{
            opacity: 1;
            transform: scale(1) translateY(0);
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
