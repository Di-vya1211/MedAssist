# -*- coding: utf-8 -*-
"""
MedAssist - Wellness Hub UI Component
Authoritative Ayurvedic & Home Remedies, ICMR Nutrition, and Active Allergy Safeguard.
Sources:
- Ministry of AYUSH, Govt of India (ayush.gov.in)
- National Health Portal (NHP India - nhp.gov.in)
- Indian Council of Medical Research (ICMR - icmr.gov.in)
- WHO Traditional Medicine Guidelines (who.int)
- NIH MedlinePlus & PubMed Central
"""

import os
import streamlit as st
from typing import Optional, Dict, Any, List

from wellness.wellness_dataset import (
    CATEGORIES,
    WELLNESS_DATA,
    get_all_categories,
    get_topics_by_category,
    get_topic_by_id,
    search_wellness_topics,
    check_allergy_warnings,
)
from voice.voice_ui import render_voice_input_widget, render_read_aloud_widget
from voice.voice_service import voice_service


def render_wellness_hub_tab(patient_id: Optional[int] = None, patient_db = None):
    """
    Renders the complete 🌿 Wellness Hub module:
    - 10 verified health categories with 93 clinical topics
    - Bilingual content (English & Hindi)
    - Open Voice Input (Speech-to-Text)
    - Voice Output / Read Aloud (Text-to-Speech)
    - Active cross-check against patient allergy profile
    - Verified AYUSH, NHP, ICMR, and WHO citations
    - Strict Red-Flag Doctor Consultation alerts
    """
    st.markdown("""
    <style>
    .wellness-header-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(6, 182, 212, 0.15));
        border: 1px solid rgba(16, 185, 129, 0.4);
        padding: 4px 12px;
        border-radius: 9999px;
        color: #34d399;
        font-size: 0.8rem;
        font-weight: 600;
        margin-bottom: 8px;
    }
    .wellness-card {
        background: rgba(15, 23, 42, 0.75);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 18px 20px;
        margin-bottom: 16px;
        backdrop-filter: blur(8px);
    }
    .wellness-card:hover {
        border-color: rgba(56, 189, 248, 0.3);
    }
    .remedy-box-ayush {
        background: rgba(16, 185, 129, 0.08);
        border-left: 4px solid #10b981;
        border-radius: 0 10px 10px 0;
        padding: 12px 16px;
        margin-bottom: 10px;
    }
    .remedy-box-home {
        background: rgba(56, 189, 248, 0.08);
        border-left: 4px solid #38bdf8;
        border-radius: 0 10px 10px 0;
        padding: 12px 16px;
        margin-bottom: 10px;
    }
    .remedy-box-diet {
        background: rgba(245, 158, 11, 0.08);
        border-left: 4px solid #f59e0b;
        border-radius: 0 10px 10px 0;
        padding: 12px 16px;
        margin-bottom: 10px;
    }
    .doctor-warning-card {
        background: rgba(239, 68, 68, 0.1);
        border: 1px solid rgba(239, 68, 68, 0.4);
        border-radius: 12px;
        padding: 14px 18px;
        margin-top: 14px;
    }
    </style>
    """, unsafe_allow_html=True)

    # 1. Header Banner
    st.markdown("""
    <div style="margin-bottom: 16px;">
        <div class="wellness-header-badge">
            🏛️ AYUSH Ministry • 🏥 NHP India • 🔬 ICMR Guidelines • 🌐 WHO Traditional Medicine
        </div>
        <h2 style="color: #f8fafc; margin: 0 0 6px 0;">🌿 Wellness Hub / प्राकृतिक स्वास्थ्य केंद्र</h2>
        <p style="color: #94a3b8; font-size: 0.95rem; margin: 0;">
            Authentic, evidence-based Ayurvedic remedies, safe home therapies, dietary nutrition, and clinical red-flag precautions across 10 categories.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 2. Voice Input Component for Wellness
    st.markdown("<p style='color:#cbd5e1; font-weight:600; font-size:0.9rem; margin-bottom:4px;'>🎙️ Voice Search / बोलकर खोजें:</p>", unsafe_allow_html=True)
    render_voice_input_widget(
        module_key="wellness",
        target_state_key="wellness_search_query",
        trigger_state_key="_trigger_wellness_search",
        help_text="Speak your wellness query in Hindi or English (e.g., 'बाल झड़ने का घरेलू नुस्खा' or 'Acne home remedies')",
        patient_id=patient_id,
        patient_db=patient_db
    )

    # Initialize session state keys
    if "wellness_search_query" not in st.session_state:
        st.session_state.wellness_search_query = ""
    if "selected_category_id" not in st.session_state:
        st.session_state.selected_category_id = "hair"
    if "selected_topic_id" not in st.session_state:
        st.session_state.selected_topic_id = "hair_fall"

    # 3. Search Bar
    col_input, col_btn, col_clear = st.columns([5, 1.5, 1])
    if "wellness_search_input" not in st.session_state:
        st.session_state.wellness_search_input = st.session_state.get("wellness_search_query", "")

    with col_input:
        user_query = st.text_input(
            "Search Wellness Topics:",
            placeholder="Search symptoms or remedies (e.g., dandruff, acidity, constipation, sleep, hair fall, stress...)",
            key="wellness_search_input",
            label_visibility="collapsed"
        )
        st.session_state.wellness_search_query = user_query

    def _reset_wellness():
        st.session_state.wellness_search_input = ""
        st.session_state.wellness_search_query = ""

    def _set_wellness_example(ex_val):
        st.session_state.wellness_search_input = ex_val
        st.session_state.wellness_search_query = ex_val

    with col_btn:
        search_clicked = st.button("🔍 Search", key="btn_wellness_search", use_container_width=True, type="primary")

    with col_clear:
        st.button("✕ Reset", key="btn_wellness_clear", on_click=_reset_wellness, use_container_width=True)

    # Quick Remedy Examples
    st.markdown("<p style='color:#64748b; font-size:0.85rem; margin-top:4px;'>Quick remedy examples:</p>", unsafe_allow_html=True)
    w_cols = st.columns(5)
    for idx, ex in enumerate(["Dandruff", "Acne", "Constipation", "Insomnia", "Stress"]):
        with w_cols[idx]:
            st.button(ex, key=f"well_ex_{idx}", on_click=_set_wellness_example, args=(ex,), use_container_width=True)

    # Determine Active Search Query
    active_query = (user_query or st.session_state.get("wellness_search_query", "")).strip()
    is_search_active = bool(active_query)

    st.markdown("<hr style='border-color: rgba(255,255,255,0.08); margin: 12px 0 16px 0;'>", unsafe_allow_html=True)

    # 4. If Search is Active -> Show Filtered Results
    if is_search_active:
        results = search_wellness_topics(active_query, language=st.session_state.get("language", "en"))
        st.markdown(f"<p style='color:#38bdf8; font-weight:600;'>🔎 Found {len(results)} remedy results matching: <i>'{active_query}'</i></p>", unsafe_allow_html=True)

        if not results:
            st.info(f"No specific wellness topics found for '{active_query}'. Try searching for keywords like 'hair', 'acne', 'gas', 'sleep', 'weight', or 'stress'.")
            available_topics = get_topics_by_category(st.session_state.selected_category_id)
        else:
            available_topics = results
            # Select topic from search results
            topic_labels = [f"{t.get('title_en')} ({t.get('title_hi')}) — {t.get('category_name')}" for t in available_topics]
            selected_idx = st.selectbox(
                "Select a remedy from search results:",
                range(len(available_topics)),
                format_func=lambda i: topic_labels[i],
                key="search_result_select"
            )
            selected_topic = available_topics[selected_idx]
            st.session_state.selected_topic_id = selected_topic["id"]
            st.session_state.selected_category_id = selected_topic["category_id"]

    # 5. If No Search Active -> Show Category Pills & Topic Selector
    else:
        # Category Selector Pills
        st.markdown("<p style='color:#cbd5e1; font-weight:600; font-size:0.9rem; margin-bottom:8px;'>🏷️ Select Health Category / श्रेणी चुनें:</p>", unsafe_allow_html=True)

        category_list = get_all_categories()
        cat_cols = st.columns(5)
        for idx, cat in enumerate(category_list):
            col_target = cat_cols[idx % 5]
            is_active = (st.session_state.selected_category_id == cat["id"])
            btn_label = f"{cat['icon']} {cat['name_en'].split()[1]}"
            if col_target.button(
                btn_label,
                key=f"cat_pill_{cat['id']}",
                use_container_width=True,
                type="primary" if is_active else "secondary"
            ):
                st.session_state.selected_category_id = cat["id"]
                # pick first topic of that category
                cat_topics = get_topics_by_category(cat["id"])
                if cat_topics:
                    st.session_state.selected_topic_id = cat_topics[0]["id"]
                st.rerun()

        current_cat_id = st.session_state.selected_category_id
        available_topics = get_topics_by_category(current_cat_id)

        # Topic Selector dropdown within category
        st.markdown("<div style='margin-top:14px;'></div>", unsafe_allow_html=True)
        col_t1, col_t2 = st.columns([3, 1])
        with col_t1:
            topic_options = [t["id"] for t in available_topics]
            topic_label_map = {t["id"]: f"{t['title_en']} • {t['title_hi']}" for t in available_topics}

            # Find index of current selected topic
            default_index = 0
            if st.session_state.selected_topic_id in topic_options:
                default_index = topic_options.index(st.session_state.selected_topic_id)

            chosen_topic_id = st.selectbox(
                f"Choose Health Concern ({len(available_topics)} verified topics in this category):",
                topic_options,
                index=default_index,
                format_func=lambda x: topic_label_map.get(x, x),
                key="topic_dropdown_select"
            )
            st.session_state.selected_topic_id = chosen_topic_id
            selected_topic = get_topic_by_id(chosen_topic_id)

        with col_t2:
            st.markdown(f"""
            <div style="background: rgba(30, 41, 59, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 10px; padding: 10px; text-align: center; margin-top: 24px;">
                <span style="color: #94a3b8; font-size: 0.8rem;">Category Topics:</span><br>
                <b style="color: #38bdf8; font-size: 1.1rem;">{len(available_topics)}</b>
            </div>
            """, unsafe_allow_html=True)

    if not selected_topic:
        st.warning("Please select a topic to view remedies.")
        return

    # ═══════════════════════════════════════════════════════════════════════════
    # 6. SELECTED TOPIC CLINICAL DOSSIER
    # ═══════════════════════════════════════════════════════════════════════════
    st.markdown("<hr style='border-color: rgba(255,255,255,0.08); margin: 18px 0;'>", unsafe_allow_html=True)

    # Patient Allergies Check
    patient_allergies = []
    if patient_id and patient_db:
        try:
            patient_allergies = patient_db.get_allergies(patient_id)
        except Exception as e:
            print(f"[Wellness] Error reading patient allergies: {e}")

    patient_allergy_names = []
    for a in patient_allergies:
        if isinstance(a, dict):
            name = a.get("medicine_name") or a.get("allergen") or a.get("name")
            if name:
                patient_allergy_names.append(str(name).strip())
        elif isinstance(a, str) and a.strip():
            patient_allergy_names.append(a.strip())

    matched_allergies = check_allergy_warnings(selected_topic, patient_allergy_names)

    # Title & Metadata Card
    st.markdown(f"""
    <div class="wellness-card" style="border-top: 3px solid #10b981;">
        <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:10px;">
            <div>
                <span style="background: rgba(56, 189, 248, 0.15); color: #38bdf8; padding: 3px 10px; border-radius: 6px; font-size: 0.82rem; font-weight: 600;">
                    {selected_topic.get('category_name')}
                </span>
                <h3 style="color:#f8fafc; margin: 8px 0 4px 0; font-size: 1.5rem;">
                    {selected_topic.get('title_en')}
                </h3>
                <h4 style="color:#38bdf8; margin: 0 0 10px 0; font-size: 1.15rem; font-weight: 500;">
                    {selected_topic.get('title_hi')}
                </h4>
            </div>
            <div style="text-align:right;">
                <span style="color: #94a3b8; font-size: 0.78rem;">Verified Sources:</span><br>
                <span style="color: #cbd5e1; font-size: 0.82rem; font-weight: 600;">{selected_topic.get('sources')}</span>
            </div>
        </div>
        <p style="color: #cbd5e1; font-size: 0.95rem; line-height: 1.5; margin: 8px 0 4px 0;">
            {selected_topic.get('overview_en')}
        </p>
        <p style="color: #94a3b8; font-size: 0.9rem; line-height: 1.5; margin: 0;">
            {selected_topic.get('overview_hi')}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════════════════════
    # ALLERGY SAFETY WARNING BANNER
    # ═══════════════════════════════════════════════════════════════════════════
    if matched_allergies:
        allergens_str = ", ".join([a.title() for a in matched_allergies])
        st.markdown(f"""
        <div style="background: rgba(239, 68, 68, 0.15); border: 2px solid #ef4444; border-radius: 12px; padding: 14px 18px; margin-bottom: 18px;">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                <span style="font-size: 1.3rem;">🚨</span>
                <h4 style="color: #f87171; margin: 0; font-size: 1.05rem;">
                    ACTIVE ALLERGY ALERT / एलर्जी सुरक्षा चेतावनी: {allergens_str}
                </h4>
            </div>
            <p style="color: #fca5a5; margin: 0; font-size: 0.9rem; line-height: 1.45;">
                <b>Important:</b> Remedies below suggest ingredients including <b>{allergens_str}</b>. 
                Your medical profile records an allergy to these substances. 
                <b>DO NOT consume or apply</b> any preparation containing these allergens. Choose alternate safe remedies or consult your physician.
            </p>
        </div>
        """, unsafe_allow_html=True)
    elif patient_allergy_names:
        safe_allergies_str = ", ".join([a.title() for a in patient_allergy_names])
        st.markdown(f"""
        <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 10px; padding: 8px 14px; margin-bottom: 16px;">
            <span style="color: #34d399; font-weight: 600; font-size: 0.85rem;">
                🛡️ Allergy Guard: Cross-checked against your recorded allergies ({safe_allergies_str}). No conflict detected.
            </span>
        </div>
        """, unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════════════════════
    # VOICE OUTPUT (TTS / READ ALOUD)
    # ═══════════════════════════════════════════════════════════════════════════
    # Universal Dual-Layer Read Aloud (Browser Web Speech + Persistent MP3)
    speech_hi = (
        f"{selected_topic['title_hi']} के लिए प्रमुख उपाय। "
        f"आयुर्वेदिक उपाय: {'. '.join(selected_topic.get('ayurvedic_remedies_hi', [])[:2])}। "
        f"घरेलू नुस्खे: {'. '.join(selected_topic.get('home_remedies_hi', [])[:2])}। "
        f"सावधानी: {selected_topic.get('when_to_see_doctor_hi', '')}"
    )
    speech_en = (
        f"Remedies for {selected_topic['title_en']}. "
        f"Ayurvedic care: {'. '.join(selected_topic.get('ayurvedic_remedies_en', [])[:2])}. "
        f"Home remedies: {'. '.join(selected_topic.get('home_remedies_en', [])[:2])}. "
        f"Safety note: {selected_topic.get('when_to_see_doctor_en', '')}"
    )

    is_curr_hindi = st.session_state.get("language", "en") == "hi"
    curr_speech = speech_hi if is_curr_hindi else speech_en
    curr_label = "🔊 Read Aloud Remedies / नुस्खे बोलकर सुनें" if is_curr_hindi else "🔊 Read Aloud Remedies (Audio)"
    render_read_aloud_widget(
        text_to_read=curr_speech,
        widget_key=f"wellness_tts_{selected_topic['id']}",
        label=curr_label,
        forced_lang="hi" if is_curr_hindi else "en"
    )

    # ═══════════════════════════════════════════════════════════════════════════
    # CLINICAL REMEDY TABS
    # ═══════════════════════════════════════════════════════════════════════════
    st.markdown("<div style='margin-top:14px;'></div>", unsafe_allow_html=True)
    tab_ayush, tab_home, tab_diet, tab_causes, tab_dos, tab_doctor = st.tabs([
        "🌿 Ayurvedic Care (AYUSH)",
        "🏡 Home Remedies (घरेलू नुस्खे)",
        "🥗 Diet & Nutrition (ICMR)",
        "📋 Causes & Triggers",
        "⚖️ Do's & Don'ts",
        "🚨 When to See Doctor"
    ])

    # 1. Ayurvedic Remedies Tab
    with tab_ayush:
        st.markdown("""
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
            <h4 style="color:#10b981; margin:0;">🌿 Verified Ayurvedic Therapies (आयुर्वेदिक उपचार)</h4>
            <span style="color:#6ee7b7; font-size:0.8rem; background:rgba(16,185,129,0.15); padding:2px 8px; border-radius:4px;">
                Ministry of AYUSH Protocols
            </span>
        </div>
        """, unsafe_allow_html=True)

        remedies_en = selected_topic.get("ayurvedic_remedies_en", [])
        remedies_hi = selected_topic.get("ayurvedic_remedies_hi", [])

        for idx in range(max(len(remedies_en), len(remedies_hi))):
            r_en = remedies_en[idx] if idx < len(remedies_en) else ""
            r_hi = remedies_hi[idx] if idx < len(remedies_hi) else ""
            st.markdown(f"""
            <div class="remedy-box-ayush">
                <div style="font-weight:600; color:#f8fafc; font-size:0.95rem; margin-bottom:3px;">
                    {idx + 1}. {r_en}
                </div>
                <div style="color:#94a3b8; font-size:0.88rem;">
                    👉 {r_hi}
                </div>
            </div>
            """, unsafe_allow_html=True)

    # 2. Home Remedies Tab
    with tab_home:
        st.markdown("""
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
            <h4 style="color:#38bdf8; margin:0;">🏡 Safe Kitchen & Home Remedies (घरेलू नुस्खे)</h4>
            <span style="color:#7dd3fc; font-size:0.8rem; background:rgba(56,189,248,0.15); padding:2px 8px; border-radius:4px;">
                National Health Portal (NHP India)
            </span>
        </div>
        """, unsafe_allow_html=True)

        home_en = selected_topic.get("home_remedies_en", [])
        home_hi = selected_topic.get("home_remedies_hi", [])

        for idx in range(max(len(home_en), len(home_hi))):
            h_en = home_en[idx] if idx < len(home_en) else ""
            h_hi = home_hi[idx] if idx < len(home_hi) else ""
            st.markdown(f"""
            <div class="remedy-box-home">
                <div style="font-weight:600; color:#f8fafc; font-size:0.95rem; margin-bottom:3px;">
                    {idx + 1}. {h_en}
                </div>
                <div style="color:#94a3b8; font-size:0.88rem;">
                    👉 {h_hi}
                </div>
            </div>
            """, unsafe_allow_html=True)

    # 3. Diet & Nutrition Tab
    with tab_diet:
        st.markdown("""
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
            <h4 style="color:#f59e0b; margin:0;">🥗 Dietary & Nutritional Guidance (आहार और पोषण)</h4>
            <span style="color:#fcd34d; font-size:0.8rem; background:rgba(245,158,11,0.15); padding:2px 8px; border-radius:4px;">
                ICMR Dietary Norms
            </span>
        </div>
        """, unsafe_allow_html=True)

        diet_en = selected_topic.get("diet_nutrition_en", [])
        diet_hi = selected_topic.get("diet_nutrition_hi", [])

        for idx in range(max(len(diet_en), len(diet_hi))):
            d_en = diet_en[idx] if idx < len(diet_en) else ""
            d_hi = diet_hi[idx] if idx < len(diet_hi) else ""
            st.markdown(f"""
            <div class="remedy-box-diet">
                <div style="font-weight:600; color:#f8fafc; font-size:0.95rem; margin-bottom:3px;">
                    • {d_en}
                </div>
                <div style="color:#94a3b8; font-size:0.88rem;">
                    👉 {d_hi}
                </div>
            </div>
            """, unsafe_allow_html=True)

    # 4. Causes Tab
    with tab_causes:
        st.markdown("<h4 style='color:#cbd5e1;'>📋 Underlying Causes & Physiological Triggers</h4>", unsafe_allow_html=True)
        causes_en = selected_topic.get("causes_en", [])
        causes_hi = selected_topic.get("causes_hi", [])

        col_c1, col_c2 = st.columns(2)
        with col_c1:
            st.markdown("<p style='color:#38bdf8; font-weight:600; font-size:0.9rem;'>English Causes:</p>", unsafe_allow_html=True)
            for c in causes_en:
                st.markdown(f"<p style='color:#cbd5e1; font-size:0.88rem; margin:4px 0;'>• {c}</p>", unsafe_allow_html=True)

        with col_c2:
            st.markdown("<p style='color:#38bdf8; font-weight:600; font-size:0.9rem;'>मुख्य कारण (हिन्दी):</p>", unsafe_allow_html=True)
            for c in causes_hi:
                st.markdown(f"<p style='color:#94a3b8; font-size:0.88rem; margin:4px 0;'>• {c}</p>", unsafe_allow_html=True)

    # 5. Do's & Don'ts Tab
    with tab_dos:
        st.markdown("<h4 style='color:#cbd5e1;'>⚖️ Daily Lifestyle Habits (क्या करें और क्या न करें)</h4>", unsafe_allow_html=True)
        dos_donts_en = selected_topic.get("dos_and_donts_en", {})
        dos_donts_hi = selected_topic.get("dos_and_donts_hi", {})

        col_d1, col_d2 = st.columns(2)
        with col_d1:
            st.markdown("<div style='background:rgba(16,185,129,0.1); border:1px solid rgba(16,185,129,0.3); border-radius:10px; padding:12px;'>", unsafe_allow_html=True)
            st.markdown("<h5 style='color:#34d399; margin:0 0 8px 0;'>✅ Recommended (क्या करें)</h5>", unsafe_allow_html=True)
            for do_item in dos_donts_en.get("dos", []):
                st.markdown(f"<p style='color:#e2e8f0; font-size:0.85rem; margin:4px 0;'>✓ {do_item}</p>", unsafe_allow_html=True)
            for do_item in dos_donts_hi.get("dos", []):
                st.markdown(f"<p style='color:#94a3b8; font-size:0.82rem; margin:2px 0 6px 12px;'>👉 {do_item}</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col_d2:
            st.markdown("<div style='background:rgba(239,68,68,0.1); border:1px solid rgba(239,68,68,0.3); border-radius:10px; padding:12px;'>", unsafe_allow_html=True)
            st.markdown("<h5 style='color:#f87171; margin:0 0 8px 0;'>❌ Avoid / Don'ts (क्या न करें)</h5>", unsafe_allow_html=True)
            for dont_item in dos_donts_en.get("donts", []):
                st.markdown(f"<p style='color:#e2e8f0; font-size:0.85rem; margin:4px 0;'>✗ {dont_item}</p>", unsafe_allow_html=True)
            for dont_item in dos_donts_hi.get("donts", []):
                st.markdown(f"<p style='color:#94a3b8; font-size:0.82rem; margin:2px 0 6px 12px;'>👉 {dont_item}</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    # 6. When to See a Doctor (Red Flags) Tab
    with tab_doctor:
        doc_en = selected_topic.get("when_to_see_doctor_en", "")
        doc_hi = selected_topic.get("when_to_see_doctor_hi", "")
        st.markdown(f"""
        <div class="doctor-warning-card">
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:8px;">
                <span style="font-size:1.4rem;">🚨</span>
                <h4 style="color:#f87171; margin:0; font-size:1.1rem;">
                    Clinical Red Flags / डॉक्टर से तुरंत परामर्श के संकेत
                </h4>
            </div>
            <p style="color:#cbd5e1; font-size:0.92rem; line-height:1.5; margin-bottom:8px;">
                <b>Medical Threshold:</b> {doc_en}
            </p>
            <p style="color:#fca5a5; font-size:0.88rem; line-height:1.5; margin:0;">
                <b>सावधानी (हिन्दी):</b> {doc_hi}
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Footer Attribution
    st.markdown("""
    <div style="margin-top:24px; text-align:center; color:#64748b; font-size:0.78rem;">
        🌿 <i>Information compiled strictly from Ministry of AYUSH, National Health Portal (NHP India), ICMR, and WHO Traditional Medicine documents. For severe or chronic illness, consult a registered medical doctor.</i>
    </div>
    """, unsafe_allow_html=True)
