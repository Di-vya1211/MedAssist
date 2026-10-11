"""
MedAssist - Visual Design System & Theme Engine
Supports 3 VS Code-style Themes:
- Dark Mode (Midnight Cyber / Deep Obsidian with Cyan Glow)
- Medium Mode (VS Code Slate / Dimmed Charcoal with Soft Cobalt)
- Light Mode (Modern Clinical Pure Light with Crisp Cerulean)

Provides interactive UI components inspired by modern public safety & healthcare networks.
"""

import streamlit as st

THEMES = {
    "dark": {
        "id": "dark",
        "name": "Dark Mode (Cyber Midnight)",
        "icon": "🌙",
        "bg_app": "#070b13",
        "bg_card": "rgba(14, 23, 42, 0.8)",
        "bg_card_hover": "rgba(20, 32, 58, 0.95)",
        "bg_card_active": "rgba(12, 28, 56, 0.9)",
        "border_color": "rgba(56, 189, 248, 0.2)",
        "border_card": "rgba(255, 255, 255, 0.09)",
        "border_active": "#38bdf8",
        "primary_accent": "#38bdf8",
        "primary_gradient": "linear-gradient(135deg, #0284c7 0%, #2563eb 100%)",
        "primary_glow": "0 0 25px rgba(56, 189, 248, 0.35)",
        "text_primary": "#f8fafc",
        "text_secondary": "#94a3b8",
        "text_muted": "#64748b",
        "input_bg": "#0c1322",
        "input_border": "rgba(56, 189, 248, 0.25)",
        "input_text": "#f8fafc",
        "tab_bar_bg": "rgba(15, 23, 42, 0.75)",
        "tab_active_bg": "linear-gradient(135deg, #0284c7 0%, #2563eb 100%)",
        "tab_active_text": "#ffffff",
        "banner_bg": "rgba(11, 19, 38, 0.85)",
        "banner_border": "rgba(56, 189, 248, 0.25)",
        "status_dot_glow": "#10b981",
        "status_pill_bg": "rgba(16, 185, 129, 0.12)",
        "status_pill_border": "rgba(16, 185, 129, 0.3)",
        "status_pill_text": "#34d399",
        "info_card_bg": "rgba(14, 23, 42, 0.75)",
        "warning_card_bg": "rgba(30, 25, 20, 0.8)",
        "warning_border": "#f59e0b",
        "critical_card_bg": "rgba(40, 20, 25, 0.85)",
        "critical_border": "#ef4444",
        "success_card_bg": "rgba(16, 35, 25, 0.75)",
        "success_border": "#10b981",
        "dialog_bg": "#0b1120",
        "shadow_card": "0 8px 30px rgba(0, 0, 0, 0.45)",
    },
    "medium": {
        "id": "medium",
        "name": "Medium Mode (VS Code Slate)",
        "icon": "🌓",
        "bg_app": "#18181b",
        "bg_card": "#242429",
        "bg_card_hover": "#2d2d34",
        "bg_card_active": "#262b3a",
        "border_color": "rgba(255, 255, 255, 0.12)",
        "border_card": "#383842",
        "border_active": "#60a5fa",
        "primary_accent": "#60a5fa",
        "primary_gradient": "linear-gradient(135deg, #2563eb 0%, #4f46e5 100%)",
        "primary_glow": "0 4px 18px rgba(37, 99, 235, 0.3)",
        "text_primary": "#f4f4f5",
        "text_secondary": "#a1a1aa",
        "text_muted": "#71717a",
        "input_bg": "#1e1e24",
        "input_border": "#3f3f46",
        "input_text": "#f4f4f5",
        "tab_bar_bg": "#202026",
        "tab_active_bg": "linear-gradient(135deg, #2563eb 0%, #4f46e5 100%)",
        "tab_active_text": "#ffffff",
        "banner_bg": "#222228",
        "banner_border": "rgba(255, 255, 255, 0.12)",
        "status_dot_glow": "#22c55e",
        "status_pill_bg": "rgba(34, 197, 94, 0.12)",
        "status_pill_border": "rgba(34, 197, 94, 0.3)",
        "status_pill_text": "#4ade80",
        "info_card_bg": "#27272a",
        "warning_card_bg": "rgba(133, 77, 14, 0.2)",
        "warning_border": "#eab308",
        "critical_card_bg": "rgba(153, 27, 27, 0.25)",
        "critical_border": "#f87171",
        "success_card_bg": "rgba(22, 101, 52, 0.25)",
        "success_border": "#22c55e",
        "dialog_bg": "#1e1e24",
        "shadow_card": "0 8px 24px rgba(0, 0, 0, 0.3)",
    },
    "light": {
        "id": "light",
        "name": "Light Mode (Clinical White)",
        "icon": "☀️",
        "bg_app": "#f1f5f9",
        "bg_card": "#ffffff",
        "bg_card_hover": "#f8fafc",
        "bg_card_active": "#f0f9ff",
        "border_color": "#e2e8f0",
        "border_card": "#e2e8f0",
        "border_active": "#0284c7",
        "primary_accent": "#0284c7",
        "primary_gradient": "linear-gradient(135deg, #0284c7 0%, #0369a1 100%)",
        "primary_glow": "0 4px 16px rgba(2, 132, 199, 0.2)",
        "text_primary": "#0f172a",
        "text_secondary": "#475569",
        "text_muted": "#64748b",
        "input_bg": "#ffffff",
        "input_border": "#cbd5e1",
        "input_text": "#0f172a",
        "tab_bar_bg": "#e2e8f0",
        "tab_active_bg": "linear-gradient(135deg, #0284c7 0%, #0369a1 100%)",
        "tab_active_text": "#ffffff",
        "banner_bg": "#ffffff",
        "banner_border": "#e2e8f0",
        "status_dot_glow": "#059669",
        "status_pill_bg": "rgba(16, 185, 129, 0.1)",
        "status_pill_border": "rgba(16, 185, 129, 0.3)",
        "status_pill_text": "#047857",
        "info_card_bg": "#ffffff",
        "warning_card_bg": "#fffbeb",
        "warning_border": "#f59e0b",
        "critical_card_bg": "#fef2f2",
        "critical_border": "#ef4444",
        "success_card_bg": "#ecfdf5",
        "success_border": "#10b981",
        "dialog_bg": "#ffffff",
        "shadow_card": "0 8px 25px rgba(0, 0, 0, 0.08), 0 1px 3px rgba(0, 0, 0, 0.05)",
    }
}


