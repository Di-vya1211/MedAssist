"""
core/instant_cache.py
Ultra-fast in-memory clinical cache for 0-latency instant button responses.
Provides pre-indexed, verified clinical data in both English and Hindi for:
- Top Diseases (Diabetes, Asthma, Pneumonia, Arthritis, Common Cold, Coronavirus, Malaria, Hypertension)
- Top Drugs (Paracetamol, Ibuprofen, Aspirin, Metformin, Amoxicillin, Cetirizine)
- Top Medical Reports (CBC, Lipid & Glucose, Renal & Liver)
- Common Symptom Checker query profiles (Fever & Cough, Headache, Stomach Pain, Breathing Issue, Joint Pain)
"""

from typing import Dict, Any, Optional

# ===========================================================================
# 1. INSTANT DISEASES (ENGLISH & HINDI)
# ===========================================================================
INSTANT_DISEASES: Dict[str, Dict[str, Any]] = {
    "diabetes": {
        "disease_name": "Type 2 Diabetes Mellitus",
        "description": "A chronic metabolic condition characterized by elevated blood glucose levels resulting from insulin resistance and progressive pancreatic beta-cell dysfunction.",
        "symptoms": [
            "Frequent urination (polyuria), especially at night",
            "Excessive thirst (polydipsia) and constant dry mouth",
            "Unexplained weight loss despite increased appetite",
            "Persistent fatigue, sluggishness, and blurred vision",
            "Slow-healing cuts, sores, and recurring infections"
        ],
        "precautions": [
            "Maintain a low-glycemic, high-fiber diet rich in whole grains and vegetables",
            "Engage in at least 150 minutes of moderate aerobic exercise weekly",
            "Track fasting and postprandial blood glucose routinely",
            "Inspect feet daily for numbness, ulcers, or pressure points",
            "Undergo biannual HbA1c testing and annual retinal screenings"
        ],
        "diagnostic_tests": [
            "Fasting Plasma Glucose (FPG)",
            "Hemoglobin A1c (HbA1c) Test",
            "Oral Glucose Tolerance Test (OGTT)",
            "Postprandial Blood Glucose (PPBS)",
            "Serum Creatinine and eGFR Panel",
            "Lipid Profile Test",
            "Urinary Albumin-to-Creatinine Ratio (UACR)"
        ],
        "treatment": [
            "Metformin (first-line biguanide therapy)",
            "SGLT2 inhibitors (Empagliflozin, Dapagliflozin)",
            "GLP-1 receptor agonists (Liraglutide, Semaglutide)",
            "Sulfonylureas (Glimepiride) or DPP-4 inhibitors",
            "Basal and bolus insulin therapy when indicated"
        ],
        "risk_factors": [
            "Sedentary lifestyle and abdominal obesity (BMI > 25)",
            "Family history in first-degree relatives",
            "Age above 40 years and gestational diabetes history",
            "Hypertension and dyslipidemia"
        ],
        "when_to_see_doctor": "Seek emergency medical care immediately if experiencing deep rapid breathing, confusion, extreme dehydration, or blood glucose exceeding 350 mg/dL (signs of DKA or HHS).",
        "confidence": "HIGH"
    },
    "asthma": {
        "disease_name": "Bronchial Asthma",
        "description": "A chronic inflammatory disorder of the airways causing recurring episodes of wheezing, breathlessness, chest tightness, and coughing due to bronchial hyperresponsiveness.",
        "symptoms": [
            "Wheezing (high-pitched whistling sound during exhalation)",
            "Shortness of breath (dyspnea) worsened by exertion",
            "Persistent chest tightness or feeling of suffocation",
            "Nighttime or early morning coughing spasms",
            "Difficulty speaking in complete sentences during attacks"
        ],
        "precautions": [
            "Identify and strictly avoid personal triggers (dust, smoke, pollen, cold air)",
            "Always carry a fast-acting rescue inhaler (Salbutamol)",
            "Use a peak flow meter daily to monitor airway obstruction",
            "Maintain optimal indoor humidity and avoid tobacco smoke",
            "Receive annual influenza and pneumococcal vaccinations"
        ],
        "diagnostic_tests": [
            "Spirometry with Bronchodilator Reversibility",
            "Peak Expiratory Flow (PEF) Monitoring",
            "Fractional Exhaled Nitric Oxide (FeNO) Test",
            "Chest X-Ray (to exclude pneumonia or pneumothorax)",
            "Allergy Skin Prick Testing",
            "Complete Blood Count (CBC with Absolute Eosinophil Count)"
        ],
        "treatment": [
            "Inhaled Corticosteroids (Budesonide, Fluticasone) as maintenance",
            "Short-Acting Beta-2 Agonists (Salbutamol) for acute relief",
            "Long-Acting Beta-2 Agonists (Formoterol, Salmeterol)",
            "Leukotriene Receptor Antagonists (Montelukast)",
            "Oral corticosteroids for severe acute exacerbations"
        ],
        "risk_factors": [
            "Genetic predisposition and family history of atopy",
            "Frequent childhood respiratory infections",
            "Exposure to second-hand cigarette smoke and occupational chemicals",
            "Allergic rhinitis and eczema history"
        ],
        "when_to_see_doctor": "Call 108/102 immediately if lips or fingernails turn blue, rescue inhaler provides no relief, or there is severe retractions around ribs while breathing.",
        "confidence": "HIGH"
    },
    "pneumonia": {
        "disease_name": "Pneumonia (Acute Lung Infection)",
        "description": "An inflammatory condition of the lung parenchyma primarily affecting the microscopic air sacs (alveoli), commonly caused by bacterial, viral, or fungal pathogens.",
        "symptoms": [
            "High fever accompanied by shaking chills (rigors)",
            "Productive cough with green, yellow, or rusty sputum",
            "Sharp, stabbing pleuritic chest pain aggravated by deep breathing",
            "Rapid, shallow breathing (tachypnea) and shortness of breath",
            "Profound fatigue, low appetite, and low blood oxygen saturation"
        ],
        "precautions": [
            "Rest completely in bed and maintain adequate oral hydration",
            "Monitor oxygen levels with a pulse oximeter (seek help if SpO2 < 93%)",
            "Practice deep breathing exercises and use steam inhalation",
            "Complete the entire antibiotic/antiviral regimen without skipping doses",
            "Get vaccinated against pneumococcus and seasonal influenza"
        ],
        "diagnostic_tests": [
            "Chest X-Ray (PA and Lateral views)",
            "Complete Blood Count (CBC with elevated WBC and neutrophil shift)",
            "Pulse Oximetry and Arterial Blood Gases (ABG)",
            "Sputum Gram Stain and Culture",
            "C-Reactive Protein (CRP) and Procalcitonin Levels"
        ],
        "treatment": [
            "Empirical Antibiotic therapy (Amoxicillin-Clavulanate, Azithromycin, Ceftriaxone)",
            "Supplemental oxygen therapy if hypoxic",
            "Antipyretics (Paracetamol) for fever and pain relief",
            "Oral rehydration and intravenous fluids if dehydrated",
            "Bronchodilators if wheezing or airway obstruction is present"
        ],
        "risk_factors": [
            "Extreme age (infants under 2 years and adults over 65 years)",
            "Chronic lung conditions (COPD, asthma, bronchiectasis)",
            "Immunocompromised states and poorly controlled diabetes",
            "Recent viral respiratory infection (e.g. influenza)"
        ],
        "when_to_see_doctor": "Call 108 immediately if you experience bluish discoloration of lips, confusion, extreme difficulty breathing, or persistent fever with inability to keep liquids down.",
        "confidence": "HIGH"
    },
    "arthritis": {
        "disease_name": "Arthritis (Osteo & Rheumatoid)",
        "description": "Inflammatory or degenerative disorders affecting one or more joints, leading to cartilage wear, pain, stiffness, and restricted musculoskeletal mobility.",
        "symptoms": [
            "Joint pain, aching, or throbbing during or after movement",
            "Joint stiffness, particularly morning stiffness lasting > 30 minutes",
            "Swelling, tenderness, and warmth around affected joints",
            "Crepitus (grating sensation or sound when moving the joint)",
            "Loss of joint flexibility and gradual functional limitation"
        ],
        "precautions": [
            "Maintain a healthy body weight to reduce mechanical stress on weight-bearing joints",
            "Perform low-impact exercises (swimming, cycling, gentle yoga)",
            "Use hot fomentation for morning stiffness and cold packs for acute swelling",
            "Avoid repetitive high-impact joint strain and heavy lifting",
            "Consume an anti-inflammatory diet rich in omega-3 fatty acids"
        ],
        "diagnostic_tests": [
            "X-Rays of affected joints (demonstrating joint space narrowing)",
            "Rheumatoid Factor (RF) Blood Test",
            "Anti-Cyclic Citrullinated Peptide (Anti-CCP) Antibodies",
            "Erythrocyte Sedimentation Rate (ESR) and C-Reactive Protein (CRP)",
            "Serum Uric Acid (to rule out Gout)",
            "Synovial Fluid Analysis"
        ],
        "treatment": [
            "Acetaminophen or topical NSAIDs for mild osteoarthritis",
            "Oral NSAIDs (Ibuprofen, Naproxen) with gastric protection",
            "Disease-Modifying Antirheumatic Drugs (DMARDs like Methotrexate) for RA",
            "Intra-articular corticosteroid or hyaluronic acid injections",
            "Physical therapy, joint bracing, and joint replacement surgery in severe cases"
        ],
        "risk_factors": [
            "Increasing age and female gender",
            "Obesity and prior joint trauma or sports injuries",
            "Genetic factors and autoimmune predisposition",
            "Repetitive joint stress occupations"
        ],
        "when_to_see_doctor": "Consult a rheumatologist or orthopedic doctor if you experience sudden intense joint redness, severe swelling with fever, or inability to bear weight on the joint.",
        "confidence": "HIGH"
    },
    "coronavirus": {
        "disease_name": "COVID-19 (Coronavirus Disease)",
        "description": "An infectious respiratory disease caused by the SARS-CoV-2 virus, presenting across a spectrum from asymptomatic to severe respiratory failure.",
        "symptoms": [
            "Fever, dry cough, and profound fatigue",
            "Loss of taste (ageusia) or loss of smell (anosmia)",
            "Sore throat, headache, body aches, and nasal congestion",
            "Shortness of breath or difficulty breathing",
            "Gastrointestinal symptoms like diarrhea and nausea"
        ],
        "precautions": [
            "Self-isolate immediately in a well-ventilated room",
            "Wear a certified N95 or well-fitting mask around others",
            "Monitor blood oxygen saturation (SpO2) every 4 to 6 hours",
            "Maintain optimal hydration and rest strictly",
            "Stay up-to-date with recommended COVID-19 booster vaccines"
        ],
        "diagnostic_tests": [
            "RT-PCR Nasopharyngeal Swab Test (Gold Standard)",
            "Rapid Antigen Test (RAT)",
            "High-Resolution Computed Tomography (HRCT) of Chest (if severe)",
            "D-Dimer, Ferritin, and CRP Inflammatory Markers",
            "Complete Blood Count (CBC) with Absolute Lymphocyte Count"
        ],
        "treatment": [
            "Antipyretics (Paracetamol 650mg) for fever and pain",
            "Oral hydration solutions and nutritional support",
            "Antiviral medications (Paxlovid/Remdesivir) for high-risk patients",
            "Inhaled Budesonide for persistent cough",
            "Supplemental oxygen and systemic steroids for severe hypoxemic illness"
        ],
        "risk_factors": [
            "Age 60 years and above",
            "Underlying medical conditions (Diabetes, Hypertension, Obesity, COPD)",
            "Immunocompromised status",
            "Unvaccinated or partially vaccinated status"
        ],
        "when_to_see_doctor": "Seek emergency medical attention if SpO2 drops below 94%, you have persistent chest pain/pressure, confusion, or difficulty staying awake.",
        "confidence": "HIGH"
    },
    "common cold": {
        "disease_name": "Acute Upper Respiratory Infection (Common Cold)",
        "description": "A mild, self-limiting viral infection of the upper respiratory tract primarily caused by rhinoviruses, coronaviruses, or adenoviruses.",
        "symptoms": [
            "Runny or congested nose with sneezing",
            "Scratchy, sore throat and mild dry cough",
            "Low-grade fever and mild body malaise",
            "Mild headache and watery eyes",
            "Decreased sense of smell and taste"
        ],
        "precautions": [
            "Get plenty of rest and drink warm water, soups, and herbal teas",
            "Perform saline nasal rinses and steam inhalation twice daily",
            "Gargle with warm salt water to relieve throat irritation",
            "Wash hands frequently and wear a mask to prevent household transmission",
            "Avoid chilled drinks, direct air conditioner blasts, and smoking"
        ],
        "diagnostic_tests": [
            "Clinical evaluation (tests generally not required for uncomplicated colds)",
            "Complete Blood Count (CBC) if symptoms persist > 10 days",
            "Rapid Throat Swab (to rule out Streptococcal Pharyngitis)",
            "Chest X-Ray (only if pneumonia is suspected)"
        ],
        "treatment": [
            "Paracetamol (500mg-650mg) for fever and body ache",
            "Antihistamines (Cetirizine 10mg) for sneezing and rhinorrhea",
            "Decongestant nasal sprays (Xylometazoline, max 3-5 days)",
            "Warm fluids, honey-ginger concoctions, and vitamin C supplements",
            "Antibiotics are strictly NOT indicated for viral colds"
        ],
        "risk_factors": [
            "Exposure to infected individuals in crowded spaces",
            "Weakened immunity, lack of sleep, and extreme cold exposure",
            "Infants and elderly individuals"
        ],
        "when_to_see_doctor": "See a doctor if fever exceeds 102°F, symptoms last longer than 10-14 days, or you develop severe ear pain, sinus pressure, or difficulty breathing.",
        "confidence": "HIGH"
    },
    "hypertension": {
        "disease_name": "Essential Hypertension (High Blood Pressure)",
        "description": "A persistent elevation of systemic arterial blood pressure (systolic >= 130 mmHg or diastolic >= 80 mmHg) that places excessive mechanical stress on the heart, kidneys, and vasculature.",
        "symptoms": [
            "Frequently asymptomatic ('the silent killer')",
            "Occipital morning headaches and throbbing temples",
            "Dizziness, lightheadedness, or ringing in ears (tinnitus)",
            "Occasional shortness of breath or nosebleeds (epistaxis)",
            "Vision blurring or chest palpitations under stress"
        ],
        "precautions": [
            "Restrict sodium intake to under 2,000 mg (under 1 teaspoon of salt) daily",
            "Follow the DASH diet (high potassium, vegetables, fruits, low saturated fat)",
            "Engage in 30 minutes of aerobic physical activity at least 5 days a week",
            "Limit alcohol consumption and eliminate tobacco smoking",
            "Measure and log blood pressure twice daily at home"
        ],
        "diagnostic_tests": [
            "24-Hour Ambulatory Blood Pressure Monitoring (ABPM)",
            "12-Lead Electrocardiogram (ECG)",
            "Lipid Profile Panel",
            "Serum Creatinine and Blood Urea Nitrogen (BUN)",
            "Urinalysis for Microalbuminuria",
            "Echocardiogram (to evaluate left ventricular hypertrophy)"
        ],
        "treatment": [
            "Angiotensin Receptor Blockers (Telmisartan, Losartan)",
            "Calcium Channel Blockers (Amlodipine)",
            "ACE Inhibitors (Enalapril, Ramipril)",
            "Thiazide Diuretics (Chlorthalidone, Hydrochlorothiazide)",
            "Beta-blockers for comorbid cardiac indications"
        ],
        "risk_factors": [
            "Excess body weight and abdominal adiposity",
            "High dietary sodium and low potassium intake",
            "Chronic stress and sleep apnea (OSA)",
            "Advancing age and family history"
        ],
        "when_to_see_doctor": "Seek emergency care immediately if blood pressure exceeds 180/120 mmHg or is accompanied by chest pain, shortness of breath, numbness, or difficulty speaking (Hypertensive Emergency).",
        "confidence": "HIGH"
    }
}

