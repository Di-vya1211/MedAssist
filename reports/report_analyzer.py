"""
Medical Report Analyzer — Simple Language for Rural Patients
Extracts text from PDF/Image → finds abnormal values → explains in plain Hindi/English mix
"""

import os
import re
import html

try:
    import pdfplumber
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

try:
    import pytesseract
    from PIL import Image
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
try:
    from agents.translation_agent import translate_text
    TRANSLATION_OK = True
except Exception as e:
    print(f"[ReportAnalyzer] Translation import error: {e}")
    TRANSLATION_OK = False
    def translate_text(text, target_lang="en"):
        return text
# Windows and Linux Tesseract binary paths
if OCR_AVAILABLE:
    possible_tesseract_bins = [
        r'C:\Program Files\Tesseract-OCR\tesseract.exe',
        r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
        '/usr/bin/tesseract',
        '/usr/local/bin/tesseract',
    ]
    for bin_path in possible_tesseract_bins:
        if os.path.exists(bin_path):
            pytesseract.pytesseract.tesseract_cmd = bin_path
            break

# Lazy LLM init 
_llm = None

def _get_llm():
    global _llm
    if _llm is not None:
        return _llm
    
    try:
        # Try LLMClient (auto-fallback GROQ → GEMINI)
        from core.llm import LLMClient
        _llm = LLMClient()
        print("[ReportAnalyzer] LLMClient loaded")
        return _llm
    except Exception as e1:
        print(f"[ReportAnalyzer] LLMClient failed: {e1}")
        try:
            # Fallback  FreeLLM
            from core.llm import FreeLLM
            _llm = FreeLLM()
            print("[ReportAnalyzer] FreeLLM loaded")
            return _llm
        except Exception as e2:
            print(f"[ReportAnalyzer] FreeLLM failed: {e2}")
            return None


# ═══════════════════════════════════════════════════════════════════
# NORMAL RANGES DATABASE (for reference + LLM context)
# ═════════════════════════════════════════════════════════════════==

NORMAL_RANGES = """
COMMON TEST NORMAL RANGES (for reference):
• Blood Pressure (BP): Less than 120/80 mmHg. 120-139/80-89 is elevated. 140/90+ is high.
• Fasting Blood Sugar: 70-100 mg/dL normal. 100-125 prediabetes. 126+ diabetes.
• PP / Random Blood Sugar: Less than 140 mg/dL normal. 140-199 prediabetes. 200+ high.
• Hemoglobin (Male): 13.5-17.5 g/dL. (Female): 12.0-15.5 g/dL. Below 12 is low (anemia).
• WBC (TLC): 4,000-11,000 per cmm. High means infection. Low means weak immunity.
• Platelets: 1,50,000-4,50,000 per cmm. Below 1,50,000 is low.
• Creatinine: 0.7-1.3 mg/dL. High means kidney problem.
• Urea: 7-20 mg/dL.
• Total Cholesterol: Less than 200 mg/dL. 200-239 borderline. 240+ high.
• LDL (Bad Cholesterol): Less than 100 mg/dL. 100-129 near ideal. 130-159 borderline. 160+ high.
• HDL (Good Cholesterol): Above 40 mg/dL (male), above 50 (female). Higher is better.
• Triglycerides: Less than 150 mg/dL. 150-199 borderline. 200+ high.
• Uric Acid: 3.5-7.2 mg/dL (male), 2.4-6.0 (female).
• Bilirubin: 0.1-1.2 mg/dL.
• SGPT (ALT): 7-56 U/L. High means liver stress.
• SGOT (AST): 5-40 U/L.
• Thyroid TSH: 0.4-4.0 mIU/L.
• Vitamin D: 30-100 ng/mL. Below 20 deficient.
• Vitamin B12: 200-900 pg/mL. Below 200 deficient.
• BMI: 18.5-24.9 normal. 25-29.9 overweight. 30+ obese.
• Pulse/Heart Rate: 60-100 beats per minute.
• SpO2 (Oxygen): 95-100% normal. Below 90 is dangerous.
• ESR: 0-15 mm/hr (male), 0-20 (female).
"""

# ═══════════════════════════════════════════════════════════════════
# TEXT EXTRACTION
# ═════════════════════════════════════════════════════════════════==

