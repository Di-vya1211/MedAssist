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
    },
    "cancer": {
        "disease_name": "Cancer (Malignant Neoplasms)",
        "description": "A group of diseases characterized by uncontrolled cellular proliferation and invasion into surrounding tissues or distant organs via bloodstream or lymphatic vessels.",
        "symptoms": [
            "Unexplained rapid weight loss (> 5 kg) and persistent profound fatigue",
            "Painless palpable lump, swelling, or thickening in breast, neck, groin, or axilla",
            "Persistent cough, hoarseness of voice, or difficulty swallowing lasting > 3 weeks",
            "Unexplained abnormal bleeding (blood in stool, urine, sputum, or abnormal vaginal bleeding)",
            "Noticeable changes in size, border, shape, or pigmentation of skin moles or non-healing sores"
        ],
        "precautions": [
            "Completely avoid all forms of tobacco (smoking, vaping, and smokeless chewing tobacco)",
            "Limit alcohol intake and protect skin against ultraviolet solar radiation",
            "Maintain an active lifestyle, healthy body mass index, and diet rich in plant antioxidants",
            "Undergo recommended clinical screenings (Mammography, Pap smear, Colonoscopy, PSA)",
            "Receive vaccinations against oncogenic pathogens (Hepatitis B and Human Papillomavirus - HPV)"
        ],
        "diagnostic_tests": [
            "Histopathological Tissue Biopsy (Core needle, incisional, or excisional biopsy)",
            "Whole-Body PET-CT Scan (Positron Emission Tomography)",
            "High-Resolution Contrast-Enhanced MRI and CT Imaging",
            "Serum Tumor Marker Panel (CEA, CA-125, PSA, CA 19-9, AFP)",
            "Complete Blood Count (CBC) and Peripheral Blood Film",
            "Bone Marrow Aspiration and Trephine Biopsy",
            "Immunohistochemistry (IHC) and Molecular Genomic Profiling"
        ],
        "treatment": [
            "Surgical oncological resection or organ-sparing debulking surgery",
            "Systemic Chemotherapy protocols tailored to tumor stage and histology",
            "Precision Radiation Therapy (IMRT, stereotactic radiosurgery)",
            "Targeted Biological Therapy and Immune Checkpoint Inhibitors",
            "Comprehensive supportive palliative oncology and pain management"
        ],
        "risk_factors": [
            "Tobacco and heavy alcohol consumption",
            "Genetic mutations and familial cancer syndromes (BRCA1/2, Lynch syndrome)",
            "Exposure to occupational carcinogens (asbestos, benzene, ionizing radiation)",
            "Chronic viral infections (HPV, Hepatitis B/C, EBV) and chronic inflammation"
        ],
        "when_to_see_doctor": "Consult an oncologist or physician immediately if you discover any new painless lump, persistent unexplained weight loss, difficulty swallowing, or blood in cough or stool.",
        "confidence": "HIGH"
    },
    "tuberculosis": {
        "disease_name": "Tuberculosis (Pulmonary & Extrapulmonary TB)",
        "description": "A serious infectious bacterial disease caused by Mycobacterium tuberculosis that primarily infects the lung parenchyma and spreads through airborne respiratory droplets.",
        "symptoms": [
            "Persistent productive cough lasting three weeks or longer",
            "Coughing up blood or blood-tinged sputum (hemoptysis)",
            "Drenching nocturnal sweats and low-grade evening fever",
            "Unexplained progressive weight loss and profound loss of appetite",
            "Pleuritic chest pain aggravated by coughing or deep breathing and chronic fatigue"
        ],
        "precautions": [
            "Strictly adhere to the complete 6-month DOTS treatment regimen without missing doses",
            "Wear an N95 or surgical mask during the initial infectious phase (first 2-3 weeks)",
            "Ensure cross-ventilation, abundant natural airflow, and direct sunlight in living areas",
            "Practice strict respiratory etiquette (covering coughs with disposable tissues)",
            "Administer BCG vaccination to all newborns at birth"
        ],
        "diagnostic_tests": [
            "Sputum Smear Examination for Acid-Fast Bacilli (AFB)",
            "GeneXpert MTB/RIF Molecular Assay (Rapid detection of TB & Rifampicin resistance)",
            "Chest X-Ray (PA View showing apical infiltrates or cavitary lesions)",
            "Mantoux Tuberculin Skin Test (TST / PPD)",
            "Interferon-Gamma Release Assay (IGRA / QuantiFERON-TB Gold)",
            "Mycobacterial Liquid Culture (MGIT)"
        ],
        "treatment": [
            "Standard First-Line DOTS Regimen (2 months HRZE: Isoniazid, Rifampicin, Pyrazinamide, Ethambutol)",
            "Continuation Phase (4 months HR: Isoniazid and Rifampicin)",
            "Pyridoxine (Vitamin B6 10-25mg) daily to prevent drug-induced peripheral neuropathy",
            "High-protein nutritional supplementation to facilitate lung healing",
            "Second-line antimycobacterial therapy (Bedaquiline, Linezolid) for Drug-Resistant TB (MDR-TB)"
        ],
        "risk_factors": [
            "Close household contact with an untreated active pulmonary TB patient",
            "Immunocompromised states (HIV/AIDS, poorly controlled diabetes, immunosuppressive therapy)",
            "Malnutrition, crowded living conditions, and poorly ventilated environments",
            "Tobacco smoking and chronic kidney failure"
        ],
        "when_to_see_doctor": "Seek urgent medical evaluation at a respiratory center if a cough persists for more than 2 weeks, if coughing up blood, or experiencing severe night sweats with fever.",
        "confidence": "HIGH"
    },
    "malaria": {
        "disease_name": "Malaria (Plasmodium Parasitic Infection)",
        "description": "A life-threatening protozoan infection transmitted through the bite of infected female Anopheles mosquitoes, causing red blood cell lysis, severe fever paroxysms, and systemic organ distress.",
        "symptoms": [
            "Classic fever paroxysms: cold shaking chills (rigors) followed by high fever spikes",
            "Profuse sweating as the fever suddenly breaks",
            "Severe throbbing headache, muscle pain (myalgia), and joint stiffness",
            "Nausea, bilious vomiting, abdominal discomfort, and diarrhea",
            "Pallor due to hemolytic anemia, fatigue, and jaundice"
        ],
        "precautions": [
            "Sleep under long-lasting insecticide-treated bed nets (ITNs)",
            "Apply DEET-based mosquito repellent creams on exposed skin during dusk and dawn",
            "Eliminate all standing water sources in coolers, flowerpots, and drains around residences",
            "Take chemoprophylaxis when traveling to high-risk endemic areas"
        ],
        "diagnostic_tests": [
            "Rapid Diagnostic Test for Malaria (RDT - Pf/Pv Antigen)",
            "Peripheral Blood Smear Examination (Thick and Thin Giemsa Stain)",
            "Complete Blood Count (CBC with Platelet Count and Hematocrit)",
            "Liver Function Tests (Serum Bilirubin and Transaminases)",
            "Quantitative Buffy Coat (QBC) Fluorescent Test"
        ],
        "treatment": [
            "Artemisinin-based Combination Therapy (ACT: Artemether-Lumefantrine or Artesunate-SP)",
            "Primaquine for radical cure of dormant liver hypnozoites (in P. vivax & P. ovale, post-G6PD check)",
            "Intravenous Artesunate for severe Falciparum malaria with complications",
            "Fluid rehydration and antipyretics (Paracetamol) for high temperatures"
        ],
        "risk_factors": [
            "Residence or travel in tropical and subtropical endemic zones",
            "Young children, pregnant women, and immunocompromised patients",
            "Lack of protective netting or vector control measures"
        ],
        "when_to_see_doctor": "Seek immediate hospital emergency admission if experiencing high cyclical fever with chills, altered consciousness, convulsions, extreme vomiting, or yellowing of eyes (cerebral malaria).",
        "confidence": "HIGH"
    },
    "dengue": {
        "disease_name": "Dengue Fever (Breakbone Viral Fever)",
        "description": "An acute mosquito-borne viral infection caused by the Dengue virus (DENV-1 to DENV-4) transmitted by day-biting Aedes aegypti mosquitoes, carrying a risk of thrombocytopenia and plasma leakage.",
        "symptoms": [
            "Sudden high fever (up to 104°F / 40°C) lasting 2 to 7 days",
            "Severe retro-orbital (behind the eye) headache",
            "Intense musculoskeletal pain ('breakbone fever') and backache",
            "Maculopapular measles-like skin rash appearing 3-5 days after fever onset",
            "Mild mucosal bleeding (epistaxis, gum bleeding, petechiae, easy bruising)",
            "Persistent nausea, vomiting, and extreme weakness"
        ],
        "precautions": [
            "Protect against day-biting mosquitoes using repellent and long-sleeved clothing",
            "Empty and scrub clean all domestic water storage containers weekly",
            "Strictly avoid Aspirin, Ibuprofen, and NSAIDs as they exacerbate bleeding tendencies",
            "Maintain aggressive oral fluid intake (ORS, coconut water, fresh lime, clear broths)"
        ],
        "diagnostic_tests": [
            "Dengue NS1 Antigen ELISA (positive in days 1-5 of fever)",
            "Dengue IgM and IgG Antibody ELISA (positive from day 5 onwards)",
            "Complete Blood Count (Daily Platelet Count and Hematocrit monitoring)",
            "Liver Function Tests (AST / ALT elevation)",
            "Serum Electrolyte Panel"
        ],
        "treatment": [
            "Supportive rehydration therapy to prevent dehydration and hemoconcentration",
            "Paracetamol (500-650mg) strictly for fever and pain relief (Avoid NSAIDs/Aspirin)",
            "Close daily monitoring of platelet counts and hematocrit percentage",
            "Immediate hospital IV crystalloid resuscitation if plasma leakage or shock occurs"
        ],
        "risk_factors": [
            "Urban and semi-urban environments with stagnant rainwater",
            "Secondary infection with a heterologous dengue serotype (increases risk of severe dengue)",
            "Infants, elderly, and individuals with underlying chronic disorders"
        ],
        "when_to_see_doctor": "CRITICAL EMERGENCY: Rush to the hospital if experiencing persistent abdominal pain, frequent vomiting, bleeding from gums/nose, extreme lethargy, or rapid drop in platelets.",
        "confidence": "HIGH"
    },
    "typhoid": {
        "disease_name": "Typhoid Fever (Enteric Fever)",
        "description": "A serious systemic bacterial infection caused by Salmonella enterica serovar Typhi, transmitted through the feco-oral route via contaminated food and drinking water.",
        "symptoms": [
            "Sustained high fever that rises in a characteristic stepwise ladder pattern (up to 104°F)",
            "Severe generalized weakness, malaise, and frontotemporal headache",
            "Abdominal tenderness, bloating, and stomach pain",
            "Constipation in early illness followed by watery 'pea soup' diarrhea",
            "Rose spots (faint salmon-colored rash on the trunk and abdomen)",
            "Loss of appetite (anorexia) and coated tongue"
        ],
        "precautions": [
            "Drink only boiled, filtered, or commercially sealed bottled water",
            "Eat freshly cooked foods served piping hot; avoid raw street foods and unpeeled fruits",
            "Wash hands thoroughly with soap and water before meals and after restroom use",
            "Avoid untreated ice cubes and unpasteurized dairy products",
            "Obtain injectable or oral Typhoid conjugate vaccination before travel to endemic regions"
        ],
        "diagnostic_tests": [
            "Blood Culture for Salmonella Typhi (Gold Standard in 1st week)",
            "Widal Agglutination Test (Significant O and H titers >= 1:160 in 2nd week)",
            "Typhidot Rapid IgM / IgG Serological Test",
            "Complete Blood Count (CBC showing relative leukopenia and eosinopenia)",
            "Stool and Urine Cultures (in 3rd week of illness)"
        ],
        "treatment": [
            "Appropriate antibiotic therapy (Ceftriaxone IV, Azithromycin oral, or Ciprofloxacin)",
            "Adequate fluid and electrolyte replenishment with oral rehydration solutions (ORS)",
            "Soft, easily digestible, nutrient-dense bland diet",
            "Antipyretics (Paracetamol) for fever control"
        ],
        "risk_factors": [
            "Consuming contaminated water supplies or food prepared in unhygienic environments",
            "Close household contact with chronic Salmonella carriers",
            "Inadequate public municipal water sanitation and sewerage systems"
        ],
        "when_to_see_doctor": "Seek emergency medical care if experiencing severe sharp abdominal pain, intestinal bleeding (dark stools), persistent vomiting, or delirium and high fever unresponsive to medications.",
        "confidence": "HIGH"
    },
    "migraine": {
        "disease_name": "Migraine (Neurological Headache Disorder)",
        "description": "A chronic neurovascular disorder characterized by recurrent attacks of severe, unilateral throbbing headaches often accompanied by autonomic, sensory, and gastrointestinal symptoms.",
        "symptoms": [
            "Moderate to severe throbbing, pulsating headache typically on one side of head",
            "Sensory visual aura (scintillating scotomas, zigzag flashing lights, temporary blind spots)",
            "Extreme sensitivity to light (photophobia) and sound (phonophobia)",
            "Nausea, vomiting, and loss of appetite",
            "Lightheadedness, cognitive fog, and neck stiffness preceding or during attacks"
        ],
        "precautions": [
            "Maintain a consistent sleep-wake schedule and avoid sleep deprivation",
            "Stay well-hydrated throughout the day and never skip meals",
            "Identify and avoid individual triggers (aged cheeses, MSG, chocolate, red wine, bright glare)",
            "Practice stress-reduction techniques such as progressive muscle relaxation and meditation"
        ],
        "diagnostic_tests": [
            "Comprehensive Neurological Clinical Examination",
            "Magnetic Resonance Imaging (Brain MRI) to rule out secondary structural causes",
            "Computed Tomography (Head CT) if sudden acute onset or red flags present",
            "Complete Blood Count and Metabolic Profile",
            "Fundoscopy (to rule out papilledema and increased intracranial pressure)"
        ],
        "treatment": [
            "Acute abortive therapy: Triptans (Sumatriptan, Rizatriptan) taken at symptom onset",
            "NSAIDs (Naproxen, Ibuprofen) or Paracetamol with antiemetics (Domperidone)",
            "Preventive pharmacotherapy (Beta-blockers, Topiramate, Amitriptyline, CGRP inhibitors)",
            "Resting in a quiet, dark, well-ventilated room with cool compresses applied to forehead"
        ],
        "risk_factors": [
            "Strong family history and genetic predisposition",
            "Female sex (3 times higher prevalence due to estrogen fluctuations)",
            "High chronic stress, irregular sleep patterns, and skipping meals"
        ],
        "when_to_see_doctor": "Seek immediate emergency attention if experiencing a sudden explosive 'thunderclap' headache, headache accompanied by high fever and stiff neck, focal weakness, or speech loss.",
        "confidence": "HIGH"
    },
    "jaundice": {
        "disease_name": "Jaundice / Icterus (Hyperbilirubinemia)",
        "description": "A clinical manifestation of elevated serum bilirubin levels (> 2.5-3.0 mg/dL) resulting in yellowish pigmentation of the skin, sclera, and mucous membranes due to hepatic, biliary, or hemolytic pathology.",
        "symptoms": [
            "Yellowish discoloration of the whites of the eyes (sclera) and skin",
            "Dark, tea-colored or brownish urine",
            "Pale, clay-colored stools (characteristic of obstructive jaundice)",
            "Generalized skin itching (pruritus) due to bile salt deposition",
            "Fatigue, weakness, nausea, anorexia, and right upper abdominal discomfort"
        ],
        "precautions": [
            "Strictly consume only boiled or purified drinking water to prevent Viral Hepatitis A and E",
            "Completely abstain from alcohol consumption to protect compromised hepatocytes",
            "Consume a clean, easily digestible, low-fat carbohydrate-rich diet",
            "Avoid all unnecessary or unprescribed medications that have potential hepatotoxicity"
        ],
        "diagnostic_tests": [
            "Total, Direct, and Indirect Serum Bilirubin Test",
            "Liver Function Tests (SGPT/ALT, SGOT/AST, Alkaline Phosphatase, GGT)",
            "Viral Hepatitis Serology Panel (Anti-HAV IgM, HBsAg, Anti-HCV, Anti-HEV IgM)",
            "Abdominal Ultrasonography (USG of Liver, Gallbladder, and Biliary Duct Tree)",
            "Complete Blood Count and Peripheral Smear (to exclude hemolytic anemia)",
            "Prothrombin Time (PT/INR) to assess liver synthetic function"
        ],
        "treatment": [
            "Targeted treatment of underlying etiology (antivirals for hepatitis, biliary stenting for gallstones)",
            "Adequate caloric hydration with easily metabolizable carbohydrates",
            "Discontinuation of all hepatotoxic medications and herbal preparations",
            "Phototherapy or exchange transfusion in neonatal hyperbilirubinemia"
        ],
        "risk_factors": [
            "Ingestion of contaminated food or water in areas with poor sanitation",
            "Heavy or chronic alcohol consumption",
            "Gallstones obstructing the common bile duct",
            "Use of hepatotoxic medications (paracetamol overdose, antitubercular drugs)"
        ],
        "when_to_see_doctor": "Consult a physician immediately if jaundice is accompanied by high fever with shaking chills, severe abdominal pain, vomiting blood, extreme drowsiness, or mental confusion.",
        "confidence": "HIGH"
    },
    "anemia": {
        "disease_name": "Anemia (Hemoglobin Deficiency)",
        "description": "A condition in which the concentration of hemoglobin and circulating red blood cells falls below physiological thresholds, diminishing oxygen-carrying capacity to vital organs.",
        "symptoms": [
            "Persistent fatigue, weakness, and decreased exercise tolerance",
            "Marked pallor of the conjunctiva, oral mucosa, nail beds, and palms",
            "Exertional shortness of breath (dyspnea) and dizziness or lightheadedness",
            "Rapid or fluttering heartbeats (palpitations) and cold hands and feet",
            "Brittle spoon-shaped nails (koilonychia) and unusual cravings for ice or dirt (pica)"
        ],
        "precautions": [
            "Consume iron-rich foods (dark green leafy vegetables, lentils, beans, jaggery, lean poultry)",
            "Consume vitamin C-rich foods (citrus fruits, tomatoes) alongside iron to boost absorption",
            "Avoid tea, coffee, and dairy with meals as tannins and calcium inhibit iron absorption",
            "Routine prenatal iron and folic acid supplementation during pregnancy and lactation"
        ],
        "diagnostic_tests": [
            "Complete Blood Count (CBC with Hemoglobin, Hematocrit, MCV, MCH, MCHC)",
            "Peripheral Blood Smear Examination (Microcytic, hypochromic RBC evaluation)",
            "Serum Ferritin (Gold standard for iron storage measurement)",
            "Total Iron-Binding Capacity (TIBC) and Serum Iron levels",
            "Serum Vitamin B12 and Folate levels",
            "Stool Occult Blood Test (to detect occult gastrointestinal bleeding)"
        ],
        "treatment": [
            "Oral Iron Supplementation (Ferrous sulfate, ferrous fumarate, or iron ascorbate)",
            "Intravenous iron sucrose/carboxymaltose for severe deficiency or malabsorption",
            "Vitamin B12 injections or high-dose oral folate for megaloblastic anemia",
            "Packed red blood cell transfusion in acute severe, symptomatic anemia (Hb < 7 g/dL)"
        ],
        "risk_factors": [
            "Nutritional deficiencies and poor dietary iron intake",
            "Heavy menstrual blood loss (menorrhagia) and frequent pregnancies",
            "Gastrointestinal blood loss (peptic ulcers, hemorrhoids, helminthic infections)",
            "Chronic diseases (chronic kidney disease, rheumatoid arthritis, malabsorption)"
        ],
        "when_to_see_doctor": "Seek emergency medical evaluation if experiencing chest pain, rapid heart rate at rest, severe shortness of breath, sudden fainting, or passing black tarry stools.",
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
    },
    "cancer": {
        "disease_name": "कैंसर / कर्क रोग (Malignant Cancer)",
        "description": "यह असामान्य और अनियंत्रित कोशिकाओं की अनियंत्रित वृद्धि की बीमारी है जो आस-पास के अंगों और ऊतकों पर आक्रमण करती है और रक्त या लसीका तंत्र के जरिए फैल सकती है।",
        "symptoms": [
            "अकारण तेजी से वजन कम होना (5 किलो से अधिक) और लगातार गहरी थकान",
            "स्तन, गर्दन, बगल या जांघ में बिना दर्द वाली नई गांठ या सूजन महसूस होना",
            "तीन सप्ताह से अधिक रहने वाली पुरानी खांसी, आवाज में भारीपन या निगलने में कठिनाई",
            "असामान्य रक्तस्राव (खांसी, पेशाब, मल में खून या अकारण रक्तस्त्राव)",
            "त्वचा के तिल या मस्से के रंग, आकार या सीमाओं में स्पष्ट बदलाव अथवा न भरने वाला घाव"
        ],
        "precautions": [
            "तंबाकू, सिगरेट, बीड़ी और गुटखे का तुरंत और स्थायी त्याग करें",
            "शराब के अत्यधिक सेवन और तेज धूप (पराबैंगनी किरणों) से त्वचा का बचाव करें",
            "नियमित शारीरिक व्यायाम करें और फल, हरी सब्जियों तथा एंटीऑक्सीडेंट्स से भरपूर आहार लें",
            "आयु के अनुसार नियमित कैंसर जांच (मैमोग्राफी, पैप स्मीयर, कोलोनोस्कोपी, PSA) कराएं",
            "कैंसर पैदा करने वाले संक्रमणों से बचाव के लिए हेपेटाइटिस बी और एचपीवी (HPV) का टीका लगवाएं"
        ],
        "diagnostic_tests": [
            "बायोप्सी जांच (Histopathological Tissue Biopsy - निश्चित जांच)",
            "पीईटी-सीटी स्कैन (Whole-Body PET-CT Scan)",
            "कंट्रास्ट एमआरआई और सीटी स्कैन (High-Resolution MRI & CT)",
            "ट्यूमर मार्कर ब्लड टेस्ट (CEA, CA-125, PSA, CA 19-9, AFP)",
            "कम्प्लीट ब्लड काउंट (CBC) और बोन मैरो एस्पिरेशन",
            "इम्यूनोहिस्टोकेमिस्ट्री (IHC) और मॉलिक्यूलर जेनेटिक प्रोफाइलिंग"
        ],
        "treatment": [
            "सर्जिकल ऑन्कोलॉजी (शल्य चिकित्सा द्वारा ट्यूमर को निकालना)",
            "कीमोथेरेपी (दवाओं द्वारा कैंसर कोशिकाओं का उन्मूलन)",
            "टारगेटेड रेडिएशन थेरेपी (Radiation Therapy - सघन विकिरण चिकित्सा)",
            "इम्यूनोथेरेपी और लक्षित जैविक दवाएं (Targeted Molecular Therapy)",
            "दर्द निवारण और व्यापक पैलिएटिव सहायक चिकित्सा"
        ],
        "risk_factors": [
            "तंबाकू, गुटखा और भारी शराब का सेवन",
            "पारिवारिक आनुवंशिक इतिहास (BRCA1/2, लिंच सिंड्रोम)",
            "औद्योगिक कार्सिनोजेन्स (एस्बेस्टस, रेडिएशन) के संपर्क में आना",
            "पुराने वायरल संक्रमण (HPV, हेपेटाइटिस बी/सी) और मोटापा"
        ],
        "when_to_see_doctor": "यदि शरीर में बिना दर्द वाली नई गांठ दिखे, अचानक वजन घटे, निगलने में कष्ट हो या खांसी/मल में खून आए तो तुरंत ऑन्कोलॉजिस्ट (कैंसर विशेषज्ञ) से संपर्क करें।",
        "confidence": "HIGH"
    },
    "tuberculosis": {
        "disease_name": "टीबी / क्षय रोग (Tuberculosis - Pulmonary TB)",
        "description": "माइकोबैक्टीरियम ट्यूबरकुलोसिस बैक्टीरिया से होने वाला एक गंभीर संक्रामक रोग जो मुख्य रूप से फेफड़ों पर हमला करता है और खांसने-छींकने से हवा में फैलता है।",
        "symptoms": [
            "तीन सप्ताह या उससे अधिक समय तक लगातार रहने वाली बलगम वाली खांसी",
            "खांसी में बलगम के साथ खून आना (Hemoptysis)",
            "रात में अत्यधिक पसीना आना और ठंड लगना",
            "शाम के समय हल्का बुखार और लगातार अत्यधिक कमजोरी",
            "अचानक भूख न लगना और तेजी से वजन कम होना"
        ],
        "precautions": [
            "डॉट्स (DOTS) का पूरा 6 महीने का कोर्स बिना एक भी खुराक छोड़े सख्ती से लें",
            "शुरुआती 2-3 हफ्तों में N95 या सर्जिकल मास्क अवश्य लगाएं ताकि परिवार में संक्रमण न फैले",
            "घर में धूप और ताजी हवा का पूरा प्रबंध रखें, बंद कमरे में न रहें",
            "खांसते-छींकते समय डिस्पोजेबल रुमाल या कोहनी से मुंह ढकें",
            "नवजात शिशुओं को जन्म के तुरंत बाद बीसीजी (BCG) का टीका लगवाएं"
        ],
        "diagnostic_tests": [
            "बलगम की जांच (Sputum Smear Examination for AFB)",
            "जीन एक्सपर्ट सीबीनाट टेस्ट (GeneXpert MTB/RIF Assay - टीबी और दवा प्रतिरोध जांच)",
            "चेस्ट एक्स-रे (Chest X-Ray PA View)",
            "मांटू टेस्ट (Mantoux Tuberculin Skin Test)",
            "आईजीआरए ब्लड टेस्ट (QuantiFERON-TB Gold)",
            "बलगम कल्चर टेस्ट (MGIT Liquid Culture)"
        ],
        "treatment": [
            "मानक डॉट्स उपचार: 2 महीने HRZE (Isoniazid, Rifampicin, Pyrazinamide, Ethambutol)",
            "कंटिन्यूएशन फेज़: 4 महीने HR (Isoniazid और Rifampicin)",
            "नसों की सुरक्षा के लिए विटामिन B6 (Pyridoxine 10-25mg) की दैनिक गोली",
            "फेफड़ों की रिकवरी के लिए उच्च प्रोटीन युक्त पोषण (दालें, अंडे, दूध, सोयाबीन)",
            "दवा प्रतिरोधी टीबी (MDR-TB) के लिए विशेष दवाएं (Bedaquiline, Linezolid)"
        ],
        "risk_factors": [
            "सक्रिय टीबी मरीज के साथ लंबे समय तक रहना",
            "कमजोर प्रतिरक्षा प्रणाली (एचआईवी, अनियंत्रित मधुमेह, कुपोषण)",
            "भीड़भाड़ और हवा-रहित तंग कमरे में रहना",
            "धूम्रपान और फेफड़ों की पुरानी बीमारियां"
        ],
        "when_to_see_doctor": "यदि खांसी 2 सप्ताह से ज्यादा रहे, बलगम में खून आए, या रात में तेज पसीना और बुखार आए तो बिना देर किए टीबी क्लिनिक या छाती रोग विशेषज्ञ से जांच कराएं।",
        "confidence": "HIGH"
    },
    "malaria": {
        "disease_name": "मलेरिया (Malaria - प्लास्मोडियम संक्रमण)",
        "description": "मादा एनोफिलीज मच्छर के काटने से फैलने वाला एक गंभीर प्रोटोजोआ परजीवी संक्रमण जो लाल रक्त कोशिकाओं को नष्ट करता है और चक्रीय तेज बुखार पैदा करता है।",
        "symptoms": [
            "कंपकंपी और दांत किटकिटाने के साथ तेज बुखार के चक्रीय दौरे",
            "बुखार उतरते समय अत्यधिक पसीने से तर-बतर होना",
            "सिर में तेज धड़कता हुआ दर्द, मांसपेशियों और जोड़ों में अकड़न",
            "जी मिचलाना, उल्टी आना और पेट में दर्द",
            "खून की कमी के कारण पीलापन और अत्यधिक कमजोरी"
        ],
        "precautions": [
            "मच्छरदानी (ITN) लगाकर ही सोएं और खिड़कियों पर जाली लगाएं",
            "शाम और सुबह के समय खुले अंगों पर मॉस्किटो रिपेलेंट क्रीम लगाएं",
            "कूलर, गमलों, टायरों और नालियों में कहीं भी पानी जमा न होने दें",
            "मलेरिया प्रभावित क्षेत्रों में जाने से पहले प्रोफिलैक्सिस दवा लें"
        ],
        "diagnostic_tests": [
            "मलेरिया रैपिड एंटीजन टेस्ट (Malaria RDT - Pf/Pv Antigen)",
            "पेरिफेरल ब्लड स्मीयर जांच (रक्त की मोटी व पतली स्लाइड जांच)",
            "कम्प्लीट ब्लड काउंट (CBC - प्लेटलेट्स और हीमोग्लोबिन जांच)",
            "लिवर फंक्शन टेस्ट (सीरम बिलीरुबिन)",
            "क्यूबीसी फ्लोरोसेंट टेस्ट (QBC Malaria)"
        ],
        "treatment": [
            "आर्टेमिसिनिन आधारित कॉम्बिनेशन थेरेपी (ACT: Artemether-Lumefantrine)",
            "लिवर में छिपे परजीवियों को खत्म करने के लिए प्राइमाक्विन (Primaquine गोली)",
            "गंभीर फाल्सीपेरम मलेरिया में इंजेक्शन आर्टेसुनेट (IV Artesunate)",
            "बुखार के लिए पेरासिटामोल और ओआरएस तरल पदार्थ"
        ],
        "risk_factors": [
            "उष्णकटिबंधीय क्षेत्रों में रहना या यात्रा करना",
            "छोटे बच्चे, गर्भवती महिलाएं और कमजोर इम्युनिटी वाले लोग",
            "मच्छर नियंत्रण की कमी"
        ],
        "when_to_see_doctor": "यदि बुखार के साथ अत्यधिक कंपकंपी हो, बेहोशी, लगातार उल्टी, या आंखों में पीलापन दिखे तो सेरेब्रल मलेरिया के खतरे से बचने के लिए तुरंत अस्पताल जाएं।",
        "confidence": "HIGH"
    },
    "dengue": {
        "disease_name": "डेंगू बुखार (Dengue - हड्डी तोड़ बुखार)",
        "description": "दिन में काटने वाले एडीज एजिप्टी मच्छरों द्वारा फैलने वाला एक तीव्र वायरल संक्रमण जिससे प्लेटलेट्स तेजी से गिर सकते हैं और प्लाज्मा लीकेज का खतरा रहता है।",
        "symptoms": [
            "अचानक 104°F तक तेज बुखार जो 2 से 7 दिन रहता है",
            "आंखों के ठीक पीछे असहनीय सिरदर्द (Retro-orbital pain)",
            "हड्डियों, जोड़ों और मांसपेशियों में तेज दर्द ('हड्डी तोड़ दर्द')",
            "बुखार आने के 3-5 दिन बाद शरीर पर खसरे जैसे लाल चकत्ते",
            "मसूड़ों या नाक से हल्का खून आना या त्वचा पर नीले निशान",
            "लगातार मतली, उल्टी और अत्यधिक बेचैनी"
        ],
        "precautions": [
            "पूरी आस्तीन के कपड़े पहनें और दिन के समय मच्छर भगाने वाली क्रीम लगाएं",
            "घर और आसपास पानी की टंकियों व बर्तनों को ढककर रखें और हफ्ते में एक बार सुखाएं",
            "एस्पिरिन या ब्रूफेन (Ibuprofen) कभी न लें क्योंकि इनसे ब्लीडिंग का खतरा बढ़ जाता है",
            "प्रचुर मात्रा में ओआरएस, नारियल पानी, नींबू पानी और सूप पिएं"
        ],
        "diagnostic_tests": [
            "डेंगू NS1 एंटीजन टेस्ट (बुखार के पहले 5 दिनों में पॉजिटिव)",
            "डेंगू IgM और IgG एंटीबॉडी टेस्ट (5वें दिन के बाद)",
            "कम्प्लीट ब्लड काउंट (CBC - दैनिक प्लेटलेट काउंट और हेमेटोक्रिट निगरानी)",
            "लिवर फंक्शन टेस्ट (SGPT/SGOT)",
            "सीरम इलेक्ट्रोलाइट्स"
        ],
        "treatment": [
            "पर्याप्त जलयोजन (Oral Rehydration Therapy) जिससे खून गाढ़ा न हो",
            "बुखार और दर्द के लिए केवल और केवल पेरासिटामोल (Paracetamol) लें",
            "प्लेटलेट्स और हेमेटोक्रिट की दैनिक जांच कराते रहें",
            "प्लेटलेट्स बहुत कम होने या प्लाज्मा लीकेज पर अस्पताल में आईवी ड्रिप थेरेपी"
        ],
        "risk_factors": [
            "बरसात के मौसम में जमे हुए साफ पानी में मच्छरों का पनपना",
            "दूसरी बार किसी दूसरे सीरोटाइप से डेंगू का संक्रमण होना",
            "शिशु, वृद्ध और पहले से बीमार व्यक्ति"
        ],
        "when_to_see_doctor": "आपातकालीन चेतावनी: पेट में तेज दर्द, बार-बार उल्टी, नाक/मसूड़ों से खून आना, अत्यधिक सुस्ती, या प्लेटलेट्स 50,000 से नीचे जाने पर बिना एक पल गंवाए अस्पताल में भर्ती हों।",
        "confidence": "HIGH"
    },
    "typhoid": {
        "disease_name": "टाइफाइड / मियादी बुखार (Enteric Fever)",
        "description": "साल्मोनेला टाइफी बैक्टीरिया से दूषित भोजन और पानी के माध्यम से फैलने वाला एक गंभीर आंतों और रक्त का प्रणालीगत संक्रमण।",
        "symptoms": [
            "लगातार तेज बुखार जो सीढ़ी की तरह रोज बढ़ता जाता है (104°F तक)",
            "सिरदर्द, अत्यधिक सुस्ती और बदन में भारी कमजोरी",
            "पेट में दर्द, भारीपन और आंतों में सूजन",
            "शुरुआत में कब्ज और बाद में पतले दस्त (Pea soup diarrhea)",
            "सीने और पेट पर हल्के गुलाबी दाने (Rose spots)",
            "जीभ पर सफेद मोटी परत जमना और भूख न लगना"
        ],
        "precautions": [
            "हमेशा उबला हुआ, फिल्टर किया हुआ या सीलबंद पानी ही पिएं",
            "खाना हमेशा ताजा और गर्म खाएं; खुले कटे फल और कच्चा भोजन न लें",
            "खाना खाने से पहले और शौच के बाद साबुन से अच्छी तरह हाथ धोएं",
            "बाजार की बर्फ और खुले डेयरी उत्पादों से परहेज करें",
            "टाइफाइड का टीका (Typhoid Conjugate Vaccine) लगवाएं"
        ],
        "diagnostic_tests": [
            "ब्लड कल्चर टेस्ट (Blood Culture for Salmonella - पहले हफ्ते की सबसे सटीक जांच)",
            "विडाल टेस्ट (Widal Agglutination Test - दूसरे हफ्ते में टाइटर 1:160 या अधिक)",
            "टायफीडॉट टेस्ट (Typhidot Rapid IgM/IgG Test)",
            "कम्प्लीट ब्लड काउंट (CBC - ल्यूकोपेनिया और इओसिनोपेनिया)",
            "स्टूल कल्चर टेस्ट"
        ],
        "treatment": [
            "उचित एंटीबायोटिक दवाएं (Ceftriaxone IV, Azithromycin या Ciprofloxacin)",
            "ओआरएस और नारियल पानी से इलेक्ट्रोलाइट्स का संतुलन",
            "सुपाच्य, हल्का और पौष्टिक आहार (खिचड़ी, दलिया, उबले आलू, सूप)",
            "बुखार नियंत्रण के लिए पेरासिटामोल"
        ],
        "risk_factors": [
            "असुरक्षित पेयजल और अस्वच्छ स्ट्रीट फूड का सेवन",
            "टाइफाइड के पुराने कैरियर मरीज के संपर्क में आना",
            "सीवरेज और पेयजल पाइपलाइनों का मिश्रण"
        ],
        "when_to_see_doctor": "यदि पेट में असहनीय दर्द हो, मल में खून आए, लगातार तेज बुखार दवाओं से भी न उतरे या बेहोशी छाने लगे तो आंतों में छेद (Perforation) से बचाव के लिए तुरंत इमरजेंसी जाएं।",
        "confidence": "HIGH"
    },
    "migraine": {
        "disease_name": "माइग्रेन / आधासीसी का दर्द (Migraine Headache)",
        "description": "यह एक न्यूरोलॉजिकल विकार है जिसमें सिर के एक हिस्से में तीव्र धड़कता हुआ दर्द होता है, साथ ही प्रकाश, ध्वनि और गंध के प्रति अत्यधिक संवेदनशीलता रहती है।",
        "symptoms": [
            "सिर के एक तरफ (कभी-कभी दोनों तरफ) धड़कने वाला तीव्र दर्द",
            "आंखों के आगे चमकती रोशनी, आड़ी-तिरछी रेखाएं या अंधेरा दिखना (Aura)",
            "रोशनी (Photophobia) और तेज आवाज (Phonophobia) से तेज चिड़चिड़ाहट",
            "जी मिचलाना, उल्टी आना और भूख खत्म होना",
            "गर्दन में अकड़न, चक्कर आना और सिर में भारीपन"
        ],
        "precautions": [
            "सोने और जागने का नियमित समय निर्धारित करें और अधूरी नींद से बचें",
            "दिनभर में पर्याप्त पानी पिएं और भोजन का समय कभी न छोड़ें",
            "व्यक्तिगत ट्रिगर्स (तेज धूप, तेज परफ्यूम, चीज, चॉकलेट, कैफीन) की पहचान कर उनसे बचें",
            "तनाव प्रबंधन के लिए गहरी सांस लेने का अभ्यास और योग करें"
        ],
        "diagnostic_tests": [
            "विस्तृत न्यूरोलॉजिकल शारीरिक परीक्षण",
            "ब्रेन एमआरआई (Brain MRI Scan - अन्य कारणों को खारिज करने के लिए)",
            "सीटी स्कैन (Head CT Scan) यदि अचानक बहुत तेज दर्द हुआ हो",
            "आंखों की रेटिना जांच (Fundoscopy)"
        ],
        "treatment": [
            "दर्द शुरू होते ही ट्रिप्टान दवाएं (Sumatriptan, Rizatriptan)",
            "एनएसएआईडी (NSAIDs) या पेरासिटामोल उल्टी-रोधी दवा के साथ",
            "बचाव के लिए डॉक्टर द्वारा निर्धारित बीटा-ब्लॉकर्स या न्यूरो दवाएं",
            "शांत और अंधेरे कमरे में माथे पर ठंडी पट्टी रखकर विश्राम करना"
        ],
        "risk_factors": [
            "पारिवारिक आनुवंशिक इतिहास",
            "हार्मोनल बदलाव (महिलाओं में 3 गुना अधिक पाया जाता है)",
            "अत्यधिक मानसिक तनाव और खान-पान में अनियमितता"
        ],
        "when_to_see_doctor": "यदि जीवन का सबसे भयानक और अचानक दर्द ('थंडरक्लैप' सिरदर्द) हो, गर्दन अकड़ जाए, तेज बुखार हो या शरीर का कोई अंग सुन्न या कमजोर हो तो तुरंत अस्पताल जाएं।",
        "confidence": "HIGH"
    },
    "jaundice": {
        "disease_name": "पीलिया (Jaundice - बिलीरुबिन की अधिकता)",
        "description": "रक्त में बिलीरुबिन का स्तर अत्यधिक बढ़ जाने से त्वचा, आंखों और श्लेष्मा झिल्लियों का पीला पड़ जाना, जो लिवर, पित्त की थैली या रक्त विकार का संकेत देता है।",
        "symptoms": [
            "आंखों की पुतलियों के सफेद हिस्से और त्वचा का पीला दिखना",
            "गहरा पीला या चाय जैसे रंग का पेशाब आना",
            "हल्के या मिट्टी के रंग का मल आना (पित्त नली में रुकावट का संकेत)",
            "पूरे शरीर में लगातार खुजली होना",
            "अत्यधिक कमजोरी, भूख बिल्कुल न लगना और पेट के ऊपरी दाहिने हिस्से में भारीपन"
        ],
        "precautions": [
            "हेपेटाइटिस ए और ई से बचाव के लिए केवल उबला या शुद्ध पानी ही पिएं",
            "शराब और नशे का पूर्ण त्याग करें ताकि लिवर कोशिकाओं को नुकसान न पहुंचे",
            "पूरी तरह सुपाच्य, कम तेल-मसाले वाला और कार्बोहाइड्रेट युक्त ताजा भोजन लें",
            "बिना डॉक्टर के पर्चे वाली दर्द निवारक या अनजान देसी दवाएं बिल्कुल न लें"
        ],
        "diagnostic_tests": [
            "सीरम बिलीरुबिन टेस्ट (Total, Direct & Indirect Bilirubin)",
            "लिवर फंक्शन टेस्ट (SGPT/ALT, SGOT/AST, Alkaline Phosphatase, GGT)",
            "वायरल हेपेटाइटिस पैनल (HBsAg, Anti-HCV, Anti-HAV IgM, Anti-HEV)",
            "पेट का अल्ट्रासाउंड (USG Abdomen - लिवर और पित्त की थैली जांच)",
            "कम्प्लीट ब्लड काउंट और प्रोथ्रोम्बिन टाइम (PT/INR)"
        ],
        "treatment": [
            "मूल कारण का उपचार (हेपेटाइटिस की दवा या पित्त की पथरी निकालना)",
            "ग्लूकोज और तरल पदार्थों से भरपूर पौष्टिक आहार (गन्ने का रस, नारियल पानी)",
            "लिवर को नुकसान पहुंचाने वाली दवाओं का तुरंत बंद किया जाना",
            "नवजात शिशुओं में फोटोथेरेपी उपचार"
        ],
        "risk_factors": [
            "दूषित पानी और अस्वच्छ भोजन का सेवन",
            "अत्यधिक शराब का सेवन",
            "पित्त की पथरी या लिवर की पुरानी बीमारियां",
            "हेपेटोटॉक्सिक दवाओं का अनुचित उपयोग"
        ],
        "when_to_see_doctor": "यदि पीलिया के साथ तेज बुखार-कंपकंपी हो, पेट में भयंकर दर्द हो, खून की उल्टी हो या मरीज बहकी-बहकी बातें करने लगे (लिवर एन्सेफैलोपैथी), तो तुरंत इमरजेंसी अस्पताल ले जाएं।",
        "confidence": "HIGH"
    },
    "anemia": {
        "disease_name": "एनीमिया (Anemia - खून की कमी)",
        "description": "रक्त में लाल रक्त कोशिकाओं या हीमोग्लोबिन की मात्रा सामान्य से कम हो जाना जिससे शरीर के अंगों और ऊतकों को पर्याप्त ऑक्सीजन नहीं मिल पाती।",
        "symptoms": [
            "लगातार कमजोरी, सुस्ती और थोड़ा काम करते ही अत्यधिक थकान",
            "आंखों के अंदर, चेहरे, होठों और हथेलियों में स्पष्ट पीलापन या सफेदी",
            "थोड़ा सा चलने या सीढ़ियां चढ़ने पर सांस फूलना और चक्कर आना",
            "दिल की धड़कन तेज होना या घबराहट महसूस होना",
            "हाथ-पैर ठंडे रहना और नाखूनों का चम्मच के आकार जैसा मुड़ जाना (Koilonychia)"
        ],
        "precautions": [
            "आयरन युक्त आहार लें (पालक, मेथी, गुड़, चना, अनार, चुकंदर, दालें)",
            "आयरन के अवशोषण को बढ़ाने के लिए विटामिन सी (नींबू, संतरा, आंवला) साथ लें",
            "खाने के तुरंत बाद चाय या कॉफी न पिएं क्योंकि ये आयरन के अवशोषण को रोकते हैं",
            "गर्भावस्था और स्तनपान के दौरान नियमित आयरन और फोलिक एसिड की गोलियां लें"
        ],
        "diagnostic_tests": [
            "कम्प्लीट ब्लड काउंट (CBC with Hemoglobin & RBC Indices)",
            "पेरिफेरल ब्लड स्मीयर जांच (माइक्रोसाइटिक हाइपोक्रोमिक आरबीसी जांच)",
            "सीरम फेरिटिन टेस्ट (Serum Ferritin - शरीर में आयरन का मुख्य भंडार)",
            "टोटल आयरन बाइंडिंग कैपेसिटी (TIBC) और सीरम आयरन",
            "विटामिन बी12 और फोलेट लेवल",
            "स्टूल ऑकल्ट ब्लड टेस्ट (आंतों से गुप्त रक्तस्राव जांच)"
        ],
        "treatment": [
            "आयरन सप्लीमेंट की गोलियां (Ferrous Ascorbate / Sulfate)",
            "गंभीर कमी होने पर नस द्वारा आयरन इंजेक्शन (IV Iron Infusion)",
            "विटामिन B12 या फोलिक एसिड की गोलियां",
            "हीमोग्लोबिन 7 g/dL से कम या गंभीर आपात स्थिति में ब्लड ट्रांसफ्यूजन"
        ],
        "risk_factors": [
            "भोजन में पौष्टिक तत्वों और आयरन की कमी",
            "मासिक धर्म में अत्यधिक रक्तस्राव या बार-बार गर्भधारण",
            "पेट के कीड़े या बवासीर/अल्सर से खून का रिसाव",
            "गुर्दे की पुरानी बीमारी या आंतों में अवशोषण की समस्या"
        ],
        "when_to_see_doctor": "यदि सीने में दर्द हो, आराम करने पर भी सांस फूले, चक्कर खाकर बेहोश हो जाएं या काले रंग का मल आए तो तुरंत अस्पताल में आपातकालीन जांच कराएं।",
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
    """Returns pre-indexed disease info instantly for fast button clicks with strict word matching."""
    q = (query or "").lower().strip()
    if not q:
        return None
    source_dict = INSTANT_DISEASES_HI if target_lang == "hi" else INSTANT_DISEASES

    # 1. Exact match on primary key
    if q in source_dict:
        return dict(source_dict[q])

    # 2. Precise word boundary match
    for key, data in source_dict.items():
        if key == q or f" {key} " in f" {q} " or q.startswith(key + " ") or q.endswith(" " + key):
            return dict(data)

    # 3. Clinical synonyms and vernacular aliases
    alias_map = {
        "cancer": ["cancer", "oncology", "tumour", "tumor", "carcinoma", "neoplasm", "malignancy", "कैंसर", "कर्क रोग"],
        "tuberculosis": ["tuberculosis", "tb", "t.b.", "t.b", "mycobacterium", "क्षय रोग", "टीबी", "तपेदिक"],
        "malaria": ["malaria", "plasmodium", "मलेरिया"],
        "dengue": ["dengue", "breakbone", "डेंगू", "डेंगी"],
        "typhoid": ["typhoid", "enteric fever", "salmonella", "टाइफाइड", "मियादी बुखार"],
        "diabetes": ["sugar", "madhumeh", "glucose", "diabetic", "मधुमेह", "शुगर"],
        "hypertension": ["bp", "blood pressure", "high bp", "raktschap", "hypertensive", "बीपी", "रक्तचाप", "उच्च रक्तचाप"],
        "asthma": ["asthma", "dama", "wheeze", "bronchial asthma", "दमा", "अस्थमा"],
        "pneumonia": ["pneumonia", "lung infection", "निमोनिया"],
        "arthritis": ["arthritis", "gathiya", "joint pain", "jod", "osteoarthritis", "rheumatoid", "गठिया", "जोड़ों का दर्द"],
        "common cold": ["cold", "flu", "sardi", "jukham", "common cold", "coryza", "सर्दी", "जुकाम", "नजला"],
        "coronavirus": ["corona", "covid", "covid-19", "covid19", "sars-cov-2", "कोरोना"],
        "migraine": ["migraine", "half headache", "throbbing headache", "आधासीसी", "माइग्रेन"],
        "jaundice": ["jaundice", "icterus", "bilirubin", "yellow eyes", "पीलिया"],
        "anemia": ["anemia", "anaemia", "low hemoglobin", "khoon ki kami", "एनीमिया", "खून की कमी"]
    }

    words = set(q.split())
    for target_key, aliases in alias_map.items():
        if target_key in source_dict:
            for alias in aliases:
                if alias == q or f" {alias} " in f" {q} " or alias in words or q.startswith(alias + " ") or q.endswith(" " + alias):
                    return dict(source_dict[target_key])

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