INSTANT_DISEASES_HI: Dict[str, Dict[str, Any]] = {
    "diabetes": {
        "disease_name": "टाइप 2 मधुमेह (Type 2 Diabetes)",
        "description": "यह एक दीर्घकालिक मेटाबॉलिक स्थिति है जिसमें इंसुलिन प्रतिरोध के कारण रक्त शर्करा (ब्लड शुगर) का स्तर लगातार अधिक रहता है।",
        "symptoms": [
            "बार-बार पेशाब आना (विशेष रूप से रात में)",
            "अत्यधिक प्यास लगना और मुँह सूखना",
            "भूख अधिक लगने पर भी अकारण वजन घटना",
            "लगातार कमजोरी, सुस्ती और आँखों से धुंधला दिखना",
            "घाव या चोट का बहुत धीमी गति से भरना"
        ],
        "precautions": [
            "कम ग्लाइसेमिक और फाइबर से भरपूर आहार लें (हरी सब्जियां, साबुत अनाज)",
            "सप्ताह में कम से कम 150 मिनट मध्यम व्यायाम या तेज पैदल चलें",
            "नियमित रूप से खाली पेट और भोजन के बाद ब्लड शुगर की जाँच करें",
            "पैरों की प्रतिदिन जाँच करें (सुन्नपन या छालों के लिए)",
            "वर्ष में दो बार HbA1c टेस्ट और आँखों की जाँच अवश्य कराएं"
        ],
        "diagnostic_tests": [
            "फास्टिंग प्लाज्मा ग्लूकोज (FPG Test)",
            "HbA1c (ग्लाइकेटेड हीमोग्लोबिन टेस्ट)",
            "ओरल ग्लूकोज टॉलरेंस टेस्ट (OGTT)",
            "पोस्टप्रांडियल ब्लड शुगर (PPBS)",
            "किडनी फंक्शन टेस्ट (Serum Creatinine & eGFR)",
            "लिपिड प्रोफाइल (Lipid Profile Panel)"
        ],
        "treatment": [
            "मेटफॉर्मिन (Metformin - पहली पंक्ति की दवा)",
            "SGLT2 इनहिबिटर (Empagliflozin, Dapagliflozin)",
            "सल्फोनिलयूरिया (Glimepiride) या DPP-4 इनहिबिटर",
            "चिकित्सक के परामर्श अनुसार इंसुलिन थेरेपी"
        ],
        "risk_factors": [
            "शारीरिक निष्क्रियता और मोटापा",
            "परिवार में मधुमेह का इतिहास",
            "40 वर्ष से अधिक आयु और उच्च रक्तचाप"
        ],
        "when_to_see_doctor": "यदि बहुत तेज सांस आ रही हो, अत्यधिक भ्रम या निर्जलीकरण हो, या शुगर 350 mg/dL से अधिक हो तो तुरंत आपातकालीन चिकित्सा (108) लें।",
        "confidence": "HIGH"
    },
    "asthma": {
        "disease_name": "ब्रोन्कियल अस्थमा / दमा (Bronchial Asthma)",
        "description": "यह वायुमार्ग (श्वसन नलियों) की एक दीर्घकालिक सूजन संबंधी बीमारी है, जिससे सांस लेने में कठिनाई, सीने में जकड़न और घरघराहट होती है।",
        "symptoms": [
            "सांस छोड़ते समय सीने से सीटी जैसी आवाज (घरघराहट)",
            "सांस फूलना, खासकर मेहनत या सीढ़ियां चढ़ते समय",
            "सीने में लगातार भारीपन या जकड़न महसूस होना",
            "रात में या सुबह तड़के तेज खांसी के दौरे",
            "अटैक के दौरान पूरे वाक्य बोलने में कठिनाई"
        ],
        "precautions": [
            "एलर्जी बढ़ाने वाले कारकों (धूल, धुआं, परागकण, ठंडी हवा) से बचें",
            "हमेशा अपनी आपातकालीन इनहेलर (Salbutamol) साथ रखें",
            "कमरे में नमी और धूल से बचाव रखें तथा धूम्रपान से दूर रहें",
            "वार्षिक फ्लू और न्यूमोकोकल का टीका लगवाएं"
        ],
        "diagnostic_tests": [
            "स्पायरोमेट्री टेस्ट (Spirometry Lung Function)",
            "पीक एक्सपायरेटरी फ्लो (PEF Monitoring)",
            "चेस्ट एक्स-रे (Chest X-Ray)",
            "एब्सोल्यूट इओसिनोफिल काउंट (CBC with AEC)"
        ],
        "treatment": [
            "इन्हेल्ड कॉर्टिकोस्टेरॉइड्स (Budesonide इनहेलर)",
            "आपातकालीन रिलीफ इनहेलर (Salbutamol Inhaler)",
            "ल्यूकोट्रिएन रिसेप्टर विरोधी (Montelukast)"
        ],
        "risk_factors": [
            "आनुवंशिक कारण या परिवार में एलर्जी/दमा",
            "बचपन में श्वसन संक्रमण और प्रदूषण का जोखिम"
        ],
        "when_to_see_doctor": "यदि होंठ या नाखून नीले पड़ने लगें, इनहेलर से भी आराम न मिले या सांस लेने में अत्यंत कष्ट हो तो तुरंत 108 पर कॉल करें।",
        "confidence": "HIGH"
    },
    "pneumonia": {
        "disease_name": "निमोनिया (Pneumonia - फेफड़ों का संक्रमण)",
        "description": "फेफड़ों के वायुकोशों (alveoli) का गंभीर संक्रमण, जिसमें फेफड़ों में मवाद या तरल पदार्थ भर जाता है।",
        "symptoms": [
            "कंपकंपी के साथ तेज बुखार आना",
            "पीले, हरे या भूरे बलगम वाली खांसी",
            "सांस लेते समय सीने में तीखा चुभन भरा दर्द",
            "तेज सांस चलना और सांस फूलना",
            "अत्यधिक कमजोरी और ऑक्सीजन स्तर में गिरावट"
        ],
        "precautions": [
            "बिस्तर पर पूरा आराम करें और प्रचुर मात्रा में तरल पदार्थ पिएं",
            "पल्स ऑक्सीमीटर से ऑक्सीजन स्तर की निगरानी करें (SpO2 < 93% पर डॉक्टर से मिलें)",
            "भाप लें और निर्धारित एंटीबायोटिक का पूरा कोर्स बिना छोड़े लें"
        ],
        "diagnostic_tests": [
            "चेस्ट एक्स-रे (Chest X-Ray PA View)",
            "कम्प्लीट ब्लड काउंट (CBC with Differential)",
            "पल्स ऑक्सीमेट्री और स्पुटम टेस्ट"
        ],
        "treatment": [
            "एंटीबायोटिक थेरेपी (Amoxicillin-Clavulanate, Azithromycin)",
            "बुखार और दर्द के लिए पेरासिटामोल (Paracetamol)",
            "आवश्यकता पड़ने पर ऑक्सीजन सपोर्ट"
        ],
        "risk_factors": [
            "2 वर्ष से छोटे बच्चे और 65 वर्ष से अधिक उम्र के बुजुर्ग",
            "कमजोर प्रतिरक्षा प्रणाली या पहले से दमा/मधुमेह"
        ],
        "when_to_see_doctor": "यदि होंठ नीले पड़ें, सांस लेने में अत्यधिक कठिनाई हो या लगातार तेज बुखार रहे तो तुरंत अस्पताल (108) जाएं।",
        "confidence": "HIGH"
    },
    "arthritis": {
        "disease_name": "गठिया / जोड़ों का दर्द (Arthritis)",
        "description": "एक या अधिक जोड़ों में सूजन और कार्टिलेज के घिसने की स्थिति, जिससे जोड़ों में दर्द, अकड़न और चलने-फिरने में परेशानी होती है।",
        "symptoms": [
            "चलने-फिरने पर जोड़ों में तेज दर्द या टीस उठना",
            "सुबह उठने पर जोड़ों में 30 मिनट से अधिक अकड़न रहना",
            "जोड़ों में सूजन, लालिमा और गर्माहट",
            "जोड़ हिलाने पर चरचराहट की आवाज आना",
            "उंगलियों या घुटनों को मोड़ने में कठिनाई"
        ],
        "precautions": [
            "वजन नियंत्रित रखें ताकि घुटनों पर अत्यधिक दबाव न पड़े",
            "हल्का व्यायाम (तैराकी, साइकिल चलाना, कोमल योग) करें",
            "सुबह की अकड़न के लिए गर्म सिकाई और सूजन के लिए बर्फ की सिकाई करें",
            "ओमेगा-3 युक्त और सूजन-रोधी आहार लें"
        ],
        "diagnostic_tests": [
            "प्रभावित जोड़ों का एक्स-रे (Joint X-Ray)",
            "आरएच फैक्टर टेस्ट (Rheumatoid Factor - RF)",
            "एंटी-सीसीपी एंटीबॉडी (Anti-CCP Test)",
            "यूरिक एसिड टेस्ट (Serum Uric Acid - गाउट जांचने के लिए)"
        ],
        "treatment": [
            "दर्द कम करने के लिए पेरासिटामोल या दर्दनिवारक जेल",
            "चिकित्सक के परामर्श से NSAIDs दवाएं",
            "फिजियोथेरेपी और जोड़ों के सपोर्ट ब्रेसिज़"
        ],
        "risk_factors": [
            "बढ़ती उम्र, मोटापा और जोड़ों की पुरानी चोट",
            "आनुवंशिक और ऑटोइम्यून कारक"
        ],
        "when_to_see_doctor": "यदि जोड़ में अचानक अत्यधिक सूजन व लालिमा आ जाए, बुखार हो या पैर पर वजन न रखा जाए तो तुरंत डॉक्टर से संपर्क करें।",
        "confidence": "HIGH"
    },
    "coronavirus": {
        "disease_name": "कोविड-19 (COVID-19 Corona)",
        "description": "सार्स-कोव-2 वायरस के कारण होने वाला संक्रामक श्वसन रोग जो हल्के से लेकर गंभीर रूप धारण कर सकता है।",
        "symptoms": [
            "तेज बुखार, सूखी खांसी और अत्यधिक थकान",
            "स्वाद और गंध की क्षमता का अचानक चले जाना",
            "गले में खराश, सिरदर्द और बदन दर्द",
            "सांस फूलना या सीने में भारीपन"
        ],
        "precautions": [
            "तुरंत हवादार कमरे में आइसोलेट हो जाएं",
            "N95 मास्क पहनें और हाथों की स्वच्छता बनाए रखें",
            "हर 4-6 घंटे में SpO2 ऑक्सीजन स्तर मापें"
        ],
        "diagnostic_tests": [
            "आरटी-पीसीआर टेस्ट (RT-PCR Nasopharyngeal Swab)",
            "रैपिड एंटीजन टेस्ट (Rapid Antigen)",
            "चेस्ट सीटी स्कैन (HRCT Chest - गंभीर मामलों में)"
        ],
        "treatment": [
            "बुखार के लिए पेरासिटामोल (Paracetamol 650mg)",
            "भरपूर तरल पदार्थ और ओआरएस का सेवन",
            "डॉक्टर के निर्देशानुसार भाप और कफ सिरप"
        ],
        "risk_factors": [
            "बुजुर्ग व्यक्ति और पहले से मौजूद रोग (डायबिटीज, बीपी)",
            "टीकाकरण न हुआ होना"
        ],
        "when_to_see_doctor": "ऑक्सीजन SpO2 स्तर 94% से नीचे जाने या सीने में लगातार दर्द होने पर तुरंत आपातकालीन चिकित्सा लें।",
        "confidence": "HIGH"
    },
    "common cold": {
        "disease_name": "सामान्य सर्दी-जुकाम (Common Cold)",
        "description": "ऊपरी श्वसन तंत्र का एक सामान्य वायरल संक्रमण जो मुख्य रूप से राइनोवायरस के कारण होता है।",
        "symptoms": [
            "नाक बहना, छींकें आना और नाक बंद होना",
            "गले में खराश और हल्की सूखी खांसी",
            "हल्का बुखार, सिरदर्द और सुस्ती",
            "आंखों से पानी आना"
        ],
        "precautions": [
            "भरपूर आराम करें और गुनगुना पानी, सूप व हर्बल चाय पिएं",
            "दिन में दो बार भाप लें और गर्म नमक के पानी से गरारे करें",
            "ठंडे पेय पदार्थों और सीधे एसी की हवा से बचें"
        ],
        "diagnostic_tests": [
            "नैदानिक परीक्षण (साधारण जुकाम में विशेष टेस्ट की जरूरत नहीं होती)",
            "लक्षण 10 दिन से अधिक रहने पर कम्प्लीट ब्लड काउंट (CBC)"
        ],
        "treatment": [
            "बुखार और बदन दर्द के लिए पेरासिटामोल (Paracetamol)",
            "छींक और नाक बहने के लिए सिट्राजिन (Cetirizine 10mg)",
            "अदरक-तुलसी का काढ़ा और विटामिन सी"
        ],
        "risk_factors": [
            "संक्रमित व्यक्ति के निकट संपर्क में आना",
            "कमजोर रोग प्रतिरोधक क्षमता और अचानक ठंड लगना"
        ],
        "when_to_see_doctor": "यदि बुखार 102°F से अधिक हो, लक्षण 10 दिनों से अधिक रहें या कान व सीने में तेज दर्द हो तो डॉक्टर से मिलें।",
        "confidence": "HIGH"
    },
    "hypertension": {
        "disease_name": "उच्च रक्तचाप / हाई बीपी (Hypertension)",
        "description": "धमनियों में रक्त के अत्यधिक दबाव की स्थिति (सिस्टोलिक 130 या डायस्टोलिक 80 से अधिक) जिससे हृदय और गुर्दों पर अतिरिक्त तनाव पड़ता है।",
        "symptoms": [
            "अक्सर कोई लक्षण नहीं होते ('साइलेंट किलर')",
            "सुबह सिर के पिछले हिस्से में भारीपन व दर्द",
            "चक्कर आना या कानों में घंटी जैसी आवाज सुनाई देना",
            "घबराहट या तनाव में दृष्टि धुंधली होना"
        ],
        "precautions": [
            "दैनिक भोजन में नमक की मात्रा 1 चम्मच (2,000 mg) से कम रखें",
            "तनाव कम करें और सप्ताह में 5 दिन 30 मिनट तेज चलें",
            "तंबाकू व शराब का पूर्ण त्याग करें",
            "नियमित रूप से घर पर बीपी मापें"
        ],
        "diagnostic_tests": [
            "24 घंटे की एंबुलेटरी ब्लड प्रेशर मॉनिटरिंग",
            "ईसीजी टेस्ट (12-Lead ECG)",
            "लिपिड प्रोफाइल और किडनी फंक्शन टेस्ट"
        ],
        "treatment": [
            "एंजियोटेंसिन रिसेप्टर ब्लॉकर्स (Telmisartan)",
            "कैल्शियम चैनल ब्लॉकर्स (Amlodipine)",
            "जीवनशैली में बदलाव और नियमित दवा"
        ],
        "risk_factors": [
            "मोटापा, अत्यधिक नमक का सेवन और मानसिक तनाव",
            "उम्र और पारिवारिक इतिहास"
        ],
        "when_to_see_doctor": "यदि बीपी 180/120 से अधिक हो या साथ में सीने में दर्द, सांस लेने में तकलीफ या सुन्नपन हो तो तुरंत 108 अस्पताल जाएं।",
        "confidence": "HIGH"
    }
}