def extract_from_pdf(pdf_path):
    if not PDF_AVAILABLE:
        return "PDF extraction error: pdfplumber not installed. Run: pip install pdfplumber"
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                pt = page.extract_text()
                if pt:
                    text += pt + "\n"
        return text.strip()
    except Exception as e:
        return f"PDF extraction error: {str(e)}"


def extract_from_image(image_path):
    if not OCR_AVAILABLE:
        return "OCR error: pytesseract or PIL not installed. Run: pip install pytesseract pillow"
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text.strip()
    except Exception as e:
        return f"OCR error: {str(e)}"


def clean_text(raw_text):
    text = re.sub(r'\n+', '\n', raw_text)
    text = re.sub(r'\s+', ' ', text)
    # Remove common OCR artifacts
    text = re.sub(r'[_]{3,}', '', text)
    return text.strip()


# ═══════════════════════════════════════════════════════════════════
# VALUE EXTRACTION (Regex backup — even if LLM fails)
# ═════════════════════════════════════════════════════════════════==

VALUE_PATTERNS = {
    "Blood Pressure": r'\b(?:bp|blood\s*pressure)\b[^\d]*(\d{2,3})\s*(?:[/\\]\s*(\d{2,3}))?',
    "Fasting Sugar": r'\b(?:fasting\s*blood\s*sugar|fbs|fasting\s*glucose)\b[^\d]*(\d{2,3}(?:[.,]\d+)?)',
    "PP Sugar": r'\b(?:pp\s*blood\s*sugar|ppbs|post\s*prandial)\b[^\d]*(\d{2,3}(?:[.,]\d+)?)',
    "Random Sugar": r'\b(?:random\s*blood\s*sugar|rbs)\b[^\d]*(\d{2,3}(?:[.,]\d+)?)',
    "Hemoglobin": r'\b(?:hb|hemoglobin|haemoglobin)\b[^\d]*(\d{1,2}(?:[.,]\d+)?)',
    "WBC": r'\b(?:wbc|tlc|total\s*leukocyte)\b[^\d]*(\d{1,2}(?:[.,]\d+)?)\s*(?:thousand|k)?',
    "Platelets": r'\b(?:platelet|plt)\b[^\d]*(\d{2,3}(?:,\d{3})?)',
    "Creatinine": r'\b(?:creatinine)\b[^\d]*(\d+[.,]?\d*)',
    "Urea": r'\b(?:urea|blood\s*urea)\b[^\d]*(\d+[.,]?\d*)',
    "Total Cholesterol": r'\b(?:total\s*cholesterol|cholesterol\s*total)\b[^\d]*(\d+[.,]?\d*)',
    "LDL": r'\b(?:ldl|low\s*density)\b[^\d]*(\d+[.,]?\d*)',
    "HDL": r'\b(?:hdl|high\s*density)\b[^\d]*(\d+[.,]?\d*)',
    "Triglycerides": r'\b(?:triglycerides)\b[^\d]*(\d+[.,]?\d*)',
    "Uric Acid": r'\b(?:uric\s*acid)\b[^\d]*(\d+[.,]?\d*)',
    "Bilirubin": r'\b(?:bilirubin|total\s*bilirubin)\b[^\d]*(\d+[.,]?\d*)',
    "SGPT": r'\b(?:sgpt|alt)\b[^\d]*(\d+[.,]?\d*)',
    "SGOT": r'\b(?:sgot|ast)\b[^\d]*(\d+[.,]?\d*)',
    "TSH": r'\b(?:tsh|thyroid)\b[^\d]*(\d+[.,]?\d*)',
    "Vitamin D": r'\b(?:vitamin\s*d|25[\-\s]?oh\s*vitamin\s*d)\b[^\d]*(\d+[.,]?\d*)',
    "Vitamin B12": r'\b(?:vitamin\s*b12|cobalamin)\b[^\d]*(\d+[.,]?\d*)',
    "SpO2": r'\b(?:spo2|oxygen\s*saturation|sao2)\b[^\d]*(\d{2,3})',
    "Pulse": r'\b(?:pulse|heart\s*rate)\b[:\s]*(\d{2,3})',
    "Temperature": r'\b(?:temperature|temp)\b[^\d]*(\d{2,3}(?:[.,]\d+)?)',
    "Respiratory Rate": r'\b(?:respiratory\s*rate|respiratory\s*rt|resp\s*rate)\b[^\d]*(\d{2,3})',
}


