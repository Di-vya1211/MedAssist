"""
MedAssist - Reusable Voice UI Component
Renders modern, open voice input in all modules:
- Streamlit web audio input (browser recording)
- Direct PC Microphone button
- Automatic language detection (Hindi / English)
- Automatic text pre-fill and trigger callback
- Real-time allergy extraction for drug queries
- One-click Cancel / Clear Voice button to reset for new input
"""

from typing import Optional, Dict, Any
import re
import urllib.parse
import streamlit as st
from voice.voice_service import voice_service


def render_voice_input_widget(
    module_key: str,
    target_state_key: str,
    trigger_state_key: Optional[str] = None,
    help_text: str = "Click to record or speak your input in Hindi or English",
    patient_id: Optional[int] = None,
    patient_db = None,
    **kwargs
) -> Optional[str]:
    """
    Renders an open, integrated voice input widget with browser recording and live mic.
    If speech is detected:
    - Transcribes the audio
    - Detects whether it's Hindi or English
    - Automatically updates st.session_state.language
    - Checks for allergy reporting if patient_id/db provided
    - Updates target_state_key and optionally sets trigger_state_key = True
    - Provides a Cancel / Clear button to reset for new input
    """
    st.markdown("""
    <style>
    .voice-card-container {
        background: rgba(15, 23, 42, 0.7);
        border: 1px solid rgba(56, 189, 248, 0.25);
        border-radius: 12px;
        padding: 12px 14px;
        margin-bottom: 12px;
    }
    .voice-tag {
        display: inline-block;
        background: rgba(56, 189, 248, 0.15);
        color: #38bdf8;
        padding: 2px 8px;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)

    title_name = module_key.replace('_', ' ').title()

    # Audio input version counter to allow complete reset/cancellation of recorded audio
    audio_ver_key = f"audio_ver_{module_key}"
    if audio_ver_key not in st.session_state:
        st.session_state[audio_ver_key] = 0
    audio_ver = st.session_state[audio_ver_key]

    widget_map = {
        "disease": "disease_text_field",
        "drug": "drug_text_input",
        "symptoms": "symp_area",
        "report": "report_voice_query",
        "wellness": "wellness_search_input",
    }

    st.markdown(f"""
    <div class="voice-card-container">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
            <span style="color: #38bdf8; font-weight: 700; font-size: 0.95rem;">
                🎙️ Voice Input / बोलकर इनपुट दें ({title_name})
            </span>
            <span class="voice-tag">🌐 Hindi & English Auto-Detect</span>
        </div>
        <p style="color: #94a3b8; font-size: 0.82rem; margin: 0 0 6px 0;">
            💡 {help_text}
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])

    # 1. Browser-based Audio Input
    with col1:
        st.markdown("<p style='color:#cbd5e1; font-size:0.8rem; font-weight:600; margin-bottom:4px;'>Web Audio (Browser):</p>", unsafe_allow_html=True)
        audio_data = st.audio_input(
            f"Record Voice ({module_key})",
            key=f"audio_input_{module_key}_{audio_ver}",
            label_visibility="collapsed"
        )

        if audio_data is not None:
            audio_cache_key = f"_last_audio_{module_key}"
            current_bytes = audio_data.getvalue()

            # Process only if new audio
            if st.session_state.get(audio_cache_key) != current_bytes:
                st.session_state[audio_cache_key] = current_bytes

                with st.spinner("🎙️ Transcribing speech & detecting language..."):
                    success, text, lang_code = voice_service.transcribe_audio_bytes(current_bytes, filename=f"{module_key}.wav")

                    if success and text:
                        # Auto-switch language if Hindi detected
                        if lang_code == "hi":
                            st.session_state.language = "hi"
                            lang_label = "हिन्दी (Hindi)"
                        else:
                            lang_label = "English"

                        # If user spoke an allergy in Drug Info or elsewhere
                        if patient_id and patient_db:
                            try:
                                from voice.voice_assistant import conversational_assistant
                                is_allg, allg_data = conversational_assistant.check_and_record_allergy_from_text(
                                    text, patient_id=patient_id, patient_db=patient_db
                                )
                                if is_allg and allg_data:
                                    st.session_state[f"allergy_flash_{module_key}"] = allg_data
                            except Exception as e:
                                print(f"[VoiceUI] Allergy check error: {e}")

                        st.session_state[f"last_voice_{module_key}"] = (text, lang_label)
                        st.session_state[target_state_key] = text
                        if module_key in widget_map:
                            st.session_state[widget_map[module_key]] = text
                        if trigger_state_key:
                            st.session_state[trigger_state_key] = True
                        st.rerun()
                    else:
                        st.warning("Could not clearly transcribe speech. Please try speaking closer to the microphone.")

    # 2. Live PC Microphone Button
    with col2:
        st.markdown("<p style='color:#cbd5e1; font-size:0.8rem; font-weight:600; margin-bottom:4px;'>Direct PC Mic:</p>", unsafe_allow_html=True)
        if st.button("🎤 Record PC Mic (6s)", key=f"pc_mic_btn_{module_key}", use_container_width=True):
            with st.spinner("🎤 Listening from PC mic (6s)... Speak in Hindi or English"):
                success, text, lang_code = voice_service.record_live_microphone(timeout=6, phrase_time_limit=8)

                if success and text:
                    if lang_code == "hi":
                        st.session_state.language = "hi"
                        lang_label = "हिन्दी (Hindi)"
                    else:
                        lang_label = "English"

                    if patient_id and patient_db:
                        try:
                            from voice.voice_assistant import conversational_assistant
                            is_allg, allg_data = conversational_assistant.check_and_record_allergy_from_text(
                                text, patient_id=patient_id, patient_db=patient_db
                            )
                            if is_allg and allg_data:
                                st.session_state[f"allergy_flash_{module_key}"] = allg_data
                        except Exception as e:
                            print(f"[VoiceUI] Allergy check error: {e}")

                    st.session_state[f"last_voice_{module_key}"] = (text, lang_label)
                    st.session_state[target_state_key] = text
                    if module_key in widget_map:
                        st.session_state[widget_map[module_key]] = text
                    if trigger_state_key:
                        st.session_state[trigger_state_key] = True
                    st.rerun()
                else:
                    st.warning("Speech not recognized from PC microphone.")

    # Show transcription feedback banner with Cancel / Clear button
    voice_info = st.session_state.get(f"last_voice_{module_key}")
    if voice_info:
        transcript, lang_display = voice_info
        b_col1, b_col2 = st.columns([4, 1.4])
        with b_col1:
            st.markdown(f"""
            <div style='background:rgba(16,185,129,0.1); border:1px solid rgba(16,185,129,0.3); border-radius:8px; padding:10px 14px;'>
                <p style='color:#10b981; font-size:0.85rem; margin:0;'>
                    <b>✅ Recognized:</b> "{transcript}" &nbsp;|&nbsp; 
                    <b>🌐 Detected Language:</b> <span class='voice-tag'>{lang_display}</span>
                </p>
            </div>
            """, unsafe_allow_html=True)
        with b_col2:
            if st.button("❌ Cancel / Clear", key=f"clear_voice_{module_key}", use_container_width=True, help="Clear this voice input and reset microphone for new input"):
                # Increment audio_ver to unmount and discard old recorded audio in browser
                st.session_state[audio_ver_key] = st.session_state.get(audio_ver_key, 0) + 1
                st.session_state.pop(f"last_voice_{module_key}", None)
                st.session_state.pop(f"_last_audio_{module_key}", None)
                st.session_state.pop(f"allergy_flash_{module_key}", None)
                st.session_state[target_state_key] = ""
                if module_key in widget_map and widget_map[module_key] in st.session_state:
                    st.session_state[widget_map[module_key]] = ""
                if trigger_state_key and trigger_state_key in st.session_state:
                    del st.session_state[trigger_state_key]
                st.rerun()

    # Show allergy flash banner if an allergy was just detected and recorded
    allg_flash = st.session_state.get(f"allergy_flash_{module_key}")
    if allg_flash:
        st.markdown(f"""
        <div style='background:rgba(239,68,68,0.15); border:1px solid #ef4444; border-radius:8px; padding:10px 14px; margin: 6px 0 10px 0;'>
            <p style='color:#ef4444; font-weight:700; margin:0;'>
                🛡️ ALLERGY RECORDED & SAVED TO PROFILE: {allg_flash.get('medicine_name')}
            </p>
            <p style='color:#f87171; font-size:0.85rem; margin:2px 0 0 0;'>
                Severity: {allg_flash.get('severity')} | Symptoms: {allg_flash.get('symptoms')}. MedAssist has permanently recorded this allergy and will avoid this medicine in future recommendations.
            </p>
        </div>
        """, unsafe_allow_html=True)

    return st.session_state.get(target_state_key)