# ===========================================================================
# 2. INSTANT DRUGS (ENGLISH & HINDI)
# ===========================================================================
INSTANT_DRUGS: Dict[str, Dict[str, Any]] = {
    "paracetamol": {
        "name": "Paracetamol (Acetaminophen)",
        "brand_names": ["Crocin", "Dolo 650", "Calpol", "Tylenol", "Panadol", "Pacimol"],
        "drug_class": "Analgesic & Antipyretic (Pain Reliever & Fever Reducer)",
        "indications": "First-line management of mild-to-moderate pain (headache, toothache, muscle ache, arthritis) and fever reduction across all age groups.",
        "dosage": "Adults: 500 mg to 650 mg orally every 4 to 6 hours as needed. Maximum daily dose: 4,000 mg (4 grams) in 24 hours. Pediatrics: 10 to 15 mg/kg per dose every 4-6 hours.",
        "warnings": "Hepatotoxicity risk: Overdosage can cause severe liver failure. Avoid in severe hepatic impairment or chronic alcoholism. Never combine with other paracetamol-containing combination medicines.",
        "side_effects": "Rare at therapeutic doses. May cause nausea, allergic skin rash, or elevated liver enzymes with prolonged excessive use.",
        "pregnancy_safety": "Category B - Generally considered the safest antipyretic/analgesic during pregnancy under physician guidance."
    },
    "ibuprofen": {
        "name": "Ibuprofen",
        "brand_names": ["Brufen", "Advil", "Motrin", "Combiflam (with Paracetamol)", "Ibugesic"],
        "drug_class": "Non-Steroidal Anti-Inflammatory Drug (NSAID)",
        "indications": "Relief of inflammatory pain, arthritis flare-ups, menstrual cramps (dysmenorrhea), dental pain, and fever unresponsive to paracetamol.",
        "dosage": "Adults: 200 mg to 400 mg orally every 6 to 8 hours strictly after food. Maximum adult OTC dose: 1,200 mg/day (prescription max: 2,400 mg/day).",
        "warnings": "Gastrointestinal risk: Can cause gastric ulcers, stomach bleeding, and gastritis. Avoid in active peptic ulcer, chronic kidney disease (CKD), or third-trimester pregnancy.",
        "side_effects": "Heartburn, dyspepsia, stomach ache, mild fluid retention, dizziness, elevated blood pressure.",
        "pregnancy_safety": "Contraindicated in third trimester (risk of premature closure of ductus arteriosus and oligohydramnios)."
    },
    "aspirin": {
        "name": "Aspirin (Acetylsalicylic Acid)",
        "brand_names": ["Disprin", "Ecosprin", "Bayer Aspirin", "Loprin", "ASA"],
        "drug_class": "Antiplatelet Agent & Salicylate NSAID",
        "indications": "Secondary prevention of cardiovascular events (myocardial infarction, ischemic stroke) at low doses (75-150 mg). Temporary relief of headache and acute migraine at higher doses.",
        "dosage": "Cardiovascular prophylaxis: 75 mg to 150 mg once daily with food. Acute analgesia/fever: 300 mg to 600 mg every 4-6 hours (max 3 g/day).",
        "warnings": "High bleeding risk. Strictly contraindicated in children/teens with viral illness due to fatal Reye's syndrome risk. Do not use if you have bleeding disorders, gastric ulcers, or aspirin-exacerbated respiratory disease.",
        "side_effects": "Gastric irritation, bruising, prolonged bleeding time, tinnitus (ringing in ears) at high doses.",
        "pregnancy_safety": "High doses contraindicated; low-dose aspirin may be prescribed under strict maternal-fetal specialist supervision."
    },
    "metformin": {
        "name": "Metformin Hydrochloride",
        "brand_names": ["Glucophage", "Glycomet", "Formin", "Obimet", "Cetapin"],
        "drug_class": "Biguanide Antidiabetic Agent",
        "indications": "First-line oral pharmacotherapy for Type 2 Diabetes Mellitus; also widely utilized off-label for Polycystic Ovary Syndrome (PCOS) and insulin resistance.",
        "dosage": "Adults: Initiate at 500 mg once or twice daily with or immediately after meals to reduce gastrointestinal side effects. Titrate up to 1,000 mg twice daily (max: 2,550 mg/day). Extended release (XR) is taken once daily with dinner.",
        "warnings": "Lactic acidosis risk (rare but serious). Avoid or adjust dose if eGFR < 30 mL/min. Temporarily discontinue prior to iodinated radiocontrast procedures and major surgery.",
        "side_effects": "Nausea, diarrhea, abdominal bloating, metallic taste, long-term Vitamin B12 deficiency (monitoring advised).",
        "pregnancy_safety": "Category B - Frequently used under endocrinologist guidance for gestational diabetes when diet alone is insufficient."
    },
    "amoxicillin": {
        "name": "Amoxicillin Trihydrate",
        "brand_names": ["Mox", "Amoxil", "Augmentin (with Clavulanate)", "Novamox", "Almox"],
        "drug_class": "Aminopenicillin Beta-Lactam Antibiotic",
        "indications": "Treatment of susceptible bacterial infections: bacterial otitis media, strep throat, sinusitis, lower respiratory infections, dental abscesses, and urinary tract infections.",
        "dosage": "Adults: 250 mg to 500 mg orally every 8 hours, or 500 mg to 875 mg every 12 hours for 5 to 10 days. Pediatrics: 25 to 50 mg/kg/day in divided doses. Complete the entire course.",
        "warnings": "Hypersensitivity: STRICTLY contraindicated in penicillin-allergic patients (risk of anaphylaxis, hives, angioedema). Can cause antibiotic-associated diarrhea.",
        "side_effects": "Nausea, mild diarrhea, abdominal discomfort, skin rash, oral thrush (Candida overgrowth).",
        "pregnancy_safety": "Category B - Widely prescribed and considered safe during pregnancy when clinically indicated."
    },
    "cetirizine": {
        "name": "Cetirizine Hydrochloride",
        "brand_names": ["Zyrtec", "Cetzine", "Alerid", "Okacet", "Zyncet"],
        "drug_class": "Second-Generation H1 Antihistamine",
        "indications": "Relief of allergic rhinitis (sneezing, runny nose, itchy watery eyes, nasal pruritus), chronic idiopathic urticaria (hives), and allergic skin dermatoses.",
        "dosage": "Adults and children >= 6 years: 5 mg to 10 mg once daily, preferably at bedtime. Reduce dose in moderate-to-severe renal impairment.",
        "warnings": "May cause mild sedation in sensitive individuals. Exercise caution when driving or operating machinery. Avoid concurrent alcohol or sedative consumption.",
        "side_effects": "Drowsiness, dry mouth, headache, fatigue, mild dizziness.",
        "pregnancy_safety": "Category B - Generally acceptable during pregnancy under medical direction."
    }
}