def get_current_theme_id() -> str:
    """Returns currently selected theme id ('dark', 'medium', 'light'). Defaults to 'dark'."""
    if "theme_mode" not in st.session_state:
        st.session_state.theme_mode = "dark"
    return st.session_state.theme_mode


def get_theme_palette() -> dict:
    """Returns the color palette dictionary for current theme."""
    t_id = get_current_theme_id()
    return THEMES.get(t_id, THEMES["dark"])


def apply_theme_css():
    """Injects high-fidelity theme CSS into the active Streamlit app."""
    theme = get_theme_palette()
    is_light = (theme["id"] == "light")
    
    css = f"""
    <style>
    /* Global Root Variables */
    :root {{
        --bg-app: {theme["bg_app"]};
        --bg-card: {theme["bg_card"]};
        --bg-card-hover: {theme["bg_card_hover"]};
        --border-color: {theme["border_color"]};
        --primary-accent: {theme["primary_accent"]};
        --text-primary: {theme["text_primary"]};
        --text-secondary: {theme["text_secondary"]};
        --text-muted: {theme["text_muted"]};
        --shadow-card: {theme["shadow_card"]};
    }}

    /* Main App Canvas */
    .stApp {{
        background-color: {theme["bg_app"]} !important;
        color: {theme["text_primary"]} !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Inter", "Helvetica Neue", Arial, sans-serif;
    }}
    .main .block-container {{
        padding-top: 1.2rem !important;
        padding-bottom: 4rem !important;
    }}

    /* Typography */
    h1, h2, h3, h4, h5, h6 {{
        color: {theme["text_primary"]} !important;
        font-weight: 700 !important;
        letter-spacing: -0.025em !important;
    }}
    p, li, span, label, div.stMarkdown {{
        color: {theme["text_secondary"]} !important;
    }}
    b, strong {{
        color: {theme["text_primary"]} !important;
    }}

    /* Top Initiative Banner Container (RakshaPath inspired) */
    .initiative-banner {{
        background: {theme["banner_bg"]};
        border: 1px solid {theme["banner_border"]};
        border-radius: 18px;
        padding: 14px 24px;
        margin-bottom: 16px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 14px;
        box-shadow: {theme["shadow_card"]};
        backdrop-filter: blur(12px);
    }}
    .initiative-left {{
        display: flex;
        align-items: center;
        gap: 14px;
    }}
    .initiative-badge-icon {{
        width: 44px;
        height: 44px;
        border-radius: 12px;
        background: {theme["status_pill_bg"]};
        border: 1px solid {theme["border_color"]};
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.45rem;
    }}
    .initiative-tag {{
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        color: {theme["primary_accent"]};
        margin: 0;
    }}
    .initiative-title {{
        font-size: 1.25rem;
        font-weight: 800;
        color: {theme["text_primary"]} !important;
        margin: 2px 0 0 0;
        letter-spacing: -0.02em;
    }}

    /* Status Indicator Pills */
    .status-pill {{
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: {theme["status_pill_bg"]};
        border: 1px solid {theme["status_pill_border"]};
        color: {theme["status_pill_text"]} !important;
        padding: 6px 14px;
        border-radius: 30px;
        font-size: 0.82rem;
        font-weight: 600;
        letter-spacing: 0.02em;
    }}
    .status-dot {{
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: {theme["status_dot_glow"]};
        box-shadow: 0 0 10px {theme["status_dot_glow"]};
        animation: pulseStatus 2s infinite ease-in-out;
    }}
    @keyframes pulseStatus {{
        0% {{ transform: scale(0.95); opacity: 0.8; }}
        50% {{ transform: scale(1.2); opacity: 1; }}
        100% {{ transform: scale(0.95); opacity: 0.8; }}
    }}

    /* Center Sub-Badge */
    .center-sub-badge {{
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: {theme["status_pill_bg"]};
        border: 1px solid {theme["border_color"]};
        color: {theme["primary_accent"]} !important;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 600;
        margin-bottom: 10px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.15);
    }}

    /* Hero Heading Box */
    .hero-box {{
        text-align: center;
        margin: 12px 0 24px 0;
    }}
    .hero-title {{
        font-size: 2.8rem !important;
        font-weight: 900 !important;
        letter-spacing: -0.04em !important;
        color: {theme["text_primary"]} !important;
        margin: 0 0 6px 0 !important;
        background: {"linear-gradient(135deg, #0284c7 0%, #0f172a 100%)" if is_light else "linear-gradient(180deg, #ffffff 0%, #94a3b8 100%)"};
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}
    .hero-subtitle {{
        font-size: 1.25rem !important;
        font-weight: 700 !important;
        color: {theme["primary_accent"]} !important;
        margin: 0 0 8px 0 !important;
    }}
    .hero-desc {{
        max-width: 820px;
        margin: 0 auto !important;
        font-size: 0.95rem !important;
        color: {theme["text_secondary"]} !important;
        line-height: 1.55 !important;
    }}
    .section-label {{
        text-align: center;
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.18em;
        color: {theme["primary_accent"]};
        margin: 22px 0 14px 0;
    }}

    /* Modern Interactive Cards Grid (RakshaPath inspired) */
    .interactive-card {{
        background: {theme["bg_card"]};
        border: 1px solid {theme["border_card"]};
        border-radius: 18px;
        padding: 22px;
        transition: all 0.28s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: {theme["shadow_card"]};
        backdrop-filter: blur(8px);
        position: relative;
        min-height: 290px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }}
    .interactive-card:hover {{
        border-color: {theme["border_active"]};
        transform: translateY(-4px);
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.35), {theme["primary_glow"]};
    }}
    .interactive-card.active {{
        border: 2px solid {theme["border_active"]};
        background: {theme["bg_card_active"]};
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.35), {theme["primary_glow"]};
    }}
    .card-top {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
    }}
    .card-icon-badge {{
        width: 42px;
        height: 42px;
        border-radius: 12px;
        background: {theme["status_pill_bg"]};
        border: 1px solid {theme["border_color"]};
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.35rem;
    }}
    .card-check-badge {{
        width: 22px;
        height: 22px;
        border-radius: 50%;
        background: {theme["primary_accent"]};
        color: #ffffff;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.75rem;
        font-weight: 900;
    }}
    .card-radio-empty {{
        width: 20px;
        height: 20px;
        border-radius: 50%;
        border: 2px solid {theme["text_muted"]};
    }}
    .card-title {{
        font-size: 1.25rem;
        font-weight: 800;
        color: {theme["text_primary"]} !important;
        margin: 0 0 4px 0;
    }}
    .card-subtitle {{
        font-size: 0.88rem;
        font-weight: 600;
        color: {theme["primary_accent"]} !important;
        margin: 0 0 10px 0;
    }}
    .card-desc {{
        font-size: 0.86rem;
        color: {theme["text_secondary"]} !important;
        line-height: 1.45;
        margin: 0 0 14px 0;
    }}
    .card-bullet-list {{
        list-style: none;
        padding: 0;
        margin: 0 0 16px 0;
    }}
    .card-bullet-item {{
        display: flex;
        align-items: flex-start;
        gap: 8px;
        font-size: 0.83rem;
        color: {theme["text_secondary"]} !important;
        margin-bottom: 6px;
    }}
    .card-bullet-check {{
        color: {theme["primary_accent"]};
        font-weight: 800;
        font-size: 0.9rem;
    }}
    .card-footer {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-top: 14px;
        border-top: 1px solid {theme["border_card"]};
        font-size: 0.82rem;
        font-weight: 600;
    }}
    .card-footer-active {{
        color: {theme["primary_accent"]};
        display: flex;
        align-items: center;
        gap: 6px;
    }}

    /* Standard Alert / Cards */
    .info-card {{
        background: {theme["info_card_bg"]};
        border: 1px solid {theme["border_color"]};
        padding: 18px 22px;
        border-radius: 14px;
        border-left: 4px solid {theme["primary_accent"]};
        margin-bottom: 16px;
        box-shadow: {theme["shadow_card"]};
    }}
    .warning-card {{
        background: {theme["warning_card_bg"]};
        border: 1px solid {theme["warning_border"]}44;
        padding: 16px 20px;
        border-radius: 14px;
        border-left: 4px solid {theme["warning_border"]};
        margin-bottom: 14px;
    }}
    .critical-card {{
        background: {theme["critical_card_bg"]};
        border: 1px solid {theme["critical_border"]}55;
        padding: 18px 22px;
        border-radius: 14px;
        border-left: 5px solid {theme["critical_border"]};
        margin-bottom: 16px;
    }}
    .success-card {{
        background: {theme["success_card_bg"]};
        border: 1px solid {theme["success_border"]}44;
        padding: 16px 20px;
        border-radius: 14px;
        border-left: 4px solid {theme["success_border"]};
        margin-bottom: 14px;
    }}

    /* Stat / Vital Metric Box */
    .stat-box {{
        background: {theme["bg_card"]};
        border: 1px solid {theme["border_color"]};
        border-radius: 14px;
        padding: 16px;
        text-align: center;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }}
    .stat-box:hover {{
        transform: translateY(-2px);
        border-color: {theme["border_active"]};
    }}

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
        background-color: {theme["tab_bar_bg"]} !important;
        padding: 8px 12px;
        border-radius: 16px;
        border: 1px solid {theme["border_color"]};
        box-shadow: {theme["shadow_card"]};
    }}
    .stTabs [data-baseweb="tab"], .stTabs button[role="tab"] {{
        background-color: transparent !important;
        color: {theme["text_secondary"]} !important;
        border-radius: 12px !important;
        padding: 9px 18px !important;
        font-weight: 600 !important;
        font-size: 0.92rem !important;
        transition: all 0.22s ease-in-out;
        border: none !important;
        outline: none !important;
    }}
    .stTabs [data-baseweb="tab"]:hover, .stTabs button[role="tab"]:hover {{
        background-color: {"rgba(0, 0, 0, 0.05)" if is_light else "rgba(255, 255, 255, 0.08)"} !important;
        color: {theme["text_primary"]} !important;
    }}
    .stTabs [aria-selected="true"], .stTabs button[role="tab"][aria-selected="true"] {{
        background: {theme["tab_active_bg"]} !important;
        color: {theme["tab_active_text"]} !important;
        border-radius: 12px !important;
        box-shadow: {theme["primary_glow"]} !important;
        font-weight: 700 !important;
    }}
    .stTabs [data-baseweb="tab-highlight"],
    .stTabs [data-baseweb="tab-border"] {{
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
    }}

    /* Form Controls: Inputs, TextAreas, Selectboxes */
    .stTextInput > div > div > input, 
    .stTextArea > div > div > textarea,
    .stNumberInput > div > div > input {{
        background-color: {theme["input_bg"]} !important;
        color: {theme["input_text"]} !important;
        border: 1px solid {theme["input_border"]} !important;
        border-radius: 11px !important;
        padding: 12px 14px !important;
        font-size: 0.98rem !important;
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }}
    .stTextInput > div > div > input:focus, 
    .stTextArea > div > div > textarea:focus,
    .stNumberInput > div > div > input:focus {{
        border-color: {theme["border_active"]} !important;
        box-shadow: 0 0 0 2px {theme["primary_accent"]}33 !important;
    }}
    .stSelectbox > div > div {{
        background-color: {theme["input_bg"]} !important;
        color: {theme["input_text"]} !important;
        border-radius: 11px !important;
        border: 1px solid {theme["input_border"]} !important;
    }}
    .stSelectbox [data-baseweb="select"] span {{
        color: {theme["input_text"]} !important;
    }}

    /* Modern Buttons */
    .stButton > button {{
        border-radius: 11px !important;
        font-weight: 600 !important;
        transition: all 0.22s cubic-bezier(0.4, 0, 0.2, 1) !important;
        padding: 9px 20px !important;
        background: {theme["bg_card"]} !important;
        color: {theme["text_primary"]} !important;
        border: 1px solid {theme["border_color"]} !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15) !important;
    }}
    .stButton > button:hover {{
        background: {theme["bg_card_hover"]} !important;
        color: {theme["primary_accent"]} !important;
        border-color: {theme["border_active"]} !important;
        box-shadow: {theme["primary_glow"]} !important;
        transform: translateY(-1px) !important;
    }}
    .stButton > button p, 
    .stButton > button span, 
    .stButton > button div {{
        color: inherit !important;
        font-weight: 600 !important;
    }}

    /* Primary Accent Button */
    .stButton > button[kind="primary"],
    .stButton > button[data-testid="stBaseButton-primary"] {{
        background: {theme["primary_gradient"]} !important;
        color: #ffffff !important;
        border: 1px solid {theme["border_active"]} !important;
        box-shadow: {theme["primary_glow"]} !important;
    }}
    .stButton > button[kind="primary"]:hover,
    .stButton > button[data-testid="stBaseButton-primary"]:hover {{
        filter: brightness(1.1) !important;
        transform: translateY(-2px) !important;
    }}
    .stButton > button[kind="primary"] p,
    .stButton > button[kind="primary"] span,
    .stButton > button[kind="primary"] div,
    .stButton > button[data-testid="stBaseButton-primary"] p,
    .stButton > button[data-testid="stBaseButton-primary"] span,
    .stButton > button[data-testid="stBaseButton-primary"] div {{
        color: #ffffff !important;
    }}

    /* Expanders */
    .streamlit-expanderHeader {{
        background-color: {theme["bg_card"]} !important;
        border-radius: 12px !important;
        color: {theme["text_primary"]} !important;
        font-weight: 600 !important;
        border: 1px solid {theme["border_color"]} !important;
    }}

    /* ========================================================
       FLOATING AI BOT DIALOG AS SIDE SQUARE CARD (BOTTOM-RIGHT)
       ======================================================== */
    div[data-baseweb="modal"],
    div[data-baseweb="modal"] > div,
    div[data-testid="stDialog"],
    div.stDialog,
    .e1mymz5c0 {{
        position: fixed !important;
        inset: 0 !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        bottom: 0 !important;
        width: 100vw !important;
        height: 100vh !important;
        background: transparent !important;
        background-color: transparent !important;
        display: flex !important;
        align-items: flex-end !important;
        justify-content: flex-end !important;
        padding: 0 !important;
        margin: 0 !important;
        z-index: 99999999 !important;
    }}

    div[data-testid="stDialog"] > div,
    div.stDialog > div,
    div[role="dialog"],
    .e1mymz5c1 {{
        position: fixed !important;
        bottom: 105px !important;
        right: 25px !important;
        inset: auto !important;
        top: auto !important;
        left: auto !important;
        margin: 0 !important;
        width: 410px !important;
        max-width: calc(100vw - 35px) !important;
        height: 550px !important;
        max-height: calc(100vh - 125px) !important;
        background: {theme["dialog_bg"]} !important;
        background-color: {theme["dialog_bg"]} !important;
        border: 2px solid {theme["border_active"]} !important;
        border-radius: 20px !important;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.9), {theme["primary_glow"]} !important;
        overflow-y: auto !important;
        padding: 1.15rem 1.3rem !important;
        display: flex !important;
        flex-direction: column !important;
        pointer-events: auto !important;
        transform-origin: bottom right !important;
        animation: botPopupFromBot 0.35s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
    }}

    @keyframes botPopupFromBot {{
        0% {{
            opacity: 0;
            transform: scale(0.12) translateY(80px) translateX(40px);
        }}
        70% {{
            opacity: 1;
            transform: scale(1.03) translateY(-4px) translateX(-2px);
        }}
        100% {{
            opacity: 1;
            transform: scale(1) translateY(0) translateX(0);
        }}
    }}

    body:has(div[data-testid="stDialog"]) .bot-speech-bubble,
    body:has(div.stDialog) .bot-speech-bubble,
    body:has(div[role="dialog"]) .bot-speech-bubble {{
        display: none !important;
    }}

    div[data-testid="stDialog"] h2,
    div.stDialog h2,
    div[role="dialog"] h2 {{
        font-size: 1.05rem !important;
        margin: 0 !important;
        padding: 0 !important;
        color: {theme["text_primary"]} !important;
        font-weight: 700 !important;
    }}

    div[data-testid="stDialog"] button[aria-label="Close"],
    div.stDialog button[aria-label="Close"],
    div[role="dialog"] button[aria-label="Close"],
    .e1mymz5c3 {{
        color: {theme["text_muted"]} !important;
        top: 14px !important;
        right: 14px !important;
        font-size: 1.2rem !important;
        border-radius: 8px !important;
        transition: all 0.2s ease !important;
    }}
    div[data-testid="stDialog"] button[aria-label="Close"]:hover,
    div.stDialog button[aria-label="Close"]:hover,
    div[role="dialog"] button[aria-label="Close"]:hover,
    .e1mymz5c3:hover {{
        color: #f43f5e !important;
        background: rgba(244, 63, 94, 0.15) !important;
        transform: scale(1.1) !important;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def render_theme_switcher():
    """
    Renders 3-mode theme switcher pills (Dark | Medium | Light).
    Just like VS Code themes.
    """
    current = get_current_theme_id()
    
    col_t1, col_t2, col_t3 = st.columns(3)
    with col_t1:
        if st.button("🌙 Dark", use_container_width=True, type="primary" if current == "dark" else "secondary", key="theme_btn_dark"):
            st.session_state.theme_mode = "dark"
            st.rerun()
    with col_t2:
        if st.button("🌓 Medium", use_container_width=True, type="primary" if current == "medium" else "secondary", key="theme_btn_medium"):
            st.session_state.theme_mode = "medium"
            st.rerun()
    with col_t3:
        if st.button("☀️ Light", use_container_width=True, type="primary" if current == "light" else "secondary", key="theme_btn_light"):
            st.session_state.theme_mode = "light"
            st.rerun()


def render_initiative_header():
    """
    Renders the top national initiative banner and status badges inspired by the RakshaPath reference design.
    """
    theme = get_theme_palette()
    
    st.markdown(f"""
    <div class="initiative-banner">
        <div class="initiative-left">
            <div class="initiative-badge-icon">
                🏥
            </div>
            <div>
                <p class="initiative-tag">CENTRAL DIGITAL HEALTH MISSION</p>
                <h3 class="initiative-title">MedAssist Clinical Network</h3>
            </div>
        </div>
        <div style="display: flex; align-items: center; gap: 10px; flex-wrap: wrap;">
            <div class="status-pill">
                <span class="status-dot"></span>
                <span>AI Clinical Grid Active</span>
            </div>
            <div class="status-pill" style="border-color: {theme['border_active']}; color: {theme['primary_accent']} !important;">
                <span>🛡️ 24/7 Allergy Guard Live</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_hero_section():
    """
    Renders the modern hero section with title, subtitle, and platform badge.
    """
    st.markdown("""
    <div class="hero-box">
        <div class="center-sub-badge">
            <span>🛡️ Rural Health Companion & Adverse Allergy Protection Platform</span>
        </div>
        <h1 class="hero-title">MedAssist</h1>
        <h3 class="hero-subtitle">National Clinical & Emergency Health Network</h3>
        <p class="hero-desc">
            AI-powered clinical triage, FDA drug safety & allergy interaction safeguards, automated diagnostic lab test analysis, and verified AYUSH traditional wellness.
        </p>
        <p class="section-label">SELECT YOUR CLINICAL MODULE TO ENTER</p>
    </div>
    """, unsafe_allow_html=True)


