from pathlib import Path
import base64

import streamlit as st

APP_DIR = Path(__file__).resolve().parent
ASSETS_DIR = APP_DIR / "assets"
BACKGROUND_IMAGE = ASSETS_DIR / "paddy_background.jpg"
PLANNER_IMAGE = ASSETS_DIR / "planner_rice.jpg"
LOGO_IMAGE = ASSETS_DIR / "logo.png"


def _image_data_uri(path: Path):
    if not path.exists():
        return None
    mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def setup_theme():
    bg_uri = _image_data_uri(BACKGROUND_IMAGE)
    if bg_uri:
        background_rule = (
            f"background-image: linear-gradient(rgba(9, 42, 27, .54), rgba(9, 42, 27, .62)), url('{bg_uri}');"
        )
    else:
        background_rule = "background: #edf4ef;"

    st.markdown(
        f"""
        <style>
        .stApp {{
            {background_rule}
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        header[data-testid="stHeader"] {{ background: transparent !important; }}
        .block-container {{ max-width: 1180px; padding-top: 1rem; padding-bottom: 3rem; }}

        section[data-testid="stSidebar"] {{
            background: rgba(19, 54, 37, .97) !important;
            border-right: 1px solid rgba(255,255,255,.10);
        }}
        section[data-testid="stSidebar"] > div {{ background: transparent !important; }}
        section[data-testid="stSidebar"] .sidebar-section-title {{
            color: #d9e9df !important; font-size: 11px; font-weight: 800;
            letter-spacing: 1.3px; margin: 18px 4px 8px;
        }}
        section[data-testid="stSidebar"] .sidebar-divider {{
            height: 1px; background: rgba(255,255,255,.16); margin: 14px 0;
        }}
        section[data-testid="stSidebar"] .stButton > button {{
            background: rgba(255,255,255,.10) !important;
            border: 1px solid rgba(255,255,255,.16) !important;
            box-shadow: none !important;
            color: #ffffff !important;
        }}
        section[data-testid="stSidebar"] .stButton > button:hover {{
            background: rgba(255,255,255,.18) !important;
        }}
        section[data-testid="stSidebar"] .stButton > button p {{ color:#ffffff !important; }}

        /* Sidebar language selector: white field + dark text, never white-on-white. */
        section[data-testid="stSidebar"] div[data-baseweb="select"] > div {{
            background: #ffffff !important;
            border: 1px solid #c9d9cf !important;
            border-radius: 10px !important;
        }}
        section[data-testid="stSidebar"] div[data-baseweb="select"] span,
        section[data-testid="stSidebar"] div[data-baseweb="select"] input {{
            color: #173d2a !important;
            -webkit-text-fill-color: #173d2a !important;
        }}
        section[data-testid="stSidebar"] div[data-baseweb="select"] svg {{ fill: #173d2a !important; }}
        div[data-baseweb="popover"] {{ background: #ffffff !important; }}
        div[data-baseweb="popover"] div[role="option"] {{
            color: #173d2a !important; background: #ffffff !important;
        }}
        div[data-baseweb="popover"] div[role="option"] * {{ color: #173d2a !important; }}
        div[data-baseweb="popover"] div[role="option"]:hover {{ background: #edf5ef !important; }}

        .top-header {{
            display:flex; align-items:center; justify-content:space-between; gap:20px;
            padding: 12px 18px; margin-bottom: 16px;
            background: rgba(255,255,255,.96); border:1px solid #dbe7df;
            border-radius:16px; box-shadow:0 7px 22px rgba(0,0,0,.10);
        }}
        .top-brand {{ font-size:22px; font-weight:850; color:#163e2b; }}
        .top-tagline {{ font-size:12px; color:#5c7065; margin-top:2px; }}

        .hero {{
            padding: 25px 28px; margin-bottom:20px; border-radius:20px;
            background: rgba(20, 73, 48, .88);
            border: 1px solid rgba(255,255,255,.14);
            box-shadow: 0 12px 30px rgba(0,0,0,.14);
        }}
        .hero-icon {{ font-size:30px; margin-bottom:6px; }}
        .hero-title {{ color:#ffffff !important; font-size:32px; font-weight:850; margin:0; }}
        .hero-subtitle {{ color:#edf6f0 !important; font-size:14px; margin-top:6px; }}
        .section-title {{ color:#ffffff !important; font-size:21px; font-weight:800; margin:18px 0 12px; }}

        div[data-testid="stVerticalBlockBorderWrapper"] {{
            background: rgba(255,255,255,.96) !important;
            border:1px solid #dbe7df !important;
            border-radius:17px !important;
            box-shadow:0 8px 24px rgba(0,0,0,.10);
        }}
        div[data-testid="stVerticalBlockBorderWrapper"] h1,
        div[data-testid="stVerticalBlockBorderWrapper"] h2,
        div[data-testid="stVerticalBlockBorderWrapper"] h3,
        div[data-testid="stVerticalBlockBorderWrapper"] h4 {{ color:#173f2b !important; }}
        div[data-testid="stVerticalBlockBorderWrapper"] p,
        div[data-testid="stVerticalBlockBorderWrapper"] label {{ color:#334d40 !important; }}

        .variety-card {{
            background:rgba(255,255,255,.96); border-radius:15px; padding:17px;
            min-height:88px; border:1px solid #dbe7df; box-shadow:0 5px 16px rgba(0,0,0,.08);
        }}
        .variety-card strong {{ display:block; color:#17472f; font-size:16px; }}
        .variety-card span {{ display:block; color:#68796f; font-size:12px; margin-top:5px; }}

        h1,h2,h3,h4 {{ color:#173f2b !important; }}
        .stMarkdown p, .stCaption, label {{ color:#eef6f1 !important; }}
        div[data-testid="stVerticalBlockBorderWrapper"] .stMarkdown p,
        div[data-testid="stVerticalBlockBorderWrapper"] .stCaption,
        div[data-testid="stVerticalBlockBorderWrapper"] label {{ color:#334d40 !important; }}

        [data-testid="stTextInput"] input, [data-testid="stNumberInput"] input {{
            background:#ffffff !important; color:#173d2a !important;
            -webkit-text-fill-color:#173d2a !important;
            border:1px solid #c7d8ce !important; border-radius:10px !important;
        }}
        div[data-baseweb="select"] > div {{
            background:#ffffff !important; color:#173d2a !important;
            border:1px solid #c7d8ce !important; border-radius:10px !important;
        }}
        div[data-baseweb="select"] span {{ color:#173d2a !important; }}

        .stButton > button {{
            background:#17633f !important; color:#ffffff !important;
            border:1px solid #17633f !important; border-radius:10px !important;
            min-height:43px !important; font-weight:800 !important;
            box-shadow:0 4px 12px rgba(23,99,63,.18) !important;
        }}
        .stButton > button:hover {{ background:#125333 !important; border-color:#125333 !important; }}
        .stButton > button p {{ color:#ffffff !important; font-weight:800 !important; }}

        .stRadio label {{ color:#edf6f1 !important; }}
        section[data-testid="stFileUploaderDropzone"] {{
            background:#ffffff !important; border:2px dashed #b8cfc0 !important; border-radius:13px !important;
        }}
        section[data-testid="stFileUploaderDropzone"] * {{ color:#2b4b3a !important; }}

        .selection-summary {{
            background:#f0f6f2; border:1px solid #d7e6dc; color:#315542;
            border-radius:10px; padding:9px 12px; margin:8px 0 14px;
        }}
        .planner-result-title {{
            background:rgba(255,255,255,.96); color:#17472f; border:1px solid #dbe7df;
            border-radius:13px; padding:13px 15px; font-weight:850; margin:10px 0 12px;
        }}
        .fact-row {{
            display:flex; align-items:flex-start; gap:18px;
            background:#ffffff; border:1px solid #dbe7df; border-radius:11px;
            padding:12px 14px; margin:8px 0; box-shadow:0 3px 10px rgba(0,0,0,.06);
        }}
        .fact-label {{ color:#24583e; font-weight:800; min-width:150px; }}
        .fact-value {{ color:#2e4037; text-align:left; flex:1; line-height:1.45; }}
        .planner-note {{
            background:rgba(255,255,255,.95); border:1px solid #dbe7df; border-radius:13px;
            padding:13px; margin:12px 0 16px; color:#315542;
        }}
        .chat-message {{
            background:#ffffff; border:1px solid #dbe7df; border-radius:11px;
            padding:10px 13px; margin:7px 0; color:#294639;
        }}
        .prediction-result-label {{ color:#ffffff !important; font-size:16px; font-weight:800; margin-top:18px; }}
        .prediction-name {{
            background:#ffffff; color:#145a38; font-size:28px; font-weight:900;
            text-align:center; padding:18px; border-radius:15px; margin-top:7px;
            box-shadow:0 8px 24px rgba(0,0,0,.12); border:1px solid #d4e4da;
        }}
        .login-spacer {{ height:7vh; }}
        .login-card-title {{ color:#ffffff !important; text-align:center; font-size:30px; font-weight:900; margin-top:12px; }}
        .login-card-subtitle {{ color:#edf6f1 !important; text-align:center; font-size:14px; margin:5px 0 18px; }}
        .login-hint {{ color:#e8f3ec !important; text-align:center; font-size:12px; margin-top:10px; }}
        .sp-footer {{ text-align:center; color:#e7f2eb; font-size:12px; margin-top:28px; padding:10px; }}

        @media (max-width: 768px) {{
            .block-container {{ padding-left:1rem; padding-right:1rem; }}
            .hero-title {{ font-size:26px; }}
            .fact-row {{ display:block; }}
            .fact-value {{ margin-top:5px; }}
            .top-header {{ display:block; }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def show_brand(sidebar=False):
    if LOGO_IMAGE.exists():
        st.image(str(LOGO_IMAGE), width=100 if sidebar else 115)
    else:
        st.markdown("<div class='top-brand'>Smart Paddy</div>", unsafe_allow_html=True)


def show_top_header():
    st.markdown(
        """
        <div class="top-header">
            <div>
                <div class="top-brand">Smart Paddy</div>
                <div class="top-tagline">Smart Paddy Cultivation &amp; Farmer Support</div>
            </div>
            <div class="top-tagline">4 Paddy Varieties</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_hero(title, subtitle, icon="🌾"):
    st.markdown(
        f"""
        <div class="hero">
            <div class="hero-icon">{icon}</div>
            <div class="hero-title">{title}</div>
            <div class="hero-subtitle">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_card(title, content):
    with st.container(border=True):
        st.subheader(title)
        st.write(content)


def show_footer():
    st.markdown("<div class='sp-footer'>Smart Paddy — Smart Support for Farmers</div>", unsafe_allow_html=True)
