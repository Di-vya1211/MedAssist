"""
MedAssist - Multilingual Voice Service
Provides dual-mode Speech-to-Text (Whisper & Google SR),
Intelligent Hindi/English language detection, TTS audio generation,
and voice assistant processing with allergy auto-recording.
"""

import os
import re
import io
import tempfile
from typing import Tuple, Optional, Dict, Any
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, "config", ".env"))

# Keywords to detect transliterated Hindi (Hinglish)
HINGLISH_KEYWORDS = {
    "dawai", "dawa", "dawaiyan", "bukhar", "khansi", "sirdard", "sir", "dard",
    "pet", "ulti", "chakkar", "kamzori", "thakan", "goli", "khana", "pani",
    "peena", "mujhe", "mera", "meri", "mere", "humko", "apna", "apni", "hai",
    "hain", "hoon", "hu", "kya", "kaise", "kare", "karein", "batao", "bataye",
    "chahiye", "lena", "lene", "khaye", "ho", "raha", "rahi", "rahe",
    "tha", "thi", "the", "nahi", "nahin", "bimari", "ilaj",
    "kharab", "khujli", "chakkte", "jalan", "sujan"
}

class VoiceService:
    def __init__(self):
        self._groq_client = None
        self._init_groq()

    def _init_groq(self):
        try:
            from groq import Groq
            api_key = os.getenv("GROQ_API_KEY")
            if api_key:
                self._groq_client = Groq(api_key=api_key)
        except Exception as e:
            print(f"[VoiceService] Groq init notice: {e}")

    def detect_language(self, text: str, hinted_lang: Optional[str] = None) -> str:
        """
        Detects if text is in Hindi ('hi') or English ('en').
        Checks Devanagari script (100% Hindi) or Hinglish keywords.
        """
        if not text:
            return hinted_lang or "en"

        # 1. Check Devanagari unicode range (0x0900 - 0x097F)
        if re.search(r'[\u0900-\u097F]', text):
            return "hi"

        # 2. Check Indian scripts
        if re.search(r'[\u0980-\u09FF]', text):
            return "bn"  # Bengali
        if re.search(r'[\u0B80-\u0BFF]', text):
            return "ta"  # Tamil
        if re.search(r'[\u0C00-\u0C7F]', text):
            return "te"  # Telugu

        # 3. Check for Whisper or explicit UI hint
        if hinted_lang in ["en", "english"]:
            # If user has English active, only override if strong Devanagari or multiple distinct Hinglish words
            words = re.findall(r'[a-zA-Z]+', text.lower())
            hinglish_count = sum(1 for w in words if w in HINGLISH_KEYWORDS)
            if hinglish_count >= 3:
                return "hi"
            return "en"

        if hinted_lang in ["hi", "hindi"]:
            return "hi"

        # 4. Check for Transliterated Hindi words
        words = re.findall(r'[a-zA-Z]+', text.lower())
        hinglish_count = sum(1 for w in words if w in HINGLISH_KEYWORDS)
        if hinglish_count >= 2:
            return "hi"

        return "en"

    def transcribe_audio_bytes(self, audio_bytes: bytes, filename: str = "audio.wav") -> Tuple[bool, str, str]:
        """
        Transcribes audio bytes using Groq Whisper, with fallback to Google SR.
        Returns: (success, transcribed_text, detected_lang_code)
        """
        if not audio_bytes or len(audio_bytes) < 100:
            return False, "", "en"

        # 1. Try Groq Whisper (ultra fast & native language detection)
        if self._groq_client:
            try:
                transcription = self._groq_client.audio.transcriptions.create(
                    file=(filename, audio_bytes),
                    model="whisper-large-v3-turbo",
                    response_format="verbose_json",
                )
                text = (transcription.text or "").strip()
                detected_lang = getattr(transcription, "language", "en") or "en"
                
                # Normalize lang tag
                if detected_lang.lower() in ["hi", "hindi"]:
                    lang_code = "hi"
                elif detected_lang.lower() in ["bn", "bengali"]:
                    lang_code = "bn"
                elif detected_lang.lower() in ["ta", "tamil"]:
                    lang_code = "ta"
                elif detected_lang.lower() in ["te", "telugu"]:
                    lang_code = "te"
                else:
                    lang_code = self.detect_language(text, hinted_lang=detected_lang)

                if text:
                    return True, text, lang_code
            except Exception as e:
                print(f"[VoiceService] Groq Whisper error: {e}")

        # 2. Fallback to speech_recognition using Google Web Speech
        try:
            import speech_recognition as sr
            recognizer = sr.Recognizer()
            buf = io.BytesIO(audio_bytes)
            with sr.AudioFile(buf) as source:
                audio_data = recognizer.record(source)

            # Try Hindi first if common
            try:
                text = recognizer.recognize_google(audio_data, language="hi-IN")
                if text:
                    return True, text, "hi"
            except Exception:
                pass

            # Fallback to English
            text = recognizer.recognize_google(audio_data, language="en-IN")
            if text:
                lang = self.detect_language(text)
                return True, text, lang

        except Exception as e:
            print(f"[VoiceService] Google SR fallback error: {e}")

        return False, "", "en"

    def record_live_microphone(self, timeout: int = 5, phrase_time_limit: int = 7) -> Tuple[bool, str, str]:
        """
        Records from PC microphone using speech_recognition with multi-device discovery.
        Returns: (success, transcribed_text, detected_lang_code)
        """
        try:
            import speech_recognition as sr
            recognizer = sr.Recognizer()
            recognizer.energy_threshold = 300
            recognizer.dynamic_energy_threshold = True

            audio_data = None
            mic_indices = [None]
            try:
                names = sr.Microphone.list_microphone_names()
                for idx, n in enumerate(names):
                    nl = n.lower()
                    if ("realtek" in nl or "microphone array" in nl or "mic in" in nl or "built-in" in nl) and "hands-free" not in nl:
                        mic_indices.append(idx)
            except Exception:
                pass

            for dev_idx in mic_indices:
                try:
                    with sr.Microphone(device_index=dev_idx) as source:
                        recognizer.adjust_for_ambient_noise(source, duration=0.3)
                        audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                    if audio_data:
                        break
                except Exception:
                    continue

            if not audio_data:
                return False, "", "en"

            # Try transcribe with Groq whisper first if audio wav is exportable
            try:
                wav_bytes = audio_data.get_wav_data()
                success, text, lang = self.transcribe_audio_bytes(wav_bytes, "mic.wav")
                if success and text:
                    return True, text, lang
            except Exception:
                pass

            # Fallback to Google SR
            try:
                text = recognizer.recognize_google(audio_data, language="hi-IN")
                if text:
                    return True, text, "hi"
            except Exception:
                pass

            try:
                text = recognizer.recognize_google(audio_data, language="en-IN")
                if text:
                    lang = self.detect_language(text)
                    return True, text, lang
            except Exception:
                pass

        except Exception as e:
            print(f"[VoiceService] Live mic error: {e}")

        return False, "", "en"

    def text_to_speech_bytes(self, text: str, lang_code: str = "en") -> Optional[bytes]:
        """
        Converts text to speech and returns MP3 audio bytes directly in memory.
        Avoids all disk file lock and permission issues.
        """
        if not text:
            return None
        
        # Clean markdown and formatting
        clean_text = re.sub(r'[*_#`~>\[\]\(\)\{\}]', '', text)
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()
        if len(clean_text) > 400:
            clean_text = clean_text[:400].rsplit(' ', 1)[0] + "..."

        try:
            from gtts import gTTS
            lang = lang_code if lang_code in ["hi", "en", "bn", "ta", "te", "mr", "gu", "pa"] else "en"
            tts = gTTS(text=clean_text, lang=lang, slow=False)
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            return fp.read()
        except Exception as e:
            print(f"[VoiceService] TTS bytes generation error: {e}")
            return None

    def text_to_speech(self, text: str, lang_code: str = "en", output_path: str = "voice_output.mp3") -> Optional[str]:
        """
        Converts text to speech in the requested language using gTTS.
        Saves safely to unique temporary or target file.
        """
        audio_bytes = self.text_to_speech_bytes(text, lang_code=lang_code)
        if not audio_bytes:
            return None

        try:
            # If output_path is relative, put it in BASE_DIR
            full_path = output_path if os.path.isabs(output_path) else os.path.join(BASE_DIR, output_path)
            
            # Avoid Windows WinError 32 (file in use by browser audio player)
            try:
                with open(full_path, "wb") as f:
                    f.write(audio_bytes)
                return full_path
            except (PermissionError, OSError):
                # Fallback to unique temp file
                import uuid
                rand_id = uuid.uuid4().hex[:6]
                alt_name = f"voice_{rand_id}.mp3"
                alt_path = os.path.join(BASE_DIR, alt_name)
                with open(alt_path, "wb") as f:
                    f.write(audio_bytes)
                return alt_path
        except Exception as e:
            print(f"[VoiceService] TTS file save error: {e}")
            return None


# Global singleton instance
voice_service = VoiceService()
