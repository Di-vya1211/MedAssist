"""
MedAssist - Floating AI Health Assistant Bot
Fixed bottom-right corner interactive companion that greets the user with
"How may I help you?", answers any clinical/health queries, guards against allergies,
and provides conversational voice/text medical guidance.
"""

import os
import streamlit as st
from typing import Optional
from voice.voice_assistant import conversational_assistant


def init_floating_bot_state():
    """Initializes session state for the floating bot."""
    if "floating_bot_history" not in st.session_state:
        is_hindi = st.session_state.get("language", "en") == "hi"
        greeting = (
            "नमस्ते! 👋 मैं आपका MedAssist AI साथी हूँ। मैं आज आपकी क्या मदद कर सकता हूँ? "
            "आप मुझसे किसी भी बीमारी, दवा के दुष्प्रभाव, या स्वास्थ्य संबंधी सवाल पूछ सकते हैं।"
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
    if "_bot_pending_query" not in st.session_state:
        st.session_state._bot_pending_query = None


def render_floating_bot(patient_id: Optional[int] = None, patient_db = None):
    """
    Renders the fixed bottom-right floating AI companion bot using st.popover.
    Positioned permanently on the bottom right corner with animated glow,
    'How may I help you?' badge, and real-time medical Q&A.
    """
    init_floating_bot_state()

    is_hindi = st.session_state.get("language", "en") == "hi"
    badge_label = "🤖 How may I help you?" if not is_hindi else "🤖 How may I help you? | सहायता"

    # Patient allergy summary for the bot header
    allergies = []
    if patient_db and patient_id:
        try:
            allergies = patient_db.get_allergies(patient_id)
        except Exception:
            pass
    allergy_names = [a.get("medicine_name", "") for a in allergies if a.get("medicine_name")]

    # Handle pending query from quick chips if any
    pending_q = st.session_state.get("_bot_pending_query")
    if pending_q:
        st.session_state._bot_pending_query = None
        _process_bot_query(pending_q, patient_id, patient_db)
        st.rerun()

    # The Popover Launcher (Fixed to bottom-right by CSS)
    with st.popover(badge_label, help="Click to chat with MedAssist AI Companion", use_container_width=False):
        # Header inside the popover
        st.markdown("""
        <div style='display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid rgba(56, 189, 248, 0.2); padding-bottom: 10px; margin-bottom: 12px;'>
            <div style='display: flex; align-items: center; gap: 10px;'>
                <div style='background: linear-gradient(135deg, #0284c7 0%, #2563eb 100%); width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.2rem; box-shadow: 0 2px 10px rgba(2, 132, 199, 0.4);'>
                    🤖
                </div>
                <div>
                    <h4 style='color: #f8fafc; margin: 0; font-size: 1.05rem; font-weight: 700;'>MedAssist AI Bot</h4>
                    <p style='color: #10b981; margin: 0; font-size: 0.75rem; font-weight: 600;'>🟢 Online • How may I help you?</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if allergy_names:
            crit_str = ", ".join(allergy_names[:3]) + ("..." if len(allergy_names) > 3 else "")
            st.markdown(f"""
            <div style='background: rgba(239, 68, 68, 0.12); border: 1px solid rgba(239, 68, 68, 0.3); border-radius: 8px; padding: 6px 10px; margin-bottom: 10px; font-size: 0.78rem; color: #fca5a5;'>
                🛡️ <b>Allergy Guard Active:</b> Guarding against {crit_str}
            </div>
            """, unsafe_allow_html=True)

        # Messages scrollable area
        st.markdown("<div style='max-height: 320px; overflow-y: auto; padding-right: 4px;'>", unsafe_allow_html=True)
        for msg in st.session_state.floating_bot_history:
            role = msg.get("role", "assistant")
            content = msg.get("content", "")
            audio_path = msg.get("audio_path")
            allergy_rec = msg.get("allergy_recorded")

            with st.chat_message(role, avatar="🧑‍⚕️" if role == "user" else "🤖"):
                st.write(content)
                if allergy_rec:
                    st.warning(f"🚨 **Allergy Recorded:** Successfully saved '{allergy_rec}' into your permanent health profile!")
                if audio_path and os.path.exists(audio_path):
                    st.audio(audio_path, format="audio/mp3")
        st.markdown("</div>", unsafe_allow_html=True)

        # Quick Question Chips (Show when history is short)
        if len(st.session_state.floating_bot_history) <= 3:
            st.markdown("<p style='color: #94a3b8; font-size: 0.75rem; margin: 10px 0 4px 0;'>Quick questions:</p>", unsafe_allow_html=True)
            q_cols = st.columns(3)
            chips = [
                ("🤒 Cold/Fever", "What medicines and remedies help with common cold and fever?"),
                ("💊 Paracetamol", "Is Paracetamol safe and what is the typical dosage?"),
                ("🛡️ My Allergies", "What drug allergies do I have recorded in my profile?")
            ] if not is_hindi else [
                ("🤒 सर्दी-बुखार", "सर्दी और बुखार में क्या उपाय और दवाएं सुरक्षित हैं?"),
                ("💊 पैरासिटामोल", "पैरासिटामोल की सही खुराक और सावधानियां क्या हैं?"),
                ("🛡️ मेरी एलर्जी", "मेरी प्रोफाइल में कौन-कौन सी दवा एलर्जी दर्ज है?")
            ]

            for i, (label, query_text) in enumerate(chips):
                with q_cols[i]:
                    if st.button(label, key=f"bot_chip_{i}", use_container_width=True):
                        st.session_state._bot_pending_query = query_text
                        st.rerun()

        # Input Form
        placeholder_text = "अपना सवाल पूछें..." if is_hindi else "Ask any medical/health question..."
        with st.form("floating_bot_input_form", clear_on_submit=True):
            user_input = st.text_input(
                "Message MedAssist AI",
                placeholder=placeholder_text,
                label_visibility="collapsed",
                key="bot_user_text_input"
            )
            col_send, col_clear = st.columns([3, 1])
            with col_send:
                send_clicked = st.form_submit_button("Ask ➤", type="primary", use_container_width=True)
            with col_clear:
                clear_clicked = st.form_submit_button("🗑️", use_container_width=True, help="Clear chat history")

        if clear_clicked:
            st.session_state.floating_bot_history = []
            init_floating_bot_state()
            st.rerun()

        if send_clicked and user_input and user_input.strip():
            _process_bot_query(user_input.strip(), patient_id, patient_db)
            st.rerun()


def _process_bot_query(query: str, patient_id: Optional[int], patient_db):
    """Sends the user question to the conversational voice assistant and updates history."""
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

    # Get response from ConversationalVoiceAssistant
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