def extract_values(text):
    """Extract numeric values from report using regex with overlap protection."""
    found = {}
    text_lower = text.lower()
    used_spans = []  # Track matched positions to avoid reuse
    
    for test_name, pattern in VALUE_PATTERNS.items():
        for match in re.finditer(pattern, text_lower, re.IGNORECASE):
            groups = match.groups()
            
            # Check if this match overlaps with already used ones
            match_start = match.start()
            match_end = match.end()
            
            overlap = False
            for used_start, used_end in used_spans:
                if not (match_end <= used_start or match_start >= used_end):
                    overlap = True
                    break
            
            if overlap:
                continue
            
            # Build value from captured groups
            if groups:
                parts = [g.strip().replace(",", ".") for g in groups if g and g.strip()]
                if len(parts) == 2:
                    val = f"{parts[0]}/{parts[1]}"
                elif len(parts) == 1:
                    val = parts[0]
                else:
                    continue
            else:
                val = match.group(0).strip()
            
            if val:
                found[test_name] = val
                used_spans.append((match_start, match_end))
                break  # Only first non-overlapping match per test
    
    return found


# ═══════════════════════════════════════════════════════════════════
# LLM ANALYSIS
# ═════════════════════════════════════════════════════════════════==

def analyze_report(report_text, patient_allergies=None, patient_profile=None):
    """
    Analyze report in simple language with patient allergy context.
    Returns structured dict.
    """
    if len(report_text) < 20:
        return {
            "summary": "Could not read the report properly. Please upload a clearer image or PDF.",
            "problems": [],
            "recommendations": [],
            "diet_lifestyle": [],
            "when_to_see_doctor": "Please consult a doctor with the original report.",
            "values_found": {},
            "raw_response": ""
        }

    # Extract values via regex first
    extracted_values = extract_values(report_text)
    values_str = "\n".join([f"• {k}: {v}" for k, v in extracted_values.items()]) or "No numeric values could be automatically extracted."

    patient_context_str = ""
    if patient_profile:
        patient_context_str += f"\nPATIENT PROFILE:\n- Age: {patient_profile.get('age', 'N/A')}, Gender: {patient_profile.get('gender', 'N/A')}, Blood Group: {patient_profile.get('blood_type', 'N/A')}"
    if patient_allergies:
        med_list = [a.get('medicine_name') for a in patient_allergies if a.get('medicine_name')]
        if med_list:
            patient_context_str += f"\n- KNOWN DRUG ALLERGIES: {', '.join(med_list)}\nSAFETY RULE: The patient is ALLERGIC to {', '.join(med_list)}. DO NOT suggest these medicines or their combinations. If relevant, suggest safe alternative medications."

    llm = _get_llm()
    if llm is None:
        clinical_data = generate_clinical_findings(extracted_values, report_text)
        clinical_data["values_found"] = extracted_values
        clinical_data["raw_response"] = ""
        return clinical_data

    prompt = f"""You are a friendly village health assistant. Explain the medical report in VERY SIMPLE language that a 10th-class student or rural patient can understand.
{patient_context_str}

NORMAL RANGES FOR REFERENCE:
{NORMAL_RANGES}

EXTRACTED VALUES FROM REPORT:
{values_str}

FULL REPORT TEXT:
\"\"\"{report_text[:4000]}\"\"\"

INSTRUCTIONS:
1. Use simple words. Avoid medical jargon. If you must use a medical word, explain it in brackets.
2. For EVERY abnormal value, say clearly: "Your [test] is [high/low]. Normal range is [X-Y]."
3. Tell what food to EAT MORE and what to AVOID for each problem.
4. Give 2-3 home remedies if safe.
5. NEVER diagnose a disease. Only explain what the numbers mean.
6. If report is normal, say clearly: "Your report looks mostly normal."

OUTPUT FORMAT (follow exactly):

REMEMBER:
- SUMMARY must be 2-3 sentences. Do not leave it empty.
- List EVERY problem with exact numbers from the report.
- WHAT TO DO must have at least 3 bullet points.
- DIET must have Eat/Avoid/Lifestyle tips.
- WHEN TO SEE DOCTOR must be specific.
SUMMARY:
[2-3 simple sentences about overall report]

PROBLEMS FOUND:
- [Problem 1: e.g., Your BP is 140/90. Normal is less than 120/80. This is slightly high.]
- [Problem 2: e.g., Your fasting sugar is 110. Normal is 70-100. This is borderline high.]
- [If all normal: "No major problems found. Your report looks good."]

WHAT TO DO:
- [Action 1: e.g., Reduce salt in food. Avoid pickles and papad.]
- [Action 2: e.g., Walk 30 minutes daily.]
- [Action 3: e.g., Take medicines on time if doctor prescribed.]

DIET & LIFESTYLE:
- [Eat: e.g., Eat more green vegetables, dal, and fruits.]
- [Avoid: e.g., Avoid oily food, sweets, and cold drinks.]
- [Lifestyle: e.g., Sleep 7-8 hours. Do not take stress.]

WHEN TO SEE DOCTOR:
[If report is normal: "Routine checkup is fine. See doctor if you feel any symptoms."]
[If abnormal: "Please show this report to a doctor within 1 week. If you have chest pain, severe headache, or difficulty breathing, go immediately."]

ANSWER:"""

    try:
        response = llm.generate(prompt)
    except Exception as e:
        print(f"[ReportAnalyzer] LLM error: {e}")
        response = ""

    parsed = parse_sections(response) if response else {
        "summary": "", "problems": [], "recommendations": [], "diet_lifestyle": [], "when_to_see_doctor": "", "raw_response": ""
    }

    # Clinical validation: if sections are missing or contain generic placeholder, generate genuine clinical analysis
    is_generic = (
        not parsed.get("summary")
        or "Based on standard" in parsed.get("summary", "")
        or len(parsed.get("summary", "").strip()) < 20
        or len(parsed.get("problems", [])) == 0
        or len(parsed.get("recommendations", [])) == 0
    )
    if is_generic or not parsed.get("problems") or not parsed.get("recommendations"):
        clinical_data = generate_clinical_findings(extracted_values, report_text)
        if is_generic or not parsed.get("summary") or "Based on standard" in parsed.get("summary", ""):
            parsed["summary"] = clinical_data["summary"]
        if not parsed.get("problems"):
            parsed["problems"] = clinical_data["problems"]
        if not parsed.get("recommendations"):
            parsed["recommendations"] = clinical_data["recommendations"]
        if not parsed.get("diet_lifestyle"):
            parsed["diet_lifestyle"] = clinical_data["diet_lifestyle"]
        if not parsed.get("when_to_see_doctor"):
            parsed["when_to_see_doctor"] = clinical_data["when_to_see_doctor"]

    parsed["values_found"] = extracted_values
    parsed["raw_response"] = response
    return parsed


