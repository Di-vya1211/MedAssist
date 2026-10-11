"""
core/llm.py
Multi-LLM Manager supporting Groq (with multi-model failover) and Gemini Flash
Designed to seamlessly operate across both Localhost and Streamlit Community Cloud.
"""

import os
import re
from enum import Enum
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv

# ═════════════════════════════════════════════════════════════════
# Load .env from config/ folder
# ═════════════════════════════════════════════════════════════════
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, "config", ".env")

if os.path.exists(ENV_PATH):
    load_dotenv(ENV_PATH)
else:
    load_dotenv()


def get_api_key(key_name: str) -> Optional[str]:
    """
    Robust API key resolution across:
    1. os.environ (case variations)
    2. Streamlit Cloud Secrets (st.secrets root and sub-tables)
    """
    # 1. Environment variables
    for k in [key_name, key_name.upper(), key_name.lower()]:
        val = os.getenv(k)
        if val and str(val).strip():
            return str(val).strip()

    # 2. Streamlit secrets
    try:
        import streamlit as st
        if hasattr(st, "secrets"):
            for k in [key_name, key_name.upper(), key_name.lower()]:
                if k in st.secrets:
                    s_val = st.secrets[k]
                    if isinstance(s_val, str) and s_val.strip():
                        return s_val.strip()

            # Nested sections e.g. st.secrets["groq"]["api_key"]
            name_upper = key_name.upper()
            if "GROQ" in name_upper and "groq" in st.secrets:
                sec = st.secrets["groq"]
                if isinstance(sec, dict) and "api_key" in sec:
                    return str(sec["api_key"]).strip()
            if "GEMINI" in name_upper and "gemini" in st.secrets:
                sec = st.secrets["gemini"]
                if isinstance(sec, dict) and "api_key" in sec:
                    return str(sec["api_key"]).strip()
    except Exception:
        pass

    return None


class LLMProvider(Enum):
    TINYLLAMA = "tinyllama"
    GROQ = "groq"
    GEMINI = "gemini"


GROQ_MODELS = [
    "openai/gpt-oss-120b",
    "openai/gpt-oss-20b",
    "qwen/qwen3.8-27b",
    "allam-2-7b"
]


class LLMManager:
    def __init__(self, provider: LLMProvider = LLMProvider.GROQ):
        self.provider = provider
        self.llm = None
        self._direct_groq = None
        self.model_name = GROQ_MODELS[0]
        self._init_model()

    def _init_model(self):
        if self.provider == LLMProvider.TINYLLAMA:
            try:
                from langchain_community.llms import Ollama
                self.llm = Ollama(model="tinyllama", temperature=0.3, num_ctx=4096)
                print("[LLM] TinyLlama loaded")
            except Exception as e:
                raise RuntimeError(f"TinyLlama failed: {e}")

        elif self.provider == LLMProvider.GROQ:
            try:
                from groq import Groq
                api_key = get_api_key("GROQ_API_KEY")
                if not api_key:
                    raise ValueError("GROQ_API_KEY not found in env or st.secrets")

                self._direct_groq = Groq(api_key=api_key)
                self.model_name = GROQ_MODELS[0]
                print(f"[LLM] Groq loaded with primary model: {self.model_name}")
            except Exception as e:
                raise RuntimeError(f"Groq initialization failed: {e}")

        elif self.provider == LLMProvider.GEMINI:
            try:
                import google.generativeai as genai
                api_key = get_api_key("GEMINI_API_KEY")
                if not api_key:
                    raise ValueError("GEMINI_API_KEY not found in env or st.secrets")

                genai.configure(api_key=api_key)
                self.llm = genai.GenerativeModel("gemini-3.8-flash")
                self._is_direct_genai = True
                print("[LLM] Gemini (direct genai) loaded")
            except Exception as e:
                try:
                    from langchain_google_genai import ChatGoogleGenerativeAI
                    api_key = get_api_key("GEMINI_API_KEY")
                    self.llm = ChatGoogleGenerativeAI(
                        model="gemini-3.8-flash",
                        temperature=0.2,
                        max_output_tokens=2048,
                        google_api_key=api_key
                    )
                    self._is_direct_genai = False
                    print("[LLM] Gemini (ChatGoogleGenerativeAI) loaded")
                except Exception as e2:
                    raise RuntimeError(f"Gemini failed: {e2}")

    def generate(self, prompt: str) -> str:
        # Provider 1: Groq with automatic multi-model failover
        if self._direct_groq is not None:
            last_err = None
            for model_candidate in GROQ_MODELS:
                try:
                    chat = self._direct_groq.chat.completions.create(
                        messages=[{"role": "user", "content": prompt}],
                        model=model_candidate,
                        temperature=0.2,
                        max_tokens=2048,
                    )
                    if chat.choices and chat.choices[0].message and chat.choices[0].message.content:
                        return chat.choices[0].message.content
                except Exception as e:
                    last_err = e
                    print(f"[LLM] Groq model '{model_candidate}' failed: {e}, trying next candidate...")
                    continue
            raise RuntimeError(f"All Groq models failed. Last error: {last_err}")

        if not self.llm:
            raise RuntimeError("LLM not initialized")

        try:
            if getattr(self, '_is_direct_genai', False):
                resp = self.llm.generate_content(prompt)
                return resp.text
            response = self.llm.invoke(prompt)
            if hasattr(response, 'content'):
                return response.content
            return str(response)
        except Exception as e:
            raise RuntimeError(f"Gemini LLM error: {e}")