def render_read_aloud_widget(
    text_to_read: str,
    widget_key: str,
    label: str = "🔊 Read Aloud / बोलकर सुनें",
    forced_lang: Optional[str] = None
):
    """
    Universal, 100% reliable Read Aloud audio widget.
    Features:
    1. Instant HTML5 Browser Speech Synthesis (zero latency, zero server roundtrip, works everywhere)
    2. Persistent MP3 Audio Player via gTTS stored in st.session_state
    3. Stop button to instantly stop browser audio
    """
    if not text_to_read or not str(text_to_read).strip():
        return

    # Clean text of markdown characters
    clean_text = re.sub(r'[*_#`~>\[\]\(\)\{\}]', ' ', str(text_to_read))
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()
    speech_text = clean_text[:450]

    is_hindi = (forced_lang == "hi") if forced_lang else (st.session_state.get("language", "en") == "hi")
    lang_code = forced_lang or ("hi" if is_hindi else "en")
    speech_lang_tag = "hi-IN" if is_hindi else "en-US"

    # URL-encode text so JavaScript decodeURIComponent is 100% immune to quotes, newlines, and unicode symbols
    encoded_js = urllib.parse.quote(speech_text)

    st.markdown(f"<h4 style='color:#38bdf8; margin: 14px 0 6px 0;'>{label}</h4>", unsafe_allow_html=True)

    col_tts_btn, col_web_speech = st.columns([1, 1.2])

    with col_tts_btn:
        if st.button("🎧 Play Audio Player (MP3)", key=f"mp3_btn_{widget_key}", use_container_width=True):
            with st.spinner("Generating speech audio..."):
                audio_bytes = voice_service.text_to_speech_bytes(speech_text, lang_code=lang_code)
                if audio_bytes:
                    st.session_state[f"_audio_cache_{widget_key}"] = audio_bytes
                    st.rerun()
                else:
                    st.info("Audio generation temporarily delayed. Please click '🗣️ Instant Speech' beside this button!")

    with col_web_speech:
        instant_label = "🗣️ Instant Speech (Browser)" if not is_hindi else "🗣️ तुरंत बोलकर सुनाएं (Browser)"
        stop_label = "⏹️ Stop" if not is_hindi else "⏹️ रोकें"
        st.html(f"""
        <div style="display:flex; gap:8px; align-items:center; margin-top:2px;">
            <button onclick="(function(){{
                if (!('speechSynthesis' in window)) {{
                    alert('Speech synthesis is not supported on this browser.');
                    return;
                }}
                window.speechSynthesis.cancel();
                var text = decodeURIComponent('{encoded_js}');
                var msg = new SpeechSynthesisUtterance(text);
                msg.lang = '{speech_lang_tag}';
                msg.rate = 0.95;
                window.speechSynthesis.speak(msg);
            }})()" style="background: linear-gradient(135deg, #0284c7, #0369a1); color: #ffffff; border: none; padding: 7px 15px; border-radius: 8px; font-weight: 600; cursor: pointer; font-size: 0.88rem; box-shadow: 0 2px 10px rgba(2, 132, 199, 0.4); display: flex; align-items: center; gap: 6px;">
                {instant_label}
            </button>
            <button onclick="(function(){{
                if ('speechSynthesis' in window) {{
                    window.speechSynthesis.cancel();
                }}
            }})()" style="background: #334155; color: #cbd5e1; border: 1px solid #475569; padding: 7px 12px; border-radius: 8px; font-weight: 600; cursor: pointer; font-size: 0.85rem;">
                {stop_label}
            </button>
        </div>
        """)

    # Display persistent player if audio was generated
    cached = st.session_state.get(f"_audio_cache_{widget_key}")
    if cached:
        st.audio(cached, format="audio/mp3", autoplay=True)