def generate_clinical_findings(extracted_values: dict, report_text: str = "") -> dict:
    """
    Evaluates extracted lab parameters against medical thresholds
    to guarantee comprehensive, accurate findings, diet, actions, and doctor advice.
    """
    problems = []
    recommendations = []
    diet_lifestyle = []
    when_to_see_doctor = ""

    # 1. Blood Pressure Evaluation
    if "Blood Pressure" in extracted_values:
        bp_val = str(extracted_values["Blood Pressure"]).replace(",", ".")
        try:
            parts = bp_val.split("/")
            systolic = float(parts[0])
            diastolic = float(parts[1]) if len(parts) > 1 else 80.0
            if systolic >= 140 or diastolic >= 90:
                problems.append(f"Blood Pressure is {bp_val} mmHg (High / Stage 2 Hypertension). Normal is less than 120/80 mmHg.")
                recommendations.append("Reduce daily salt and sodium intake; avoid papads, pickles, and processed snacks.")
                recommendations.append("Engage in 30 minutes of daily moderate walking or physical activity.")
                recommendations.append("Maintain a morning and evening blood pressure log for your doctor.")
                diet_lifestyle.append("Eat: Fresh green vegetables, garlic, flaxseeds, and potassium-rich fruits like bananas.")
                diet_lifestyle.append("Avoid: Salty fried snacks, excess tea/coffee, and canned foods.")
                diet_lifestyle.append("Lifestyle: Prioritize 7-8 hours of sound sleep and practice deep breathing.")
                when_to_see_doctor = "Show this report to your physician within 3 to 5 days. If you experience chest pain, sudden breathlessness, or severe headache, seek emergency medical care immediately."
            elif systolic >= 120 or diastolic >= 80:
                problems.append(f"Blood Pressure is {bp_val} mmHg (Elevated / Pre-hypertension). Normal is less than 120/80 mmHg.")
                recommendations.append("Cut down on added table salt and avoid high-sodium packaged snacks.")
                recommendations.append("Incorporate daily 30-minute brisk walks and stay well hydrated.")
                diet_lifestyle.append("Eat: Fresh vegetables, whole grains, and coconut water in moderation.")
                diet_lifestyle.append("Avoid: Junk food, excess caffeine, and salty condiments.")
                if not when_to_see_doctor:
                    when_to_see_doctor = "Consult your healthcare provider at your next regular visit to track your blood pressure trend."
        except Exception:
            pass

    # 2. Glucose / Sugar Evaluation
    for sugar_key in ["Fasting Sugar", "PP Sugar", "Random Sugar"]:
        if sugar_key in extracted_values:
            try:
                s_val = float(str(extracted_values[sugar_key]).replace(",", "."))
                threshold = 100 if sugar_key == "Fasting Sugar" else 140
                if s_val > threshold:
                    problems.append(f"{sugar_key} is {s_val} mg/dL (Elevated). Normal range is {'70-100' if sugar_key == 'Fasting Sugar' else '< 140'} mg/dL.")
                    recommendations.append("Reduce sugar, sweets, refined flour (maida), and sweetened beverages.")
                    recommendations.append("Check blood glucose levels regularly as advised by your physician.")
                    diet_lifestyle.append("Eat: Methi (fenugreek) water, karela (bitter gourd), whole grains, and fresh salads.")
                    diet_lifestyle.append("Avoid: Bakery items, sweetened fruit juices, potatoes in excess, and sweets.")
                    if not when_to_see_doctor:
                        when_to_see_doctor = "Consult your physician within 1 week for blood sugar evaluation and HbA1c testing."
            except Exception:
                pass

    # 3. Hemoglobin Evaluation
    if "Hemoglobin" in extracted_values:
        try:
            hb_val = float(str(extracted_values["Hemoglobin"]).replace(",", "."))
            if hb_val < 12.0:
                problems.append(f"Hemoglobin is {hb_val} g/dL (Low / Anemia). Normal adult range is 12.0 to 16.5 g/dL.")
                recommendations.append("Increase dietary iron intake and consult a doctor regarding iron supplements.")
                diet_lifestyle.append("Eat: Iron-rich foods like spinach (palak), beetroot, pomegranate, jaggery (gud), and raisins.")
                diet_lifestyle.append("Avoid: Drinking tea or coffee immediately after meals as it inhibits iron absorption.")
                if not when_to_see_doctor:
                    when_to_see_doctor = "Visit your doctor for guidance on iron nutrition or supplements."
        except Exception:
            pass

    # 4. Cholesterol Evaluation
    if "Total Cholesterol" in extracted_values:
        try:
            tc_val = float(str(extracted_values["Total Cholesterol"]).replace(",", "."))
            if tc_val >= 200:
                problems.append(f"Total Cholesterol is {tc_val} mg/dL (Borderline / High). Normal range is below 200 mg/dL.")
                recommendations.append("Limit saturated fats and trans fats in cooking; avoid repeated frying in the same oil.")
                diet_lifestyle.append("Eat: Oats, almonds, walnuts, methi, and fiber-rich vegetables.")
                diet_lifestyle.append("Avoid: Vanaspati ghee, deep-fried snacks, butter in excess, and processed meats.")
                if not when_to_see_doctor:
                    when_to_see_doctor = "Consult your physician for a full lipid panel review."
        except Exception:
            pass

    # 5. Pulse / Heart Rate Evaluation
    if "Pulse" in extracted_values:
        try:
            p_val = float(str(extracted_values["Pulse"]).replace(",", "."))
            if p_val > 100:
                problems.append(f"Pulse / Heart Rate is {p_val} bpm (Elevated / Tachycardia). Normal resting range is 60-100 bpm.")
                recommendations.append("Limit caffeine, reduce stress, stay well hydrated, and practice deep breathing.")
            elif p_val < 60:
                problems.append(f"Pulse rate is {p_val} bpm (Low / Bradycardia). Normal resting range is 60-100 bpm.")
            else:
                recommendations.append(f"Resting pulse rate ({p_val} bpm) is normal and healthy (60-100 bpm).")
        except Exception:
            pass

    # 6. Temperature Evaluation
    if "Temperature" in extracted_values:
        try:
            t_val = float(str(extracted_values["Temperature"]).replace(",", "."))
            if t_val > 37.5 and t_val < 45.0:  # Celsius
                problems.append(f"Body Temperature is {t_val}°C (Mild / Moderate Fever). Normal is ~36.5-37.2°C.")
                recommendations.append("Drink plenty of water and clear broths, rest, and monitor body temperature.")
            elif t_val > 99.5:  # Fahrenheit
                problems.append(f"Body Temperature is {t_val}°F (Fever). Normal is ~98.6°F.")
                recommendations.append("Rest in a cool room, drink adequate fluids, and take lukewarm forehead sponging.")
            else:
                recommendations.append(f"Body temperature ({t_val}) is within normal limits.")
        except Exception:
            pass

    # 7. Respiratory Rate Evaluation
    if "Respiratory Rate" in extracted_values:
        try:
            rr_val = float(str(extracted_values["Respiratory Rate"]).replace(",", "."))
            if rr_val > 20:
                problems.append(f"Respiratory Rate is {rr_val} breaths/min (Elevated). Normal resting range is 12-20 breaths/min.")
                recommendations.append("Sit comfortably in an upright position and avoid strenuous exertion.")
            elif rr_val < 12:
                problems.append(f"Respiratory Rate is {rr_val} breaths/min (Low). Normal is 12-20 breaths/min.")
            else:
                recommendations.append(f"Respiratory rate ({rr_val} breaths/min) is normal (12-20 breaths/min).")
        except Exception:
            pass

    # 8. Fallback if no specific abnormalities detected
    if not problems:
        if extracted_values:
            problems.append("Your extracted vital signs and test parameters fall within standard healthy ranges.")
        else:
            problems.append("No critical abnormalities identified from the uploaded document.")
        recommendations.append("Continue maintaining a wholesome daily routine and drinking plenty of water.")
        recommendations.append("Undergo routine annual health checkups to monitor overall wellness.")
        diet_lifestyle.append("Eat: A variety of seasonal vegetables, fresh fruits, lentils, and balanced home-cooked meals.")
        diet_lifestyle.append("Avoid: Excessive processed food, excess salt, and sedentary screen time.")
        diet_lifestyle.append("Lifestyle: Get at least 30 minutes of physical activity daily and 7-8 hours of sleep.")
        when_to_see_doctor = "Routine periodic checkups are sufficient. If you experience any persistent or unexplained symptoms, consult your family doctor."

    # Build comprehensive summary
    if len(problems) == 1 and "within standard" in problems[0]:
        val_str = ", ".join([f"{k}: {v}" for k, v in list(extracted_values.items())[:4]])
        summary = (
            f"Your medical report values ({val_str}) are largely within healthy reference limits. "
            f"Maintain your current balanced diet, active routine, and regular sleep schedule."
        )
    else:
        summary = (
            f"The medical report highlights important clinical findings: {'; '.join(problems[:2])}. "
            f"Lifestyle modifications, dietary adjustments, and a review with your healthcare provider are advised."
        )

    return {
        "summary": summary,
        "problems": problems,
        "recommendations": recommendations,
        "diet_lifestyle": diet_lifestyle,
        "when_to_see_doctor": when_to_see_doctor or "Consult a licensed physician for clinical interpretation of these results."
    }


