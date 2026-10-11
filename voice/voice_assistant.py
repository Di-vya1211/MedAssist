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

        # Pre-filter: Only call clinical NLP if text suggests medicine reaction
        allergy_triggers = [
            "allergy", "allergic", "reaction", "side effect", "side-effect",
            "adverse", "rash", "vomit", "itching", "swelling", "hives",
            "kharab", "khujli", "chakkte", "jalan", "sujan", "suit", "ulti",
            "dawa se", "dawai se", "goli se", "allergi"
        ]
        msg_low = clean_msg.lower()
        if not any(trig in msg_low for trig in allergy_triggers):
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
            if not response_text or len(response_text) < 15:
                raise ValueError("LLM response too short")
        except Exception as e:
            print(f"[VoiceAssistant] Response generation fallback notice: {e}")
            q_low = clean_msg.lower()
            if any(w in q_low for w in ["fever", "bukhar", "temperature", "tapmaan"]):
                response_text = (
                    "बुखार आमतौर पर किसी संक्रमण के खिलाफ शरीर की स्वाभाविक प्रतिक्रिया है। पर्याप्त पानी और तरल पदार्थ पिएं, आराम करें और तापमान मापते रहें। यदि बुखार 102°F से अधिक रहता है या 3 दिनों से ज्यादा रहता है, तो कृपया तुरंत डॉक्टर से संपर्क करें।"
                    if is_hindi else
                    "Fever is often the body's natural response to an infection. Stay well hydrated, rest adequately, and keep track of your body temperature. If the fever stays above 102°F (38.9°C) or lasts more than 3 days, please consult a physician promptly."
                )
            elif any(w in q_low for w in ["headache", "sirdard", "sir dard"]):
                response_text = (
                    "सिरदर्द थकान, तनाव या निर्जलीकरण के कारण हो सकता है। शांत कमरे में आराम करें, पानी पिएं और स्क्रीन से दूर रहें। यदि सिरदर्द अचानक और बहुत तीव्र हो, तो तुरंत चिकित्सक से परामर्श लें।"
                    if is_hindi else
                    "Headaches are frequently caused by stress, dehydration, or eye strain. Drink plenty of water and rest in a quiet, dimly lit room. Seek immediate medical attention if the headache is sudden, severe, or accompanied by vision changes."
                )
            elif any(w in q_low for w in ["cough", "khansi", "cold", "sardi", "jukham"]):
                response_text = (
                    "हल्की सर्दी-खांसी में गर्म पानी का सेवन, भाप लेना और तुलसी-अदरक का काढ़ा फायदेमंद होता है। यदि सांस लेने में कठिनाई हो या खांसी 2 सप्ताह से अधिक रहे, तो डॉक्टर को दिखाएं।"
                    if is_hindi else
                    "For a mild cold and cough, staying hydrated with warm fluids and steam inhalation can help soothe airways. If you experience difficulty breathing, high fever, or the cough persists beyond two weeks, please see a doctor."
                )
            else:
                response_text = (
                    "आपके स्वास्थ्य की देखभाल के लिए पर्याप्त विश्राम और संतुलित आहार आवश्यक है। यदि आपके लक्षण बने रहते हैं या बढ़ रहे हैं, तो कृपया व्यक्तिगत जांच के लिए डॉक्टर से अवश्य सलाह लें।"
                    if is_hindi else
                    "To support your recovery, ensure you get sufficient rest and stay properly hydrated. If your symptoms are persistent or worsening, please consult a qualified healthcare professional for a personalized clinical evaluation."
                )

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
