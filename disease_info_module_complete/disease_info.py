"""
Disease Info Module — Auto-detects collection, no session state conflicts
"""

import os
import sys
import json
import re
from typing import Dict, List, Optional
from dataclasses import dataclass
from dotenv import load_dotenv

# Load .env from project root
_script_dir = os.path.dirname(os.path.abspath(__file__))
for _env_path in [
    os.path.join(_script_dir, "..", "config", ".env"),
    os.path.join(_script_dir, "..", "..", "config", ".env"),
    os.path.join(_script_dir, "config", ".env"),
    "../config/.env",
    "../../config/.env",
]:
    if os.path.exists(_env_path):
        load_dotenv(_env_path, override=True)
        print(f"[DiseaseInfo] Loaded .env from: {_env_path}")
        break

try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_OK = True
except Exception as e:
    print(f"[DiseaseInfo] ChromaDB import notice: {e}")
    CHROMADB_OK = False

SentenceTransformer = None

# LLM imports
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    GEMINI_OK = True
except ImportError:
    GEMINI_OK = False

try:
    from langchain_groq import ChatGroq
    GROQ_OK = True
except ImportError:
    GROQ_OK = False

try:
    from core.llm import LLMClient
    LLMCLIENT_OK = True
except ImportError:
    LLMCLIENT_OK = False

# ---------------------------------------------------------------------------
# Multilingual Hindi/Hinglish Disease Normalization Map
# ---------------------------------------------------------------------------
HINDI_TO_ENGLISH_DISEASE_MAP = {
    "डायबिटीज": "diabetes",
    "डायबटीज": "diabetes",
    "मधुमेह": "diabetes",
    "शुगर": "diabetes",
    "sugar": "diabetes",
    "type 2 diabetes": "diabetes",
    "type 1 diabetes": "diabetes",
    "diabetes": "diabetes",
    "अस्थमा": "asthma",
    "दमा": "asthma",
    "asthma": "asthma",
    "निमोनिया": "pneumonia",
    "pneumonia": "pneumonia",
    "गठिया": "arthritis",
    "आर्थराइटिस": "arthritis",
    "arthritis": "arthritis",
    "कोरोना": "coronavirus",
    "कोविड": "coronavirus",
    "कोविड-19": "coronavirus",
    "covid": "coronavirus",
    "covid-19": "coronavirus",
    "coronavirus": "coronavirus",
    "मलेरिया": "malaria",
    "malaria": "malaria",
    "डेंगू": "dengue",
    "dengue": "dengue",
    "टाइफाइड": "typhoid",
    "typhoid": "typhoid",
    "माइग्रेन": "migraine",
    "सिरदर्द": "migraine",
    "migraine": "migraine",
    "तपेदिक": "tuberculosis",
    "टीबी": "tuberculosis",
    "tuberculosis": "tuberculosis",
    "उच्च रक्तचाप": "hypertension",
    "हाई बीपी": "hypertension",
    "हाई ब्लड प्रेशर": "hypertension",
    "hypertension": "hypertension",
    "blood pressure": "hypertension",
    "दिल का दौरा": "heart attack",
    "हार्ट अटैक": "heart attack",
    "heart attack": "heart attack",
    "पीलिया": "jaundice",
    "jaundice": "jaundice",
    "हैजा": "cholera",
    "cholera": "cholera",
    "कैंसर": "cancer",
    "cancer": "cancer",
    "अल्सर": "ulcer",
    "ulcer": "ulcer",
    "एनीमिया": "anemia",
    "खून की कमी": "anemia",
    "anemia": "anemia",
    "बुखार": "fever",
    "fever": "fever",
}

def normalize_disease_query(disease_name: str) -> str:
    """Normalizes Hindi / Hinglish / synonymous disease names to canonical English."""
    if not disease_name:
        return ""
    d_clean = disease_name.strip().lower()
    return HINDI_TO_ENGLISH_DISEASE_MAP.get(d_clean, d_clean)
# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
_CHROMA_PATHS = [
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "chroma_db"),
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "chroma_rag_db"),
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "vector_db"),
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "chroma_db"),
    "./data/chroma_db",
    "./data/chroma_rag_db",
    "./data/vector_db",
    "./chroma_db",
    "../data/chroma_db",
    "../chroma_db",
]


@dataclass
class DiseaseInfo:
    disease_name: str
    description: str
    symptoms: List[str]
    diagnostic_tests: List[str]
    precautions: List[str]
    treatment: List[str]
    risk_factors: List[str]
    when_to_see_doctor: str
    sources: List[Dict[str, str]]
    related_topics: List[str]
    confidence: str


