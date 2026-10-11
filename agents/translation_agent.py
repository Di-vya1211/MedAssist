"""
Translation agent.

Purpose: MedlinePlus only returns English (or Spanish) content. Rural users
need the final response in their own language. This module translates text
into Hindi (or any other language) using the free Google Translate backend
via the deep-translator library.

Install requirement:
    pip install deep-translator

Note: This needs an internet connection at runtime (it calls Google's
translation service). If there is no internet, translation will fail —
handle that failure by falling back to the original English text, so the
user still gets an answer.
"""

from deep_translator import GoogleTranslator

# Languages the user can choose from, mapped to Google Translate's language codes.
# Add more entries here if you need to support additional Indian languages.
SUPPORTED_LANGUAGES = {
    "1": ("Hindi", "hi"),
    "2": ("Bengali", "bn"),
    "3": ("Tamil", "ta"),
    "4": ("Telugu", "te"),
    "5": ("Marathi", "mr"),
    "6": ("Gujarati", "gu"),
    "7": ("Punjabi", "pa"),
    "8": ("Kannada", "kn"),
    "9": ("Malayalam", "ml"),
    "10": ("Odia", "or"),
    "11": ("Urdu", "ur"),
    "12": ("English (no translation)", "en"),
}


def prompt_language_choice() -> str:
    """
    Shows a numbered menu of supported languages and asks the user to pick
    one. Returns the language code (e.g. 'hi') for the chosen language.
    Keeps asking until a valid number is entered.
    """
    print("\nApni bhasha chunein / Select your language:")
    for key, (name, _) in SUPPORTED_LANGUAGES.items():
        print(f"  {key}. {name}")

    while True:
        choice = input("Number daalein: ").strip()
        if choice in SUPPORTED_LANGUAGES:
            name, code = SUPPORTED_LANGUAGES[choice]
            print(f"Selected: {name}\n")
            return code
        print("Galat choice, dobara try karein.")


# MedlinePlus field names that contain readable text worth translating.
# We skip fields like 'url' and 'mesh' (medical vocabulary code, not prose).
TRANSLATABLE_FIELDS = ["title", "altTitle", "FullSummary", "snippet"]


_llm_translator = None

def _get_llm_translator():
    global _llm_translator
    if _llm_translator is None:
        try:
            import os, sys
            sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            from core.llm import LLMClient
            _llm_translator = LLMClient()
        except Exception as e:
            print(f"[translation_agent] LLM client init error: {e}")
            _llm_translator = False
    return _llm_translator if _llm_translator else None


_translation_cache = {}

def translate_with_llm(text: str, target_lang: str = "hi") -> str:
    """Translates text using LLM when GoogleTranslator fails."""
    llm = _get_llm_translator()
    if not llm or not text or len(text.strip()) < 2:
        return text
    lang_names = {
        "hi": "Hindi", "bn": "Bengali", "ta": "Tamil", "te": "Telugu",
        "mr": "Marathi", "gu": "Gujarati", "pa": "Punjabi", "kn": "Kannada",
        "ml": "Malayalam", "or": "Odia", "ur": "Urdu", "en": "English"
    }
    lang_name = lang_names.get(target_lang, "Hindi")
    prompt = (
        f"You are a medical translator. Translate the following medical health text into simple, natural {lang_name} (हिन्दी).\n"
        f"Keep medicine brand names and scientific drug names in English in brackets if helpful.\n"
        f"Output ONLY the translated text without explanations, headers, or quotes:\n\n{text}"
    )
    try:
        translated = llm.generate(prompt).strip()
        # Verify translation didn't return an error message or placeholder
        if translated and len(translated) >= 3:
            if not any(bad in translated for bad in ["Based on standard", "LLM service currently unavailable", "RuntimeError", "error occurred"]):
                return translated
        return text
    except Exception as e:
        print(f"[translation_agent] LLM fallback translation notice: {e}")
        return text


def translate_text(text: str, target_lang: str = "hi") -> str:
    """
    Translates a single string into the target language.
    Tries GoogleTranslator first; falls back to LLM, then safely preserves original text.
    """
    if not text or target_lang == "en" or not str(text).strip():
        return text

    clean_str = str(text).strip()
    cache_key = (clean_str, target_lang)
    if cache_key in _translation_cache:
        return _translation_cache[cache_key]

    result = clean_str
    try:
        translated = GoogleTranslator(source="auto", target=target_lang).translate(clean_str)
        if translated and str(translated).strip():
            result = translated
    except Exception as e:
        print(f"[translation_agent] GoogleTranslator notice ({e}), trying LLM...")
        result = translate_with_llm(clean_str, target_lang=target_lang)

    _translation_cache[cache_key] = result
    return result


def translate_pipeline_output(pipeline_output: dict, target_lang: str = "hi") -> dict:
    """
    Takes the full pipeline output (from pipeline.run_pipeline) and translates
    the human-readable fields inside 'results', plus the safety messages.
    Returns a new dict — does not modify the original in place.
    """
    if pipeline_output.get("status") != "ok":
        return pipeline_output

    translated_results = []
    for item in pipeline_output.get("results", []):
        new_item = dict(item)  # copy so we don't mutate the original
        for field in TRANSLATABLE_FIELDS:
            if field in new_item:
                new_item[field] = translate_text(new_item[field], target_lang)
        translated_results.append(new_item)

    pipeline_output["results"] = translated_results

    if pipeline_output.get("safety_message"):
        pipeline_output["safety_message"] = translate_text(pipeline_output["safety_message"], target_lang)
    if pipeline_output.get("disclaimer"):
        pipeline_output["disclaimer"] = translate_text(pipeline_output["disclaimer"], target_lang)

    return pipeline_output


if __name__ == "__main__":
    # Quick manual test — needs internet to actually call Google Translate
    sample = "A fever is a body temperature that is higher than normal."
    print(f"Original: {sample}")
    print(f"Translated: {translate_text(sample)}")