# ===========================================================================
# 3. INSTANT MEDICAL REPORTS (ENGLISH & HINDI)
# ===========================================================================
INSTANT_SAMPLE_REPORTS: Dict[str, Dict[str, Any]] = {
    "cbc": {
        "report_type": "Complete Blood Count (CBC) with ESR",
        "summary": "The patient exhibits microcytic hypochromic anemia (Hemoglobin 10.2 g/dL) along with mild leukocytosis (WBC 12,500/mcL) and elevated ESR (28 mm/hr), pointing to iron deficiency anemia coupled with low-grade inflammatory or infectious response.",
        "values_found": {
            "Hemoglobin": "10.2 g/dL [LOW - Ref: 13.0-17.0]",
            "WBC Count": "12,500 /mcL [HIGH - Ref: 4,000-11,000]",
            "Platelets": "180,000 /mcL [NORMAL - Ref: 150k-450k]",
            "Hematocrit (PCV)": "32.1 % [LOW - Ref: 40-50%]",
            "ESR (Westergren)": "28 mm/hr [HIGH - Ref: 0-15]"
        },
        "problems": [
            "Mild Microcytic Hypochromic Anemia (Hemoglobin 10.2 g/dL)",
            "Mild Leukocytosis (WBC 12,500 /mcL, indicating acute or subacute immune activation)",
            "Elevated Inflammatory Marker (ESR 28 mm/hr)"
        ],
        "recommendations": [
            "Follow-up with Serum Ferritin and Total Iron Binding Capacity (TIBC) to quantify iron stores",
            "Initiate oral elemental iron supplementation (e.g., Ferrous Ascorbate 100 mg daily) paired with Vitamin C",
            "Screen stool for occult blood to rule out subclinical gastrointestinal blood loss",
            "Repeat Complete Blood Count (CBC) in 4 to 6 weeks to evaluate marrow response"
        ],
        "diet_lifestyle": [
            "Increase intake of dietary iron: spinach, lentils, beetroot, pomegranate, dates, and jaggery",
            "Consume lean poultry, eggs, and legumes for hemoglobin protein synthesis",
            "Avoid drinking tea, coffee, or milk within 2 hours of iron-rich meals or supplements (prevents calcium/tannin chelation)",
            "Maintain adequate hydration with at least 2.5 liters of clean water daily"
        ],
        "when_to_see_doctor": "Consult your primary care physician within 3 to 5 days. Seek immediate emergency evaluation if you develop severe dizziness, chest palpitations, or shortness of breath on mild exertion."
    },
    "lipid": {
        "report_type": "Metabolic & Lipid Profile Panel",
        "summary": "Findings reveal poorly controlled hyperglycemia (Fasting Blood Sugar 168 mg/dL, HbA1c 8.4%) accompanied by combined dyslipidemia (Total Cholesterol 245 mg/dL, LDL 162 mg/dL, Triglycerides 220 mg/dL, and low HDL 38 mg/dL), significantly increasing atherosclerotic cardiovascular risk.",
        "values_found": {
            "Fasting Glucose (FBS)": "168 mg/dL [HIGH - Diabetic Range]",
            "HbA1c Glycated Hb": "8.4 % [HIGH - Target < 7.0%]",
            "Total Cholesterol": "245 mg/dL [HIGH - Ref: < 200]",
            "LDL Bad Cholesterol": "162 mg/dL [HIGH - Ref: < 100]",
            "HDL Good Cholesterol": "38 mg/dL [LOW - Ref: > 50]",
            "Serum Triglycerides": "220 mg/dL [HIGH - Ref: < 150]"
        },
        "problems": [
            "Suboptimally Controlled Type 2 Diabetes Mellitus (HbA1c 8.4%)",
            "Atherogenic Dyslipidemia (Elevated LDL 162 mg/dL and Triglycerides 220 mg/dL)",
            "Depressed Cardioprotective HDL Cholesterol (38 mg/dL)"
        ],
        "recommendations": [
            "Consult endocrinologist or physician for antihyperglycemic medication adjustment (e.g. Metformin uptitration or SGLT2i addition)",
            "Initiate statin lipid-lowering therapy (e.g., Atorvastatin 20mg or Rosuvastatin 10mg) per clinical cardiovascular risk profile",
            "Undergo baseline Electrocardiogram (ECG) and urine microalbuminuria testing",
            "Repeat HbA1c and Lipid panel in 90 days to assess therapeutic efficacy"
        ],
        "diet_lifestyle": [
            "Adopt the Mediterranean or DASH dietary pattern: eliminate refined sugars, sweets, and sweetened beverages",
            "Substitute refined grains with high-fiber whole oats, barley, quinoa, and green vegetables",
            "Eliminate hydrogenated trans-fats, fried foods, and palm oil; use cold-pressed mustard or olive oil in moderation",
            "Engage in brisk walking for 40 minutes daily (minimum 10,000 steps)"
        ],
        "when_to_see_doctor": "Consult an endocrinologist or internal medicine specialist within 48 to 72 hours for treatment optimization. If experiencing acute chest tightness, sweating, or severe breathlessness, call 108 immediately."
    },
    "renal": {
        "report_type": "Renal & Hepatic Function Panel (KFT + LFT)",
        "summary": "Profile indicates moderate impairment in renal filtration (Serum Creatinine 1.8 mg/dL, BUN 28 mg/dL) and hyperuricemia (Uric Acid 7.8 mg/dL), alongside mild hepatocellular enzyme leakage (ALT 68 U/L, AST 54 U/L) with normal bilirubin (0.9 mg/dL).",
        "values_found": {
            "Serum Creatinine": "1.8 mg/dL [HIGH - Impaired Clearance]",
            "Blood Urea Nitrogen (BUN)": "28 mg/dL [HIGH - Ref: 7-20]",
            "Serum Uric Acid": "7.8 mg/dL [HIGH - Gout/Kidney Risk]",
            "SGPT / ALT (Liver)": "68 U/L [MILD ELEVATION - Ref: < 45]",
            "SGOT / AST (Liver)": "54 U/L [MILD ELEVATION - Ref: < 40]",
            "Total Bilirubin": "0.9 mg/dL [NORMAL - Ref: 0.2-1.2]"
        },
        "problems": [
            "Renal Functional Impairment (Creatinine 1.8 mg/dL, estimated eGFR reduced)",
            "Hyperuricemia (Serum Uric Acid 7.8 mg/dL)",
            "Mild Transaminitis (ALT 68 U/L, AST 54 U/L, suggestive of fatty liver or drug-induced enzyme rise)"
        ],
        "recommendations": [
            "CRITICAL: Avoid nephrotoxic medications, especially NSAID painkillers (Ibuprofen, Diclofenac, Naproxen); use Paracetamol cautiously for pain",
            "Order Renal Ultrasound (KUB) to assess kidney size, parenchymal echogenicity, and rule out obstruction",
            "Perform 24-hour urine protein or spot urine albumin-to-creatinine ratio (ACR)",
            "Review current prescription drugs for renal dose adjustment"
        ],
        "diet_lifestyle": [
            "Limit excessive dietary protein to 0.8g/kg body weight to reduce glomerular hyperfiltration",
            "Reduce high-purine foods (red meat, organ meats, shellfish, beer) to lower uric acid",
            "Maintain steady hydration (approx. 2 liters daily unless fluid restricted by doctor)",
            "Avoid alcohol completely to facilitate hepatic recovery and lower uric acid"
        ],
        "when_to_see_doctor": "Schedule a nephrology consultation within 48 hours. Report to emergency care immediately if you notice marked reduction in urine volume, ankle swelling, or vomiting."
    }
}