# ═════════════════════════════════════════════════════════════════
# LLMClient: Auto-fallback GROQ → GEMINI → Graceful Heuristic
# ═════════════════════════════════════════════════════════════════
class LLMClient:
    def __init__(self):
        self._manager = None
        self._provider = None
        self._init_with_fallback()

    def _init_with_fallback(self):
        # Try GROQ first
        try:
            self._manager = LLMManager(provider=LLMProvider.GROQ)
            self._provider = "groq"
            print("[LLMClient] Primary provider: Groq")
            return
        except Exception as e:
            print(f"[LLMClient] Groq initialization failed: {e}")

        # Fallback to GEMINI
        try:
            self._manager = LLMManager(provider=LLMProvider.GEMINI)
            self._provider = "gemini"
            print("[LLMClient] Fallback provider: Gemini")
            return
        except Exception as e:
            print(f"[LLMClient] Gemini fallback failed: {e}")

        print("[LLMClient] Warning: Could not initialize cloud LLMs. Check API keys.")

    def generate(self, prompt: str) -> str:
        # Attempt primary provider
        if self._manager is not None:
            try:
                return self._manager.generate(prompt)
            except Exception as e:
                print(f"[LLMClient] Primary provider ({self._provider}) error: {e}")

                # If Groq failed, try Gemini as dynamic fallback
                if self._provider == "groq":
                    try:
                        print("[LLMClient] Attempting dynamic switch to Gemini...")
                        alt_manager = LLMManager(provider=LLMProvider.GEMINI)
                        res = alt_manager.generate(prompt)
                        self._manager = alt_manager
                        self._provider = "gemini"
                        return res
                    except Exception as gem_err:
                        print(f"[LLMClient] Gemini fallback also failed: {gem_err}")
                elif self._provider == "gemini":
                    try:
                        print("[LLMClient] Attempting dynamic switch to Groq...")
                        alt_manager = LLMManager(provider=LLMProvider.GROQ)
                        res = alt_manager.generate(prompt)
                        self._manager = alt_manager
                        self._provider = "groq"
                        return res
                    except Exception as groq_err:
                        print(f"[LLMClient] Groq fallback also failed: {groq_err}")

        # Fallback clinical response when offline or network fails
        return (
            "Based on standard clinical guidelines, it is advised to monitor your symptoms closely, "
            "stay hydrated, maintain adequate rest, and avoid self-medicating without medical guidance. "
            "If symptoms worsen or red flags appear, please consult a licensed healthcare professional promptly."
        )


# Backward compatibility
class FreeLLM:
    def __init__(self):
        self._llm = LLMClient()

    def predict(self, prompt, temperature=0.7):
        return self._llm.generate(prompt)