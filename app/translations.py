# app/translations.py

import streamlit as st


# ============================================================
# SUPPORTED LANGUAGES
# ============================================================

LANGUAGES = {
    "English": "en",
    "తెలుగు": "te",
    "हिंदी": "hi",
}

LANGUAGE_NAMES = {
    "en": "English",
    "te": "తెలుగు",
    "hi": "हिंदी",
}


# ============================================================
# ALL TRANSLATIONS
# ============================================================

TRANSLATIONS = {

    # --------------------------------------------------------
    # BRAND
    # --------------------------------------------------------

    "app_name": {
        "en": "Smart Paddy",
        "te": "స్మార్ట్ ప్యాడీ",
        "hi": "स्मार्ट पैडी",
    },

    "tagline": {
        "en": "Smart Paddy Cultivation & Farmer Support",
        "te": "స్మార్ట్ ప్యాడీ సాగు & రైతు సహాయం",
        "hi": "स्मार्ट पैडी खेती और किसान सहायता",
    },

    "language": {
        "en": "Language",
        "te": "భాష",
        "hi": "भाषा",
    },

    # --------------------------------------------------------
    # NAVIGATION
    # --------------------------------------------------------

    "home": {
        "en": "Home",
        "te": "హోమ్",
        "hi": "होम",
    },

    "profile": {
        "en": "Profile",
        "te": "ప్రొఫైల్",
        "hi": "प्रोफ़ाइल",
    },

    "logout": {
        "en": "Logout",
        "te": "లాగ్ అవుట్",
        "hi": "लॉग आउट",
    },

    "back": {
        "en": "Back",
        "te": "వెనక్కి",
        "hi": "वापस",
    },

    # --------------------------------------------------------
    # MAIN TWO PAGES
    # --------------------------------------------------------

    "prediction_analyzer": {
        "en": "Prediction Analyzer",
        "te": "ప్రిడిక్షన్ అనలైజర్",
        "hi": "प्रेडिक्शन एनालाइज़र",
    },

    "prediction_analyzer_desc": {
        "en": "Identify the paddy grain variety using an image.",
        "te": "చిత్రాన్ని ఉపయోగించి వరి ధాన్యం రకాన్ని గుర్తించండి.",
        "hi": "चित्र का उपयोग करके धान की किस्म पहचानें।",
    },

    "cultivation_planner": {
        "en": "Cultivation Planner",
        "te": "సాగు ప్లానర్",
        "hi": "खेती प्लानर",
    },

    "cultivation_planner_desc": {
        "en": "Generate a complete cultivation plan using grain type and land area.",
        "te": "ధాన్యం రకం మరియు భూమి విస్తీర్ణంతో పూర్తి సాగు ప్రణాళికను రూపొందించండి.",
        "hi": "धान की किस्म और भूमि क्षेत्र के आधार पर पूरी खेती योजना बनाएं।",
    },

    # --------------------------------------------------------
    # PREDICTION ANALYZER
    # --------------------------------------------------------

    "choose_prediction_input": {
        "en": "Choose Prediction Input",
        "te": "ప్రిడిక్షన్ ఇన్‌పుట్ ఎంచుకోండి",
        "hi": "प्रेडिक्शन इनपुट चुनें",
    },

    "upload_image": {
        "en": "Upload Image",
        "te": "చిత్రాన్ని అప్‌లోడ్ చేయండి",
        "hi": "चित्र अपलोड करें",
    },

    "scan_grain": {
        "en": "Scan Grain",
        "te": "ధాన్యాన్ని స్కాన్ చేయండి",
        "hi": "धान स्कैन करें",
    },

    "select_image": {
        "en": "Select Paddy Image",
        "te": "వరి చిత్రాన్ని ఎంచుకోండి",
        "hi": "धान का चित्र चुनें",
    },

    "capture_image": {
        "en": "Capture Paddy Image",
        "te": "వరి చిత్రాన్ని క్యాప్చర్ చేయండి",
        "hi": "धान का चित्र कैप्चर करें",
    },

    "uploaded_image": {
        "en": "Uploaded Image",
        "te": "అప్‌లోడ్ చేసిన చిత్రం",
        "hi": "अपलोड किया गया चित्र",
    },

    "captured_image": {
        "en": "Captured Image",
        "te": "క్యాప్చర్ చేసిన చిత్రం",
        "hi": "कैप्चर किया गया चित्र",
    },

    "analyze_image": {
        "en": "Analyze Image",
        "te": "చిత్రాన్ని విశ్లేషించండి",
        "hi": "चित्र का विश्लेषण करें",
    },

    "prediction_result": {
        "en": "Prediction Result",
        "te": "ప్రిడిక్షన్ ఫలితం",
        "hi": "प्रेडिक्शन परिणाम",
    },

    "grain_name": {
        "en": "Grain Name",
        "te": "ధాన్యం పేరు",
        "hi": "धान का नाम",
    },

    "prediction_not_available": {
        "en": "Prediction model is not connected yet.",
        "te": "ప్రిడిక్షన్ మోడల్ ఇంకా కనెక్ట్ కాలేదు.",
        "hi": "प्रेडिक्शन मॉडल अभी कनेक्ट नहीं है।",
    },

    # --------------------------------------------------------
    # ONLY FOUR SUPPORTED VARIETIES
    # --------------------------------------------------------

    "sannalu": {
        "en": "Sannalu — MTU 1010",
        "te": "సన్నాలు — MTU 1010",
        "hi": "सन्नालु — MTU 1010",
    },

    "bondalu": {
        "en": "Bondalu — PLA 1100",
        "te": "బొండాలు — PLA 1100",
        "hi": "बोंडालु — PLA 1100",
    },

    "rnr": {
        "en": "RNR 15048 — Telangana Sona",
        "te": "RNR 15048 — తెలంగాణ సోనా",
        "hi": "RNR 15048 — तेलंगाना सोना",
    },

    "swarna": {
        "en": "Swarna — MTU 7029",
        "te": "స్వర్ణ — MTU 7029",
        "hi": "स्वर्ण — MTU 7029",
    },

    # --------------------------------------------------------
    # CULTIVATION PLANNER
    # --------------------------------------------------------

    "select_grain_type": {
        "en": "Select Grain Type",
        "te": "ధాన్యం రకాన్ని ఎంచుకోండి",
        "hi": "धान की किस्म चुनें",
    },

    "grain_type": {
        "en": "Grain Type",
        "te": "ధాన్యం రకం",
        "hi": "धान की किस्म",
    },

    "land_area": {
        "en": "Land Area",
        "te": "భూమి విస్తీర్ణం",
        "hi": "भूमि क्षेत्र",
    },

    "select_land_size": {
        "en": "Select Land Size",
        "te": "భూమి పరిమాణాన్ని ఎంచుకోండి",
        "hi": "भूमि का आकार चुनें",
    },

    "one_acre": {
        "en": "1 Acre",
        "te": "1 ఎకరం",
        "hi": "1 एकड़",
    },

    "two_acres": {
        "en": "2 Acres",
        "te": "2 ఎకరాలు",
        "hi": "2 एकड़",
    },

    "three_acres": {
        "en": "3 Acres",
        "te": "3 ఎకరాలు",
        "hi": "3 एकड़",
    },

    "other_custom": {
        "en": "Other / Custom",
        "te": "ఇతర / కస్టమ్",
        "hi": "अन्य / कस्टम",
    },

    "enter_land_size": {
        "en": "Enter Land Area",
        "te": "భూమి విస్తీర్ణం నమోదు చేయండి",
        "hi": "भूमि क्षेत्र दर्ज करें",
    },

    "generate_plan": {
        "en": "Generate Cultivation Plan",
        "te": "సాగు ప్రణాళికను రూపొందించండి",
        "hi": "खेती योजना बनाएं",
    },

    "cultivation_plan": {
        "en": "Complete Cultivation Plan",
        "te": "పూర్తి సాగు ప్రణాళిక",
        "hi": "पूरी खेती योजना",
    },

    "selected_variety": {
        "en": "Selected Variety",
        "te": "ఎంచుకున్న రకం",
        "hi": "चयनित किस्म",
    },

    "selected_land_area": {
        "en": "Selected Land Area",
        "te": "ఎంచుకున్న భూమి విస్తీర్ణం",
        "hi": "चयनित भूमि क्षेत्र",
    },

    "expected_yield": {
        "en": "Expected Yield",
        "te": "అంచనా దిగుబడి",
        "hi": "अनुमానित उपज",
    },

    "grain_production": {
        "en": "Expected Grain Production",
        "te": "అంచనా ధాన్యం ఉత్పత్తి",
        "hi": "अनुमानित धान उत्पादन",
    },

    "soil": {
        "en": "Suitable Soil",
        "te": "అనుకూలమైన నేల",
        "hi": "उपयुक्त मिट्टी",
    },

    "fertilizer": {
        "en": "Fertilizer Management",
        "te": "ఎరువుల నిర్వహణ",
        "hi": "उर्वरक प्रबंधन",
    },

    "water": {
        "en": "Water Management",
        "te": "నీటి నిర్వహణ",
        "hi": "जल प्रबंधन",
    },

    "workers": {
        "en": "Worker Estimation",
        "te": "కార్మికుల అంచనా",
        "hi": "श्रमिक अनुमान",
    },

    "pests": {
        "en": "Pest & Disease Management",
        "te": "తెగుళ్లు & వ్యాధుల నిర్వహణ",
        "hi": "कीट और रोग प्रबंधन",
    },

    "weed_management": {
        "en": "Weed Management",
        "te": "కలుపు మొక్కల నిర్వహణ",
        "hi": "खरपतवार प्रबंधन",
    },

    "seed_requirement": {
        "en": "Seed Requirement",
        "te": "విత్తనాల అవసరం",
        "hi": "बीज आवश्यकता",
    },

    "crop_duration": {
        "en": "Crop Duration",
        "te": "పంట కాలం",
        "hi": "फसल अवधि",
    },

    "harvesting": {
        "en": "Harvesting",
        "te": "కోత",
        "hi": "कटाई",
    },

    # --------------------------------------------------------
    # PADDYMITRA
    # --------------------------------------------------------

    "paddy_mitra": {
        "en": "PaddyMitra",
        "te": "PaddyMitra",
        "hi": "PaddyMitra",
    },

    "paddy_mitra_subtitle": {
        "en": "Smart Paddy Cultivation Assistant",
        "te": "స్మార్ట్ ప్యాడీ సాగు సహాయకుడు",
        "hi": "स्मार्ट पैडी खेती सहायक",
    },

    "ask_paddy_mitra": {
        "en": "Ask PaddyMitra your question",
        "te": "PaddyMitra ను మీ ప్రశ్న అడగండి",
        "hi": "PaddyMitra से अपना प्रश्न पूछें",
    },

    "type_question": {
        "en": "Type your question",
        "te": "మీ ప్రశ్నను టైప్ చేయండి",
        "hi": "अपना प्रश्न लिखें",
    },

    "send": {
        "en": "Send",
        "te": "పంపండి",
        "hi": "भेजें",
    },

    "thinking": {
        "en": "PaddyMitra is preparing your answer...",
        "te": "PaddyMitra మీ సమాధానాన్ని సిద్ధం చేస్తోంది...",
        "hi": "PaddyMitra आपका उत्तर तैयार कर रहा है...",
    },

    "out_of_scope": {
        "en": "Sorry, I can answer questions related to Smart Paddy cultivation and the four supported paddy varieties only.",
        "te": "క్షమించండి, నేను Smart Paddy సాగు మరియు మద్దతు ఉన్న నాలుగు వరి రకాల గురించి మాత్రమే సమాధానం ఇవ్వగలను.",
        "hi": "क्षमा करें, मैं केवल Smart Paddy खेती और चार समर्थित धान की किस्मों से संबंधित प्रश्नों का उत्तर दे सकता हूँ।",
    },

    # --------------------------------------------------------
    # HOME
    # --------------------------------------------------------

    "welcome": {
        "en": "Welcome to Smart Paddy",
        "te": "Smart Paddy కి స్వాగతం",
        "hi": "Smart Paddy में आपका स्वागत है",
    },

    "choose_service": {
        "en": "Choose a service to continue.",
        "te": "కొనసాగించడానికి ఒక సేవను ఎంచుకోండి.",
        "hi": "जारी रखने के लिए एक सेवा चुनें।",
    },

    # --------------------------------------------------------
    # LOGIN
    # --------------------------------------------------------

    "login": {
        "en": "Login",
        "te": "లాగిన్",
        "hi": "लॉगिन",
    },

    "username": {
        "en": "Username",
        "te": "యూజర్‌నేమ్",
        "hi": "यूज़रनेम",
    },

    "password": {
        "en": "Password",
        "te": "పాస్‌వర్డ్",
        "hi": "पासवर्ड",
    },

    "login_success": {
        "en": "Login successful.",
        "te": "లాగిన్ విజయవంతమైంది.",
        "hi": "लॉगिन सफल हुआ।",
    },

    "invalid_login": {
        "en": "Invalid username or password.",
        "te": "యూజర్‌నేమ్ లేదా పాస్‌వర్డ్ తప్పుగా ఉంది.",
        "hi": "यूज़रनेम या पासवर्ड गलत है।",
    },

    # --------------------------------------------------------
    # GENERAL
    # --------------------------------------------------------

    "processing": {
        "en": "Processing...",
        "te": "ప్రాసెస్ అవుతోంది...",
        "hi": "प्रोसेस हो रहा है...",
    },

    "please_select": {
        "en": "Please select an option.",
        "te": "దయచేసి ఒక ఎంపికను ఎంచుకోండి.",
        "hi": "कृपया एक विकल्प चुनें।",
    },

    "success": {
        "en": "Success",
        "te": "విజయం",
        "hi": "सफलता",
    },

    "error": {
        "en": "Error",
        "te": "లోపం",
        "hi": "त्रुटि",
    },

    "information": {
        "en": "Information",
        "te": "సమాచారం",
        "hi": "जानकारी",
    },

    "not_available": {
        "en": "Information is not available in the project knowledge base.",
        "te": "ఈ సమాచారం ప్రాజెక్ట్ నాలెడ్జ్ బేస్‌లో అందుబాటులో లేదు.",
        "hi": "यह जानकारी प्रोजेक्ट नॉलेज बेस में उपलब्ध नहीं है।",
    },

    "footer": {
        "en": "Smart Paddy — Smart Support for Farmers",
        "te": "Smart Paddy — రైతులకు స్మార్ట్ సహాయం",
        "hi": "Smart Paddy — किसानों के लिए स्मार्ट सहायता",
    },
}


