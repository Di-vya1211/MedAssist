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
            response_text = self._generate_smart_fallback(clean_msg, is_hindi)

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

    def _generate_smart_fallback(self, clean_msg: str, is_hindi: bool) -> str:
        """Domain-grounded clinical fallback when LLM API is unavailable."""
        q_low = clean_msg.lower()

        # 1. Drug lookup in FDA database (e.g. Paracetamol, Ibuprofen, Aspirin)
        try:
            from core.drug_qa_backend import DrugQABackend
            d_back = DrugQABackend()
            d_match = d_back.get_by_name(clean_msg)
            if not d_match:
                cand = d_back.search(clean_msg, top_k=1)
                if cand:
                    d_match = cand[0]
            if d_match:
                d_name = d_match.get("name", "Medication").title()
                d_ind = (d_match.get("indications") or "Symptom relief and management.")[:180]
                d_dose = (d_match.get("dosage") or "Take as directed by doctor or product instructions.")[:140]
                d_warn = (d_match.get("warnings") or "Consult a licensed physician before taking.")[:160]
                if is_hindi:
                    return f"{d_name}: इसका उपयोग {d_ind} के लिए किया जाता है। सामान्य खुराक: {d_dose}। मुख्य चेतावनी: {d_warn}। किसी भी दवा के सेवन से पहले डॉक्टर या फार्मासिस्ट से परामर्श अवश्य लें।"
                else:
                    return f"{d_name}: Indicated for {d_ind}. Typical dosage: {d_dose}. Important warnings: {d_warn}. Always consult your physician or pharmacist before taking any medication."
        except Exception:
            pass

        # 2. Asthma / Respiratory
        if any(w in q_low for w in ["asthma", "saans", "breathing", "wheezing", "dama"]):
            if is_hindi:
                return "अस्थमा (दमा) में वायुमार्ग में सूजन आ जाती है। धूल, धुएं, परागकण, और ठंडी हवा से बचें। चिकित्सक द्वारा निर्धारित इन्हेलर हमेशा अपने पास रखें। यदि सांस लेने में अत्यधिक तकलीफ या सीने में तेज दबाव हो, तो तुरंत आपातकालीन चिकित्सा सहायता (108) लें।"
            else:
                return "Asthma causes chronic inflammation and airway narrowing. Key precautions include avoiding dust, smoke, cold air, and known allergens. Keep your prescribed rescue inhaler accessible at all times. Seek immediate emergency medical care if you experience severe breathlessness."

        # 3. Diabetes / Blood Sugar
        if any(w in q_low for w in ["diabetes", "sugar", "madhumeh", "glucose"]):
            if is_hindi:
                return "मधुमेह (डायबिटीज) में रक्त शर्करा का नियंत्रण आवश्यक है। कम मीठा और उच्च फाइबर युक्त आहार लें, प्रतिदिन 30 मिनट टहलें, और समय-समय पर फास्टिंग व खाने के बाद शुगर जांचें। डॉक्टर द्वारा दी गई दवाएं नियमित लें।"
            else:
                return "Diabetes requires diligent blood sugar tracking and dietary moderation. Emphasize low-glycemic, fiber-rich foods, daily exercise, and regular fasting/post-meal glucose checks under physician supervision."

        # 4. Blood Pressure / Hypertension
        if any(w in q_low for w in ["bp", "blood pressure", "hypertension", "uchh raktchap"]):
            if is_hindi:
                return "उच्च रक्तचाप (High BP) में नमक का सेवन कम रखें, तली-भुनी चीजों से बचें, और नियमित व्यायाम करें। नियमित रूप से बीपी मापें और डॉक्टर द्वारा निर्धारित बीपी की गोलियां समय पर लें।"
            else:
                return "Hypertension management involves limiting sodium intake to under 5g daily, regular aerobic activity, and avoiding excess stress. Monitor blood pressure frequently and adhere strictly to prescribed antihypertensive therapy."

        # 5. Fever
        if any(w in q_low for w in ["fever", "bukhar", "temperature", "tapmaan"]):
            if is_hindi:
                return "बुखार आमतौर पर किसी संक्रमण के खिलाफ शरीर की स्वाभाविक प्रतिक्रिया है। पर्याप्त पानी और तरल पदार्थ पिएं, आराम करें और तापमान मापते रहें। यदि बुखार 102°F से अधिक रहता है या 3 दिनों से ज्यादा रहता है, तो कृपया तुरंत डॉक्टर से संपर्क करें।"
            else:
                return "Fever is typically your body's immune response to an infection. Stay well hydrated, rest adequately, and monitor your temperature. If fever exceeds 102°F (38.9°C) or lasts more than 3 days, please consult a physician promptly."

        # 6. Headache
        if any(w in q_low for w in ["headache", "sirdard", "sir dard", "migraine"]):
            if is_hindi:
                return "सिरदर्द अक्सर थकान, तनाव, निर्जलीकरण या नींद की कमी के कारण होता है। शांत कमरे में आराम करें, पानी पिएं और स्क्रीन से ब्रेक लें। यदि सिरदर्द अचानक और बहुत तीव्र हो, तो तुरंत चिकित्सक से परामर्श लें।"
            else:
                return "Headaches are often caused by stress, dehydration, lack of sleep, or eye strain. Drink plenty of water and rest in a quiet, dimly lit room. Seek immediate medical attention if the headache is sudden and unusually severe."

        # 7. Cough / Cold
        if any(w in q_low for w in ["cough", "khansi", "cold", "sardi", "jukham"]):
            if is_hindi:
                return "हल्की सर्दी-खांसी में गर्म पानी का सेवन, भाप लेना और गर्म तरल पदार्थ गले को आराम देते हैं। यदि सांस लेने में कठिनाई हो या खांसी 2 सप्ताह से अधिक रहे, तो डॉक्टर को दिखाएं।"
            else:
                return "For mild colds and coughs, warm fluids and steam inhalation can help soothe airways. If you experience difficulty breathing, high fever, or the cough persists beyond two weeks, please see a doctor."

        # 8. Stomach / Digestion / Acidity
        if any(w in q_low for w in ["stomach", "pet", "dard", "gas", "acidity", "vomiting", "ulti", "nausea"]):
            if is_hindi:
                return "पेट दर्द, गैस या उल्टी में सुपाच्य और हल्का भोजन (जैसे दलिया, खिचड़ी) लें और ओआरएस पिएं ताकि कमजोरी न आए। यदि दर्द बहुत तीव्र हो या बार-बार उल्टी हो, तो तुरंत डॉक्टर को दिखाएं।"
            else:
                return "For stomach pain, indigestion, or nausea, sip oral rehydration fluids and eat small, bland meals. Seek clinical evaluation if abdominal pain is acute or accompanied by persistent vomiting."

        # 9. General safe advice
        if is_hindi:
            return "आपके स्वास्थ्य की देखभाल के लिए पर्याप्त विश्राम, भरपूर पानी और संतुलित आहार आवश्यक है। यदि आपके लक्षण बने रहते हैं या बढ़ रहे हैं, तो कृपया व्यक्तिगत जांच के लिए डॉक्टर से अवश्य सलाह लें।"
        else:
            return "To support your recovery, ensure you get sufficient rest and stay properly hydrated. If your symptoms are persistent or worsening, please consult a qualified healthcare professional for a personalized clinical evaluation."


# Global singleton instance
conversational_assistant = ConversationalVoiceAssistant()