def render_interactive_overview_cards():
    """
    Renders the dual interactive cards directly matching the RakshaPath reference UI.
    """
    theme = get_theme_palette()
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown(f"""
        <div class="interactive-card active">
            <div>
                <div class="card-top">
                    <div class="card-icon-badge">🛡️</div>
                    <div class="card-check-badge">✓</div>
                </div>
                <h3 class="card-title">Citizen & Patient Triage</h3>
                <p class="card-subtitle">Public Health Diagnostic & Allergy Protection</p>
                <p class="card-desc">
                    Differential disease diagnosis, 100+ diagnostic lab test details, personalized medication safety, and verified Indian home remedies.
                </p>
                <ul class="card-bullet-list">
                    <li class="card-bullet-item"><span class="card-bullet-check">✓</span> Real-time active allergy blocking for penicillin & NSAIDs</li>
                    <li class="card-bullet-item"><span class="card-bullet-check">✓</span> 100+ diagnostic lab procedures, normal ranges & fasting rules</li>
                    <li class="card-bullet-item"><span class="card-bullet-check">✓</span> One-click voice assistance in 12+ Indian languages</li>
                </ul>
            </div>
            <div class="card-footer">
                <span class="card-footer-active">● Active Selection</span>
                <span style="color: {theme['primary_accent']};">Standard Access</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="interactive-card">
            <div>
                <div class="card-top">
                    <div class="card-icon-badge">🔬</div>
                    <div class="card-radio-empty"></div>
                </div>
                <h3 class="card-title">Clinical Diagnostics & Pharmacy</h3>
                <p class="card-subtitle" style="color: #f59e0b !important;">FDA Safety, Lab OCR & Emergency Logistics</p>
                <p class="card-desc">
                    Comprehensive blood lab report analysis (CBC, Lipid, Renal), FDA drug interaction monographs, and National Emergency 108 triage.
                </p>
                <ul class="card-bullet-list">
                    <li class="card-bullet-item"><span class="card-bullet-check" style="color: #f59e0b;">✓</span> Automated medical test values and abnormal alert ranges</li>
                    <li class="card-bullet-item"><span class="card-bullet-check" style="color: #f59e0b;">✓</span> Comprehensive drug dosage and therapeutic toxicity warnings</li>
                    <li class="card-bullet-item"><span class="card-bullet-check" style="color: #f59e0b;">✓</span> One-click 108 ambulance dispatch and ICE emergency contacts</li>
                </ul>
            </div>
            <div class="card-footer">
                <span style="color: {theme['text_muted']};">Module Available</span>
                <span style="color: #f59e0b;">Clinical Console</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
