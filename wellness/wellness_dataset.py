"""
MedAssist - Wellness Hub Verified Dataset
Authoritative Ayurvedic remedies, evidence-based home care, nutrition and safety warnings.
Sources:
- Ministry of AYUSH, Government of India (ayush.gov.in)
- National Health Portal (NHP India - nhp.gov.in)
- Indian Council of Medical Research (ICMR - icmr.gov.in)
- WHO Traditional Medicine & Global Health Guidelines (who.int)
- NIH MedlinePlus & PubMed Central (medlineplus.gov / ncbi.nlm.nih.gov)
"""

from typing import List, Dict, Any, Optional

CATEGORIES = [
    {"id": "hair", "name_en": "💇 Hair Issues", "name_hi": "💇 बालों की समस्याएं", "icon": "💇"},
    {"id": "skin", "name_en": "💄 Skin Issues", "name_hi": "💄 त्वचा की समस्याएं", "icon": "💄"},
    {"id": "weight", "name_en": "⚖️ Weight & Fitness", "name_hi": "⚖️ वजन और फिटनेस", "icon": "⚖️"},
    {"id": "digestion", "name_en": "🍽️ Digestive Issues", "name_hi": "🍽️ पाचन संबंधी समस्याएं", "icon": "🍽️"},
    {"id": "sleep", "name_en": "😴 Sleep & Energy", "name_hi": "😴 नींद और ऊर्जा", "icon": "😴"},
    {"id": "mental", "name_en": "😰 Mental & Stress", "name_hi": "😰 मानसिक तनाव और चिंता", "icon": "😰"},
    {"id": "general", "name_en": "💪 General Health & Lifestyle", "name_hi": "💪 सामान्य स्वास्थ्य और जीवनशैली", "icon": "💪"},
    {"id": "women", "name_en": "👶 Women-Specific", "name_hi": "👶 महिला स्वास्थ्य", "icon": "👶"},
    {"id": "men", "name_en": "👨 Men-Specific", "name_hi": "👨 पुरुष स्वास्थ्य", "icon": "👨"},
    {"id": "seasonal", "name_en": "🌡️ Seasonal Issues", "name_hi": "🌡️ मौसमी समस्याएं", "icon": "🌡️"}
]

# Full 83 topics across all 10 categories
WELLNESS_DATA = {
    # ==========================================
    # CATEGORY 1: 💇 Hair Issues (10 issues)
    # ==========================================
    "hair_fall": {
        "id": "hair_fall",
        "category_id": "hair",
        "category_name": "💇 Hair Issues",
        "title_en": "Hair Fall / Hair Loss",
        "title_hi": "बालों का झड़ना (Hair Fall)",
        "overview_en": "Losing 50-100 hair strands daily is normal. Excessive loss often stems from nutritional deficits, stress, hard water, or hormonal imbalance.",
        "overview_hi": "रोजाना 50-100 बाल गिरना सामान्य है। इससे अधिक बाल गिरना पोषण की कमी, तनाव, खारा पानी या हार्मोनल असंतुलन का संकेत हो सकता है।",
        "causes_en": ["Iron, Zinc & Biotin deficiency", "Chronic stress and poor sleep", "Hormonal imbalance (Thyroid / PCOS)", "Hard water and harsh chemical shampoos", "Dandruff and fungal scalp build-up"],
        "causes_hi": ["आयरन, जिंक और बायोटिन की कमी", "अत्यधिक मानसिक तनाव व अनिद्रा", "थायराइड या पीसीओएस (PCOS)", "खारा पानी व सल्फेट युक्त शैम्पू", "रूसी (Dandruff) और स्कैल्प इन्फेक्शन"],
        "ayurvedic_remedies_en": [
            "Bhringraj (King of Hair) Taila: Warm gentle massage into scalp twice weekly. Promotes follicular circulation.",
            "Amla & Shikakai Paste: Soak dried amla and shikakai overnight, grind and apply as a pack for 25 mins.",
            "Nasyam (AYUSH Protocol): 2 drops of Anu Taila or pure cow ghee in each nostril in the morning to calm Pitta dosha.",
            "Brahmi & Ashwagandha Churna: 1/2 tsp with warm milk at bedtime to reduce stress-induced shedding."
        ],
        "ayurvedic_remedies_hi": [
            "भृंगराज तैल मालिश: हफ्ते में दो बार गुनगुने भृंगराज तेल से हल्के हाथों से 10 मिनट स्कैल्प की मालिश करें।",
            "आंवला और शिकाकाई पैक: सूखे आंवले का चूर्ण पानी में भिगोकर पेस्ट बनाएं और बालों की जड़ों में 25 मिनट लगाएं।",
            "नस्य (AYUSH विधि): सुबह खाली पेट दोनों नथुनों में 2-2 बूंद अणु तैल या शुद्ध गाय का घी डालें (पित्त शामक)।",
            "अश्वगंधा व ब्राह्मी: रात को सोने से पहले आधा चम्मच गुनगुने दूध के साथ लें, तनाव से बाल गिरना रुकता है।"
        ],
        "home_remedies_en": [
            "Onion Juice Extract: Apply fresh sulfur-rich onion juice to patches for 15-20 mins, then rinse with mild shampoo.",
            "Methi (Fenugreek) Mask: Soak 2 tbsp fenugreek seeds overnight, grind into a smooth paste and apply for 30 mins.",
            "Curd & Curry Leaves: Blend fresh curry leaves with unflavored curd to nourish weakened roots."
        ],
        "home_remedies_hi": [
            "प्याज का रस: ताजे प्याज का रस निकालकर स्कैल्प पर 15-20 मिनट लगाएं, फिर माइल्ड शैम्पू से धो लें।",
            "मेथी दाना लेप: 2 चम्मच मेथी रातभर पानी में भिगोकर पीसें और जड़ों में 30 मिनट तक लगाएं।",
            "कढ़ी पत्ता व दही: ताजी कढ़ी पत्तियों को दही के साथ पीसकर हेयर मास्क बनाएं।"
        ],
        "diet_nutrition_en": [
            "Protein-rich lentils, chickpeas, paneer, and eggs for keratin building.",
            "Iron sources: Spinach, beetroot, dates, jaggery, and sesame seeds.",
            "Healthy fats: Walnuts, almonds, and flaxseeds rich in Omega-3.",
            "Hydration: Minimum 2.5 - 3 liters of water daily."
        ],
        "diet_nutrition_hi": [
            "प्रोटीन युक्त दालें, चना, पनीर और सोयाबीन ताकि केराटिन मजबूत बने।",
            "आयरन स्रोत: पालक, चुकंदर, खजूर, गुड़ और तिल।",
            "ओमेगा-3 फैटी एसिड: अखरोट, बादाम और अलसी के बीज।",
            "भरपूर जलपान: प्रतिदिन कम से कम 2.5 से 3 लीटर पानी पिएं।"
        ],
        "dos_and_donts_en": {
            "dos": ["Use a wide-toothed wooden comb", "Wash hair with lukewarm or cold water", "Practice Sarvangasana or Pranayama daily for scalp blood flow"],
            "donts": ["Avoid hot blow-drying and frequent chemical straightening", "Do not comb wet hair aggressively", "Avoid tight hairstyles that cause traction alopecia"]
        },
        "dos_and_donts_hi": {
            "dos": ["चौड़े दांतों वाली लकड़ी की कंघी का प्रयोग करें", "बाल हमेशा गुनगुने या ताजे पानी से धोएं", "रोजाना 10 मिनट अनुलोम-विलोम व सर्वांगासन करें"],
            "donts": ["गीले बालों में जोर से कंघी न करें", "हेयर ड्रायर की तेज गर्म हवा से बचें", "बालों को बहुत कसकर न बांधें"]
        },
        "when_to_see_doctor_en": "See a dermatologist if you notice sudden coin-shaped bald spots (Alopecia Areata), severe scalp redness/burning, or dramatic hair shedding after starting a new prescription medicine.",
        "when_to_see_doctor_hi": "यदि सिर में सिक्के जैसे गोल चकत्ते (Alopecia) दिखें, स्कैल्प में तेज जलन या मवाद हो, अथवा किसी नई दवा के बाद अचानक गुच्छे गिरने लगें तो तुरंत चर्म रोग विशेषज्ञ (Dermatologist) से मिलें।",
        "allergy_keywords": ["mustard", "onion", "sesame", "curd", "dairy", "fenugreek"],
        "sources": "Ministry of AYUSH Guidelines, National Health Portal (NHP India) & ICMR Dietary Norms"
    },
    "dandruff": {
        "id": "dandruff",
        "category_id": "hair",
        "category_name": "💇 Hair Issues",
        "title_en": "Dandruff / Flaky Scalp",
        "title_hi": "रूसी / डैंड्रफ (Dandruff)",
        "overview_en": "A common fungal-inflammatory condition (Malassezia yeast) causing flaky, itchy scalp, aggravated by cold weather and excess sebum.",
        "overview_hi": "स्कैल्प पर फंगल असंतुलन (Malassezia) के कारण होने वाली पपड़ीदार रूसी और खुजली, जो सर्दियों और तनाव में बढ़ जाती है।",
        "causes_en": ["Overgrowth of Malassezia yeast", "Excess sebum or overly dry scalp", "Infrequent hair washing", "Reaction to harsh hair styling gels"],
        "causes_hi": ["फंगल संक्रमण (मलासेजिया)", "स्कैल्प का बहुत ज्यादा तैलीय या सूखा होना", "हफ्ते में पर्याप्त बाल न धोना", "केमिकल युक्त हेयर जेल व स्प्रे"],
        "ayurvedic_remedies_en": [
            "Neem Taila & Coconut Oil: Warm mixture applied 30 minutes before washing. Neem provides natural antifungal azadirachtin.",
            "Triphala Kashayam Wash: Rinse hair with cooled Triphala decoction to balance Kapha-Vata in scalp.",
            "Tulsi & Camphor Lepa: Ground holy basil leaves with a pinch of pure camphor (Kapoor) in coconut oil."
        ],
        "ayurvedic_remedies_hi": [
            "नीम तैल व नारियल तेल: हल्के गुनगुने नीम तेल से मालिश करें। नीम फंगस को जड़ से खत्म करता है।",
            "त्रिफला काढ़े से धुलाई: त्रिफला पाउडर को पानी में उबालकर ठंडा करें और सिर धोने के बाद अंतिम रिंस के रूप में डालें।",
            "तुलसी व कपूर लेप: तुलसी के पत्तों का पेस्ट थोड़े से कपूर और नारियल तेल में मिलाकर 20 मिनट लगाएं।"
        ],
        "home_remedies_en": [
            "Lemon Juice with Coconut Oil: 1 tbsp fresh lemon juice mixed with 2 tbsp coconut oil applied for 15 mins.",
            "Apple Cider Vinegar (ACV) Rinse: Dilute ACV 1:3 with water, spray on scalp after shampooing, rinse after 5 mins.",
            "Aloe Vera Gel: Fresh gel applied directly to cool itching and soothe inflammation."
        ],
        "home_remedies_hi": [
            "नींबू का रस और नारियल तेल: 1 चम्मच नींबू का रस 2 चम्मच नारियल तेल में मिलाकर 15 मिनट लगाएं।",
            "सेब का सिरका (ACV): 1 भाग सिरका 3 भाग पानी में मिलाकर सिर धोने के बाद स्प्रे करें और 5 मिनट बाद धो लें।",
            "एलोवेरा जेल: ताजा एलोवेरा जेल खुजली और जलन को तुरंत शांत करता है।"
        ],
        "diet_nutrition_en": [
            "Incorporate Zinc and B-complex vitamins (whole grains, nuts, pulses).",
            "Reduce refined sugars and deep-fried oily street foods which feed yeast.",
            "Drink probiotic chaas (buttermilk) infused with roasted cumin."
        ],
        "diet_nutrition_hi": [
            "जिंक और विटामिन बी युक्त खाद्य पदार्थ (साबुत अनाज, दालें)।",
            "ज्यादा चीनी और तली-भुनी चीजें कम करें क्योंकि ये फंगस को बढ़ाती हैं।",
            "भुने जीरे वाली ताजी छाछ रोज दोपहर पिएं।"
        ],
        "dos_and_donts_en": {
            "dos": ["Wash pillow covers and combs weekly in hot water", "Keep hair completely dry after bathing before tying"],
            "donts": ["Do not scratch aggressively with fingernails", "Avoid leaving heavy sticky oils overnight on acute dandruff"]
        },
        "dos_and_donts_hi": {
            "dos": ["तकिए का कवर और कंघी हफ्ते में एक बार गर्म पानी से धोएं", "बाल धोने के बाद पूरी तरह सूखने पर ही बांधें"],
            "donts": ["नाखूनों से स्कैल्प को जोर से न खरोंचें", "रूसी होने पर रातभर गाढ़ा तेल लगाकर न छोड़ें"]
        },
        "when_to_see_doctor_en": "Consult a doctor if scales spread to eyebrows, ears, or chest (Seborrheic Dermatitis) or if you see yellowish crusts and thick bleeding flakes.",
        "when_to_see_doctor_hi": "अगर पपड़ी भौंहों, कानों के पीछे या छाती तक फैल जाए या पीले रंग की बदबूदार पपड़ी जमे, तो तुरंत डॉक्टर को दिखाएं।",
        "allergy_keywords": ["lemon", "neem", "camphor", "curd"],
        "sources": "Ministry of AYUSH Ayurvedic Pharmacopoeia & National Health Portal (NHP)"
    },
    "hair_thinning": {
        "id": "hair_thinning",
        "category_id": "hair",
        "category_name": "💇 Hair Issues",
        "title_en": "Hair Thinning",
        "title_hi": "बालों का पतला होना (Hair Thinning)",
        "overview_en": "Gradual reduction in hair diameter and volume across the crown, often linked to age, micro-nutrient deficiencies, and androgen sensitivity.",
        "overview_hi": "बालों की मोटाई और घनत्व का धीरे-धीरे कम होना। यह पोषण की कमी, तनाव या उम्र के प्रभाव से होता है।",
        "causes_en": ["Protein & amino acid deficiency", "Age-related follicular miniaturization", "Thyroid imbalance", "Excessive heat styling"],
        "causes_hi": ["प्रोटीन और अमीनो एसिड की कमी", "उम्र के साथ बालों की जड़ों का कमजोर होना", "थायराइड का असंतुलन", "हेयर स्ट्रेटनर व केमिकल्स का अत्यधिक उपयोग"],
        "ayurvedic_remedies_en": ["Brahmi-Amla hair pack applied weekly", "Castor oil diluted 1:1 with almond oil", "Shirodhara or daily Brahmi Ghrita intake (1 tsp)"],
        "ayurvedic_remedies_hi": ["ब्राह्मी और आंवले का चूर्ण पानी में घोलकर हफ्ते में एक बार लगाएं", "अरंडी (कैस्टर) का तेल बादाम तेल में मिलाकर लगाएं", "रोज सुबह 1 चम्मच ब्राह्मी घृत का सेवन करें"],
        "home_remedies_en": ["Rosemary water spray applied to roots daily", "Egg white mask for pure natural keratin", "Green tea rinse loaded with antioxidants"],
        "home_remedies_hi": ["रोजमेरी पानी का स्कैल्प पर रोजाना स्प्रे", "अंडे की सफेदी का पैक (प्राकृतिक प्रोटीन)", "ग्रीन टी से सिर धोना (एंटीऑक्सीडेंट युक्त)"],
        "diet_nutrition_en": ["Sprouts, paneer, pumpkin seeds, and amla candy daily.", "Zinc and Vitamin C for collagen synthesis."],
        "diet_nutrition_hi": ["अंकुरित मूंग, चना, पनीर और कद्दू के बीज।", "विटामिन सी युक्त ताजे खट्टे फल और आंवला।"],
        "dos_and_donts_en": {"dos": ["Gentle scalp massage to stimulate blood flow", "Air-dry hair naturally"], "donts": ["Avoid tight rubber bands", "Limit bleaching and dyes"]},
        "dos_and_donts_hi": {"dos": ["रोजाना 5 मिनट उंगलियों से स्कैल्प की सौम्य मालिश करें", "बालों को प्राकृतिक हवा में सुखाएं"], "donts": ["कसे हुए रबर बैंड न लगाएं", "ब्लीच और केमिकल डाई से बचें"]},
        "when_to_see_doctor_en": "Seek medical review if hair thinning is accompanied by sudden weight changes, cold intolerance, or cycle irregularities.",
        "when_to_see_doctor_hi": "अगर बाल पतले होने के साथ अचानक वजन बढ़े, ठंड ज्यादा लगे या पीरियड्स अनियमित हों तो थायराइड टेस्ट करवाएं।",
        "allergy_keywords": ["egg", "almond", "castor"],
        "sources": "ICMR Guidelines on Micronutrients & AYUSH Clinical Protocols"
    },
    "premature_graying": {
        "id": "premature_graying",
        "category_id": "hair",
        "category_name": "💇 Hair Issues",
        "title_en": "Premature Graying",
        "title_hi": "कम उम्र में सफेद बाल (Premature Graying)",
        "overview_en": "Graying of hair before age 25-30, primarily caused by melanocyte oxidation, Vitamin B12 / Copper deficiency, and excessive Pitta.",
        "overview_hi": "कम उम्र में बालों का सफेद होना। यह विटामिन B12 व कॉपर की कमी, पित्त दोष के असंतुलन और ऑक्सीडेटिव स्ट्रेस से होता है।",
        "causes_en": ["Vitamin B12 and Ferritin deficiency", "Excessive mental stress and smoking", "Genetics and copper deficiency", "High Pitta dosha (spicy/sour diet)"],
        "causes_hi": ["विटामिन B12 और फेरिटिन की कमी", "ज्यादा तनाव व धूम्रपान", "पित्त दोष की अधिकता (अत्यधिक तला-मसालेदार भोजन)", "आनुवंशिक कारण"],
        "ayurvedic_remedies_en": ["Amlaki Rasayana: 1 tsp Amla powder with honey in the morning", "Mahabhringraj Taila cooked with iron vessel Amla", "Nasya with cow's ghee"],
        "ayurvedic_remedies_hi": ["आंवला रसायन: सुबह 1 चम्मच आंवला चूर्ण शहद के साथ लें", "लोहे की कड़ाही में पकाया हुआ महाभृंगराज तेल लगाएं", "प्रतिदिन नस्य में 2 बूंद देसी गाय का घी डालें"],
        "home_remedies_en": ["Curry leaves boiled in coconut oil applied weekly", "Black tea rinse to naturally tone gray strands", "Kalonji (Black seed) oil massage"],
        "home_remedies_hi": ["नारियल तेल में कढ़ी पत्ता काला होने तक पकाएं और लगाएं", "काली चाय के पानी से बाल धोएं (नेचुरल कंडीशनर)", "कलोंजी के तेल से मालिश"],
        "diet_nutrition_en": ["Vitamin B12 enriched dairy, mushrooms, and fortified foods.", "Sesame seeds (Til) and soaked walnuts."],
        "diet_nutrition_hi": ["विटामिन B12 युक्त दूध, दही, मशरूम।", "काले तिल और भीगे हुए अखरोट का सेवन।"],
        "dos_and_donts_en": {"dos": ["Eat cooling foods to pacify Pitta", "Protect hair from harsh noon UV rays"], "donts": ["Avoid excessive red chilies and smoking", "Do not pluck gray hair"]},
        "dos_and_donts_hi": {"dos": ["पित्त शांत करने वाले फल व हरी सब्जियां खाएं", "तेज धूप में सिर को सूती कपड़े से ढकें"], "donts": ["सफेद बाल कभी नोचें नहीं", "ज्यादा तीखा, खट्टा और बीड़ी-सिगरेट बंद करें"]},
        "when_to_see_doctor_en": "Get blood tests for Vitamin B12, Thyroid profile, and Serum Ferritin if graying is rapid within a few months.",
        "when_to_see_doctor_hi": "यदि कुछ ही महीनों में तेजी से बाल सफेद हों, तो विटामिन B12 और थायराइड की जांच करवाएं।",
        "allergy_keywords": ["sesame", "walnut", "honey"],
        "sources": "NHP India Ayurveda Compendium & WHO Nutrition Norms"
    },
    "dry_hair": {
        "id": "dry_hair",
        "category_id": "hair",
        "category_name": "💇 Hair Issues",
        "title_en": "Dry Hair",
        "title_hi": "रूखे और बेजान बाल (Dry Hair)",
        "overview_en": "Lack of natural sebum and moisture in hair cuticles, causing frizzy, brittle, and unmanageable hair.",
        "overview_hi": "बालों में प्राकृतिक नमी व सीबम की कमी, जिससे बाल उलझे, बेजान और झाड़ू जैसे रूखे हो जाते हैं।",
        "causes_en": ["Frequent hot water showers", "Over-washing with high-sulfate shampoo", "Dry climate and lack of oiling", "Dehydration"],
        "causes_hi": ["गर्म पानी से सिर धोना", "केमिकल शैम्पू का ज्यादा इस्तेमाल", "तेल न लगाना", "शरीर में पानी की कमी"],
        "ayurvedic_remedies_en": ["Warm Sesame (Til) or Coconut oil champi with steam towel", "Hibiscus (Gurhal) flower paste conditioning", "Aloe vera + honey mask"],
        "ayurvedic_remedies_hi": ["तिल या नारियल तेल की मालिश के बाद गर्म तौलिया लपेटें", "गुड़हल के फूल और पत्तों का पेस्ट कंडीशनर के रूप में लगाएं", "एलोवेरा जेल में थोड़ा शहद मिलाकर लगाएं"],
        "home_remedies_en": ["Mashed ripe banana + 1 tbsp honey mask for 20 mins", "Diluted raw milk spray on dry ends", "Coconut milk rinse"],
        "home_remedies_hi": ["पका केला और 1 चम्मच शहद का पेस्ट 20 मिनट लगाएं", "कच्चे दूध का स्प्रे बालों की छोर पर करें", "ताजे नारियल के दूध से बाल धोएं"],
        "diet_nutrition_en": ["Ghee (1 tsp in warm meals), almonds, hydration (3L water), flaxseed."],
        "diet_nutrition_hi": ["भोजन में 1 चम्मच गाय का घी, भीगे बादाम और 3 लीटर पानी।"],
        "dos_and_donts_en": {"dos": ["Condition after every wash", "Use satin or silk pillowcases"], "donts": ["Never wash with steaming hot water", "Avoid alcohol-based hair sprays"]},
        "dos_and_donts_hi": {"dos": ["बाल धोने के बाद हमेशा कंडीशन करें", "सूती की जगह साटन के तकिए का प्रयोग करें"], "donts": ["कभी भी बहुत गर्म पानी से बाल न धोएं", "अल्कोहल वाले हेयर स्प्रे न लगाएं"]},
        "when_to_see_doctor_en": "Consult if hair becomes extremely brittle with severe scalp scaling or skin cracking.",
        "when_to_see_doctor_hi": "यदि बाल छूने पर ही टूटने लगें या स्कैल्प में घाव बनने लगें तो डॉक्टर को दिखाएं।",
        "allergy_keywords": ["milk", "dairy", "banana", "honey"],
        "sources": "AYUSH Lifestyle Advisory & NHP Portal"
    },
    "oily_scalp": {
        "id": "oily_scalp",
        "category_id": "hair",
        "category_name": "💇 Hair Issues",
        "title_en": "Oily Scalp",
        "title_hi": "अत्यधिक तैलीय स्कैल्प (Oily Scalp)",
        "overview_en": "Hyperactive sebaceous glands producing excess oil, leading to limp, sticky hair that attracts dirt quickly.",
        "overview_hi": "स्कैल्प की तेल ग्रंथियों का अधिक सक्रिय होना, जिससे बाल हमेशा चिपचिपे रहते हैं और धूल चिपकती है।",
        "causes_en": ["Hormonal fluctuations (Androgens)", "High humidity", "Over-washing causing rebound oil", "Diet high in greasy fast food"],
        "causes_hi": ["हार्मोनल बदलाव", "मौसम में उमस", "रोज शैम्पू करने से ज्यादा तेल बनना", "ज्यादा तली-भुनी चीजें खाना"],
        "ayurvedic_remedies_en": ["Multani Mitti (Fuller's earth) + Rose water scalp pack", "Triphala powder wash to clear sebum", "Neem leaf water final rinse"],
        "ayurvedic_remedies_hi": ["मुल्तानी मिट्टी और गुलाब जल का लेप जड़ों में 15 मिनट लगाएं", "त्रिफला चूर्ण के पानी से बाल धोएं", "नीम के पानी से अंतिम बार बाल धोएं"],
        "home_remedies_en": ["Diluted Apple cider vinegar rinse", "Lemon juice diluted in water", "Black tea wash"],
        "home_remedies_hi": ["हल्का सेब का सिरका पानी में मिलाकर धोएं", "नींबू का रस पानी में मिलाकर रिंस करें", "ब्लैक टी के पानी से बाल धोएं"],
        "diet_nutrition_en": ["Green tea, cucumbers, citrus fruits, and zinc-rich foods. Avoid oily fried snacks."],
        "diet_nutrition_hi": ["खीरा, संतरा, नींबू, ग्रीन टी। पकोड़े, समोसे व तली चीजों से बचें।"],
        "dos_and_donts_en": {"dos": ["Wash hair 2-3 times weekly with clarifying herbal shampoo", "Wash hair brushes regularly"], "donts": ["Avoid applying conditioner directly to scalp", "Don't touch hair repeatedly with hands"]},
        "dos_and_donts_hi": {"dos": ["हफ्ते में 2-3 बार हर्बल शैम्पू से धोएं", "कंघी नियमित साफ करें"], "donts": ["कंडीशनर कभी जड़ों में न लगाएं", "बार-बार बालों में हाथ न फेरें"]},
        "when_to_see_doctor_en": "See doctor if accompanied by severe scalp acne, pustules, or foul odor.",
        "when_to_see_doctor_hi": "अगर चिपचिपेपन के साथ सिर में फुंसियां या मवाद बनने लगे तो डॉक्टर को दिखाएं।",
        "allergy_keywords": ["lemon", "neem"],
        "sources": "AYUSH Traditional Skin and Hair Guidelines"
    },
    "hair_breakage": {
        "id": "hair_breakage",
        "category_id": "hair",
        "category_name": "💇 Hair Issues",
        "title_en": "Hair Breakage",
        "title_hi": "बालों का बीच से टूटना (Hair Breakage)",
        "overview_en": "Hair snapping mid-shaft due to damaged cuticles, lack of elasticity, and mechanical or thermal stress.",
        "overview_hi": "बालों का जड़ों से नहीं बल्कि बीच से टूटना। यह बालों की बाहरी परत के क्षतिग्रस्त होने से होता है।",
        "causes_en": ["Chemical treatments (bleach, perm)", "Vigorous towel drying", "Iron deficiency anemia", "Excessive heat"],
        "causes_hi": ["हेयर ब्लीच व केमिकल ट्रीटमेंट", "तौलिए से जोर-जोर से रगड़ना", "खून की कमी (एनीमिया)", "हेयर ड्रायर व कर्लर"],
        "ayurvedic_remedies_en": ["Yashtimadhu (Licorice) + Milk pack for root strength", "Almond oil with vitamin E", "Ashwagandha rasayana"],
        "ayurvedic_remedies_hi": ["मुलेठी चूर्ण दूध में मिलाकर बालों में लगाएं", "बादाम तेल में विटामिन ई मिलाकर हल्की मालिश", "अश्वगंधा चूर्ण का सेवन"],
        "home_remedies_en": ["Soft cotton T-shirt instead of rough towel", "Coconut oil pre-shampoo protection", "Egg yolk + olive oil mask"],
        "home_remedies_hi": ["तौलिए की जगह सूती टी-शर्ट से हल्के से सुखाएं", "बाल धोने से पहले 20 मिनट नारियल तेल लगाएं", "अंडे की जर्दी और जैतून का तेल"],
        "diet_nutrition_en": ["Collagen boosters: Citrus fruits, carrots, spinach, chia seeds, and protein pulses."],
        "diet_nutrition_hi": ["दालें, सोयाबीन, गाजर, पालक और चिया सीड्स।"],
        "dos_and_donts_en": {"dos": ["Detangle gently from ends upwards", "Trim split ends every 2-3 months"], "donts": ["Never brush wet hair", "Avoid hot irons"]},
        "dos_and_donts_hi": {"dos": ["सुलझाते समय नीचे से ऊपर की ओर कंघी करें", "हर 2-3 महीने में कटिंग करवाएं"], "donts": ["गीले बालों में ब्रश न चलाएं", "गर्म चिमटी/आयरन से बचें"]},
        "when_to_see_doctor_en": "Consult if breakage is sudden and accompanied by severe fatigue and pale skin.",
        "when_to_see_doctor_hi": "यदि बाल बहुत ज्यादा टूट रहे हों और साथ में अत्यधिक थकान व कमजोरी हो तो हीमोग्लोबिन चेक करवाएं।",
        "allergy_keywords": ["egg", "almond", "milk"],
        "sources": "ICMR Women Health Guidelines & NHP"
    },
    "split_ends": {
        "id": "split_ends",
        "category_id": "hair",
        "category_name": "💇 Hair Issues",
        "title_en": "Split Ends",
        "title_hi": "दोमुंहे बाल (Split Ends)",
        "overview_en": "Splitting of the hair shaft at the tip due to dryness, UV exposure, and mechanical abrasion.",
        "overview_hi": "बालों के अंतिम सिरे का दो या अधिक भागों में विभाजित हो जाना, जिससे बालों की ग्रोथ रुक जाती है।",
        "causes_en": ["Over-exposure to sun & heat", "Rough combing", "Lack of hair trimming", "Harsh chemical shampoos"],
        "causes_hi": ["तेज धूप और हीटिंग टूल्स", "नियमित ट्रिमिंग न कराना", "रूखापन व पोषण की कमी"],
        "ayurvedic_remedies_en": ["Apply cow ghee or almond oil specifically to hair ends before sleep", "Triphala wash"],
        "ayurvedic_remedies_hi": ["सोने से पहले बालों के अंतिम सिरों पर शुद्ध देसी घी या बादाम तेल लगाएं", "त्रिफला पानी से धोएं"],
        "home_remedies_en": ["Papaya and curd hair mask", "Coconut oil tip coating", "Honey and olive oil leave-in on tips"],
        "home_remedies_hi": ["पपीते और दही का हेयर मास्क", "सिरों पर नारियल तेल की सीलिंग", "शहद और जैतून का तेल सिरों पर"],
        "diet_nutrition_en": ["Biotin rich eggs/nuts, healthy seeds (sunflower, pumpkin), adequate water."],
        "diet_nutrition_hi": ["बायोटिन युक्त बादाम, कद्दू के बीज, हरी सब्जियां।"],
        "dos_and_donts_en": {"dos": ["Trim 0.5 inch every 8-10 weeks", "Always oil hair ends"], "donts": ["Do not peel or split ends with fingers", "Avoid friction with rough fabrics"]},
        "dos_and_donts_hi": {"dos": ["हर 2 महीने में हल्के से छोर कटवाएं", "अंतिम सिरों पर तेल जरूर लगाएं"], "donts": ["हाथों से दोमुंहे बालों को खींचे नहीं", "गीले बाल रगड़ें नहीं"]},
        "when_to_see_doctor_en": "Standard split ends require trimming; see doctor if hair texture suddenly changes completely.",
        "when_to_see_doctor_hi": "दोमुंहे बालों के लिए ट्रिमिंग सबसे बेहतर उपाय है; यदि बालों का पूरा टेक्सचर ही अचानक बदल जाए तो सलाह लें।",
        "allergy_keywords": ["papaya", "curd", "honey"],
        "sources": "AYUSH Ministry Guidelines"
    },
    "scalp_itching": {
        "id": "scalp_itching",
        "category_id": "hair",
        "category_name": "💇 Hair Issues",
        "title_en": "Scalp Itching",
        "title_hi": "सिर में खुजली (Scalp Itching)",
        "overview_en": "Pruritus of the scalp caused by sweat accumulation, product residue, lice, fungal flare-ups, or contact allergy.",
        "overview_hi": "पसीना जमने, रूसी, जूँ या केमिकल एलर्जी के कारण सिर में निरंतर तेज खुजली और जलन होना।",
        "causes_en": ["Sweat & dust accumulation", "Dandruff/Seborrheic dermatitis", "Pediculosis (Head lice)", "Allergy to hair dye"],
        "causes_hi": ["पसीना व धूल जमना", "रूसी व फंगल इन्फेक्शन", "जूँ (Lice) की समस्या", "हेयर डाई से एलर्जी"],
        "ayurvedic_remedies_en": ["Neem leaf boiled water rinse", "Karanja Taila application for anti-parasitic protection", "Camphor in coconut oil"],
        "ayurvedic_remedies_hi": ["नीम के उबले पानी से सिर धोएं", "करंज तेल का प्रयोग (एंटी-पैरासिटिक)", "नारियल तेल में थोड़ा भीमसेनी कपूर मिलाकर लगाएं"],
        "home_remedies_en": ["Tea tree oil (2 drops in 1 tbsp coconut oil)", "Fresh aloe vera soothing gel", "Apple cider vinegar spray"],
        "home_remedies_hi": ["टी ट्री ऑयल 2 बूंद नारियल तेल में मिलाकर लगाएं", "ताजा एलोवेरा जेल लगाएं", "हल्के सिरके के पानी का स्प्रे"],
        "diet_nutrition_en": ["Hydration, avoid excessively spicy fermented foods that trigger itching."],
        "diet_nutrition_hi": ["भरपूर पानी पिएं, ज्यादा खट्टी और बहुत तीखी चीजों से बचें।"],
        "dos_and_donts_en": {"dos": ["Wash hair after heavy sweating/workouts", "Keep hair combs clean"], "donts": ["Never use toxic pest sprays on scalp", "Avoid sharing caps and towels"]},
        "dos_and_donts_hi": {"dos": ["पसीना आने पर सिर जरूर धोएं", "कंघी दूसरों से शेयर न करें"], "donts": ["नाखूनों से स्कैल्प को छीलें नहीं", "असुरक्षित कीटनाशक सिर पर न लगाएं"]},
        "when_to_see_doctor_en": "Seek medical help if you see swelling, weeping yellow sores, or painful swollen lymph nodes in neck.",
        "when_to_see_doctor_hi": "अगर सिर में मवाद वाले दाने हों या गर्दन की गिल्टियों (Lymph nodes) में सूजन आए तो डॉक्टर को दिखाएं।",
        "allergy_keywords": ["tea tree", "camphor", "neem"],
        "sources": "NHP Guidelines on Head Hygiene & AYUSH"
    },
    "hair_dullness": {
        "id": "hair_dullness",
        "category_id": "hair",
        "category_name": "💇 Hair Issues",
        "title_en": "Hair Dullness / Lack of Shine",
        "title_hi": "बालों का रूखापन व चमक खोना (Hair Dullness)",
        "overview_en": "Loss of natural gloss and light reflection caused by open cuticles, pollution deposits, and hard water minerals.",
        "overview_hi": "प्रदूषण, खारे पानी और पोषण की कमी के कारण बालों की स्वाभाविक चमक खो जाना।",
        "causes_en": ["Mineral deposits from hard water", "Sun bleaching and pollution", "Product build-up", "Lack of healthy dietary fats"],
        "causes_hi": ["खारे पानी के मिनरल्स", "धूल व प्रदूषण", "बालों में केमिकल का जमाव", "डाइट में अच्छे फैट्स की कमी"],
        "ayurvedic_remedies_en": ["Methi-Amla conditioning rinse", "Coconut milk hair bath", "Nasya with cow ghee"],
        "ayurvedic_remedies_hi": ["मेथी और आंवले के पानी से बाल धोना", "ताजे नारियल के दूध से बालों का पोषण", "सुबह नाक में गाय का घी डालना"],
        "home_remedies_en": ["Rice water rinse (fermented 24 hrs, diluted)", "Diluted apple cider vinegar final rinse", "Egg white + honey wash"],
        "home_remedies_hi": ["चावल का पानी (Rice water) से बाल धोएं", "सेब का सिरका पानी में घोलकर अंतिम रिंस करें", "अंडे की सफेदी और थोड़ा शहद"],
        "diet_nutrition_en": ["Flaxseeds, walnuts, spinach, amla, and sufficient protein."],
        "diet_nutrition_hi": ["अलसी के बीज, अखरोट, आंवला और हरी पत्तेदार सब्जियां।"],
        "dos_and_donts_en": {"dos": ["Finish hair rinse with cold water to seal cuticles", "Cover hair in traffic/pollution"], "donts": ["Avoid harsh alkaline soaps on hair", "Don't use boiling water"]},
        "dos_and_donts_hi": {"dos": ["आखिरी बार ठंडे पानी से धोएं ताकि चमक लॉक हो सके", "प्रदूषण में सिर ढकें"], "donts": ["कपड़े धोने वाले साबुन या हार्ड शैम्पू से बचें", "बहुत गर्म पानी न डालें"]},
        "when_to_see_doctor_en": "Usually reversible with home care; consult if accompanied by brittle nails and fatigue.",
        "when_to_see_doctor_hi": "सामान्य घरेलू उपायों से ठीक हो जाता है; यदि नाखूनों में भी दरारें आएं तो पोषण जांच करवाएं।",
        "allergy_keywords": ["rice", "honey", "egg"],
        "sources": "AYUSH Traditional Beauty Protocols & ICMR"
    },

    # ==========================================
    # CATEGORY 2: 💄 Skin Issues (15 issues)
    # ==========================================
    "acne_pimples": {
        "id": "acne_pimples",
        "category_id": "skin",
        "category_name": "💄 Skin Issues",
        "title_en": "Acne / Pimples",
        "title_hi": "मुंहासे और पिंपल्स (Acne / Pimples)",
        "overview_en": "Clogged sebaceous pores, bacterial growth (C. acnes), and hormonal surges causing blackheads, whiteheads, and inflamed pimples.",
        "overview_hi": "रोमछिद्रों में तेल और गंदगी जमने तथा बैक्टीरिया पनपने से चेहरे पर होने वाले दाने और मुंहासे।",
        "causes_en": ["Hormonal fluctuations (puberty, menstrual, PCOS)", "Excess oil and dead skin accumulation", "High glycemic sugar & junk food diet", "Stress and touching face repeatedly"],
        "causes_hi": ["हार्मोनल बदलाव (किशोरावस्था, पीरियड्स, पीसीओएस)", "चेहरे पर अतिरिक्त तेल व धूल जमना", "ज्यादा मीठा व जंक फूड खाना", "गंदे हाथों से चेहरे को बार-बार छूना"],
        "ayurvedic_remedies_en": [
            "Neem & Haldi (Turmeric) Lepa: Fresh neem paste with a pinch of organic turmeric applied on spots for 15 mins (Purifies Rakta & Pitta).",
            "Manjistha & Sariva Churna: 1/2 tsp with warm water to naturally detoxify blood as per AYUSH protocols.",
            "Lodhra & Chandan Lepa: Soothing cooling mask for inflamed red pustules."
        ],
        "ayurvedic_remedies_hi": [
            "नीम और हल्दी का लेप: ताजी नीम की पत्तियों का पेस्ट चुटकी भर हल्दी के साथ मुंहासों पर 15 मिनट लगाएं।",
            "मंजिष्ठा और सारिवा: आधा चम्मच गुनगुने पानी से लें (रक्त शोधक औषधि)।",
            "लोध्र व चंदन लेप: लाल और दर्द वाले दानों पर ठंडक देने वाला सुरक्षित लेप।"
        ],
        "home_remedies_en": [
            "Multani Mitti + Rose Water: Absorbs excess oil without stripping moisture (twice weekly).",
            "Ice Compress: Wrap an ice cube in clean cotton cloth and press gently on painful swelling for 2 mins.",
            "Diluted Tea Tree Oil: 1 drop diluted in 1 tsp aloe vera applied as spot treatment only."
        ],
        "home_remedies_hi": [
            "मुल्तानी मिट्टी और गुलाब जल: चेहरे का अतिरिक्त तेल सोखने के लिए हफ्ते में 2 बार लगाएं।",
            "बर्फ की सिकाई: साफ सूती कपड़े में बर्फ लपेटकर पिंपल पर 2 मिनट रखें, सूजन और दर्द कम होगा।",
            "एलोवेरा जेल: ताजा एलोवेरा जेल रात को चेहरे पर लगाएं।"
        ],
        "diet_nutrition_en": [
            "Eat zinc-rich pumpkin seeds, seasonal berries, green leafy vegetables.",
            "Cut out sodas, packaged sweets, deep fried snacks, and excessive dairy.",
            "Drink warm water with mint or coriander seeds (cooling infusion)."
        ],
        "diet_nutrition_hi": [
            "कद्दू के बीज, हरी सब्जियां, खीरा और ताजे मौसमी फल खाएं।",
            "कोल्ड ड्रिंक, ज्यादा चीनी, समोसा-कचोरी और ज्यादा तला खाना बिल्कुल बंद करें।",
            "धनिया के बीज या पुदीने वाला गुनगुना पानी पिएं।"
        ],
        "dos_and_donts_en": {
            "dos": ["Wash face twice daily with mild non-comedogenic cleanser", "Change pillowcase twice a week", "Use separate clean face towel"],
            "donts": ["NEVER pop, squeeze, or pick at pimples (prevents permanent scarring)", "Avoid heavy greasy oil creams on face", "Don't sleep with makeup on"]
        },
        "dos_and_donts_hi": {
            "dos": ["दिन में 2 बार सौम्य फेस वॉश से मुंह धोएं", "तकिए का कवर हफ्ते में दो बार बदलें", "मुंह पोंछने के लिए अलग साफ तौलिया रखें"],
            "donts": ["मुंहासे को कभी भी फोड़ें या दबाएं नहीं (वरना दाग और गड्ढे बन जाएंगे)", "चेहरे पर बहुत गाढ़े तेल न लगाएं", "मेकअप लगाकर कभी न सोएं"]
        },
        "when_to_see_doctor_en": "See a dermatologist for severe cystic/nodular acne, painful lesions spreading below jawline, or if you suspect underlying hormonal issues like PCOS.",
        "when_to_see_doctor_hi": "अगर चेहरे पर गांठदार बड़े दर्दनाक मुंहासे (Cystic acne) हों या चेहरे पर अनचाहे बाल और अनियमित माहवारी हो, तो डॉक्टर को तुरंत दिखाएं।",
        "allergy_keywords": ["turmeric", "haldi", "neem", "tea tree"],
        "sources": "Ministry of AYUSH Guidelines, National Health Portal (NHP India) & ICMR"
    },
    "dark_circles": {
        "id": "dark_circles",
        "category_id": "skin",
        "category_name": "💄 Skin Issues",
        "title_en": "Dark Circles (Periorbital Hyperpigmentation)",
        "title_hi": "आंखों के नीचे काले घेरे (Dark Circles)",
        "overview_en": "Pigmentation and visible blood vessels under thin lower-eyelid skin, triggered by poor sleep, eye strain, anemia, and screen fatigue.",
        "overview_hi": "नींद की कमी, मोबाइल-लैपटॉप का ज्यादा प्रयोग और खून की कमी से आंखों के नीचे बनने वाले काले घेरे।",
        "causes_en": ["Lack of 7-8 hours restful sleep", "Prolonged screen blue-light exposure", "Iron deficiency anemia", "Dehydration and rubbing eyes"],
        "causes_hi": ["पर्याप्त नींद न लेना", "घंटों स्क्रीन (मोबाइल/कंप्यूटर) देखना", "आयरन और हीमोग्लोबिन की कमी", "पानी कम पीना और आंखें रगड़ना"],
        "ayurvedic_remedies_en": ["Kumkumadi Taila: 1-2 drops gently dabbed with ring finger at night", "Triphala eye wash (netra tarpana approach)", "Pure cow ghee dabbed under eyes"],
        "ayurvedic_remedies_hi": ["कुंकुमादि तैल: रात को अनामिका उंगली से 1 बूंद हल्के से थपथपाएं", "त्रिफला के छने हुए पानी से आंखों के छींटे मारना", "शुद्ध देसी गाय का घी रात को लगाएं"],
        "home_remedies_en": ["Cold cucumber slices placed over eyes for 15 mins", "Used chilled green tea bags", "Grated potato juice compress (natural catecholase enzyme)"],
        "home_remedies_hi": ["ठंडे खीरे के टुकड़े 15 मिनट आंखों पर रखें", "ठंडे ग्रीन टी बैग्स आंखों पर रखें", "कच्चे आलू का रस रूई से लगाएं (कालेपन को हल्का करता है)"],
        "diet_nutrition_en": ["Iron and Vitamin K rich foods: Spinach, pomegranate, amla, beetroot, and 3L water daily."],
        "diet_nutrition_hi": ["अनार, चुकंदर, पालक, आंवला और खजूर खाएं ताकि खून की कमी न हो।"],
        "dos_and_donts_en": {"dos": ["Sleep 7-8 hours every night", "Take 20-20-20 screen breaks"], "donts": ["Don't rub eyes aggressively", "Avoid late-night screen browsing in dark"]},
        "dos_and_donts_hi": {"dos": ["रोजाना 7-8 घंटे की गहरी नींद लें", "स्क्रीन देखते समय बीच-बीच में पलकें झपकाएं"], "donts": ["आंखों को जोर से न रगड़ें", "अंधेरे कमरे में लेटकर मोबाइल न चलाएं"]},
        "when_to_see_doctor_en": "See doctor if swelling or dark discoloration is only in one eye and worsening rapidly.",
        "when_to_see_doctor_hi": "यदि केवल एक ही आंख के नीचे अचानक सूजन व दर्द हो तो तुरंत नेत्र रोग विशेषज्ञ को दिखाएं।",
        "allergy_keywords": ["potato", "cucumber", "ghee"],
        "sources": "NHP India Eye and Skin Care Protocols & ICMR"
    },
    "puffiness_under_eyes": {
        "id": "puffiness_under_eyes",
        "category_id": "skin",
        "category_name": "💄 Skin Issues",
        "title_en": "Puffiness (Under Eyes)",
        "title_hi": "आंखों के नीचे सूजन (Eye Puffiness)",
        "overview_en": "Mild swelling or fluid retention in tissue beneath eyes, often after salty meals, crying, or inadequate sleep.",
        "overview_hi": "आंखों के आसपास पानी का जमाव और सूजन, जो ज्यादा नमक खाने, रोने या कम सोने से होती है।",
        "causes_en": ["High sodium/salt intake at dinner", "Poor lymphatic drainage & sleep deficit", "Allergies and sinus congestion"],
        "causes_hi": ["रात के खाने में ज्यादा नमक", "नींद की कमी", "एलर्जी और साइनस की समस्या"],
        "ayurvedic_remedies_en": ["Rose water soaked cotton pads placed for 15 mins", "Gentle massage towards temples with pure almond oil"],
        "ayurvedic_remedies_hi": ["गुलाब जल में भीगी रूई आंखों पर 15 मिनट रखें", "बादाम तेल से कनपटी की ओर हल्के हाथ से लिम्फैटिक मसाज करें"],
        "home_remedies_en": ["Chilled metal spoon press", "Cold green tea compresses (caffeine constricts vessels)", "Elevate head with an extra pillow while sleeping"],
        "home_remedies_hi": ["फ्रिज में रखी ठंडी चम्मच से हल्की सिकाई", "ठंडे ग्रीन टी बैग्स रखें (कैफीन सूजन कम करता है)", "सोते समय सिर को थोड़ा ऊंचा रखें"],
        "diet_nutrition_en": ["Cut late-night salt. Eat potassium rich bananas, cucumbers, and stay hydrated."],
        "diet_nutrition_hi": ["रात को नमक कम खाएं। पोटैशियम युक्त केला, खीरा और नारियल पानी लें।"],
        "dos_and_donts_en": {"dos": ["Sleep with head elevated", "Stay well hydrated during day"], "donts": ["Avoid salty pickles/chips late night", "Don't sleep face down on stomach"]},
        "dos_and_donts_hi": {"dos": ["सिर थोड़ा ऊंचा रखकर सोएं", "दिनभर खूब पानी पिएं"], "donts": ["रात में चिप्स, नमकीन या ज्यादा अचार न खाएं", "पेट के बल उल्टा होकर न सोएं"]},
        "when_to_see_doctor_en": "Seek medical review if eye swelling is severe, red, painful, or accompanied by kidney/thyroid symptoms.",
        "when_to_see_doctor_hi": "अगर आंखों की सूजन के साथ चेहरे और पैरों में भी सूजन हो, तो किडनी व थायराइड की जांच करवाएं।",
        "allergy_keywords": ["almond", "rose water"],
        "sources": "NHP Guidelines & Mayo Clinic Clinical Review"
    },
    "oily_skin": {
        "id": "oily_skin",
        "category_id": "skin",
        "category_name": "💄 Skin Issues",
        "title_en": "Oily Skin",
        "title_hi": "अत्यधिक तैलीय त्वचा (Oily Skin)",
        "overview_en": "Hyper-production of sebum giving a greasy sheen and enlarging facial pores, especially over the T-zone.",
        "overview_hi": "चेहरे पर सीबम का ज्यादा बनना, जिससे त्वचा हमेशा चिपचिपी दिखती है और रोमछिद्र बड़े हो जाते हैं।",
        "causes_en": ["Genetics & hormones", "Humid weather", "Over-cleansing triggering rebound oil", "Heavy greasy skincare products"],
        "causes_hi": ["आनुवंशिक और हार्मोनल कारण", "गर्म और उमस भरा मौसम", "बार-बार साबुन से धोना", "गाढ़ी क्रीम लगाना"],
        "ayurvedic_remedies_en": ["Multani Mitti (Fuller's Earth) + Chandan (Sandalwood) pack", "Neem decoction toner", "Lodhra powder pack"],
        "ayurvedic_remedies_hi": ["मुल्तानी मिट्टी और चंदन का लेप गुलाब जल के साथ", "नीम के पानी से चेहरा साफ करना", "लोध्र पाउडर का फेस पैक"],
        "home_remedies_en": ["Tomato slice rub for 2 mins (natural astringent acids)", "Gram flour (Besan) + raw milk wash", "Witch hazel or rose water splash"],
        "home_remedies_hi": ["टमाटर के टुकड़े से 2 मिनट चेहरे की मालिश (प्राकृतिक एस्ट्रिंजेंट)", "बेसन से मुंह धोना", "गुलाब जल का स्प्रे"],
        "diet_nutrition_en": ["Avoid oily street foods and refined sugar. Eat cucumbers, watermelon, and high-fiber foods."],
        "diet_nutrition_hi": ["खीरा, तरबूज, संतरा खाएं। समोसा, पकोड़ा और ज्यादा चीनी छोड़ें।"],
        "dos_and_donts_en": {"dos": ["Use gel-based non-comedogenic sunscreen", "Blot excess oil with tissue"], "donts": ["Don't wash face more than 3 times daily", "Avoid heavy oil-based creams"]},
        "dos_and_donts_hi": {"dos": ["जेल-बेस्ड सनस्क्रीन का प्रयोग करें", "चेहरे को साफ टिश्यू से थपथपाएं"], "donts": ["दिन में 3 बार से ज्यादा मुंह न धोएं", "गाढ़े तेल वाली क्रीम से बचें"]},
        "when_to_see_doctor_en": "See dermatologist if oily skin leads to severe recurring pustular cystic acne.",
        "when_to_see_doctor_hi": "यदि अत्यधिक तेल के कारण चेहरे पर लगातार मवाद वाले दाने बन रहे हों तो डॉक्टर से मिलें।",
        "allergy_keywords": ["sandalwood", "chandan", "tomato", "besan"],
        "sources": "Ministry of AYUSH Skin Health Guidelines"
    },
    "dry_skin": {
        "id": "dry_skin",
        "category_id": "skin",
        "category_name": "💄 Skin Issues",
        "title_en": "Dry Skin (Xerosis)",
        "title_hi": "रूखी त्वचा (Dry Skin)",
        "overview_en": "Compromised skin barrier lacking hydration and lipids, leading to flaking, tightness, and ash-like dull appearance.",
        "overview_hi": "त्वचा में नमी और तेल की कमी, जिससे त्वचा खिंची-खिंची, सफेद पपड़ीदार और बेजान लगती है।",
        "causes_en": ["Cold dry winter air", "Hot water baths", "Harsh soaps with high pH", "Low dietary healthy fats and water"],
        "causes_hi": ["सर्दियों की शुष्क हवा", "बहुत गर्म पानी से नहाना", "कड़े साबुन का प्रयोग", "पानी कम पीना"],
        "ayurvedic_remedies_en": ["Abhyanga: Full body warm sesame or almond oil massage before bath", "Shatadhauta Ghrita (100-times washed ghee)", "Malai (milk cream) + turmeric application"],
        "ayurvedic_remedies_hi": ["अभ्यंग: नहाने से पहले गुनगुने तिल या बादाम तेल से मालिश", "शतधौत घृत (100 बार धोया हुआ औषधीय घी)", "दूध की ताजी मलाई में चुटकी भर हल्दी लगाकर लगाना"],
        "home_remedies_en": ["Coconut oil applied on damp skin right after bath", "Oatmeal soak paste for dry itchy patches", "Honey mask for 15 mins (natural humectant)"],
        "home_remedies_hi": ["नहाने के तुरंत बाद गीली त्वचा पर नारियल तेल लगाना", "ओट्स (जई) का पेस्ट सूखे चकत्तों पर लगाना", "शहद का फेस पैक 15 मिनट (प्राकृतिक मॉइस्चराइजर)"],
        "diet_nutrition_en": ["Consume 1-2 tsp pure cow ghee, soaked almonds, walnuts, flaxseeds, and plenty of water."],
        "diet_nutrition_hi": ["भोजन में देसी गाय का घी, भीगे बादाम, अखरोट और भरपूर पानी।"],
        "dos_and_donts_en": {"dos": ["Moisturize within 3 minutes of bathing", "Use mild moisturizing soap"], "donts": ["Avoid long steaming showers", "Do not scrub dry flaking skin with harsh loofahs"]},
        "dos_and_donts_hi": {"dos": ["नहाने के 3 मिनट के भीतर मॉइस्चराइजर लगाएं", "माइल्ड ग्लिसरीन साबुन का प्रयोग करें"], "donts": ["ज्यादा गर्म पानी से न नहाएं", "रूखी त्वचा को लूफा से न रगड़ें"]},
        "when_to_see_doctor_en": "Consult if skin cracks deeply with bleeding, severe itching keeping you awake, or signs of infected eczema.",
        "when_to_see_doctor_hi": "यदि त्वचा में दरारें पड़कर खून आने लगे या खुजली के कारण रात को नींद न आए तो चर्म रोग विशेषज्ञ से मिलें।",
        "allergy_keywords": ["milk", "dairy", "honey", "almond", "sesame"],
        "sources": "NHP India Dermatology Advisory & AYUSH"
    },
    "sensitive_skin": {
        "id": "sensitive_skin",
        "category_id": "skin",
        "category_name": "💄 Skin Issues",
        "title_en": "Sensitive Skin",
        "title_hi": "संवेदनशील त्वचा (Sensitive Skin)",
        "overview_en": "Hyper-reactive skin barrier easily irritated by fragrances, chemicals, weather, or touch with redness and stinging.",
        "overview_hi": "ऐसी त्वचा जो किसी भी नए साबुन, धूप या खुशबूदार क्रीम से तुरंत लाल हो जाती है और जलन होने लगती है।",
        "causes_en": ["Damaged skin lipid barrier", "Allergic contact dermatitis", "Harsh fragrances and preservatives in cosmetics"],
        "causes_hi": ["कमजोर त्वचा सुरक्षा परत", "खुशबूदार कॉस्मेटिक्स से एलर्जी", "धूप और धूल का असर"],
        "ayurvedic_remedies_en": ["Chandan (Sandalwood) and Rose water soothing compress", "Ghee application (Vata-Pitta pacifying)", "Cooled coriander seed water wash"],
        "ayurvedic_remedies_hi": ["सफेद चंदन और गुलाब जल का ठंडा लेप", "शुद्ध देसी घी की हल्की परत", "धनिया के उबले व ठंडे पानी से चेहरा धोना"],
        "home_remedies_en": ["Fresh pure aloe vera gel directly from plant", "Cold cucumber slices", "Plain oatmeal paste compress"],
        "home_remedies_hi": ["ताजा शुद्ध एलोवेरा जेल", "खीरे का ठंडा रस", "ओटमील (जई) का सौम्य लेप"],
        "diet_nutrition_en": ["Anti-inflammatory foods: Turmeric, coconut water, leafy greens, pomegranate. Avoid overly spicy food."],
        "diet_nutrition_hi": ["नारियल पानी, अनार, लौकी, तोरी। बहुत तीखे और खट्टे भोजन से बचें।"],
        "dos_and_donts_en": {"dos": ["Always patch-test new products on inner wrist", "Use fragrance-free products"], "donts": ["Never use physical walnut scrubs", "Avoid strong chemical peels"]},
        "dos_and_donts_hi": {"dos": ["कोई भी नई क्रीम लगाने से पहले हाथ पर पैच टेस्ट करें", "बिना खुशबू वाले उत्पाद चुनें"], "donts": ["अखरोट वाले दरदरे स्क्रब से बचें", "केमिकल पीलिंग न कराएं"]},
        "when_to_see_doctor_en": "Consult an allergist/dermatologist if face develops intense burning hives or blistering rash.",
        "when_to_see_doctor_hi": "अगर चेहरे पर तेज जलन, पित्ती (Hives) या फफोले उठने लगें तो तुरंत डॉक्टर को दिखाएं।",
        "allergy_keywords": ["sandalwood", "aloe vera"],
        "sources": "ICMR Guidelines on Allergic Skin Conditions"
    },
    "dark_spots_pigmentation": {
        "id": "dark_spots_pigmentation",
        "category_id": "skin",
        "category_name": "💄 Skin Issues",
        "title_en": "Dark Spots / Hyperpigmentation",
        "title_hi": "झाइयां और काले धब्बे (Dark Spots / Melasma)",
        "overview_en": "Excess melanin clusters caused by UV radiation, post-acne inflammation (PIH), or hormonal triggers (Melasma).",
        "overview_hi": "धूप, पिंपल्स के बाद के निशान या हार्मोनल बदलाव के कारण चेहरे पर पड़ने वाले काले धब्बे और झाइयां।",
        "causes_en": ["UV sunlight exposure without sunscreen", "Post-inflammatory marks after acne", "Hormonal shifts (Pregnancy / Melasma)"],
        "causes_hi": ["धूप में बिना सनस्क्रीन जाना", "पिंपल्स फोड़ने के बाद बने काले निशान", "प्रेग्नेंसी या हार्मोनल झाइयां"],
        "ayurvedic_remedies_en": ["Kumkumadi Taila 3-4 drops massaged nightly", "Manjistha powder with raw milk as face pack", "Licorice (Yashtimadhu) paste"],
        "ayurvedic_remedies_hi": ["कुंकुमादि तेल से रात को 5 मिनट चेहरे की मालिश", "मंजिष्ठा चूर्ण कच्चे दूध में मिलाकर चेहरे पर लगाएं", "मुलेठी का पेस्ट दाग-धब्बों पर लगाएं"],
        "home_remedies_en": ["Potato juice and lemon drops spot application", "Aloe vera gel with pinch of turmeric", "Papaya pulp pack (contains papain enzyme)"],
        "home_remedies_hi": ["आलू का रस और 2 बूंद नींबू का रस", "एलोवेरा जेल में चुटकी भर हल्दी", "पके पपीते का गूदा 15 मिनट लगाएं"],
        "diet_nutrition_en": ["Vitamin C rich amla, oranges, guavas, and antioxidants to naturally suppress excess tyrosinase."],
        "diet_nutrition_hi": ["आंवला, संतरा, अमरूद, नींबू (विटामिन सी त्वचा की रंगत निखारता है)।"],
        "dos_and_donts_en": {"dos": ["Wear SPF 30+ sunscreen daily rain or shine", "Wear wide-brim hats in sun"], "donts": ["Do not scrub pigmented spots aggressively", "Avoid direct noon sun exposure"]},
        "dos_and_donts_hi": {"dos": ["रोजाना सनस्क्रीन जरूर लगाएं (चाहे धूप हो या छांव)", "धूप में छतरी या टोपी का प्रयोग करें"], "donts": ["दाग-धब्बों को स्क्रब से न रगड़ें", "दोपहर की तेज धूप से बचें"]},
        "when_to_see_doctor_en": "Get an evaluation if a spot changes size, shape, has irregular borders, or starts bleeding (rule out Melanoma).",
        "when_to_see_doctor_hi": "यदि कोई तिल या काला धब्बा अचानक बढ़ने लगे, उसका आकार टेढ़ा-मेढ़ा हो या खून निकले तो तुरंत त्वचा कैंसर विशेषज्ञ को दिखाएं।",
        "allergy_keywords": ["licorice", "milk", "papaya", "lemon"],
        "sources": "NHP India Dermatology & AYUSH Pharmacopoeia"
    },
    "wrinkles_fine_lines": {
        "id": "wrinkles_fine_lines",
        "category_id": "skin",
        "category_name": "💄 Skin Issues",
        "title_en": "Wrinkles / Fine Lines",
        "title_hi": "झुर्रियां और बारीक रेखाएं (Wrinkles)",
        "overview_en": "Gradual loss of collagen and elastin fibers in dermis accelerated by sun damage, smoking, dehydration, and free radicals.",
        "overview_hi": "उम्र बढ़ने, धूप और त्वचा में कोलेजन की कमी से चेहरे और माथे पर झुर्रियां पड़ना।",
        "causes_en": ["Sun photoaging (UV breakdown of collagen)", "Dehydration and smoking", "Facial repetitive expressions", "Lack of sleep"],
        "causes_hi": ["धूप से कोलेजन का टूटना", "पानी कम पीना व धूम्रपान", "तनाव और कम नींद"],
        "ayurvedic_remedies_en": ["Ashwagandha & Shatavari Rasayana for cellular rejuvenation", "Almond oil gentle upward massage", "Triphala Ghritham"],
        "ayurvedic_remedies_hi": ["अश्वगंधा व शतावरी का सेवन (कोशिकाओं का कायाकल्प)", "बादाम तेल से नीचे से ऊपर की ओर चेहरे की मालिश", "त्रिफला घृत का प्रयोग"],
        "home_remedies_en": ["Egg white mask with honey for instant skin firming", "Banana and olive oil nourishment pack", "Flaxseed gel application"],
        "home_remedies_hi": ["अंडे की सफेदी और शहद का पैक (त्वचा में कसाव लाता है)", "पका केला और जैतून का तेल", "अलसी के बीज का जेल चेहरे पर लगाना"],
        "diet_nutrition_en": ["Antioxidant-rich pomegranate, carrots, amla, walnuts, and Vitamin E sources."],
        "diet_nutrition_hi": ["अनार, गाजर, चुकंदर, बादाम, अखरोट और पर्याप्त पानी।"],
        "dos_and_donts_en": {"dos": ["Always massage in upward strokes", "Apply broad-spectrum sunscreen"], "donts": ["Avoid squinting without sunglasses", "Do not smoke"]},
        "dos_and_donts_hi": {"dos": ["हमेशा नीचे से ऊपर की दिशा में चेहरे की मालिश करें", "सनस्क्रीन रोज लगाएं"], "donts": ["धूप में बिना चश्मे के आंखें न सिकोड़ें", "धूम्रपान से बचें"]},
        "when_to_see_doctor_en": "Normal aging sign; consult a dermatologist if premature aging occurs alongside extreme fatigue or joint pain.",
        "when_to_see_doctor_hi": "यह स्वाभाविक उम्र का हिस्सा है; यदि बहुत कम उम्र में त्वचा अचानक ढीली पड़ने लगे तो स्वास्थ्य जांच कराएं।",
        "allergy_keywords": ["egg", "honey", "almond"],
        "sources": "ICMR Healthy Aging Guidelines & AYUSH"
    },
    "dull_skin": {
        "id": "dull_skin",
        "category_id": "skin",
        "category_name": "💄 Skin Issues",
        "title_en": "Dull Skin",
        "title_hi": "बेजान और फीकी त्वचा (Dull Skin)",
        "overview_en": "Lack of natural radiance and glow due to dead skin cell build-up, poor microcirculation, and systemic fatigue.",
        "overview_hi": "चेहरे पर प्राकृतिक निखार न होना, मृत त्वचा का जमना और थकान की वजह से चेहरा फीका दिखना।",
        "causes_en": ["Dead skin build-up", "Dehydration and pollution", "Lack of exercise and poor sleep", "Iron deficiency"],
        "causes_hi": ["मृत त्वचा की परत", "शरीर में पानी और नींद की कमी", "व्यायाम न करना", "खून की कमी"],
        "ayurvedic_remedies_en": ["Ubtan: Besan, turmeric, sandalwood, raw milk paste", "Kumkumadi taila night drops", "Anu Taila Nasya"],
        "ayurvedic_remedies_hi": ["उबटन: बेसन, हल्दी, चंदन और कच्चे दूध का पारंपरिक लेप", "कुंकुमादि तेल की रात में मालिश", "नस्य का प्रयोग"],
        "home_remedies_en": ["Coffee powder + honey gentle scrub (once weekly)", "Papaya pulp face mask", "Rose water spray splash"],
        "home_remedies_hi": ["कॉफी पाउडर और शहद का सौम्य स्क्रब (हफ्ते में 1 बार)", "पपीते का पल्प लगाना", "दिन में 2 बार गुलाब जल का छिड़काव"],
        "diet_nutrition_en": ["Citrus fruits, beetroot juice, carrots, tender coconut water, and 3 liters water daily."],
        "diet_nutrition_hi": ["चुकंदर और गाजर का जूस, नारियल पानी, संतरा और 3 लीटर पानी रोज।"],
        "dos_and_donts_en": {"dos": ["Exfoliate gently once a week", "Do 20 mins brisk walking for blood circulation"], "donts": ["Avoid daily harsh scrubbing", "Avoid skipping moisturizer"]},
        "dos_and_donts_hi": {"dos": ["हफ्ते में एक बार सौम्य स्क्रब करें", "रोजाना 20 मिनट तेज टहलें ताकि चेहरे तक खून का दौरा बढ़े"], "donts": ["रोज-रोज चेहरे को न रगड़ें", "बिना मॉइस्चराइजर न रहें"]},
        "when_to_see_doctor_en": "Seek medical review if dullness is accompanied by extreme fatigue, pallor, or shortness of breath (Anemia).",
        "when_to_see_doctor_hi": "यदि चेहरे के फीकेपन के साथ सांस फूलना और अत्यधिक कमजोरी हो तो हीमोग्लोबिन टेस्ट कराएं।",
        "allergy_keywords": ["coffee", "honey", "papaya", "besan", "turmeric"],
        "sources": "NHP India Traditional Wellness & ICMR"
    },
    "eczema_mild": {
        "id": "eczema_mild",
        "category_id": "skin",
        "category_name": "💄 Skin Issues",
        "title_en": "Eczema (Mild)",
        "title_hi": "एक्जिमा - हल्का (Mild Eczema)",
        "overview_en": "Atopic dermatitis causing dry, intensely itchy, inflamed, and scaly skin patches.",
        "overview_hi": "त्वचा पर लाल, सूखे, खुजलीदार चकत्ते जो मौसम बदलने या साबुन की एलर्जी से भड़क जाते हैं।",
        "causes_en": ["Immune hyper-reactivity & genetic barrier defect", "Harsh soaps, detergents, and synthetic fabrics", "Food triggers and winter dryness"],
        "causes_hi": ["त्वचा की रोग प्रतिरोधक क्षमता का असंतुलन", "डिटर्जेंट, कड़े साबुन और नायलॉन के कपड़े", "सर्दियों का सूखापन"],
        "ayurvedic_remedies_en": ["Neem Taila + Virgin Coconut oil application", "Mahamanjishtadi Kwatha (purifying decoction)", "Khadirarishta under physician guidance"],
        "ayurvedic_remedies_hi": ["नीम तेल और शुद्ध नारियल तेल मिलाकर लगाना", "महामंजिष्ठादि काढ़े का सेवन", "खदिरादिष्ट का सेवन (रक्तशोधक)"],
        "home_remedies_en": ["Colloidal oatmeal bath paste applied to patches", "Pure virgin coconut oil applied 3-4 times daily", "Cold milk compress on itchy areas"],
        "home_remedies_hi": ["ओट्स (जई) का पेस्ट चकत्तों पर लगाना", "शुद्ध नारियल तेल दिन में 3-4 बार लगाएं", "ठंडे दूध में भीगे कपड़े से हल्की सिकाई"],
        "diet_nutrition_en": ["Anti-inflammatory foods: Turmeric, flaxseed, chia seeds, green leafy vegetables. Avoid excessive sour/fermented foods."],
        "diet_nutrition_hi": ["हल्दी, अलसी, हरी सब्जियां। ज्यादा खट्टी और फर्मेंटेड चीजों से परहेज रखें।"],
        "dos_and_donts_en": {"dos": ["Wear loose breathable 100% cotton clothes", "Moisturize skin continuously"], "donts": ["NEVER scratch (causes secondary bacterial infection)", "Avoid scented detergents and hot baths"]},
        "dos_and_donts_hi": {"dos": ["ढीले और 100% सूती कपड़े पहनें", "त्वचा को हमेशा नम रखें"], "donts": ["खुजली कभी न करें (वरना मवाद पड़ सकता है)", "खुशबूदार साबुन और गर्म पानी से बचें"]},
        "when_to_see_doctor_en": "See doctor immediately if patches ooze yellow fluid, become warm and painful, or spread rapidly.",
        "when_to_see_doctor_hi": "यदि चकत्तों से पीला पानी/मवाद निकले या तेज दर्द और बुखार हो तो तुरंत डॉक्टर को दिखाएं।",
        "allergy_keywords": ["coconut", "neem", "oatmeal"],
        "sources": "ICMR Guidelines on Atopic Dermatitis & AYUSH Protocols"
    },
    "psoriasis_mild": {
        "id": "psoriasis_mild",
        "category_id": "skin",
        "category_name": "💄 Skin Issues",
        "title_en": "Psoriasis (Mild)",
        "title_hi": "सोरायसिस - हल्का (Mild Psoriasis)",
        "overview_en": "Autoimmune condition where skin cells multiply too quickly, forming raised, red plaques covered with silvery scales.",
        "overview_hi": "त्वचा पर चांदी जैसी सफेद पपड़ी और लाल चकत्ते बनने की समस्या (ऑटोइम्यून स्थिति)।",
        "causes_en": ["Immune system dysregulation", "Stress, skin trauma (Koebner phenomenon)", "Cold dry weather and infections"],
        "causes_hi": ["इम्यून सिस्टम का असंतुलन", "तनाव और चोट लगना", "सर्दियों का मौसम"],
        "ayurvedic_remedies_en": ["Bakuchi (Psoralea) oil applied under herbal guidance", "Neem and Triphala daily intake", "Panchakarma (Vamana/Virechana) by qualified Vaidya"],
        "ayurvedic_remedies_hi": ["बाकुची तैल का बाहरी प्रयोग", "नीम और त्रिफला का सेवन", "आयुर्वेदिक पंचकर्म चिकित्सा"],
        "home_remedies_en": ["Coconut oil thick application to soften silvery scales", "Aloe vera gel application 3 times daily", "Mild morning sunbathing (10 mins gentle UV rays)"],
        "home_remedies_hi": ["नारियल तेल की मोटी परत लगाएं ताकि पपड़ी नरम रहे", "ताजा एलोवेरा जेल दिन में 3 बार लगाएं", "सुबह की हल्की धूप में 10 मिनट बैठें"],
        "diet_nutrition_en": ["Omega-3 rich walnuts, flaxseeds, turmeric, and pumpkin seeds. Strictly avoid smoking and alcohol."],
        "diet_nutrition_hi": ["हल्दी, अलसी, अखरोट और कद्दू के बीज। बीड़ी, शराब और तंबाकू पूरी तरह बंद करें।"],
        "dos_and_donts_en": {"dos": ["Keep skin thoroughly lubricated", "Practice yoga and meditation to lower stress"], "donts": ["Do not peel silvery scales forcefully", "Avoid skin cuts and scratches"]},
        "dos_and_donts_hi": {"dos": ["त्वचा को कभी सूखने न दें, हमेशा तेल लगाएं", "तनाव कम करने के लिए ध्यान और प्राणायाम करें"], "donts": ["पपड़ी को जबरदस्ती उखाड़ें नहीं (खून निकल सकता है)", "त्वचा पर खरोंच न लगने दें"]},
        "when_to_see_doctor_en": "Requires regular medical monitoring by a dermatologist. See immediately if joints become painful/swollen (Psoriatic arthritis).",
        "when_to_see_doctor_hi": "सोरायसिस में डॉक्टर की निगरानी जरूरी है। यदि जोड़ों में दर्द और सूजन शुरू हो तो तुरंत डॉक्टर से मिलें।",
        "allergy_keywords": ["bakuchi", "neem", "aloe vera"],
        "sources": "WHO Guidelines on Psoriasis & AYUSH Research Protocols"
    },
    "rashes": {
        "id": "rashes",
        "category_id": "skin",
        "category_name": "💄 Skin Issues",
        "title_en": "Rashes (Contact Dermatitis / Heat Rashes)",
        "title_hi": "त्वचा पर दाने और रैशेज (Skin Rashes)",
        "overview_en": "Red, itchy, bumpy skin irritation caused by contact allergens, sweat entrapment, plants, or friction.",
        "overview_hi": "एलर्जी, पसीने या किसी केमिकल के संपर्क में आने से त्वचा पर लाल दाने, खुजली और चकत्ते होना।",
        "causes_en": ["Contact with irritants (detergent, nickel, cosmetics)", "Sweat duct blockage (Prickly heat)", "Insect bites or friction"],
        "causes_hi": ["कड़े डिटर्जेंट, धातु या कॉस्मेटिक्स से एलर्जी", "पसीना रुकना (घमौरियां)", "कीड़े का काटना"],
        "ayurvedic_remedies_en": ["Chandan & Rose water cold paste", "Neem leaf paste with coconut oil", "Turmeric and aloe vera soothing mask"],
        "ayurvedic_remedies_hi": ["चंदन और गुलाब जल का ठंडा लेप", "नीम के पत्तों का पेस्ट नारियल तेल के साथ", "हल्दी और एलोवेरा जेल"],
        "home_remedies_en": ["Cold water cloth compress for 10 mins", "Baking soda bath or paste on localized spot", "Calamine lotion application"],
        "home_remedies_hi": ["ठंडे पानी की पट्टी 10 मिनट रखें", "कैलामाइन लोशन लगाएं (जलन शांत करता है)", "बेकिंग सोडा का हल्का लेप"],
        "diet_nutrition_en": ["Cooling foods: Mint, coconut water, cucumber, coriander seed water. Avoid excess spices."],
        "diet_nutrition_hi": ["पुदीना, नारियल पानी, खीरा, सौंफ का पानी। गरम मसालों से परहेज करें।"],
        "dos_and_donts_en": {"dos": ["Keep area cool, clean, and dry", "Wear light cotton clothing"], "donts": ["Avoid tight synthetic underwear/clothes", "Do not scratch"]},
        "dos_and_donts_hi": {"dos": ["प्रभावित जगह को सूखा और ठंडा रखें", "सूती कपड़े पहनें"], "donts": ["टाइट कपड़े न पहनें", "नाखूनों से न खुजलाएं"]},
        "when_to_see_doctor_en": "Emergency: See doctor immediately if rash spreads rapidly with facial swelling, difficulty breathing, or high fever.",
        "when_to_see_doctor_hi": "आपातकालीन: अगर रैश तेजी से पूरे शरीर में फैले, चेहरे या होंठों पर सूजन आए या सांस लेने में तकलीफ हो तो तुरंत अस्पताल जाएं।",
        "allergy_keywords": ["sandalwood", "neem", "turmeric"],
        "sources": "NHP India Emergency Guidelines & ICMR"
    },
    "blackheads_whiteheads": {
        "id": "blackheads_whiteheads",
        "category_id": "skin",
        "category_name": "💄 Skin Issues",
        "title_en": "Blackheads & Whiteheads (Comedones)",
        "title_hi": "ब्लैकहेड्स और व्हाइटहेड्स (Blackheads & Whiteheads)",
        "overview_en": "Non-inflammatory acne caused by follicles plugged with sebum and keratin; blackheads are open (oxidized), whiteheads are closed.",
        "overview_hi": "रोमछिद्रों में तेल और मृत त्वचा जमने से नाक व ठोड़ी पर बनने वाले काले और सफेद दाने।",
        "causes_en": ["Excess sebum production", "Inadequate cleansing of pores", "Comedogenic makeup and oily creams"],
        "causes_hi": ["अत्यधिक सीबम का बनना", "चेहरे की सही सफाई न होना", "गाढ़े तेल वाले ब्यूटी प्रोडक्ट्स"],
        "ayurvedic_remedies_en": ["Multani Mitti + Lemon juice paste on nose", "Steam with neem leaves to open pores", "Cinnamon (Dalchini) + Honey spot mask"],
        "ayurvedic_remedies_hi": ["मुल्तानी मिट्टी में थोड़ा नींबू का रस मिलाकर नाक पर लगाएं", "नीम की पत्तियों के पानी की भाप लें", "दालचीनी पाउडर और शहद का लेप"],
        "home_remedies_en": ["Facial steam for 5 mins followed by gentle cleansing", "Egg white tissue peel-off mask", "Baking soda and water gentle scrub"],
        "home_remedies_hi": ["हफ्ते में एक बार 5 मिनट चेहरे की भाप लें", "अंडे की सफेदी का पील-ऑफ मास्क", "बेकिंग सोडा का हल्का स्क्रब"],
        "diet_nutrition_en": ["High fiber vegetables, zinc foods, green tea. Cut out fried fast food."],
        "diet_nutrition_hi": ["हरी सब्जियां, ग्रीन टी और खूब पानी पिएं।"],
        "dos_and_donts_en": {"dos": ["Wash face after workouts", "Use salicylic acid or herbal neem washes"], "donts": ["Do not use sharp metal extractors forcefully", "Avoid heavy coconut oil on acne-prone T-zone"]},
        "dos_and_donts_hi": {"dos": ["कसरत के बाद मुंह जरूर धोएं", "नीम युक्त फेसवॉश का प्रयोग करें"], "donts": ["सुई या पिन से ब्लैकहेड्स न कुरेदें", "नाक पर नारियल तेल न लगाएं"]},
        "when_to_see_doctor_en": "See dermatologist if comedones become inflamed into painful cystic pustules.",
        "when_to_see_doctor_hi": "अगर ब्लैकहेड्स में इन्फेक्शन होकर दर्दनाक मुंहासे बनने लगें तो डॉक्टर को दिखाएं।",
        "allergy_keywords": ["cinnamon", "honey", "egg"],
        "sources": "NHP India & AYUSH Dermatology"
    },
    "uneven_skin_tone": {
        "id": "uneven_skin_tone",
        "category_id": "skin",
        "category_name": "💄 Skin Issues",
        "title_en": "Uneven Skin Tone",
        "title_hi": "असमान त्वचा की रंगत (Uneven Skin Tone)",
        "overview_en": "Patchy skin coloring and texture caused by sun exposure, hormonal imbalances, and cellular damage.",
        "overview_hi": "चेहरे के कुछ हिस्सों का ज्यादा गहरा और कुछ का हल्का होना, जो धूप और टैनिंग के कारण होता है।",
        "causes_en": ["Sun damage & tanning", "Post-acne blemishes", "Pollution exposure", "Hormonal shifts"],
        "causes_hi": ["धूप में टैनिंग", "पिंपल्स के पुराने दाग", "प्रदूषण का असर"],
        "ayurvedic_remedies_en": ["Haldi + Chandan + Kesar in raw milk mask", "Kumkumadi Taila overnight application", "Manjistha churna paste"],
        "ayurvedic_remedies_hi": ["हल्दी, चंदन और केसर का कच्चे दूध में उबटन", "कुंकुमादि तेल रात में लगाना", "मंजिष्ठा लेप"],
        "home_remedies_en": ["Tomato and yogurt tan removal pack", "Raw milk cleansing with cotton pad", "Aloe vera + orange peel powder pack"],
        "home_remedies_hi": ["टमाटर और दही का टैन रिमूवल पैक", "कच्चे दूध से चेहरे की सफाई", "एलोवेरा जेल में संतरे के छिलके का पाउडर"],
        "diet_nutrition_en": ["Vitamin C and E: Oranges, amla, almonds, sunflower seeds, green leafy vegetables."],
        "diet_nutrition_hi": ["संतरा, आंवला, बादाम, गाजर और हरी सब्जियां।"],
        "dos_and_donts_en": {"dos": ["Use SPF 30+ sunscreen daily", "Wear sunglasses and hats in direct sun"], "donts": ["Avoid harsh chemical bleaches", "Don't skip night hydration"]},
        "dos_and_donts_hi": {"dos": ["धूप में निकलने से 20 मिनट पहले सनस्क्रीन लगाएं", "धूप का चश्मा पहनें"], "donts": ["केमिकल ब्लीच का बार-बार इस्तेमाल न करें", "रात को बिना मॉइस्चराइजर न सोएं"]},
        "when_to_see_doctor_en": "Consult if skin discoloration is accompanied by numbness or localized loss of sensation.",
        "when_to_see_doctor_hi": "यदि त्वचा के किसी हिस्से पर सुन्नपन (संवेदना खोना) महसूस हो तो तुरंत त्वचा विशेषज्ञ को दिखाएं।",
        "allergy_keywords": ["milk", "turmeric", "sandalwood", "yogurt"],
        "sources": "AYUSH Traditional Guidelines & ICMR"
    },
    "under_eye_bags": {
        "id": "under_eye_bags",
        "category_id": "skin",
        "category_name": "💄 Skin Issues",
        "title_en": "Under-Eye Bags",
        "title_hi": "आंखों के नीचे ढीली त्वचा व थैलियां (Under-Eye Bags)",
        "overview_en": "Mild swelling and sagging of lower eyelid fat pads due to tissue weakening, fluid retention, or aging.",
        "overview_hi": "उम्र और नींद की कमी से आंखों के नीचे की त्वचा का ढीला पड़ना और सूजन की तरह लटकना।",
        "causes_en": ["Aging and loss of skin elasticity", "Chronic fluid retention & high salt diet", "Allergies and sinus issues", "Hereditary predisposition"],
        "causes_hi": ["उम्र के साथ त्वचा की ढीली पड़ना", "ज्यादा नमक खाने से पानी का जमाव", "एलर्जी और आनुवंशिक कारण"],
        "ayurvedic_remedies_en": ["Triphala eye wash infusion", "Light almond oil upward tapping massage", "Nasya with cow's ghee"],
        "ayurvedic_remedies_hi": ["त्रिफला के छने पानी से आंखें धोना", "बादाम तेल से उंगलियों से हल्की थपथपाने वाली मालिश", "नाक में 2 बूंद गाय का घी डालना"],
        "home_remedies_en": ["Cold green tea compress", "Chilled cucumber slices", "Cold spoon press for 2 mins"],
        "home_remedies_hi": ["ठंडे ग्रीन टी बैग्स रखें", "खीरे की ठंडी स्लाइस रखें", "ठंडी चम्मच से 2 मिनट हल्की सिकाई"],
        "diet_nutrition_en": ["Cut back on sodium/salt at dinner. Drink water, eat watermelon, cucumber, and celery."],
        "diet_nutrition_hi": ["रात के खाने में नमक कम करें। तरबूज, खीरा और खूब पानी पिएं।"],
        "dos_and_donts_en": {"dos": ["Elevate head with an extra pillow while sleeping", "Get 7-8 hours sleep"], "donts": ["Avoid heavy salty dinners", "Don't rub lower eyelids roughly"]},
        "dos_and_donts_hi": {"dos": ["सोते समय सिर ऊंचा रखें", "7-8 घंटे की पर्याप्त नींद लें"], "donts": ["रात में चिप्स व ज्यादा नमक न खाएं", "आंखों के नीचे जोर से न रगड़ें"]},
        "when_to_see_doctor_en": "Seek medical review if eye bags are accompanied by swelling in legs/ankles, which could indicate kidney/thyroid concerns.",
        "when_to_see_doctor_hi": "यदि आंखों के साथ पैरों और टखनों में भी सूजन हो तो गुर्दे (Kidney) और थायराइड की जांच करवाएं।",
        "allergy_keywords": ["almond"],
        "sources": "Mayo Clinic Review & NHP India"
    },

    # ==========================================
    # CATEGORY 3: ⚖️ Weight & Fitness (10 issues)
    # ==========================================
    "overweight": {
        "id": "overweight",
        "category_id": "weight",
        "category_name": "⚖️ Weight & Fitness",
        "title_en": "Overweight (BMI 25 - 29.9)",
        "title_hi": "अधिक वजन / मोटापा (Overweight)",
        "overview_en": "Body Mass Index between 25 and 29.9 kg/m2, representing excess adiposity that increases risk of diabetes and hypertension.",
        "overview_hi": "बीएमआई 25 से 29.9 के बीच होना, जिससे भविष्य में डायबिटीज और हाई ब्लड प्रेशर का खतरा बढ़ जाता है।",
        "causes_en": ["Caloric surplus (calories in > calories out)", "Sedentary lifestyle and lack of physical exercise", "High intake of refined carbs, sugar, and saturated fats", "Stress and poor sleep causing high cortisol"],
        "causes_hi": ["शारीरिक मेहनत की कमी और बैठकर काम करना", "ज्यादा मीठा, तली-भुनी चीजें और मैदा खाना", "तनाव और कम नींद से कॉर्टिसोल बढ़ना"],
        "ayurvedic_remedies_en": [
            "Medohar Guggulu: AYUSH approved classical formulation to improve lipid metabolism under consultation.",
            "Warm Honey-Lemon Water: Drink 1 glass of lukewarm water with 1/2 lemon and 1 tsp pure honey in the morning on an empty stomach (Deepana & Pachana).",
            "Triphala Churna: 1 tsp with warm water before bedtime to cleanse digestive tract.",
            "Ginger & Cinnamon Tea: Boosts Agni (digestive fire) and burns excess Meda dhatu (fat tissue)."
        ],
        "ayurvedic_remedies_hi": [
            "गुनगुना नींबू-शहद पानी: रोज सुबह खाली पेट 1 गिलास गुनगुने पानी में आधा नींबू और 1 चम्मच शहद मिलाकर पिएं।",
            "त्रिफला चूर्ण: रात को सोने से पहले 1 चम्मच गुनगुने पानी से लें, पाचन दुरुस्त रहेगा और वसा घटेगी।",
            "अदरक व दालचीनी की चाय: दिन में 1-2 बार पिएं, यह पाचन अग्नि को बढ़ाकर चर्बी घटाती है।",
            "मेदोहर गुग्गुलु: आयुर्वेदिक विशेषज्ञ की सलाह से मेटाबॉलिज्म तेज करने के लिए।"
        ],
        "home_remedies_en": [
            "Jeera (Cumin) Water: Boil 1 tsp cumin seeds in 2 cups of water until reduced to half, drink warm in morning.",
            "Methi Water: Soak 1 tsp fenugreek seeds overnight, strain and drink the water to control hunger cravings.",
            "Brisk 45-minute daily walk or 10,000 steps daily."
        ],
        "home_remedies_hi": [
            "जीरा पानी: 1 चम्मच जीरा 2 गिलास पानी में उबालकर आधा करें और सुबह गुनगुना पिएं।",
            "मेथी का पानी: 1 चम्मच मेथी दाना रातभर भिगोकर सुबह पानी पिएं (भूख नियंत्रित करता है)।",
            "रोजाना 45 मिनट तेज चाल में टहलना या 10,000 कदम चलना।"
        ],
        "diet_nutrition_en": [
            "Follow ICMR plate method: 50% vegetables/salad, 25% protein (dal, paneer, sprouts), 25% complex carbs (millet, brown rice, whole wheat).",
            "Switch to millets (Ragi, Jowar, Bajra) instead of refined wheat/maida.",
            "Drink water 30 minutes before meals, never during meals.",
            "Strictly avoid sugary sodas, packaged fruit juices, and sweets."
        ],
        "diet_nutrition_hi": [
            "ICMR थाली नियम: आधी थाली सलाद व सब्जी, एक चौथाई दाल/पनीर/प्रोटीन, एक चौथाई बाजरा/ज्वार/रोटी।",
            "गेहूं-मैदे की जगह मिलेट्स (बाजरा, ज्वार, रागी) का सेवन बढ़ाएं।",
            "भोजन से आधा घंटा पहले पानी पिएं, खाने के बीच में ज्यादा पानी न पिएं।",
            "मीठी चाय, कोल्ड ड्रिंक और मिठाइयां पूरी तरह छोड़ें।"
        ],
        "dos_and_donts_en": {
            "dos": ["Eat light dinner before 8 PM", "Chew each bite 20-30 times for proper satiety signalling", "Practice Kapalbhati and Surya Namaskar daily"],
            "donts": ["Do not sleep immediately after eating meals", "Avoid crash starvation diets (they destroy muscle and slow metabolism)", "Avoid midnight snacking"]
        },
        "dos_and_donts_hi": {
            "dos": ["रात का खाना हल्का और रात 8 बजे से पहले खाएं", "भोजन को 25-30 बार चबाकर खाएं", "रोज 15 मिनट कपालभाति और सूर्य नमस्कार करें"],
            "donts": ["खाना खाकर तुरंत सोएं नहीं", "क्रैश डाइटिंग (भूखे रहना) न करें, इससे मेटाबॉलिज्म खराब होता है", "देर रात मंचिंग न करें"]
        },
        "when_to_see_doctor_en": "Consult a physician or endocrinologist if weight gain is rapid despite poor appetite, or accompanied by severe lethargy, cold sensitivity, and neck swelling (Thyroid/Cushing's).",
        "when_to_see_doctor_hi": "अगर कम खाने पर भी वजन तेजी से बढ़ रहा हो, बहुत ज्यादा सुस्ती और सांस फूल रही हो तो थायराइड और शुगर की जांच करवाएं।",
        "allergy_keywords": ["honey", "cumin", "fenugreek", "cinnamon"],
        "sources": "ICMR Dietary Guidelines for Indians & Ministry of AYUSH Obesity Protocols"
    },
    "obesity": {
        "id": "obesity",
        "category_id": "weight",
        "category_name": "⚖️ Weight & Fitness",
        "title_en": "Obesity (BMI ≥ 30)",
        "title_hi": "गंभीर मोटापा (Obesity)",
        "overview_en": "Chronic complex disease characterized by excessive adiposity (BMI ≥ 30 kg/m2 for general, ≥ 27.5 for South Asians as per WHO).",
        "overview_hi": "अत्यधिक चर्बी का जमाव जिससे हृदय रोग, डायबिटीज, जोड़ों का दर्द और फैटी लिवर का खतरा बहुत बढ़ जाता है।",
        "causes_en": ["Chronic positive energy balance", "Genetic and metabolic factors", "Hormonal (Insulin resistance, Leptin resistance)", "Medication side effects (steroids, antidepressants)"],
        "causes_hi": ["कैलोरी का असंतुलन", "इंसुलिन रेजिस्टेंस", "हार्मोनल असंतुलन", "लगातार तनाव व शारीरिक निष्क्रियता"],
        "ayurvedic_remedies_en": ["Vrikshamla (Garcinia indica) to regulate lipid synthesis", "Guggul formulations under Ayurvedic MD", "Udvartana (dry herbal powder massage) to mobilize deep tissue fat"],
        "ayurvedic_remedies_hi": ["वृक्षाम्ल (गार्सिनिया) का प्रयोग", "उद्वर्तन (सूखे त्रिफला पाउडर से शरीर की मालिश)", "आयुर्वेदिक चिकित्सक की देखरेख में मेदोहर चिकित्सा"],
        "home_remedies_en": ["Warm water sipping throughout the day (Ushnodaka)", "Intermittent fasting (14:10 or 16:8 schedule under doctor guidance)", "Daily progressive walking and strength training"],
        "home_remedies_hi": ["दिनभर थोड़ा-थोड़ा गुनगुना पानी पीना (उष्णोदक)", "14 से 16 घंटे का उपवास (Intermittent fasting) डॉक्टर की सलाह से", "रोजाना 45 मिनट नियमित व्यायाम"],
        "diet_nutrition_en": ["High protein, high fiber, zero processed sugar. Replace white rice and wheat with millets. Green vegetables, salads before every meal."],
        "diet_nutrition_hi": ["हाई प्रोटीन, हरी सब्जियां, सलाद। सफेद चावल व मैदा बंद करके मिलेट्स खाएं।"],
        "dos_and_donts_en": {"dos": ["Keep a daily food and step diary", "Join a structured fitness program"], "donts": ["Avoid all deep fried snacks, alcohol, and sugary drinks", "Never skip protein"]},
        "dos_and_donts_hi": {"dos": ["रोजाना अपने कदम और खान-पान का हिसाब रखें", "नियमित वजन नापें"], "donts": ["शराब, कोल्ड ड्रिंक और फास्ट फूड पूरी तरह बंद करें", "भूखे रहने के बाद एकदम ज्यादा न खाएं"]},
        "when_to_see_doctor_en": "Consult a physician for personalized medical weight management, screening for Sleep Apnea, Diabetes, and Fatty Liver.",
        "when_to_see_doctor_hi": "मोटापे के साथ सांस फूलना, सोते समय खर्राटे या सीने में भारीपन हो तो तुरंत डॉक्टर से संपर्क करें।",
        "allergy_keywords": ["guggulu", "triphala"],
        "sources": "WHO Obesity Factsheet & ICMR Guidelines"
    },
    "underweight": {
        "id": "underweight",
        "category_id": "weight",
        "category_name": "⚖️ Weight & Fitness",
        "title_en": "Underweight (BMI < 18.5)",
        "title_hi": "कम वजन / दुबलापन (Underweight)",
        "overview_en": "BMI below 18.5 indicating insufficient body mass, associated with weakened immunity, nutritional anemia, and bone density loss.",
        "overview_hi": "बीएमआई 18.5 से कम होना। इससे रोग प्रतिरोधक क्षमता कमजोर होती है, खून की कमी और हड्डियों में कमजोरी आ सकती है।",
        "causes_en": ["Malnutrition or malabsorption", "Hyperthyroidism", "High metabolic rate and poor appetite", "Chronic stress or eating disorders"],
        "causes_hi": ["पोषक तत्वों का शरीर में न लगना", "हाइपरथायरायडिज्म (थायराइड का तेज होना)", "भूख न लगना और कमजोरी", "मानसिक तनाव"],
        "ayurvedic_remedies_en": ["Ashwagandha Lehyam or Churna: 1 tsp with warm milk, banana and ghee", "Shatavari Ghrita for nourishing Dhatus", "Drakshasava to naturally stimulate Agni and appetite"],
        "ayurvedic_remedies_hi": ["अश्वगंधा चूर्ण: 1 चम्मच गुनगुने दूध, केले और 1 चम्मच देसी घी के साथ लें", "शतावरी घृत का सेवन", "द्राक्षासव: भोजन के बाद 2 चम्मच पानी के साथ (भूख बढ़ाता है)"],
        "home_remedies_en": ["Banana and Milk Shake with 5 soaked almonds and dates", "Peanut butter with whole grain bread", "Soaked raisins and figs in morning"],
        "home_remedies_hi": ["केला, दूध, 5 भीगे बादाम और खजूर का शेक", "मूंगफली या पीनट बटर का सेवन", "सुबह भीगी किशमिश और अंजीर खाना"],
        "diet_nutrition_en": ["Nutrient-dense calorie foods: Ghee, paneer, nuts, seeds, dates, bananas, lentils, and whole milk."],
        "diet_nutrition_hi": ["पोषक तत्वों से भरपूर भोजन: देसी घी, पनीर, मखाना, बादाम, अखरोट, खजूर, दालें और दूध।"],
        "dos_and_donts_en": {"dos": ["Eat 5-6 smaller nutrient-dense meals throughout the day", "Do resistance/strength training to build muscle"], "donts": ["Do not rely on unhealthy junk food to gain weight", "Don't skip meals"]},
        "dos_and_donts_hi": {"dos": ["दिन में 5-6 बार पौष्टिक खाना खाएं", "वजन बढ़ाने के लिए कसरत और स्ट्रेंथ ट्रेनिंग करें"], "donts": ["वजन बढ़ाने के चक्कर में तला-भुना जंक फूड न खाएं", "कभी भी भोजन न छोड़ें"]},
        "when_to_see_doctor_en": "Consult doctor if weight loss is unexplained and rapid, or accompanied by night sweats, persistent cough, or diarrhea.",
        "when_to_see_doctor_hi": "अगर बिना किसी कारण के तेजी से वजन घट रहा हो, रात में पसीना या लगातार दस्त हों तो डॉक्टर से जांच करवाएं।",
        "allergy_keywords": ["milk", "dairy", "peanut", "almond"],
        "sources": "ICMR Guidelines on Nutrition & AYUSH Brihmana Protocols"
    },
    "slow_metabolism": {
        "id": "slow_metabolism",
        "category_id": "weight",
        "category_name": "⚖️ Weight & Fitness",
        "title_en": "Slow Metabolism",
        "title_hi": "धीमा मेटाबॉलिज्म (Slow Metabolism)",
        "overview_en": "Low basal metabolic rate (Manda Agni) where body burns fewer calories at rest, leading to fatigue and easy weight gain.",
        "overview_hi": "पाचन अग्नि का मंद होना, जिससे शरीर कम कैलोरी जलाता है और वजन आसानी से बढ़ता है तथा सुस्ती रहती है।",
        "causes_en": ["Sedentary lifestyle & low muscle mass", "Hypothyroidism", "Crash dieting and prolonged fasting", "Inadequate water and protein"],
        "causes_hi": ["मांसपेशियों की कमी और कसरत न करना", "थायराइड का धीमा होना", "बार-बार भूखे रहने वाली डाइटिंग", "पानी और प्रोटीन की कमी"],
        "ayurvedic_remedies_en": ["Trikatu Churna (Ginger, Black Pepper, Pippali): 1/4 tsp with honey before meals to kindle digestive Agni", "Warm ginger tea", "Chitrakadi Vati under Vaidya guidance"],
        "ayurvedic_remedies_hi": ["त्रिकटु चूर्ण (सोंठ, काली मिर्च, पिप्पली): भोजन से पहले चुटकी भर शहद के साथ (पाचन अग्नि तेज करता है)", "अदरक वाली गर्म चाय", "चित्रकादि वटी"],
        "home_remedies_en": ["Green tea (2 cups daily)", "Brisk morning walk in sunlight", "Add a pinch of black pepper and jeera to cooking"],
        "home_remedies_hi": ["ग्रीन टी 1-2 कप रोजाना", "सुबह धूप में 30 मिनट तेज टहलना", "खाने में काली मिर्च, जीरा और हींग का उपयोग"],
        "diet_nutrition_en": ["High protein meals (lentils, paneer, eggs), green leafy vegetables, black pepper, and 3L warm water."],
        "diet_nutrition_hi": ["प्रोटीन युक्त दालें, स्प्राउट्स, पनीर, हल्दी और गुनगुना पानी।"],
        "dos_and_donts_en": {"dos": ["Do strength training 3x weekly to build calorie-burning muscle", "Sleep 7-8 hours"], "donts": ["Avoid starving or skipping meals", "Avoid cold iced drinks"]},
        "dos_and_donts_hi": {"dos": ["हफ्ते में 3 दिन स्ट्रेंथ ट्रेनिंग करें ताकि मांसपेशियां मजबूत हों", "अच्छी नींद लें"], "donts": ["भूखे न रहें", "बर्फ वाला ठंडा पानी न पिएं"]},
        "when_to_see_doctor_en": "Check TSH, Free T3/T4 for hypothyroidism if combined with hair thinning, constipation, and extreme cold intolerance.",
        "when_to_see_doctor_hi": "यदि हमेशा ठंड लगे, कब्ज रहे और बाल पतले हों तो थायराइड (TSH) की जांच करवाएं।",
        "allergy_keywords": ["black pepper", "ginger", "honey"],
        "sources": "ICMR Energy Metabolism Advisory & AYUSH"
    },
    "weight_loss_tips": {
        "id": "weight_loss_tips",
        "category_id": "weight",
        "category_name": "⚖️ Weight & Fitness",
        "title_en": "Weight Loss Tips (Safe & Scientific)",
        "title_hi": "वजन घटाने के सुरक्षित टिप्स (Weight Loss Tips)",
        "overview_en": "Sustainable, clinically sound lifestyle habits to lose fat without sacrificing muscle mass, bone health, or daily vitality.",
        "overview_hi": "सुरक्षित और वैज्ञानिक तरीके से चर्बी घटाने के उपाय, जिससे शरीर में कमजोरी न आए।",
        "causes_en": ["Lifestyle imbalance", "High calorie liquid intake", "Late night eating", "Lack of physical movement"],
        "causes_hi": ["शारीरिक निष्क्रियता", "मीठे ड्रिंक्स पीना", "रात में देर से खाना"],
        "ayurvedic_remedies_en": ["Triphala Guggulu daily with warm water", "Ushnodaka (warm water sipping)", "Takra (spiced buttermilk) with roasted cumin after lunch"],
        "ayurvedic_remedies_hi": ["त्रिफला गुग्गुलु का सेवन", "दिनभर गुनगुना पानी पीना", "दोपहर के खाने के बाद भुने जीरे वाली छाछ पीना"],
        "home_remedies_en": ["Salad bowl 15 minutes before lunch & dinner", "10,000 steps daily", "Replace sugar with cardamom or cinnamon"],
        "home_remedies_hi": ["भोजन से 15 मिनट पहले 1 कटोरी खीरा-टमाटर का सलाद खाएं", "रोजाना 10,000 कदम चलें", "चाय में चीनी की जगह दालचीनी डालें"],
        "diet_nutrition_en": ["Portion control, 500 kcal deficit, whole grains, high fiber, high protein, zero sodas."],
        "diet_nutrition_hi": ["कम तेल-मसाले वाला खाना, हरी सब्जियां, दालें, और मीठा बिल्कुल बंद।"],
        "dos_and_donts_en": {"dos": ["Eat mindfully without TV/phone", "Drink water before meals"], "donts": ["Never skip breakfast", "Avoid instant fad diets"]},
        "dos_and_donts_hi": {"dos": ["टीवी या मोबाइल देखे बिना ध्यान से चबाकर खाएं", "भोजन से पहले पानी पिएं"], "donts": ["नाश्ता कभी न छोड़ें", "तुरंत वजन घटाने वाली दवाओं के चक्कर में न पड़ें"]},
        "when_to_see_doctor_en": "Consult a registered dietitian or doctor if you have diabetes, hypertension, or heart disease before starting new diets.",
        "when_to_see_doctor_hi": "यदि बीपी या शुगर की दवा चल रही हो तो डाइट बदलने से पहले डॉक्टर की सलाह लें।",
        "allergy_keywords": ["cumin", "buttermilk", "cinnamon"],
        "sources": "ICMR Guidelines for Healthy Weight Management"
    },
    "muscle_building": {
        "id": "muscle_building",
        "category_id": "weight",
        "category_name": "⚖️ Weight & Fitness",
        "title_en": "Muscle Building & Strength",
        "title_hi": "मांसपेशियों का निर्माण और ताकत (Muscle Building)",
        "overview_en": "Hypertrophy and musculoskeletal strengthening through progressive resistance training, adequate protein synthesis, and restorative sleep.",
        "overview_hi": "शरीर की ताकत और मांसपेशियों को मजबूत बनाना, जिससे कमजोरी दूर हो और चुस्ती-फुर्ती आए।",
        "causes_en": ["Inadequate dietary protein", "Sedentary living and muscle wasting (Sarcopenia)", "Insufficient recovery sleep"],
        "causes_hi": ["डाइट में प्रोटीन की कमी", "कसरत न करना", "नींद की कमी से रिकवरी न होना"],
        "ayurvedic_remedies_en": ["Ashwagandha Churna: 1 tsp with warm milk for muscle strength (Balya)", "Safed Musli & Shatavari for endurance", "Abhyanga with Bala Taila"],
        "ayurvedic_remedies_hi": ["अश्वगंधा चूर्ण: 1 चम्मच रात को गुनगुने दूध के साथ (मांसपेशियों को बल देता है)", "सफेद मूसली व शतावरी", "बला तैल से शरीर की मालिश"],
        "home_remedies_en": ["Boiled eggs / Paneer / Soya chunks pre and post workout", "Banana with peanut butter 30 mins before training", "Sufficient rest days between muscle groups"],
        "home_remedies_hi": ["पनीर, उबले अंडे या सोया चंक्स का सेवन", "कसरत से 30 मिनट पहले केला और पीनट बटर", "कसरत के बाद शरीर को पर्याप्त आराम"],
        "diet_nutrition_en": ["Target 1.2 to 1.6g protein per kg body weight: Paneer, sattu, lentils, eggs, chicken, Greek yogurt, almonds."],
        "diet_nutrition_hi": ["पर्याप्त प्रोटीन: पनीर, सत्तू, दालें, सोयाबीन, अंडे, दूध और बादाम।"],
        "dos_and_donts_en": {"dos": ["Progressive overload in strength exercises", "Sleep 8 hours for growth hormone release"], "donts": ["Don't overtrain without rest days", "Avoid unregulated steroid powders"]},
        "dos_and_donts_hi": {"dos": ["नियमित व्यायाम का वजन धीरे-धीरे बढ़ाएं", "8 घंटे की भरपूर नींद लें"], "donts": ["बिना डॉक्टर की सलाह के नकली सप्लीमेंट्स या स्टेरॉयड न लें", "बिना आराम के लगातार कसरत न करें"]},
        "when_to_see_doctor_en": "Consult an orthopedist or sports physician if you experience sharp joint tears, intense spine pain, or dark brown urine after workouts.",
        "when_to_see_doctor_hi": "यदि कसरत के बाद जोड़ों में तेज दर्द, नस खिंचना या पेशाब का रंग गहरा भूरा हो तो तुरंत डॉक्टर को दिखाएं।",
        "allergy_keywords": ["milk", "dairy", "peanut", "egg", "soya"],
        "sources": "ICMR Guidelines on Physical Activity & AYUSH Balya Dravyas"
    },
    "belly_fat": {
        "id": "belly_fat",
        "category_id": "weight",
        "category_name": "⚖️ Weight & Fitness",
        "title_en": "Belly Fat / Abdominal Fat",
        "title_hi": "पेट की चर्बी (Belly Fat)",
        "overview_en": "Visceral fat surrounding abdominal organs, strongly correlated with insulin resistance, non-alcoholic fatty liver, and cardiovascular events.",
        "overview_hi": "पेट और कमर के आसपास जमी चर्बी (Visceral Fat), जो फैटी लिवर और दिल की बीमारियों का बड़ा कारण बनती है।",
        "causes_en": ["Excess sugar and refined wheat flour (maida)", "High cortisol from chronic stress and poor sleep", "Alcohol intake and late night heavy dinners", "Lack of core and cardio exercise"],
        "causes_hi": ["मैदा और ज्यादा चीनी का सेवन", "तनाव से कॉर्टिसोल बढ़ना", "देर रात भारी खाना और शराब पीना", "व्यायाम न करना"],
        "ayurvedic_remedies_en": ["Guggul & Triphala daily", "Warm lemon-honey-ginger water in morning", "Takra (buttermilk) infused with roasted cumin"],
        "ayurvedic_remedies_hi": ["त्रिफला चूर्ण गुनगुने पानी के साथ", "सुबह खाली पेट गुनगुना नींबू-अदरक पानी", "भुने जीरे वाली ताजी छाछ"],
        "home_remedies_en": ["Jeera-Ajwain-Methi boiled water taken warm", "Core strengthening: Planks, Surya Namaskar", "Brisk walking 45 mins daily"],
        "home_remedies_hi": ["जीरा, अजवाइन और मेथी का उबला पानी सुबह पिएं", "रोज 10 मिनट सूर्य नमस्कार और प्लैंक", "रोजाना 45 मिनट तेज चाल में चलना"],
        "diet_nutrition_en": ["Cut refined sugar completely. Increase fiber with oats, chia seeds, vegetables. Replace white rice with millets."],
        "diet_nutrition_hi": ["मीठा बिल्कुल छोड़ें। हरी सब्जियां, दलिया, ओट्स और चिया सीड्स खाएं।"],
        "dos_and_donts_en": {"dos": ["Eat dinner 3 hours before sleeping", "Walk 1000 steps after dinner"], "donts": ["Never drink cold chilled water right after meals", "Avoid sweet sodas and alcohol"]},
        "dos_and_donts_hi": {"dos": ["सोने से 3 घंटे पहले डिनर कर लें", "खाने के बाद 15 मिनट वज्रासन में बैठें"], "donts": ["खाने के तुरंत बाद ठंडा पानी न पिएं", "शराब और मीठे ड्रिंक्स से बचें"]},
        "when_to_see_doctor_en": "Get fasting blood sugar and lipid profile tested if waist circumference exceeds 90 cm (men) or 80 cm (women) for South Asians.",
        "when_to_see_doctor_hi": "यदि पुरुषों की कमर 90 सेमी या महिलाओं की 80 सेमी से ज्यादा हो, तो शुगर और लिपिड प्रोफाइल की जांच जरूर करवाएं।",
        "allergy_keywords": ["honey", "ajwain", "cumin", "fenugreek"],
        "sources": "ICMR Guidelines on Metabolic Syndrome & AYUSH"
    },
    "lack_of_energy": {
        "id": "lack_of_energy",
        "category_id": "weight",
        "category_name": "⚖️ Weight & Fitness",
        "title_en": "Lack of Energy / Sluggishness",
        "title_hi": "ऊर्जा की कमी और सुस्ती (Lack of Energy)",
        "overview_en": "Persistent feeling of low vitality, physical heaviness, and cognitive slowness caused by poor nutrition, dehydration, and low Agni.",
        "overview_hi": "दिनभर आलस, सुस्ती और बिना काम किए भी कमजोरी महसूस होना।",
        "causes_en": ["Dehydration and electrolyte imbalance", "Iron, B12, or Vitamin D deficiency", "Heavy greasy meals causing sluggish digestion", "Lack of physical movement and sunlight"],
        "causes_hi": ["पानी की कमी", "विटामिन B12, डी और हीमोग्लोबिन की कमी", "भारी और तला-भुना खाना", "धूप और कसरत की कमी"],
        "ayurvedic_remedies_en": ["Chyawanprash: 1 tsp in the morning with warm milk (Ojas booster)", "Ashwagandha with honey", "Draksha (raisins) soaked overnight"],
        "ayurvedic_remedies_hi": ["च्यवनप्राश: सुबह 1 चम्मच गुनगुने दूध के साथ (ओजस बढ़ाता है)", "अश्वगंधा चूर्ण शहद के साथ", "रात में भीगी 10-15 मुनक्का सुबह चबाकर खाना"],
        "home_remedies_en": ["Fresh lemon water with a pinch of rock salt (Sendha Namak)", "Morning 15-minute sunlight exposure", "Green tea or herbal tulsi tea"],
        "home_remedies_hi": ["नींबू पानी में चुटकी भर सेंधा नमक डालकर पिएं", "सुबह 15 मिनट गुनगुनी धूप लें", "तुलसी और अदरक की हर्बल चाय"],
        "diet_nutrition_en": ["Dates, soaked almonds, bananas, roasted chana, seasonal fruits, and 3 liters of water."],
        "diet_nutrition_hi": ["खजूर, भीगे बादाम, केला, भुना चना और पर्याप्त पानी।"],
        "dos_and_donts_en": {"dos": ["Take short walking breaks every hour", "Maintain consistent sleep-wake times"], "donts": ["Avoid relying on multiple sugary cups of coffee", "Avoid heavy afternoon meals"]},
        "dos_and_donts_hi": {"dos": ["हर घंटे 2 मिनट उठकर टहलें", "सोने और जागने का समय निश्चित रखें"], "donts": ["सुस्ती भगाने के लिए बार-बार मीठी चाय या कॉफी न पिएं", "दोपहर में बहुत भारी खाना न खाएं"]},
        "when_to_see_doctor_en": "Seek medical review if sluggishness is accompanied by dizziness, shortness of breath, or pale skin (check CBC, Thyroid, B12).",
        "when_to_see_doctor_hi": "अगर सुस्ती के साथ चक्कर आएं, दिल की धड़कन तेज हो या सांस फूले तो सीबीसी (खून) और थायराइड टेस्ट करवाएं।",
        "allergy_keywords": ["milk", "dairy", "almond", "raisins"],
        "sources": "ICMR Guidelines on Fatigue and Micronutrients & AYUSH"
    },
    "poor_fitness": {
        "id": "poor_fitness",
        "category_id": "weight",
        "category_name": "⚖️ Weight & Fitness",
        "title_en": "Poor Fitness Level",
        "title_hi": "कम शारीरिक सहनशक्ति (Poor Fitness Level)",
        "overview_en": "Low cardiovascular stamina, reduced muscular endurance, and quick breathlessness during routine daily activities like climbing stairs.",
        "overview_hi": "सीढ़ियां चढ़ने या थोड़ा चलने पर ही सांस फूलना और जल्दी थक जाना।",
        "causes_en": ["Prolonged sedentary screen habits", "Low lung capacity from lack of aerobic activity", "Anemia and low muscle tone"],
        "causes_hi": ["लगातार बैठकर काम करना", "कसरत न करने से फेफड़ों की क्षमता कम होना", "खून की कमी"],
        "ayurvedic_remedies_en": ["Pranayama (Anulom Vilom & Bhastrika) daily for 15 mins", "Ashwagandha Rasayana for endurance", "Abhyanga with sesame oil"],
        "ayurvedic_remedies_hi": ["रोजाना 15 मिनट अनुलोम-विलोम और भस्त्रिका प्राणायाम", "अश्वगंधा रसायन का सेवन", "तिल तेल से शरीर की मालिश"],
        "home_remedies_en": ["Start with brisk 20-minute daily walk and gradually increase by 5 mins each week", "Take stairs instead of elevators", "Deep belly breathing"],
        "home_remedies_hi": ["रोजाना 20 मिनट तेज टहलने से शुरुआत करें", "लिफ्ट की जगह सीढ़ियों का प्रयोग करें", "गहरी सांस लेने का अभ्यास"],
        "diet_nutrition_en": ["Iron rich foods (spinach, beetroot, pomegranate), complex carbs (dalia, oats), and protein."],
        "diet_nutrition_hi": ["पालक, चुकंदर, अनार, दलिया और प्रोटीन युक्त दालें।"],
        "dos_and_donts_en": {"dos": ["Consistency over intensity: Exercise 5 days a week", "Stay hydrated"], "donts": ["Don't jump straight into high-intensity exercise without warming up", "Avoid smoking"]},
        "dos_and_donts_hi": {"dos": ["नियमितता जरूरी है: हफ्ते में कम से कम 5 दिन व्यायाम करें", "खूब पानी पिएं"], "donts": ["बिना वार्म-अप किए अचानक भारी कसरत न करें", "बीड़ी-सिगरेट से बचें"]},
        "when_to_see_doctor_en": "Consult a cardiologist immediately if breathlessness is accompanied by chest tightness, radiating jaw pain, or fainting.",
        "when_to_see_doctor_hi": "यदि सांस फूलने के साथ सीने में जकड़न, पसीना या बाएं हाथ में दर्द हो तो तुरंत आपातकालीन डॉक्टर से मिलें।",
        "allergy_keywords": ["sesame"],
        "sources": "WHO Physical Activity Guidelines & ICMR"
    },
    "body_toning": {
        "id": "body_toning",
        "category_id": "weight",
        "category_name": "⚖️ Weight & Fitness",
        "title_en": "Body Toning",
        "title_hi": "शरीर को सुडौल बनाना (Body Toning)",
        "overview_en": "Achieving balanced muscular definition and reducing subcutaneous body fat percentage while preserving functional strength.",
        "overview_hi": "शरीर की ढीली चर्बी को कम करके मांसपेशियों को सुडौल और आकर्षक बनाना।",
        "causes_en": ["Low muscle-to-fat ratio", "Sedentary lifestyle", "High carbohydrate and low protein intake"],
        "causes_hi": ["मांसपेशियों का ढीला होना", "कसरत न करना", "ज्यादा कार्बोहाइड्रेट और कम प्रोटीन खाना"],
        "ayurvedic_remedies_en": ["Surya Namaskar 12 rounds daily (complete body toning)", "Bala Ashwagandha Taila massage", "Triphala water"],
        "ayurvedic_remedies_hi": ["रोजाना 12 चक्र सूर्य नमस्कार (पूरे शरीर को टोन करता है)", "बला-अश्वगंधा तेल से मालिश", "त्रिफला पानी का सेवन"],
        "home_remedies_en": ["Bodyweight exercises: Push-ups, squats, lunges, and planks", "Skipping rope for 10 mins", "Yoga asanas"],
        "home_remedies_hi": ["घर पर कसरत: पुश-अप्स, उठक-बैठक (स्क्वैट्स) और प्लैंक", "रस्सी कूदना 10 मिनट", "योगासन का अभ्यास"],
        "diet_nutrition_en": ["Lean protein (paneer, dal, soya, eggs), roasted makhana, sprouts, and 3L water. Cut sugar."],
        "diet_nutrition_hi": ["पनीर, स्प्राउट्स, मखाना, दालें और 3 लीटर पानी। चीनी छोड़ें।"],
        "dos_and_donts_en": {"dos": ["Focus on full-body functional exercises", "Sleep 7-8 hours for muscle repair"], "donts": ["Avoid spot-reduction myths (fat is lost systemically)", "Avoid starvation"]},
        "dos_and_donts_hi": {"dos": ["पूरे शरीर की कसरत पर ध्यान दें", "7-8 घंटे सोएं ताकि मांसपेशियां रिकवर हों"], "donts": ["केवल पेट या किसी एक अंग की चर्बी घटाने के बहकावे में न आएं", "भूखे न रहें"]},
        "when_to_see_doctor_en": "Consult a physiotherapist if you experience chronic tendonitis or joint strain during workouts.",
        "when_to_see_doctor_hi": "कसरत के दौरान जोड़ों या लिगामेंट में खिंचाव या तेज दर्द हो तो फिजियोथेरेपिस्ट से मिलें।",
        "allergy_keywords": ["soya", "dairy", "egg"],
        "sources": "ICMR Guidelines on Fitness & AYUSH Yoga Protocols"
    },

    # ==========================================
    # CATEGORY 4: 🍽️ Digestive Issues (10 issues)
    # ==========================================
    "constipation": {
        "id": "constipation",
        "category_id": "digestion",
        "category_name": "🍽️ Digestive Issues",
        "title_en": "Constipation",
        "title_hi": "कब्ज (Constipation)",
        "overview_en": "Infrequent bowel movements (fewer than 3 times a week), hard stools, and painful straining during defecation caused by sluggish intestinal transit.",
        "overview_hi": "सप्ताह में 3 बार से कम मल त्याग, मल का कठोर होना और पेट साफ न होने की समस्या।",
        "causes_en": ["Low dietary fiber intake", "Insufficient hydration (<2 liters daily)", "Sedentary lifestyle and lack of abdominal movement", "Suppressing natural defecation urge (Vega Dharana)", "Side effect of iron or calcium supplements"],
        "causes_hi": ["भोजन में फाइबर (रफेज) की भारी कमी", "दिनभर में कम पानी पीना", "शारीरिक निष्क्रियता और लगातार बैठे रहना", "मल त्याग के वेग को रोकना", "आयरन या कैल्शियम की गोलियों का प्रभाव"],
        "ayurvedic_remedies_en": [
            "Triphala Churna: 1 tsp with lukewarm water or warm milk 30 minutes before bed (Anulomana therapy).",
            "Castor Oil (Erand Taila): 1 tsp in warm milk once a week for stubborn constipation (under guidance).",
            "Isabgol (Psyllium Husk): 1-2 tbsp soaked in warm water or milk for 10 minutes before bed.",
            "Haritaki (Chebulic Myrobalan): Mild laxative that cleanses colon without dependency."
        ],
        "ayurvedic_remedies_hi": [
            "त्रिफला चूर्ण: रात को सोने से पहले 1 चम्मच गुनगुने पानी या दूध के साथ लें (आंतों की सफाई करता है)।",
            "इसबगोल की भूसी: 1-2 चम्मच गुनगुने पानी या दूध में 10 मिनट भिगोकर पिएं।",
            "एरंड तेल (कैस्टर ऑयल): 1 चम्मच गुनगुने दूध में मिलाकर सप्ताह में एक बार जिद्दी कब्ज के लिए लें।",
            "हरड़ (हरीतकी): आंतों को प्राकृतिक रूप से गतिमान करने वाली उत्तम औषधि।"
        ],
        "home_remedies_en": [
            "Drink 2 glasses of warm water on an empty stomach immediately upon waking (Ushapan).",
            "Soak 4-5 dried figs (Anjeer) and black raisins (Munakka) in water overnight; consume in the morning.",
            "Eat a bowl of ripe papaya or guava with seeds daily as an afternoon snack.",
            "Flaxseed powder: 1 tbsp mixed in warm water with dinner."
        ],
        "home_remedies_hi": [
            "उषापान: सुबह उठते ही बासी मुंह 2 गिलास गुनगुना पानी पिएं।",
            "अंजीर और मुनक्का: 4-5 मुनक्का और 2 अंजीर रात को भिगोकर सुबह चबाकर खाएं और पानी पिएं।",
            "पका पपीता या अमरूद: दोपहर में पपीता या बीजों सहित पका अमरूद खाएं।",
            "अलसी का चूर्ण: 1 चम्मच गुनगुने पानी के साथ रात के खाने के बाद लें।"
        ],
        "diet_nutrition_en": [
            "Fiber-rich foods: Whole wheat, oats, dalia, green leafy vegetables, carrots, and apples with skin.",
            "Hydration: Minimum 3 liters of warm or room-temperature water daily.",
            "Healthy fats: 1 tsp pure cow ghee with warm dinner helps lubricate the dry colon (Sneha).",
            "Avoid: White refined flour (maida), fast food, bakery goods, and excessive black tea."
        ],
        "diet_nutrition_hi": [
            "फाइबर युक्त भोजन: दलिया, ओट्स, चोकरदार रोटी, हरी सब्जियां, गाजर और सेब छिलके सहित।",
            "पर्याप्त जलपान: दिनभर में 3 लीटर गुनगुना या ताजा पानी पिएं।",
            "शुद्ध गाय का घी: रात के भोजन में 1 चम्मच देसी घी आंतों में चिकनाई लाता है।",
            "परहेज: मैदा, बिस्कुट, जंक फूड, समोसा और ज्यादा कड़क चाय से बचें।"
        ],
        "dos_and_donts_en": {
            "dos": ["Fix a dedicated morning toilet timing", "Practice Malasana (Squatting pose) and Pawanmuktasana", "Walk for 15 minutes after dinner"],
            "donts": ["Do not delay or suppress the urge to use the restroom", "Avoid overuse of harsh chemical laxatives", "Avoid eating dry, cold food"]
        },
        "dos_and_donts_hi": {
            "dos": ["शौच का एक निश्चित समय बनाएं", "मलासन और पवनमुक्तासन का नियमित अभ्यास करें", "रात के खाने के बाद 15 मिनट वज्रासन या वॉक करें"],
            "donts": ["शौच का वेग कभी न रोकें", "दवा की दुकानों से मिलने वाले तेज जुलाब की आदत न डालें", "सूखा और बासी खाना न खाएं"]
        },
        "when_to_see_doctor_en": "Consult a doctor immediately if constipation lasts >2 weeks despite diet changes, or if accompanied by rectal bleeding, intense abdominal pain, unexplained weight loss, or vomiting.",
        "when_to_see_doctor_hi": "यदि 2 हफ्ते से पेट साफ न हो, मल में खून आए, पेट में असहनीय दर्द हो, उल्टी हो या वजन तेजी से घटे तो तुरंत डॉक्टर से मिलें।",
        "allergy_keywords": ["milk", "dairy", "psyllium", "fig", "flaxseed"],
        "sources": "Ministry of AYUSH Ayurvedic Pharmacopoeia & ICMR Guidelines on Dietary Fiber"
    },
    "bloating_gas": {
        "id": "bloating_gas",
        "category_id": "digestion",
        "category_name": "🍽️ Digestive Issues",
        "title_en": "Bloating / Gas (Adhmana)",
        "title_hi": "पेट फूलना और गैस (Bloating & Gas)",
        "overview_en": "Accumulation of intestinal gas causing abdominal distension, tightness, gurgling noises, and flatulence caused by weak digestive fire (Manda Agni).",
        "overview_hi": "पेट में गैस बनना, पेट का फूलना, भारीपन और डकारें आना जो कमजोर पाचन क्रिया (अग्निमांद्य) का संकेत है।",
        "causes_en": ["Eating too fast and swallowing air (aerophagia)", "Heavy, hard-to-digest legumes without digestive spices", "Carbonated beverages and artificial sweeteners", "Lactose or gluten intolerance", "Chronic stress disrupting gut motility"],
        "causes_hi": ["जल्दबाजी में बिना चबाए खाना खाना", "राजमा, छोले या उड़द दाल बिना हींग/अजवाइन के पकाना", "कोल्ड ड्रिंक और सोडा पीना", "दूध या गेहूं से पाचन में एलर्जी", "तनाव से पाचन धीमा होना"],
        "ayurvedic_remedies_en": [
            "Hingwashtak Churna: 1/2 tsp mixed with the first bite of warm rice and 1/2 tsp ghee.",
            "Lavan Bhaskar Churna: 1/2 tsp with warm water or buttermilk after meals.",
            "Jeera-Ajwain Ark: Sip water boiled with cumin and carom seeds throughout the day.",
            "Trikatu Churna (Sunthi, Maricha, Pippali): Pinch with honey before heavy meals to rekindle Agni."
        ],
        "ayurvedic_remedies_hi": [
            "हिंग्वाष्टक चूर्ण: भोजन के पहले कौर में आधा चम्मच घी के साथ लें (गैस तुरंत शांत होती है)।",
            "लवण भास्कर चूर्ण: भोजन के बाद आधा चम्मच छाछ या गुनगुने पानी के साथ लें।",
            "जीरा-अजवाइन का काढ़ा: पानी में जीरा और अजवाइन उबालकर दिनभर गुनगुना पिएं।",
            "त्रिकटु चूर्ण: चुटकी भर त्रिकटु शहद के साथ भोजन से पहले लें ताकि जठराग्नि तेज हो।"
        ],
        "home_remedies_en": [
            "Chew 1/2 tsp roasted Ajwain (carom seeds) with a pinch of rock salt (Kala Namak) and swallow with warm water.",
            "Fresh Ginger Tea: Boil crushed ginger in water with a few drops of lemon juice after heavy meals.",
            "Chew a few Fennel seeds (Saunf) after every meal.",
            "Warm compress: Place a hot water bottle on the abdomen for 10 minutes to release trapped gas."
        ],
        "home_remedies_hi": [
            "भुनी अजवाइन और काला नमक: आधा चम्मच अजवाइन और चुटकी भर काला नमक चबाकर गुनगुना पानी पिएं।",
            "अदरक का पानी: ताजी अदरक को पानी में उबालकर भोजन के बाद घूंट-घूंट पिएं।",
            "भोजन के बाद सौंफ चबाना: सौंफ पाचक एंजाइमों को उत्तेजित करती है।",
            "पेट पर गर्म पानी की सिकाई: गैस की ऐंठन से तुरंत आराम मिलता है।"
        ],
        "diet_nutrition_en": [
            "Always cook lentils with ginger, cumin, and hing (asafetida).",
            "Drink fresh buttermilk (Takra) churned with roasted cumin and mint.",
            "Eat light, warm, freshly prepared meals; avoid cold salads, ice water, and reheating stale food.",
            "Limit cruciferous vegetables (raw cabbage, cauliflower, broccoli) if prone to bloating."
        ],
        "diet_nutrition_hi": [
            "दालों में हमेशा हींग, जीरा और अदरक का तड़का लगाएं।",
            "ताजी छाछ में भुना जीरा, पुदीना और काला नमक डालकर दोपहर में पिएं।",
            "ताजा, गर्म और सुपाच्य भोजन करें; फ्रिज का ठंडा पानी और बासी खाना बंद करें।",
            "कच्ची पत्तागोभी, फूलगोभी का सेवन कम करें।"
        ],
        "dos_and_donts_en": {
            "dos": ["Chew each bite slowly with mouth closed", "Sit in Vajrasana for 10 minutes after lunch and dinner", "Eat at consistent times daily"],
            "donts": ["Do not drink large quantities of water during or immediately after meals", "Avoid chewing gum and drinking with straws", "Avoid carbonated beverages"]
        },
        "dos_and_donts_hi": {
            "dos": ["भोजन को धीरे-धीरे और अच्छी तरह चबाकर खाएं", "खाने के बाद 10 मिनट वज्रासन में बैठें", "नियत समय पर भोजन करें"],
            "donts": ["खाना खाते समय या तुरंत बाद ज्यादा पानी न पिएं", "च्युइंग गम और स्ट्रॉ से पीने से बचें", "सोडा व कोल्ड ड्रिंक न पिएं"]
        },
        "when_to_see_doctor_en": "Consult a gastroenterologist if bloating is severe and accompanied by persistent severe cramps, unexplained weight loss, fever, or blood in stool.",
        "when_to_see_doctor_hi": "यदि पेट फूलने के साथ तेज चुभन वाला दर्द हो, वजन लगातार घटे, तेज बुखार हो या मल में खून दिखे तो तुरंत विशेषज्ञ से परामर्श लें।",
        "allergy_keywords": ["ajwain", "cumin", "ginger", "asafetida", "dairy", "buttermilk"],
        "sources": "National Health Portal (NHP India) & Ministry of AYUSH Guidelines"
    },
    "acidity_gerd": {
        "id": "acidity_gerd",
        "category_id": "digestion",
        "category_name": "🍽️ Digestive Issues",
        "title_en": "Acidity / GERD (Amlapitta)",
        "title_hi": "एसिडिटी और सीने में जलन (Acidity & Acid Reflux)",
        "overview_en": "Excess stomach acid flowing back into the esophagus, causing burning sensation behind the breastbone (heartburn), sour belching, and throat irritation.",
        "overview_hi": "पेट में अतिरिक्त अम्ल (तेजाब) का बनना, जिससे सीने में जलन, खट्टी डकारें और गले में तीखापन महसूस होता है।",
        "causes_en": ["Spicy, oily, deep-fried, and heavily processed food", "Excessive tea, coffee, alcohol, or tobacco consumption", "Eating late at night and lying down immediately", "Chronic mental stress causing acid hypersecretion", "Skipping breakfast and irregular meal timings"],
        "causes_hi": ["ज्यादा मिर्च-मसालेदार और तला-भुना खाना", "अत्यधिक चाय, कॉफी, तंबाकू या सिगरेट", "देर रात खाना खाकर तुरंत सो जाना", "मानसिक तनाव व चिंता", "नाश्ता न करना और लंबे समय तक भूखे रहना"],
        "ayurvedic_remedies_en": [
            "Avipattikar Churna: 1 tsp with cool water before meals (the premier Ayurvedic Pitta pacifier).",
            "Yashtimadhu (Licorice / Mulethi): 1/2 tsp powder in warm water forms a soothing mucosal coating.",
            "Shatavari Churna: 1/2 tsp with cold milk to neutralize excess digestive acid.",
            "Kamdudha Ras or Praval Pishti: Classical calcium-rich Ayurvedic antacids under doctor supervision."
        ],
        "ayurvedic_remedies_hi": [
            "अविपत्तिकर चूर्ण: भोजन से पहले 1 चम्मच ताजे पानी के साथ लें (पित्त और तेजाब को शांत करता है)।",
            "मुलेठी चूर्ण (यष्टिमधु): आधा चम्मच मुलेठी पाउडर गुनगुने पानी में घोलकर पिएं, यह पेट की अंदरूनी परत को ठंडक देता है।",
            "शतावरी चूर्ण: आधा चम्मच ठंडे दूध के साथ एसिडिटी शांत करने में उपयोगी है।",
            "प्रवाल पिष्टी या कामदुधा रस: आयुर्वेदिक डॉक्टर के परामर्श से ली जाने वाली सौम्य भस्म।"
        ],
        "home_remedies_en": [
            "Cold Milk: Sip 1/2 cup of cold unboiled milk slowly when burning occurs.",
            "Fennel (Saunf) & Mishri Water: Soak 1 tbsp crushed fennel seeds in water, strain, and sip.",
            "Fresh Coconut Water: Naturally alkaline, cools the stomach instantly.",
            "Chew 4-5 fresh Basil (Tulsi) leaves to stimulate mucin production in the stomach."
        ],
        "home_remedies_hi": [
            "ठंडा दूध: जलन होने पर आधा कप ठंडा दूध घूंट-घूंट करके पिएं।",
            "सौंफ और मिश्री का पानी: 1 चम्मच सौंफ को पानी में भिगोकर छान लें और मिश्री मिलाकर पिएं।",
            "नारियल पानी: पेट की जलन को तुरंत शांत करने वाला प्राकृतिक क्षारीय पेय।",
            "तुलसी के पत्ते: 4-5 तुलसी की पत्तियां चबाने से पेट में एसिड शांत होता है।"
        ],
        "diet_nutrition_en": [
            "Alkaline fruits: Bananas, ripe sweet melons, watermelon, papaya, and sweet apples.",
            "Grains: Oats, puffed rice (murmura), and barley (jau).",
            "Vegetables: Cucumber, bottle gourd (lauki), ridge gourd (turai), and pumpkin.",
            "Avoid: Citrus fruits (lemons, oranges on empty stomach), vinegar, pickles, black pepper, and dark chocolate."
        ],
        "diet_nutrition_hi": [
            "शीतल फल: केला, पपीता, तरबूज, खरबूजा और मीठा सेब खाएं।",
            "अनाज: दलिया, ओट्स, मुरमुरा और जौ का सत्तू।",
            "सब्जियां: लौकी, तोरी, कद्दू और खीरा अत्यंत लाभकारी हैं।",
            "परहेज: खाली पेट खट्टे फल, सिरका, अचार, तीखी लाल मिर्च और चॉकलेट।"
        ],
        "dos_and_donts_en": {
            "dos": ["Keep a gap of at least 2.5 to 3 hours between dinner and sleeping", "Elevate the head of your bed by 6 inches", "Eat small, frequent meals rather than 2 giant feasts"],
            "donts": ["Do not lie down immediately after eating", "Avoid tight belts or waistbands around the abdomen", "Avoid smoking and caffeine"]
        },
        "dos_and_donts_hi": {
            "dos": ["रात के खाने और सोने के बीच कम से कम 2.5-3 घंटे का अंतर रखें", "सोते समय सिर को 6 इंच ऊंचा रखें", "एक बार में बहुत ज्यादा खाने की जगह थोड़ा-थोड़ा खाएं"],
            "donts": ["खाना खाने के तुरंत बाद बिस्तर पर न लेटें", "पेट पर बहुत तंग बेल्ट न बांधें", "सिगरेट, तंबाकू और ज्यादा चाय से दूर रहें"]
        },
        "when_to_see_doctor_en": "CRITICAL RED FLAG: Seek immediate medical care if chest pain radiates to the left arm, neck, or jaw, or is accompanied by cold sweats (rule out myocardial infarction / heart attack). Also see a doctor for vomiting blood or difficulty swallowing.",
        "when_to_see_doctor_hi": "आपातकालीन चेतावनी: यदि सीने में दर्द बाएं हाथ, गर्दन या जबड़े में फैले, साथ में पसीना या घबराहट हो तो इसे दिल का दौरा समझकर तुरंत अस्पताल जाएं। उल्टी में खून आने पर भी तुरंत डॉक्टर को दिखाएं।",
        "allergy_keywords": ["milk", "dairy", "licorice", "fennel", "coconut"],
        "sources": "National Health Portal (NHP India) & ICMR Clinical Guidelines on GERD"
    },
    "indigestion": {
        "id": "indigestion",
        "category_id": "digestion",
        "category_name": "🍽️ Digestive Issues",
        "title_en": "Indigestion (Ajeerna / Dyspepsia)",
        "title_hi": "बदहजमी और अपच (Indigestion)",
        "overview_en": "Impaired digestion characterized by discomfort in the upper abdomen, feeling uncomfortably full too soon, nausea, and sour burps.",
        "overview_hi": "खाना ठीक से न पचना, पेट के ऊपरी हिस्से में भारीपन, खट्टी डकारें और जी मिचलाना।",
        "causes_en": ["Eating before the previous meal is completely digested", "Overeating or eating under emotional stress", "Heavy, greasy, oily, and stale foods", "Lack of physical activity after meals"],
        "causes_hi": ["पिछला भोजन पचे बिना दोबारा खा लेना", "तनाव में या जरूरत से ज्यादा खाना", "बासी, भारी और गरिष्ठ भोजन", "भोजन के बाद बिल्कुल न हिलना-डुलना"],
        "ayurvedic_remedies_en": [
            "Shankh Vati or Chitrakadi Vati: Classical digestives to rekindle sluggish gastric fire.",
            "Fresh Ginger-Lemon Shorba: 1 tsp fresh ginger juice + 1/2 tsp lemon juice + pinch of rock salt 10 mins before meals.",
            "Short Fasting (Langhana): Skip one meal or consume only light moong dal soup to allow digestive fire to recover."
        ],
        "ayurvedic_remedies_hi": [
            "चित्रकादि वटी या शंख वटी: कमजोर जठराग्नि को तेज करने वाली प्रमुख आयुर्वेदिक औषधि।",
            "अदरक-नींबू रस: भोजन से 10 मिनट पहले अदरक का रस, नींबू और चुटकी भर सेंधा नमक चाटें।",
            "लंघन (उपवास): एक समय का खाना छोड़कर केवल मूंग दाल का पानी पिएं ताकि आंतों को विश्राम मिले।"
        ],
        "home_remedies_en": [
            "Sip warm water every 30 minutes to facilitate enzymatic breakdown.",
            "Coriander & Cumin Decoction: Boil 1 tsp coriander seeds and 1 tsp cumin seeds; drink warm.",
            "Pomegranate Juice with black pepper and rock salt."
        ],
        "home_remedies_hi": [
            "दिनभर में घूंट-घूंट करके गुनगुना पानी पिएं।",
            "धनिया-जीरा काढ़ा: एक चम्मच धनिया और जीरा पानी में उबालकर गुनगुना पिएं।",
            "अनार के दाने काले नमक और काली मिर्च के साथ चबाएं।"
        ],
        "diet_nutrition_en": ["Light foods: Moong dal khichdi, thin vegetable soup, steamed rice with boiled vegetables. Avoid cheese, paneer, and sweets until digestion recovers."],
        "diet_nutrition_hi": ["हल्का भोजन: मूंग दाल की पतली खिचड़ी, दलिया, सब्जियों का सूप। ठीक होने तक पनीर, मिठाई और तेल-घी से बचें।"],
        "dos_and_donts_en": {"dos": ["Eat only when truly hungry", "Sit in Vajrasana after eating"], "donts": ["Do not eat heavy snacks between meals", "Do not sleep during daytime after lunch"]},
        "dos_and_donts_hi": {"dos": ["तभी खाएं जब तेज भूख लगे", "भोजन के बाद 10 मिनट वज्रासन में बैठें"], "donts": ["दिनभर थोड़ा-थोड़ा कुछ न कुछ खाने की आदत छोड़ें", "दोपहर में खाना खाकर तुरंत न सोएं"]},
        "when_to_see_doctor_en": "See a doctor if indigestion persists >10 days, causes rapid involuntary weight loss, or is accompanied by persistent vomiting.",
        "when_to_see_doctor_hi": "यदि बदहजमी 10 दिन से ज्यादा रहे, बार-बार उल्टी हो या वजन तेजी से घटे तो डॉक्टर से जांच करवाएं।",
        "allergy_keywords": ["ginger", "lemon", "cumin", "coriander"],
        "sources": "Ministry of AYUSH Agni-Deepana Protocol & NHP India"
    },
    "stomach_cramps": {
        "id": "stomach_cramps",
        "category_id": "digestion",
        "category_name": "🍽️ Digestive Issues",
        "title_en": "Stomach Cramps (Abdominal Spasms)",
        "title_hi": "पेट में मरोड़ और ऐंठन (Stomach Cramps)",
        "overview_en": "Painful spasmodic contractions of smooth intestinal muscles, often associated with gas, mild viral gastroenteritis, or dietary indiscretion.",
        "overview_hi": "पेट की मांसपेशियों में अचानक खिंचाव, ऐंठन और मरोड़ उठना, जो गैस, पेट के संक्रमण या गलत खानपान से होता है।",
        "causes_en": ["Trapped gas bubbles causing bowel wall distension", "Mild food poisoning or gastroenteritis", "Dehydration and electrolyte imbalance", "Menstrual cramping (referred to abdomen)", "Sudden ingestion of freezing cold beverages"],
        "causes_hi": ["पेट में फंसी गैस से आंतों का खिंचाव", "बासी या दूषित खाना (फूड पॉइजनिंग)", "पानी और इलेक्ट्रोलाइट्स की कमी", "पीरियड्स का दर्द", "अचानक बहुत ठंडा पानी या बर्फ खाना"],
        "ayurvedic_remedies_en": [
            "Bilwadi Churna: 1/2 tsp with warm water to settle hyperactive gut motility and spasmodic pain.",
            "Ajwain & Hing Ark: 1 tsp carom seed distillate or infusion with pinch of rock salt.",
            "Warm Sesame Oil compress: Gentle clockwise circular massage on the belly followed by a warm towel."
        ],
        "ayurvedic_remedies_hi": [
            "बिल्वादि चूर्ण: आधा चम्मच गुनगुने पानी के साथ आंतों के मरोड़ को शांत करता है।",
            "अजवाइन और हींग का पानी: चुटकी भर हींग और अजवाइन का काढ़ा पेट दर्द में तुरंत असरदार है।",
            "तिल तेल की मालिश: पेट पर गुनगुने तिल के तेल से हल्के हाथ से क्लॉकवाइज मालिश करें।"
        ],
        "home_remedies_en": [
            "Hot water bag applied to the abdomen for 15-20 minutes relaxes smooth muscle spasms.",
            "Warm Chamomile or Peppermint tea provides antispasmodic menthol compounds.",
            "ORS or coconut water with a pinch of salt to restore fluid balance."
        ],
        "home_remedies_hi": [
            "गर्म पानी की बोतल (हॉट वॉटर बैग) से पेट की सिकाई मांसपेशियों की ऐंठन खोलती है।",
            "पुदीने या कैमोमाइल की हल्की चाय पिएं।",
            "ओआरएस (ORS) या नारियल पानी में चुटकी भर नमक डालकर घूंट-घूंट पिएं।"
        ],
        "diet_nutrition_en": ["BRAT diet (Banana, Rice, Applesauce, Toast). Clear vegetable broths. Strictly avoid milk, greasy curries, and spicy gravies."],
        "diet_nutrition_hi": ["केला, उबले चावल, सेब और मूंग दाल का पानी। दूध, मसालेदार और तली हुई चीजें बंद रखें।"],
        "dos_and_donts_en": {"dos": ["Rest in a fetal curled position if it provides comfort", "Stay hydrated with warm fluids"], "donts": ["Do not take NSAID pain pills (like ibuprofen) without doctor advice as they irritate stomach lining", "Do not eat heavy solids"]},
        "dos_and_donts_hi": {"dos": ["घुटने मोड़कर करवट से लेटें", "गुनगुना पानी व ओआरएस पिएं"], "donts": ["बिना डॉक्टर पूछे पेनकिलर (जैसे ब्रूफेन) न खाएं, यह पेट की परत छील सकती है", "भारी खाना न खाएं"]},
        "when_to_see_doctor_en": "EMERGENCY: Seek emergency hospital care if pain shifts to lower-right abdomen (Appendicitis risk), abdomen is rigid like a board, or there is high fever and continuous vomiting.",
        "when_to_see_doctor_hi": "आपातकालीन चेतावनी: यदि दर्द पेट के निचले दाहिने हिस्से में चला जाए (अपेंडिक्स का खतरा), पेट छूने पर पत्थर जैसा कड़ा लगे, या तेज बुखार हो तो तुरंत आपातकालीन अस्पताल जाएं।",
        "allergy_keywords": ["ajwain", "peppermint", "sesame"],
        "sources": "ICMR Emergency Clinical Guidelines & AYUSH Gastro Care"
    },
    "poor_appetite": {
        "id": "poor_appetite",
        "category_id": "digestion",
        "category_name": "🍽️ Digestive Issues",
        "title_en": "Poor Appetite (Aruchi / Low Agni)",
        "title_hi": "भूख न लगना (Poor Appetite)",
        "overview_en": "Loss of desire to eat or early satiety, often following a viral illness, chronic stress, or inactive lifestyle causing diminished gastric secretions.",
        "overview_hi": "खाने की इच्छा न होना, थोड़ा खाने पर ही पेट भर जाना और भोजन में कोई स्वाद न आना।",
        "causes_en": ["Sluggish metabolism (Manda Agni)", "Post-viral illness recovery (after dengue, malaria, fever)", "Chronic psychological anxiety or depression", "Zinc or B-complex vitamin deficiency", "Smoking and tobacco use"],
        "causes_hi": ["जठराग्नि की कमजोरी", "वायरल बुखार या बीमारी के बाद कमजोरी", "मानसिक तनाव और डिप्रेशन", "जिंक या विटामिन बी-कॉम्प्लेक्स की कमी", "तंबाकू व सिगरेट"],
        "ayurvedic_remedies_en": [
            "Draksharishta: 15 ml with equal water after lunch to enhance appetite and nourish blood.",
            "Trikatu with honey: 1/4 tsp Trikatu churna mixed with raw honey 15 mins before meals.",
            "Pippalyasava: Classical fermented tonic to stimulate digestive enzymes."
        ],
        "ayurvedic_remedies_hi": [
            "द्राक्षारिष्ट: 15 मिली बराबर पानी मिलाकर भोजन के बाद लें (भूख और खून दोनों बढ़ाता है)।",
            "त्रिकटु और शहद: चुटकी भर त्रिकटु शहद के साथ चाटने से जीभ का स्वाद और भूख खुलती है।",
            "पिप्पल्यासव: पाचक रस बढ़ाने वाली प्रसिद्ध आयुर्वेदिक औषधि।"
        ],
        "home_remedies_en": [
            "Slice fresh ginger into thin strips, dip in fresh lemon juice and rock salt; chew 2-3 strips before lunch.",
            "Fresh pomegranate juice with a pinch of roasted cumin and black salt.",
            "Sip warm water infused with mint and black pepper."
        ],
        "home_remedies_hi": [
            "अदरक के लच्छों में नींबू का रस और सेंधा नमक मिलाकर खाना खाने से 10 मिनट पहले चबाएं।",
            "अनार के ताजे रस में भुना जीरा और काला नमक डालकर पिएं।",
            "पुदीना और काली मिर्च का गुनगुना काढ़ा लें।"
        ],
        "diet_nutrition_en": ["Eat visually appealing, warm, well-seasoned dishes. Sprouted lentils, fresh fruit chaat, buttermilk with roasted spices."],
        "diet_nutrition_hi": ["स्वादिष्ट, गर्म और सुपाच्य भोजन लें। अंकुरित मूंग, फलों की चाट, भुने मसालों वाली छाछ।"],
        "dos_and_donts_en": {"dos": ["Exercise or walk outdoors in morning sunlight to naturally trigger hunger hormones", "Eat in pleasant company"], "donts": ["Do not force-feed heavy meals", "Avoid constant snacking on junk between meals"]},
        "dos_and_donts_hi": {"dos": ["सुबह धूप में टहलें और कसरत करें ताकि प्राकृतिक भूख लगे", "शांत माहौल में खाएं"], "donts": ["जबरदस्ती भारी खाना न ठूंसें", "दिनभर बिस्कुट-नमकीन चरने से बचें"]},
        "when_to_see_doctor_en": "Consult a doctor if appetite loss causes significant unintentional weight loss, or is accompanied by persistent fever, pale skin, or jaundice.",
        "when_to_see_doctor_hi": "यदि भूख न लगने से वजन लगातार घट रहा हो, आंखें पीली हों (पीलिया) या लंबे समय से हल्का बुखार हो तो डॉक्टर से जांच कराएं।",
        "allergy_keywords": ["ginger", "honey", "pomegranate", "cumin"],
        "sources": "National Health Portal (NHP India) & Ministry of AYUSH Protocols"
    },
    "overeating_habits": {
        "id": "overeating_habits",
        "category_id": "digestion",
        "category_name": "🍽️ Digestive Issues",
        "title_en": "Overeating Habits & Food Cravings",
        "title_hi": "ज्यादा खाने की आदत और क्रेविंग्स (Overeating)",
        "overview_en": "Consuming food beyond physiological fullness, driven by stress, dopamine-seeking habits, screen distractions, or refined sugar spikes.",
        "overview_hi": "भूख न होने पर भी बार-बार खाना, टीवी/मोबाइल देखते हुए ज्यादा खा लेना और मीठे या जंक की तीव्र इच्छा।",
        "causes_en": ["Eating while distracted by screens (mindless eating)", "Sugar and simple-carb spikes followed by insulin crashes", "Emotional eating (eating to numb stress or loneliness)", "Lack of sufficient protein and fiber in meals"],
        "causes_hi": ["मोबाइल या टीवी देखते हुए खाना खाना", "मीठी चीजों से ब्लड शुगर का तेजी से गिरना", "तनाव, बोरियत या अकेलेपन में खाना", "भोजन में प्रोटीन और फाइबर की कमी"],
        "ayurvedic_remedies_en": [
            "Mitahara Principle (AYUSH): Fill 2 parts of stomach with solid food, 1 part with liquids, and leave 1 part empty for air and digestive movement.",
            "Triphala water: 1 cup lukewarm triphala water at night to cleanse gut and regulate appetite hormones.",
            "Guggulu or Medohar Guggulu to balance Kapha-induced cravings."
        ],
        "ayurvedic_remedies_hi": [
            "मिताहार सिद्धांत (AYUSH): पेट का आधा हिस्सा ठोस भोजन से भरें, एक-चौथाई पानी के लिए और एक-चौथाई हवा और पाचन के लिए खाली छोड़ें।",
            "त्रिफला जल: रात में गुनगुना त्रिफला पानी आंतों को साफ कर भूख के हार्मोन संतुलित करता है।",
            "मेदोहर गुग्गुलु: अत्यधिक कफ और खाने की लालसा को कम करने वाली औषधि।"
        ],
        "home_remedies_en": [
            "Drink 1 large glass of lukewarm water 20 minutes before every major meal.",
            "Chew each mouthful of food 25-30 times; it takes 20 minutes for leptin (satiety hormone) to reach the brain.",
            "Keep healthy emergency snacks (roasted makhana, roasted chana) instead of biscuits."
        ],
        "home_remedies_hi": [
            "भोजन से 20 मिनट पहले एक बड़ा गिलास गुनगुना पानी पिएं।",
            "खाने के हर कौर को कम से कम 25-30 बार चबाएं; दिमाग तक पेट भरने का संकेत पहुंचने में 20 मिनट लगते हैं।",
            "घर में बिस्कुट-नमकीन की जगह भुना मखाना और भुना चना रखें।"
        ],
        "diet_nutrition_en": ["Ensure 20-25g protein per meal (dal, paneer, eggs, sprouts). High fiber salads before main meal."],
        "diet_nutrition_hi": ["हर भोजन में प्रोटीन (दाल, पनीर, स्प्राउट्स) जरूर शामिल करें ताकि पेट लंबे समय तक भरा रहे।"],
        "dos_and_donts_en": {"dos": ["Eat from a smaller plate", "Put gadgets away during meal times"], "donts": ["Never eat directly out of snack packages", "Do not skip meals as it triggers compensatory binging"]},
        "dos_and_donts_hi": {"dos": ["छोटी थाली में खाना परोसें", "खाना खाते समय फोन और टीवी बंद रखें"], "donts": ["पैकेट से सीधे चिप्स या नमकीन न खाएं", "मील स्किप न करें क्योंकि बाद में ज्यादा भूख लगती है"]},
        "when_to_see_doctor_en": "Consult a physician or clinical psychologist if overeating involves induced vomiting, extreme shame, or symptoms of Binge Eating Disorder (BED).",
        "when_to_see_doctor_hi": "यदि बार-बार अनियंत्रित रूप से खाने के बाद उल्टी करने का मन करे या गंभीर अवसाद हो तो मनोचिकित्सक से मिलें।",
        "allergy_keywords": ["makhana", "chana", "dairy"],
        "sources": "ICMR Guidelines on Healthy Eating & WHO Non-Communicable Disease Prevention"
    },
    "food_sensitivity": {
        "id": "food_sensitivity",
        "category_id": "digestion",
        "category_name": "🍽️ Digestive Issues",
        "title_en": "Food Sensitivity (Non-Allergic)",
        "title_hi": "भोजन की संवेदनशीलता (Food Sensitivity)",
        "overview_en": "Digestive discomfort (bloating, loose motions, or lethargy) after consuming specific foods (like dairy, gluten, or FODMAPs), without anaphylactic immune reaction.",
        "overview_hi": "कुछ खास खाद्य पदार्थों (जैसे दूध, मैदा) को खाने के बाद पेट खराब होना, गैस या मरोड़ होना, जो गंभीर एलर्जी नहीं बल्कि संवेदनशीलता है।",
        "causes_en": ["Low digestive enzyme activity (e.g. low lactase)", "Altered gut microbiome (dysbiosis) after antibiotics", "Irritable bowel syndrome (IBS)", "Leaky gut / impaired intestinal permeability"],
        "causes_hi": ["पाचक एंजाइमों की कमी (जैसे दूध पचाने वाले लैक्टेज की कमी)", "एंटीबायोटिक दवाओं के बाद आंतों के अच्छे बैक्टीरिया कम होना", "आईबीएस (IBS)", "कमजोर आंतें"],
        "ayurvedic_remedies_en": [
            "Takra (Ayurvedic Buttermilk Therapy): Fresh churned curd diluted 1:4 with water, spiced with roasted cumin and curry leaves. Renowned gut healer (Grahani roga).",
            "Musta (Nutgrass / Nagarmotha): Calms inflamed intestinal linings.",
            "Kutajghan Vati for sensitive bowels with loose motions."
        ],
        "ayurvedic_remedies_hi": [
            "तक्र कल्प (छाछ चिकित्सा): ताजे दही में चार गुना पानी मिलाकर मथें, भुना जीरा व कढ़ी पत्ता डालकर पिएं (आंतों के लिए सर्वोत्तम अमृत)।",
            "नागरमोथा (मुस्ता): आंतों की सूजन और संवेदनशीलता शांत करने वाली बूटी।",
            "कुटजघन वटी: यदि संवेदनशीलता से बार-बार दस्त लगते हों तो अत्यंत लाभकारी।"
        ],
        "home_remedies_en": [
            "Maintain a 14-day Food & Symptom Diary to systematically identify trigger foods.",
            "Cumin-Coriander-Fennel (CCF) tea: 1/2 tsp each boiled in 2 cups of water, reduced to 1 cup; sip warm.",
            "Drink warm bone broth or vegetable broth to nourish intestinal barrier."
        ],
        "home_remedies_hi": [
            "14 दिन तक एक डायरी बनाएं कि क्या खाने के बाद पेट में तकलीफ होती है।",
            "जीरा-धनिया-सौंफ (CCF) की चाय: आधा-आधा चम्मच तीनों को पानी में उबालकर गुनगुना पिएं।",
            "हल्का सब्जियों का सूप पिएं जो आंतों को आराम दे।"
        ],
        "diet_nutrition_en": ["Substitute lactose with plant-based milks or curd. Try gluten-free millets (Jowar, Ragi, Bajra) if wheat causes discomfort."],
        "diet_nutrition_hi": ["यदि दूध से दिक्कत हो तो दही लें या बादाम/सोया दूध। गेहूं की जगह ज्वार, बाजरा, रागी का आटा अपनाएं।"],
        "dos_and_donts_en": {"dos": ["Eliminate suspected food for 3 weeks, then reintroduce slowly", "Cook food thoroughly"], "donts": ["Do not eliminate entire food groups without medical testing", "Avoid raw cold foods"]},
        "dos_and_donts_hi": {"dos": ["संदेहास्पद भोजन को 3 हफ्ते बंद करके फिर थोड़ा खाकर जांचें", "खाना अच्छी तरह पकाकर खाएं"], "donts": ["बिना जांच के सारे अनाज खाना बंद न करें", "कच्चा और ठंडा खाना न खाएं"]},
        "when_to_see_doctor_en": "WARNING: If food reaction causes hives, throat tightness, lip swelling, or breathing difficulty, this is a severe allergy (Anaphylaxis) — call an ambulance immediately.",
        "when_to_see_doctor_hi": "चेतावनी: यदि खाना खाने के बाद होंठ या गले में सूजन आए, सांस लेने में तकलीफ हो या शरीर पर लाल चकत्ते पड़ें तो यह जानलेवा एलर्जी है — तुरंत अस्पताल जाएं।",
        "allergy_keywords": ["dairy", "curd", "cumin", "fennel", "coriander"],
        "sources": "ICMR Guidelines on Food Intolerances & AYUSH Grahani Protocols"
    },
    "irregular_digestion": {
        "id": "irregular_digestion",
        "category_id": "digestion",
        "category_name": "🍽️ Digestive Issues",
        "title_en": "Irregular Digestion (Visham Agni)",
        "title_hi": "अनियमित पाचन (Irregular Digestion)",
        "overview_en": "Unpredictable digestive fire — sometimes strong and digesting quickly, other times sluggish and causing bloating and gas, classic of Vata disturbance.",
        "overview_hi": "कभी बहुत तेज भूख लगना और कभी दिनभर बिल्कुल भूख न लगना, पेट का कभी सही और कभी अचानक खराब रहना।",
        "causes_en": ["Erratic eating schedules (different meal times every day)", "Frequent travel, night shifts, and irregular sleep", "Excessive dry, cold, light foods (salads, chips)", "Chronic stress and anxiety"],
        "causes_hi": ["रोजाना अलग-अलग समय पर खाना खाना", "लगातार यात्राएं या नाइट शिफ्ट", "सूखा और ठंडा खाना (जैसे चिप्स, कोल्ड ड्रिंक)", "तनाव और अनिश्चित दिनचर्या"],
        "ayurvedic_remedies_en": [
            "Pure Cow Ghee: 1 tsp warm cow ghee added to the first mouthful of warm rice or dal stabilizes erratic Vata fire.",
            "Hingwashtak Churna: 1/2 tsp before meals with warm water.",
            "Dashamoola Kashayam: Herbal decoction to calm systemic Vata."
        ],
        "ayurvedic_remedies_hi": [
            "देसी गाय का घी: गर्म दाल-चावल में 1 चम्मच गाय का घी डालकर खाएं (अनियमित वात को शांत करता है)।",
            "हिंग्वाष्टक चूर्ण: भोजन से पहले आधा चम्मच गुनगुने पानी के साथ लें।",
            "दशमूल काढ़ा: शरीर के वात दोष को संतुलित करने वाली प्राचीन औषधि।"
        ],
        "home_remedies_en": [
            "Establish strict, unvarying meal times: Breakfast 8:30 AM, Lunch 1:00 PM, Dinner 7:30 PM.",
            "Drink warm ginger-cinnamon tea 30 minutes after meals.",
            "Abhyanga: Self-massage with warm sesame oil before bath."
        ],
        "home_remedies_hi": [
            "भोजन का समय बिल्कुल निश्चित करें: नाश्ता 8:30 बजे, दोपहर का खाना 1:00 बजे, रात का खाना 7:30 बजे।",
            "खाने के 30 मिनट बाद अदरक और दालचीनी का गुनगुना पानी पिएं।",
            "नहाने से पहले शरीर पर गुनगुने तिल के तेल की मालिश करें।"
        ],
        "diet_nutrition_en": ["Warm, soupy, moist meals with healthy fats (ghee, sesame oil). Khichdi, pumpkin soup, stewed vegetables."],
        "diet_nutrition_hi": ["गर्म, रसदार और घी युक्त ताजा भोजन लें। खिचड़ी, कद्दू का सूप, उबली सब्जियां।"],
        "dos_and_donts_en": {"dos": ["Keep your feet warm", "Eat sitting peacefully on a chair or floor"], "donts": ["Do not eat while walking, driving, or in a rush", "Avoid icy cold drinks"]},
        "dos_and_donts_hi": {"dos": ["पैरों को गर्म रखें", "शांति से बैठकर भोजन करें"], "donts": ["चलते-फिरते या गाड़ी चलाते हुए न खाएं", "बर्फ वाला पानी न पिएं"]},
        "when_to_see_doctor_en": "Consult a doctor if irregular digestion is accompanied by persistent alternation of severe diarrhea and constipation with weight loss.",
        "when_to_see_doctor_hi": "यदि पेट कभी बहुत ढीला और कभी बेहद कब्ज रहे और साथ में वजन घटे तो आंतों की जांच कराएं।",
        "allergy_keywords": ["ghee", "dairy", "sesame", "cinnamon"],
        "sources": "Ministry of AYUSH Vata Management & NHP India"
    },
    "nausea_mild": {
        "id": "nausea_mild",
        "category_id": "digestion",
        "category_name": "🍽️ Digestive Issues",
        "title_en": "Nausea (Non-Medical / Motion / Mild)",
        "title_hi": "जी मिचलाना और उल्टी का अहसास (Nausea)",
        "overview_en": "Mild feeling of gastric unease and urge to vomit, commonly triggered by travel motion, unpleasant smells, indigestion, or morning sickness.",
        "overview_hi": "उल्टी आने जैसा महसूस होना, चक्कर आना, जो सफर (मोशन सिकनेस), बदहजमी या तेज गंध के कारण होता है।",
        "causes_en": ["Motion sickness while traveling in cars, buses, or boats", "Gastric hyperacidity or overeating", "Unpleasant strong odors or stuffy rooms", "Early pregnancy hormonal changes"],
        "causes_hi": ["गाड़ी या बस में सफर करते समय मोशन सिकनेस", "एसिडिटी या बहुत ज्यादा खाना", "तेज गंध या बंद कमरे में घुटन", "गर्भावस्था के शुरुआती हफ्तों में हार्मोनल बदलाव"],
        "ayurvedic_remedies_en": [
            "Eladi Vati: Classical chewable herbal tablet with cardamom, cinnamon, and camphor that soothes the vomiting center.",
            "Clove (Laung): Keep one whole clove in the mouth and slowly suck its juice.",
            "Amla Murabba or dried salty amla slices."
        ],
        "ayurvedic_remedies_hi": [
            "एलादि वटी: इलायची युक्त आयुर्वेदिक चूसने वाली गोली जो जी मिचलाना तुरंत रोकती है।",
            "लौंग: मुंह में एक लौंग रखकर धीरे-धीरे रस चूसें।",
            "आंवले का मुरब्बा या सूखा आंवला चबाएं।"
        ],
        "home_remedies_en": [
            "Inhale the aroma of a freshly cut lemon wedge with a sprinkle of black salt.",
            "Sip iced ginger ale or fresh ginger tea slowly through a straw.",
            "Acupressure Point P6 (Neiguan): Press firmly 3 finger-widths below the inner wrist crease for 2 minutes."
        ],
        "home_remedies_hi": [
            "नींबू पर काला नमक छिड़ककर सूंघें और थोड़ा चाटें।",
            "अदरक का ताजा पानी घूंट-घूंट करके पिएं।",
            "कलाई के अंदरूनी हिस्से पर 3 उंगली नीचे (P6 पॉइंट) 2 मिनट तक दबाएं।"
        ],
        "diet_nutrition_en": ["Dry toast, plain salted crackers, boiled potatoes. Avoid greasy gravies and strong dairy."],
        "diet_nutrition_hi": ["सूखा टोस्ट, हल्के बिस्कुट, उबला आलू। तली-भुनी चीजें बिल्कुल न खाएं।"],
        "dos_and_donts_en": {"dos": ["Sit in the front passenger seat during car rides and look at the distant horizon", "Get fresh circulating air"], "donts": ["Do not read books or stare at mobile phones during travel", "Avoid strong perfumes"]},
        "dos_and_donts_hi": {"dos": ["सफर के दौरान आगे की सीट पर बैठें और खिड़की खोलकर दूर क्षितिज को देखें", "ताजी हवा लें"], "donts": ["चलती गाड़ी में मोबाइल न देखें और किताबें न पढ़ें", "तेज इत्र व परफ्यूम से बचें"]},
        "when_to_see_doctor_en": "Seek medical evaluation if nausea is accompanied by high fever, severe stiff neck, persistent inability to keep liquids down for >24 hours, or head injury.",
        "when_to_see_doctor_hi": "यदि जी मिचलाने के साथ तेज सिरदर्द, गर्दन में अकड़न हो, सिर में चोट लगी हो या 24 घंटे से पानी भी न रुक रहा हो तो तुरंत अस्पताल जाएं।",
        "allergy_keywords": ["clove", "cardamom", "ginger", "lemon"],
        "sources": "WHO Clinical Guidelines on Primary Care & NHP India"
    },

    # ==========================================
    # CATEGORY 5: 😴 Sleep & Energy (10 issues)
    # ==========================================
    "insomnia": {
        "id": "insomnia",
        "category_id": "sleep",
        "category_name": "😴 Sleep & Energy",
        "title_en": "Insomnia / Sleep Issues (Anidra)",
        "title_hi": "अनिद्रा (Insomnia / Sleeplessness)",
        "overview_en": "Difficulty initiating or maintaining restful sleep, leading to unrefreshing rest, daytime cognitive fatigue, and irritability.",
        "overview_hi": "रात में नींद न आना, बार-बार आंख खुलना और सुबह उठने पर भी शरीर में थकावट महसूस होना।",
        "causes_en": ["Elevated Vata and Pitta doshas disrupting mental tranquility", "Blue light from smartphone and laptop screens before bed", "High caffeine consumption in the evening", "Chronic emotional stress, rumination, and anxiety", "Noisy, warm, or uncomfortable sleep environment"],
        "causes_hi": ["मानसिक तनाव और चिंता से दिमाग शांत न होना", "सोने से ठीक पहले मोबाइल या लैपटॉप चलाना (ब्लू लाइट)", "शाम को चाय या कॉफी पीना", "शारीरिक मेहनत की कमी", "कमरे में गर्मी या शोर होना"],
        "ayurvedic_remedies_en": [
            "Ashwagandha & Nutmeg Milk: 1/2 tsp Ashwagandha + pinch of Jaiphal (nutmeg) in warm cow milk 30 mins before bed.",
            "Shiroabhyanga: Warm sesame or Brahmi oil massage to the scalp and temples.",
            "Pada Abhyanga: Massaging the soles of feet with warm cow ghee or mustard oil before sleeping instantly calms Vata.",
            "Brahmi Vati: Classical medhya rasayana to quiet repetitive racing thoughts."
        ],
        "ayurvedic_remedies_hi": [
            "अश्वगंधा व जायफल वाला दूध: रात को सोने से पहले आधा चम्मच अश्वगंधा और चुटकी भर जायफल गुनगुने दूध में मिलाकर पिएं।",
            "शिरोअभ्यंग: सोने से पहले ब्राह्मी या तिल के गुनगुने तेल से सिर की 10 मिनट मालिश करें।",
            "पादाभ्यंग: रात को सोने से पहले तलवों में शुद्ध गाय के घी या सरसों के तेल की मालिश करें (गहरी नींद का रामबाण उपाय)।",
            "ब्राह्मी वटी: दिमाग के अनियंत्रित विचारों को शांत करने वाली औषधि।"
        ],
        "home_remedies_en": [
            "Chamomile Tea: Drink 1 cup 45 minutes before bedtime to trigger natural sleep receptors.",
            "Warm Water Foot Bath: Soak feet in warm water with rock salt for 10 minutes before bed.",
            "4-7-8 Breathing Technique: Inhale for 4s, hold for 7s, exhale slowly for 8s (repeat 4 rounds)."
        ],
        "home_remedies_hi": [
            "कैमोमाइल टी: सोने से 45 मिनट पहले कैमोमाइल की हल्की हर्बल चाय पिएं।",
            "गुनगुने पानी में पैर भिगोना: रात को सोने से पहले 10 मिनट गुनगुने पानी में थोड़ा नमक डालकर पैर रखें।",
            "4-7-8 श्वास प्राणायाम: 4 सेकंड सांस लें, 7 सेकंड रोकें, 8 सेकंड में धीरे-धीरे छोड़ें (4 बार करें)।"
        ],
        "diet_nutrition_en": [
            "Tryptophan-rich evening foods: Warm milk, soaked almonds, pumpkin seeds, and bananas.",
            "Avoid: Heavy greasy dinners, spicy curries, dark chocolate, and energy drinks after 4 PM."
        ],
        "diet_nutrition_hi": [
            "शाम को ट्रिप्टोफैन युक्त आहार: गुनगुना दूध, भीगे बादाम, कद्दू के बीज और केला।",
            "परहेज: रात को भारी तला-भुना खाना, रात में चाय-कॉफी या एनर्जी ड्रिंक।"
        ],
        "dos_and_donts_en": {
            "dos": ["Set a strict digital curfew: Turn off all screens 60 minutes before bed", "Keep bedroom cool (18-21°C), pitch dark, and silent"],
            "donts": ["Do not stare at the bedroom clock if awake", "Do not exercise vigorously within 2 hours of bedtime"]
        },
        "dos_and_donts_hi": {
            "dos": ["सोने से 1 घंटा पहले मोबाइल और टीवी स्क्रीन बंद कर दें", "कमरे में पूरा अंधेरा और शांति रखें"],
            "donts": ["नींद न आने पर बार-बार घड़ी न देखें", "सोने से ठीक पहले भारी कसरत न करें"]
        },
        "when_to_see_doctor_en": "Consult a physician or sleep specialist if insomnia persists for >1 month despite sleep hygiene, or if accompanied by choking/gasping sounds during sleep (Sleep Apnea).",
        "when_to_see_doctor_hi": "यदि 1 महीने से नींद न आ रही हो या सोते समय सांस रुकने या खर्राटों के साथ दम घुटने लगे (स्लीप एप्निया) तो डॉक्टर से जांच कराएं।",
        "allergy_keywords": ["milk", "dairy", "nutmeg", "almond", "sesame", "mustard"],
        "sources": "Ministry of AYUSH Guidelines on Sleep Disorders & ICMR Mental Health Norms"
    },
    "sleep_deprivation": {
        "id": "sleep_deprivation",
        "category_id": "sleep",
        "category_name": "😴 Sleep & Energy",
        "title_en": "Sleep Deprivation",
        "title_hi": "नींद की कमी के दुष्प्रभाव (Sleep Deprivation)",
        "overview_en": "The cumulative physiological deficit resulting from consistently receiving less than 7 hours of restorative sleep per night.",
        "overview_hi": "लगातार 7 घंटे से कम सोने से शरीर में कमजोरी, चिड़चिड़ापन, प्रतिरोधक क्षमता में गिरावट और एकाग्रता की कमी होना।",
        "causes_en": ["Prolonged late-night work shifts or academic cramming", "Revenge bedtime procrastination on smartphones", "Newborn caregiving demands", "Chronic pain conditions waking patient repeatedly"],
        "causes_hi": ["देर रात तक काम करना या पढ़ाई करना", "रात में देर तक फोन पर रील्स और वीडियो देखना", "छोटे बच्चे की देखभाल", "शरीर में किसी दर्द की वजह से नींद टूटना"],
        "ayurvedic_remedies_en": [
            "Chyawanprash: 1 tsp in the morning with warm milk to replenish cellular Ojas drained by sleeplessness.",
            "Ashwagandha Rasayana: Restores adrenal vitality and nervous system balance.",
            "Nasya with pure Cow Ghee: 2 drops in nostrils in morning restores mental alertness."
        ],
        "ayurvedic_remedies_hi": [
            "च्यवनप्राश: सुबह 1 चम्मच गुनगुने दूध के साथ लें ताकि नींद की कमी से घटा ओजस (ऊर्जा) वापस आए।",
            "अश्वगंधा रसायन: तंत्रिका तंत्र और एड्रेनल ग्रंथियों को मजबूती देता है।",
            "गाय के घी का नस्य: सुबह दोनों नथुनों में 2-2 बूंद शुद्ध घी डालने से सिर हल्का रहता है।"
        ],
        "home_remedies_en": [
            "Power Nap: Take a 20-minute power nap between 1:00 PM and 2:30 PM (do not exceed 25 mins).",
            "Hydrate with electrolyte-rich coconut water to counter cognitive sluggishness.",
            "Morning Sun Gazing: 15 minutes of direct sunlight into eyes within 30 minutes of waking resets circadian clock."
        ],
        "home_remedies_hi": [
            "20 मिनट की पावर नैप: दोपहर 1 से 2:30 बजे के बीच 20 मिनट की छोटी नींद लें (25 मिनट से ज्यादा न सोएं)।",
            "नारियल पानी पिएं ताकि शरीर और दिमाग में ताजगी आए।",
            "सुबह की धूप: उठने के आधे घंटे के भीतर 15 मिनट धूप में बैठें, इससे बॉडी क्लॉक रिसेट होती है।"
        ],
        "diet_nutrition_en": ["Nutrient-dense whole foods: Walnuts, seeds, spinach, eggs, lentils. Avoid excess sugar to prevent energy crashes."],
        "diet_nutrition_hi": ["पोषक तत्वों से भरपूर आहार: अखरोट, पालक, दालें और फल। मीठी चीजें कम खाएं ताकि शुगर क्रैश न हो।"],
        "dos_and_donts_en": {"dos": ["Prioritize sleep as an essential biological requirement", "Go to bed 30 minutes earlier tonight"], "donts": ["Do not attempt long-distance driving when severely sleep-deprived", "Do not rely on excess caffeine"]},
        "dos_and_donts_hi": {"dos": ["नींद को भी दवाई की तरह जरूरी समझें", "आज रात 30 मिनट पहले सोने जाएं"], "donts": ["नींद की कमी में लंबी गाड़ी न चलाएं (दुर्घटना का खतरा)", "बार-बार चाय-कॉफी न पिएं"]},
        "when_to_see_doctor_en": "See a physician if sleep deprivation triggers micro-sleep episodes during the day, severe chest palpitations, or hallucinations.",
        "when_to_see_doctor_hi": "यदि दिन में बैठे-बैठे अचानक आंखें बंद होने लगें, दिल की धड़कन तेज हो या मतिभ्रम हो तो तुरंत डॉक्टर से संपर्क करें।",
        "allergy_keywords": ["milk", "dairy", "walnut"],
        "sources": "National Health Portal (NHP India) & WHO Sleep Health Advisory"
    },
    "irregular_sleep_pattern": {
        "id": "irregular_sleep_pattern",
        "category_id": "sleep",
        "category_name": "😴 Sleep & Energy",
        "title_en": "Irregular Sleep Pattern (Circadian Disruption)",
        "title_hi": "अनियमित सोने का चक्र (Irregular Sleep Cycle)",
        "overview_en": "Sleeping and waking at widely varying hours each day, causing desynchronization of internal biological clocks (social jetlag).",
        "overview_hi": "रोजाना सोने और जागने का समय अलग-अलग होना, जिससे शरीर की आंतरिक घड़ी (बायोलॉजिकल क्लॉक) गड़बड़ा जाती है।",
        "causes_en": ["Rotating shift work or night duties", "Staying awake late on weekends and oversleeping by 4 hours", "Irregular work-from-home timings", "Eating dinner at widely inconsistent hours"],
        "causes_hi": ["रोटेटिंग शिफ्ट या नाइट ड्यूटी", "वीकेंड पर देर रात तक जागना और दोपहर 12 बजे तक सोना", "वर्क फ्रॉम होम में अनियमित दिनचर्या", "कभी रात 8 बजे तो कभी 12 बजे खाना खाना"],
        "ayurvedic_remedies_en": [
            "Dinacharya Discipline: Strict wake-up at Brahma Muhurta (around 6:00 AM) every day regardless of sleep time.",
            "Brahmi Tea in the evening: Calms mental Pitta.",
            "Shankhpushpi Syrup: 2 tsp after dinner supports cognitive circadian balance."
        ],
        "ayurvedic_remedies_hi": [
            "दिनचर्या का पालन: चाहे रात में किसी भी समय सोए हों, सुबह हमेशा एक निश्चित समय (सुबह 6-7 बजे) ही उठें।",
            "ब्राह्मी चाय: शाम के समय ब्राह्मी की चाय मन को शांत करती है।",
            "शंखपुष्पी सिरप: रात के खाने के बाद 2 चम्मच शंखपुष्पी मानसिक संतुलन बनाती है।"
        ],
        "home_remedies_en": [
            "Consistent Wake Time: Wake up at the exact same minute 7 days a week (including weekends).",
            "Morning outdoor walk for 20 minutes to flood retinas with natural lux light.",
            "Evening dimming: Dim home lighting to 20% after 8:00 PM."
        ],
        "home_remedies_hi": [
            "उठने का समय पक्का रखें: हफ्ते के सातों दिन एक ही समय पर अलार्म लगाकर उठें।",
            "सुबह 20 मिनट बाहर खुली धूप में घूमें।",
            "रात 8 बजे के बाद घर की तेज लाइटें बंद करके मद्धिम रोशनी रखें।"
        ],
        "diet_nutrition_en": ["Finish your last bite of food at least 3 hours before targeted bed time every single night."],
        "diet_nutrition_hi": ["सोने के तय समय से ठीक 3 घंटे पहले रात का भोजन समाप्त कर लें।"],
        "dos_and_donts_en": {"dos": ["Expose yourself to sunlight immediately on waking", "Use bedroom only for sleep"], "donts": ["Do not sleep in for >1 hour on Sundays", "Do not work from your bed"]},
        "dos_and_donts_hi": {"dos": ["उठते ही प्राकृतिक धूप में जाएं", "बिस्तर का इस्तेमाल सिर्फ सोने के लिए करें"], "donts": ["रविवार को 2-3 घंटे ज्यादा सोने की गलती न करें", "बिस्तर पर बैठकर लैपटॉप न चलाएं"]},
        "when_to_see_doctor_en": "Consult a sleep specialist if your sleep cycle remains inverted or you suffer from Non-24-Hour Sleep-Wake Disorder.",
        "when_to_see_doctor_hi": "यदि दिन-रात का चक्र पूरी तरह उल्टा हो चुका हो और दिन में जागना असंभव हो तो स्लीप क्लीनिक में परामर्श लें।",
        "allergy_keywords": ["shankhpushpi"],
        "sources": "ICMR Guidelines on Chronobiology & AYUSH Dinacharya"
    },
    "chronic_fatigue": {
        "id": "chronic_fatigue",
        "category_id": "sleep",
        "category_name": "😴 Sleep & Energy",
        "title_en": "Fatigue / Low Energy (Klama / Daurbalya)",
        "title_hi": "अत्यधिक थकान और कमजोरी (Chronic Fatigue)",
        "overview_en": "Persistent state of profound physical and mental exhaustion that is not relieved by ordinary sleep or rest.",
        "overview_hi": "पर्याप्त सोने के बाद भी दिनभर शरीर टूटा-टूटा रहना, काम करने की शक्ति न होना और मानसिक सुस्ती।",
        "causes_en": ["Nutritional deficiencies: Anemia (low hemoglobin), Vitamin B12, or Vitamin D3", "Underactive thyroid gland (Hypothyroidism)", "Post-viral convalescence syndrome", "Chronic unmanaged emotional burnout", "Dehydration and low metabolic Agni"],
        "causes_hi": ["खून की कमी (एनीमिया), विटामिन B12 या विटामिन D3 की कमी", "थायराइड ग्रंथि का धीमा होना (हाइपोथायरायडिज्म)", "बुखार या बीमारी के बाद आई कमजोरी", "लंबे समय से मानसिक तनाव", "शरीर में पानी की कमी"],
        "ayurvedic_remedies_en": [
            "Ashwagandha Avaleha or Churna: 1 tsp with warm cow milk twice daily (the supreme adaptogen).",
            "Drakshavaleha (Raisin paste): Excellent for iron deficiency and liver vitality.",
            "Suvarna Prashan / Rasayana herbs like Guduchi (Giloy) for cellular detoxification and vitality."
        ],
        "ayurvedic_remedies_hi": [
            "अश्वगंधा चूर्ण: सुबह और शाम 1 चम्मच गुनगुने दूध के साथ लें (ऊर्जा और ताकत का सबसे बड़ा स्रोत)।",
            "द्राक्षावलेह: मुनक्का युक्त आयुर्वेदिक रसायन जो खून बढ़ाता है और थकान मिटाता है।",
            "गिलोय क्वाथ: शरीर से टॉक्सिन्स निकालकर रोग प्रतिरोधक क्षमता बढ़ाता है।"
        ],
        "home_remedies_en": [
            "Soak 10 black raisins (Munakka) and 5 almonds overnight; peel and chew slowly in the morning.",
            "Fresh lemon water with a pinch of rock salt and 1 tsp pure honey mid-morning.",
            "15 minutes of gentle Surya Namaskar or brisk walking in fresh air."
        ],
        "home_remedies_hi": [
            "रात को 10 मुनक्का और 5 बादाम भिगोएं; सुबह छिलका उतारकर चबाएं और पानी पिएं।",
            "गुनगुने पानी में आधा नींबू, चुटकी भर सेंधा नमक और 1 चम्मच शहद मिलाकर पिएं।",
            "सुबह ताजी हवा में 15 मिनट टहलें।"
        ],
        "diet_nutrition_en": ["Iron & B12 foods: Dates, beetroot, spinach, lentils, jaggery, paneer, and eggs. Drink 3 liters of water."],
        "diet_nutrition_hi": ["आयरन युक्त आहार: खजूर, चुकंदर, पालक, दालें, गुड़ और चना। 3 लीटर पानी अवश्य पिएं।"],
        "dos_and_donts_en": {"dos": ["Get a complete blood count (CBC), Vitamin B12, and TSH blood test", "Pace your activities"], "donts": ["Do not mask exhaustion with 6 cups of sweet tea", "Avoid prolonged bed rest (it worsens muscle deconditioning)"]},
        "dos_and_donts_hi": {"dos": ["खून की जांच (CBC, B12, D3 और थायराइड) जरूर करवाएं", "काम के बीच में 5 मिनट का ब्रेक लें"], "donts": ["थकान मिटाने के लिए बार-बार चाय-कॉफी न पिएं", "पूरा दिन बिस्तर पर पड़े रहने से कमजोरी और बढ़ती है"]},
        "when_to_see_doctor_en": "Consult a physician promptly if fatigue is accompanied by swollen lymph nodes, unexplained weight loss, shortness of breath on mild exertion, or fainting.",
        "when_to_see_doctor_hi": "यदि थकान के साथ थोड़ा चलने पर भी सांस फूले, चक्कर आकर गिर पड़ें या गर्दन में गांठें महसूस हों तो तुरंत डॉक्टर से जांच करवाएं।",
        "allergy_keywords": ["milk", "dairy", "almond", "raisins", "honey"],
        "sources": "ICMR Guidelines on Micronutrient Deficiencies & AYUSH Rasayana Protocols"
    },
    "daytime_sleepiness": {
        "id": "daytime_sleepiness",
        "category_id": "sleep",
        "category_name": "😴 Sleep & Energy",
        "title_en": "Daytime Sleepiness (Tandra / Hypersomnia)",
        "title_hi": "दिन में ज्यादा नींद आना (Daytime Sleepiness)",
        "overview_en": "Inability to maintain wakefulness and alertness during waking hours, accompanied by involuntary dozing off at work or during study.",
        "overview_hi": "दिन के समय लगातार उनींदापन, सुस्ती और ऑफिस या पढ़ाई के दौरान बार-बार झपकी आना।",
        "causes_en": ["Poor nocturnal sleep quality or untreated sleep apnea", "Heavy carbohydrate-rich lunches (causing high serotonin spikes)", "Kapha dosha predominance and metabolic stagnation", "Lack of physical movement and oxygenation"],
        "causes_hi": ["रात में गहरी नींद न आना या खर्राटे से नींद टूटना", "दोपहर में बहुत ज्यादा चावल या भारी खाना खाना", "शरीर में कफ दोष का बढ़ना", "कमरे में ताजी हवा और ऑक्सीजन की कमी"],
        "ayurvedic_remedies_en": [
            "Trikatu Churna: Pinch of Trikatu with honey before lunch burns away sluggish Kapha and enhances mental Agni.",
            "Nasya with Vacha Taila: Restores mental clarity and dispels lethargy.",
            "Varunadi Kashayam or Triphala to alleviate heavy Kapha tissues."
        ],
        "ayurvedic_remedies_hi": [
            "त्रिकटु चूर्ण: चुटकी भर त्रिकटु शहद के साथ दोपहर के खाने से पहले चाटें (कफ और सुस्ती दूर करता है)।",
            "वचा तैल नस्य: दिमाग को सतर्क और तरोताजा करने वाली आयुर्वेदिक विधि।",
            "त्रिफला पानी: पाचन तंत्र को साफ और हल्का रखता है।"
        ],
        "home_remedies_en": [
            "Splash cold water on face and wash eyes every 2 hours.",
            "Take a brisk 5-minute walk outdoors after lunch instead of remaining seated.",
            "Sip warm green tea or peppermint water when drowsiness hits."
        ],
        "home_remedies_hi": [
            "हर दो घंटे में चेहरे और आंखों पर ठंडे पानी के छींटे मारें।",
            "दोपहर के खाने के बाद तुरंत बैठने की जगह 5-10 मिनट टहलें।",
            "नींद आने पर पुदीने की चाय या ग्रीन टी पिएं।"
        ],
        "diet_nutrition_en": ["Light lunch: Salads, clear dal, steamed vegetables, and whole grain roti. Avoid giant bowls of white rice or deep-fried pakoras at noon."],
        "diet_nutrition_hi": ["हल्का दोपहर का भोजन: पतली दाल, हरी सब्जी और रोटी। दोपहर में बहुत ज्यादा सफेद चावल या पूड़ी-कचौड़ी न खाएं।"],
        "dos_and_donts_en": {"dos": ["Work in a brightly lit room with natural daylight", "Stand up and stretch every 45 minutes"], "donts": ["Do not take long naps (>30 mins) during daytime", "Avoid working in dark or poorly ventilated rooms"]},
        "dos_and_donts_hi": {"dos": ["खिड़की के पास अच्छी रोशनी वाली जगह पर बैठें", "हर 45 मिनट में खड़े होकर अंगड़ाई लें"], "donts": ["दोपहर में 30 मिनट से लंबी नींद न लें", "अंधेरे और घुटन भरे कमरे में काम न करें"]},
        "when_to_see_doctor_en": "See a doctor immediately if you fall asleep while driving or operating machinery, or if your partner notices loud snoring with breathing pauses (Obstructive Sleep Apnea).",
        "when_to_see_doctor_hi": "यदि गाड़ी चलाते हुए झपकी आ जाए या सोते समय सांस रुकने के बाद तेज खर्राटा आता हो (स्लीप एप्निया) तो डॉक्टर से जांच कराएं।",
        "allergy_keywords": ["honey", "peppermint"],
        "sources": "National Health Portal (NHP India) & WHO Neurological Advisory"
    },
    "restless_sleep": {
        "id": "restless_sleep",
        "category_id": "sleep",
        "category_name": "😴 Sleep & Energy",
        "title_en": "Restless Sleep / Frequent Awakenings",
        "title_hi": "बेचैन और टूटी-फूटी नींद (Restless Sleep)",
        "overview_en": "Waking up repeatedly through the night, tossing and turning, vivid distressing dreams, and feeling like you barely slept.",
        "overview_hi": "रात में बार-बार नींद खुलना, करवटें बदलते रहना, बेचैनी और बुरे सपने आना।",
        "causes_en": ["Restless Legs Syndrome (iron/magnesium deficiency)", "Late-night heavy digestion or acid reflux irritating esophagus", "High cortisol levels from unresolved worry", "Room temperature too warm or uncomfortable mattress"],
        "causes_hi": ["पैरों में बेचैनी (आयरन या मैग्नीशियम की कमी)", "देर रात भारी खाना खाने से पेट में जलन", "तनाव से कोर्टिसोल हार्मोन का बढ़ा होना", "कमरे में गर्मी या गद्दे का असुविधाजनक होना"],
        "ayurvedic_remedies_en": [
            "Brahmi Ghrita: 1/2 tsp warm medicated ghee before bed to stabilize erratic dreams.",
            "Ashwagandha & Shankhpushpi Churna with warm milk.",
            "Castor oil massage to the soles of the feet."
        ],
        "ayurvedic_remedies_hi": [
            "ब्राह्मी घृत: आधा चम्मच गुनगुना ब्राह्मी घी रात को लेने से दिमाग शांत होता है और बुरे सपने रुकते हैं।",
            "अश्वगंधा व शंखपुष्पी: दूध के साथ सेवन करने से गहरी और शांत नींद आती है।",
            "पैरों के तलवों में अरंडी (कैस्टर) या तिल के तेल की मालिश।"
        ],
        "home_remedies_en": [
            "Magnesium-rich snack: Handful of pumpkin seeds and 1 banana 1 hour before bed relaxes leg muscles.",
            "Keep an absolute dark room (use blackout curtains or eye mask).",
            "Listen to slow delta-wave sleep soundscapes or chanting before sleep."
        ],
        "home_remedies_hi": [
            "मैग्नीशियम युक्त आहार: सोने से 1 घंटा पहले केला और कद्दू के बीज खाएं (मांसपेशियां रिलैक्स होती हैं)।",
            "कमरे में शत-प्रतिशत अंधेरा रखें या आई-मास्क पहनें।",
            "सोते समय धीमी आवाज में मधुर संगीत या ध्यान लगाएं।"
        ],
        "diet_nutrition_en": ["Magnesium & Calcium sources: Sesame seeds, leafy greens, curd, and almonds. Avoid alcohol before bed."],
        "diet_nutrition_hi": ["तिल, हरी सब्जियां, दही और बादाम। सोने से पहले शराब या बीयर बिल्कुल न पिएं (यह नींद को तोड़ती है)।"],
        "dos_and_donts_en": {"dos": ["Stretch your calves and hamstrings for 5 minutes before bed", "Keep room temperature cool"], "donts": ["Do not drink large amounts of water in the 90 minutes before bed (prevents nighttime urination)", "Avoid late caffeine"]},
        "dos_and_donts_hi": {"dos": ["सोने से पहले 5 मिनट पिंडलियों की हल्की स्ट्रेचिंग करें", "कमरे को ठंडा रखें"], "donts": ["सोने से 1.5 घंटा पहले ज्यादा पानी न पिएं ताकि बार-बार पेशाब न जाना पड़े", "शाम को चाय न पिएं"]},
        "when_to_see_doctor_en": "See a neurologist or sleep clinic if restless legs cause severe creeping, crawling sensations in your calves (Restless Legs Syndrome requires ferritin testing).",
        "when_to_see_doctor_hi": "यदि रात में पिंडलियों में कीड़े रेंगने जैसी बेचैनी हो और पैर हिलाए बिना चैन न मिले तो फेरिटिन (आयरन) की जांच करवाएं।",
        "allergy_keywords": ["milk", "dairy", "sesame", "almond"],
        "sources": "ICMR Guidelines on Sleep Neuropathy & AYUSH Medhya Therapies"
    },
    "early_waking": {
        "id": "early_waking",
        "category_id": "sleep",
        "category_name": "😴 Sleep & Energy",
        "title_en": "Waking Up Too Early (Terminal Insomnia)",
        "title_hi": "सुबह बहुत जल्दी नींद खुल जाना (Early Waking)",
        "overview_en": "Awakening at 3:00 AM to 5:00 AM and being unable to fall back asleep despite feeling exhausted, classic of Vata aggravation and depressive rumination.",
        "overview_hi": "भोर में 3 या 4 बजे अचानक आंख खुल जाना और फिर लाख कोशिशों के बाद भी दोबारा नींद न आना।",
        "causes_en": ["Early morning blood sugar dips (nocturnal hypoglycemia)", "Underlying clinical depression or acute bereavement", "Early morning bladder urgency (prostate enlargement in older men)", "Excess Vata dosha peaking between 2:00 AM and 6:00 AM"],
        "causes_hi": ["रात में ब्लड शुगर का अचानक गिरना", "गंभीर मानसिक अवसाद या दुख", "सुबह पेशाब का तेज दबाव (बुजुर्गों में प्रोस्टेट समस्या)", "भोर में वात दोष का प्राकृतिक रूप से बढ़ना"],
        "ayurvedic_remedies_en": [
            "Medhya Rasayana: Jatamansi Churna (1/2 tsp with warm water before bed) is the supreme Ayurvedic herb for terminal insomnia.",
            "Saraswatarishta: 15 ml with equal water after dinner.",
            "Warm ghee applied to crown of head (Brahmarandhra) and temples."
        ],
        "ayurvedic_remedies_hi": [
            "जटामांसी चूर्ण: आधा चम्मच गुनगुने पानी के साथ रात को लें (सुबह जल्दी नींद खुलने की समस्या का सर्वश्रेष्ठ उपाय)।",
            "सारस्वतारिष्ट: रात के भोजन के बाद 15 मिली पानी मिलाकर लें।",
            "सिर के तालू और कनपटियों पर गुनगुने गाय के घी की मालिश करें।"
        ],
        "home_remedies_en": [
            "Bedtime Complex Snack: Eat 1 tbsp peanut butter or a handful of walnuts before bed to stabilize nighttime blood glucose.",
            "If awake at 4:00 AM, do not turn on bright lights; practice slow abdominal breathing in bed.",
            "Write tomorrow's worries in a notebook before sleeping to empty the mental loop."
        ],
        "home_remedies_hi": [
            "सोने से पहले 1 चम्मच पीनट बटर या 4 अखरोट खाएं ताकि रात में शुगर लेवल स्थिर रहे।",
            "सुबह 4 बजे आंख खुलने पर मोबाइल की तेज लाइट न जलाएं; बिस्तर पर ही गहरी सांस लें।",
            "सोने से पहले अगले दिन की चिंताओं को डायरी में लिख लें ताकि दिमाग शांत रहे।"
        ],
        "diet_nutrition_en": ["Complex carbohydrates at dinner (quinoa, brown rice, whole wheat roti) that release glucose steadily."],
        "diet_nutrition_hi": ["रात के खाने में साबुत अनाज (दलिया, रोटी) लें जो रातभर धीरे-धीरे ऊर्जा देते रहें।"],
        "dos_and_donts_en": {"dos": ["If unable to sleep after 20 mins, get out of bed and read a physical book under dim amber light", "Stay warm"], "donts": ["Never pick up your smartphone when you wake up at 4 AM", "Do not panic"]},
        "dos_and_donts_hi": {"dos": ["यदि 20 मिनट तक नींद न आए तो उठकर मद्धिम रोशनी में कोई किताब पढ़ें", "शरीर को गर्म रखें"], "donts": ["भोर में नींद खुलते ही मोबाइल स्क्रीन बिल्कुल न देखें", "घबराएं नहीं"]},
        "when_to_see_doctor_en": "Early morning awakenings coupled with persistent low mood, loss of interest in life, and feelings of worthlessness are clinical signs of depression — consult a mental health professional.",
        "when_to_see_doctor_hi": "यदि सुबह जल्दी नींद खुलने के साथ मन में उदासी, निराशा या जीने की इच्छा न होने के विचार आएं तो तुरंत मनोचिकित्सक से परामर्श लें।",
        "allergy_keywords": ["peanut", "walnut", "ghee"],
        "sources": "National Health Portal (NHP India) & ICMR Mental Health Clinical Protocol"
    },
    "difficulty_falling_asleep": {
        "id": "difficulty_falling_asleep",
        "category_id": "sleep",
        "category_name": "😴 Sleep & Energy",
        "title_en": "Difficulty Falling Asleep (Sleep-Onset Latency)",
        "title_hi": "बिस्तर पर करवटें बदलना (Difficulty Falling Asleep)",
        "overview_en": "Lying awake in bed for more than 30 to 60 minutes unable to cross the threshold into sleep, usually driven by an overactive sympathetic nervous system.",
        "overview_hi": "बिस्तर पर लेटने के बाद घंटों तक नींद न आना, दिमाग में विचारों का बवंडर चलना और बेचैनी होना।",
        "causes_en": ["Racing thoughts and hyper-arousal before sleep", "Late screen exposure suppressing pineal melatonin secretion", "Consuming dinner too close to bedtime", "Lack of daytime physical fatigue"],
        "causes_hi": ["सोने से पहले दिमाग में काम या पढ़ाई की चिंता चलना", "सोने के समय मोबाइल देखने से मेलाटोनिन हार्मोन का रुकना", "सोने से ठीक पहले भारी खाना खाना", "दिनभर कोई शारीरिक कसरत न करना"],
        "ayurvedic_remedies_en": [
            "Tagara (Valerian wallichii): 1 tablet or 1/2 tsp powder with warm water 45 mins before sleep.",
            "Ashwagandha Root Powder: 1/2 tsp with warm cow milk.",
            "Shiropichu: Cotton pad soaked in warm Brahmi taila placed on vertex of head for 15 mins."
        ],
        "ayurvedic_remedies_hi": [
            "तगर (Tagara): सोने से 45 मिनट पहले आधा चम्मच गुनगुने पानी से लें (नींद लाने वाली प्राकृतिक जड़ी-बूटी)।",
            "अश्वगंधा चूर्ण: गुनगुने दूध के साथ रात को लें।",
            "ब्राह्मी तेल का फाहा: गुनगुने ब्राह्मी तेल में भीगी रुई सिर के तालू पर 15 मिनट रखें।"
        ],
        "home_remedies_en": [
            "Warm Shower: Take a warm shower 90 minutes before bed; the subsequent drop in body temperature triggers sleepiness.",
            "Progressive Muscle Relaxation (PMR): Tense and release each muscle group from toes to forehead.",
            "Keep the bedroom strictly at 19-21°C."
        ],
        "home_remedies_hi": [
            "गुनगुने पानी से स्नान: सोने से डेढ़ घंटा पहले गुनगुने पानी से नहाएं; इसके बाद शरीर ठंडा होकर नींद की तरफ जाता है।",
            "प्रोग्रेसिव मसल रिलैक्सेशन: पैरों की उंगलियों से लेकर माथे तक हर मांसपेशी को 5 सेकंड कसें और फिर ढीला छोड़ें।",
            "कमरे को ठंडा और हवादार रखें।"
        ],
        "diet_nutrition_en": ["Warm turmeric-nutmeg milk (Golden milk) 45 mins before bedtime. Avoid late snacks."],
        "diet_nutrition_hi": ["हल्दी और जायफल वाला गुनगुना दूध सोने से 45 मिनट पहले पिएं।"],
        "dos_and_donts_en": {"dos": ["Leave your smartphone in another room overnight", "Read printed literature"], "donts": ["Do not lay in bed tossing and turning for >30 minutes", "Do not drink espresso or cola after 3 PM"]},
        "dos_and_donts_hi": {"dos": ["सोते समय मोबाइल को दूसरे कमरे में रख दें", "कागज की कोई अच्छी किताब पढ़ें"], "donts": ["30 मिनट से ज्यादा बिना नींद के करवटें न बदलते रहें", "दोपहर बाद कोल्ड ड्रिंक या कॉफी न पिएं"]},
        "when_to_see_doctor_en": "Consult a doctor if sleep-onset latency exceeds 60 minutes nightly for >3 weeks.",
        "when_to_see_doctor_hi": "यदि 3 हफ्ते से ज्यादा समय से रोज रात 1 घंटे से अधिक समय तक नींद न आ रही हो तो डॉक्टर से सलाह लें।",
        "allergy_keywords": ["milk", "dairy", "nutmeg", "turmeric"],
        "sources": "Ministry of AYUSH Sleep Protocols & WHO Healthy Living"
    },
    "poor_sleep_quality": {
        "id": "poor_sleep_quality",
        "category_id": "sleep",
        "category_name": "😴 Sleep & Energy",
        "title_en": "Poor Sleep Quality (Non-Restorative Sleep)",
        "title_hi": "हल्की व असंतोषजनक नींद (Poor Sleep Quality)",
        "overview_en": "Sleeping for 7-8 hours but waking up unrefreshed, groggy, with body aches and cognitive fog, indicating lack of deep slow-wave (Stage 3) and REM sleep.",
        "overview_hi": "पूरी रात सोने के बाद भी सुबह उठकर ताजगी न लगना, सिर भारी रहना और ऐसा लगना जैसे बिल्कुल सोए ही नहीं।",
        "causes_en": ["Micro-arousals caused by silent mouth breathing or snoring", "Subtle environmental disturbances (noise, street lights, uncomfortable pillow)", "Late heavy digestion competing with cellular repair", "Alcohol consumption fragmenting REM sleep architecture"],
        "causes_hi": ["मुंह से सांस लेना या हल्के खर्राटे से गहरी नींद टूटना", "कमरे में हल्की रोशनी, गाड़ियों का शोर या खराब तकिया", "देर रात का भारी खाना", "शराब पीने से गहरी नींद की कमी होना"],
        "ayurvedic_remedies_en": [
            "Brahmi Vati with Shankhpushpi to enhance deep brain wave coherence.",
            "Ashwagandha Avaleha in the evening.",
            "Ksheerabala 101 Taila: 2 drops in nostrils (Nasya) cleanses airways and promotes oxygenation during sleep."
        ],
        "ayurvedic_remedies_hi": [
            "ब्राह्मी वटी और शंखपुष्पी: गहरी नींद (डीप स्लीप) को बढ़ावा देने वाली औषधियां।",
            "अश्वगंधा अवलेह: शाम के समय सेवन करें।",
            "क्षीरबला तैल नस्य: रात को सोते समय 2 बूंद नाक में डालने से सांस की नली खुलती है और गहरी नींद आती है।"
        ],
        "home_remedies_en": [
            "Switch to nasal breathing: Elevate head with an ergonomic cervical pillow.",
            "Complete Darkness: Use blackout eye mask and earplugs.",
            "Stop eating all food 3.5 hours before sleep."
        ],
        "home_remedies_hi": [
            "नाक से सांस लेने का अभ्यास करें; गर्दन के अनुकूल तकिए का प्रयोग करें।",
            "आई-मास्क और ईयरप्लग का प्रयोग करके कमरे को शांत व अंधेरा रखें।",
            "सोने से ठीक साढ़े तीन घंटे पहले भोजन समाप्त कर लें।"
        ],
        "diet_nutrition_en": ["High-zinc and high-magnesium foods: Pumpkin seeds, spinach, walnuts, soaked figs."],
        "diet_nutrition_hi": ["जिंक और मैग्नीशियम युक्त आहार: कद्दू के बीज, पालक, अखरोट और भीगे अंजीर।"],
        "dos_and_donts_en": {"dos": ["Aerobic exercise for 30 minutes in morning sunlight deepens slow-wave sleep", "Keep mattress firm"], "donts": ["Avoid alcohol as a sleep aid (it ruins sleep quality)", "Avoid synthetic polyester bedsheets (use cotton)"]},
        "dos_and_donts_hi": {"dos": ["सुबह 30 मिनट कसरत करने से रात में गहरी नींद आती है", "सूती (कॉटन) की चादरों का प्रयोग करें"], "donts": ["नींद लाने के लिए शराब का सहारा कभी न लें", "गद्दे बहुत ज्यादा नरम न हों"]},
        "when_to_see_doctor_en": "Consult an ENT or sleep specialist to rule out UARS (Upper Airway Resistance Syndrome) or nocturnal bruxism (teeth grinding).",
        "when_to_see_doctor_hi": "यदि रात में दांत पीसने की आदत हो या मुंह सूखकर नींद खुलती हो तो ईएनटी (ENT) डॉक्टर को दिखाएं।",
        "allergy_keywords": ["milk", "dairy", "walnut", "fig"],
        "sources": "National Health Portal (NHP India) & ICMR Sleep Research"
    },
    "jet_lag": {
        "id": "jet_lag",
        "category_id": "sleep",
        "category_name": "😴 Sleep & Energy",
        "title_en": "Jet Lag & Shift Work Fatigue",
        "title_hi": "जेट लैग और नाइट शिफ्ट की थकान (Jet Lag)",
        "overview_en": "Temporary sleep and digestive disturbance caused by rapid travel across multiple time zones or abrupt rotation into night work shifts.",
        "overview_hi": "लंबे हवाई सफर के बाद या नाइट शिफ्ट करने से शरीर की प्राकृतिक लय का टूट जाना, जिससे गलत समय पर नींद और भूख लगती है।",
        "causes_en": ["Mismatch between the internal circadian suprachiasmatic nucleus and local solar time", "Dry cabin air dehydration during long-haul flights", "Irregular meal schedules in new time zones"],
        "causes_hi": ["शरीर की बॉडी क्लॉक और स्थानीय समय में अंतर", "हवाई जहाज की सूखी हवा से शरीर में पानी की कमी", "नए समय के अनुसार भूख न लगना"],
        "ayurvedic_remedies_en": [
            "Abhyanga with warm Sesame Oil immediately upon arrival calms aggravated Vata.",
            "Ashwagandha Churna with warm milk at destination bedtime.",
            "Triphala tea to regulate travel-induced sluggish digestion."
        ],
        "ayurvedic_remedies_hi": [
            "पहुंचते ही गुनगुने तिल के तेल से शरीर की मालिश करें (हवाई सफर से बढ़े वात को तुरंत शांत करता है)।",
            "नए स्थान पर रात के समय अश्वगंधा दूध के साथ लें।",
            "त्रिफला की चाय सफर से बिगड़े पेट को सही करती है।"
        ],
        "home_remedies_en": [
            "Outdoor Sunlight Anchor: Immediately spend 30-45 minutes in direct sunlight during the morning of the new time zone.",
            "Aggressive Hydration: Drink 250ml water for every hour in flight; avoid cabin alcohol and coffee.",
            "Fast or eat very lightly during flight; eat your first substantial meal at the local breakfast hour."
        ],
        "home_remedies_hi": [
            "नए शहर में पहुंचते ही सुबह 45 मिनट तेज धूप में टहलें, इससे दिमाग नया समय स्वीकार कर लेता है।",
            "सफर के दौरान खूब पानी पिएं; फ्लाइट में चाय, कॉफी और शराब से बचें।",
            "फ्लाइट में हल्का खाएं और नए स्थान के नाश्ते के समय ही खाना खाएं।"
        ],
        "diet_nutrition_en": ["Light khichdi, fresh fruit, vegetable soups, and herbal teas. Avoid heavy meats upon arrival."],
        "diet_nutrition_hi": ["खिचड़ी, फल, सब्जियों का सूप और हर्बल चाय लें।"],
        "dos_and_donts_en": {"dos": ["Set watch to destination time zone the moment you board the aircraft", "Stay awake until local night time"], "donts": ["Do not immediately take a 4-hour nap upon daytime arrival", "Avoid heavy sleeping pills"]},
        "dos_and_donts_hi": {"dos": ["फ्लाइट में बैठते ही अपनी घड़ी में नए शहर का समय सेट कर लें", "दिन में पहुंचने पर तुरंत सोने से बचें"], "donts": ["दिन में 4 घंटे की लंबी नींद न लें", "बिना डॉक्टर पूछे नींद की तेज गोलियां न खाएं"]},
        "when_to_see_doctor_en": "See a doctor if shift work disorder leads to chronic gastrointestinal ulceration, severe depression, or accidents.",
        "when_to_see_doctor_hi": "यदि लगातार नाइट शिफ्ट से पेट में अल्सर या गंभीर डिप्रेशन हो जाए तो डॉक्टर से मिलें।",
        "allergy_keywords": ["sesame", "milk", "dairy"],
        "sources": "WHO International Travel and Health & Ministry of AYUSH"
    },

    # ==========================================
    # CATEGORY 6: 😰 Mental & Stress (10 issues)
    # ==========================================
    "stress_anxiety": {
        "id": "stress_anxiety",
        "category_id": "mental",
        "category_name": "😰 Mental & Stress",
        "title_en": "Stress & Anxiety (Chitta Udvega)",
        "title_hi": "तनाव और घबराहट (Stress & Anxiety)",
        "overview_en": "Persistent nervous apprehension, physical muscle tension, racing heart, and shallow breathing triggered by modern lifestyle demands and Prana Vata imbalance.",
        "overview_hi": "मन में निरंतर बेचैनी, दिल की धड़कन तेज होना, मांसपेशियों में जकड़न और घबराहट होना जो बढ़े हुए वात दोष का लक्षण है।",
        "causes_en": ["High sensory overload and continuous screen stimulation", "Workplace deadlines and financial uncertainties", "Suppressed emotions and lack of recovery downtime", "Excessive caffeine intake triggering adrenergic rushes"],
        "causes_hi": ["दिनभर स्क्रीन का अत्यधिक उपयोग", "ऑफिस और काम का दबाव व आर्थिक चिंताएं", "आराम और नींद की कमी", "ज्यादा चाय-कॉफी से एड्रेनालिन का बढ़ना"],
        "ayurvedic_remedies_en": [
            "Brahmi & Ashwagandha Churna: 1/2 tsp each with warm milk or water twice daily (the gold standard for mental calm).",
            "Shirodhara (AYUSH Classical Therapy): Continuous pouring of medicated Brahmi/Ksheerabala oil on forehead.",
            "Nasya with Cow Ghee: 2 drops pure warm ghee in each nostril morning and evening clears prana channels.",
            "Pranayama: 10 minutes of Anulom-Vilom and 5 minutes of Bhramari (humming bee breath)."
        ],
        "ayurvedic_remedies_hi": [
            "ब्राह्मी और अश्वगंधा: दोनों आधा-आधा चम्मच गुनगुने दूध के साथ लें (मानसिक शांति का सबसे उत्तम उपाय)।",
            "शिरोधारा (AYUSH चिकित्सा): माथे पर गुनगुने हर्बल तेल की निरंतर धार, जो तनाव को तुरंत शांत करती है।",
            "गाय के घी का नस्य: दोनों नथुनों में 2-2 बूंद शुद्ध घी डालने से प्राण वायु शांत होती है।",
            "भ्रामरी और अनुलोम-विलोम प्राणायाम: रोजाना 15 मिनट करने से घबराहट तुरंत दूर होती है।"
        ],
        "home_remedies_en": [
            "Chamomile or Tulsi-Cardamom Tea: Sip warm herbal tea slowly when anxiety strikes.",
            "Box Breathing (Navy SEAL technique): Inhale 4s, Hold 4s, Exhale 4s, Hold 4s.",
            "Barefoot Earthing (Walking barefoot on green grass for 15 minutes in the morning)."
        ],
        "home_remedies_hi": [
            "तुलसी और इलायची की हर्बल चाय पिएं।",
            "बॉक्स ब्रीदिंग: 4 सेकंड सांस लें, 4 सेकंड रोकें, 4 सेकंड में छोड़ें, 4 सेकंड खाली रखें।",
            "सुबह हरी घास पर 15 मिनट नंगे पैर टहलें।"
        ],
        "diet_nutrition_en": ["Sattvic diet: Warm khichdi, soaked almonds, walnuts, pumpkin seeds, fresh milk. Avoid red chilies, junk, and stale reheated food."],
        "diet_nutrition_hi": ["सात्विक आहार: भीगे बादाम, अखरोट, दूध, हरी सब्जियां और खिचड़ी। तीखे मसाले, शराब और फास्ट फूड से बचें।"],
        "dos_and_donts_en": {"dos": ["Take 15-minute nature walks without smartphone", "Practice daily gratitude journaling"], "donts": ["Do not read negative news first thing in the morning", "Avoid excessive caffeine"]},
        "dos_and_donts_hi": {"dos": ["बिना मोबाइल के 15 मिनट टहलें", "रोजाना 10 मिनट ध्यान लगाएं"], "donts": ["सुबह उठते ही सोशल मीडिया या नकारात्मक खबरें न देखें", "दिन में 3 कप से ज्यादा चाय न पिएं"]},
        "when_to_see_doctor_en": "EMERGENCY: Seek immediate medical care if anxiety produces sudden intense chest pain, shortness of breath, numbness in fingers, or thoughts of self-harm.",
        "when_to_see_doctor_hi": "आपातकालीन चेतावनी: यदि घबराहट में सीने में तेज दर्द, सांस न आना, हाथ सुन्न होना या आत्महत्या के विचार आएं तो तुरंत डॉक्टर या हेल्पलाइन से संपर्क करें।",
        "allergy_keywords": ["milk", "dairy", "almond", "walnut", "ghee", "tulsi"],
        "sources": "Ministry of AYUSH Mental Health Protocol & ICMR Guidelines"
    },
    "overthinking": {
        "id": "overthinking",
        "category_id": "mental",
        "category_name": "😰 Mental & Stress",
        "title_en": "Overthinking & Racing Thoughts",
        "title_hi": "अत्यधिक विचार और ओवरथिंकिंग (Overthinking)",
        "overview_en": "Incessant loops of repetitive, non-productive thoughts, catastrophizing future events, and mental exhaustion caused by hyperactive Prana Vata.",
        "overview_hi": "दिमाग में बिना रुके विचारों का चक्रव्यूह चलना, भविष्य को लेकर बेवजह डरना और दिमाग का कभी शांत न होना।",
        "causes_en": ["Hyperactive nervous system from chronic multitasking", "Fear of failure and perfectionism", "Information overload from social media doomscrolling", "Lack of grounding physical activities"],
        "causes_hi": ["एक साथ कई काम करने से दिमाग का थकना", "हर काम में परफेक्शन की चाह और असफलता का डर", "इंटरनेट और सोशल मीडिया पर सूचनाओं की भरमार", "शारीरिक मेहनत की कमी"],
        "ayurvedic_remedies_en": [
            "Shankhpushpi Syrup: 2 tsp twice daily with water; clinical intellect tonic (Medhya) that calms thought storms.",
            "Jatamansi Churna: 1/2 tsp with warm water before bed.",
            "Padabhyanga (Foot massage with warm sesame or Ksheerabala oil) before sleep grounds dispersed Vata."
        ],
        "ayurvedic_remedies_hi": [
            "शंखपुष्पी सिरप: 2 चम्मच दिन में दो बार पानी के साथ (दिमाग को शांत और स्थिर करने वाली औषधि)।",
            "जटामांसी चूर्ण: आधा चम्मच गुनगुने पानी के साथ रात को लें।",
            "तलवों की मालिश: रात को गुनगुने तिल के तेल से पैरों के तलवों की 10 मिनट मालिश करें।"
        ],
        "home_remedies_en": [
            "Brain Dump Journaling: Write down every single thought onto physical paper for 10 minutes, then close the notebook.",
            "5-4-3-2-1 Sensory Grounding: Notice 5 things you can see, 4 you can feel, 3 you hear, 2 you smell, 1 you taste.",
            "Yoga Asana: Child Pose (Balasana) for 5 minutes."
        ],
        "home_remedies_hi": [
            "डायरी लेखन: मन में चल रहे सारे विचारों को 10 मिनट में कागज पर लिख लें, दिमाग तुरंत हल्का हो जाता है।",
            "5-4-3-2-1 तकनीक: 5 चीजें देखें, 4 छुएं, 3 सुनें, 2 सूंघें और 1 का स्वाद महसूस करें।",
            "बालासन (शिशु आसन) में 5 मिनट विश्राम करें।"
        ],
        "diet_nutrition_en": ["Warm, grounding foods: Stewed apples, sweet potatoes, oats with ghee, herbal teas. Cut white sugar."],
        "diet_nutrition_hi": ["गर्म और सुपाच्य भोजन: उबला शकरकंद, दलिया, घी और बादाम। सफेद चीनी का प्रयोग बंद करें।"],
        "dos_and_donts_en": {"dos": ["Focus on the single task directly in front of you", "Practice mindfulness"], "donts": ["Do not dwell on past events that cannot be changed", "Avoid endless night scrolling"]},
        "dos_and_donts_hi": {"dos": ["एक समय में केवल एक ही काम पर ध्यान दें", "वर्तमान क्षण में जीने का अभ्यास करें"], "donts": ["बीती बातों पर बार-बार पछताना छोड़ें", "रात में फोन चलाना बंद करें"]},
        "when_to_see_doctor_en": "Consult a psychiatrist or psychologist if overthinking takes the form of intrusive OCD obsessions or severe paralysis of daily functioning.",
        "when_to_see_doctor_hi": "यदि ओवरथिंकिंग से रोजमर्रा के काम रुक जाएं या बार-बार एक ही काम करने की सनक (OCD) हो तो मनोचिकित्सक से मिलें।",
        "allergy_keywords": ["shankhpushpi", "sesame", "ghee", "almond"],
        "sources": "National Health Portal (NHP India) & AYUSH Medhya Guidelines"
    },
    "tension_headaches": {
        "id": "tension_headaches",
        "category_id": "mental",
        "category_name": "😰 Mental & Stress",
        "title_en": "Tension Headaches (Shiroruk)",
        "title_hi": "तनाव जनित सिरदर्द (Tension Headaches)",
        "overview_en": "Dull, aching band of tightness around the forehead, temples, or back of the neck and head caused by muscle contraction and mental strain.",
        "overview_hi": "माथे और कनपटियों पर किसी पट्टी के कसने जैसा दर्द, गर्दन और सिर के पिछले हिस्से में भारीपन।",
        "causes_en": ["Prolonged computer screen glare and eye strain", "Poor neck and shoulder desk posture", "Emotional stress, jaw clenching (bruxism), and lack of hydration", "Skipping lunch"],
        "causes_hi": ["कंप्यूटर स्क्रीन पर लगातार आंखें गड़ाए रखना", "झुककर बैठने से गर्दन की मांसपेशियों में खिंचाव", "पानी कम पीना और मानसिक तनाव", "दोपहर का खाना न खाना"],
        "ayurvedic_remedies_en": [
            "Shirishadi / Dashamoola Lepa: Apply herbal paste of sandalwood (Chandan) and dried ginger (Sunthi) to forehead.",
            "Anu Taila Nasya: 2 drops in nostrils clears cranial tension.",
            "Brahmi Taila gentle temple massage."
        ],
        "ayurvedic_remedies_hi": [
            "चंदन व सौंठ का लेप: माथे पर चंदन और थोड़ी सौंठ का लेप लगाने से सिरदर्द तुरंत शांत होता है।",
            "अणु तैल नस्य: 2-2 बूंद नाक में डालने से सिर और नसों का तनाव दूर होता है।",
            "कनपटियों पर हल्के हाथों से ब्राह्मी तेल की मालिश करें।"
        ],
        "home_remedies_en": [
            "Cold or Warm Compress: Place a warm towel on neck and a cool pack on forehead for 15 mins.",
            "Hydrate immediately with 2 tall glasses of room-temperature water with lemon.",
            "Peppermint Essential Oil: Dilute 2 drops in coconut oil and gently massage on temples."
        ],
        "home_remedies_hi": [
            "माथे पर ठंडी पट्टी और गर्दन के पीछे गर्म कपड़े की सिकाई करें।",
            "तुरंत 2 गिलास पानी में थोड़ा नींबू डालकर पिएं (अक्सर डिहाइड्रेशन से सिरदर्द होता है)।",
            "पुदीने का तेल (पिपरमिंट) नारियल तेल में मिलाकर कनपटियों पर लगाएं।"
        ],
        "diet_nutrition_en": ["Magnesium-rich foods: Green leafy vegetables, soaked almonds, sunflower seeds, and bananas."],
        "diet_nutrition_hi": ["पालक, भीगे बादाम, केला और सूरजमुखी के बीज।"],
        "dos_and_donts_en": {"dos": ["Follow the 20-20-20 rule: Every 20 mins look 20 feet away for 20 seconds", "Keep shoulders relaxed"], "donts": ["Do not skip meals", "Avoid squinting at bright screens in dark rooms"]},
        "dos_and_donts_hi": {"dos": ["20-20-20 नियम: हर 20 मिनट में स्क्रीन से हटाकर 20 फीट दूर देखें", "कंधों को ढीला रखें"], "donts": ["खाना न छोड़ें", "अंधेरे कमरे में तेज मोबाइल स्क्रीन न देखें"]},
        "when_to_see_doctor_en": "RED FLAG: Seek emergency care if headache is sudden and explosive ('worst headache of life' - thunderclap), or accompanied by blurred vision, speech slurring, or weakness on one side.",
        "when_to_see_doctor_hi": "आपातकालीन चेतावनी: यदि अचानक बिजली गिरने जैसा भयंकर सिरदर्द हो, बोलने में लड़खड़ाहट हो या चेहरे का एक हिस्सा सुन्न हो तो तुरंत इमरजेंसी में जाएं (स्ट्रोक का खतरा)।",
        "allergy_keywords": ["peppermint", "coconut", "almond", "ginger"],
        "sources": "National Health Portal (NHP India) & ICMR Neurological Guidelines"
    },
    "mood_swings": {
        "id": "mood_swings",
        "category_id": "mental",
        "category_name": "😰 Mental & Stress",
        "title_en": "Mood Swings & Emotional Volatility",
        "title_hi": "मिजाज में बार-बार बदलाव (Mood Swings)",
        "overview_en": "Rapid, unpredictable shifts in emotional state from calm to intense anger, sadness, or anxiety, reflecting Pitta-Vata fluctuations.",
        "overview_hi": "अचानक खुश और तुरंत बहुत उदास या गुस्सा हो जाना, भावनाओं पर नियंत्रण न रहना।",
        "causes_en": ["Hormonal fluctuations (PMS, perimenopause, thyroid imbalance)", "Blood sugar peaks and valleys from refined carbohydrates", "Chronic sleep deficit dysregulating emotional amygdala centers", "High chronic psychological stress"],
        "causes_hi": ["हार्मोनल बदलाव (माहवारी से पहले, थायराइड या मेनोपॉज)", "मीठा खाने के बाद ब्लड शुगर का तेजी से गिरना", "नींद पूरी न होना", "लगातार तनाव में रहना"],
        "ayurvedic_remedies_en": [
            "Shatavari & Brahmi: 1/2 tsp each with warm milk helps harmonize endocrine-neurotransmitter pathways.",
            "Rose Petal Jam (Gulkand): 1 tsp daily pacifies scorching emotional Pitta fire (anger/irritability).",
            "Nasya with pure Cow Ghee."
        ],
        "ayurvedic_remedies_hi": [
            "शतावरी और ब्राह्मी: दोनों आधा-आधा चम्मच दूध के साथ लें, यह हार्मोन्स और दिमाग को संतुलित करता है।",
            "गुलकंद: सुबह 1 चम्मच गुलकंद खाने से पित्त शांत होता है और चिड़चिड़ापन मिटता है।",
            "गाय के घी का नस्य लें।"
        ],
        "home_remedies_en": [
            "Keep blood sugar stable: Eat small balanced meals with healthy protein every 3-4 hours.",
            "Practice Sitali Pranayama (cooling breath) 10 rounds when feeling irritated.",
            "Spend time in nature / green parks."
        ],
        "home_remedies_hi": [
            "हर 3-4 घंटे में थोड़ा पौष्टिक खाना लें ताकि भूख से मिजाज न बिगड़े।",
            "शीतली प्राणायाम (जीभ को गोल करके ठंडी सांस अंदर लेना) करें।",
            "ताजी हवा और पार्क में घूमें।"
        ],
        "diet_nutrition_en": ["Omega-3 rich foods (walnuts, flaxseed), sweet fruits (pears, sweet apples, melons), and leafy greens."],
        "diet_nutrition_hi": ["अखरोट, अलसी के बीज, मीठे फल (सेब, नाशपाती, खरबूजा) और हरी सब्जियां।"],
        "dos_and_donts_en": {"dos": ["Communicate calmly with loved ones about feeling overwhelmed", "Get 7-8 hours of sound sleep"], "donts": ["Avoid alcohol and energy drinks", "Do not skip lunch"]},
        "dos_and_donts_hi": {"dos": ["परिवार से अपनी भावनाएं खुलकर साझा करें", "7-8 घंटे सोएं"], "donts": ["शराब और एनर्जी ड्रिंक से दूर रहें", "दोपहर का खाना कभी न छोड़ें"]},
        "when_to_see_doctor_en": "Consult a psychiatrist if mood swings alternate with severe manic highs and deep depressive lows (bipolar spectrum screening).",
        "when_to_see_doctor_hi": "यदि अत्यधिक उत्साह और फिर गहरा अवसाद बारी-बारी से आए तो बाइपोलर विकार की जांच हेतु मनोचिकित्सक से मिलें।",
        "allergy_keywords": ["milk", "dairy", "gulkand", "walnut", "flaxseed"],
        "sources": "Ministry of AYUSH Mental Well-being Guidelines & WHO Mental Health"
    },
    "irritability": {
        "id": "irritability",
        "category_id": "mental",
        "category_name": "😰 Mental & Stress",
        "title_en": "Irritability & Anger (Krodha)",
        "title_hi": "चिड़चिड़ापन और गुस्सा (Irritability & Anger)",
        "overview_en": "Low tolerance for minor daily frustrations, quick temper flare-ups, and impatient hostility driven by aggravated Pitta dosha.",
        "overview_hi": "छोटी-छोटी बातों पर तुरंत गुस्सा आ जाना, सब्र की कमी और दूसरों पर बेवजह खीझ निकालना।",
        "causes_en": ["Excess Pitta aggravation in blood and liver", "Hunger and low blood glucose (feeling 'hangry')", "Chronic sleep deprivation and burnout", "Overheating and prolonged exposure to hot sun"],
        "causes_hi": ["शरीर और लिवर में पित्त की अधिकता", "भूख लगना और सही समय पर खाना न मिलना", "नींद की भारी कमी", "धूप और गर्मी में ज्यादा रहना"],
        "ayurvedic_remedies_en": [
            "Gulkand with cold milk in the afternoon (instantly cools emotional temper).",
            "Sandalwood (Chandan) paste applied to the brow center (Ajna chakra).",
            "Praval Pishti / Kamdudha Ras to neutralize acidic Pitta."
        ],
        "ayurvedic_remedies_hi": [
            "दोपहर में ठंडे दूध के साथ गुलकंद खाएं (गुस्सा और पित्त शांत करने का अचूक उपाय)।",
            "माथे के बीच में असली सफेद चंदन का तिलक लगाएं।",
            "प्रवाल पिष्टी का सेवन पित्त को शांत करता है।"
        ],
        "home_remedies_en": [
            "Drink 1 tall glass of cool Tender Coconut Water when feeling irritable.",
            "Pause Rule: Count backwards from 10 to 1 before reacting to a provocation.",
            "Splash cold rose water onto eyes and face."
        ],
        "home_remedies_hi": [
            "गुस्सा या खीझ महसूस होते ही एक गिलास ताजा नारियल पानी पिएं।",
            "10 से 1 तक उल्टी गिनती गिनें और तुरंत प्रतिक्रिया देने से बचें।",
            "चेहरे और आंखों पर ठंडा गुलाब जल छिड़कें।"
        ],
        "diet_nutrition_en": ["Cooling foods: Cucumber, mint, watermelon, coriander, fennel. Strictly avoid red chilies, mustard oil, and alcohol."],
        "diet_nutrition_hi": ["शीतल खाद्य पदार्थ: खीरा, पुदीना, तरबूज, सौंफ और धनिया। तीखी लाल मिर्च, खटाई और शराब से बचें।"],
        "dos_and_donts_en": {"dos": ["Practice Chandra Bhedana pranayama (left nostril cooling breath)", "Take breaks"], "donts": ["Do not make major decisions while angry", "Do not drink hot coffee when agitated"]},
        "dos_and_donts_hi": {"dos": ["चंद्रभेदी प्राणायाम (बाईं नाक से सांस लेना) करें", "काम के बीच थोड़ा ब्रेक लें"], "donts": ["गुस्से में कोई बड़ा फैसला न लें", "गुस्से में कड़क गर्म कॉफी न पिएं"]},
        "when_to_see_doctor_en": "See a counselor or physician if irritability turns into uncontrollable explosive outbursts or interpersonal violence.",
        "when_to_see_doctor_hi": "यदि गुस्सा बेकाबू होकर तोड़फोड़ या मारपीट में बदलने लगे तो मानसिक स्वास्थ्य विशेषज्ञ से तुरंत परामर्श लें।",
        "allergy_keywords": ["milk", "dairy", "gulkand", "coconut", "fennel"],
        "sources": "Ministry of AYUSH Pitta Shanti Protocols & NHP India"
    },
    "concentration_issues": {
        "id": "concentration_issues",
        "category_id": "mental",
        "category_name": "😰 Mental & Stress",
        "title_en": "Concentration & Focus Issues",
        "title_hi": "एकाग्रता की कमी (Lack of Focus)",
        "overview_en": "Inability to sustain mental attention on a single task, frequent mind-wandering, distractibility, and lowered productivity.",
        "overview_hi": "पढ़ाई या काम में मन न लगना, ध्यान बार-बार भटकना और किसी काम को पूरा करने में बहुत समय लगना।",
        "causes_en": ["Constant digital notifications and fractured attention span", "Subclinical anemia, thyroid dysfunction, or Vitamin B12 deficit", "Inadequate sleep and chronic mental fatigue", "Dehydration"],
        "causes_hi": ["मोबाइल नोटिफिकेशन और रील्स की लत", "विटामिन B12, आयरन या थायराइड की कमी", "नींद की कमी", "शरीर में पानी की कमी"],
        "ayurvedic_remedies_en": [
            "Brahmi Ghrita: 1/2 tsp on empty stomach with warm water to nourish cognitive neurons.",
            "Saraswatarishta: 15 ml after meals enhances mental sharpness and retention.",
            "Trataka (Candle Flame Gazing): 5 minutes daily sharpens focal concentration."
        ],
        "ayurvedic_remedies_hi": [
            "ब्राह्मी घृत: सुबह खाली पेट आधा चम्मच गुनगुने पानी के साथ (स्मृति और एकाग्रता बढ़ाता है)।",
            "सारस्वतारिष्ट: भोजन के बाद 15 मिली पानी मिलाकर लें।",
            "त्राटक क्रिया: रोजाना 5 मिनट दीपक की लौ को एकटक देखना एकाग्रता की अचूक साधना है।"
        ],
        "home_remedies_en": [
            "Pomodoro Technique: Work with complete focus for 25 minutes, then take a 5-minute break.",
            "Rosemary / Peppermint aroma: Sniffing rosemary essential oil stimulates focus receptors.",
            "Keep phone on 'Do Not Disturb' in another room while studying or working."
        ],
        "home_remedies_hi": [
            "पोमोडोरो तकनीक: 25 मिनट बिना रुके मन लगाकर पढ़ें/काम करें, फिर 5 मिनट का ब्रेक लें।",
            "पढ़ाई के दौरान मोबाइल को साइलेंट करके दूसरे कमरे में रखें।",
            "पुदीने या रोजमेरी की खुशबू सूंघने से दिमाग सक्रिय होता है।"
        ],
        "diet_nutrition_en": ["Brain foods: Soaked almonds, walnuts, blueberries, eggs, pumpkin seeds, and green tea."],
        "diet_nutrition_hi": ["दिमागी पोषण: भीगे बादाम, अखरोट, कद्दू के बीज और ग्रीन टी।"],
        "dos_and_donts_en": {"dos": ["Declutter your physical study/work desk", "Drink a glass of water before starting work"], "donts": ["Do not attempt to multitask between 5 tabs simultaneously", "Avoid sugary snacks"]},
        "dos_and_donts_hi": {"dos": ["काम करने की मेज साफ-सुथरी रखें", "काम शुरू करने से पहले एक गिलास पानी पिएं"], "donts": ["एक साथ 5 काम करने की कोशिश न करें", "मीठी चीजें खाकर पढ़ाई न करें"]},
        "when_to_see_doctor_en": "Consult a physician to screen for Adult ADHD or severe Vitamin B12/Iron deficiency if concentration problems severely disrupt career or studies.",
        "when_to_see_doctor_hi": "यदि एकाग्रता की कमी से जीवन पूरी तरह प्रभावित हो तो B12 टेस्ट कराएं और ADHD की जांच हेतु डॉक्टर से मिलें।",
        "allergy_keywords": ["almond", "walnut", "ghee", "dairy"],
        "sources": "National Health Portal (NHP India) & ICMR Guidelines on Cognitive Health"
    },
    "memory_problems": {
        "id": "memory_problems",
        "category_id": "mental",
        "category_name": "😰 Mental & Stress",
        "title_en": "Memory Problems (Mild Forgetfulness / Smriti Daurbalya)",
        "title_hi": "याददाश्त की कमजोरी (Memory Weakness - Mild)",
        "overview_en": "Occasional forgetfulness, misplacing items, taking longer to recall names, often caused by stress, lack of sleep, or micronutrient deficits.",
        "overview_hi": "बातें भूल जाना, सामान रखकर भूलना और नाम याद न आना, जो अक्सर तनाव, नींद की कमी या पोषण की कमी से होता है।",
        "causes_en": ["High chronic cortisol shrinking hippocampal memory networks", "Vitamin B12 or folic acid deficiency", "Poor sleep (lack of REM sleep prevents memory consolidation)", "Thyroid dysfunction"],
        "causes_hi": ["तनाव हार्मोन (कोर्टिसोल) से याददाश्त कमजोर होना", "विटामिन B12 और फोलिक एसिड की कमी", "गहरी नींद न आना", "थायराइड की समस्या"],
        "ayurvedic_remedies_en": [
            "Shankhpushpi & Brahmi: Classical Medhya Rasayanas proven to enhance acetylcholine neurotransmission.",
            "Ashwagandha Rasayana: Promotes synaptic neuroplasticity.",
            "Kalyanaka Ghrita or pure cow ghee daily."
        ],
        "ayurvedic_remedies_hi": [
            "शंखपुष्पी व ब्राह्मी: मस्तिष्क की कोशिकाओं को पुनर्जीवित करने वाले सर्वश्रेष्ठ मेध्य रसायन।",
            "अश्वगंधा चूर्ण: नसों की स्मरण शक्ति को मजबूत करता है।",
            "शुद्ध गाय का घी रोजाना भोजन में लें।"
        ],
        "home_remedies_en": [
            "Soak 7 almonds and 2 walnuts overnight, crush with milk and 1 tsp mishri in the morning.",
            "Crossword puzzles, sudoku, or learning a new skill (mental gymnastics).",
            "Review your day's activities in reverse chronological order before falling asleep."
        ],
        "home_remedies_hi": [
            "7 भीगे बादाम और 2 अखरोट पीसकर सुबह दूध में मिलाकर पिएं।",
            "सुडोकू, पहेलियां हल करें या कोई नया हुनर सीखें ताकि दिमाग सक्रिय रहे।",
            "रात को सोने से पहले दिनभर की घटनाओं को उल्टे क्रम में याद करने का अभ्यास करें।"
        ],
        "diet_nutrition_en": ["Choline & Omega-3 foods: Egg yolks, flaxseeds, walnuts, spinach, and sunflower seeds."],
        "diet_nutrition_hi": ["अंडे, अलसी, अखरोट, पालक और सूरजमुखी के बीज।"],
        "dos_and_donts_en": {"dos": ["Keep a daily planner and write things down", "Exercise 30 mins daily (boosts BDNF)"], "donts": ["Do not smoke (nicotine accelerates brain atrophy)", "Avoid chronic sleep deprivation"]},
        "dos_and_donts_hi": {"dos": ["जरूरी बातें डायरी में नोट करने की आदत डालें", "रोजाना 30 मिनट कसरत करें"], "donts": ["सिगरेट-शराब से दूर रहें (दिमाग की नसों को सिकोड़ते हैं)", "नींद कम न लें"]},
        "when_to_see_doctor_en": "See a neurologist immediately if forgetfulness is severe, patient gets lost in familiar neighborhoods, fails to recognize close relatives, or shows personality disintegration (rule out Dementia / Alzheimer's).",
        "when_to_see_doctor_hi": "चेतावनी: यदि व्यक्ति जाने-पहचाने रास्तों पर रास्ता भूल जाए, परिजनों को पहचानने में असमर्थ हो तो तुरंत न्यूरोलॉजिस्ट को दिखाएं (डिमेंशिया या अल्जाइमर का खतरा)।",
        "allergy_keywords": ["milk", "dairy", "almond", "walnut", "ghee", "flaxseed"],
        "sources": "Ministry of AYUSH Medhya Protocols & WHO Dementia Advisory"
    },
    "emotional_eating": {
        "id": "emotional_eating",
        "category_id": "mental",
        "category_name": "😰 Mental & Stress",
        "title_en": "Emotional Eating (Stress Binging)",
        "title_hi": "तनाव में अनियंत्रित खाना (Emotional Eating)",
        "overview_en": "Using food to cope with negative emotions (stress, boredom, sadness, anger) rather than biological nutritional hunger.",
        "overview_hi": "भूख न होने पर भी तनाव, अकेलेपन या उदासी को दबाने के लिए मीठा, चिप्स या पिज्जा जैसी चीजें खाना।",
        "causes_en": ["Elevated cortisol triggering strong cravings for high-sugar, high-fat comfort foods", "Using dopamine hits from food as a coping mechanism", "Inability to distinguish physical hunger from emotional emptiness"],
        "causes_hi": ["तनाव में कोर्टिसोल बढ़ने से मीठा और तला-भुना खाने की तीव्र इच्छा", "मन को खुश करने के लिए खाने का सहारा लेना", "असली भूख और मानसिक भूख में फर्क न पहचान पाना"],
        "ayurvedic_remedies_en": [
            "Brahmi Tea when cravings hit to soothe mental turmoil instead of eating.",
            "Triphala water at bedtime cleanses the digestive tract and re-sensitizes natural fullness signals.",
            "Mindful eating (Mitahara) with deep gratitude before every meal."
        ],
        "ayurvedic_remedies_hi": [
            "क्रेविंग्स होने पर खाने की जगह ब्राह्मी की हर्बल चाय पिएं।",
            "रात को गुनगुना त्रिफला पानी आंतों को शुद्ध कर प्राकृतिक भूख के संकेत जगाता है।",
            "मिताहार का पालन करें और भोजन से पहले 3 बार गहरी सांस लें।"
        ],
        "home_remedies_en": [
            "HALT Check: Before reaching for a snack, ask yourself: Am I Hungry, Angry, Lonely, or Tired?",
            "The 15-Minute Delay Rule: When a craving strikes, set a timer for 15 mins and drink a glass of water; 80% of cravings vanish.",
            "Do not keep high-calorie junk food stored in the house."
        ],
        "home_remedies_hi": [
            "HALT नियम: कुछ भी खाने से पहले खुद से पूछें - क्या मैं सच में भूखा (Hungry) हूँ, या गुस्सा (Angry), अकेला (Lonely), या थका (Tired) हूँ?",
            "15 मिनट का नियम: जब कुछ खाने का मन करे तो 1 गिलास पानी पिएं और 15 मिनट रुकें; 80% लालसा शांत हो जाती है।",
            "घर में बिस्कुट, नमकीन और मीठे का स्टॉक न रखें।"
        ],
        "diet_nutrition_en": ["Stock crisp cucumber sticks, roasted makhana, roasted chana, and herbal teas as safe substitutes."],
        "diet_nutrition_hi": ["घर में खीरा, भुना मखाना, भुना चना और फल रखें।"],
        "dos_and_donts_en": {"dos": ["Find non-food self-care activities (take a bath, call a friend, listen to music)", "Eat sitting down"], "donts": ["Never eat directly out of packages", "Do not punish yourself with severe fasting after binging"]},
        "dos_and_donts_hi": {"dos": ["मन बहलाने के लिए दोस्तों से बात करें, टहलें या संगीत सुनें", "बैठकर शांति से खाएं"], "donts": ["पैकेट से सीधे न खाएं", "ज्यादा खा लेने के बाद खुद को भूखा रखकर सजा न दें"]},
        "when_to_see_doctor_en": "Consult an eating disorder specialist or clinical psychologist if binging is accompanied by severe guilt, depression, or compensatory purging.",
        "when_to_see_doctor_hi": "यदि खाने के बाद अत्यधिक अपराधबोध, अवसाद या जानबूझकर उल्टी करने की प्रवृत्ति हो तो मनोचिकित्सक से मिलें।",
        "allergy_keywords": ["makhana", "chana"],
        "sources": "ICMR Guidelines on Behavioral Nutrition & WHO Mental Health"
    },
    "work_life_balance": {
        "id": "work_life_balance",
        "category_id": "mental",
        "category_name": "😰 Mental & Stress",
        "title_en": "Work-Life Balance Stress",
        "title_hi": "काम और जीवन में असंतुलन (Work-Life Balance Stress)",
        "overview_en": "Chronic strain from the blurring of professional obligations and personal life, leading to neglected relationships, health, and hobbies.",
        "overview_hi": "ऑफिस के काम के दबाव में खुद के लिए, परिवार के लिए और स्वास्थ्य के लिए बिल्कुल समय न मिलना।",
        "causes_en": ["Always-on smartphone communication expectations (late evening emails/chats)", "Long exhausting commutes in heavy traffic", "Inability to say 'No' to unreasonable workloads", "Lack of clear boundaries between home and office"],
        "causes_hi": ["देर रात तक ऑफिस के मैसेज और ईमेल का जवाब देना", "ट्रैफिक में घंटों का थका देने वाला सफर", "हर काम के लिए 'हां' कह देना (सीमाएं न बना पाना)", "घर और दफ्तर के बीच कोई दीवार न होना"],
        "ayurvedic_remedies_en": [
            "Dinacharya Restructuring: Setting sacred morning and evening non-work routines.",
            "Ashwagandha twice daily supports resilience against prolonged workplace stress.",
            "Brahmi Taila head massage on weekends."
        ],
        "ayurvedic_remedies_hi": [
            "दिनचर्या का नियमन: सुबह का पहला घंटा और रात का आखिरी घंटा केवल खुद और परिवार के लिए रखें।",
            "अश्वगंधा का नियमित सेवन काम के दबाव को झेलने की मानसिक शक्ति देता है।",
            "वीकेंड पर ब्राह्मी तेल से सिर की मालिश करें।"
        ],
        "home_remedies_en": [
            "Digital Sunset: Mute work notifications strictly at 7:00 PM every evening.",
            "Schedule 'Me-Time' in your calendar like an unmissable client meeting.",
            "Spend at least 30 uninterrupted minutes daily playing with children or conversing with spouse."
        ],
        "home_remedies_hi": [
            "डिजिटल सनसेट: शाम 7 बजे के बाद ऑफिस के नोटिफिकेशन म्यूट कर दें।",
            "कैलेंडर में अपने शौक और व्यायाम का समय भी पहले से तय करें।",
            "रोजाना 30 मिनट परिवार और बच्चों के साथ बिना फोन के बिताएं।"
        ],
        "diet_nutrition_en": ["Home-cooked fresh meals. Avoid relying on late-night takeout pizzas or biryanis."],
        "diet_nutrition_hi": ["घर का बना सादा और ताजा खाना खाएं। बाहर से मंगवाए गए खाने से बचें।"],
        "dos_and_donts_en": {"dos": ["Learn to say polite but firm 'No' when at capacity", "Take your allotted annual vacation"], "donts": ["Do not check office emails from bed", "Do not sacrifice sleep for work deadlines regularly"]},
        "dos_and_donts_hi": {"dos": ["अपनी क्षमता से ज्यादा काम मिलने पर विनम्रता से मना करना सीखें", "साल में छुट्टियां जरूर लें"], "donts": ["बिस्तर पर लेटकर दफ्तर के मेल न देखें", "काम के लिए नींद की कुर्बानी न दें"]},
        "when_to_see_doctor_en": "Seek medical help if workplace stress causes persistent panic attacks, severe insomnia, or clinical depression.",
        "when_to_see_doctor_hi": "यदि काम के तनाव से पैनिक अटैक, अनिद्रा या डिप्रेशन होने लगे तो तुरंत डॉक्टर से परामर्श लें।",
        "allergy_keywords": ["milk", "dairy"],
        "sources": "WHO Guidelines on Mental Health at Work & Ministry of AYUSH"
    },
    "burnout": {
        "id": "burnout",
        "category_id": "mental",
        "category_name": "😰 Mental & Stress",
        "title_en": "Burnout & Mental Exhaustion",
        "title_hi": "मानसिक थकान और बर्नआउट (Burnout)",
        "overview_en": "A state of emotional, physical, and mental exhaustion caused by excessive and prolonged stress, characterized by cynicism and detachment.",
        "overview_hi": "लगातार तनाव से मानसिक, भावनात्मक और शारीरिक रूप से पूरी तरह टूट जाना, काम के प्रति अरुचि और शून्य महसूस होना।",
        "causes_en": ["Prolonged unmanaged chronic stress without recovery periods", "Feeling lack of control or recognition in one's career", "High-empathy caregiver burden", "Lack of supportive social connections"],
        "causes_hi": ["महीनों तक बिना आराम किए काम का अत्यधिक बोझ", "काम में अपनी मेहनत की कद्र न होना", "मरीजों या बुजुर्गों की लगातार तीमारदारी", "अकेलापन और दोस्तों की कमी"],
        "ayurvedic_remedies_en": [
            "Chyawanprash + Ashwagandha: Supreme rejuvenating combination to restore completely depleted Ojas.",
            "Panchakarma (Abhyanga + Shirodhara) for deep nervous system reset.",
            "Brahmi Rasayana to repair cognitive fatigue."
        ],
        "ayurvedic_remedies_hi": [
            "च्यवनप्राश और अश्वगंधा: शरीर के समाप्त हो चुके ओजस (जीवन शक्ति) को दोबारा लौटाने वाला सर्वोत्तम रसायन।",
            "पंचकर्म (अभ्यंग और शिरोधारा): नर्वस सिस्टम को पूरी तरह रीसेट करने वाली प्राचीन चिकित्सा।",
            "ब्राह्मी रसायन का सेवन करें।"
        ],
        "home_remedies_en": [
            "Take a mandatory 3-to-5 day complete detachment break from professional duties.",
            "Spend time in deep nature (forest bathing / hill walking).",
            "Re-engage with a non-monetized childhood hobby (painting, gardening, playing an instrument)."
        ],
        "home_remedies_hi": [
            "काम से कम से कम 3 से 5 दिन की पूरी छुट्टी लें और फोन बंद रखें।",
            "प्रकृति के बीच समय बिताएं (पहाड़ों या बगीचे में टहलें)।",
            "बचपन का कोई शौक (पेंटिंग, बागवानी, संगीत) दोबारा शुरू करें।"
        ],
        "diet_nutrition_en": ["Nourishing, unctuous foods: Moong khichdi with cow ghee, warm spiced almond milk, fresh seasonal fruits."],
        "diet_nutrition_hi": ["गाय के घी वाली मूंग दाल खिचड़ी, बादाम वाला गुनगुना दूध और ताजे फल।"],
        "dos_and_donts_en": {"dos": ["Accept that rest is not a reward, it is a biological necessity", "Talk to a trusted friend or counselor"], "donts": ["Do not attempt to 'push through' clinical burnout", "Avoid turning to alcohol or smoking"]},
        "dos_and_donts_hi": {"dos": ["यह समझें कि आराम कोई विलासिता नहीं बल्कि शरीर की बुनियादी जरूरत है", "काउंसलर से बात करें"], "donts": ["बर्नआउट में खुद को और ज्यादा न घसीटें", "शराब या सिगरेट का सहारा न लें"]},
        "when_to_see_doctor_en": "See a mental health professional immediately if burnout manifests as severe hopelessness, anhedonia (inability to feel pleasure), or severe depression.",
        "when_to_see_doctor_hi": "यदि बर्नआउट से जीने की इच्छा समाप्त हो जाए, किसी चीज में खुशी न मिले या गहरा अवसाद हो तो तुरंत मनोचिकित्सक से मिलें।",
        "allergy_keywords": ["milk", "dairy", "almond", "ghee"],
        "sources": "WHO ICD-11 Occupational Burnout Guidelines & Ministry of AYUSH Ojas Care"
    },

    # ==========================================
    # CATEGORY 7: 💪 General Health & Lifestyle (10 issues)
    # ==========================================
    "low_immunity": {
        "id": "low_immunity",
        "category_id": "general",
        "category_name": "💪 General Health & Lifestyle",
        "title_en": "Low Immunity (Ojo Kshaya / Weak Resistance)",
        "title_hi": "रोग प्रतिरोधक क्षमता की कमी (Low Immunity)",
        "overview_en": "Susceptibility to frequent infections, recurrent colds, slow wound healing, and prolonged convalescence due to depleted immunological defenses.",
        "overview_hi": "बार-बार बीमार पड़ना, हल्का मौसम बदलते ही सर्दी-खांसी होना और घाव का देर से भरना जो कमजोर प्रतिरोधक क्षमता का संकेत है।",
        "causes_en": ["Micronutrient deficits: Low Zinc, Vitamin C, and Vitamin D3", "Chronic sleep deprivation suppressing T-cell production", "High chronic stress depleting immunoglobulins", "High refined sugar intake paralyzing white blood cell phagocytosis"],
        "causes_hi": ["विटामिन सी, डी और जिंक की कमी", "नींद पूरी न होने से इम्यून सेल्स का कम बनना", "लगातार तनाव", "ज्यादा मीठा खाने से श्वेत रक्त कणिकाओं की क्षमता घटना"],
        "ayurvedic_remedies_en": [
            "Chyawanprash (AYUSH Golden Standard): 1 tsp daily with warm milk on an empty stomach.",
            "AYUSH Kwath: Decoction of Tulsi (4 parts), Dalchini (2 parts), Sunthi (2 parts), and Krishna Marich (1 part) boiled in water.",
            "Giloy (Guduchi) Ghanvati: 1-2 tablets daily to stimulate macrophage phagocytosis.",
            "Haldi Doodh (Golden Milk): 1/2 tsp pure turmeric with pinch of black pepper in warm cow milk."
        ],
        "ayurvedic_remedies_hi": [
            "च्यवनप्राश (AYUSH मान्यता प्राप्त): सुबह खाली पेट 1 चम्मच गुनगुने दूध के साथ लें।",
            "आयुष क्वाथ: तुलसी, दालचीनी, सौंठ और काली मिर्च का काढ़ा बनाकर पिएं।",
            "गिलोय घनवटी: रोजाना 1-2 गोली खाने से खून के श्वेत कण मजबूत होते हैं।",
            "हल्दी वाला दूध: आधा चम्मच हल्दी और चुटकी भर काली मिर्च गुनगुने दूध में मिलाकर पिएं।"
        ],
        "home_remedies_en": [
            "Daily Morning Sunlight: 20 minutes between 8:00 AM and 10:00 AM for natural Vitamin D synthesis.",
            "Fresh Amla (Indian Gooseberry) Juice: 20 ml with equal water in morning (rich natural Vitamin C).",
            "Garlic clove: Swallow 1 small crushed clove with water in morning (allicin is antibacterial/antiviral)."
        ],
        "home_remedies_hi": [
            "सुबह की गुनगुनी धूप में 20 मिनट बैठें ताकि प्राकृतिक विटामिन डी मिले।",
            "आंवले का ताजा रस: 20 मिली आंवला रस पानी मिलाकर सुबह पिएं (विटामिन सी का सबसे बड़ा भंडार)।",
            "लहसुन की एक कली सुबह पानी के साथ निगलें।"
        ],
        "diet_nutrition_en": ["Citrus fruits, amla, bell peppers, spinach, yogurt/curd, almonds, and pumpkin seeds. Cut white sugar."],
        "diet_nutrition_hi": ["आंवला, संतरा, हरी पत्तेदार सब्जियां, दही, बादाम और कद्दू के बीज। चीनी कम करें।"],
        "dos_and_donts_en": {"dos": ["Sleep 7-8 hours nightly (essential for cytokine release)", "Exercise moderately 5 days a week"], "donts": ["Do not take random over-the-counter antibiotics for viral colds", "Avoid smoking"]},
        "dos_and_donts_hi": {"dos": ["7-8 घंटे की पूरी नींद लें", "रोजाना आधा घंटा हल्का व्यायाम करें"], "donts": ["बिना डॉक्टर पूछे हर जुकाम में एंटीबायोटिक न खाएं", "सिगरेट व तंबाकू से बचें"]},
        "when_to_see_doctor_en": "See an immunologist or physician if you suffer from >4 ear infections per year, recurrent pneumonia, or non-healing skin abscesses (rule out primary or secondary immunodeficiency).",
        "when_to_see_doctor_hi": "यदि साल में 4 से ज्यादा बार गंभीर संक्रमण हो या घाव कई हफ्तों तक न भरे तो इम्यून सिस्टम की विस्तृत जांच करवाएं।",
        "allergy_keywords": ["milk", "dairy", "turmeric", "tulsi", "cinnamon", "garlic", "amla"],
        "sources": "Ministry of AYUSH Immunity Guidelines & ICMR Nutrition Guidelines"
    },
    "seasonal_allergies_mild": {
        "id": "seasonal_allergies_mild",
        "category_id": "general",
        "category_name": "💪 General Health & Lifestyle",
        "title_en": "Seasonal Allergies (Allergic Rhinitis / Pratishyaya)",
        "title_hi": "मौसमी एलर्जी और छींकें (Seasonal Allergies)",
        "overview_en": "Sneezing bursts, itchy watery eyes, clear runny nose, and nasal congestion triggered by airborne pollens, dust mites, or seasonal humidity shifts.",
        "overview_hi": "मौसम बदलते ही लगातार छींकें आना, नाक और आंखों से पानी बहना, खुजली और नाक बंद होना।",
        "causes_en": ["Tree, weed, or grass pollens during spring and autumn", "Dust mites and mold spores during damp monsoon months", "Hyperactive histamine response in nasal mucosa", "Low immune tolerance"],
        "causes_hi": ["बसंत और पतझड़ में हवा में फूलों के परागकण (Pollen)", "बारिश के मौसम में धूल के कण और फंगस (Mould)", "नाक की झिल्ली में हिस्टामाइन का बढ़ना"],
        "ayurvedic_remedies_en": [
            "Haridra Khanda: 1 tsp twice daily with warm milk (the gold standard Ayurvedic anti-allergic formulation).",
            "Anu Taila Nasya: 2 drops in nostrils creates a protective lipid barrier against airborne pollen.",
            "Trikatu Churna with Honey to dry excess Kapha fluid.",
            "Steam Inhalation with Nilgiri (Eucalyptus) oil and Ajwain seeds."
        ],
        "ayurvedic_remedies_hi": [
            "हरिद्रा खंड: 1 चम्मच गुनगुने दूध के साथ सुबह-शाम लें (एलर्जी की सबसे प्रसिद्ध आयुर्वेदिक दवा)।",
            "अणु तैल नस्य: रोज सुबह 2-2 बूंद नाक में डालने से परागकण और धूल नाक में चिपक नहीं पाते।",
            "त्रिकटु चूर्ण शहद के साथ लें।",
            "अजवाइन और यूकेलिप्टस के तेल की भाप लें।"
        ],
        "home_remedies_en": [
            "Saline Nasal Rinse (Jala Neti): Flush nasal passages with warm saline water using a neti pot.",
            "Local Raw Honey: 1 tsp daily can help desensitize immune system to local pollens.",
            "Keep home windows closed during high-pollen early mornings (5 AM - 10 AM)."
        ],
        "home_remedies_hi": [
            "जलनेति: गुनगुने हल्के नमक वाले पानी से नाक की सफाई करें।",
            "शुद्ध शहद का सेवन करें।",
            "सुबह 5 से 10 बजे के बीच जब हवा में परागकण ज्यादा हों तो घर की खिड़कियां बंद रखें।"
        ],
        "diet_nutrition_en": ["Warm foods with black pepper, ginger, and turmeric. Strictly avoid ice cream, cold curd, and chilled drinks during flare-ups."],
        "diet_nutrition_hi": ["काली मिर्च, अदरक और हल्दी वाला गर्म भोजन लें। ठंडी चीजें, आइसक्रीम और ठंडा दही न खाएं।"],
        "dos_and_donts_en": {"dos": ["Wash hair and change clothes immediately after coming home from outdoors", "Wear a mask in dusty areas"], "donts": ["Do not dry bedsheets outdoors during high-pollen season", "Avoid rubbing itchy eyes"]},
        "dos_and_donts_hi": {"dos": ["बाहर से आकर हाथ-मुंह धोएं और कपड़े बदलें", "धूल वाली जगह पर मास्क लगाएं"], "donts": ["पराग के मौसम में बाहर खुले में चादरें न सुखाएं", "आंखों को जोर से न मलें"]},
        "when_to_see_doctor_en": "Consult a doctor immediately if allergy symptoms escalate to wheezing, chest tightness, or asthma flare-ups.",
        "when_to_see_doctor_hi": "यदि छींकों के साथ सांस में घरघराहट (सीटी की आवाज) हो या सांस फूलने लगे तो तुरंत डॉक्टर को दिखाएं (अस्थमा का खतरा)।",
        "allergy_keywords": ["milk", "dairy", "honey", "turmeric", "eucalyptus", "ajwain"],
        "sources": "Ministry of AYUSH Allergic Rhinitis Protocols & NHP India"
    },
    "cold_cough_prevention": {
        "id": "cold_cough_prevention",
        "category_id": "general",
        "category_name": "💪 General Health & Lifestyle",
        "title_en": "Cold & Cough Prevention (Kasa-Pratishyaya)",
        "title_hi": "सर्दी-जुकाम से बचाव (Cold & Cough Prevention)",
        "overview_en": "Preventative measures against viral upper respiratory tract infections, sore throat, and cough during seasonal weather transitions.",
        "overview_hi": "मौसम बदलने पर होने वाले जुकाम, गले की खराश और खांसी से पूर्व-बचाव के उपाय।",
        "causes_en": ["Rhinovirus or Coronavirus exposure through airborne droplets", "Sudden exposure to cold air or drinking chilled water after sweating", "Weakened mucosal immunity from dehydration and dry air"],
        "causes_hi": ["सर्दी के वायरस का संक्रमण", "पसीने में अचानक ठंडा पानी पीना या एसी में बैठना", "हवा में सूखापन होने से गले की झिल्ली कमजोर होना"],
        "ayurvedic_remedies_en": [
            "Sitopaladi Churna: 1/2 tsp mixed with honey and ghee twice daily at first hint of tickle in throat.",
            "Khadiradi Vati: Chewable classical tablet for immediate sore throat relief.",
            "Kantakari Avaleha or Talisadi Churna for bronchial clearance.",
            "Salt-Water Gargle with pinch of turmeric powder twice daily."
        ],
        "ayurvedic_remedies_hi": [
            "सितोपलादि चूर्ण: आधा चम्मच शहद के साथ चाटें (गले की खराश और जुकाम की पहली निशानी पर रामबाण)।",
            "खदिरादि वटी: मुंह में रखकर चूसें, गले का दर्द और खांसी तुरंत रुकती है।",
            "तालिसादि चूर्ण का सेवन करें।",
            "गुनगुने पानी में नमक और चुटकी भर हल्दी डालकर दिन में दो बार गरारे करें।"
        ],
        "home_remedies_en": [
            "Ginger-Tulsi Kadha: Boil crushed ginger, 7 holy basil leaves, 4 black peppercorns, and 1 clove in water; sip warm with jaggery.",
            "Steam inhalation with ajwain seeds twice daily.",
            "Drink warm water exclusively during cold weather."
        ],
        "home_remedies_hi": [
            "अदरक-तुलसी का काढ़ा: अदरक, 7 तुलसी के पत्ते, 4 काली मिर्च और 1 लौंग पानी में उबालें और थोड़ा गुड़ डालकर पिएं।",
            "अजवाइन डालकर गर्म पानी की भाप लें।",
            "सर्दियों में केवल गुनगुना पानी ही पिएं।"
        ],
        "diet_nutrition_en": ["Hot vegetable soups with garlic and black pepper, roasted chana, warm dalia. Avoid bananas, curd, and ice cream at night."],
        "diet_nutrition_hi": ["लहसुन और काली मिर्च वाला गर्म सूप, भुना चना और गर्म दलिया। रात में दही, केला और ठंडी चीजें न खाएं।"],
        "dos_and_donts_en": {"dos": ["Keep your throat and chest covered with a scarf in chilly winds", "Wash hands regularly"], "donts": ["Do not drink chilled water immediately after intense sweating", "Avoid crowded poorly ventilated spaces"]},
        "dos_and_donts_hi": {"dos": ["ठंडी हवा में गले और छाती को मफलर से ढकें", "नियमित हाथ धोएं"], "donts": ["पसीने से लथपथ होकर फ्रिज का ठंडा पानी न पिएं", "बंद कमरों में भीड़भाड़ से बचें"]},
        "when_to_see_doctor_en": "See a doctor if fever exceeds 102°F, cough produces rust-colored or foul phlegm, or persists longer than 2 weeks.",
        "when_to_see_doctor_hi": "यदि बुखार 102 डिग्री से ऊपर जाए, सांस लेने में दर्द हो या खांसी 2 हफ्ते से ज्यादा रहे तो डॉक्टर को दिखाएं (निमोनिया की जांच)।",
        "allergy_keywords": ["honey", "ghee", "tulsi", "ginger", "clove", "turmeric", "ajwain"],
        "sources": "National Health Portal (NHP India) & Ministry of AYUSH Respiratory Advisory"
    },
    "dehydration": {
        "id": "dehydration",
        "category_id": "general",
        "category_name": "💪 General Health & Lifestyle",
        "title_en": "Dehydration (Trishna / Fluid Deficit)",
        "title_hi": "शरीर में पानी की कमी (Dehydration)",
        "overview_en": "Excessive loss of bodily water and essential electrolytes, manifesting as dark yellow urine, dry mouth, dizziness, headaches, and sunken eyes.",
        "overview_hi": "शरीर में पानी और इलेक्ट्रोलाइट्स की कमी होना, जिससे पेशाब गहरा पीला आना, मुंह सूखना, सिर चकराना और कमजोरी होना।",
        "causes_en": ["Insufficient water consumption (<1.5L daily)", "Heavy sweating during summer heat or vigorous exercise", "Diarrhea or vomiting episodes", "Excessive tea, coffee, or alcohol causing diuretic fluid loss"],
        "causes_hi": ["दिनभर में कम पानी पीना", "गर्मियों में पसीना ज्यादा बहना", "उल्टी या दस्त होना", "ज्यादा चाय-कॉफी पीने से बार-बार पेशाब आना"],
        "ayurvedic_remedies_en": [
            "Shadanga Paniya (AYUSH Classic): Water boiled with 6 herbs (Musta, Chandana, Sunthi, Ushira, Parpata, Udichya) and cooled to room temp; premier thirst-quencher.",
            "Tender Coconut Water (Narikela Udaka) with pinch of rock salt.",
            "Lemon water with rock salt and raw honey."
        ],
        "ayurvedic_remedies_hi": [
            "षडंग पानीय (AYUSH शास्त्रीय विधि): नागरमोथा, चंदन, सौंठ और खस का उबला पानी (अत्यधिक प्यास और डिहाइड्रेशन का सर्वोत्तम पेय)।",
            "नारियल पानी में चुटकी भर सेंधा नमक डालकर पिएं।",
            "नींबू पानी में काला नमक और शहद मिलाकर पिएं।"
        ],
        "home_remedies_en": [
            "WHO-Standard ORS: Dissolve 1 sachet in 1 liter clean drinking water; sip continuously throughout the day.",
            "Homemade Electrolyte: 1 liter water + 6 level tsp sugar + 1/2 level tsp salt + juice of half a lemon.",
            "Watermelon and cucumber slices sprinkled with mint."
        ],
        "home_remedies_hi": [
            "डब्ल्यूएचओ (WHO) प्रमाणित ओआरएस (ORS) का घोल पिएं।",
            "घर पर जीवनरक्षक घोल: 1 लीटर पानी में 6 चम्मच चीनी, आधा चम्मच नमक और थोड़ा नींबू मिलाएं।",
            "तरबूज और खीरा खाएं।"
        ],
        "diet_nutrition_en": ["Hydrating foods: Cucumbers (96% water), watermelon, tomatoes, buttermilk, clear soups."],
        "diet_nutrition_hi": ["खीरा, तरबूज, संतरा, छाछ और नारियल पानी।"],
        "dos_and_donts_en": {"dos": ["Carry a reusable water bottle everywhere", "Monitor urine color: Pale straw yellow is the healthy target"], "donts": ["Do not wait until you are parched with thirst to drink", "Avoid high-sugar sodas for hydration"]},
        "dos_and_donts_hi": {"dos": ["अपने साथ पानी की बोतल रखें", "पेशाब का रंग देखें: हल्का पीला या पानी जैसा रंग सही हाइड्रेशन दर्शाता है"], "donts": ["प्यास से गला सूखने तक का इंतजार न करें", "प्यास बुझाने के लिए कोल्ड ड्रिंक न पिएं"]},
        "when_to_see_doctor_en": "CRITICAL: Seek emergency medical care for confusion, inability to urinate for >8 hours, rapid pulse, lethargy, or fainting (severe dehydration requires IV fluids).",
        "when_to_see_doctor_hi": "आपातकालीन चेतावनी: यदि 8 घंटे से पेशाब न आया हो, चक्कर आकर बेहोश हो जाएं, या धड़कन बहुत तेज हो तो तुरंत अस्पताल जाकर ग्लूकोज (IV ड्रिप) चढ़वाएं।",
        "allergy_keywords": ["coconut", "lemon", "honey"],
        "sources": "WHO Oral Rehydration Protocols & NHP India"
    },
    "poor_posture": {
        "id": "poor_posture",
        "category_id": "general",
        "category_name": "💪 General Health & Lifestyle",
        "title_en": "Poor Posture & Spinal Slouching",
        "title_hi": "गलत शारीरिक मुद्रा और झुककर बैठना (Poor Posture)",
        "overview_en": "Chronic forward head posture, rounded shoulders, and hunched upper back (kyphosis) resulting from prolonged desk work and smartphone viewing.",
        "overview_hi": "लगातार झुककर बैठना, गर्दन का आगे निकलना और कंधे झुक जाना, जिससे रीढ़ की हड्डी और मांसपेशियों में विकृति आती है।",
        "causes_en": ["Slouching over laptop screens and low desks", "Looking down at smartphones for hours ('Tech Neck')", "Weak core and back extensor muscles", "Carrying heavy one-sided shoulder bags"],
        "causes_hi": ["लैपटॉप पर झुककर काम करना", "घंटों नीचे गर्दन झुकाकर मोबाइल चलाना ('टेक नेक')", "पीठ और पेट की मांसपेशियों की कमजोरी", "एक कंधे पर भारी बैग लटकाना"],
        "ayurvedic_remedies_en": [
            "Bala Ashwagandha Taila Abhyanga: Daily self-massage to spine and shoulders strengthens paraspinal muscles.",
            "Yoga Asanas: Bhujangasana (Cobra), Dhanurasana (Bow), and Tadasana (Mountain Pose).",
            "Mahanarayan Taila application for tight trapezius muscles."
        ],
        "ayurvedic_remedies_hi": [
            "बला-अश्वगंधा तेल से रीढ़ और कंधों की मालिश मांसपेशियों को मजबूत करती है।",
            "योगासन: भुजंगासन, धनुरासन और ताड़ासन का रोजाना अभ्यास रीढ़ को सीधा करता है।",
            "कंधों की जकड़न पर महानारायण तेल लगाएं।"
        ],
        "home_remedies_en": [
            "Ergonomic Screen Setup: Elevate laptop so the top third of the screen is at eye level.",
            "Doorway Chest Stretch: Stand in a doorway, place elbows on frame at 90°, and lean forward for 30s to open tight pec muscles.",
            "Chin Tucks: Gently retract chin backward like making a double chin (hold 5s, repeat 10 times)."
        ],
        "home_remedies_hi": [
            "लैपटॉप स्क्रीन को आंखों की सीध में रखें (नीचे झुककर न देखें)।",
            "दरवाजे के फ्रेम में हाथ रखकर छाती को आगे झुकाएं और कंधों को स्ट्रेच करें।",
            "चिन टक व्यायाम: ठुड्डी को पीछे की तरफ खींचें और गर्दन सीधी रखें (10 बार दोहराएं)।"
        ],
        "diet_nutrition_en": ["Calcium & Vitamin D: Ragi, sesame seeds, paneer, fortified milk, and sunlight for bone density."],
        "diet_nutrition_hi": ["रागी, सफेद तिल, पनीर और धूप का सेवन हड्डियों को मजबूत रखता है।"],
        "dos_and_donts_en": {"dos": ["Keep feet flat on floor with hips at 90-100 degrees while sitting", "Set a posture alarm every 30 mins"], "donts": ["Do not cross legs while sitting at desk", "Do not cradle phone between shoulder and ear"]},
        "dos_and_donts_hi": {"dos": ["कुर्सी पर बैठते समय पैर जमीन पर सपाट रखें और पीठ सीधी", "हर 30 मिनट में सीधे बैठने की याद दिलाएं"], "donts": ["एक पैर पर दूसरा पैर चढ़ाकर न बैठें", "फोन को कंधे और कान के बीच दबाकर बात न करें"]},
        "when_to_see_doctor_en": "Consult a spine specialist or physiotherapist if posture triggers radiating numbness, tingling in hands or fingers, or severe spinal pain.",
        "when_to_see_doctor_hi": "यदि गलत बैठने से हाथों की उंगलियों में झनझनाहट या सुन्नपन आए (सर्वाइकल नस दबना) तो तुरंत डॉक्टर को दिखाएं।",
        "allergy_keywords": ["sesame", "dairy"],
        "sources": "ICMR Ergonomic Guidelines & AYUSH Yoga Therapy Protocols"
    },
    "back_pain_lifestyle": {
        "id": "back_pain_lifestyle",
        "category_id": "general",
        "category_name": "💪 General Health & Lifestyle",
        "title_en": "Back Pain (Lifestyle & Sedentary / Katishoola)",
        "title_hi": "कमर दर्द (बैठने के कारण) (Back Pain - Lifestyle)",
        "overview_en": "Aching stiffness and dull soreness in the lumbosacral spine caused by prolonged sitting, weak core muscles, or improper lifting mechanics.",
        "overview_hi": "लगातार बैठे रहने से कमर के निचले हिस्से में दर्द, जकड़न और उठने-बैठने में तकलीफ होना।",
        "causes_en": ["Prolonged sitting (>8 hours daily) weakening gluteal and core muscles", "Improper bending while lifting heavy household objects", "Sleeping on a sagging, overly soft mattress", "Excess abdominal weight straining lumbar spine"],
        "causes_hi": ["ऑफिस में 8-10 घंटे लगातार बैठे रहना", "गलत तरीके से झुककर भारी वजन उठाना", "बहुत ज्यादा नरम या पुराना गद्दा", "पेट की चर्बी बढ़ने से रीढ़ पर खिंचाव"],
        "ayurvedic_remedies_en": [
            "Kati Basti (AYUSH Special Therapy): Warm medicated oil (Mahanarayan / Sahacharadi) pooled over lumbar region in a dough reservoir.",
            "Yograj Guggulu: 2 tablets twice daily after meals relieves muscular stiffness.",
            "Dashamoola Kashayam: Decoction to pacify aggravated lumbar Vata.",
            "Castor oil (1 tsp in warm milk once weekly) cleanses colon and reduces lower back Vata tension."
        ],
        "ayurvedic_remedies_hi": [
            "कटि बस्ती (AYUSH विशेष चिकित्सा): कमर पर उड़द के आटे का घेरा बनाकर गुनगुना महानारायण तेल भरना (कमर दर्द का सबसे प्रसिद्ध इलाज)।",
            "योगराज गुग्गुलु: 2-2 गोली भोजन के बाद लें, कमर की जकड़न दूर होती है।",
            "दशमूल काढ़ा कमर के वात दोष को शांत करता है।",
            "हफ्ते में एक बार दूध में थोड़ा अरंडी का तेल मिलाकर पीने से कमर का दर्द कम होता है।"
        ],
        "home_remedies_en": [
            "Heat Therapy: Apply a heating pad or hot water bottle to the lower back for 15-20 minutes.",
            "Gentle Cat-Cow Yoga Stretch (Marjaryasana) 10 rounds to mobilize spinal discs.",
            "Bird-Dog exercise: Strengthens deep stabilizing multifidus muscles without spinal strain."
        ],
        "home_remedies_hi": [
            "कमर पर गर्म पानी की थैली (हीटिंग पैड) से 15-20 मिनट सिकाई करें।",
            "मार्जरी आसन (बिल्ली मुद्रा) में 10 बार रीढ़ को ऊपर-नीचे मोड़ें।",
            "हल्की वॉक करें; लगातार लेटे रहने की जगह थोड़ा टहलना बेहतर है।"
        ],
        "diet_nutrition_en": ["Anti-inflammatory spices: Turmeric, ginger, garlic. Calcium from sesame, ragi, and dairy. Avoid gas-producing foods (which aggravate Katishoola)."],
        "diet_nutrition_hi": ["हल्दी, अदरक, लहसुन और तिल। गैस बनाने वाली चीजों (जैसे राजमा, छोले) से बचें क्योंकि गैस से कमर दर्द बढ़ता है।"],
        "dos_and_donts_en": {"dos": ["Bend at the knees and hips (squat), not at the waist, when lifting heavy objects", "Use lumbar support pillow on your chair"], "donts": ["Do not stay in bed for >24 hours (prolonged bed rest delays back pain recovery)", "Avoid high heels"]},
        "dos_and_donts_hi": {"dos": ["नीचे से भारी सामान उठाते समय घुटने मोड़कर बैठें, कमर से न झुकें", "कुर्सी पर कमर के पीछे तकिया लगाएं"], "donts": ["कमर दर्द में कई दिन तक लगातार बिस्तर पर पड़े न रहें", "ऊंची हील वाले जूते-चप्पल न पहनें"]},
        "when_to_see_doctor_en": "RED FLAG: Seek emergency spine care if back pain radiates down the leg past the knee (Sciatica), or causes loss of bowel/bladder control or foot numbness (Cauda Equina Syndrome).",
        "when_to_see_doctor_hi": "आपातकालीन चेतावनी: यदि कमर दर्द पैर से होता हुआ पंजे तक जाए (साइटिका), या पेशाब/शौच पर नियंत्रण खो जाए तो बिना देर किए रीढ़ के सर्जन (Spine Surgeon) को दिखाएं।",
        "allergy_keywords": ["turmeric", "ginger", "garlic", "sesame", "dairy"],
        "sources": "National Health Portal (NHP India) & Ministry of AYUSH Musculoskeletal Guidelines"
    },
    "neck_pain_lifestyle": {
        "id": "neck_pain_lifestyle",
        "category_id": "general",
        "category_name": "💪 General Health & Lifestyle",
        "title_en": "Neck Pain & Tech Neck (Manya Stambha)",
        "title_hi": "गर्दन दर्द और टेक-नेक (Neck Pain & Tech Neck)",
        "overview_en": "Stiffness, muscle spasm, and soreness in the cervical spine and trapezius muscles caused by looking down at screens and bad sleeping postures.",
        "overview_hi": "गर्दन में अकड़न, दर्द और सिर घुमाने में परेशानी, जो मोबाइल और लैपटॉप पर लगातार गर्दन झुकाकर देखने से होती है।",
        "causes_en": ["Looking down at mobile phones (tilting head 60° puts 27 kg of pressure on cervical spine)", "Using multiple thick pillows while sleeping", "Holding phone against shoulder with cheek", "Draft of cold air-conditioner blowing directly on the neck"],
        "causes_hi": ["मोबाइल में नीचे देखकर गर्दन पर 27 किलो का अतिरिक्त दबाव डालना", "सोते समय बहुत ऊंचा या 2-2 तकिए लगाना", "कंधे और गाल से फोन दबाना", "एसी की ठंडी हवा सीधे गर्दन पर लगना"],
        "ayurvedic_remedies_en": [
            "Greeva Basti: Medicated warm oil retention on cervical spine.",
            "Mahanarayan Taila or Ksheerabala Taila gentle massage to neck and shoulders.",
            "Ekangaveer Ras or Trayodashanga Guggulu under physician supervision."
        ],
        "ayurvedic_remedies_hi": [
            "ग्रीवा बस्ती: गर्दन पर औषधीय तेल का घेरा बनाकर सिकाई करना (सर्वाइकल का अचूक इलाज)।",
            "महानारायण या क्षीरबला तेल से गर्दन और कंधों की हल्के हाथ से मालिश।",
            "त्रयोदशांग गुग्गुलु का सेवन नसों की जकड़न खोलता है।"
        ],
        "home_remedies_en": [
            "Warm Sesame Oil compress followed by hot towel fomentation.",
            "Neck Isometric Exercises: Press forehead against palm (hold 5s), then back of head, then left and right temples without moving neck.",
            "Hold mobile phone at eye level rather than dropping head downward."
        ],
        "home_remedies_hi": [
            "गुनगुने तिल के तेल की मालिश के बाद गर्म तौलिए से 10 मिनट भाप दें।",
            "आइसोमेट्रिक गर्दन व्यायाम: हथेली से माथे और सिर के पीछे हल्का दबाव डालें बिना गर्दन हिलाए (10 सेकंड)।",
            "मोबाइल फोन को आंखों की ऊंचाई पर रखकर चलाएं, गर्दन न झुकाएं।"
        ],
        "diet_nutrition_en": ["Anti-inflammatory turmeric milk with dry ginger (Sunthi). Adequate hydration for cervical disc fluid."],
        "diet_nutrition_hi": ["हल्दी और सौंठ वाला गुनगुना दूध पिएं और खूब पानी पिएं ताकि रीढ़ की डिस्क में सूखापन न आए।"],
        "dos_and_donts_en": {"dos": ["Use a contoured ergonomic cervical pillow", "Take neck mobility breaks every 30 mins"], "donts": ["Do not crack your neck aggressively with your hands", "Avoid sleeping on your stomach with neck twisted"]},
        "dos_and_donts_hi": {"dos": ["पतला और गर्दन के अनुकूल तकिया लगाएं", "हर आधे घंटे में गर्दन को दाएं-बाएं धीरे-धीरे घुमाएं"], "donts": ["गर्दन को हाथ से पकड़कर झटके से न चटकाएं", "पेट के बल गर्दन मोड़कर न सोएं"]},
        "when_to_see_doctor_en": "Consult an orthopedic/spine specialist if neck pain radiates down your arm into fingers, or causes loss of hand grip strength or balance problems.",
        "when_to_see_doctor_hi": "यदि गर्दन का दर्द हाथ या उंगलियों में बिजली के करंट जैसा दौड़े, या हाथ की पकड़ कमजोर होने लगे तो तुरंत डॉक्टर को दिखाएं।",
        "allergy_keywords": ["sesame", "milk", "dairy", "turmeric", "ginger"],
        "sources": "ICMR Guidelines on Cervical Spondylosis & AYUSH Protocols"
    },
    "poor_circulation": {
        "id": "poor_circulation",
        "category_id": "general",
        "category_name": "💪 General Health & Lifestyle",
        "title_en": "Poor Circulation (Cold Hands & Feet / Rasa Samvahana)",
        "title_hi": "रक्त संचार की कमजोरी (Poor Circulation)",
        "overview_en": "Sluggish peripheral blood flow causing chronically cold fingers, toes, pale nail beds, numbness, and slow wound healing.",
        "overview_hi": "हाथ और पैरों का हमेशा ठंडा रहना, उंगलियों में सुन्नपन और झनझनाहट जो कमजोर ब्लड सर्कुलेशन का संकेत है।",
        "causes_en": ["Sedentary lifestyle and lack of cardiovascular movement", "Smoking causing peripheral vasoconstriction", "Low hemoglobin (Anemia) or Raynaud's phenomenon", "High cholesterol or early arterial narrowing"],
        "causes_hi": ["कसरत और पैदल चलने की कमी", "सिगरेट-बीड़ी से नसों का सिकुड़ना", "खून की कमी (एनीमिया) या ठंड से नसों का सिकुड़ना", "कोलेस्ट्रॉल का बढ़ना"],
        "ayurvedic_remedies_en": [
            "Arjuna Churna: 1/2 tsp boiled with milk or water supports coronary and peripheral endothelial circulation.",
            "Ginger (Sunthi) & Black Pepper tea enhances peripheral microcirculation.",
            "Whole-body Abhyanga with warm Mustard or Sesame oil followed by warm bath."
        ],
        "ayurvedic_remedies_hi": [
            "अर्जुन की छाल का काढ़ा: आधा चम्मच अर्जुन पाउडर दूध या पानी में उबालकर पिएं (नसों और दिल के लिए अमृत)।",
            "सोंठ और काली मिर्च की चाय रक्त संचार तेज करती है।",
            "गुनगुने सरसों या तिल के तेल से पूरे शरीर की मालिश करके गर्म पानी से नहाएं।"
        ],
        "home_remedies_en": [
            "Brisk 30-minute daily walking instantly forces calf muscle pumps to return venous blood.",
            "Contrast Foot Bath: Alternate soaking feet in warm water for 3 mins and cold water for 1 min (3 cycles).",
            "Elevate legs on a pillow for 15 minutes in the evening."
        ],
        "home_remedies_hi": [
            "रोजाना 30 मिनट तेज गति से पैदल चलें, इससे पिंडलियां खून को तेजी से पंप करती हैं।",
            "कंट्रास्ट बाथ: 3 मिनट गुनगुने पानी में और 1 मिनट ठंडे पानी में पैर डालें (रक्त नलियां खुलती हैं)।",
            "शाम को दीवार के सहारे पैर 15 मिनट ऊपर उठाकर लेटें।"
        ],
        "diet_nutrition_en": ["Nitric oxide boosters: Beetroot juice, garlic, pomegranate, walnuts, and citrus fruits."],
        "diet_nutrition_hi": ["चुकंदर का रस, लहसुन, अनार, अखरोट और खट्टे फल (नसों को चौड़ा करते हैं)।"],
        "dos_and_donts_en": {"dos": ["Wear warm woollen socks in winter", "Stay well hydrated"], "donts": ["Quit smoking completely (nicotine shuts down peripheral capillaries)", "Avoid tight restrictive socks"]},
        "dos_and_donts_hi": {"dos": ["सर्दियों में गर्म मोजे पहनें", "खूब पानी पिएं"], "donts": ["धूम्रपान तुरंत छोड़ें (यह नसों को बंद कर देता है)", "बहुत तंग इलास्टिक वाले मोजे न पहनें"]},
        "when_to_see_doctor_en": "Consult a vascular surgeon immediately if fingers turn ghostly white then blue in cold (Raynaud's), or if you develop leg pain while walking that stops when resting (Claudication / PAD).",
        "when_to_see_doctor_hi": "यदि ठंड में उंगलियां नीली या सफेद पड़ जाएं, या चलने पर पिंडलियों में असहनीय दर्द हो जो रुकने पर ठीक हो जाए तो तुरंत वैस्कुलर डॉक्टर को दिखाएं।",
        "allergy_keywords": ["milk", "dairy", "mustard", "sesame", "walnut", "garlic", "pomegranate"],
        "sources": "ICMR Guidelines on Peripheral Arterial Health & Ministry of AYUSH"
    },
    "hormonal_imbalance_general": {
        "id": "hormonal_imbalance_general",
        "category_id": "general",
        "category_name": "💪 General Health & Lifestyle",
        "title_en": "Hormonal Imbalance (General / Dhatu Asamtulana)",
        "title_hi": "सामान्य हार्मोनल असंतुलन (Hormonal Imbalance)",
        "overview_en": "Systemic endocrine dysregulation affecting metabolism, mood, weight, and reproductive rhythms, driven by chronic stress and endocrine-disrupting chemicals.",
        "overview_hi": "हार्मोनल संतुलन बिगड़ना, जिससे वजन अचानक बढ़ना/घटना, चेहरे पर बाल या मुँहासे, मूड स्विंग्स और थकान होना।",
        "causes_en": ["Chronic cortisol elevation suppressing thyroid and sex hormones", "Endocrine-disrupting chemicals (plastics, BPA, phthalates, pesticides)", "Insulin resistance from refined sugar and white flour", "Disrupted sleep and circadian rhythms"],
        "causes_hi": ["तनाव से कोर्टिसोल का लगातार बढ़ा रहना", "प्लास्टिक की बोतलों और बर्तनों का अधिक प्रयोग (BPA)", "मीठे और मैदे से इंसुलिन का बिगड़ना", "रात में देर से सोना"],
        "ayurvedic_remedies_en": [
            "Ashwagandha & Shatavari: Combined adaptogenic therapy to balance hypothalamic-pituitary-adrenal (HPA) axis.",
            "Kanchnar Guggulu: Classical Ayurvedic medicine for glandular swelling, thyroid, and cysts.",
            "Triphala daily to promote hepatic estrogen clearance."
        ],
        "ayurvedic_remedies_hi": [
            "अश्वगंधा और शतावरी का चूर्ण: दोनों को मिलाकर दूध के साथ लेने से शरीर के सभी हार्मोन्स संतुलित होते हैं।",
            "कांचनार गुग्गुलु: थायराइड, गांठों और हार्मोनल असंतुलन की प्रमुख आयुर्वेदिक औषधि।",
            "रोज रात को त्रिफला लें ताकि लिवर अतिरिक्त हार्मोन्स को शरीर से बाहर निकाल सके।"
        ],
        "home_remedies_en": [
            "Switch from plastic containers to glass, stainless steel, or clay vessels for food and water.",
            "Seed Cycling: Pumpkin & Flaxseeds during days 1-14; Sunflower & Sesame seeds during days 15-28 (for women).",
            "30 minutes of daily moderate exercise reduces insulin and cortisol."
        ],
        "home_remedies_hi": [
            "प्लास्टिक के बर्तनों और बोतलों को त्यागें; कांच, मिट्टी या स्टील के बर्तन अपनाएं।",
            "सीड साइकिलिंग: अलसी और कद्दू के बीज पहले 14 दिन; तिल और सूरजमुखी के बीज अगले 14 दिन खाएं।",
            "रोजाना 30 मिनट कसरत करने से इंसुलिन सही रहता है।"
        ],
        "diet_nutrition_en": ["Cruciferous vegetables (cabbage, broccoli) aid estrogen metabolism. High fiber millets, green tea, healthy fats from seeds."],
        "diet_nutrition_hi": ["हरी सब्जियां, पत्तागोभी, ब्रोकली, मोटे अनाज और अलसी। सफेद चीनी और रिफाइंड तेल बंद करें।"],
        "dos_and_donts_en": {"dos": ["Sleep by 10:30 PM (melatonin regulates endocrine clocks)", "Manage stress"], "donts": ["Avoid reheating food in plastic in the microwave", "Avoid crash starvation diets"]},
        "dos_and_donts_hi": {"dos": ["रात 10:30 बजे तक सो जाएं", "तनाव मुक्त रहें"], "donts": ["प्लास्टिक के डिब्बे में खाना माइक्रोवेव में गर्म न करें", "अचानक भूखे रहकर डाइटिंग न करें"]},
        "when_to_see_doctor_en": "Consult an endocrinologist for comprehensive blood tests (Thyroid panel, Fasting Insulin, Cortisol, LH/FSH) if experiencing rapid unexplained weight changes, hair loss, or menstrual cessation.",
        "when_to_see_doctor_hi": "यदि अचानक बहुत ज्यादा वजन बढ़े या घटे, बाल तेजी से झड़ें या माहवारी बंद हो जाए तो एंडोक्रिनोलॉजिस्ट से मिलकर खून की जांच करवाएं।",
        "allergy_keywords": ["milk", "dairy", "flaxseed", "sesame"],
        "sources": "ICMR Guidelines on Endocrine Health & Ministry of AYUSH Dhatu Care"
    },
    "brain_fog": {
        "id": "brain_fog",
        "category_id": "general",
        "category_name": "💪 General Health & Lifestyle",
        "title_en": "Brain Fog (Mental Cloudiness / Buddhi Manda)",
        "title_hi": "दिमाग का सुन्न होना और अस्पष्टता (Brain Fog)",
        "overview_en": "Subjective feeling of mental blunting, forgetfulness, lack of mental clarity, slow processing speed, and feeling detached or 'in a cloud'.",
        "overview_hi": "दिमाग का ठीक से काम न करना, सोच में धुंधलापन, सोचने-समझने की गति धीमी होना और किसी काम पर फोकस न कर पाना।",
        "causes_en": ["Systemic low-grade neuroinflammation (post-COVID, chronic allergies)", "Vitamin B12, Iron, or Vitamin D3 deficiency", "Gut dysbiosis and leaky gut (gut-brain axis impairment)", "Blood sugar spikes and subsequent reactive hypoglycemia"],
        "causes_hi": ["वायरल बुखार (जैसे पोस्ट-कोविड) के बाद नसों में सूजन", "विटामिन B12, डी या हीमोग्लोबिन की कमी", "पेट और आंतों की खराबी (गट-ब्रेन कनेक्शन)", "मीठा खाने के बाद ब्लड शुगर का तेजी से गिरना"],
        "ayurvedic_remedies_en": [
            "Brahmi & Shankhpushpi Syrup: 2 tsp twice daily sharpens cognition and clears neurological fog.",
            "Nasya with pure Cow Ghee (2 drops in each nostril in morning resets cranial senses).",
            "Suvarna Vasant Malti Ras or Ashwagandha Rasayana under physician supervision."
        ],
        "ayurvedic_remedies_hi": [
            "ब्राह्मी और शंखपुष्पी सिरप: दिन में दो बार 2 चम्मच लें (दिमाग की धुंध को साफ करता है)।",
            "गाय के घी का नस्य: सुबह दोनों नथुनों में 2-2 बूंद घी डालने से मस्तिष्क के संवेदी अंग खुलते हैं।",
            "अश्वगंधा रसायन का सेवन करें।"
        ],
        "home_remedies_en": [
            "Cold Water Face Plunge: Submerge face in cold water for 15 seconds to stimulate vagus nerve and reset alertness.",
            "Electrolyte Hydration: Drink 500ml water with a pinch of rock salt and lemon first thing in morning.",
            "10-minute high-intensity walk in fresh cold morning air."
        ],
        "home_remedies_hi": [
            "चेहरे पर बर्फ के ठंडे पानी के छींटे मारें (वेगस नर्व सक्रिय होती है और दिमाग तुरंत जागता है)।",
            "सुबह उठते ही गुनगुने पानी में थोड़ा नींबू और सेंधा नमक डालकर पिएं।",
            "सुबह ताजी हवा में 10 मिनट तेज चाल से टहलें।"
        ],
        "diet_nutrition_en": ["Ketone-friendly brain fuels: Virgin coconut oil (medium-chain triglycerides), soaked walnuts, blueberries, eggs, and leafy greens."],
        "diet_nutrition_hi": ["नारियल तेल, भीगे अखरोट, पालक, अंडे और जामुन। मैदे और चीनी से बचें।"],
        "dos_and_donts_en": {"dos": ["Get blood levels of B12, D3, and TSH checked", "Prioritize 8 hours of sleep"], "donts": ["Do not consume heavy carb breakfasts like 4 parathas with sweet tea", "Avoid multitasking"]},
        "dos_and_donts_hi": {"dos": ["विटामिन B12 और D3 की जांच जरूर करवाएं", "8 घंटे की पूरी नींद लें"], "donts": ["नाश्ते में बहुत ज्यादा तला-भुना या मीठा न खाएं (इससे दिमाग सुस्त होता है)", "एक साथ कई काम न करें"]},
        "when_to_see_doctor_en": "See a neurologist if brain fog is accompanied by slurred speech, motor clumsiness, facial drooping, or sudden severe confusion.",
        "when_to_see_doctor_hi": "यदि दिमागी धुंध के साथ बोलने में लड़खड़ाहट, हाथ-पैर में कमजोरी या गंभीर भ्रम हो तो तुरंत आपातकालीन न्यूरोलॉजिस्ट को दिखाएं।",
        "allergy_keywords": ["ghee", "shankhpushpi", "walnut", "coconut"],
        "sources": "National Health Portal (NHP India) & ICMR Guidelines on Neuro-Cognitive Health"
    },

    # ==========================================
    # CATEGORY 8: 👶 Women-Specific (7 issues)
    # ==========================================
    "heavy_periods": {
        "id": "heavy_periods",
        "category_id": "women",
        "category_name": "👶 Women-Specific",
        "title_en": "Heavy Periods (Menorrhagia - Mild / Asrigdara)",
        "title_hi": "माहवारी में अत्यधिक रक्तस्राव (Heavy Periods)",
        "overview_en": "Excessive or prolonged menstrual bleeding (>7 days or soaking a pad every 2 hours), leading to fatigue, pallor, and iron-deficiency anemia.",
        "overview_hi": "पीरियड्स के दौरान बहुत ज्यादा ब्लीडिंग होना, 7 दिन से अधिक चलना और हर 1-2 घंटे में पैड बदलना पड़ना।",
        "causes_en": ["Hormonal imbalance (estrogen dominance with low progesterone)", "Uterine fibroids or endometrial polyps", "PCOS or thyroid disorders", "Bleeding disorders or copper-IUD side effect"],
        "causes_hi": ["एस्ट्रोजन और प्रोजेस्टेरोन हार्मोन का असंतुलन", "गर्भाशय में रसौली (फाइब्रॉएड) या सिस्ट", "थायराइड या पीसीओएस (PCOS)", "कॉपर-टी (IUD) का दुष्प्रभाव"],
        "ayurvedic_remedies_en": [
            "Ashokarishta: 15-20 ml with equal water twice daily after meals (the supreme classical uterine tonic for heavy flow).",
            "Lodhrasava or Pushyanug Churna with rice water (tandulodaka).",
            "Praval Pishti with honey helps coagulate and pacify Pitta bleeding.",
            "Shatavari Churna with milk supports ovarian hormonal balance."
        ],
        "ayurvedic_remedies_hi": [
            "अशोकारिष्ट: 15-20 मिली बराबर पानी मिलाकर भोजन के बाद लें (माहवारी के ज्यादा रक्तस्राव की सबसे प्रसिद्ध दवा)।",
            "लोध्रासव या पुष्यानुग चूर्ण: चावल के पानी (तंदुलोदक) के साथ सेवन करें।",
            "प्रवाल पिष्टी शहद के साथ लेने से अतिरिक्त ब्लीडिंग रुकती है।",
            "शतावरी चूर्ण दूध के साथ लें।"
        ],
        "home_remedies_en": [
            "Coriander Seed Decoction: Boil 20g coriander seeds in 200ml water until reduced to 50ml; strain and sip twice daily.",
            "Pomegranate peel or juice: Natural astringent tannins reduce excessive uterine capillary permeability.",
            "Rest with elevated legs during heavy flow days."
        ],
        "home_remedies_hi": [
            "धनिया के बीज का काढ़ा: 2 चम्मच साबुत धनिया 1 गिलास पानी में उबालकर आधा रहने पर पिएं।",
            "अनार का ताजा रस पिएं (यह खून बढ़ाता है और ब्लीडिंग नियंत्रित करता है)।",
            "ज्यादा ब्लीडिंग के दिनों में भारी काम न करें और आराम करें।"
        ],
        "diet_nutrition_en": ["Iron replenishment: Spinach, beetroot, black raisins, jaggery with sesame, dates, and lentils. Vitamin C (amla) to enhance iron absorption."],
        "diet_nutrition_hi": ["आयरन से भरपूर भोजन: पालक, चुकंदर, मुनक्का, गुड़, तिल और खजूर। आंवला जरूर खाएं ताकि आयरन शरीर में सोख सके।"],
        "dos_and_donts_en": {"dos": ["Get a CBC and pelvic ultrasound done", "Stay well hydrated"], "donts": ["Avoid hot, spicy, sour, and fermented foods during periods", "Do not perform intense heavy workouts during heavy bleeding"]},
        "dos_and_donts_hi": {"dos": ["खून की जांच (हीमोग्लोबिन) और पेल्विक अल्ट्रासाउंड जरूर कराएं", "खूब पानी पिएं"], "donts": ["पीरियड्स में ज्यादा मिर्च-मसाले, अचार और खटाई न खाएं", "ज्यादा ब्लीडिंग में भारी वजन या कसरत न करें"]},
        "when_to_see_doctor_en": "EMERGENCY: Seek immediate gynecological attention if soaking 2 pads per hour for 2 consecutive hours, passing blood clots larger than a coin, or feeling dizzy and faint.",
        "when_to_see_doctor_hi": "आपातकालीन चेतावनी: यदि 2 घंटे तक लगातार हर घंटे 2 पैड भीग रहे हों, बड़े-बड़े खून के थक्के आएं या चक्कर आकर बेहोशी छाए तो तुरंत अस्पताल जाएं।",
        "allergy_keywords": ["milk", "dairy", "coriander", "pomegranate", "sesame", "raisins"],
        "sources": "Ministry of AYUSH Stri-Roga Guidelines & ICMR Anemia Control Protocol"
    },
    "period_cramps": {
        "id": "period_cramps",
        "category_id": "women",
        "category_name": "👶 Women-Specific",
        "title_en": "Period Cramps (Dysmenorrhea / Kashtartava)",
        "title_hi": "माहवारी का दर्द और ऐंठन (Period Cramps)",
        "overview_en": "Throbbing or cramping pains in the lower abdomen, lower back, and inner thighs before and during menstruation caused by uterine prostaglandins.",
        "overview_hi": "माहवारी के दौरान या पहले पेट के निचले हिस्से, कमर और जांघों में असहनीय मरोड़ और दर्द होना।",
        "causes_en": ["Excess uterine prostaglandins triggering intense muscle contractions", "Aggravated Apana Vata obstructing natural pelvic downward flow", "Endometriosis or adenomyosis", "High stress and lack of magnesium"],
        "causes_hi": ["गर्भाशय में प्रोस्टाग्लैंडीन हार्मोन की अधिकता से मांसपेशियों का सिकुड़ना", "अपान वात का असंतुलन", "एंडोमेट्रियोसिस या रसौली", "तनाव और मैग्नीशियम की कमी"],
        "ayurvedic_remedies_en": [
            "Dashamoolarishta: 15 ml with equal water twice daily after meals calms pelvic Apana Vata.",
            "Castor Oil Compress: Warm castor oil applied to lower belly with a hot water bottle.",
            "Raja Pravartini Vati under Ayurvedic physician supervision for spasmodic dysmenorrhea.",
            "Ginger & Ajwain Kwath with jaggery."
        ],
        "ayurvedic_remedies_hi": [
            "दशमूलारिष्ट: 15 मिली बराबर पानी मिलाकर भोजन के बाद लें (गर्भाशय के दर्द और ऐंठन की सबसे श्रेष्ठ दवा)।",
            "अरंडी (कैस्टर) के तेल की मालिश: पेट के निचले हिस्से में गुनगुने तेल की मालिश के बाद गर्म पानी की बोतल से सिकाई करें।",
            "रजःप्रवर्तिनी वटी का सेवन आयुर्वेदिक चिकित्सक की सलाह से करें।",
            "अदरक और अजवाइन का काढ़ा गुड़ डालकर पिएं।"
        ],
        "home_remedies_en": [
            "Hot Water Bag: Applying continuous heat to lower abdomen relaxes myometrial contractions as effectively as ibuprofen.",
            "Warm Chamomile or Fennel (Saunf) Tea: Fennel inhibits prostaglandin synthesis.",
            "Gentle Child's Pose (Balasana) and Supta Baddha Konasana."
        ],
        "home_remedies_hi": [
            "गर्म पानी की थैली (हॉट वॉटर बैग) से पेट के निचले हिस्से की सिकाई करें (दर्द निवारक गोली जितना असरदार)।",
            "सौंफ की चाय: 1 चम्मच सौंफ पानी में उबालकर गुनगुनी पिएं (गर्भाशय की ऐंठन खोलती है)।",
            "बालासन और बटरफ्लाई आसन में हल्के से बैठें।"
        ],
        "diet_nutrition_en": ["Magnesium & Omega-3 foods: Dark chocolate (70%+), pumpkin seeds, walnuts, bananas, and warm ginger water. Avoid salty, processed snacks."],
        "diet_nutrition_hi": ["कद्दू के बीज, अखरोट, केला और डार्क चॉकलेट (मैग्नीशियम से भरपूर)। ज्यादा नमक और चिप्स से बचें (यह सूजन बढ़ाते हैं)।"],
        "dos_and_donts_en": {"dos": ["Sip warm fluids throughout the day", "Rest comfortably with knees drawn up"], "donts": ["Avoid cold water, ice creams, and cold drinks during cramps", "Avoid caffeine which constricts pelvic vessels"]},
        "dos_and_donts_hi": {"dos": ["दिनभर गुनगुना पानी पिएं", "घुटने मोड़कर आराम से लेटें"], "donts": ["पीरियड्स में फ्रिज का ठंडा पानी और आइसक्रीम न खाएं", "चाय-कॉफी कम करें क्योंकि ये नसों को सिकोड़ती हैं"]},
        "when_to_see_doctor_en": "Consult a gynecologist if pain is incapacitating, worsens progressively over months, causes vomiting, or does not respond to standard pain relief (rule out Endometriosis).",
        "when_to_see_doctor_hi": "यदि दर्द इतना तेज हो कि बिस्तर से उठना नामुमकिन हो, उल्टी हो या हर महीने दर्द बढ़ता जाए तो एंडोमेट्रियोसिस की जांच के लिए गायनेकोलॉजिस्ट से मिलें।",
        "allergy_keywords": ["ajwain", "ginger", "fennel", "walnut"],
        "sources": "National Health Portal (NHP India) & Ministry of AYUSH Kashtartava Protocol"
    },
    "pms_symptoms": {
        "id": "pms_symptoms",
        "category_id": "women",
        "category_name": "👶 Women-Specific",
        "title_en": "PMS Symptoms (Premenstrual Syndrome)",
        "title_hi": "पीएमएस के लक्षण (Premenstrual Syndrome)",
        "overview_en": "Physical and emotional symptoms (bloating, breast tenderness, mood swings, fatigue, sugar cravings) occurring 5-10 days before menstruation.",
        "overview_hi": "माहवारी शुरू होने से 5-10 दिन पहले चिड़चिड़ापन, स्तनों में भारीपन, पेट फूलना, सिरदर्द और अचानक उदासी होना।",
        "causes_en": ["Abrupt drop in estrogen and progesterone post-ovulation", "Transient dip in serotonin neurotransmitter levels", "Water and sodium retention from aldosterone shifts", "Nutritional deficiencies in Magnesium and Vitamin B6"],
        "causes_hi": ["ओव्यूलेशन के बाद हार्मोन्स का तेजी से गिरना", "दिमाग में सेरोटोनिन (खुशी के हार्मोन) की कमी", "शरीर में पानी का जमा होना (ब्लोटिंग)", "मैग्नीशियम और विटामिन बी6 की कमी"],
        "ayurvedic_remedies_en": [
            "Shatavari Gulam or Churna: 1 tsp with warm milk pacifies premenstrual Vata-Pitta swings.",
            "Ashokarishta in the second half of the cycle.",
            "Brahmi Vati to stabilize emotional mood volatility."
        ],
        "ayurvedic_remedies_hi": [
            "शतावरी चूर्ण: 1 चम्मच गुनगुने दूध के साथ लें (हार्मोन्स को संतुलित कर पीएमएस के लक्षण मिटाता है)।",
            "माहवारी से 10 दिन पहले अशोकारिष्ट लेना शुरू करें।",
            "ब्राह्मी वटी चिड़चिड़ापन और मूड स्विंग्स को शांत करती है।"
        ],
        "home_remedies_en": [
            "Reduce Sodium: Cut salt intake in the 7 days before periods to prevent fluid retention and breast soreness.",
            "Magnesium + Vitamin B6: Eat 1 banana and a handful of sunflower/pumpkin seeds daily.",
            "30 minutes of aerobic walking or yoga releases endorphins."
        ],
        "home_remedies_hi": [
            "नमक कम करें: पीरियड्स से 7 दिन पहले खाने में नमक कम कर दें ताकि शरीर में सूजन और भारीपन न आए।",
            "रोजाना 1 केला और सूरजमुखी/कद्दू के बीज खाएं।",
            "रोज 30 मिनट टहलें या योग करें।"
        ],
        "diet_nutrition_en": ["Complex carbs: Oats, sweet potatoes, whole grain roti. Cut white sugar to avoid mood crashes. Herbal teas (chamomile, peppermint)."],
        "diet_nutrition_hi": ["ओट्स, शकरकंद और दलिया खाएं। सफेद चीनी और ज्यादा कॉफी से बचें ताकि मूड न बिगड़े।"],
        "dos_and_donts_en": {"dos": ["Prioritize 8 hours of sleep", "Wear a supportive, non-wired cotton bra for breast tenderness"], "donts": ["Avoid caffeine and alcohol 7 days before periods", "Avoid high-sugar binges"]},
        "dos_and_donts_hi": {"dos": ["8 घंटे की अच्छी नींद लें", "स्तनों में भारीपन हो तो आरामदायक कॉटन ब्रा पहनें"], "donts": ["पीरियड्स से पहले शराब और चाय-कॉफी कम करें", "मीठी चीजों पर टूट पड़ने से बचें"]},
        "when_to_see_doctor_en": "Consult a doctor if emotional symptoms are severe enough to disrupt relationships, work, or cause depression (Premenstrual Dysphoric Disorder - PMDD requires medical therapy).",
        "when_to_see_doctor_hi": "यदि पीएमएस के दौरान अत्यधिक अवसाद, खुद को चोट पहुंचाने के विचार या रिश्तों में गंभीर तनाव आने लगे (PMDD) तो तुरंत डॉक्टर से मिलें।",
        "allergy_keywords": ["milk", "dairy", "peppermint"],
        "sources": "ICMR Guidelines on Women's Health & Ministry of AYUSH"
    },
    "hormonal_acne_women": {
        "id": "hormonal_acne_women",
        "category_id": "women",
        "category_name": "👶 Women-Specific",
        "title_en": "Hormonal Acne (Women / Mukhadushika)",
        "title_hi": "हार्मोनल मुँहासे (Hormonal Acne in Women)",
        "overview_en": "Deep, painful cystic bumps primarily located along the jawline, chin, and lower cheeks, flaring up cyclically before menstrual periods or in PCOS.",
        "overview_hi": "ठुड्डी, जबड़े और गालों के निचले हिस्से पर दर्दनाक लाल फुंसियां और गाठें, जो पीरियड्स से पहले या पीसीओएस (PCOS) में बढ़ जाती हैं।",
        "causes_en": ["Relative androgen excess (high DHEA or testosterone) stimulating sebaceous glands", "Insulin spikes driving ovarian androgen production", "PCOS (Polycystic Ovary Syndrome)", "Pitta and Rakta vitiation in Ayurvedic physiology"],
        "causes_hi": ["शरीर में पुरुष हार्मोन (एंड्रोजन/टेस्टोस्टेरोन) का बढ़ना", "इंसुलिन का बढ़ना जिससे चेहरे की ग्रंथियां ज्यादा तेल बनाती हैं", "पीसीओएस (PCOS) की समस्या", "खून और पित्त में खराबी"],
        "ayurvedic_remedies_en": [
            "Kanchnar Guggulu: 2 tablets twice daily after meals dissolves cystic hormonal build-up.",
            "Manjishtadi Kwath: Premier Ayurvedic blood purifier for clearing chronic inflammatory skin eruptions.",
            "Lodhra & Neem Paste applied topically to cystic breakouts.",
            "Khadirarishta for purifying Rakta dhatu."
        ],
        "ayurvedic_remedies_hi": [
            "कांचनार गुग्गुलु: 2-2 गोली भोजन के बाद लें (हार्मोनल गांठों और मुंहासों को अंदर से सुखाती है)।",
            "मंजिष्ठादि काढ़ा: खून साफ करने वाली प्रसिद्ध दवा जो चेहरे के मुंहासे जड़ से मिटाती है।",
            "लोध्र और नीम का लेप मुंहासों पर लगाएं।",
            "खदिरारिष्ट का सेवन करें।"
        ],
        "home_remedies_en": [
            "Spearmint Tea: Drink 1 cup daily; clinical studies show spearmint has mild natural anti-androgenic effects in women.",
            "Neem & Multani Mitti Face Pack with rose water applied twice weekly.",
            "Wash pillowcases twice a week in unscented detergent."
        ],
        "home_remedies_hi": [
            "स्पीयरमिंट (पहाड़ी पुदीना) चाय: रोजाना 1 कप पिएं; यह महिलाओं में अतिरिक्त एंड्रोजन हार्मोन को कम करती है।",
            "नीम और मुल्तानी मिट्टी में गुलाब जल मिलाकर हफ्ते में दो बार लगाएं।",
            "तकिए का कवर हफ्ते में दो बार बदलें।"
        ],
        "diet_nutrition_en": ["Eliminate cow dairy and high-glycemic sugar for 30 days (dairy contains IGF-1 which fuels hormonal breakouts). Eat zinc-rich pumpkin seeds and cruciferous veggies."],
        "diet_nutrition_hi": ["30 दिन के लिए दूध, पनीर और मीठा बंद करके देखें (डेयरी उत्पाद हार्मोनल मुँहासे भड़काते हैं)। कद्दू के बीज और हरी सब्जियां खाएं।"],
        "dos_and_donts_en": {"dos": ["Use non-comedogenic, oil-free skincare", "Manage stress through yoga"], "donts": ["Never squeeze or pop deep cystic jawline bumps (causes severe scarring)", "Do not scrub face harshly"]},
        "dos_and_donts_hi": {"dos": ["ऑयल-फ्री फेसवॉश का प्रयोग करें", "तनाव कम रखें"], "donts": ["ठुड्डी के मुंहासों को कभी न फोड़ें (गहरे गड्ढे बन जाते हैं)", "चेहरे को खुरदरे तौलिए से न रगड़ें"]},
        "when_to_see_doctor_en": "Consult a dermatologist or gynecologist if acne is accompanied by irregular periods, excess facial hair (hirsutism), or scalp hair thinning (to screen for PCOS).",
        "when_to_see_doctor_hi": "यदि मुंहासों के साथ पीरियड्स अनियमित हों या चेहरे/ठुड्डी पर मोटे बाल आ रहे हों तो पीसीओएस (PCOS) की जांच के लिए डॉक्टर से मिलें।",
        "allergy_keywords": ["neem", "spearmint", "dairy", "multani_mitti"],
        "sources": "Ministry of AYUSH Mukhadushika Protocols & ICMR PCOS Guidelines"
    },
    "pregnancy_wellness_tips": {
        "id": "pregnancy_wellness_tips",
        "category_id": "women",
        "category_name": "👶 Women-Specific",
        "title_en": "Pregnancy Tips (General Wellness / Garbhini Paricharya)",
        "title_hi": "गर्भावस्था में सामान्य स्वास्थ्य (Pregnancy Wellness)",
        "overview_en": "Evidence-based, safe Ayurvedic and modern lifestyle principles for expectant mothers to support maternal vitality and healthy fetal development.",
        "overview_hi": "गर्भवती महिला और गर्भस्थ शिशु के उत्तम स्वास्थ्य के लिए सुरक्षित पोषण, दिनचर्या और सावधानियां।",
        "causes_en": ["Physiological hormonal shifts, increased blood volume demand, growing fetal nutritional requirements."],
        "causes_hi": ["गर्भावस्था में शरीर के हार्मोन्स में बदलाव और शिशु के विकास के लिए अतिरिक्त पोषण की जरूरत।"],
        "ayurvedic_remedies_en": [
            "Garbhini Paricharya (AYUSH Classical Protocol): Month-by-month dietary regimen emphasizing medicated milk, ghee, and sweet (Madhura) herbs.",
            "Pure Cow Ghee: 1-2 tsp in warm milk in 2nd and 3rd trimesters nourishes fetal brain and eases pelvic ligaments.",
            "Gentle Abhyanga: Daily massage with warm Dhanwantharam Taila to lower back and legs reduces swelling and fatigue."
        ],
        "ayurvedic_remedies_hi": [
            "गर्भिणी परिचर्या (AYUSH विधि): महीने-दर-महीने आहार नियम, जिसमें शुद्ध दूध, देसी घी और सुपाच्य सात्विक भोजन मुख्य है।",
            "गाय का शुद्ध घी: दूसरी और तीसरी तिमाही में गुनगुने दूध में 1 चम्मच घी लेने से शिशु का पोषण होता है और प्रसव आसान होता है।",
            "धनवंतरी तेल की हल्की मालिश: पैरों और कमर पर हल्के हाथों से मालिश करने से सूजन और दर्द में आराम मिलता है।"
        ],
        "home_remedies_en": [
            "Morning Sickness: Nibble on dry crackers or sip fresh ginger-lemon water before stepping out of bed.",
            "Soaked dry fruits: 5 soaked almonds, 1 walnut, and 2 soaked figs every morning.",
            "Prenatal walking: 30 minutes of gentle level walking daily in fresh air."
        ],
        "home_remedies_hi": [
            "सुबह जी मिचलाने पर बिस्तर से उठने से पहले सूखा टोस्ट या अदरक का हल्का पानी लें।",
            "भीगे मेवे: 5 भीगे बादाम, 1 अखरोट और 2 भीगे अंजीर रोज सुबह खाएं।",
            "रोजाना 30 मिनट समतल जगह पर ताजी हवा में टहलें।"
        ],
        "diet_nutrition_en": ["Iron & Folic Acid: Spinach, beetroot, lentils, pomegranate, citrus fruits. Calcium from ragi, curd, and milk. Hydrate with 3 liters water."],
        "diet_nutrition_hi": ["फोलिक एसिड व आयरन: पालक, चुकंदर, दालें, अनार और संतरा। कैल्शियम के लिए रागी और दूध। 3 लीटर पानी पिएं।"],
        "dos_and_donts_en": {"dos": ["Take doctor-prescribed Iron, Folic Acid, and Calcium regularly", "Sleep on your left side with a pillow between knees"], "donts": ["DO NOT consume unpasteurized raw milk, raw papaya, or pineapple", "Avoid heavy lifting, sudden jerks, and unguided self-medication"]},
        "dos_and_donts_hi": {"dos": ["डॉक्टर द्वारा दी गई आयरन, फोलिक एसिड और कैल्शियम की गोलियां समय पर लें", "बाईं करवट लेकर सोएं"], "donts": ["कच्चा पपीता, अनानास या बिना उबला कच्चा दूध बिल्कुल न लें", "भारी वजन न उठाएं और बिना डॉक्टर पूछे कोई दवा न खाएं"]},
        "when_to_see_doctor_en": "CRITICAL EMERGENCY: Immediately rush to hospital if you experience vaginal bleeding, fluid leakage, severe headache with blurred vision, sudden facial swelling, or reduced fetal kicks.",
        "when_to_see_doctor_hi": "आपातकालीन चेतावनी: यदि ब्लीडिंग हो, पानी की थैली फटे, आंखों के आगे अंधेरा छाए, अचानक चेहरे पर सूजन आए या बच्चे की हलचल कम लगे तो बिना 1 मिनट गंवाए अस्पताल जाएं।",
        "allergy_keywords": ["milk", "dairy", "ghee", "almond", "walnut", "fig", "ginger"],
        "sources": "Ministry of AYUSH Garbhini Paricharya Guidelines & WHO Antenatal Care Norms"
    },
    "post_pregnancy_recovery": {
        "id": "post_pregnancy_recovery",
        "category_id": "women",
        "category_name": "👶 Women-Specific",
        "title_en": "Post-Pregnancy Recovery (Sutika Paricharya)",
        "title_hi": "प्रसवोपरांत स्वास्थ्य सुधार (Post-Pregnancy Recovery)",
        "overview_en": "Traditional maternal care during the 6-week postnatal period (Sutika Kala) to restore pelvic floor strength, uterine involution, and optimal lactation.",
        "overview_hi": "डिलीवरी के बाद मां के शरीर की रिकवरी, गर्भाशय को अपनी सामान्य स्थिति में लाना, कमर की मजबूती और भरपूर स्तनपान के उपाय।",
        "causes_en": ["Severe physical exhaustion, blood loss, hormonal drop post-placenta delivery, and intense round-the-clock lactation demands."],
        "causes_hi": ["प्रसव के बाद शरीर की कमजोरी, खून की कमी और दिन-रात स्तनपान कराने से आई थकान।"],
        "ayurvedic_remedies_en": [
            "Dashamoolarishta & Jeerakarishta: 15 ml each after meals promotes uterine cleansing (involution) and digestion.",
            "Shatavari Kalpa or Churna with milk: Premier galactagogue that enhances quality and volume of breast milk.",
            "Daily Postnatal Abhyanga: Full-body warm oil massage followed by gentle abdominal binding (Udara Veshtana).",
            "Saubhagya Sunthi Paka for deep pelvic strengthening."
        ],
        "ayurvedic_remedies_hi": [
            "दशमूलारिष्ट और जीरकारिष्ट: भोजन के बाद 15-15 मिली पानी मिलाकर लें (गर्भाशय की सफाई और पाचन के लिए सर्वोत्तम)।",
            "शतावरी कल्प: दूध के साथ लेने से स्तनपान के लिए भरपूर और पौष्टिक दूध बनता है।",
            "सूतिका मालिश और पेट बांधना: गुनगुने तेल से मालिश के बाद सूती कपड़े से पेट को हल्के से बांधें ताकि गर्भाशय अपनी जगह आए।",
            "सौभाग्य सोंठ पाक का सेवन कमर मजबूत करता है।"
        ],
        "home_remedies_en": [
            "Gond ke Laddu (Edible gum, dry fruits, methi, pure cow ghee) provides sustained postpartum caloric and bone recovery.",
            "Jeera-Ajwain warm water: Boil 1 tsp cumin and 1 tsp ajwain in water; drink warm throughout the day to boost breast milk and prevent infant colic.",
            "Rest whenever the baby sleeps (Sleep synchronization)."
        ],
        "home_remedies_hi": [
            "गोंद और मेथी के लड्डू: शुद्ध देसी घी, मेवे और गोंद के लड्डू हड्डियों को मजबूती देते हैं और कमजोरी दूर करते हैं।",
            "जीरा और अजवाइन का पानी: दिनभर गुनगुना पिएं, इससे मां का दूध बढ़ता है और शिशु को गैस नहीं होती।",
            "जब बच्चा सोए, मां भी तुरंत सोए (नींद पूरी करना बहुत जरूरी है)।"
        ],
        "diet_nutrition_en": ["Warm, easily digestible meals: Moong dal khichdi with ghee, dalia, garlic-seasoned soups, almonds, milk, and dates."],
        "diet_nutrition_hi": ["घी वाली मूंग दाल खिचड़ी, दलिया, लहसुन का सूप, बादाम, खजूर और दूध। ठंडा या बासी खाना न खाएं।"],
        "dos_and_donts_en": {"dos": ["Keep body and ears covered warmly", "Practice Kegel exercises after 2 weeks for pelvic floor repair"], "donts": ["Do not lift heavy weights or do strenuous gym exercises for 6-8 weeks", "Avoid cold water and icy foods"]},
        "dos_and_donts_hi": {"dos": ["सिर और कानों को कपड़े से ढककर रखें", "पेल्विक फ्लोर मजबूत करने के लिए कीगल एक्सरसाइज करें"], "donts": ["6-8 हफ्ते तक भारी वजन न उठाएं और भारी कसरत न करें", "ठंडा पानी न पिएं"]},
        "when_to_see_doctor_en": "See a doctor immediately for high fever with chills, foul-smelling lochia discharge, severe calf pain/swelling (DVT risk), or feelings of hopelessness/crying spells (Postpartum Depression).",
        "when_to_see_doctor_hi": "यदि तेज बुखार आए, डिस्चार्ज से दुर्गंध आए, पिंडली में तेज सूजन/दर्द हो या लगातार रोने का मन करे व बच्चे से लगाव न लगे (पोस्टपार्टम डिप्रेशन) तो तुरंत डॉक्टर से मिलें।",
        "allergy_keywords": ["milk", "dairy", "ghee", "methi", "ajwain", "cumin", "almond"],
        "sources": "Ministry of AYUSH Sutika Paricharya & WHO Postnatal Care Guidelines"
    },
    "menopausal_symptoms": {
        "id": "menopausal_symptoms",
        "category_id": "women",
        "category_name": "👶 Women-Specific",
        "title_en": "Menopausal Symptoms (Rajonivritti / Perimenopause)",
        "title_hi": "रजोनिवृत्ति (मेनोपॉज) के लक्षण (Menopause Symptoms)",
        "overview_en": "Vasomotor and psychological transition symptoms (hot flashes, night sweats, vaginal dryness, mood swings, sleep disruption) as ovarian estrogen production ceases.",
        "overview_hi": "माहवारी बंद होने की उम्र (45-55 वर्ष) में अचानक तेज गर्मी लगना (हॉट फ्लैशेस), पसीना आना, चिड़चिड़ापन और हड्डियों में दर्द होना।",
        "causes_en": ["Depletion of ovarian follicular reserve and sharp drop in circulating estradiol", "Hypothalamic temperature regulation dysregulation", "Accelerated bone mineral density loss"],
        "causes_hi": ["उम्र के साथ अंडाशय से एस्ट्रोजन हार्मोन का बनना बंद होना", "दिमाग द्वारा शरीर का तापमान नियंत्रित न रख पाना", "हड्डियों से कैल्शियम का तेजी से घटना"],
        "ayurvedic_remedies_en": [
            "Shatavari Churna or Gulam: Premier plant-derived phytoestrogen that cools hot flashes and nourishes mucosal tissues.",
            "Ashoka & Lodhra Kashayam to balance systemic Vata-Pitta transition.",
            "Brahmi Ghrita to calm cognitive brain fog and night sweats.",
            "Mukta Pishti or Praval Pishti: Natural coral/pearl calcium for bone density."
        ],
        "ayurvedic_remedies_hi": [
            "शतावरी चूर्ण: 1 चम्मच दूध के साथ सुबह-शाम (हॉट फ्लैशेस और गर्मी को शांत करने वाली प्राकृतिक औषधि)।",
            "अशोकादि काढ़ा हार्मोनल बदलाव को संतुलित करता है।",
            "ब्राह्मी घृत रात के पसीने और अनिद्रा को दूर करता है।",
            "प्रवाल पिष्टी या मुक्ता पिष्टी: हड्डियों को कमजोर होने (ऑस्टियोपोरोसिस) से बचाने वाला प्राकृतिक कैल्शियम।"
        ],
        "home_remedies_en": [
            "Flaxseed (Alsi) Powder: 1-2 tbsp daily in warm water or curd; rich in lignans (natural dietary phytoestrogens).",
            "Soybean / Edamame or Tofu: Natural isoflavones bind estrogen beta-receptors.",
            "Dress in layers of breathable cotton; keep an ice-water flask nearby during hot flashes."
        ],
        "home_remedies_hi": [
            "पिसी हुई अलसी (Flaxseed): 1 चम्मच रोज पानी या दही में मिलाकर लें (इसमें प्राकृतिक फाइटोएस्ट्रोजन होते हैं)।",
            "सोयाबीन, टोफू या सोया दूध का सेवन करें।",
            "सूती और ढीले कपड़े पहनें; हॉट फ्लैश आने पर ठंडा पानी पिएं।"
        ],
        "diet_nutrition_en": ["High-calcium & Vitamin D foods: Ragi, sesame seeds, paneer, fortified curd, almonds, and leafy greens. Cut alcohol, spicy foods, and excess caffeine."],
        "diet_nutrition_hi": ["रागी, सफेद तिल, पनीर, दही, बादाम और पालक खाएं। तीखे मसाले, शराब और चाय कम करें (ये गर्मी भड़काते हैं)।"],
        "dos_and_donts_en": {"dos": ["Perform weight-bearing exercises (walking, strength training) to preserve bones", "Practice deep abdominal breathing during hot flashes"], "donts": ["Do not smoke (hastens menopause and bone loss)", "Avoid sleeping in warm, stuffy rooms"]},
        "dos_and_donts_hi": {"dos": ["रोजाना 30 मिनट तेज चलें या हल्का वजन उठाएं ताकि हड्डियां मजबूत रहें", "हॉट फ्लैश आने पर गहरी सांस लें"], "donts": ["धूम्रपान से बचें (यह हड्डियों को खोखला करता है)", "गर्म कमरे में न सोएं"]},
        "when_to_see_doctor_en": "CRITICAL: Any vaginal bleeding occurring 12 months after your last period is 'Postmenopausal Bleeding' and requires urgent gynecological review to rule out endometrial pathology.",
        "when_to_see_doctor_hi": "अति महत्वपूर्ण चेतावनी: माहवारी पूरी तरह बंद होने के 1 साल बाद यदि कभी भी दोबारा ब्लीडिंग हो, तो इसे हल्के में न लें और तुरंत गायनेकोलॉजिस्ट को दिखाएं (गर्भाशय कैंसर की जांच जरूरी)।",
        "allergy_keywords": ["milk", "dairy", "flaxseed", "soya", "sesame", "almond"],
        "sources": "ICMR Guidelines on Menopause & Ministry of AYUSH Rajonivritti Protocols"
    },

    # ==========================================
    # CATEGORY 9: 👨 Men-Specific (5 issues)
    # ==========================================
    "male_pattern_baldness": {
        "id": "male_pattern_baldness",
        "category_id": "men",
        "category_name": "👨 Men-Specific",
        "title_en": "Male Pattern Baldness (Androgenetic Alopecia / Indralupta)",
        "title_hi": "पुरुषों में गंजापन (Male Pattern Baldness)",
        "overview_en": "Progressive miniaturization of hair follicles along the receding temples and crown vertex driven by genetic sensitivity to Dihydrotestosterone (DHT).",
        "overview_hi": "पुरुषों में माथे के दोनों कोनों से बालों का पीछे जाना और सिर के बीच (तालू) से बाल पतले होकर गंजापन आना (DHT हार्मोन का प्रभाव)।",
        "causes_en": ["Genetic sensitivity of hair follicles to 5-alpha reductase enzyme and DHT", "Chronic scalp tension and reduced microvascular perfusion", "High stress elevating cortisol and shedding phases", "Nutritional deficiencies in Zinc, Biotin, and Iron"],
        "causes_hi": ["आनुवंशिक कारण और डीएचटी (DHT) हार्मोन का प्रभाव", "स्कैल्प में रक्त संचार की कमी", "अत्यधिक तनाव", "जिंक, बायोटिन और प्रोटीन की कमी"],
        "ayurvedic_remedies_en": [
            "Bhringraj Taila + Neelibhringadi Taila: Regular circular scalp massage 3 times weekly.",
            "Nasyam with Anu Taila (2 drops in nostrils daily pacifies Pitta in the head).",
            "Amla & Shikakai scalp packs.",
            "Brahmi and Ashwagandha to lower DHT-elevating stress."
        ],
        "ayurvedic_remedies_hi": [
            "भृंगराज व नीलीभृंगादि तेल: हफ्ते में 3 बार रात को हल्के हाथों से स्कैल्प की मालिश करें।",
            "अणु तैल नस्य: रोज सुबह नाक में 2 बूंद अणु तेल डालें (सिर के पित्त को शांत करता है)।",
            "आंवला और भृंगराज का लेप बालों की जड़ों में लगाएं।",
            "अश्वगंधा का सेवन तनाव कम करता है जिससे बाल गिरना धीमा होता है।"
        ],
        "home_remedies_en": [
            "Pumpkin Seed Oil / Saw Palmetto Extract: Natural natural 5-alpha reductase inhibitors that help block DHT.",
            "Onion juice applied to thinning crown for 20 minutes before shampooing (sulfur boosts blood supply).",
            "Daily scalp massage (Derma-rolling / gentle finger kneading for 5 mins daily)."
        ],
        "home_remedies_hi": [
            "कद्दू के बीज (Pumpkin seeds) रोज 1 चम्मच खाएं; इनमें प्राकृतिक DHT ब्लॉकर गुण होते हैं।",
            "प्याज का रस हफ्ते में दो बार बालों की जड़ों में 20 मिनट लगाएं।",
            "रोजाना 5 मिनट उंगलियों के पोरों से सिर की मालिश करें ताकि खून का दौरा बढ़े।"
        ],
        "diet_nutrition_en": ["DHT-fighting foods: Pumpkin seeds, green tea (EGCG), tomatoes (lycopene), carrots, eggs, and walnuts. Protein intake 1g/kg body weight."],
        "diet_nutrition_hi": ["कद्दू के बीज, ग्रीन टी, टमाटर, गाजर, अंडे और अखरोट। पर्याप्त प्रोटीन लें।"],
        "dos_and_donts_en": {"dos": ["Wash scalp with gentle sulfate-free shampoo 3 times a week", "Practice Sarvangasana or Sirsasana for scalp blood flow"], "donts": ["Avoid tight helmets/caps that trap sweat and cause traction", "Do not smoke (nicotine damages hair papillae)"]},
        "dos_and_donts_hi": {"dos": ["सप्ताह में 3 बार माइल्ड शैम्पू से बाल धोएं", "सर्वांगासन या अनुलोम-विलोम करें"], "donts": ["बहुत टाइट हेलमेट या टोपी लगातार न पहने रहें", "धूम्रपान से बचें (यह बालों की जड़ों को सुखाता है)"]},
        "when_to_see_doctor_en": "Consult a dermatologist early for clinical options like topical Minoxidil or Finasteride before follicles undergo complete fibrotic scarring.",
        "when_to_see_doctor_hi": "यदि बाल बहुत तेजी से गिर रहे हों तो चर्म रोग विशेषज्ञ (Dermatologist) से मिलकर मिनोक्सिडिल या पीआरपी (PRP) थेरेपी पर सलाह लें।",
        "allergy_keywords": ["onion", "pumpkin", "green_tea", "walnut"],
        "sources": "Ministry of AYUSH Indralupta Protocols & ICMR Dermatology Advisory"
    },
    "body_hair_issues": {
        "id": "body_hair_issues",
        "category_id": "men",
        "category_name": "👨 Men-Specific",
        "title_en": "Body Hair Issues & Folliculitis (Romakupa Shotha)",
        "title_hi": "इनग्रोन बाल और फॉलिकुलाइटिस (Ingrown Hair & Folliculitis)",
        "overview_en": "Inflamed, itchy, or infected red bumps around hair follicles (beard area, chest, back, groin) caused by razor shaving friction or bacterial trapping.",
        "overview_hi": "दाढ़ी बनाने या पसीने के बाद बालों की जड़ों में लाल दाने, मवाद, खुजली और इनग्रोन बाल (बालों का अंदर मुड़ जाना)।",
        "causes_en": ["Shaving against the grain with dull, multi-blade razors", "Bacterial overgrowth (Staphylococcus aureus) trapped in sweaty gym clothes", "Tight synthetic compression clothing", "Excess sebum and dead skin cells blocking follicular pore"],
        "causes_hi": ["पुराने या कुंद रेजर से उलटी दिशा में दाढ़ी बनाना", "पसीने वाले जिम के कपड़ों में बैक्टीरिया पनपना", "बहुत तंग सिंथेटिक कपड़े पहनना", "मृत त्वचा से रोमछिद्रों का बंद होना"],
        "ayurvedic_remedies_en": [
            "Neem & Turmeric wash: Boil fresh neem leaves and turmeric in water; use as antiseptic rinse.",
            "Khadirarishta or Manjishtadi Kwath for systemic blood purification.",
            "Triphala Guggulu: 2 tablets twice daily clears follicular pustules."
        ],
        "ayurvedic_remedies_hi": [
            "नीम और हल्दी का पानी: नीम की पत्तियां और हल्दी पानी में उबालकर दाने वाली जगह धोएं।",
            "मंजिष्ठादि काढ़ा खून को साफ करके दानों को सुखाता है।",
            "त्रिफला गुग्गुलु: 2-2 गोली लेने से मवाद वाले दाने ठीक होते हैं।"
        ],
        "home_remedies_en": [
            "Warm Saline Compress: Apply a warm cloth soaked in salt water for 10 minutes to draw out trapped ingrown hair.",
            "Tea Tree Oil: Dilute 2 drops in coconut oil and apply as natural antibacterial spot treatment.",
            "Always shave in the direction of hair growth (with the grain), never against it."
        ],
        "home_remedies_hi": [
            "गर्म नमक वाले पानी के कपड़े से 10 मिनट सिकाई करें, दबा हुआ बाल बाहर निकल आता है।",
            "नारियल तेल में 2 बूंद टी-ट्री ऑयल मिलाकर दानों पर लगाएं।",
            "दाढ़ी हमेशा बालों के उगने की दिशा में ही बनाएं, कभी उलटी दिशा में रेजर न चलाएं।"
        ],
        "diet_nutrition_en": ["Anti-inflammatory diet: Turmeric, garlic, citrus fruits, green tea. Cut excess greasy fried snacks."],
        "diet_nutrition_hi": ["हल्दी, लहसुन, आंवला और ग्रीन टी लें। ज्यादा तला-भुना खाना बंद करें।"],
        "dos_and_donts_en": {"dos": ["Exfoliate skin gently 24 hours before shaving", "Change sweaty gym clothes immediately after workout"], "donts": ["Never pick or squeeze pus-filled follicular bumps with dirty fingernails", "Do not dry shave without shaving foam/gel"]},
        "dos_and_donts_hi": {"dos": ["शेविंग से पहले चेहरे को गुनगुने पानी से धोएं", "जिम के तुरंत बाद पसीने वाले कपड़े बदलकर नहाएं"], "donts": ["नाखूनों से दानों को न फोड़ें (इन्फेक्शन फैल सकता है)", "बिना शेविंग क्रीम के सूखी शेव न बनाएं"]},
        "when_to_see_doctor_en": "See a dermatologist if bumps turn into large, throbbing, painful carbuncles, or if folliculitis spreads extensively across chest and back.",
        "when_to_see_doctor_hi": "यदि दानों में तेज दर्द हो, वे बड़े फोड़े का रूप ले लें या बुखार आ जाए तो डॉक्टर से एंटीबायोटिक का परामर्श लें।",
        "allergy_keywords": ["neem", "turmeric", "tea_tree", "coconut"],
        "sources": "National Health Portal (NHP India) & ICMR Dermatology Guidelines"
    },
    "men_muscle_gain": {
        "id": "men_muscle_gain",
        "category_id": "men",
        "category_name": "👨 Men-Specific",
        "title_en": "Muscle Gain (Mamsa Dhatu Vardhana)",
        "title_hi": "मांसपेशियों का विकास और बल (Men Muscle Gain)",
        "overview_en": "Building lean muscular hypertrophy, skeletal strength, and metabolic power through progressive resistance training and optimal nutrient timing.",
        "overview_hi": "कमजोरी दूर करके प्राकृतिक रूप से सुडौल मांसपेशियां और शारीरिक ताकत बढ़ाना।",
        "causes_en": ["Inadequate dietary protein and caloric surplus", "Lack of progressive mechanical tension on muscles", "Low natural testosterone from poor sleep and chronic stress", "Excessive cardio without resistance training"],
        "causes_hi": ["भोजन में प्रोटीन और कैलोरी की भारी कमी", "वजन वाली कसरत न करना", "नींद की कमी से टेस्टोस्टेरोन का गिरना", "अत्यधिक तनाव"],
        "ayurvedic_remedies_en": [
            "Ashwagandha Avaleha or Churna: 1 tsp with warm full-cream milk twice daily (clinically proven to enhance muscle size and testosterone).",
            "Shatavari & Safed Musli: 1/2 tsp each with milk for cellular mass building.",
            "Bala Ashwagandha Taila Abhyanga: Pre-bath full body massage strengthens muscle fibers (Mamsa dhatu)."
        ],
        "ayurvedic_remedies_hi": [
            "अश्वगंधा अवलेह या चूर्ण: 1 चम्मच सुबह-शाम मलाई वाले गुनगुने दूध के साथ (मांसपेशियों और ताकत को बढ़ाने में वैज्ञानिक रूप से प्रमाणित)।",
            "सफेद मूसली और शतावरी: दूध के साथ लेने से शरीर का वजन और बल बढ़ता है।",
            "बला-अश्वगंधा तेल से मालिश: कसरत से पहले मालिश करने से मांसपेशियों में खिंचाव और ताकत आती है।"
        ],
        "home_remedies_en": [
            "Natural High-Protein Smoothie: Blend 1 glass milk + 2 bananas + 2 tbsp peanut butter + 1 tbsp roasted oats + 1 tbsp sattu.",
            "Progressive Overload Training: Lift challenging weights 4-5 days weekly focusing on compound movements (Squats, Deadlifts, Pull-ups, Bench Press).",
            "Post-workout 30-minute anabolic window snack."
        ],
        "home_remedies_hi": [
            "देसी प्रोटीन शेक: 1 गिलास दूध + 2 केले + 2 चम्मच पीनट बटर + 2 चम्मच सत्तू + भीगे बादाम पीसकर शेक बनाएं।",
            "हफ्ते में 4-5 दिन जिम में स्क्वैट्स, पुल-अप्स, पुश-अप्स जैसी भारी कसरतें करें।",
            "कसरत के 30 मिनट के भीतर प्रोटीन और कार्बोहाइड्रेट जरूर लें।"
        ],
        "diet_nutrition_en": ["1.6 - 2.0g protein per kg bodyweight: Paneer, soya chunks, eggs, chicken, lentils, roasted chana, sattu, and milk. Eat in a 300-500 calorie surplus."],
        "diet_nutrition_hi": ["प्रतिदिन वजन के हिसाब से पर्याप्त प्रोटीन लें: पनीर, सोया चंक्स, अंडे, दालें, भुना चना, सत्तू और दूध। पेट भरकर पौष्टिक खाना खाएं।"],
        "dos_and_donts_en": {"dos": ["Sleep 8 hours nightly (growth hormone peaks during deep stage 3 sleep)", "Stay hydrated with 3.5L water"], "donts": ["DO NOT use illegal anabolic steroids (they destroy liver, heart, and natural endocrine axis)", "Do not train same muscle group on consecutive days"]},
        "dos_and_donts_hi": {"dos": ["रात को 8 घंटे की गहरी नींद लें (नींद में ही मांसपेशियां बनती हैं)", "खूब पानी पिएं"], "donts": ["स्टेरॉयड या खतरनाक केमिकल इंजेक्शन का इस्तेमाल कभी न करें (यह दिल और किडनी बर्बाद करते हैं)", "एक ही मांसपेशी को रोज-रोज न थकाएं"]},
        "when_to_see_doctor_en": "Consult a sports physician if you experience severe muscle tears, dark tea-colored urine after extreme workouts (Rhabdomyolysis), or chronic joint instability.",
        "when_to_see_doctor_hi": "यदि भारी कसरत के बाद पेशाब का रंग चाय जैसा गहरा भूरा हो जाए (रैबडोमायोलिसिस) तो तुरंत इमरजेंसी में जाएं।",
        "allergy_keywords": ["milk", "dairy", "peanut", "soya", "egg", "oats"],
        "sources": "ICMR Dietary Guidelines on Athletes & AYUSH Rasayana Protocols"
    },
    "gym_tips_recovery": {
        "id": "gym_tips_recovery",
        "category_id": "men",
        "category_name": "👨 Men-Specific",
        "title_en": "Gym Tips & Injury Prevention",
        "title_hi": "जिम कसरत और चोट से बचाव (Gym Tips & Form)",
        "overview_en": "Essential biomechanical safety principles, warm-up protocols, and lifting technique guidelines to maximize muscular gains without spinal or joint injuries.",
        "overview_hi": "जिम में कसरत करते समय सही तकनीक (फॉर्म), वार्म-अप और कमर/घुटनों को चोट से बचाने के महत्वपूर्ण नियम।",
        "causes_en": ["Ego lifting (lifting weights beyond capacity with bad form)", "Skipping dynamic warm-up and jumping straight into heavy sets", "Poor core bracing mechanics during deadlifts and squats", "Overtraining without adequate deload weeks"],
        "causes_hi": ["औकात से ज्यादा भारी वजन उठाना (ईगो लिफ्टिंग)", "बिना वार्म-अप किए सीधे भारी वजन पर चले जाना", "कमर को सीधा रखे बिना वजन उठाना", "बिना आराम किए लगातार भारी कसरत करना"],
        "ayurvedic_remedies_en": [
            "Mahanarayan Taila joint massage before bath keeps synovial fluid fluid and lubricated.",
            "Shallaki (Boswellia serrata) & Hadjod (Cissus quadrangularis): Natural protectors of cartilage, ligaments, and tendons.",
            "Ashwagandha to protect against exercise-induced cortisol spikes."
        ],
        "ayurvedic_remedies_hi": [
            "महानारायण तेल से कसरत के बाद जोड़ों की मालिश करने से लिगामेंट्स सुरक्षित रहते हैं।",
            "हड़जोड़ और शल्लाकी: हड्डियों और जोड़ों के कार्टिलेज को मजबूत रखने वाली प्राचीन जड़ी-बूटियां।",
            "अश्वगंधा कसरत की थकान को रोकता है।"
        ],
        "home_remedies_en": [
            "10-Minute Dynamic Warm-Up: Arm circles, leg swings, bodyweight squats, and cat-cow before lifting weights.",
            "RICE Protocol for acute sprains: Rest, Ice (for 48 hrs), Compression, Elevation.",
            "Use a weightlifting belt and wrist wraps during maximal load compound lifts."
        ],
        "home_remedies_hi": [
            "कसरत से पहले 10 मिनट वार्म-अप: हाथ-पैर घुमाना, बिना वजन के उठक-बैठक और स्ट्रेचिंग।",
            "चोट लगने पर बर्फ की सिकाई (पहले 48 घंटे) करें और आराम दें।",
            "भारी वजन उठाते समय वेटलिफ्टिंग बेल्ट का प्रयोग करें।"
        ],
        "diet_nutrition_en": ["Hydrate with electrolyte water during workout. Consume whey protein or dal-paneer meal within 45 mins post-workout."],
        "diet_nutrition_hi": ["कसरत के दौरान थोड़ा-थोड़ा पानी पीते रहें। कसरत के 45 मिनट के भीतर प्रोटीन युक्त भोजन लें।"],
        "dos_and_donts_en": {"dos": ["Leave your ego at the gym door: Prioritize strict form over heavy weight", "Always use safety bar pins in the squat rack"], "donts": ["Never round your lower back during deadlifts or bent-over rows", "Do not bounce heavy barbells off your chest during bench press"]},
        "dos_and_donts_hi": {"dos": ["वजन से ज्यादा सही तरीके (फॉर्म) पर ध्यान दें", "स्क्वैट रैक में हमेशा सेफ्टी बार लगाकर रखें"], "donts": ["डेडलिफ्ट में कमर को कभी भी गोल या झुका हुआ न रखें (स्लिप डिस्क का खतरा)", "छाती पर वजन को झटके से न पटकें"]},
        "when_to_see_doctor_en": "See an orthopedic surgeon immediately if you hear or feel a loud 'pop' in a muscle or joint accompanied by sudden sharp pain, joint deformity, or inability to bear weight.",
        "when_to_see_doctor_hi": "यदि कसरत के दौरान जोड़ में 'पॉप' की आवाज आए, तेज दर्द हो या अंग पर वजन रखना नामुमकिन हो (लिगामेंट फटना) तो तुरंत अस्पताल जाएं।",
        "allergy_keywords": ["dairy"],
        "sources": "WHO Physical Activity Guidelines & Sports Authority of India Guidelines"
    },
    "workout_recovery_men": {
        "id": "workout_recovery_men",
        "category_id": "men",
        "category_name": "👨 Men-Specific",
        "title_en": "Workout Recovery & Soreness (DOMS)",
        "title_hi": "कसरत के बाद रिकवरी और सोरनेस (Workout Recovery)",
        "overview_en": "Managing Delayed Onset Muscle Soreness (DOMS), repairing microscopic myofibrillar tears, and replenishing glycogen stores after strenuous exercise.",
        "overview_hi": "जिम या भारी कसरत के अगले दिन मांसपेशियों में होने वाला दर्द, जकड़न और अकड़न (DOMS) को जल्दी ठीक करने के उपाय।",
        "causes_en": ["Microscopic eccentric muscle fiber tears triggering inflammatory repair", "Lactic acid clearance followed by cellular remodeling", "Dehydration and electrolyte depletion", "Inadequate sleep preventing growth hormone release"],
        "causes_hi": ["कसरत से मांसपेशियों के रेशों में सूक्ष्म खिंचाव व सूजन", "शरीर में पानी और नमक की कमी", "कम सोना जिससे मांसपेशियां रिपेयर नहीं हो पातीं"],
        "ayurvedic_remedies_en": [
            "Haldi Doodh (Golden Milk with black pepper): Powerful natural curcumin reduces exercise-induced muscle inflammation and soreness.",
            "Ashwagandha Churna with warm milk before bed facilitates cellular repair.",
            "Ksheerabala 101 Taila massage relieves muscular micro-trauma."
        ],
        "ayurvedic_remedies_hi": [
            "हल्दी वाला दूध (काली मिर्च के साथ): करक्यूमिन मांसपेशियों की सूजन और दर्द को प्राकृतिक रूप से तेजी से मिटाता है।",
            "अश्वगंधा चूर्ण रात को गुनगुने दूध के साथ लें।",
            "क्षीरबला तेल से सोरनेस वाली मांसपेशियों की मालिश करें।"
        ],
        "home_remedies_en": [
            "Foam Rolling: Roll major sore muscle groups (quads, hamstrings, back) for 10 minutes post-workout.",
            "Epsom Salt Bath: Soak in warm water with 2 cups of magnesium sulfate (Epsom salt) for 20 minutes to relax muscle fibers.",
            "Active Recovery Walk: Light 20-minute walk flushes out metabolic waste without adding fatigue."
        ],
        "home_remedies_hi": [
            "फोम रोलर का इस्तेमाल: दर्द वाली मांसपेशियों पर 10 मिनट फोम रोलर चलाएं।",
            "एप्सम सॉल्ट (सेंधा नमक) वाले गुनगुने पानी से नहाएं (मांसपेशियों को रिलैक्स करता है)।",
            "सोरनेस के दिन बिल्कुल लेटे रहने की जगह 20 मिनट हल्की वॉक करें।"
        ],
        "diet_nutrition_en": ["Tart cherry juice or watermelon juice (citrulline reduces DOMS). 30g protein + 50g complex carbs post-workout. Hydrate with 3L water."],
        "diet_nutrition_hi": ["तरबूज का रस (सिट्रूलिन मांसपेशियों का दर्द घटाता है), पनीर, अंडे और दलिया। 3 लीटर पानी जरूर पिएं।"],
        "dos_and_donts_en": {"dos": ["Get 8 hours of uninterrupted nocturnal sleep", "Eat anti-inflammatory whole foods"], "donts": ["Do not take NSAID pain pills (ibuprofen) after workouts (they blunt muscle protein synthesis)", "Avoid alcohol post-workout"]},
        "dos_and_donts_hi": {"dos": ["8 घंटे की पूरी नींद लें", "पौष्टिक खाना खाएं"], "donts": ["कसरत के दर्द के लिए पेनकिलर (जैसे ब्रूफेन) न खाएं (यह मांसपेशियों के विकास को रोक देती है)", "कसरत के बाद शराब न पिएं"]},
        "when_to_see_doctor_en": "See a doctor if muscle pain is excruciating and accompanied by dark brown urine (Rhabdomyolysis) or localized swelling that feels burning hot.",
        "when_to_see_doctor_hi": "यदि दर्द बहुत भयानक हो, मांसपेशी में तेज सूजन और लाली हो या पेशाब का रंग कोला/चाय जैसा काला हो तो तुरंत अस्पताल जाएं।",
        "allergy_keywords": ["milk", "dairy", "turmeric"],
        "sources": "ICMR Guidelines on Sports Medicine & Ministry of AYUSH"
    },

    # ==========================================
    # CATEGORY 10: 🌡️ Seasonal Issues (6 issues)
    # ==========================================
    "heat_rash": {
        "id": "heat_rash",
        "category_id": "seasonal",
        "category_name": "🌡️ Seasonal Issues",
        "title_en": "Heat Rash (Prickly Heat / Ghamoriya / Miliaria)",
        "title_hi": "घमौरियां और लाल दाने (Heat Rash / Ghamoriya)",
        "overview_en": "Tiny, intensely itchy red bumps and stinging prickles on the skin (neck, chest, back, skin folds) caused by blocked sweat ducts during hot, humid weather.",
        "overview_hi": "गर्मियों में पसीने की ग्रंथियां बंद होने से गर्दन, पीठ और छाती पर बारीक लाल दाने, तेज खुजली और कांटे जैसी चुभन होना।",
        "causes_en": ["Sweat ducts (eccrine glands) becoming blocked by dead skin cells and bacteria", "Wearing tight synthetic non-breathable clothing in intense heat", "Heavy physical exertion causing copious sweating in humid conditions", "Overheating during sleep"],
        "causes_hi": ["पसीने की नलियों का गंदगी और मृत त्वचा से बंद होना", "गर्मियों में तंग और सिंथेटिक (पॉलिएस्टर) कपड़े पहनना", "उमस भरे मौसम में ज्यादा पसीना आना", "रात को गर्म कमरे में सोना"],
        "ayurvedic_remedies_en": [
            "Sandalwood (Chandan) & Rose Water Paste: Apply pure sandalwood paste to prickly heat rash for immediate cooling and anti-inflammatory relief.",
            "Multani Mitti (Fuller's Earth) with cooling mint water pack.",
            "Ushira (Vetiver / Khas) infused water for bathing.",
            "Sarivadya Asava to cool systemic blood heat (Rakta-Pitta)."
        ],
        "ayurvedic_remedies_hi": [
            "चंदन और गुलाब जल का लेप: घमौरियों पर असली सफेद चंदन का लेप लगाएं (तुरंत ठंडक देता है और चुभन मिटाता है)।",
            "मुल्तानी मिट्टी में पुदीने का पानी मिलाकर लेप करें।",
            "खस के अर्क वाले पानी से स्नान करें।",
            "सारिवाद्यासव का सेवन शरीर की अंदरूनी गर्मी शांत करता है।"
        ],
        "home_remedies_en": [
            "Cold Water Compress: Apply a clean cloth soaked in cool water to affected areas for 10 minutes.",
            "Fresh Aloe Vera Gel: Apply pure cold aloe vera pulp straight from the leaf.",
            "Bathe twice daily in lukewarm or cool water; avoid harsh antibacterial soaps that dry skin."
        ],
        "home_remedies_hi": [
            "ठंडे पानी में भीगा साफ कपड़ा 10 मिनट घमौरियों पर रखें।",
            "ताजा एलोवेरा जेल: पौधे से ताजा एलोवेरा निकालकर घमौरियों पर लगाएं।",
            "दिन में दो बार ताजे ठंडे पानी से नहाएं; तेज केमिकल वाले साबुन से बचें।"
        ],
        "diet_nutrition_en": ["Cooling foods: Tender coconut water, watermelon, cucumber, mint lassi, fennel water, and sattu drink. Avoid hot chilies, deep-fried foods, and hot tea in summer."],
        "diet_nutrition_hi": ["नारियल पानी, तरबूज, खीरा, पुदीने की छाछ, सौंफ का पानी और जौ का सत्तू। तीखे मसाले, चाय और समोसे-पकौड़े से बचें।"],
        "dos_and_donts_en": {"dos": ["Wear loose, lightweight 100% cotton clothing", "Stay in air-conditioned or well-ventilated fan rooms"], "donts": ["Do not scratch or rub the rash with dirty hands", "Avoid applying thick oil-based creams or petroleum jelly (they clog sweat ducts further)"]},
        "dos_and_donts_hi": {"dos": ["ढीले और हल्के सूती (कॉटन) के कपड़े पहनें", "हवादार और ठंडे कमरे में रहें"], "donts": ["नाखूनों से घमौरियों को न खुजलाएं", "घमौरियों पर कोई भी गाढ़ा तेल या वैसलीन न लगाएं (इससे रोमछिद्र और बंद हो जाएंगे)"]},
        "when_to_see_doctor_en": "See a doctor if the bumps fill with yellow pus, skin feels intensely hot and swollen, or if heat rash is accompanied by high fever and chills (secondary bacterial infection).",
        "when_to_see_doctor_hi": "यदि घमौरियों में पीली मवाद भर जाए, त्वचा बहुत लाल और गर्म हो जाए या साथ में तेज बुखार आ जाए तो डॉक्टर को दिखाएं।",
        "allergy_keywords": ["sandalwood", "aloe_vera", "mint", "coconut"],
        "sources": "National Health Portal (NHP India) & Ministry of AYUSH Seasonal Advisory"
    },
    "sun_damage": {
        "id": "sun_damage",
        "category_id": "seasonal",
        "category_name": "🌡️ Seasonal Issues",
        "title_en": "Sun Damage & Tan (Surya Dagdha / Sunburn)",
        "title_hi": "धूप से झुलसी त्वचा और टैनिंग (Sun Damage & Tan)",
        "overview_en": "Erythema, burning, hyperpigmentation, and premature photoaging caused by unprotected exposure to ultraviolet (UVA & UVB) solar radiation.",
        "overview_hi": "तेज धूप से त्वचा का काला पड़ जाना (टैनिंग), चेहरे पर जलन, लालिमा और समय से पहले झुर्रियां पड़ना।",
        "causes_en": ["Direct sun exposure between 10 AM and 4 PM without sunscreen", "UV radiation triggering excess melanin synthesis and DNA cellular stress", "Depletion of skin antioxidants (glutathione and vitamin E)"],
        "causes_hi": ["दोपहर 10 से 4 बजे के बीच बिना सनस्क्रीन के धूप में रहना", "अल्ट्रावायलेट किरणों से त्वचा में अतिरिक्त मेलेनिन बनना", "त्वचा की नमी और एंटीऑक्सीडेंट्स का खत्म होना"],
        "ayurvedic_remedies_en": [
            "Kumkumadi Taila: 3-4 drops applied at bedtime restores photodamaged complexion.",
            "Raw Milk & Turmeric wash: Cold raw milk with a pinch of pure turmeric soothes sun-inflamed skin.",
            "Raktachandan (Red Sandalwood) paste with rose water clears stubborn sun tan."
        ],
        "ayurvedic_remedies_hi": [
            "कुंकुमादि तेल: रात को सोने से पहले 3-4 बूंद लगाने से धूप से झुलसी त्वचा में चमक लौटती है।",
            "कच्चा दूध और हल्दी: ठंडे कच्चे दूध में चुटकी भर हल्दी मिलाकर चेहरे पर लगाएं, टैनिंग और जलन शांत होती है।",
            "रक्तचंदन (लाल चंदन) का लेप गुलाब जल के साथ लगाने से टैनिंग तेजी से हटती है।"
        ],
        "home_remedies_en": [
            "Tomato & Curd Pack: Mix fresh tomato pulp with unflavored curd; apply for 15 mins (natural lycopene and lactic acid brighten tan).",
            "Chilled Cucumber Slices placed over face and eyes for 20 minutes.",
            "Cold Green Tea mist sprayed over sun-exposed skin neutralizes free radicals."
        ],
        "home_remedies_hi": [
            "टमाटर और दही का पैक: ताजे टमाटर के रस में थोड़ा दही मिलाकर 15 मिनट लगाएं (टैनिंग हटाने का प्राकृतिक उपाय)।",
            "खीरे के ठंडे टुकड़े चेहरे पर रखें।",
            "ठंडी ग्रीन टी का स्प्रे चेहरे पर करें।"
        ],
        "diet_nutrition_en": ["Lycopene & Beta-carotene: Tomatoes, carrots, watermelons, papayas, and citrus fruits boost systemic photo-protection."],
        "diet_nutrition_hi": ["टमाटर, गाजर, तरबूज, पपीता और संतरा खाएं जो धूप से त्वचा की रक्षा करते हैं।"],
        "dos_and_donts_en": {"dos": ["Apply broad-spectrum SPF 30+ or SPF 50 sunscreen 20 minutes before going out", "Wear a wide-brimmed hat and UV sunglasses"], "donts": ["Do not peel peeling skin from a sunburn", "Do not apply butter or vaseline to fresh sunburns"]},
        "dos_and_donts_hi": {"dos": ["धूप में निकलने से 20 मिनट पहले SPF 30+ या SPF 50 सनस्क्रीन लगाएं", "धूप का चश्मा और टोपी पहनें"], "donts": ["धूप से उतरी चमड़ी को नाखूनों से न खींचे", "ताजा जली त्वचा पर मक्खन या गाढ़ी क्रीम न लगाएं"]},
        "when_to_see_doctor_en": "Seek emergency medical care if sunburn covers a large area with severe blistering, high fever, severe dizziness, or confusion (Sunstroke / Heatstroke).",
        "when_to_see_doctor_hi": "यदि धूप में रहने के बाद बड़े-बड़े छाले पड़ जाएं, तेज बुखार, उल्टी या चक्कर आकर बेहोशी होने लगे (लू लगना / हीटस्ट्रोक) तो तुरंत अस्पताल जाएं।",
        "allergy_keywords": ["milk", "dairy", "turmeric", "curd", "tomato", "green_tea"],
        "sources": "ICMR Guidelines on Photodermatology & Ministry of AYUSH Tvak Care"
    },
    "winter_dryness": {
        "id": "winter_dryness",
        "category_id": "seasonal",
        "category_name": "🌡️ Seasonal Issues",
        "title_en": "Winter Dryness & Cracked Skin (Sheetata / Xerosis)",
        "title_hi": "सर्दियों में त्वचा का रूखापन व फटना (Winter Dryness)",
        "overview_en": "Flaking, cracking, tight, and itchy skin (especially on hands, lips, and heels) during cold months caused by plummeting humidity and harsh indoor heating.",
        "overview_hi": "सर्दियों में त्वचा का सफेद पड़ना, पपड़ी जमना, होठों और एड़ियों का फटना जो ठंडी सूखी हवा से वात बढ़ने का लक्षण है।",
        "causes_en": ["Low environmental humidity stripping moisture from stratum corneum", "Long, piping-hot showers washing away natural sebum oils", "Harsh sodium lauryl sulfate bathing soaps", "Drinking inadequate water during cold months"],
        "causes_hi": ["हवा में नमी की भारी कमी", "सर्दियों में बहुत तेज खौलते गर्म पानी से देर तक नहाना", "केमिकल वाले कठोर साबुन का प्रयोग", "ठंड में कम पानी पीना"],
        "ayurvedic_remedies_en": [
            "Whole-Body Abhyanga: Daily massage with warm Sesame oil, Coconut oil, or Badam Rogan 20 mins before bath.",
            "Shatadhouta Ghrita (100-times washed cow ghee): The world's finest natural emollient cream for cracked skin and lips.",
            "Manjishtadi Taila for cracked winter heels (Padadari)."
        ],
        "ayurvedic_remedies_hi": [
            "नहाने से पहले अभ्यंग: नहाने से 20 मिनट पहले गुनगुने तिल के तेल, नारियल तेल या बादाम रोगन से मालिश करें।",
            "शतधौत घृत (100 बार धोया हुआ गाय का घी): फटी त्वचा, होठों और चेहरे के लिए दुनिया का सबसे बेहतरीन प्राकृतिक मॉइस्चराइजर।",
            "फटी एड़ियों पर मंजिष्ठादि तेल या सरसों का तेल लगाएं।"
        ],
        "home_remedies_en": [
            "Raw Honey & Malai (Milk Cream) Face Pack: 1 tsp fresh milk cream + 1/2 tsp honey applied for 15 mins.",
            "Foot Care: Soak feet in warm water for 10 mins, scrub gently with pumice, apply mustard oil or ghee, and wear cotton socks overnight.",
            "Keep an indoor humidifier or bowl of water near heaters."
        ],
        "home_remedies_hi": [
            "मलाई और शहद का लेप: 1 चम्मच ताजी मलाई में आधा चम्मच शहद मिलाकर चेहरे पर लगाएं।",
            "एड़ियों की देखभाल: रात को पैरों में गुनगुना सरसों का तेल या घी लगाकर सूती मोजे पहनकर सोएं।",
            "कमरे में हीटर के पास एक बर्तन में पानी रखें ताकि हवा में नमी बनी रहे।"
        ],
        "diet_nutrition_en": ["Healthy fats: Pure cow ghee with meals, soaked almonds, walnuts, flaxseeds, sesame jaggery chikki. Drink 2.5L warm water."],
        "diet_nutrition_hi": ["देसी गाय का घी, भीगे बादाम, अखरोट, तिल और गुड़ की चिक्की खाएं। 2.5 लीटर गुनगुना पानी जरूर पिएं।"],
        "dos_and_donts_en": {"dos": ["Apply moisturizer within 3 minutes of stepping out of the shower ('soak and seal')", "Bathe in lukewarm, not scalding hot, water"], "donts": ["Do not lick dry, chapped lips (saliva enzymes worsen lip cracking)", "Avoid synthetic wool directly against sensitive bare skin"]},
        "dos_and_donts_hi": {"dos": ["नहाने के तुरंत 3 मिनट के भीतर जब त्वचा हल्की नम हो तभी तेल या क्रीम लगाएं", "बहुत खौलते पानी से न नहाएं"], "donts": ["फटे होठों पर बार-बार जीभ न लगाएं (थूक से होंठ और ज्यादा फटते हैं)", "सीधे त्वचा पर खुरदरा ऊनी कपड़ा न पहनें"]},
        "when_to_see_doctor_en": "Consult a dermatologist if dry skin cracks deeply and bleeds, weeps clear fluid, or develops painful infections.",
        "when_to_see_doctor_hi": "यदि एड़ियों या हाथों की दरारों से खून बहने लगे, तेज दर्द हो या मवाद पड़ जाए तो डॉक्टर से दवा लें।",
        "allergy_keywords": ["milk", "dairy", "ghee", "honey", "sesame", "mustard", "almond", "walnut"],
        "sources": "Ministry of AYUSH Dinacharya Guidelines & NHP India"
    },
    "seasonal_hair_fall": {
        "id": "seasonal_hair_fall",
        "category_id": "seasonal",
        "category_name": "🌡️ Seasonal Issues",
        "title_en": "Seasonal Hair Fall (Rutucharya Hair Shedding)",
        "title_hi": "मौसम बदलने पर बाल गिरना (Seasonal Hair Fall)",
        "overview_en": "A transient spike in daily hair shedding occurring during seasonal transitions (especially monsoon humidity and early winter dryness).",
        "overview_hi": "बारिश के मौसम में उमस से या सर्दियों की शुरुआत में अचानक रोजाना 100 से ज्यादा बाल टूटने लगना।",
        "causes_en": ["Monsoon scalp humidity fostering fungal yeast build-up and weak follicle roots", "Winter dry air causing brittle, static-prone hair shafts", "Biological evolutionary synchronized telogen shedding in autumn"],
        "causes_hi": ["बारिश में पसीने और नमी से स्कैल्प में फंगस और रूसी होना", "सर्दियों में बालों का रूखा और बेजान होकर टूटना", "मौसम बदलने पर बालों का प्राकृतिक शेडिंग चक्र"],
        "ayurvedic_remedies_en": [
            "Neem-Tulsi Scalp Rinse: Boil neem and tulsi leaves in water; use as final rinse after shampooing in monsoon.",
            "Bhringraj Taila gentle warm oil massage twice weekly in winter.",
            "Amla Churna: 1 tsp daily with warm water in morning provides internal vitamin C and keratin nourishment."
        ],
        "ayurvedic_remedies_hi": [
            "नीम और तुलसी का पानी: बारिश में बाल धोने के बाद नीम-तुलसी के उबले पानी से स्कैल्प धोएं (फंगस खत्म करता है)।",
            "सर्दियों में हफ्ते में दो बार गुनगुने भृंगराज तेल से मालिश करें।",
            "रोज सुबह 1 चम्मच आंवला चूर्ण गुनगुने पानी से लें।"
        ],
        "home_remedies_en": [
            "Never tie up damp, sweaty hair during monsoon; dry hair thoroughly under a gentle fan.",
            "Methi (Fenugreek) and Curd hair mask once a week to strengthen seasonal roots.",
            "Use a wide-toothed wooden comb."
        ],
        "home_remedies_hi": [
            "बारिश में भीगे या पसीने वाले बालों को कभी कसकर न बांधें; पंखे की हवा में अच्छी तरह सुखाएं।",
            "मेथी दाना और दही का हेयर मास्क हफ्ते में एक बार लगाएं।",
            "लकड़ी की चौड़े दांतों वाली कंघी का प्रयोग करें।"
        ],
        "diet_nutrition_en": ["Iron and protein: Sprouted moong, sesame seeds, spinach, jaggery, eggs, and amla murabba."],
        "diet_nutrition_hi": ["अंकुरित मूंग, तिल, पालक, गुड़ और आंवले का मुरब्बा खाएं।"],
        "dos_and_donts_en": {"dos": ["Wash rain-soaked hair immediately with clean tap water", "Keep comb sanitized"], "donts": ["Do not use hot blow dryers aggressively in dry winter", "Avoid chemical smoothing treatments during shedding season"]},
        "dos_and_donts_hi": {"dos": ["बारिश के पानी में भीगने पर तुरंत साफ ताजे पानी से बाल धोएं", "कंघी को हमेशा साफ रखें"], "donts": ["सर्दियों में तेज गर्म हेयर ड्रायर न चलाएं", "इस मौसम में बालों पर केमिकल या स्ट्रेटनिंग न करवाएं"]},
        "when_to_see_doctor_en": "See a dermatologist if shedding continues heavily for >8 weeks or produces localized bald patches.",
        "when_to_see_doctor_hi": "यदि बाल गिरना 2 महीने से ज्यादा समय तक लगातार जारी रहे या सिर में गोल चकत्ते दिखने लगें तो तुरंत डॉक्टर को दिखाएं।",
        "allergy_keywords": ["neem", "tulsi", "curd", "dairy", "fenugreek", "amla", "sesame"],
        "sources": "Ministry of AYUSH Rutucharya Hair Protocol & NHP India"
    },
    "monsoon_fungal_prevention": {
        "id": "monsoon_fungal_prevention",
        "category_id": "seasonal",
        "category_name": "🌡️ Seasonal Issues",
        "title_en": "Monsoon Issues (Fungal & Ringworm Prevention / Dadru)",
        "title_hi": "बारिश में दाद, खाज और फंगल संक्रमण (Monsoon Fungal Prevention)",
        "overview_en": "Superficial fungal infections (Ringworm/Dadru, Athlete's Foot, Jock Itch) flaring up in body folds due to high monsoon heat and humidity.",
        "overview_hi": "बारिश के मौसम में नमी और पसीने से जांघों, पैरों की उंगलियों और बगलों में दाद, खाज, खुजली और गोल लाल चकत्ते होना।",
        "causes_en": ["Dermatophyte fungi proliferating rapidly in damp, warm skin folds", "Wearing wet, rain-soaked socks and shoes for hours", "Sharing damp towels, undergarments, or bedsheets with infected persons", "High humidity preventing sweat evaporation"],
        "causes_hi": ["पसीने और नमी वाली जगहों पर फंगस (दाद) का तेजी से बढ़ना", "बारिश में भीगे मोजे और जूते दिनभर पहने रहना", "गीले तौलिए या कपड़े किसी दूसरे के इस्तेमाल करना"],
        "ayurvedic_remedies_en": [
            "Gandhak Rasayan & Kaishore Guggulu: Classical internal Ayurvedic medications to eradicate fungal blood toxins (Krimi/Dadru).",
            "Marichyadi Taila or Neem Taila applied externally to clean dry skin.",
            "Khadiradi Kwath wash."
        ],
        "ayurvedic_remedies_hi": [
            "गंधक रसायन और कैशोर गुग्गुलु: खून से फंगल इन्फेक्शन को जड़ से खत्म करने वाली प्रसिद्ध आयुर्वेदिक दवाएं।",
            "मरिच्यादि तेल या नीम का तेल साफ और सूखे दाद पर लगाएं।",
            "खदिरारिष्ट का सेवन करें।"
        ],
        "home_remedies_en": [
            "Keep Skin 100% Dry: After bathing, dry groin and underarms completely and dust with antifungal or dusting powder.",
            "Raw Turmeric & Neem paste applied to the ringworm patch for 20 mins, then rinsed and dried thoroughly.",
            "Iron all underwear and socks with a hot iron before wearing (kills microscopic fungal spores)."
        ],
        "home_remedies_hi": [
            "त्वचा को पूरी तरह सूखा रखें: नहाने के बाद जांघों और पैरों को पोंछकर एंटीफंगल पाउडर लगाएं।",
            "कच्ची हल्दी और नीम की पत्तियों का लेप दाद पर लगाएं और 20 मिनट बाद धोकर सुखा लें।",
            "अंडरगारमेंट्स और मोजों को पहनने से पहले गर्म प्रेस (इस्त्री) जरूर करें (फंगस के अंडे मर जाते हैं)।"
        ],
        "diet_nutrition_en": ["Bitter greens (bitter gourd/karela, neem flower, methi). Strictly eliminate white sugar, stale sweets, and fermented foods which feed fungal overgrowth."],
        "diet_nutrition_hi": ["करेला, मेथी और हरी सब्जियां खाएं। मीठा, मिठाई और बासी खाना बंद करें क्योंकि चीनी से फंगस तेजी से बढ़ती है।"],
        "dos_and_donts_en": {"dos": ["Change socks and underwear twice daily if sweating", "Wear open ventilated sandals in the rain"], "donts": ["NEVER apply steroid creams (like Betnovate, Quadriderm) without prescription (they cause fungal flare-ups and skin thinning)", "Never share towels"]},
        "dos_and_donts_hi": {"dos": ["दिन में दो बार साफ और सूखे कपड़े बदलें", "बारिश में बंद जूतों की जगह खुली चप्पल पहनें"], "donts": ["दाद पर बिना डॉक्टर पूछे स्टेरॉयड वाली क्रीम (जैसे बेटनोवेट) कभी न लगाएं (यह फंगस को बेकाबू कर देती है)", "किसी का तौलिया इस्तेमाल न करें"]},
        "when_to_see_doctor_en": "Consult a dermatologist if ringworm rash spreads rapidly across groin or body, oozes yellow pus, or does not improve in 10 days.",
        "when_to_see_doctor_hi": "यदि दाद तेजी से पूरे शरीर में फैलने लगे, मवाद आए या 10 दिन में आराम न मिले तो तुरंत चर्म रोग विशेषज्ञ को दिखाएं।",
        "allergy_keywords": ["neem", "turmeric"],
        "sources": "National Health Portal (NHP India) & Ministry of AYUSH Dadru Protocols"
    },
    "summer_dehydration": {
        "id": "summer_dehydration",
        "category_id": "seasonal",
        "category_name": "🌡️ Seasonal Issues",
        "title_en": "Dehydration & Heat Exhaustion (Summer / Grishma Ritu)",
        "title_hi": "गर्मियों में लू और निर्जलीकरण (Summer Heat & Dehydration)",
        "overview_en": "Severe water and salt depletion during peak summer heat waves, leading to intense fatigue, dizziness, muscle cramps, and heat exhaustion (Loo).",
        "overview_hi": "गर्मियों में तेज धूप और लू (Loo) लगने से शरीर में पानी-नमक की कमी, चक्कर आना, तेज सिरदर्द और उल्टी-दस्त होना।",
        "causes_en": ["Exposure to hot dry winds ('Loo') between 12 PM and 4 PM", "Excessive sweating without electrolyte replenishment", "Working outdoors in high heat without drinking enough water", "Consuming dehydrating iced colas or alcohol"],
        "causes_hi": ["दोपहर में 12 से 4 बजे के बीच गर्म हवाओं (लू) में घूमना", "पसीना निकलने पर केवल सादा पानी पीना और नमक की कमी होना", "धूप में बिना सिर ढके काम करना", "गर्मियों में शराब या कोल्ड ड्रिंक पीना"],
        "ayurvedic_remedies_en": [
            "Aam Panna (Raw Mango Cooler): Boiled green mango pulp blended with roasted cumin, mint, and black salt; the ultimate ancient antidote to heat stroke.",
            "Bel Sharbat (Wood Apple drink): Pacifies intense Pitta and protects intestinal lining from heat.",
            "Gulab Sharbat (Rose syrup) or Chandana drink."
        ],
        "ayurvedic_remedies_hi": [
            "आम पन्ना: उबले कच्चे आम का पल्प, भुना जीरा, पुदीना और काला नमक मिलाकर पिएं (लू से बचने और इलाज का सबसे बड़ा अमृत)।",
            "बेल का शरबत: पेट की आंतों को ठंडक देता है और गर्मियों के दस्त-उल्टी से बचाता है।",
            "गुलाब या खस का शरबत पिएं।"
        ],
        "home_remedies_en": [
            "Keep an onion in your pocket or rub raw onion juice on temples and soles of feet (traditional rural safeguard against heat waves).",
            "Sip WHO ORS or fresh lemon-salt-sugar water continuously when working outdoors.",
            "Place a cool wet towel over the forehead and neck if feeling overheated."
        ],
        "home_remedies_hi": [
            "गांव का पारंपरिक नुस्खा: धूप में निकलते समय जेब में छोटा प्याज रखें या लू लगने पर तलवों में प्याज का रस मलें।",
            "ओआरएस (ORS) या नींबू-नमक-चीनी का पानी दिनभर घूंट-घूंट पीते रहें।",
            "गर्मी चढ़ने पर माथे और गर्दन पर ठंडे पानी की गीली पट्टी रखें।"
        ],
        "diet_nutrition_en": ["Watermelon, tender coconut water, sweet muskmelon, cucumber, barley sattu drink, buttermilk with roasted jeera. Avoid hot spicy curries."],
        "diet_nutrition_hi": ["तरबूज, खरबूजा, नारियल पानी, खीरा, जौ का सत्तू और भुने जीरे वाली छाछ। तीखे और गर्म मसालों से बचें।"],
        "dos_and_donts_en": {"dos": ["Always cover head and face with a wet cotton scarf when stepping outdoors in summer", "Drink at least 3.5 to 4 liters of fluids daily"], "donts": ["Do not venture out during peak heat (12 PM - 3:30 PM) unless emergency", "Never leave children or pets inside parked cars in summer"]},
        "dos_and_donts_hi": {"dos": ["धूप में निकलते समय सिर और चेहरे को सूती गमछे/दुपट्टे से ढकें", "दिनभर में 3.5 से 4 लीटर तरल पदार्थ पिएं"], "donts": ["दोपहर 12 से 3:30 बजे के बीच बिना जरूरी काम के बाहर न निकलें", "धूप में खड़ी बंद कार में किसी को न छोड़ें"]},
        "when_to_see_doctor_en": "CRITICAL EMERGENCY: If a person stops sweating, has hot dry red skin, body temperature >104°F, confusion, or loses consciousness, this is Heat Stroke (Sunstroke) — call an ambulance and apply ice packs immediately.",
        "when_to_see_doctor_hi": "आपातकालीन चेतावनी: यदि व्यक्ति को पसीना आना बंद हो जाए, शरीर का तापमान 104 डिग्री से ऊपर हो, चमड़ी तपने लगे या वह बेहोश हो जाए तो यह हीटस्ट्रोक (सनस्ट्रोक) है — तुरंत एम्बुलेंस बुलाएं और बर्फ से शरीर ठंडा करें।",
        "allergy_keywords": ["mango", "mint", "cumin", "onion", "coconut", "barley"],
        "sources": "National Health Portal (NHP India) Heat Wave Advisory & Ministry of AYUSH Grishma Protocols"
    }
}


# ==============================================================================
# HELPER QUERY & SEARCH FUNCTIONS
# ==============================================================================

def get_all_categories():
    """Return list of all categories."""
    return CATEGORIES


def get_topics_by_category(category_id: str):
    """Return all topic dicts belonging to a category."""
    return [t for t in WELLNESS_DATA.values() if t.get("category_id") == category_id]


def get_topic_by_id(topic_id: str):
    """Return topic dict by topic ID."""
    return WELLNESS_DATA.get(topic_id)


def search_wellness_topics(query: str, language: str = "en"):
    """Search topics by keyword across titles, causes, and remedies."""
    if not query or not query.strip():
        return list(WELLNESS_DATA.values())
    q = query.strip().lower()
    results = []
    for topic in WELLNESS_DATA.values():
        score = 0
        title_en = topic.get("title_en", "").lower()
        title_hi = topic.get("title_hi", "").lower()
        if q in title_en or q in title_hi:
            score += 15
        if q in topic.get("overview_en", "").lower() or q in topic.get("overview_hi", "").lower():
            score += 8
        for c in topic.get("causes_en", []) + topic.get("causes_hi", []):
            if q in c.lower():
                score += 4
        for r in (
            topic.get("ayurvedic_remedies_en", [])
            + topic.get("ayurvedic_remedies_hi", [])
            + topic.get("home_remedies_en", [])
            + topic.get("home_remedies_hi", [])
        ):
            if q in r.lower():
                score += 3
        if score > 0:
            results.append((score, topic))
    results.sort(key=lambda x: x[0], reverse=True)
    return [item[1] for item in results]


def check_allergy_warnings(topic: dict, patient_allergies: list):
    """Check if any remedy allergen keyword matches the patient's known allergies."""
    if not patient_allergies or not topic:
        return []
    keywords = topic.get("allergy_keywords", [])
    matched = []
    patient_allergies_lower = [str(a).lower().strip() for a in patient_allergies]
    for kw in keywords:
        kw_l = kw.lower().strip()
        for pa in patient_allergies_lower:
            if kw_l in pa or pa in kw_l:
                matched.append(kw)
    return list(set(matched))