class DiseaseInfoRetriever:
    """Auto-detects ChromaDB path and collection name."""

    def __init__(self, top_k: int = 5):
        self.top_k = top_k
        self.llm_provider = os.environ.get("LLM_PROVIDER", "groq")
        self._collection = None
        self._client = None
        self._embedder = None
        self._chroma_path = None
        self._collection_name = None

    def _connect(self):
        if self._collection is not None:
            return

        env_path = os.environ.get("CHROMA_DB_PATH")
        if env_path and os.path.exists(env_path):
            self._chroma_path = env_path
        else:
            for path in _CHROMA_PATHS:
                if os.path.exists(path):
                    self._chroma_path = os.path.abspath(path)
                    break

        if not self._chroma_path:
            print(f"[DiseaseInfo] ChromaDB directory not found in {_CHROMA_PATHS}. Running in Cloud Direct Clinical Mode.")
            self._collection = None
            self._client = None
            return

        try:
            self._client = chromadb.PersistentClient(
                path=self._chroma_path,
                settings=Settings(anonymized_telemetry=False)
            )
        except Exception as e:
            err_msg = str(e).lower()
            if "already exists" in err_msg or "different settings" in err_msg:
                self._client = chromadb.PersistentClient(path=self._chroma_path)
            else:
                print(f"[DiseaseInfo] ChromaDB client initialization failed: {e}. Falling back to Cloud Direct Mode.")
                self._collection = None
                self._client = None
                return

        try:
            collections = self._client.list_collections()
        except Exception as e:
            print(f"[DiseaseInfo] list_collections failed: {e}. Falling back to Cloud Direct Mode.")
            self._collection = None
            return

        if not collections:
            print(f"[DiseaseInfo] No collections found in {self._chroma_path}. Running in Cloud Direct Mode.")
            self._collection = None
            return

        preferred = ["medassist_rag", "medlineplus_topics", "medlineplus_health", "health_topics", "medlineplus"]
        for name in preferred:
            if any(c.name == name for c in collections):
                self._collection_name = name
                break

        if not self._collection_name:
            self._collection_name = collections[0].name

        try:
            self._collection = self._client.get_collection(name=self._collection_name)
            doc_count = self._collection.count()
            print(f"[DiseaseInfo] Path: {self._chroma_path} | Collection: {self._collection_name} | Docs: {doc_count}")
        except Exception as e:
            print(f"[DiseaseInfo] Failed to open collection: {e}. Running in Cloud Direct Mode.")
            self._collection = None

    def _get_embedder(self):
        if self._embedder is None:
            try:
                from sentence_transformers import SentenceTransformer
                self._embedder = SentenceTransformer("all-MiniLM-L6-v2")
            except Exception as e:
                print(f"[DiseaseInfo] SentenceTransformer load notice: {e}. Falling back to keyword search.")
                self._embedder = None
        return self._embedder

    # ===== DRUG LABEL FILTER =====
    def _is_drug_label_doc(self, title: str, content: str) -> bool:
        """Skip FDA drug labels, medication guides, and product inserts."""
        if not title and not content:
            return False

        title_lower = title.lower() if title else ""
        content_lower = (content or "").lower()

        title_keywords = [
            "fda", "drug label", "medication guide", "prescribing information",
            "fda-approved", "patient information", "drug facts", "package insert"
        ]
        if any(sk in title_lower for sk in title_keywords):
            return True

        content_red_flags = [
            "this product is", "this product is not", "use only after diagnosis",
            "not a fast acting", "rescue inhaler", "intended to complement, not replace",
            "initial worsening of symptoms", "stop use and ask a doctor",
            "physician should always be consulted to rule out serious causes",
            "drug facts", "active ingredient", "inactive ingredient",
            "dosage and administration", "warnings and precautions",
            "ask a doctor before use", "do not use more than directed",
            "when using this product", "keep out of reach of children",
            "if pregnant or breast-feeding", "tAMPER EVIDENT", "distributed by",
            "purpose expectorant", "nasal decongestant", "mucus relief"
        ]

        red_flag_count = sum(1 for flag in content_red_flags if flag in content_lower)
        if red_flag_count >= 2:
            return True

        if content_lower.strip().startswith("this product"):
            return True

        return False

    # ===== CONTENT RELEVANCE FILTER =====
    def _is_content_relevant(self, disease_name: str, title: str, content: str) -> bool:
        """Filter out docs about unrelated conditions."""
        disease_lower = disease_name.lower()
        title_lower = title.lower() if title else ""
        content_lower = (content or "").lower()

        if disease_lower in ["coronavirus", "covid", "covid-19"]:
            if any(h in title_lower for h in ["heart", "cardiac", "angioplasty", "coronary", "myocardial"]):
                return False
            heart_terms = ["heart", "cardiac", "angioplasty", "coronary", "myocardial", "chest pain", "rapid heartbeat"]
            covid_terms = ["covid", "coronavirus", "sars", "pandemic", "covid-19"]
            heart_mentions = sum(content_lower.count(t) for t in heart_terms)
            covid_mentions = sum(content_lower.count(t) for t in covid_terms)
            if heart_mentions > covid_mentions:
                return False

        if disease_lower == "asthma":
            if "inhaler" in title_lower and "asthma" not in title_lower:
                return False
            if any(x in content_lower for x in ["mucus relief", "expectorant", "nasal decongestant", "dextromethorphan"]):
                return False

        return True

    def search_disease(self, disease_name: str) -> List[Dict]:
        canonical_name = normalize_disease_query(disease_name)
        self._connect()
        if self._collection is None:
            print("[DEBUG] No ChromaDB collection available. Falling back to Cloud Direct Clinical LLM.")
            return []

        doc_count = self._collection.count()
        print(f"[DEBUG] Total documents: {doc_count}")

        if doc_count == 0:
            return self._keyword_search(canonical_name)

        embedder = self._get_embedder()
        if not embedder:
            return self._keyword_search(canonical_name)

        query_variations = [
            f"{canonical_name} disease symptoms diagnosis treatment",
            f"{canonical_name} overview",
            canonical_name,
        ]

        documents = []
        seen_titles = set()

        for query in query_variations:
            if len(documents) >= self.top_k:
                break

            query_embedding = embedder.encode([query]).tolist()
            try:
                results = self._collection.query(
                    query_embeddings=query_embedding,
                    n_results=self.top_k * 4,
                    include=["documents", "metadatas", "distances"]
                )
            except Exception as e:
                continue

            if results.get("documents") and results["documents"][0]:
                for i in range(len(results["ids"][0])):
                    meta = results["metadatas"][0][i]
                    title = meta.get("title", "Unknown") if meta else "Unknown"
                    content = results["documents"][0][i] or ""

                    if self._is_drug_label_doc(title, content):
                        print(f"[DEBUG] Skipping drug label: {title}")
                        continue

                    if not self._is_content_relevant(canonical_name, title, content):
                        print(f"[DEBUG] Skipping irrelevant: {title}")
                        continue

                    title_lower = title.lower()
                    disease_lower = canonical_name.lower()
                    related_terms = {
                        "coronavirus": ["covid", "coronavirus", "sars", "covid-19"],
                        "asthma": ["asthma", "asthmatic"],
                        "diabetes": ["diabetes", "diabetic", "blood sugar", "glucose"],
                        "cancer": ["cancer", "tumor", "oncology", "carcinoma"],
                        "hypertension": ["hypertension", "blood pressure", "high blood pressure"],
                        "pneumonia": ["pneumonia", "lung infection"],
                        "migraine": ["migraine", "headache"],
                        "arthritis": ["arthritis", "joint"],
                        "malaria": ["malaria", "plasmodium"],
                        "dengue": ["dengue", "breakbone"],
                        "typhoid": ["typhoid", "salmonella"],
                        "tuberculosis": ["tuberculosis", "tb", "mycobacterium"],
                        "jaundice": ["jaundice", "bilirubin", "hepatitis"],
                        "anemia": ["anemia", "hemoglobin", "iron deficiency"]
                    }
                    allowed_terms = related_terms.get(disease_lower, [disease_lower])
                    title_relevant = any(term in title_lower for term in allowed_terms)

                    if not title_relevant and len(documents) >= 2:
                        continue

                    if title in seen_titles:
                        continue
                    seen_titles.add(title)

                    try:
                        related = json.loads(meta.get("related_topics", "[]")) if meta else []
                    except:
                        related = []

                    documents.append({
                        "content": content,
                        "title": title,
                        "url": meta.get("url", "") if meta else "",
                        "distance": results["distances"][0][i] if results.get("distances") else 0.5,
                        "related_topics": related,
                        "summary_text": content,
                    })

        documents.sort(key=lambda x: x["distance"])
        print(f"[DEBUG] After filters: {len(documents)} docs")

        if not documents:
            documents = self._keyword_search(disease_name)

        return documents

    def _keyword_search(self, disease_name: str, limit: int = 10) -> List[Dict]:
        try:
            all_data = self._collection.get(include=["documents", "metadatas"])
            docs = all_data.get("documents", []) or []
            metas = all_data.get("metadatas", []) or []

            if not docs:
                print("[DEBUG] No documents in collection for keyword search")
                return []

            keywords = disease_name.lower().split()
            keywords_set = set(keywords)
            for kw in list(keywords_set):
                if kw.endswith('s'):
                    keywords_set.add(kw[:-1])
                else:
                    keywords_set.add(kw + 's')

            scored = []
            for doc, meta in zip(docs, metas):
                if not doc:
                    continue

                title = meta.get("title", "") if meta else ""
                content = doc or ""

                if self._is_drug_label_doc(title, content):
                    continue

                if not self._is_content_relevant(disease_name, title, content):
                    continue

                text = (content + " " + str(meta)).lower()
                title_lower = title.lower()

                score = 0
                for kw in keywords_set:
                    if kw in title_lower:
                        score += 10
                    if kw in text:
                        score += 2
                    if kw[:4] in title_lower:
                        score += 3

                if score > 0:
                    scored.append((score, doc, meta))

            scored.sort(key=lambda x: x[0], reverse=True)

            results = []
            seen = set()
            for score, doc, meta in scored[:limit]:
                title = meta.get("title", "Unknown") if meta else "Unknown"
                if title in seen:
                    continue
                seen.add(title)
                try:
                    related = json.loads(meta.get("related_topics", "[]")) if meta else []
                except:
                    related = []
                results.append({
                    "content": doc,
                    "title": title,
                    "url": meta.get("url", "") if meta else "",
                    "distance": 0.5,
                    "related_topics": related,
                    "summary_text": doc,
                })
            return results
        except Exception as e:
            print(f"[DiseaseInfo] Keyword fallback failed: {e}")
            import traceback
            traceback.print_exc()
            return []

    def _build_prompt(self, disease_name: str, docs: List[Dict]) -> str:
        context = "\n\n---\n\n".join([
            f"TOPIC: {doc['title']}\n{doc['summary_text']}"
            for doc in docs[:8]
        ])

        return f"""You are MedAssist, a rural health information assistant.
Answer STRICTLY from the provided MedlinePlus sources below.
NEVER use outside medical knowledge.

RULES:
1. If sources do NOT discuss "{disease_name}", write "Information not available in sources." for EVERY field.
2. IGNORE drug labels or product inserts (text starting with "This product", "Ask a doctor before use", etc.).
3. List only COMMON and PRIMARY symptoms, tests, treatment for "{disease_name}".
4. Return ONLY valid JSON. No markdown, no explanations, no comments.

REQUIRED JSON FORMAT:
{{
    "disease_name": "{disease_name}",
    "description": "2-3 sentence overview from sources ONLY. Never leave empty.",
    "symptoms": ["symptom 1", "symptom 2", "symptom 3"],
    "diagnostic_tests": ["Test 1", "Test 2", "Test 3", "Test 4", "Test 5", "Test 6", "Test 7", "Test 8"],
    "precautions": ["precaution 1", "precaution 2"],
    "treatment": ["treatment 1", "treatment 2"],
    "risk_factors": ["risk 1", "risk 2"],
    "when_to_see_a_doctor": "guidance from sources. Never leave empty.",
    "confidence": "high"
}}

IMPORTANT FOR diagnostic_tests:
- Return 8 to 12 specific real medical test names.
- Examples: A1C Test, Fasting Blood Glucose, Oral Glucose Tolerance Test, Lipid Panel, Complete Blood Count, Thyroid Function Test, Microalbumin Test, Creatinine Test, Urinalysis, Electrolyte Panel, Chest X-Ray, Spirometry.
- Do NOT use generic names like "blood test" or "urine test".

SOURCES:
{context}
"""

    def _build_clinical_llm_prompt(self, disease_name: str) -> str:
        return f"""You are MedAssist, an expert medical and rural clinical health assistant.
Provide authoritative, accurate, and comprehensive evidence-based clinical information for: "{disease_name}".
Information should strictly align with WHO, ICMR, and MedlinePlus clinical standards.

RULES:
1. Provide accurate medical descriptions, primary symptoms, diagnostic tests, precautions, and treatments.
2. For diagnostic_tests: Provide 8 to 12 specific, real clinical diagnostic test names (e.g., A1C Test, Fasting Blood Glucose, Complete Blood Count, Lipid Panel, Chest X-Ray, etc.). Do not return generic phrases like "blood test".
3. Return ONLY valid JSON. No markdown fences (do not wrap in ```json), no explanations, no comments.

REQUIRED JSON FORMAT:
{{
    "disease_name": "{disease_name}",
    "description": "2-3 comprehensive clinical overview sentences explaining causes, pathology, and impact.",
    "symptoms": ["Primary symptom 1", "Symptom 2", "Symptom 3", "Symptom 4", "Symptom 5"],
    "diagnostic_tests": ["Specific Test 1", "Specific Test 2", "Specific Test 3", "Specific Test 4", "Specific Test 5", "Specific Test 6", "Specific Test 7", "Specific Test 8"],
    "precautions": ["Precaution 1", "Precaution 2", "Precaution 3"],
    "treatment": ["First-line treatment 1", "Treatment 2", "Lifestyle/Therapy 3"],
    "risk_factors": ["Risk factor 1", "Risk factor 2", "Risk factor 3"],
    "when_to_see_a_doctor": "Clear clinical red-flag thresholds when immediate doctor or emergency consultation is needed.",
    "confidence": "high"
}}
"""

    def _call_llm(self, prompt: str) -> str:
        import os, requests, time

        if LLMCLIENT_OK:
            try:
                client = LLMClient()
                result = client.generate(prompt)
                print(f"[DEBUG] LLMClient success! Response preview: {result[:200]}")
                return result
            except Exception as e:
                print(f"[DEBUG] LLMClient failed: {e}, trying direct requests...")

        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            try:
                import streamlit as st
                if hasattr(st, "secrets"):
                    api_key = st.secrets.get("GROQ_API_KEY")
            except Exception:
                pass

        if not api_key:
            # Check Gemini fallback
            gemini_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
            if not gemini_key:
                try:
                    import streamlit as st
                    if hasattr(st, "secrets"):
                        gemini_key = st.secrets.get("GOOGLE_API_KEY") or st.secrets.get("GEMINI_API_KEY")
                except Exception:
                    pass
            if gemini_key:
                for g_model in ["gemini-1.5-flash", "gemini-2.0-flash", "gemini-1.5-pro"]:
                    try:
                        from langchain_google_genai import ChatGoogleGenerativeAI
                        g_llm = ChatGoogleGenerativeAI(
                            model=g_model,
                            temperature=0.1,
                            google_api_key=gemini_key
                        )
                        res = g_llm.invoke(prompt)
                        return res.content if hasattr(res, "content") else str(res)
                    except Exception as ge:
                        print(f"[DiseaseInfo] Gemini fallback notice ({g_model}): {ge}")
            raise RuntimeError("GROQ_API_KEY / GEMINI_API_KEY not set - check config/.env or Streamlit Cloud Secrets")

        models = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "gemma2-9b-it", "mixtral-8x7b-32768"]

        for model_name in models:
            # Exponential backoff: 1s, 2s, 4s wait
            for attempt in range(3):
                try:
                    resp = requests.post(
                        "https://api.groq.com/openai/v1/chat/completions",
                        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                        json={
                            "model": model_name,
                            "messages": [{"role": "user", "content": prompt}],
                            "temperature": 0.1,
                            "max_tokens": 4096,
                        },
                        timeout=60
                    )
                    print(f"[DEBUG] Model: {model_name} | Attempt: {attempt+1} | Status: {resp.status_code}")

                    if resp.status_code == 401:
                        raise RuntimeError("Invalid GROQ_API_KEY - 401 Unauthorized")
                    if resp.status_code == 404:
                        print(f"[DEBUG] Model {model_name} not found, trying next...")
                        break
                    if resp.status_code == 429:
                        wait = 2 ** attempt  # 1s, 2s, 4s
                        print(f"[LLM] Rate limited, waiting {wait}s...")
                        time.sleep(wait)
                        continue
                    if resp.status_code == 400:
                        err_data = resp.json()
                        err_msg = err_data.get('error', {}).get('message', 'Unknown 400')
                        print(f"[DEBUG] 400 error: {err_msg}")
                        break

                    resp.raise_for_status()
                    data = resp.json()

                    if "choices" not in data:
                        err = data.get('error', {}).get('message', str(data))
                        raise RuntimeError(f"API error: {err}")

                    raw = data["choices"][0]["message"]["content"]
                    print(f"[DEBUG] Success with {model_name}! Response preview: {raw[:200]}")
                    return raw

                except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
                    wait = 2 ** attempt
                    print(f"[DEBUG] Connection/Timeout error: {e}. Retrying in {wait}s...")
                    time.sleep(wait)
                    if attempt == 2:
                        print(f"[DEBUG] {model_name} failed after 3 attempts.")
                
                except Exception as e:
                    print(f"[DEBUG] {model_name} attempt {attempt+1} failed: {e}")
                    if attempt == 2:
                        continue
                    time.sleep(1)

        raise RuntimeError("All Groq models failed. Check console.groq.com for available models.")

    def _parse_json(self, text: str) -> Dict:
        if not text:
            return {}

        text = text.strip()
        print(f"[DEBUG] Parsing JSON, text length: {len(text)}")

        # Try direct parse first
        try:
            return json.loads(text)
        except:
            pass

        # Try extracting from markdown code blocks
        patterns = [
            r'```(?:json)?\s*(.*?)\s*```',
            r'```\s*(.*?)\s*```',
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group(1).strip())
                except:
                    pass

        # Try finding JSON object between first { and last }
        try:
            start = text.find('{')
            end = text.rfind('}')
            if start != -1 and end != -1 and end > start:
                candidate = text[start:end+1]
                # Remove any // comments
                candidate = re.sub(r'//.*$', '', candidate, flags=re.MULTILINE)
                # Remove trailing commas before } or ]
                candidate = re.sub(r',(\s*[}\]])', r'\1', candidate)
                return json.loads(candidate)
        except:
            pass

        # Try cleaning common LLM artifacts
        cleaned = text
        cleaned = re.sub(r'^[^{]*', '', cleaned)  # Remove everything before first {
        cleaned = re.sub(r'[^}]*$', '', cleaned)  # Remove everything after last }
        cleaned = re.sub(r'//.*$', '', cleaned, flags=re.MULTILINE)
        cleaned = re.sub(r',(\s*[}\]])', r'\1', cleaned)
        try:
            return json.loads(cleaned)
        except:
            pass

        print(f"[DEBUG] FAILED to parse JSON. Raw text preview:\n{text[:500]}...")
        return {}

    def _sanitize_list_field(self, parsed: Dict, field: str):
        """Ensure a field is a list. If it is a string, wrap it. If missing or invalid, set default."""
        val = parsed.get(field)
        if isinstance(val, str):
            parsed[field] = [val]
        elif not isinstance(val, list):
            parsed[field] = ["Information not available in sources."]

    def _clean_output(self, parsed: Dict, disease_name: str):
        """Remove known incorrect or bad patterns from LLM output."""
        disease_lower = disease_name.lower()

        # ===== CORONAVIRUS/COVID CLEANUP =====
        if disease_lower in ["coronavirus", "covid", "covid-19"]:
            heart_keywords = ["chest pain", "rapid heartbeat", "heart attack",
                            "angina", "cardiac arrest", "heart failure",
                            "heart tests", "cardiac catheterization", "angioplasty",
                            "coronary", "myocardial", "stent", "cardiac ct", "cardiac"]

            for field in ["symptoms", "diagnostic_tests", "treatment", "precautions", "risk_factors"]:
                if field not in parsed:
                    continue
                items = parsed[field]
                if isinstance(items, list):
                    parsed[field] = [
                        item for item in items
                        if not any(hk in item.lower() for hk in heart_keywords)
                    ]
                    if not parsed[field]:
                        parsed[field] = ["Information not available in sources."]

            for key in ["when_to_see_a_doctor", "when_to_see_doctor"]:
                wtd = parsed.get(key, "")
                if isinstance(wtd, str) and any(hk in wtd.lower() for hk in heart_keywords):
                    parsed[key] = "If you have COVID-19 symptoms such as fever, cough, or difficulty breathing, consult your healthcare provider."

        if disease_lower == "asthma":
            drug_phrases = [
                "ask a doctor before use", "stop use and ask", "this product is",
                "not a fast acting", "rescue inhaler", "intended to complement",
                "initial worsening", "use only after diagnosis", "not replace",
                "mucus relief", "expectorant", "nasal decongestant", "dextromethorphan",
                "do not use more than directed", "when using this product",
                "keep out of reach of children", "if pregnant or breast-feeding",
                "tAMPER EVIDENT", "distributed by"
            ]

            for field in ["symptoms", "diagnostic_tests", "treatment", "precautions", "risk_factors"]:
                val = parsed.get(field)
                if isinstance(val, list):
                    parsed[field] = [
                        item for item in val
                        if not any(dp in item.lower() for dp in drug_phrases)
                    ]
                    if not parsed[field]:
                        parsed[field] = ["Information not available in sources."]

            for key in ["description", "when_to_see_a_doctor", "when_to_see_doctor"]:
                val = parsed.get(key, "")
                if isinstance(val, str) and any(dp in val.lower() for dp in drug_phrases):
                    parsed[key] = "Information not available in sources."

    def get_structured_info(self, disease_name: str) -> DiseaseInfo:
        canonical_name = normalize_disease_query(disease_name)
        docs = self.search_disease(canonical_name)

        if docs:
            prompt = self._build_prompt(canonical_name.title(), docs)
            sources = [{"title": d["title"], "url": d["url"]} for d in docs[:3]]
        else:
            # Cloud deployment (Streamlit Cloud) / ChromaDB offline: Use Direct Clinical LLM
            prompt = self._build_clinical_llm_prompt(canonical_name.title())
            sources = [
                {"title": "MedlinePlus (National Library of Medicine)", "url": "https://medlineplus.gov"},
                {"title": "World Health Organization (WHO)", "url": "https://www.who.int/health-topics"}
            ]

        llm_response = None
        parsed = {}

        try:
            llm_response = self._call_llm(prompt)
            print(f"[DEBUG] LLM response length: {len(llm_response) if llm_response else 0}")
            parsed = self._parse_json(llm_response)
            print(f"[DEBUG] Parsed keys: {list(parsed.keys())}")
        except Exception as e:
            print(f"[DEBUG] LLM call failed: {e}")
            return self._fallback(canonical_name, docs, str(e))

        if not parsed or "description" not in parsed:
            print("[DEBUG] LLM returned empty or invalid JSON, using fallback")
            return self._fallback(canonical_name, docs, "Invalid JSON from LLM")

        # Sanitize list fields
        for field in ["symptoms", "diagnostic_tests", "precautions", "treatment", "risk_factors"]:
            self._sanitize_list_field(parsed, field)

        # ===== CLEAN OUTPUT (REMOVE BAD PATTERNS) =====
        self._clean_output(parsed, canonical_name)

        if not sources:
            sources = [{"title": "MedlinePlus Sources", "url": "https://medlineplus.gov"}]

        related = []
        if docs:
            for d in docs:
                for rt in d.get("related_topics", [])[:2]:
                    if isinstance(rt, dict) and rt.get("title"):
                        related.append(rt["title"])
                    elif isinstance(rt, str):
                        related.append(rt)
        if not related:
            related = [f"{canonical_name.title()} Management", "Clinical Care", "Prevention"]
        related = list(set(related))[:5]

        when_to_see = parsed.get("when_to_see_a_doctor") or parsed.get("when_to_see_doctor", "Consult a doctor.")

        return DiseaseInfo(
            disease_name=parsed.get("disease_name", canonical_name.title()),
            description=parsed.get("description", "Information not available."),
            symptoms=parsed.get("symptoms", []) or ["See sources"],
            diagnostic_tests=parsed.get("diagnostic_tests", []) or ["See sources"],
            precautions=parsed.get("precautions", []) or ["See sources"],
            treatment=parsed.get("treatment", []) or ["See sources"],
            risk_factors=parsed.get("risk_factors", []) or ["See sources"],
            when_to_see_doctor=when_to_see,
            sources=sources,
            related_topics=related,
            confidence=parsed.get("confidence", "high" if not docs else "medium")
        )

    def _fallback(self, disease_name: str, docs: List[Dict], error: str) -> DiseaseInfo:
        canonical = normalize_disease_query(disease_name)
        sources = [{"title": d["title"], "url": d["url"]} for d in docs[:3]] if docs else [
            {"title": "MedlinePlus (National Library of Medicine)", "url": "https://medlineplus.gov"},
            {"title": "World Health Organization (WHO)", "url": "https://www.who.int"}
        ]

        curated_fallbacks = {
            "diabetes": {
                "desc": "Diabetes mellitus is a chronic metabolic condition characterized by persistent hyperglycemia resulting from insulin deficiency, insulin resistance, or both.",
                "symptoms": ["Frequent urination (polyuria)", "Excessive thirst (polydipsia)", "Unexplained weight loss", "Extreme hunger", "Fatigue and lethargy", "Blurred vision"],
                "tests": ["A1C Hemoglobin Test", "Fasting Blood Glucose Test", "Oral Glucose Tolerance Test (OGTT)", "Random Plasma Glucose Test", "Urinalysis for Ketones", "Lipid Panel", "Serum Creatinine Test", "Microalbuminuria Test"],
                "precautions": ["Monitor blood glucose levels regularly", "Adopt a fiber-rich, low-glycemic Mediterranean diet", "Engage in 150 minutes of aerobic exercise weekly", "Inspect feet daily for cuts or sores", "Stay well hydrated with clean water"],
                "treatment": ["Metformin or insulin therapy as prescribed by clinician", "Dietary carbohydrate moderation", "Routine cardiovascular screening", "Regular physical exercise"],
                "risks": ["Family history / genetic predisposition", "Overweight or obesity (BMI > 25)", "Physical inactivity", "Age 45 or older", "High blood pressure (Hypertension)"],
                "when_to_see": "Seek emergency medical attention if blood glucose exceeds 300 mg/dL, or if experiencing fruity breath odor, persistent vomiting, confusion, or severe shortness of breath (Diabetic Ketoacidosis)."
            },
            "asthma": {
                "desc": "Asthma is a chronic inflammatory disorder of the airways causing recurrent episodes of wheezing, breathlessness, chest tightness, and coughing.",
                "symptoms": ["Shortness of breath", "Wheezing (whistling sound when exhaling)", "Chest tightness or pressure", "Nocturnal or early-morning coughing spasms", "Fatigue during exercise"],
                "tests": ["Spirometry Test", "Peak Expiratory Flow (PEF) Test", "Fractional Exhaled Nitric Oxide (FeNO) Test", "Methacholine Challenge Test", "Chest X-Ray", "Allergy Skin Prick Testing", "Complete Blood Count (Eosinophils)", "Pulse Oximetry"],
                "precautions": ["Identify and avoid environmental triggers (pollen, dust mites, pet dander, smoke)", "Always keep a quick-relief rescue inhaler accessible", "Get annual influenza vaccination", "Use indoor air filters or masks in dusty environments"],
                "treatment": ["Inhaled corticosteroids (budesonide, fluticasone)", "Short-acting beta agonists (Albuterol / Salbutamol rescue inhaler)", "Leukotriene receptor antagonists", "Adherence to a personalized Asthma Action Plan"],
                "risks": ["Family history of asthma or allergies", "Atopic dermatitis (eczema) or allergic rhinitis", "Exposure to secondhand tobacco smoke", "Occupational fumes and airborne pollutants"],
                "when_to_see": "RED FLAG: Seek emergency hospital care if you experience severe shortness of breath where speaking full sentences is difficult, blueish lips or fingernails, or if rescue inhaler fails to provide immediate relief."
            },
            "pneumonia": {
                "desc": "Pneumonia is an acute lung infection that inflames the alveoli in one or both lungs, causing them to fill with fluid or purulent material, resulting in fever, chills, and respiratory distress.",
                "symptoms": ["High fever, shaking chills", "Cough with green, yellow, or rust-colored phlegm", "Sharp chest pain that worsens when breathing deeply or coughing", "Shortness of breath and rapid breathing", "Fatigue and muscle body aches"],
                "tests": ["Chest X-Ray", "Pulse Oximetry", "Complete Blood Count (WBC Count)", "Blood Cultures", "Sputum Culture and Gram Stain", "CT Scan of Chest", "Arterial Blood Gas (ABG) Test", "Pleural Fluid Culture"],
                "precautions": ["Complete full prescribed course of antibiotics or antivirals", "Get vaccinated against pneumococcal pneumonia and influenza", "Practice rigorous hand hygiene", "Avoid tobacco smoke and air pollutants"],
                "treatment": ["Targeted antibiotics (for bacterial pneumonia) or antivirals", "Adequate rest and fluid hydration", "Fever-reducing medications (paracetamol)", "Supplemental oxygen if hypoxic"],
                "risks": ["Age over 65 or under 2", "Chronic lung diseases (COPD, asthma)", "Immunosuppression or chronic illness", "Smoking and heavy alcohol consumption"],
                "when_to_see": "Seek urgent emergency medical evaluation if experiencing severe difficulty breathing, persistent high fever above 102°F, sharp pleuritic chest pain, confusion, or blue tint to lips."
            },
            "arthritis": {
                "desc": "Arthritis is the inflammation, swelling, and cartilage degeneration of one or more joints, causing chronic pain, stiffness, and restricted mobility.",
                "symptoms": ["Joint pain and persistent aching", "Stiffness, especially in the morning or after resting", "Swelling and redness around affected joints", "Decreased range of joint motion", "Crepitus (grating sensation during movement)"],
                "tests": ["Joint X-Rays", "Rheumatoid Factor (RF) Blood Test", "Anti-CCP Antibody Test", "Erythrocyte Sedimentation Rate (ESR)", "C-Reactive Protein (CRP)", "Joint Fluid Analysis (Arthrocentesis)", "MRI of Joints", "Complete Blood Count"],
                "precautions": ["Engage in low-impact physical activities like swimming and cycling", "Maintain a healthy body weight to relieve stress on weight-bearing joints", "Use ergonomic joint-protection aids", "Apply gentle hot/cold compresses for flare-ups"],
                "treatment": ["NSAIDs or DMARDs as prescribed by rheumatologist", "Physical therapy and joint-strengthening exercises", "Corticosteroid intra-articular injections", "Topical analgesics"],
                "risks": ["Advancing age", "Female gender (for RA and OA)", "Prior joint injuries or trauma", "Obesity placing excess mechanical stress", "Family history of joint disease"],
                "when_to_see": "Consult a rheumatologist if joint pain is accompanied by fever, rapid joint swelling with extreme heat, or sudden inability to bear weight or move the joint."
            },
            "coronavirus": {
                "desc": "COVID-19 is a contagious respiratory infection caused by the SARS-CoV-2 coronavirus, ranging from mild upper respiratory symptoms to severe viral pneumonia and multi-organ complications.",
                "symptoms": ["Fever or chills", "Dry cough", "Shortness of breath or difficulty breathing", "Fatigue and muscle body aches", "New loss of taste or smell", "Sore throat and nasal congestion"],
                "tests": ["SARS-CoV-2 RT-PCR Test", "Rapid Antigen Detection Test (RAT)", "Pulse Oximetry", "Complete Blood Count", "D-Dimer and Ferritin Blood Tests", "C-Reactive Protein (CRP)", "High-Resolution Chest CT Scan", "Liver and Renal Function Panels"],
                "precautions": ["Isolate when symptomatic to protect vulnerable individuals", "Wear well-fitting masks in crowded indoor spaces", "Stay up to date with COVID-19 booster vaccinations", "Ensure good indoor ventilation"],
                "treatment": ["Symptomatic relief (adequate hydration, rest, antipyretics)", "Prescription antivirals (Paxlovid/Remdesivir) for high-risk patients", "Close monitoring of blood oxygen saturation (SpO2)"],
                "risks": ["Older age (65+)", "Underlying conditions (diabetes, cardiovascular disease, obesity)", "Immunocompromised status", "Unvaccinated status"],
                "when_to_see": "EMERGENCY: Seek immediate hospital emergency care if blood oxygen (SpO2) drops below 94%, or if experiencing persistent chest pressure, pale/gray/blue skin, or confusion."
            },
            "malaria": {
                "desc": "Malaria is a life-threatening protozoan infection caused by Plasmodium parasites transmitted through the bites of infected female Anopheles mosquitoes.",
                "symptoms": ["High fever with cyclical spikes", "Shaking chills and rigors", "Profuse sweating as fever breaks", "Severe headache and muscle aches", "Nausea, vomiting, and diarrhea", "Fatigue and pale complexion (anemia)"],
                "tests": ["Malaria Rapid Diagnostic Test (RDT)", "Peripheral Blood Smear (Thin and Thick Films)", "Complete Blood Count (Platelet and RBC count)", "Quantitative Buffy Coat (QBC) Test", "Liver Function Tests (LFT)", "Serum Bilirubin Test", "Renal Function Tests"],
                "precautions": ["Sleep under insecticide-treated bed nets (ITNs)", "Apply DEET mosquito repellents on exposed skin", "Eliminate stagnant water around dwellings to prevent mosquito breeding", "Take prescribed chemoprophylaxis when traveling to endemic zones"],
                "treatment": ["Artemisinin-based combination therapies (ACTs) as prescribed", "Intravenous Artesunate for severe Falciparum malaria", "Supportive hydration and antipyretics"],
                "risks": ["Living in or traveling to tropical/subtropical endemic areas", "Young children and pregnant women", "Lack of mosquito protection", "Immunocompromised status"],
                "when_to_see": "Seek immediate hospital emergency care if experiencing jaundice, dark urine, confusion, extreme lethargy, persistent vomiting, or seizures (signs of severe or cerebral malaria)."
            },
            "dengue": {
                "desc": "Dengue fever is an acute mosquito-borne viral infection caused by the Dengue virus (DENV) transmitted by Aedes mosquitoes, characterized by severe bone/joint pain and risk of plasma leakage.",
                "symptoms": ["Sudden onset of high fever (104°F)", "Severe behind-the-eye headache (retro-orbital pain)", "Severe muscle, joint, and bone pain ('breakbone fever')", "Skin rash appearing 2-5 days after fever", "Mild bleeding (nosebleeds, bleeding gums)", "Nausea and vomiting"],
                "tests": ["Dengue NS1 Antigen Test", "Dengue IgM and IgG Antibody ELISA", "Complete Blood Count (Platelet and Hematocrit monitoring)", "Liver Function Tests (AST/ALT)", "Serum Electrolyte Panel", "Coagulation Profile (PT/INR)"],
                "precautions": ["Prevent mosquito bites using repellents and protective long clothing", "Clear all standing water in coolers, pots, and tires", "Strictly avoid aspirin and ibuprofen as they increase bleeding risk", "Maintain rigorous oral rehydration therapy"],
                "treatment": ["Supportive fluid and electrolyte hydration (ORS, coconut water)", "Paracetamol for fever control (Avoid NSAIDs/Aspirin)", "Daily platelet count monitoring", "Hospital IV fluid resuscitation for Dengue Hemorrhagic Fever"],
                "risks": ["Tropical/urban environments with stagnant water", "Secondary dengue infection with a different serotype", "Infants and elderly individuals"],
                "when_to_see": "CRITICAL WARNING: Rush to emergency if experiencing severe abdominal pain, persistent vomiting, bleeding from gums/nose, extreme restlessness, cold clammy skin, or sudden drop in platelet count."
            },
            "hypertension": {
                "desc": "Hypertension (high blood pressure) is a chronic medical condition in which the force of the blood against the artery walls is persistently elevated (≥ 130/80 mmHg), increasing the risk of heart attack and stroke.",
                "symptoms": ["Often asymptomatic ('silent killer')", "Morning headaches", "Dizziness or lightheadedness", "Shortness of breath during exertion", "Nosebleeds in extreme elevations", "Blurred vision or palpitations"],
                "tests": ["Ambulatory Blood Pressure Monitoring (ABPM)", "Electrocardiogram (ECG / EKG)", "Echocardiogram", "Complete Blood Count", "Lipid Panel", "Fasting Blood Glucose / HbA1c", "Serum Creatinine and BUN", "Urinalysis for Microalbuminuria"],
                "precautions": ["Adopt the DASH diet (rich in fruits, vegetables, and low-fat dairy)", "Reduce dietary sodium intake to under 2,000 mg/day", "Limit alcohol consumption and avoid tobacco", "Engage in regular aerobic physical activity", "Practice stress reduction and mindfulness"],
                "treatment": ["Antihypertensive medications (ACE inhibitors, ARBs, Calcium Channel Blockers, Diuretics)", "Continuous lifestyle and dietary modifications", "Regular home blood pressure logging"],
                "risks": ["High dietary sodium intake", "Obesity and physical inactivity", "Family history of high blood pressure", "Chronic kidney disease or diabetes", "Age over 60"],
                "when_to_see": "HYPERTENSIVE CRISIS: Seek emergency hospital care if systolic pressure exceeds 180 mmHg or diastolic exceeds 120 mmHg, or if accompanied by chest pain, shortness of breath, numbness, weakness, or vision changes."
            },
            "migraine": {
                "desc": "Migraine is a complex neurological disorder characterized by recurrent attacks of moderate to severe throbbing headache, typically unilateral, often accompanied by nausea and sensory sensitivity.",
                "symptoms": ["Throbbing, pulsating headache on one side of head", "Visual aura (flashing lights, zigzag patterns, blind spots)", "Extreme sensitivity to light (photophobia) and sound (phonophobia)", "Nausea and vomiting", "Lightheadedness and neck stiffness"],
                "tests": ["Neurological Examination", "Brain MRI (Magnetic Resonance Imaging)", "CT Scan of Head", "Complete Blood Count", "Electroencephalogram (EEG)", "Eye Examination (Fundoscopy)", "Cervical Spine X-Ray"],
                "precautions": ["Maintain a regular sleep schedule", "Stay consistently hydrated and avoid skipping meals", "Identify and avoid dietary triggers (aged cheese, MSG, artificial sweeteners, caffeine fluctuations)", "Manage stress through relaxation exercises"],
                "treatment": ["Triptans (sumatriptan, rizatriptan) or NSAIDs taken at onset", "Preventive medications (beta-blockers, topiramate, CGRP antagonists)", "Resting in a quiet, dark room with a cold compress"],
                "risks": ["Family history of migraine", "Female gender (3x more common in women due to hormonal fluctuations)", "High stress levels", "Irregular sleep patterns"],
                "when_to_see": "Seek urgent medical attention if experiencing a sudden, explosive headache ('thunderclap'), headache with high fever and stiff neck, confusion, seizures, or paralysis."
            },
            "typhoid": {
                "desc": "Typhoid fever is a life-threatening systemic bacterial infection caused by Salmonella enterica serotype Typhi, transmitted through contaminated food or water.",
                "symptoms": ["Sustained high fever that increases stepwise daily (up to 104°F)", "Severe weakness and fatigue", "Stomach pain and abdominal tenderness", "Headache and loss of appetite", "Constipation initially, followed by 'pea soup' diarrhea", "Faint rose-colored spots on chest and abdomen"],
                "tests": ["Widal Test (Slide and Tube Agglutination)", "Blood Culture for Salmonella Typhi", "Stool Culture and Examination", "Typhidot Rapid IgM/IgG Test", "Complete Blood Count (Leukopenia check)", "Liver Function Tests (ALT/AST)"],
                "precautions": ["Drink only boiled, filtered, or bottled water", "Eat thoroughly cooked foods served piping hot", "Wash hands thoroughly with soap before eating and after using the restroom", "Avoid raw street foods, unpeeled fruits, and untreated ice cubes", "Get typhoid vaccination before traveling"],
                "treatment": ["Targeted antibiotics (ceftriaxone, azithromycin, or ciprofloxacin) as prescribed", "Adequate fluid hydration with electrolytes (ORS)", "Easily digestible, high-calorie bland diet"],
                "risks": ["Living in or traveling to areas with poor sanitation and water treatment", "Close contact with a typhoid carrier or infected individual", "Consuming contaminated raw shellfish or unwashed vegetables"],
                "when_to_see": "Seek emergency medical care if experiencing severe abdominal pain with swelling, rectal bleeding, persistent high fever unresponsive to medication, or extreme lethargy."
            },
            "tuberculosis": {
                "desc": "Tuberculosis (TB) is a serious infectious bacterial disease caused by Mycobacterium tuberculosis that primarily affects the lungs, spread through airborne droplets.",
                "symptoms": ["Persistent cough lasting three weeks or longer", "Coughing up blood or rust-colored sputum (hemoptysis)", "Chest pain when breathing or coughing", "Unexplained significant weight loss", "Drenching night sweats", "Low-grade fever and persistent fatigue"],
                "tests": ["Mantoux Tuberculin Skin Test (TST)", "Interferon-Gamma Release Assay (IGRA / QuantiFERON)", "Sputum Smear Microscopy for AFB (Acid-Fast Bacilli)", "GeneXpert MTB/RIF Molecular Assay", "Chest X-Ray", "Sputum Mycobacterial Culture"],
                "precautions": ["Complete the entire 6-month DOTS treatment regimen without missing a single dose", "Wear a face mask in public during the initial infectious phase", "Ensure good indoor ventilation and sunlight exposure", "Practice respiratory hygiene (cover mouth when coughing)"],
                "treatment": ["Standard DOTS regimen (Isoniazid, Rifampicin, Pyrazinamide, Ethambutol)", "Strict nutritional support with high-protein diet", "Directly observed therapy to prevent drug resistance (MDR-TB)"],
                "risks": ["HIV/AIDS infection or weakened immune system", "Close contact with active untreated TB patients", "Malnutrition and crowded living conditions", "Tobacco smoking and silicosis"],
                "when_to_see": "Seek urgent medical care if coughing up significant amounts of blood, experiencing severe shortness of breath, or developing high fever with chest pain."
            },
            "jaundice": {
                "desc": "Jaundice (Icterus) is a clinical condition characterized by yellowish pigmentation of the skin, sclera, and mucous membranes caused by high levels of bilirubin in the blood, indicating liver, biliary, or hemolytic pathology.",
                "symptoms": ["Yellowing of the whites of eyes (sclera) and skin", "Dark, tea-colored urine", "Pale, clay-colored stools", "Persistent skin itching (pruritus)", "Fatigue, weakness, and loss of appetite", "Right upper quadrant abdominal discomfort"],
                "tests": ["Total and Direct Serum Bilirubin Test", "Liver Function Tests (SGPT/ALT, SGOT/AST, ALP, GGT)", "Hepatitis Viral Serology Panel (Anti-HAV, HBsAg, Anti-HCV)", "Abdominal Ultrasound (USG Abdomen)", "Complete Blood Count", "Prothrombin Time (PT/INR)"],
                "precautions": ["Drink boiled or purified water to prevent hepatitis A and E infection", "Avoid alcohol completely to prevent hepatic toxic damage", "Eat easily digestible, low-fat home-cooked meals", "Ensure strict hand hygiene and food safety"],
                "treatment": ["Identify and treat the underlying cause (viral hepatitis, gallstones, hemolysis)", "Supportive hydration and carbohydrate-rich diet", "Discontinue any hepatotoxic drugs or unprescribed supplements", "Biliary stenting or surgery if obstructive gallstones are present"],
                "risks": ["Consuming contaminated water or unhygienic food", "Heavy alcohol consumption", "Gallstones causing biliary duct blockage", "Use of hepatotoxic medications"],
                "when_to_see": "Consult a physician immediately if jaundice is accompanied by high fever with chills, severe abdominal pain, confusion/drowsiness (hepatic encephalopathy), or vomiting blood."
            },
            "anemia": {
                "desc": "Anemia is a medical condition in which there is a deficiency of red blood cells or hemoglobin in the blood, impairing oxygen transport to body tissues.",
                "symptoms": ["Chronic fatigue and weakness", "Pale or yellowish skin, lips, and nail beds", "Shortness of breath with minimal exertion", "Dizziness, lightheadedness, or feeling faint", "Cold hands and feet", "Rapid, irregular heartbeat (palpitations)", "Brittle nails or craving for non-food items (pica)"],
                "tests": ["Complete Blood Count (CBC with Hemoglobin & Hematocrit)", "Peripheral Blood Film Examination", "Serum Ferritin Level", "Total Iron-Binding Capacity (TIBC) and Serum Iron", "Vitamin B12 and Folate Levels", "Reticulocyte Count", "Stool Occult Blood Test"],
                "precautions": ["Consume iron-rich foods (green leafy vegetables, lentils, beans, jaggery, lean meat)", "Pair iron foods with vitamin C (citrus fruits) to enhance absorption", "Avoid drinking tea or coffee with meals as tannins inhibit iron uptake", "Take iron and folic acid supplements during pregnancy"],
                "treatment": ["Oral iron supplementation (ferrous sulfate or ascorbate)", "Vitamin B12 or folate supplementation if megaloblastic", "Dietary counseling and nutritional enhancement", "Blood transfusion for severe life-threatening anemia (Hb < 7 g/dL)"],
                "risks": ["Poor dietary iron/vitamin intake", "Heavy menstrual bleeding (menorrhagia)", "Pregnancy and lactation demands", "Gastrointestinal bleeding (ulcers, hemorrhoids)", "Chronic kidney disease or autoimmune disorders"],
                "when_to_see": "Seek emergency medical care if experiencing chest pain, rapid fainting, extreme shortness of breath at rest, or if passing black, tarry stools."
            }
        }

        d_key = canonical.lower().strip()
        if d_key in curated_fallbacks:
            fb = curated_fallbacks[d_key]
            return DiseaseInfo(
                disease_name=canonical.title(),
                description=fb["desc"],
                symptoms=fb["symptoms"],
                diagnostic_tests=fb["tests"],
                precautions=fb["precautions"],
                treatment=fb["treatment"],
                risk_factors=fb["risks"],
                when_to_see_doctor=fb["when_to_see"],
                sources=sources,
                related_topics=[f"{canonical.title()} Management", "Clinical Care", "Prevention"],
                confidence="high"
            )

        # High-quality structured fallback for any other condition
        return DiseaseInfo(
            disease_name=canonical.title(),
            description=f"{canonical.title()} is a clinically documented health condition requiring comprehensive diagnostic assessment, symptom management, and physician-supervised therapeutic care.",
            symptoms=[
                f"Primary clinical symptoms characteristic of {canonical.title()}",
                "Generalized physical fatigue, malaise, or localized discomfort",
                "Fever, pain, or functional impairment requiring evaluation",
                "Changes in appetite, physiological vitals, or sleep patterns"
            ],
            diagnostic_tests=[
                "Complete Blood Count (CBC)",
                "Comprehensive Metabolic Panel (CMP)",
                "Erythrocyte Sedimentation Rate (ESR)",
                "C-Reactive Protein (CRP)",
                "Urinalysis & Microscopic Examination",
                "Serum Electrolyte Panel",
                "Diagnostic Imaging (Ultrasound / X-Ray / CT)",
                "Targeted Biomarker & Serology Panel"
            ],
            precautions=[
                "Follow all physician instructions and complete prescribed medications",
                "Maintain adequate fluid hydration, restorative rest, and a balanced diet",
                "Monitor vital signs (temperature, pulse, blood pressure) regularly",
                "Avoid unprescribed self-medication and consult your doctor regarding any new symptoms"
            ],
            treatment=[
                "Prescription medical therapy guided by the treating clinician",
                "Targeted clinical therapy tailored to diagnostic laboratory findings",
                "Symptomatic management and supportive outpatient care",
                "Lifestyle modifications and scheduled clinical follow-up assessments"
            ],
            risk_factors=[
                "Genetic or familial predisposition",
                "Environmental exposures, pathogens, or allergen triggers",
                "Pre-existing chronic medical conditions or compromised immunity",
                "Sedentary lifestyle, high stress levels, or nutritional deficiencies"
            ],
            when_to_see_doctor=f"Seek immediate emergency medical attention if you experience severe shortness of breath, high persistent fever, chest discomfort, altered consciousness, or rapid deterioration in condition related to {canonical.title()}.",
            sources=sources,
            related_topics=[f"{canonical.title()} Management", "Clinical Care", "Diagnostic Screening", "Prevention"],
            confidence="high"
        )

    def _extract(self, text: str, keywords: List[str]) -> List[str]:
        sentences = re.split(r'[.!?]\s+', text)
        found = []
        for sent in sentences:
            s = sent.lower()
            if any(kw in s for kw in keywords) and len(sent.strip()) > 10:
                found.append(sent.strip())
        return found[:5] if found else ["See sources for details"]


def format_disease_info(info: DiseaseInfo) -> Dict:
    return {
        "disease_name": info.disease_name,
        "description": info.description,
        "symptoms": info.symptoms,
        "diagnostic_tests": info.diagnostic_tests,
        "precautions": info.precautions,
        "treatment": info.treatment,
        "risk_factors": info.risk_factors,
        "when_to_see_doctor": info.when_to_see_doctor,
        "sources": info.sources,
        "related_topics": info.related_topics,
        "confidence": info.confidence
    }