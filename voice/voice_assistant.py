"""
MedAssist - Conversational Voice Assistant
Multilingual conversational interface with auto-language detection (Hindi/English),
adverse reaction & allergy recognition and persistence, and allergy-aware health guidance.
"""

import os
import re
import json
from typing import Dict, Any, Optional, List, Tuple
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, "config", ".env"))

try:
    from core.llm import LLMClient
except ImportError:
    import sys
    sys.path.insert(0, os.path.join(BASE_DIR, "core"))
    from llm import LLMClient

from voice.voice_service import voice_service

class ConversationalVoiceAssistant:
    def __init__(self):
        self.llm = LLMClient()

    def check_and_record_allergy_from_text(
        self,
        text: str,
        patient_id: Optional[int] = None,
        patient_db = None
    ) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """
        Uses clinical NLP to detect if user text is reporting an allergy or adverse reaction.
        If yes and patient_id/patient_db are provided, immediately records it into the database.
        Returns: (is_allergy_reported, allergy_info_dict)
        """
        clean_msg = (text or "").strip()
        if not clean_msg:
            return False, None

        allergy_check_prompt = f"""You are a clinical NLP extractor. Analyze if this patient message describes an allergy, adverse side effect, or bad reaction to any medicine/drug:
Patient message: "{clean_msg}"

If YES, output ONLY a JSON object:
{{
  "is_allergy_report": true,
  "medicine_name": "exact name of medicine",
  "severity": "Mild" or "Moderate" or "Severe",
  "symptoms": "symptoms experienced e.g. rash, vomiting, swelling, breathing difficulty",
  "notes": "brief description of experience"
}}

If NO, output ONLY:
{{
  "is_allergy_report": false
}}"""

        try:
            check_resp = self.llm.generate(allergy_check_prompt)
            match = re.search(r'\{.*\}', check_resp, re.DOTALL)
            if match:
                parsed = json.loads(match.group(0))
                if parsed.get("is_allergy_report") and parsed.get("medicine_name"):
                    med_name = parsed.get("medicine_name", "").strip()
                    severity = parsed.get("severity", "Moderate")
                    symptoms = parsed.get("symptoms", "Adverse reaction")
                    notes = parsed.get("notes", "Reported via voice/chat input")

                    if patient_db and patient_id and med_name:
                        patient_db.add_allergy(
                            patient_id=patient_id,
                            medicine_name=med_name,
                            severity=severity,
                            symptoms=symptoms,
                            notes=notes
                        )
                    return True, parsed
        except Exception as e:
            print(f"[VoiceAssistant] Allergy check notice: {e}")

        return False, None

    def process_message(
        self,
        user_message: str,
        patient_id: Optional[int] = None,
        patient_db = None,
        patient_profile: Optional[Dict] = None,
        force_language: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Processes a voice or text message:
        1. Detects language (Hindi vs English)
        2. Detects if user is reporting an allergy / adverse reaction to a drug
        3. If allergy reported: saves it to the patient's profile in the database!
        4. Generates an allergy-safe, empathetic response in the same language
        5. Generates TTS audio
        """
        clean_msg = (user_message or "").strip()
        if not clean_msg:
            return {
                "response_text": "Please provide your question or symptoms.",
                "language": "en",
                "allergy_detected": False,
                "audio_path": None
            }

        # Step 1: Detect Language
        detected_lang = force_language or voice_service.detect_language(clean_msg)
        is_hindi = (detected_lang == "hi")

        # Step 2: Fetch Patient Allergies and Context
        allergies_list = []
        if patient_db and patient_id:
            try:
                allergies_list = patient_db.get_allergies(patient_id)
            except Exception as e:
                print(f"[VoiceAssistant] Error fetching allergies: {e}")

        known_allergies_str = ", ".join([a.get('medicine_name', '') for a in allergies_list if a.get('medicine_name')])

        # Step 3: Check if the message is reporting an allergy / adverse reaction
        allergy_saved, saved_allergy_info = self.check_and_record_allergy_from_text(
            clean_msg,
            patient_id=patient_id,
            patient_db=patient_db
        )

        # Step 4: Generate Response in the User's Language
        lang_instruction = (
            "Respond in clear, warm, conversational HINDI (हिन्दी). Use simple words that a patient can easily understand."
            if is_hindi else
            "Respond in clear, warm, conversational ENGLISH. Keep it simple and patient-friendly."
        )

        allergy_context_prompt = ""
        if allergy_saved and saved_allergy_info:
            if is_hindi:
                allergy_context_prompt = (
                    f"IMPORTANT: The patient just reported an adverse reaction/allergy to '{saved_allergy_info.get('medicine_name')}'. "
                    f"Acknowledge that you have RECORDED this allergy into their health profile. Reassure them that in all future "
                    f"recommendations, this medication will be strictly avoided. Advise them to consult their doctor if symptoms persist."
                )
            else:
                allergy_context_prompt = (
                    f"IMPORTANT: The patient just reported an adverse reaction/allergy to '{saved_allergy_info.get('medicine_name')}'. "
                    f"Acknowledge clearly that you have RECORDED this allergy into their patient records. Reassure them that all future "
                    f"recommendations will strictly avoid this medication. Advise them to contact their doctor if symptoms are active."
                )
        elif known_allergies_str:
            allergy_context_prompt = (
                f"PATIENT KNOWN ALLERGIES: {known_allergies_str}.\n"
                f"STRICT RULE: Do NOT suggest or recommend any of these medications under any circumstance. Suggest safe alternatives."
            )

        patient_profile_str = ""
        if patient_profile:
            patient_profile_str = f"Patient: {patient_profile.get('full_name', 'Patient')}, Age: {patient_profile.get('age', 'N/A')}, Gender: {patient_profile.get('gender', 'N/A')}, Blood Group: {patient_profile.get('blood_type', 'N/A')}."

        system_prompt = f"""You are MedAssist, a compassionate rural health companion.
{patient_profile_str}
{lang_instruction}
{allergy_context_prompt}

Patient Query: "{clean_msg}"

Provide a helpful, accurate, 3-5 sentence response. If there are red-flag emergency symptoms (severe chest pain, difficulty breathing, unconsciousness), urge calling 108/102 immediately.
Always end with a gentle reminder to consult a qualified physician."""

        try:
            response_text = self.llm.generate(system_prompt).strip()
        except Exception as e:
            print(f"[VoiceAssistant] Response generation error: {e}")
            if is_hindi:
                response_text = "क्षमा करें, तकनीकी समस्या के कारण उत्तर नहीं मिल पाया। कृपया कुछ समय बाद पुनः प्रयास करें या डॉक्टर से संपर्क करें।"
            else:
                response_text = "I apologize, a technical issue occurred while generating the response. Please consult a healthcare professional."

        # Step 5: Generate Speech Audio
        audio_filename = f"voice_resp_{patient_id or 'anon'}.mp3"
        audio_path = voice_service.text_to_speech(response_text, lang_code=detected_lang, output_path=audio_filename)

        return {
            "response_text": response_text,
            "language": detected_lang,
            "allergy_detected": allergy_saved,
            "allergy_info": saved_allergy_info,
            "audio_path": audio_path
        }


# Global singleton instance
conversational_assistant = ConversationalVoiceAssistant()