# ===========================================================================
# 4. INSTANT SYMPTOM PREDICTIONS (MATCHING Tab 5 SCHEMA EXACTLY)
# ===========================================================================
INSTANT_SYMPTOM_PREDICTIONS: Dict[str, Dict[str, Any]] = {
    "fever_cough": {
        "type": "success",
        "symptoms": ["fever", "cough", "body ache"],
        "duration": "2",
        "predictions": [
            {
                "disease": "Acute Viral Pharyngitis / Flu",
                "confidence": 86,
                "matched_symptoms": ["fever", "cough", "body ache"],
                "urgency": "moderate"
            },
            {
                "disease": "Acute Bronchitis",
                "confidence": 68,
                "matched_symptoms": ["cough", "fever"],
                "urgency": "moderate"
            },
            {
                "disease": "Early Bronchial Pneumonia",
                "confidence": 42,
                "matched_symptoms": ["cough", "body ache"],
                "urgency": "high"
            }
        ]
    },
    "headache": {
        "type": "success",
        "symptoms": ["severe headache", "nausea"],
        "duration": "1",
        "predictions": [
            {
                "disease": "Acute Migraine Attack",
                "confidence": 88,
                "matched_symptoms": ["severe headache", "nausea"],
                "urgency": "moderate"
            },
            {
                "disease": "Tension-Type Headache",
                "confidence": 62,
                "matched_symptoms": ["severe headache"],
                "urgency": "low"
            },
            {
                "disease": "Cervicogenic Cephalea",
                "confidence": 38,
                "matched_symptoms": ["severe headache"],
                "urgency": "low"
            }
        ]
    },
    "stomach_pain": {
        "type": "success",
        "symptoms": ["stomach pain", "vomiting"],
        "duration": "1",
        "predictions": [
            {
                "disease": "Acute Gastroenteritis / Food Poisoning",
                "confidence": 89,
                "matched_symptoms": ["stomach pain", "vomiting"],
                "urgency": "moderate"
            },
            {
                "disease": "Acid Peptic Disease / Gastritis",
                "confidence": 65,
                "matched_symptoms": ["stomach pain"],
                "urgency": "moderate"
            },
            {
                "disease": "Early Appendicitis",
                "confidence": 35,
                "matched_symptoms": ["stomach pain", "vomiting"],
                "urgency": "high"
            }
        ]
    },
    "breathing_issue": {
        "type": "success",
        "symptoms": ["shortness of breath", "chest tightness"],
        "duration": "2",
        "predictions": [
            {
                "disease": "Bronchial Asthma Exacerbation",
                "confidence": 84,
                "matched_symptoms": ["shortness of breath", "chest tightness"],
                "urgency": "high"
            },
            {
                "disease": "Acute Bronchitis with Airway Spasm",
                "confidence": 66,
                "matched_symptoms": ["shortness of breath"],
                "urgency": "moderate"
            },
            {
                "disease": "Cardiopulmonary Dyspnea",
                "confidence": 40,
                "matched_symptoms": ["chest tightness"],
                "urgency": "emergency"
            }
        ]
    },
    "joint_pain": {
        "type": "success",
        "symptoms": ["joint pain", "morning stiffness"],
        "duration": "14",
        "predictions": [
            {
                "disease": "Osteoarthritis / Early Rheumatoid Arthritis",
                "confidence": 82,
                "matched_symptoms": ["joint pain", "morning stiffness"],
                "urgency": "moderate"
            },
            {
                "disease": "Post-Viral Reactive Arthralgia",
                "confidence": 60,
                "matched_symptoms": ["joint pain"],
                "urgency": "moderate"
            },
            {
                "disease": "Gouty Arthritis / Hyperuricemia",
                "confidence": 45,
                "matched_symptoms": ["joint pain"],
                "urgency": "moderate"
            }
        ]
    }
}