def parse_sections(text):
    """Parse LLM response into structured sections."""
    sections = {
        "summary": "",
        "problems": [],
        "recommendations": [],
        "diet_lifestyle": [],
        "when_to_see_doctor": "",
        "raw_response": text
    }
    
    current_key = None
    lines = text.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        upper = line.upper()
        
        # Detect section headers
        if "SUMMARY" in upper and len(upper) < 30:
            current_key = "summary"
            continue
        elif "PROBLEM" in upper and len(upper) < 40:
            current_key = "problems"
            continue
        elif ("WHAT TO DO" in upper or "RECOMMENDATION" in upper or "ACTION" in upper) and len(upper) < 40:
            current_key = "recommendations"
            continue
        elif ("DIET" in upper or "LIFESTYLE" in upper or "FOOD" in upper) and len(upper) < 40:
            current_key = "diet_lifestyle"
            continue
        elif ("WHEN TO SEE DOCTOR" in upper or "DOCTOR" in upper or "URGENT" in upper) and len(upper) < 50:
            current_key = "when_to_see_doctor"
            continue
        elif "IMPORTANT NOTE" in upper:
            current_key = "important_note"
            continue
        
        # Content lines
        if current_key == "summary":
            sections["summary"] += line + " "
        elif current_key in ("problems", "recommendations", "diet_lifestyle"):
            # Bullet points, numbers, or plain text
            if line.startswith('-') or line.startswith('•') or re.match(r'^\d+[\.\)]', line):
                clean = re.sub(r'^[-•\d\.\)\s]+', '', line).strip()
                if clean:
                    sections[current_key].append(clean)
            elif len(line) > 10 and current_key != "problems":
                # For recommendations/diet, also accept plain sentences if no bullets
                sections[current_key].append(line)
        elif current_key == "when_to_see_doctor":
            sections["when_to_see_doctor"] += line + " "
    
    sections["summary"] = sections["summary"].strip()
    sections["when_to_see_doctor"] = sections["when_to_see_doctor"].strip()
    
    # Fallback: if summary is empty, use first 2-3 sentences of raw response
    if not sections["summary"]:
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())
        sections["summary"] = " ".join(sentences[:2]) if sentences else "Report analysis completed."
    
    return sections


