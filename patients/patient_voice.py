"""
MedAssist - Voice Interface
Speech-to-text and text-to-speech with gTTS
"""

import streamlit as st
from google.cloud import speech_v1
from google.cloud import texttospeech_v1
from gtts import gTTS
import speech_recognition as sr
import os
import io
from datetime import datetime
from typing import Tuple, Optional
import tempfile
from .patient_db import PatientDatabase

class VoiceManager:
    """Manage voice interactions"""
    
    SUPPORTED_LANGUAGES = {
        'Hindi': 'hi-IN',
        'English': 'en-IN',
        'Bengali': 'bn-IN',
        'Tamil': 'ta-IN',
        'Telugu': 'te-IN',
        'Marathi': 'mr-IN',
        'Gujarati': 'gu-IN',
        'Kannada': 'kn-IN',
        'Malayalam': 'ml-IN',
        'Odia': 'or-IN',
        'Punjabi': 'pa-IN',
        'Urdu': 'ur-IN'
    }
    
    LANGUAGE_CODES = {
        'Hindi': 'hi',
        'English': 'en',
        'Bengali': 'bn',
        'Tamil': 'ta',
        'Telugu': 'te',
        'Marathi': 'mr',
        'Gujarati': 'gu',
        'Kannada': 'kn',
        'Malayalam': 'ml',
        'Odia': 'or',
        'Punjabi': 'pa',
        'Urdu': 'ur'
    }
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
    
    def speech_to_text(self, language: str = 'Hindi') -> Tuple[bool, str]:
        """
        Convert speech to text using Google Speech Recognition
        Returns: (success, text)
        """
        try:
            with sr.Microphone() as source:
                st.info("🎤 Listening... Please speak clearly")
                
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                
                # Listen for audio
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=10)
            
            # Recognize speech
            lang_code = self.LANGUAGE_CODES.get(language, 'en')
            text = self.recognizer.recognize_google(audio, language=lang_code)
            
            st.success(f"✅ Heard: {text}")
            return True, text
        
        except sr.UnknownValueError:
            st.error("❌ Could not understand audio. Please try again.")
            return False, ""
        
        except sr.RequestError as e:
            st.error(f"❌ Speech Recognition Error: {e}")
            return False, ""
        
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            return False, ""
    
    def text_to_speech(self, text: str, language: str = 'Hindi') -> bool:
        """
        Convert text to speech using gTTS
        """
        try:
            lang_code = self.LANGUAGE_CODES.get(language, 'en')
            
            # Create gTTS object
            tts = gTTS(text=text, lang=lang_code, slow=False)
            
            # Save to temp file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
                tts.save(fp.name)
                temp_path = fp.name
            
            # Play audio in Streamlit
            with open(temp_path, 'rb') as audio_file:
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format='audio/mp3')
            
            # Clean up
            os.unlink(temp_path)
            return True
        
        except Exception as e:
            st.error(f"❌ Text-to-speech error: {str(e)}")
            return False
    
    def get_language_greeting(self, language: str) -> str:
        """Get greeting in patient's language"""
        greetings = {
            'Hindi': 'नमस्ते! कृपया अपनी समस्या बताएं।',
            'English': 'Hello! Please tell me about your problem.',
            'Bengali': 'নমস্কার! দয়া করে আপনার সমস্যা বলুন।',
            'Tamil': 'வணக்கம்! உங்கள் பிரச்சனை பற்றி சொல்லுங்கள்.',
            'Telugu': 'నమస్కారం! దయచేసి మీ సమస్యను చెప్పండి.',
            'Marathi': 'नमस्कार! कृपया तुमची समस्या सांगा।',
            'Gujarati': 'નમસ્તે! કૃપયા તમારી સમસ્યા જણાવો।',
            'Kannada': 'ನಮಸ್ಕಾರ! ದಯವಿಟ್ಟು ನಿಮ್ಮ ಸಮಸ್ಯೆ ಹೇಳಿ।',
            'Malayalam': 'നമസ്കാരം! ദയവായി നിങ്ങളുടെ പ്രശ്നം പറയുക.',
            'Odia': 'ନମସ୍କାର! ଦୟା କରି ତୁମର ସମସ୍ୟା କହ।',
            'Punjabi': 'ਨਮਸਤੇ! ਕਿਰਪਾ ਕਰਕੇ ਆਪਣੀ ਸਮੱਸਿਆ ਦੱਸੋ।',
            'Urdu': 'السلام علیکم! براہ کرم اپنا مسئلہ بتائیں۔'
        }
        return greetings.get(language, 'Hello! Please tell me about your problem.')