# ===========================================================================
# 5. PUBLIC ACCESS HELPERS (0.0001 SECONDS)
# ===========================================================================
def get_instant_disease(query: str, target_lang: str = "en") -> Optional[Dict[str, Any]]:
    """Returns pre-indexed disease info instantly for fast button clicks."""
    q = (query or "").lower().strip()
    source_dict = INSTANT_DISEASES_HI if target_lang == "hi" else INSTANT_DISEASES

    for key, data in source_dict.items():
        if key in q or q in key:
            return dict(data)
    if "sugar" in q or "madhumeh" in q or "glucose" in q:
        return dict(source_dict.get("diabetes", INSTANT_DISEASES["diabetes"]))
    if "bp" in q or "blood pressure" in q or "raktschap" in q:
        return dict(source_dict.get("hypertension", INSTANT_DISEASES["hypertension"]))
    if "dama" in q or "saans" in q or "wheeze" in q:
        return dict(source_dict.get("asthma", INSTANT_DISEASES["asthma"]))
    if "flu" in q or "sardi" in q or "jukham" in q:
        return dict(source_dict.get("common cold", INSTANT_DISEASES["common cold"]))
    if "corona" in q or "covid" in q:
        return dict(source_dict.get("coronavirus", INSTANT_DISEASES["coronavirus"]))
    if "gathiya" in q or "joint" in q or "jodon" in q:
        return dict(source_dict.get("arthritis", INSTANT_DISEASES["arthritis"]))
    return None