# ============================================================
# LANGUAGE FUNCTIONS
# ============================================================

def initialize_language():
    """Set English as the default language."""
    if "language" not in st.session_state:
        st.session_state.language = "en"


def get_language():
    """Get the currently selected language."""
    initialize_language()
    return st.session_state.language


def set_language(language_code):
    """Set the selected language."""
    if language_code in LANGUAGE_NAMES:
        st.session_state.language = language_code


def get_language_name(language_code=None):
    """Get the display name of a language."""
    if language_code is None:
        language_code = get_language()

    return LANGUAGE_NAMES.get(language_code, "English")


def t(key):
    """
    Return translated text for the current language.
    English is used as fallback if translation is missing.
    """

    language = get_language()

    if key not in TRANSLATIONS:
        return key

    return TRANSLATIONS[key].get(
        language,
        TRANSLATIONS[key].get("en", key)
    )


def get_supported_languages():
    """Return all supported language display names."""
    return list(LANGUAGES.keys())


def validate_translations():
    """Check whether all translations contain all 3 languages."""

    required_languages = {"en", "te", "hi"}
    problems = []

    for key, values in TRANSLATIONS.items():

        missing = required_languages - set(values.keys())

        if missing:
            problems.append(
                f"{key}: missing {sorted(missing)}"
            )

    return problems