def render_voice_input_ui(patient_id: int, db) -> Tuple[bool, str]:
    """
    Display voice input UI in Streamlit
    Returns: (success, transcribed_text)
    """
    col1, col2, col3 = st.columns(3)
    
    with col2:
        st.markdown("### 🎤 Voice Assistant")
    
    # Get patient language preference
    patient = db.get_patient(patient_id)
    language = patient.get('language_preference', 'Hindi') if patient else 'Hindi'
    
    voice_manager = VoiceManager()
    
    # Show greeting
    greeting = voice_manager.get_language_greeting(language)
    st.info(f"💬 {greeting}")
    
    # Voice input
    if st.button("🎤 Start Recording", use_container_width=True, key="voice_input"):
        success, text = voice_manager.speech_to_text(language)
        
        if success:
            st.session_state.voice_text = text
            
            # Play confirmation in patient's language
            response_text = "आपकी बात समझ आ गई।" if language == 'Hindi' else "Got it!"
            voice_manager.text_to_speech(response_text, language)
            
            # Log interaction
            if db:
                db.add_voice_interaction(
                    patient_id=patient_id,
                    language=language,
                    user_text=text,
                    response_text=response_text,
                    interaction_type="speech_to_text"
                )
            
            return True, text
    
    return False, ""


def render_voice_response(text: str, language: str = 'Hindi') -> None:
    """
    Render voice response (text + audio)
    """
    voice_manager = VoiceManager()
    
    # Show text
    st.markdown(f"### Response:\n{text}")
    
    # Play audio
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔊 Hear Response", use_container_width=True):
            voice_manager.text_to_speech(text, language)


def render_voice_symptom_checker(patient_id: int, db) -> Optional[str]:
    """
    Complete voice interface for symptom checking
    """
    st.markdown("### 🎙️ Voice Symptom Checker")
    
    patient = db.get_patient(patient_id)
    language = patient.get('language_preference', 'Hindi') if patient else 'Hindi'
    
    voice_manager = VoiceManager()
    
    # Show greeting
    greeting = voice_manager.get_language_greeting(language)
    st.info(greeting)
    
    # Create two columns
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🎤 Speak Your Symptoms", use_container_width=True):
            success, text = voice_manager.speech_to_text(language)
            
            if success:
                st.session_state.symptom_voice_text = text
                st.session_state.show_voice_processing = True
                st.rerun()
    
    with col2:
        symptom_text = st.text_area(
            "Or type your symptoms:",
            value=st.session_state.get('symptom_voice_text', ''),
            height=100,
            key="symptom_text_manual"
        )
    
    # Process voice input if available
    if st.session_state.get('show_voice_processing'):
        voice_text = st.session_state.get('symptom_voice_text', '')
        
        if voice_text:
            st.success(f"✅ You said: {voice_text}")
            
            # Log voice interaction
            db.add_voice_interaction(
                patient_id=patient_id,
                language=language,
                user_text=voice_text,
                response_text="Processing...",
                interaction_type="symptom_checker_voice"
            )
            
            return voice_text
    
    return symptom_text if st.session_state.get('symptom_text_manual') else None


def render_voice_history(patient_id: int, db):
    """Display voice interaction history"""
    st.markdown("### 📜 Voice History")
    
    history = db.get_voice_history(patient_id, limit=5)
    
    if not history:
        st.info("No voice interactions yet")
        return
    
    for interaction in history:
        with st.expander(f"🎤 {interaction['interaction_type']} - {interaction['created_at'][:10]}"):
            st.markdown(f"**Language:** {interaction['language']}")
            st.markdown(f"**Your Input:** {interaction['user_input_text']}")
            st.markdown(f"**System Response:** {interaction['system_response_text']}")