def get_instant_drug(query: str, target_lang: str = "en") -> Optional[Dict[str, Any]]:
    """Returns pre-indexed drug info wrapped in direct response schema in 0.001 seconds."""
    q = (query or "").lower().strip()
    data = None
    for key, d in INSTANT_DRUGS.items():
        if key in q or q in key:
            data = d
            break
    if not data:
        if "crocin" in q or "dolo" in q or "calpol" in q or "tylenol" in q:
            data = INSTANT_DRUGS["paracetamol"]
        elif "brufen" in q or "advil" in q or "combiflam" in q:
            data = INSTANT_DRUGS["ibuprofen"]
        elif "disprin" in q or "ecosprin" in q:
            data = INSTANT_DRUGS["aspirin"]
        elif "glycomet" in q or "glucophage" in q or "sugar" in q:
            data = INSTANT_DRUGS["metformin"]
        elif "mox" in q or "augmentin" in q or "amoxil" in q:
            data = INSTANT_DRUGS["amoxicillin"]
        elif "zyrtec" in q or "cetzine" in q or "alerid" in q:
            data = INSTANT_DRUGS["cetirizine"]

    if not data:
        return None

    ans_text = (
        f"**{data['name'].upper()}**\n\n"
        f"**Drug Class:** {data.get('drug_class', '')}\n"
        f"**Brand Names:** {', '.join(data.get('brand_names', []))}\n\n"
        f"**What it's used for (Indications):**\n{data.get('indications', '')}\n\n"
        f"**Recommended Dosage:**\n{data.get('dosage', '')}\n\n"
        f"**Safety Warnings & Precautions:**\n{data.get('warnings', '')}\n\n"
        f"**Possible Side Effects:**\n{data.get('side_effects', '')}\n\n"
        f"**Pregnancy & Lactation:**\n{data.get('pregnancy_safety', '')}\n\n"
        f"⚠️ For any personal decisions regarding medication, always consult with a doctor or pharmacist."
    )

    return {
        "type": "direct",
        "answer": ans_text,
        "drugs": [
            {
                "name": data["name"],
                "indications": data["indications"],
                "dosage": data["dosage"],
                "warnings": data["warnings"],
                "side_effects": data.get("side_effects", ""),
                "pregnancy_safety": data.get("pregnancy_safety", "")
            }
        ],
        "sources": [{"drug_name": data["name"]}]
    }