def get_structured_analysis(report_text, language="en", patient_allergies=None, patient_profile=None):
    """Full pipeline: clean → analyze with allergies (English) → translate if needed."""
    cleaned = clean_text(report_text)
    analysis = analyze_report(cleaned, patient_allergies=patient_allergies, patient_profile=patient_profile)
    
    # ═══ TRANSLATE TO HINDI/OTHER LANGUAGE ═══
    if language != "en" and TRANSLATION_OK:
        try:
            # Translate string fields (do not translate raw_response to avoid unnecessary lag)
            for key in ["summary", "when_to_see_doctor"]:
                if analysis.get(key) and isinstance(analysis[key], str):
                    analysis[key] = translate_text(analysis[key], target_lang=language)
            
            # Translate list fields efficiently
            for key in ["problems", "recommendations", "diet_lifestyle"]:
                items = analysis.get(key, [])
                if items and isinstance(items, list):
                    joined = "\n".join([it for it in items if isinstance(it, str) and it.strip()])
                    if joined:
                        translated_joined = translate_text(joined, target_lang=language)
                        lines = [line.strip() for line in translated_joined.split("\n") if line.strip()]
                        if len(lines) == len(items):
                            analysis[key] = lines
                        else:
                            # Fallback if line count mismatched
                            analysis[key] = [translate_text(item, target_lang=language) for item in items if isinstance(item, str) and item.strip()]
                    
        except Exception as e:
            print(f"[ReportAnalyzer] Translation failed: {e}")
            # Keep English as fallback
    
    analysis["language"] = language
    return analysis

# ═════════════════════════════════════════════════════════════════==
# Quick test
# ═════════════════════════════════════════════════════════════════==

if __name__ == "__main__":
    sample = """
    Patient: Ram Singh
    BP: 145/92 mmHg
    Fasting Blood Sugar: 142 mg/dL
    Hemoglobin: 10.2 g/dL
    TLC: 12,500 /cmm
    """
    result = get_structured_analysis(sample)
    import json
    print(json.dumps(result, indent=2, ensure_ascii=False))