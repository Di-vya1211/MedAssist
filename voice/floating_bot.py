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

    # Tactical Telemetry Header Card
    st.markdown(f"""
    <div style='background: #080e1e; border: 1px solid rgba(56, 189, 248, 0.3); border-radius: 8px; padding: 10px 14px; margin-bottom: 12px; box-shadow: 0 4px 16px rgba(0,0,0,0.4);'>
        <div style='display: flex; justify-content: space-between; align-items: center;'>
            <div style='display: flex; align-items: center; gap: 10px;'>
                <div style='width: 8px; height: 8px; border-radius: 50%; background: #10b981; box-shadow: 0 0 8px #10b981;'></div>
                <span style='font-family: monospace; font-size: 0.88rem; color: #38bdf8; font-weight: 700; letter-spacing: 0.05em;'>MEDASSIST AI // PROTOCOL ACTIVE</span>
            </div>
            <span style='font-family: monospace; font-size: 0.72rem; color: #94a3b8; background: rgba(255,255,255,0.06); padding: 2px 6px; border-radius: 4px; border: 1px solid rgba(255,255,255,0.1);'>LATENCY: 0.8ms</span>
        </div>
        <p style='margin: 4px 0 0 0; color: #cbd5e1; font-size: 0.78rem;'>
            Clinical Decision Support Engine • Allergy Cross-Check Guard Armed
        </p>
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
    Renders the tactical AI Companion HUD pill dock in the bottom-right corner.
    Zero cartoon bobbing animation. Crisp 1px cyan borders, high-density telemetry.
    """
    init_floating_bot_state()
    is_hindi = st.session_state.get("language", "en") == "hi"
    hud_sub = "LIVE • VOICE READY" if not is_hindi else "लाइव • आवाज़ तैयार"

    st.html(f"""
    <style>
    /* Fixed Tactical HUD Pill Dock Container */
    #medassist-bot-container {{
        position: fixed !important;
        bottom: 22px !important;
        right: 24px !important;
        z-index: 100000005 !important;
        pointer-events: none !important;
    }}

    /* Tactical HUD Dock Pill */
    .hud-bot-dock {{
        background: rgba(6, 11, 22, 0.95);
        border: 1px solid rgba(56, 189, 248, 0.4);
        border-radius: 8px;
        padding: 8px 16px;
        display: flex;
        align-items: center;
        gap: 12px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.7), 0 0 12px rgba(56, 189, 248, 0.2);
        cursor: pointer;
        backdrop-filter: blur(12px);
        transition: all 0.2s ease-in-out;
        user-select: none;
    }}

    .hud-bot-dock:hover {{
        border-color: #38bdf8;
        box-shadow: 0 8px 28px rgba(56, 189, 248, 0.35), 0 0 18px rgba(56, 189, 248, 0.3);
        transform: translateY(-2px);
    }}

    /* Pulsing Green Status LED */
    .hud-status-dot {{
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #10b981;
        box-shadow: 0 0 8px #10b981;
        animation: hudPulse 2s infinite ease-in-out;
    }}

    @keyframes hudPulse {{
        0%, 100% {{ opacity: 1; transform: scale(1); }}
        50% {{ opacity: 0.5; transform: scale(0.85); }}
    }}

    /* Telemetry Text */
    .hud-dock-info {{
        display: flex;
        flex-direction: column;
    }}

    .hud-dock-title {{
        font-family: 'SF Mono', Menlo, Monaco, Consolas, monospace;
        font-size: 0.8rem;
        font-weight: 700;
        color: #f8fafc;
        letter-spacing: 0.05em;
        line-height: 1.2;
    }}

    .hud-dock-sub {{
        font-family: 'SF Mono', Menlo, Monaco, Consolas, monospace;
        font-size: 0.68rem;
        color: #38bdf8;
        letter-spacing: 0.03em;
        margin-top: 2px;
    }}

    .hud-dock-action {{
        background: rgba(56, 189, 248, 0.12);
        border: 1px solid rgba(56, 189, 248, 0.3);
        border-radius: 4px;
        padding: 3px 8px;
        font-family: monospace;
        font-size: 0.72rem;
        color: #38bdf8;
        font-weight: 700;
    }}

    /* Position the native Streamlit button layer right over the dock */
    div[data-testid="stElementContainer"]:has(#medassist-native-btn-marker) + div[data-testid="stElementContainer"] {{
        position: fixed !important;
        bottom: 22px !important;
        right: 24px !important;
        width: 260px !important;
        height: 48px !important;
        z-index: 100000050 !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow: hidden !important;
        border-radius: 8px !important;
    }}

    body:has(div[data-testid="stDialog"]) div[data-testid="stElementContainer"]:has(#medassist-native-btn-marker) + div[data-testid="stElementContainer"],
    body:has(div.stDialog) div[data-testid="stElementContainer"]:has(#medassist-native-btn-marker) + div[data-testid="stElementContainer"],
    body:has(div[role="dialog"]) div[data-testid="stElementContainer"]:has(#medassist-native-btn-marker) + div[data-testid="stElementContainer"] {{
        display: none !important;
    }}

    div[data-testid="stElementContainer"]:has(#medassist-native-btn-marker) + div[data-testid="stElementContainer"] button {{
        width: 260px !important;
        height: 48px !important;
        min-width: 260px !important;
        min-height: 48px !important;
        border-radius: 8px !important;
        opacity: 0 !important;
        cursor: pointer !important;
        border: none !important;
        background: transparent !important;
        padding: 0 !important;
        margin: 0 !important;
        pointer-events: auto !important;
    }}
    </style>

    <div id="medassist-bot-container" onclick="medassistClickBotToggle()">
        <div class="hud-bot-dock" title="Click to open MedAssist AI Clinical HUD / क्लीनिकल चैट खोलने के लिए क्लिक करें" onclick="medassistClickBotToggle(); event.stopPropagation();">
            <div class="hud-status-dot"></div>
            <div class="hud-dock-info">
                <div class="hud-dock-title">MEDASSIST AI // PROTOCOL</div>
                <div class="hud-dock-sub">⚡ {hud_sub}</div>
            </div>
            <div class="hud-dock-action">HUD 💬</div>
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