def get_instant_sample_report(key: str, target_lang: str = "en") -> Optional[Dict[str, Any]]:
    """Returns pre-indexed clinical report analysis in 0.001 seconds."""
    k = (key or "").lower().strip()
    if "cbc" in k or "blood" in k:
        rep = dict(INSTANT_SAMPLE_REPORTS["cbc"])
    elif "lipid" in k or "diabetes" in k or "sugar" in k or "cholesterol" in k:
        rep = dict(INSTANT_SAMPLE_REPORTS["lipid"])
    elif "renal" in k or "liver" in k or "kft" in k or "lft" in k or "kidney" in k:
        rep = dict(INSTANT_SAMPLE_REPORTS["renal"])
    else:
        return None

    return rep


def get_instant_symptom_prediction(query: str, target_lang: str = "en") -> Optional[Dict[str, Any]]:
    """Returns pre-indexed symptom analysis in 0.001 seconds."""
    q = (query or "").lower().strip()
    if any(w in q for w in ["cough", "khansi", "fever, cough", "fever & cough"]) and any(w in q for w in ["fever", "bukhar", "body"]):
        return dict(INSTANT_SYMPTOM_PREDICTIONS["fever_cough"])
    if any(w in q for w in ["headache", "sirdard", "migraine", "severe headache"]):
        return dict(INSTANT_SYMPTOM_PREDICTIONS["headache"])
    if any(w in q for w in ["stomach", "pet", "vomit", "ulti", "gastro"]):
        return dict(INSTANT_SYMPTOM_PREDICTIONS["stomach_pain"])
    if any(w in q for w in ["breath", "saans", "chest tightness", "shortness"]):
        return dict(INSTANT_SYMPTOM_PREDICTIONS["breathing_issue"])
    if any(w in q for w in ["joint", "jod", "gathiya", "stiffness", "arthritis"]):
        return dict(INSTANT_SYMPTOM_PREDICTIONS["joint_pain"])
    if any(w in q for w in ["fever", "bukhar"]):
        return dict(INSTANT_SYMPTOM_PREDICTIONS["fever_cough"])
    return None
