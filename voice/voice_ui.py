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

    user_active_lang = st.session_state.get("language", "en")
    target_speech_lang = "hi-IN" if user_active_lang == "hi" else "en-US"
    lang_display_name = "हिन्दी (Hindi)" if user_active_lang == "hi" else "English"

    # Embed Browser Native Web Speech API Live Microphone
    import streamlit.components.v1 as components
    web_mic_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
      * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }}
      body {{ background: transparent; overflow: hidden; }}
      .live-mic-wrap {{
        display: flex;
        align-items: center;
        gap: 12px;
        background: rgba(15, 23, 42, 0.7);
        border: 1px solid rgba(56, 189, 248, 0.35);
        border-radius: 12px;
        padding: 7px 14px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25);
      }}
      .mic-btn {{
        background: linear-gradient(135deg, #0284c7, #0369a1);
        color: #ffffff;
        border: none;
        border-radius: 30px;
        padding: 8px 18px;
        font-size: 0.92rem;
        font-weight: 700;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 8px;
        box-shadow: 0 0 14px rgba(2, 132, 199, 0.4);
        transition: all 0.2s ease;
        white-space: nowrap;
      }}
      .mic-btn:hover {{
        background: linear-gradient(135deg, #0369a1, #075985);
        transform: translateY(-1px);
        box-shadow: 0 0 20px rgba(2, 132, 199, 0.6);
      }}
      .mic-btn.active {{
        background: linear-gradient(135deg, #ef4444, #dc2626) !important;
        animation: pulse 1.4s infinite;
      }}
      @keyframes pulse {{
        0% {{ box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7); }}
        70% {{ box-shadow: 0 0 0 14px rgba(239, 68, 68, 0); }}
        100% {{ box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }}
      }}
      .live-status {{
        color: #94a3b8;
        font-size: 0.85rem;
        flex: 1;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }}
    </style>
    </head>
    <body>
    <div class="live-mic-wrap">
      <button id="liveMicBtn" class="mic-btn" onclick="toggleListening()">
        <span id="micIcon" style="font-size:1.15rem;">🎙️</span>
        <span id="btnText">Live Microphone (Click & Speak)</span>
      </button>
      <div id="liveStatus" class="live-status">
        Mode: <b>{lang_display_name}</b> • Click mic & speak directly
      </div>
    </div>

    <script>
    let recognition = null;
    let isListening = false;
    const targetLang = "{target_speech_lang}";
    const targetModule = "{module_key}";

    function toggleListening() {{
      const SpeechRec = window.parent.SpeechRecognition || window.parent.webkitSpeechRecognition || window.SpeechRecognition || window.webkitSpeechRecognition;
      const btn = document.getElementById('liveMicBtn');
      const btnText = document.getElementById('btnText');
      const status = document.getElementById('liveStatus');

      if (!SpeechRec) {{
        status.innerHTML = "<span style='color:#f59e0b;'>⚠️ Browser Speech API unavailable. Please use the PC Hardware Mic below.</span>";
        return;
      }}

      if (isListening && recognition) {{
        recognition.stop();
        return;
      }}

      try {{
        recognition = new SpeechRec();
        recognition.lang = targetLang;
        recognition.continuous = false;
        recognition.interimResults = true;

        recognition.onstart = function() {{
          isListening = true;
          btn.classList.add('active');
          btnText.innerText = "🔴 Listening... Speak now!";
          status.innerHTML = "<span style='color:#38bdf8; font-weight:600;'>Listening live in {lang_display_name}... Speak now!</span>";
        }};

        recognition.onresult = function(event) {{
          let interim = '';
          let final = '';
          for (let i = event.resultIndex; i < event.results.length; ++i) {{
            if (event.results[i].isFinal) {{
              final += event.results[i][0].transcript;
            }} else {{
              interim += event.results[i][0].transcript;
            }}
          }}
          const current = final || interim;
          status.innerHTML = "<span style='color:#10b981; font-weight:700;'>🗣️ " + current + "</span>";

          try {{
            const pDoc = window.parent.document;
            const inputs = pDoc.querySelectorAll('input[type="text"]');
            for (const inp of inputs) {{
              if (inp.placeholder && (inp.placeholder.includes('Diabetes') || inp.placeholder.includes('disease') || inp.placeholder.includes('medicine') || inp.placeholder.includes('e.g.'))) {{
                const nativeSetter = Object.getOwnPropertyDescriptor(window.parent.HTMLInputElement.prototype, 'value').set;
                nativeSetter.call(inp, current);
                inp.dispatchEvent(new Event('input', {{ bubbles: true }}));
                break;
              }}
            }}
          }} catch(e) {{}}

          if (final) {{
            onFinalTranscript(final.trim());
          }}
        }};

        recognition.onerror = function(event) {{
          isListening = false;
          btn.classList.remove('active');
          btnText.innerText = "Live Microphone (Click & Speak)";
          status.innerHTML = "<span style='color:#ef4444;'>Microphone notice: " + event.error + ". Click to retry.</span>";
        }};

        recognition.onend = function() {{
          isListening = false;
          btn.classList.remove('active');
          btnText.innerText = "Live Microphone (Click & Speak)";
        }};

        recognition.start();
      }} catch(err) {{
        status.innerHTML = "<span style='color:#ef4444;'>Mic error: " + err.message + "</span>";
      }}
    }}

    function onFinalTranscript(text) {{
      try {{
        const pDoc = window.parent.document;
        const inputs = pDoc.querySelectorAll('input[type="text"]');
        for (const inp of inputs) {{
          if (inp.placeholder && (inp.placeholder.includes('Diabetes') || inp.placeholder.includes('disease') || inp.placeholder.includes('medicine') || inp.placeholder.includes('e.g.'))) {{
            const nativeSetter = Object.getOwnPropertyDescriptor(window.parent.HTMLInputElement.prototype, 'value').set;
            nativeSetter.call(inp, text);
            inp.dispatchEvent(new Event('input', {{ bubbles: true }}));
            inp.dispatchEvent(new Event('change', {{ bubbles: true }}));
            break;
          }}
        }}

        setTimeout(() => {{
          const btns = pDoc.querySelectorAll('button');
          for (const b of btns) {{
            const bt = (b.innerText || '').toLowerCase();
            if (bt.includes('search disease') || bt.includes('search medication') || bt.includes('search')) {{
              b.click();
              break;
            }}
          }}
        }}, 350);

        const url = new URL(window.parent.location.href);
        url.searchParams.set('live_voice_text', encodeURIComponent(text));
        url.searchParams.set('live_voice_module', targetModule);
        window.parent.location.href = url.href;
      }} catch(e) {{
        console.error("Error finalizing transcript:", e);
      }}
    }}
    </script>
    </body>
    </html>
    """
    components.html(web_mic_html, height=58)

    col_live, col_alt = st.columns([3, 2])

    # 1. Fallback PC Hardware Mic Button
    with col_live:
        btn_label = "🎤 PC Hardware Mic (डायरेक्ट माइक)" if user_active_lang == "hi" else "🎤 PC Hardware Mic (Direct Input)"
        if st.button(btn_label, key=f"hw_mic_btn_{module_key}", use_container_width=True):
            lang_prompt = "Speak in English or Hindi" if user_active_lang == "en" else "हिन्दी या English में बोलिए"
            with st.spinner(f"🔴 Live Microphone Active... {lang_prompt}..."):
                success, text, lang_code = voice_service.record_live_microphone(
                    timeout=5, phrase_time_limit=8, hinted_lang=user_active_lang
                )

                if success and text:
                    lang_label = "हिन्दी (Hindi)" if lang_code == "hi" else "English"

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
                    st.warning("⚠️ Microphone could not capture speech. Please ensure mic permissions are allowed and try speaking again!")

    # 2. Secondary Browser Audio File / Recording
    with col_alt:
        with st.popover("📁 Audio File / Clip (वैकल्पिक)", use_container_width=True):
            st.markdown("<p style='color:#94a3b8; font-size:0.8rem; margin:0 0 4px 0;'>Record or upload an audio clip via browser:</p>", unsafe_allow_html=True)
            audio_data = st.audio_input(
                f"Audio ({module_key})",
                key=f"audio_input_{module_key}_{audio_ver}",
                label_visibility="collapsed"
            )

            if audio_data is not None:
                audio_cache_key = f"_last_audio_{module_key}"
                current_bytes = audio_data.getvalue()

                if st.session_state.get(audio_cache_key) != current_bytes:
                    st.session_state[audio_cache_key] = current_bytes

                    with st.spinner("🎙️ Transcribing audio clip..."):
                        success, text, lang_code = voice_service.transcribe_audio_bytes(
                            current_bytes, filename=f"{module_key}.wav", hinted_lang=user_active_lang
                        )

                        if success and text:
                            lang_label = "हिन्दी (Hindi)" if lang_code == "hi" else "English"

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
                            st.warning("Could not transcribe audio clip.")

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
