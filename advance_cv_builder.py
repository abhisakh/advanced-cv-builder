"""Advanced CV Builder with AI Enhancement, Job Matcher, Built-in Text Formatter,
Multiple Templates & Dynamic Custom Section Types (EN / DE Support)
"""

import base64
import json
import os
import re
import pymupdf
from datetime import datetime
from io import BytesIO
from typing import Dict, List, Any, cast
import streamlit as st
from weasyprint import HTML
from google import genai
from dotenv import load_dotenv

load_dotenv()

# ============================================================================
# LOCALIZATION DICTIONARIES (EN / DE)
# ============================================================================
TRANSLATIONS = {
    "en": {
        "page_title": "Advanced CV Builder Pro",
        "sidebar_profile": "📁 Profile Management",
        "load_profile": "Load Profile",
        "btn_load": "📂 Load",
        "new_profile": "New Profile Name",
        "btn_save": "💾 Save",
        "restore_version": "Restore Saved Version",
        "btn_restore": "⏪ Restore Selected Version",
        "template_styling": "🎨 Template & Styling",
        "select_template": "Select Template",
        "customize_colors": "Customize Colors",
        "primary_color": "Primary Color",
        "accent_color": "Accent Color",
        "typography": "Typography",
        "font_family": "Font Family",
        "heading_size": "Heading Size (pt)",
        "body_size": "Body Text Size (pt)",
        "line_height": "Line Height",
        "margin_size": "Page Margin (mm)",
        "layout_mode": "Layout Mode",
        "two_columns": "Two Columns",
        "single_column": "Single Column",
        "layout_control": "🧩 Layout & Section Control",
        "section_control_caption": "Toggle visibility and column layout:",
        "sidebar_position": "Sidebar Position",
        "left": "Left",
        "right": "Right",
        "sidebar_width": "Sidebar Width (%)",
        "reorder_priority": "Reorder Section Priority:",
        "section_render_order": "Section Render Order",
        "profile_photo": "🖼️ Profile Photo",
        "include_photo": "Include Profile Photo",
        "upload_photo": "Upload Photo",
        "position": "Position",
        "shape": "Shape",
        "circular": "Circular",
        "square": "Square",
        "rectangular": "Rectangular",
        "width_px": "Width (px)",
        "height_px": "Height (px)",
        "photo_offsets": "Photo Frame Offsets",
        "horizontal_offset": "Horizontal Offset (%)",
        "vertical_offset": "Vertical Offset (%)",
        "custom_sections": "➕ Custom Sections",
        "section_name": "Section Name",
        "section_type": "Section Type",
        "btn_add_section": "Add Section",
        "current_custom_sections": "**Current Custom Sections:**",
        "personal_info": "👤 Personal Information",
        "full_name": "Full Name *",
        "professional_title": "Professional Title *",
        "phone": "Phone *",
        "phone_warning": "⚠️ Phone format may be invalid",
        "email": "Email *",
        "email_error": "❌ Invalid email format",
        "location": "Location",
        "residency": "Residency Status",
        "relocation": "Relocation",
        "linkedin_profile": "LinkedIn Profile",
        "url_warning": "⚠️ Invalid URL format",
        "summary": "Professional Summary (Markdown supported: **bold**, *italic*, `code`, ^sup^, ~sub~)",
        "summary_warning": "💡 Summary is quite short. Aim for 150-300 words for better impact.",
        "cv_content": "📝 CV Content",
        "profiles_links": "🔗 Profiles & Links",
        "github": "GitHub",
        "linkedin": "LinkedIn",
        "portfolio": "Portfolio/Website",
        "tech_skills": "💻 Technical Skills",
        "num_tech": "Number of Technical Skill Categories/Items",
        "name": "Name",
        "description": "Description",
        "keywords": "Keywords (comma separated or lines)",
        "soft_skills": "🤝 Soft Skills",
        "num_soft": "Number of Soft Skill Categories/Items",
        "strengths": "💪 Strengths",
        "num_strengths": "Number of Strength Categories/Items",
        "interests": "🎯 Interests",
        "num_interests": "Number of Interest Categories/Items",
        "certifications": "🏆 Certifications",
        "num_certs": "Number of Certifications",
        "issuer": "Issuer",
        "date": "Date",
        "website_url": "Website URL",
        "link_label": "Link Label",
        "awards": "🎖️ Awards",
        "num_awards": "Number of Awards",
        "awarder": "Awarder",
        "languages": "🌍 Languages",
        "num_langs": "Number of Languages",
        "experience": "💼 Work Experience",
        "num_exp": "Number of Experience Entries",
        "company_name": "Company Name",
        "position_title": "Position / Job Title",
        "date_range": "Date Range",
        "summary_placeholder": "Brief overview of the role...",
        "achievements": "Key Achievements / Bullets (Markdown supported)",
        "education": "🎓 Education",
        "num_edu": "Number of Education Entries",
        "school": "School/University",
        "graduation_date": "Graduation Date",
        "gpa": "GPA (optional)",
        "highlights": "Highlights/Details (Markdown supported)",
        "projects": "🚀 Projects",
        "num_projects": "Number of Projects",
        "project_name": "Name",
        "project_desc": "Description (Markdown supported)",
        "analysis_export": "📊 CV Analysis & Export Options",
        "completeness_score": "CV Completeness Score",
        "improvement_suggestions": "📋 Improvement Suggestions",
        "btn_ai_general": "✨ Get General AI Suggestions",
        "general_ai_suggestions": "🤖 General AI Suggestions",
        "job_matching": "🎯 Target Job Matching & Customization",
        "paste_job_desc": "Paste Job Description / Requirements",
        "btn_analyze_job": "🎯 Analyze & Match Job Description",
        "tailored_recommendations": "📌 Tailored Job Recommendations",
        "export_options": "⚙️ Export Options",
        "btn_download_pdf": "📥 Download PDF",
        "btn_download_json": "💾 Download JSON",
        "save_version": "📝 Save Version",
        "version_tag": "Version Tag",
        "confirm_save": "Confirm Save",
        "live_preview": "👀 Live Preview",
        "preview_pages": "Preview ({num} Page/s)",
        "pro_tips": "💡 Pro Tips: Fill all fields with *, keep summary 150-300 words, use action verbs in experience bullets, maintain consistent formatting",
        "lang_switch_label": "🌐 Sprache / Language",
        "visit_website": "Visit Website",
        "view_credentials": "View Credentials",
        "view_project": "View Project"
    },
    "de": {
        "page_title": "Erweiterter Lebenslauf-Generator Pro",
        "sidebar_profile": "📁 Profilverwaltung",
        "load_profile": "Profil laden",
        "btn_load": "📂 Laden",
        "new_profile": "Neuer Profilname",
        "btn_save": "💾 Speichern",
        "restore_version": "Gespeicherte Version wiederherstellen",
        "btn_restore": "⏪ Ausgewählte Version wiederherstellen",
        "template_styling": "🎨 Design & Vorlagen",
        "select_template": "Vorlage auswählen",
        "customize_colors": "Farben anpassen",
        "primary_color": "Primärfarbe",
        "accent_color": "Akzentfarbe",
        "typography": "Typografie",
        "font_family": "Schriftart",
        "heading_size": "Überschriftengröße (pt)",
        "body_size": "Fließtextgröße (pt)",
        "line_height": "Zeilenabstand",
        "margin_size": "Seitenrand (mm)",
        "layout_mode": "Layout-Modus",
        "two_columns": "Zweispaltig",
        "single_column": "Einspaltig",
        "layout_control": "🧩 Layout- & Abschnittssteuerung",
        "section_control_caption": "Sichtbarkeit und Spaltenlayout umschalten:",
        "sidebar_position": "Seitenleisten-Position",
        "left": "Links",
        "right": "Rechts",
        "sidebar_width": "Seitenleisten-Breite (%)",
        "reorder_priority": "Abschnittspriorität ändern:",
        "section_render_order": "Reihenfolge der Abschnitte",
        "profile_photo": "🖼️ Profilfoto",
        "include_photo": "Profilfoto einschließen",
        "upload_photo": "Foto hochladen",
        "position": "Position",
        "shape": "Form",
        "circular": "Kreisrund",
        "square": "Quadratisch",
        "rectangular": "Rechteckig",
        "width_px": "Breite (px)",
        "height_px": "Höhe (px)",
        "photo_offsets": "Foto-Rahmen-Verschiebung",
        "horizontal_offset": "Horizontale Verschiebung (%)",
        "vertical_offset": "Vertikale Verschiebung (%)",
        "custom_sections": "➕ Benutzerdefinierte Abschnitte",
        "section_name": "Abschnittsname",
        "section_type": "Abschnittstyp",
        "btn_add_section": "Abschnitt hinzufügen",
        "current_custom_sections": "**Aktuelle benutzerdefinierte Abschnitte:**",
        "personal_info": "👤 Persönliche Informationen",
        "full_name": "Vollständiger Name *",
        "professional_title": "Berufsbezeichnung *",
        "phone": "Telefon *",
        "phone_warning": "⚠️ Telefonformat ist möglicherweise ungültig",
        "email": "E-Mail *",
        "email_error": "❌ Ungültiges E-Mail-Format",
        "location": "Standort",
        "residency": "Aufenthaltsstatus",
        "relocation": "Umzugsbereitschaft",
        "linkedin_profile": "LinkedIn-Profil",
        "url_warning": "⚠️ Ungültiges URL-Format",
        "summary": "Berufliches Profil (Markdown unterstützt: **fett**, *kursiv*, `code`, ^hoch^, ~tief~)",
        "summary_warning": "💡 Die Zusammenfassung ist recht kurz. Streben Sie 150-300 Wörter an.",
        "cv_content": "📝 Lebenslauf-Inhalt",
        "profiles_links": "🔗 Profile & Links",
        "github": "GitHub",
        "linkedin": "LinkedIn",
        "portfolio": "Portfolio/Website",
        "tech_skills": "💻 Technische Fähigkeiten",
        "num_tech": "Anzahl technischer Skill-Kategorien/Einträge",
        "name": "Name",
        "description": "Beschreibung",
        "keywords": "Schlüsselwörter (kommagetrennt oder zeilenweise)",
        "soft_skills": "🤝 Soziale Kompetenzen (Soft Skills)",
        "num_soft": "Anzahl Soft-Skill-Kategorien/Einträge",
        "strengths": "💪 Stärken",
        "num_strengths": "Anzahl Stärken-Kategorien/Einträge",
        "interests": "🎯 Interessen",
        "num_interests": "Anzahl Interessen-Kategorien/Einträge",
        "certifications": "🏆 Zertifizierungen",
        "num_certs": "Anzahl Zertifizierungen",
        "issuer": "Aussteller",
        "date": "Datum",
        "website_url": "Web-URL",
        "link_label": "Link-Beschriftung",
        "awards": "🎖️ Auszeichnungen",
        "num_awards": "Anzahl Auszeichnungen",
        "awarder": "Verleiher",
        "languages": "🌍 Sprachen",
        "num_langs": "Anzahl Sprachen",
        "experience": "💼 Berufserfahrung",
        "num_exp": "Anzahl Berufserfahrungseinträge",
        "company_name": "Unternehmensname",
        "position_title": "Position / Jobtitel",
        "date_range": "Zeitraum",
        "summary_placeholder": "Kurze Übersicht über die Rolle...",
        "achievements": "Wichtigste Erfolge / Aufzählungspunkte (Markdown unterstützt)",
        "education": "🎓 Ausbildung",
        "num_edu": "Anzahl Ausbildungseinträge",
        "school": "Schule / Universität",
        "graduation_date": "Abschlussdatum",
        "gpa": "Notendurchschnitt (optional)",
        "highlights": "Highlights / Details (Markdown unterstützt)",
        "projects": "🚀 Projekte",
        "num_projects": "Anzahl Projekte",
        "project_name": "Name",
        "project_desc": "Beschreibung (Markdown unterstützt)",
        "analysis_export": "📊 Lebenslauf-Analyse & Exportoptionen",
        "completeness_score": "Vollständigkeitsgrad des Lebenslaufs",
        "improvement_suggestions": "📋 Verbesserungsvorschläge",
        "btn_ai_general": "✨ Allgemeine KI-Vorschläge abrufen",
        "general_ai_suggestions": "🤖 Allgemeine KI-Vorschläge",
        "job_matching": "🎯 Stellenabgleich & KI-Anpassung",
        "paste_job_desc": "Stellenbeschreibung / Anforderungen einfügen",
        "btn_analyze_job": "🎯 Stellenbeschreibung analysieren & abgleichen",
        "tailored_recommendations": "📌 Maßgeschneiderte Job-Empfehlungen",
        "export_options": "⚙️ Exportoptionen",
        "btn_download_pdf": "📥 PDF herunterladen",
        "btn_download_json": "💾 JSON herunterladen",
        "save_version": "📝 Version speichern",
        "version_tag": "Versions-Tag",
        "confirm_save": "Speichern bestätigen",
        "live_preview": "👀 Live-Vorschau",
        "preview_pages": "Vorschau ({num} Seite/n)",
        "pro_tips": "💡 Profi-Tipps: Alle Felder mit * ausfüllen, Zusammenfassung 150-300 Wörter lang halten, Aktionsverben nutzen",
        "lang_switch_label": "🌐 Language / Sprache",
        "visit_website": "Website besuchen",
        "view_credentials": "Nachweise anzeigen",
        "view_project": "Projekt ansehen"
    }
}

# ============================================================================
# BUILT-IN TEXT FORMATTER
# ============================================================================

class TextFormatter:
    """Parses lightweight markdown syntax into standard HTML tags for PDF rendering."""

    @staticmethod
    def format_html_for_pdf(text: str) -> str:
        if not text:
            return ""

        text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

        text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
        text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
        text = re.sub(r'__(.*?)__', r'<u>\1</u>', text)
        text = re.sub(r'~~(.*?)~~', r'<del>\1</del>', text)
        text = re.sub(r'\^(.*?)\^', r'<sup>\1</sup>', text)
        text = re.sub(r'~(.*?)~', r'<sub>\1</sub>', text)
        text = re.sub(r'`(.*?)`', r'<code>\1</code>', text)

        lines = text.split('\n')
        processed_lines = []
        in_list = False

        for line in lines:
            stripped = line.strip()
            if re.match(r'^[\*\-]\s+', stripped):
                bullet_content = re.sub(r'^[\*\-]\s+', '', stripped)
                if not in_list:
                    processed_lines.append('<ul>')
                    in_list = True
                processed_lines.append(f'<li>{bullet_content}</li>')
            else:
                if in_list:
                    processed_lines.append('</ul>')
                    in_list = False
                if stripped:
                    processed_lines.append(f'{line}<br>')
                else:
                    processed_lines.append('<br>')

        if in_list:
            processed_lines.append('</ul>')

        return "".join(processed_lines)

# ============================================================================
# CONFIGURATION & CONSTANTS
# ============================================================================
SAVED_PROFILES_DIR = "saved_cvs"
VERSION_HISTORY_DIR = "cv_versions"
os.makedirs(SAVED_PROFILES_DIR, exist_ok=True)
os.makedirs(VERSION_HISTORY_DIR, exist_ok=True)

CV_TEMPLATES = {
    "Modern": {
        "layout": "two-column",
        "primary_color": "#2b3a4a",
        "accent": "#0066cc",
        "sidebar_bg": "#f0f4f8",
        "font": "Helvetica",
        "style": "professional"
    },
    "Classic": {
        "layout": "single-column",
        "primary_color": "#1a1a1a",
        "accent": "#333333",
        "sidebar_bg": "#ffffff",
        "font": "Georgia",
        "style": "traditional"
    },
    "Minimal": {
        "layout": "single-column",
        "primary_color": "#000000",
        "accent": "#666666",
        "sidebar_bg": "#ffffff",
        "font": "Arial",
        "style": "minimal"
    },
    "Creative": {
        "layout": "two-column",
        "primary_color": "#E63946",
        "accent": "#A23B72",
        "sidebar_bg": "#F7F7F7",
        "font": "Helvetica",
        "style": "creative"
    }
}

DEFAULT_SECTIONS = [
    "Profiles & Links",
    "Technical Skills",
    "Soft Skills",
    "Strengths",
    "Interests",
    "Experience",
    "Education",
    "Projects",
    "Certifications",
    "Awards",
    "Languages"
]

SECTION_TYPES = [
    "Experience Layout",
    "Certification Layout",
    "Summary Layout",
    "Projects",
    "Technical Skills",
    "Soft Skills",
    "Strengths",
    "Interests",
    "Generic Text"
]

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_image_base64(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        base64_encoded = base64.b64encode(bytes_data).decode("utf-8")
        return f"data:{uploaded_file.type};base64,{base64_encoded}"
    return None

def validate_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_url(url: str) -> bool:
    pattern = r'^https?://[^\s/$.?#].[^\s]*$'
    return re.match(pattern, url) is not None

def validate_phone(phone: str) -> bool:
    phone = phone.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
    return len(phone) >= 7 and phone.replace("+", "").isdigit()

def save_version(cv_data: Dict, version_name: str):
    version_data = {
        "timestamp": datetime.now().isoformat(),
        "name": version_name,
        "data": cv_data
    }
    file_path = os.path.join(VERSION_HISTORY_DIR, f"{version_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    with open(file_path, 'w') as f:
        json.dump(version_data, f, indent=2)
    return file_path

def load_all_versions(profile_name: str) -> List[Dict]:
    versions = []
    if os.path.exists(VERSION_HISTORY_DIR):
        for file in os.listdir(VERSION_HISTORY_DIR):
            if file.startswith(profile_name):
                with open(os.path.join(VERSION_HISTORY_DIR, file), 'r') as f:
                    versions.append(json.load(f))
    return sorted(versions, key=lambda x: x['timestamp'], reverse=True)

def get_cv_score(cv_data: Dict) -> tuple[int, List[str]]:
    score = 0
    suggestions = []

    if cv_data.get("full_name"): score += 5
    else: suggestions.append("❌ Add your full name")

    if cv_data.get("email"): score += 5
    else: suggestions.append("❌ Add your email address")

    if cv_data.get("phone"): score += 5
    else: suggestions.append("❌ Add your phone number")

    if cv_data.get("summary"): score += 5
    else: suggestions.append("❌ Write a professional summary")

    sections = cv_data.get("sections_data", {})

    if sections.get("Technical Skills"): score += 10
    else: suggestions.append("⚠️ Add technical skills")

    if sections.get("Experience"): score += 15
    else: suggestions.append("⚠️ Add work experience")

    if sections.get("Education"): score += 10
    else: suggestions.append("⚠️ Add education")

    if sections.get("Projects"): score += 10
    else: suggestions.append("⚠️ Add projects to showcase impact")

    if sections.get("Certifications"): score += 5
    else: suggestions.append("💡 Consider adding certifications")

    if cv_data.get("email") and validate_email(cv_data.get("email", "")):
        score += 5

    if cv_data.get("phone") and validate_phone(cv_data.get("phone", "")):
        score += 5

    if sections.get("Profiles & Links"):
        profiles = sections["Profiles & Links"]
        valid_count = 0
        for link in profiles.values():
            if link and validate_url(link):
                valid_count += 1
        score += min(5, valid_count * 2)

    summary = cv_data.get("summary", "")
    if len(summary) > 50: score += 5
    if len(summary) > 100: score += 5

    return min(100, score), suggestions

@st.cache_resource
def get_gemini_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        try:
            api_key = st.secrets.get("GEMINI_API_KEY")
        except Exception:
            pass
    if not api_key:
        raise ValueError("GEMINI_API_KEY is missing. Please check your .env file or Streamlit secrets.")
    return genai.Client(api_key=api_key)

def get_cv_enhancement_suggestions(cv_data: Dict) -> str:
    try:
        client = get_gemini_client()
        prompt = f"""Analyze this CV data and provide specific, actionable improvements:

Full Name: {cv_data.get('full_name', 'N/A')}
Title: {cv_data.get('title', 'N/A')}
Summary: {cv_data.get('summary', 'N/A')}

Experience: {json.dumps(cv_data.get('sections_data', {}).get('Experience', {}), indent=2)}

Skills: {json.dumps(cv_data.get('sections_data', {}).get('Technical Skills', []), indent=2)}

Provide:
1. 2-3 specific improvements to make this CV more impactful
2. Keywords to add based on current role
3. Format improvements for clarity
4. Action verbs to strengthen experience descriptions

Be concise and actionable."""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        return response.text or ""
    except Exception as e:
        return f"⚠️ Could not generate AI suggestions: {str(e)}"

def get_job_tailored_suggestions(cv_data: Dict, job_description: str) -> str:
    try:
        client = get_gemini_client()
        prompt = f"""You are an expert ATS (Applicant Tracking System) reviewer and hiring consultant.
Compare the provided Candidate CV against the Target Job Description below.

--- TARGET JOB DESCRIPTION ---
{job_description}

--- CANDIDATE CV DATA ---
Target Title: {cv_data.get('title', 'N/A')}
Summary: {cv_data.get('summary', 'N/A')}
Skills: {json.dumps(cv_data.get('sections_data', {}).get('Technical Skills', []), indent=2)}
Experience: {json.dumps(cv_data.get('sections_data', {}).get('Experience', {}), indent=2)}
Projects: {json.dumps(cv_data.get('sections_data', {}).get('Projects', {}), indent=2)}

--- INSTRUCTIONS ---
Provide a targeted gap analysis formatted cleanly in markdown with the following sections:
1. **Match Score**: Provide an estimated ATS match percentage (0-100%).
2. **Missing Keywords & Skills**: List key technical/hard/soft skills present in the job posting that are missing or weak in the CV.
3. **Tailored Summary Recommendation**: Provide a rewritten, optimized version of the candidate's professional summary tailored specifically for this role.
4. **Experience Bullet Point Modifications**: Suggest 3 specific bullet point edits from their past roles to highlight requirements from the job description.
"""
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        return response.text or ""
    except Exception as e:
        return f"⚠️ Could not generate job tailoring analysis: {str(e)}"

# ============================================================================
# PAGE CONFIGURATION, STYLES & SESSION STATE
# ============================================================================

st.set_page_config(
    page_title="Advanced CV Builder Pro",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "language" not in st.session_state:
    st.session_state.language = "en"

def t(key: str) -> str:
    lang_dict = TRANSLATIONS.get(st.session_state.language, TRANSLATIONS["en"])
    return lang_dict.get(key, TRANSLATIONS["en"].get(key, key))

st.markdown(
    """
    <style>
    html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"], .main .block-container {
        height: 100vh !important;
        overflow: hidden !important;
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
        max-width: 100% !important;
    }
    [data-testid="stHorizontalBlock"] {
        height: calc(100vh - 2.5rem) !important;
        align-items: stretch !important;
        gap: 1.5rem !important;
    }
    [data-testid="stHorizontalBlock"] > [data-testid="column"] {
        height: 100% !important;
        min-height: 0 !important;
        display: flex !important;
        flex-direction: column !important;
    }
    [data-testid="stHorizontalBlock"] > [data-testid="column"] > div,
    [data-testid="stHorizontalBlock"] > [data-testid="column"] [data-testid="stVerticalBlockBorderWrapper"],
    [data-testid="stHorizontalBlock"] > [data-testid="column"] [data-testid="stVerticalBlock"] {
        height: 100% !important;
        max-height: 100% !important;
        overflow-y: auto !important;
        overflow-x: hidden !important;
        flex: 1 1 auto !important;
        display: flex !important;
        flex-direction: column !important;
        padding-bottom: 5rem !important;
        box-sizing: border-box !important;
    }
    [data-testid="stHorizontalBlock"] > [data-testid="column"] div::-webkit-scrollbar {
        width: 6px;
    }
    [data-testid="stHorizontalBlock"] > [data-testid="column"] div::-webkit-scrollbar-thumb {
        background-color: #cccccc;
        border-radius: 4px;
    }
    div[data-testid="stExpander"] {
        height: auto !important;
        min-height: 0 !important;
    }
    [data-testid="stVerticalBlock"] {
        gap: 0.5rem !important;
    }
    .column-footer {
        margin-top: auto !important;
        padding-top: 1rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

if "custom_sections" not in st.session_state:
    st.session_state.custom_sections = []
if "custom_section_types" not in st.session_state:
    st.session_state.custom_section_types = {}
if "cv_data" not in st.session_state:
    st.session_state.cv_data = {}
if "selected_template" not in st.session_state:
    st.session_state.selected_template = "Modern"
if "show_ai_suggestions" not in st.session_state:
    st.session_state.show_ai_suggestions = False
if "show_job_match" not in st.session_state:
    st.session_state.show_job_match = False

if "section_visibility" not in st.session_state:
    st.session_state.section_visibility = {sec: True for sec in DEFAULT_SECTIONS}
if "section_placement" not in st.session_state:
    st.session_state.section_placement = {
        "Profiles & Links": "Sidebar",
        "Technical Skills": "Sidebar",
        "Soft Skills": "Sidebar",
        "Strengths": "Sidebar",
        "Interests": "Sidebar",
        "Languages": "Sidebar",
        "Certifications": "Sidebar",
        "Awards": "Sidebar",
        "Experience": "Main Column",
        "Education": "Main Column",
        "Projects": "Main Column"
    }
if "section_order" not in st.session_state:
    st.session_state.section_order = list(DEFAULT_SECTIONS)

# ============================================================================
# SIDEBAR - LANGUAGE SWITCHER & PROFILE MANAGEMENT
# ============================================================================

st.sidebar.title("🎯 CV Builder Pro")

selected_lang_label = st.sidebar.selectbox(
    t("lang_switch_label"),
    options=["English", "Deutsch"],
    index=0 if st.session_state.language == "en" else 1
)
new_lang_code = "en" if selected_lang_label == "English" else "de"
if new_lang_code != st.session_state.language:
    st.session_state.language = new_lang_code
    st.rerun()

with st.sidebar.expander(t("sidebar_profile"), expanded=True):
    saved_files = [f.replace(".json", "") for f in os.listdir(SAVED_PROFILES_DIR) if f.endswith(".json")]

    col_load, col_new = st.columns(2)

    with col_load:
        selected_profile = st.selectbox(t("load_profile"), ["Default"] + saved_files, key="profile_select")
        if st.button(t("btn_load"), use_container_width=True):
            if selected_profile != "Default":
                file_path = os.path.join(SAVED_PROFILES_DIR, f"{selected_profile}.json")
                with open(file_path, "r") as f:
                    loaded_data = json.load(f)
                    st.session_state.cv_data = loaded_data
                    st.session_state.custom_sections = loaded_data.get("custom_sections", [])
                    st.session_state.custom_section_types = loaded_data.get("custom_section_types", {})
                    st.session_state.section_visibility = loaded_data.get("section_visibility", st.session_state.section_visibility)
                    st.session_state.section_placement = loaded_data.get("section_placement", st.session_state.section_placement)
                    st.session_state.section_order = loaded_data.get("section_order", st.session_state.section_order)
                st.success(f"✅ Loaded '{selected_profile}'")
                st.rerun()

    with col_new:
        new_profile_name = st.text_input(t("new_profile"), placeholder="My CV")
        if st.button(t("btn_save"), use_container_width=True):
            if new_profile_name:
                st.session_state.cv_data["custom_sections"] = st.session_state.custom_sections
                st.session_state.cv_data["custom_section_types"] = st.session_state.custom_section_types
                st.session_state.cv_data["section_visibility"] = st.session_state.section_visibility
                st.session_state.cv_data["section_placement"] = st.session_state.section_placement
                st.session_state.cv_data["section_order"] = st.session_state.section_order
                file_path = os.path.join(SAVED_PROFILES_DIR, f"{new_profile_name}.json")
                with open(file_path, "w") as f:
                    json.dump(st.session_state.cv_data, f, indent=2)
                st.success(f"✅ Saved '{new_profile_name}'")

    if selected_profile != "Default":
        st.divider()
        versions = load_all_versions(selected_profile)
        if versions:
            version_names = [f"{v['timestamp'][:16].replace('T', ' ')} - {v['name']}" for v in versions]
            selected_v_idx = st.selectbox(t("restore_version"), range(len(version_names)), format_func=lambda x: version_names[x])
            if st.button(t("btn_restore"), use_container_width=True):
                restored = versions[selected_v_idx]["data"]
                st.session_state.cv_data = restored
                st.session_state.custom_sections = restored.get("custom_sections", [])
                st.session_state.custom_section_types = restored.get("custom_section_types", {})
                st.session_state.section_visibility = restored.get("section_visibility", st.session_state.section_visibility)
                st.session_state.section_placement = restored.get("section_placement", st.session_state.section_placement)
                st.session_state.section_order = restored.get("section_order", st.session_state.section_order)
                st.success("✅ Restored version!")
                st.rerun()

# ============================================================================
# SIDEBAR - TEMPLATE SELECTION & DYNAMIC LAYOUT
# ============================================================================

with st.sidebar.expander(t("template_styling"), expanded=True):
    st.session_state.selected_template = st.selectbox(t("select_template"), list(CV_TEMPLATES.keys()))
    selected_tpl = cast(str, st.session_state.selected_template)
    template_config = CV_TEMPLATES[selected_tpl]

    st.divider()
    st.subheader(t("customize_colors"))
    col_primary, col_accent = st.columns(2)

    with col_primary:
        primary_color = st.color_picker(t("primary_color"), template_config["primary_color"])
    with col_accent:
        accent_color = st.color_picker(t("accent_color"), template_config["accent"])

    st.subheader(t("typography"))
    col_font, col_size = st.columns(2)

    with col_font:
        font_family = st.selectbox(t("font_family"), ["Helvetica", "Arial", "Georgia", "Times New Roman"])
    with col_size:
        heading_size = st.slider(t("heading_size"), 10, 16, 13)

    body_size = st.slider(t("body_size"), 9, 12, 10)
    line_height = st.slider(t("line_height"), 1.2, 1.8, 1.4, 0.1)
    margin_size = st.slider(t("margin_size"), 8, 20, 12)

    layout_mode = st.radio(t("layout_mode"), [t("two_columns"), t("single_column")])
    layout_mode = "Two Columns" if layout_mode == t("two_columns") else "Single Column"

with st.sidebar.expander(t("layout_control"), expanded=False):
    st.caption(t("section_control_caption"))

    if layout_mode == "Two Columns":
        st.subheader("Column Configuration")
        sidebar_position = st.selectbox(t("sidebar_position"), [t("left"), t("right")])
        sidebar_position = "Left" if sidebar_position == t("left") else "Right"
        sidebar_width_pct = st.slider(t("sidebar_width"), 20, 50, 32)
        main_width_pct = 100 - sidebar_width_pct
    else:
        sidebar_position = "Right"
        sidebar_width_pct = 0
        main_width_pct = 100

    available_sections = list(dict.fromkeys(DEFAULT_SECTIONS + st.session_state.custom_sections))

    st.session_state.section_order = [s for s in st.session_state.section_order if s in available_sections]
    for s in available_sections:
        if s not in st.session_state.section_order:
            st.session_state.section_order.append(s)

    for sec in list(st.session_state.section_order):
        st.markdown(f"**{sec}**")
        c_vis, c_pos = st.columns([1, 1])
        with c_vis:
            st.session_state.section_visibility[sec] = st.checkbox(
                "Show",
                value=st.session_state.section_visibility.get(sec, True),
                key=f"vis_{sec}"
            )
        with c_pos:
            st.session_state.section_placement[sec] = st.selectbox(
                "Column",
                ["Main Column", "Sidebar"],
                index=0 if st.session_state.section_placement.get(sec, "Main Column") == "Main Column" else 1,
                key=f"pos_{sec}"
            )

    st.divider()
    st.subheader("🔄 " + t("reorder_priority"))
    st.info("⚠️ Reorder sections here to change their order in PDF export.", icon="ℹ️")

    new_order = list(st.session_state.section_order)

    for idx in range(len(new_order)):
        col1, col2, col3, col4 = st.columns([2, 0.8, 0.8, 1.5])

        with col1:
            st.write(f"**{idx+1}.** {new_order[idx]}")

        with col2:
            if idx > 0 and st.button("⬆ Up", key=f"move_up_{idx}_{new_order[idx]}"):
                new_order[idx], new_order[idx-1] = new_order[idx-1], new_order[idx]
                st.session_state.section_order = new_order
                st.rerun()

        with col3:
            if idx < len(new_order) - 1 and st.button("⬇ Down", key=f"move_down_{idx}_{new_order[idx]}"):
                new_order[idx], new_order[idx+1] = new_order[idx+1], new_order[idx]
                st.session_state.section_order = new_order
                st.rerun()

        with col4:
            is_visible = st.session_state.section_visibility.get(new_order[idx], True)
            show_section = st.checkbox("👁️ Show in CV", value=is_visible, key=f"show_section_{idx}_{new_order[idx]}")
            st.session_state.section_visibility[new_order[idx]] = show_section

    st.session_state.section_order = new_order

# ============================================================================
# SIDEBAR - PROFILE PHOTO & FRAME OFFSETS
# ============================================================================

photo_b64 = None
photo_settings = {
    "position": "Header Right",
    "shape": "Circular",
    "width": 100,
    "height": 100,
    "border_radius": "50%",
    "offset_x": 50,
    "offset_y": 50,
}

with st.sidebar.expander(t("profile_photo")):
    show_photo = st.checkbox(t("include_photo"), value=False)

    if show_photo:
        uploaded_photo = st.file_uploader(t("upload_photo"), type=["jpg", "jpeg", "png"])

        col_pos, col_shape = st.columns(2)
        with col_pos:
            photo_settings["position"] = st.selectbox(t("position"), ["Left Sidebar", "Header Right", "Header Left"])
        with col_shape:
            photo_settings["shape"] = st.selectbox(t("shape"), [t("circular"), t("square"), t("rectangular")])
            if photo_settings["shape"] == t("circular"): photo_settings["shape"] = "Circular"
            elif photo_settings["shape"] == t("square"): photo_settings["shape"] = "Square"
            else: photo_settings["shape"] = "Rectangular"

        col_w, col_h = st.columns(2)
        with col_w:
            photo_settings["width"] = st.slider(t("width_px"), 80, 180, 100)
        with col_h:
            if photo_settings["shape"] == "Rectangular":
                photo_settings["height"] = st.slider(t("height_px"), 80, 220, 130)
            else:
                photo_settings["height"] = photo_settings["width"]

        photo_settings["border_radius"] = "50%" if photo_settings["shape"] == "Circular" else "0px"

        st.subheader(t("photo_offsets"))
        photo_settings["offset_x"] = st.slider(t("horizontal_offset"), 0, 100, 50)
        photo_settings["offset_y"] = st.slider(t("vertical_offset"), 0, 100, 50)

        if uploaded_photo:
            photo_b64 = get_image_base64(uploaded_photo)

# ============================================================================
# SIDEBAR - CUSTOM SECTIONS WITH DROPDOWN TYPE SELECTION
# ============================================================================

with st.sidebar.expander(t("custom_sections")):
    new_sec_name = st.text_input(t("section_name"), placeholder="e.g., Publications")
    sec_type_choice = st.selectbox(t("section_type"), SECTION_TYPES)

    if st.button(t("btn_add_section"), use_container_width=True):
        if new_sec_name and new_sec_name not in st.session_state.custom_sections:
            st.session_state.custom_sections.append(new_sec_name)
            st.session_state.custom_section_types[new_sec_name] = sec_type_choice
            st.session_state.section_visibility[new_sec_name] = True
            st.session_state.section_placement[new_sec_name] = "Main Column"
            st.session_state.section_order.append(new_sec_name)
            st.success(f"✅ Added '{new_sec_name}' as {sec_type_choice}")
            st.rerun()

    if st.session_state.custom_sections:
        st.markdown(t("current_custom_sections"))
        for i, sec in enumerate(list(st.session_state.custom_sections)):
            col_name, col_del = st.columns([4, 1])
            with col_name:
                sec_t = st.session_state.custom_section_types.get(sec, "Generic Text")
                st.caption(f"• {sec} ({sec_t})")
            with col_del:
                if st.button("🗑️", key=f"del_{sec}", use_container_width=True):
                    st.session_state.custom_sections.remove(sec)
                    if sec in st.session_state.custom_section_types:
                        del st.session_state.custom_section_types[sec]
                    if sec in st.session_state.section_order:
                        st.session_state.section_order.remove(sec)
                    st.rerun()

# ============================================================================
# RENDERING UTILITIES FOR PDF PREVIEW
# ============================================================================

def render_experience_items(exp_list):
    sec_html = ""
    for exp in exp_list:
        company = exp.get("company", "")
        title = exp.get("title", "")
        website = exp.get("website", "")
        link_label = exp.get("link_label") or t("visit_website")
        date_range = exp.get("date_range", "")
        loc = exp.get("location", "")
        summary = TextFormatter.format_html_for_pdf(exp.get("summary", ""))

        comp_bold = "font-weight: bold;" if exp.get("bold_company", False) else ""
        comp_italic = "font-style: italic;" if exp.get("italic_company", False) else ""
        comp_size = f"font-size: {exp.get('company_size', 10)}pt;"
        company_html = f'<span class="entry-subtitle" style="{comp_bold} {comp_italic} {comp_size}">{company}</span>' if company else ""

        title_html = f'<span class="entry-title">{TextFormatter.format_html_for_pdf(title)}</span>' if title else ""
        date_html = f'<span class="entry-meta">{date_range}</span>' if date_range else ""

        link_html = f'<div class="entry-meta" style="margin-top: 2px;"><a href="{website}" target="_blank">{link_label} &rarr;</a></div>' if website else ""
        loc_html = f'<span class="entry-meta" style="margin-left: 8px;">📍 {loc}</span>' if loc else ""

        sub_container = ""
        if company_html or loc_html:
            sub_container = f'<div style="margin-bottom: 4px;">{company_html} {loc_html}</div>'

        summary_html = f'<p style="margin-bottom: 6px;">{summary}</p>' if summary else ""

        bullets_html = ""
        if exp.get("bullets"):
            bullets_html += '<ul>'
            for bullet in exp.get("bullets", []):
                bullets_html += f'<li>{TextFormatter.format_html_for_pdf(bullet)}</li>'
            bullets_html += '</ul>'

        if title_html or sub_container or summary_html or bullets_html or link_html:
            sec_html += f'''
            <div class="entry">
                <div class="entry-header">
                    {title_html}
                    {date_html}
                </div>
                {sub_container}
                {link_html}
                {summary_html}
                {bullets_html}
            </div>
            '''
    return sec_html

def render_certification_items(cert_list):
    sec_html = ""
    for cert in cert_list:
        title_str = cert.get("title", "")
        url_str = cert.get("url", "")
        label_str = cert.get("label") or t("view_credentials")
        issuer_str = cert.get("issuer", "")
        date_str = cert.get("date", "")
        summary_str = TextFormatter.format_html_for_pdf(cert.get("summary", ""))

        title_html = f'<span class="entry-title">{title_str}</span>' if title_str else ""
        date_html = f'<span class="entry-meta">{date_str}</span>' if date_str else ""

        iss_bold = "font-weight: bold;" if cert.get("bold_issuer", False) else ""
        iss_italic = "font-style: italic;" if cert.get("italic_issuer", False) else ""
        iss_size = f"font-size: {cert.get('issuer_size', 10)}pt;"
        issuer_html = f'<div class="entry-subtitle" style="{iss_bold} {iss_italic} {iss_size}">{issuer_str}</div>' if issuer_str else ""

        link_html = f'<div class="entry-meta"><a href="{url_str}" target="_blank">{label_str} &rarr;</a></div>' if url_str else ""
        summary_html = f'<p>{summary_str}</p>' if summary_str else ""

        if title_html or issuer_html or date_html or summary_html or link_html:
            sec_html += f'''
            <div class="entry">
                <div class="entry-header">
                    {title_html}
                    {date_html}
                </div>
                {issuer_html}
                {link_html}
                {summary_html}
            </div>
            '''
    return sec_html

def render_single_section(sec_name, sections_data, layout_mode="Two Columns", custom_sections=None, custom_section_types=None):
    sec_html = ""
    custom_sections = custom_sections or []
    custom_section_types = custom_section_types or {}

    if sec_name == "Profiles & Links" and sections_data.get("Profiles & Links"):
        links = sections_data["Profiles & Links"]
        sec_html += f'<div class="section"><h2>{t("profiles_links")}</h2><div class="social-links">'
        if links.get("GitHub"):
            sec_html += f'<a href="{links["GitHub"]}" target="_blank"><i class="fab fa-github"></i> GitHub</a>'
        if links.get("LinkedIn"):
            sec_html += f'<a href="{links["LinkedIn"]}" target="_blank"><i class="fab fa-linkedin"></i> LinkedIn</a>'
        if links.get("Portfolio"):
            sec_html += f'<a href="{links["Portfolio"]}" target="_blank"><i class="fas fa-globe"></i> Portfolio</a>'
        sec_html += '</div></div>'

    elif sec_name == "Technical Skills" and sections_data.get("Technical Skills"):
        sec_html += f'<div class="section"><h2>{t("tech_skills")}</h2>'
        for item in sections_data["Technical Skills"]:
            name = TextFormatter.format_html_for_pdf(item.get("name", ""))
            desc = TextFormatter.format_html_for_pdf(item.get("description", ""))
            kw = TextFormatter.format_html_for_pdf(item.get("keywords", ""))
            sec_html += f'''
            <div class="entry">
                <div class="entry-title">{name}</div>
                <div class="entry-subtitle">{desc}</div>
                <p style="font-size: 9pt; color: #555;">{kw}</p>
            </div>
            '''
        sec_html += '</div>'

    elif sec_name == "Soft Skills" and sections_data.get("Soft Skills"):
        sec_html += f'<div class="section"><h2>{t("soft_skills")}</h2>'
        for item in sections_data["Soft Skills"]:
            name = TextFormatter.format_html_for_pdf(item.get("name", ""))
            desc = TextFormatter.format_html_for_pdf(item.get("description", ""))
            kw = TextFormatter.format_html_for_pdf(item.get("keywords", ""))
            sec_html += f'''
            <div class="entry">
                <div class="entry-title">{name}</div>
                <div class="entry-subtitle">{desc}</div>
                <p style="font-size: 9pt; color: #555;">{kw}</p>
            </div>
            '''
        sec_html += '</div>'

    elif sec_name == "Strengths" and sections_data.get("Strengths"):
        sec_html += f'<div class="section"><h2>{t("strengths")}</h2>'
        for item in sections_data["Strengths"]:
            name = TextFormatter.format_html_for_pdf(item.get("name", ""))
            desc = TextFormatter.format_html_for_pdf(item.get("description", ""))
            kw = TextFormatter.format_html_for_pdf(item.get("keywords", ""))
            sec_html += f'''
            <div class="entry">
                <div class="entry-title">{name}</div>
                <div class="entry-subtitle">{desc}</div>
                <p style="font-size: 9pt; color: #555;">{kw}</p>
            </div>
            '''
        sec_html += '</div>'

    elif sec_name == "Interests" and sections_data.get("Interests"):
        sec_html += f'<div class="section"><h2>{t("interests")}</h2>'
        for item in sections_data["Interests"]:
            name = TextFormatter.format_html_for_pdf(item.get("name", ""))
            desc = TextFormatter.format_html_for_pdf(item.get("description", ""))
            kw = TextFormatter.format_html_for_pdf(item.get("keywords", ""))
            sec_html += f'''
            <div class="entry">
                <div class="entry-title">{name}</div>
                <div class="entry-subtitle">{desc}</div>
                <p style="font-size: 9pt; color: #555;">{kw}</p>
            </div>
            '''
        sec_html += '</div>'

    elif sec_name == "Experience" and sections_data.get("Experience"):
        sec_html += f'<div class="section"><h2>{t("experience")}</h2>{render_experience_items(sections_data["Experience"])}</div>'

    elif sec_name == "Education" and sections_data.get("Education"):
        sec_html += f'<div class="section"><h2>{t("education")}</h2>'
        for edu in sections_data["Education"]:
            formatted_highlights = TextFormatter.format_html_for_pdf(edu.get("highlights", ""))
            gpa_block = f"<div class='entry-meta'>GPA: {edu.get('gpa', '')}</div>" if edu.get("gpa") else ""
            high_block = f"<p>{formatted_highlights}</p>" if formatted_highlights else ""

            sch_bold = "font-weight: bold;" if edu.get("bold_school", False) else ""
            sch_italic = "font-style: italic;" if edu.get("italic_school", False) else ""
            sch_size = f"font-size: {edu.get('school_size', 10)}pt;"
            school_html = f'<div class="entry-subtitle" style="{sch_bold} {sch_italic} {sch_size}">{edu.get("school", "")}</div>'

            sec_html += f'''
            <div class="entry">
                <div class="entry-header">
                    <span class="entry-title">{edu.get("degree", "")}</span>
                    <span class="entry-meta">{edu.get("graduation", "")}</span>
                </div>
                {school_html}
                {gpa_block}
                {high_block}
            </div>
            '''
        sec_html += '</div>'

    elif sec_name == "Projects" and sections_data.get("Projects"):
        sec_html += f'<div class="section"><h2>{t("projects")}</h2>'
        for proj in sections_data["Projects"]:
            name = TextFormatter.format_html_for_pdf(proj.get("name", ""))
            desc = TextFormatter.format_html_for_pdf(proj.get("description", ""))
            date_range = proj.get("date_range", "")
            website = proj.get("website", "")
            summary = TextFormatter.format_html_for_pdf(proj.get("summary", ""))

            link_block = f"<a href='{website}' target='_blank'>Website &rarr;</a>" if website else ""
            sec_html += f'''
            <div class="entry">
                <div class="entry-header">
                    <span class="entry-title">{name}</span>
                    <span class="entry-meta">{date_range}</span>
                </div>
                <div class="entry-subtitle">{desc}</div>
                <p>{summary}</p>
                {link_block}
            </div>
            '''
        sec_html += '</div>'

    elif sec_name == "Certifications" and sections_data.get("Certifications"):
        sec_html += f'<div class="section"><h2>{t("certifications")}</h2>{render_certification_items(sections_data["Certifications"])}</div>'

    elif sec_name == "Awards" and sections_data.get("Awards"):
        sec_html += f'<div class="section"><h2>{t("awards")}</h2>'
        for awd in sections_data["Awards"]:
            title = TextFormatter.format_html_for_pdf(awd.get("title", ""))
            awarder = TextFormatter.format_html_for_pdf(awd.get("awarder", ""))
            date = awd.get("date", "")
            url = awd.get("url", "")
            link_block = f"<a href='{url}' target='_blank'>Website &rarr;</a>" if url else ""
            sec_html += f'''
            <div class="entry">
                <div class="entry-header">
                    <span class="entry-title">{title}</span>
                    <span class="entry-meta">{date}</span>
                </div>
                <div class="entry-subtitle">{awarder}</div>
                {link_block}
            </div>
            '''
        sec_html += '</div>'

    elif sec_name == "Languages" and sections_data.get("Languages"):
        sec_html += f'<div class="section"><h2>{t("languages")}</h2>'
        for lang in sections_data["Languages"]:
            name = TextFormatter.format_html_for_pdf(lang.get("name", ""))
            desc = TextFormatter.format_html_for_pdf(lang.get("description", ""))
            sec_html += f'<p><strong>{name}:</strong> {desc}</p>'
        sec_html += '</div>'

    elif sec_name in custom_sections and sections_data.get(sec_name):
        sec_type = custom_section_types.get(sec_name, "Generic Text")
        custom_val = sections_data[sec_name]

        sec_html += f'<div class="section"><h2>{sec_name}</h2>'
        if sec_type == "Experience Layout" and isinstance(custom_val, list):
            sec_html += render_experience_items(custom_val)
        elif sec_type == "Certification Layout" and isinstance(custom_val, list):
            sec_html += render_certification_items(custom_val)
        elif sec_type == "Summary Layout":
            formatted_summary = TextFormatter.format_html_for_pdf(str(custom_val))
            sec_html += f'<div class="summary">{formatted_summary}</div>'
        else:
            formatted_custom = TextFormatter.format_html_for_pdf(str(custom_val))
            sec_html += f'<p>{formatted_custom}</p>'
        sec_html += '</div>'

    return sec_html

def generate_cv_html(cv_data, template_config, photo_settings, sidebar_width_pct=32, sidebar_position="Right", layout_mode="Two Columns", primary_color=None, accent_color=None, font_family=None, heading_size=13, body_size=10, line_height=1.4, margin_size=12):
    formatted_summary = TextFormatter.format_html_for_pdf(cv_data.get("summary", ""))
    full_name = cv_data.get("full_name", "")
    title_str = cv_data.get("title", "")
    location_str = cv_data.get("location", "")
    phone_str = cv_data.get("phone", "")
    email_str = cv_data.get("email", "")
    residency_str = cv_data.get("residency", "")
    relocation_str = cv_data.get("relocation", "")

    primary_color = primary_color or template_config["primary_color"]
    accent_color = accent_color or template_config["accent"]
    font_family = font_family or template_config["font"]

    main_html = ""
    sidebar_html = ""

    for sec in st.session_state.section_order:
        if st.session_state.section_visibility.get(sec, True):
            rendered = render_single_section(
                sec,
                cv_data.get("sections_data", {}),
                layout_mode=layout_mode,
                custom_sections=cv_data.get("custom_sections", []),
                custom_section_types=cv_data.get("custom_section_types", {})
            )
            if layout_mode == "Single Column":
                main_html += rendered
            else:
                placement = st.session_state.section_placement.get(sec, "Main Column")
                if placement == "Sidebar":
                    sidebar_html += rendered
                else:
                    main_html += rendered

    is_two_column = (layout_mode == "Two Columns")
    main_width_pct = 100 - sidebar_width_pct if is_two_column else 100
    flex_direction = "row-reverse" if sidebar_position == "Left" else "row"

    photo_html = f'<img src="{photo_b64}" class="profile-photo" />' if photo_b64 else ''
    meta_extra = f'<br/>{residency_str} | {relocation_str}' if (residency_str or relocation_str) else ''
    summary_html = f'<div class="summary">{formatted_summary}</div>' if formatted_summary else ''
    side_col_html = f'<div class="side-col">{sidebar_html}</div>' if (is_two_column and sidebar_html) else ''

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        @page {{ size: A4 portrait; margin: {margin_size}mm; }}
        body {{ font-family: '{font_family}', sans-serif; color: #333333; line-height: {line_height}; font-size: {body_size}pt; background: white; }}
        .header {{ border-bottom: 3px solid {primary_color}; padding-bottom: 15px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: flex-start; gap: 20px; }}
        .header-info {{ flex: 1; }}
        .header-info h1 {{ font-size: {heading_size + 6}pt; color: {primary_color}; margin-bottom: 5px; text-transform: uppercase; letter-spacing: 1px; }}
        .header-info .title {{ font-size: {body_size + 2}pt; color: {accent_color}; font-weight: bold; margin-bottom: 5px; }}
        .header-info .meta {{ font-size: {body_size - 1}pt; color: #666; line-height: 1.5; }}
        .profile-photo {{ width: {photo_settings['width']}px; height: {photo_settings['height']}px; object-fit: cover; object-position: {photo_settings['offset_x']}% {photo_settings['offset_y']}%; border: 2px solid {primary_color}; border-radius: {photo_settings['border_radius']}; flex-shrink: 0; }}
        .summary {{ font-size: {body_size}pt; margin-bottom: 20px; line-height: 1.6; color: #333; }}
        .layout-container {{ display: flex; flex-direction: {flex_direction}; gap: 20px; width: 100%; }}
        .main-col {{ width: {main_width_pct}%; }}
        .side-col {{ width: {sidebar_width_pct}%; background-color: {template_config["sidebar_bg"]}; padding: 12px; border-radius: 6px; }}
        .section {{ margin-bottom: 20px; page-break-inside: avoid; }}
        .section h2 {{ font-size: {heading_size}pt; color: {primary_color}; border-bottom: 2px solid {accent_color}; padding-bottom: 4px; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 0.5px; }}
        .entry {{ margin-bottom: 12px; }}
        .entry-header {{ display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 4px; }}
        .entry-title {{ font-weight: bold; font-size: {body_size + 1}pt; color: #000; }}
        .entry-subtitle {{ font-size: {body_size - 1}pt; color: #666; }}
        .entry-meta {{ font-size: {body_size - 1}pt; color: #888; }}
        ul {{ margin-left: 20px; margin-bottom: 8px; }}
        li {{ margin-bottom: 3px; }}
        code {{ background: #f4f4f4; padding: 2px 4px; border-radius: 3px; font-family: monospace; }}
        .social-links {{ display: flex; flex-direction: column; gap: 6px; margin-bottom: 10px; font-size: {body_size}pt; }}
        .social-links a {{ color: {primary_color}; text-decoration: none; }}
    </style>
    </head>
    <body>
        <div class="header">
            <div class="header-info">
                <h1>{full_name}</h1>
                <div class="title">{title_str}</div>
                <div class="meta">{location_str} | {phone_str} | {email_str}{meta_extra}</div>
            </div>
            {photo_html}
        </div>
        {summary_html}
        <div class="layout-container">
            <div class="main-col">{main_html}</div>
            {side_col_html}
        </div>
    </body>
    </html>
    """
    return html

def render_pdf_preview(pdf_bytes: bytes):
    try:
        doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")
        st.write(f"**{t('preview_pages').format(num=len(doc))}**")
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            pix = page.get_pixmap(dpi=120)
            img_bytes = pix.tobytes("png")
            st.image(img_bytes, caption=f"Page {page_num + 1}", use_container_width=True)
    except Exception as e:
        st.warning(f"Could not render visual preview: {e}")

# ============================================================================
# TWO-COLUMN SPLIT WITH INDEPENDENT SCROLL CONTAINERS
# ============================================================================

col_edit_area, col_prev = st.columns([1.2, 1])

with col_edit_area:
    with st.container(height=800, border=False):
        st.title(t("personal_info"))
        cv_data = st.session_state.cv_data

        col1, col2, col3 = st.columns(3)

        with col1:
            full_name = st.text_input(t("full_name"), cv_data.get("full_name", ""), placeholder="John Doe")
            title = st.text_input(t("professional_title"), cv_data.get("title", ""), placeholder="Software Engineer")
            phone = st.text_input(t("phone"), cv_data.get("phone", ""), placeholder="+1 234 567 8900")
            if phone and not validate_phone(phone):
                st.warning(t("phone_warning"))

        with col2:
            email = st.text_input(t("email"), cv_data.get("email", ""), placeholder="your@email.com")
            if email and not validate_email(email):
                st.error(t("email_error"))

            location = st.text_input(t("location"), cv_data.get("location", ""), placeholder="City, Country")
            residency = st.text_input(t("residency"), cv_data.get("residency", ""))

        with col3:
            relocation = st.text_input(t("relocation"), cv_data.get("relocation", ""), placeholder="Open to relocation")
            linkedin_url = st.text_input(t("linkedin_profile"), cv_data.get("linkedin_url", ""), placeholder="https://linkedin.com/in/...")

            if linkedin_url and not validate_url(linkedin_url):
                st.warning(t("url_warning"))

        summary = st.text_area(t("summary"), cv_data.get("summary", ""), height=100, placeholder="Brief overview...")

        if summary and len(summary) < 50:
            st.warning(t("summary_warning"))

        st.divider()
        st.header(t("cv_content"))

        sections_data = {}
        saved_sec = cv_data.get("sections_data", {})

        # -------- PROFILES & LINKS --------
        with st.expander(t("profiles_links"), expanded=True):
            col_github, col_linkedin_s, col_portfolio = st.columns(3)
            with col_github:
                github = st.text_input(t("github"), saved_sec.get("Profiles & Links", {}).get("GitHub", ""), placeholder="https://github.com/...")
            with col_linkedin_s:
                linkedin = st.text_input(t("linkedin"), saved_sec.get("Profiles & Links", {}).get("LinkedIn", ""), placeholder="https://linkedin.com/in/...")
            with col_portfolio:
                portfolio = st.text_input(t("portfolio"), saved_sec.get("Profiles & Links", {}).get("Portfolio", ""), placeholder="https://...")

            sections_data["Profiles & Links"] = {"GitHub": github, "LinkedIn": linkedin, "Portfolio": portfolio}

        # -------- TECHNICAL SKILLS --------
        with st.expander(t("tech_skills")):
            num_tech = int(st.number_input(t("num_tech"), 0, 10, len(saved_sec.get("Technical Skills", [])) if isinstance(saved_sec.get("Technical Skills"), list) else 1))
            tech_items = []
            for i in range(num_tech):
                item_data = saved_sec.get("Technical Skills", [])[i] if isinstance(saved_sec.get("Technical Skills"), list) and i < len(saved_sec.get("Technical Skills", [])) else {}
                c_name, c_desc = st.columns(2)
                with c_name:
                    t_name = st.text_input(t("name"), key=f"tech_name_{i}", value=item_data.get("name", ""))
                with c_desc:
                    t_desc = st.text_input(t("description"), key=f"tech_desc_{i}", value=item_data.get("description", ""))
                t_keywords = st.text_area(t("keywords"), key=f"tech_keywords_{i}", value=item_data.get("keywords", ""), height=60)
                if t_name or t_keywords:
                    tech_items.append({"name": t_name, "description": t_desc, "keywords": t_keywords})
                st.divider()
            sections_data["Technical Skills"] = tech_items

        # -------- SOFT SKILLS --------
        with st.expander(t("soft_skills")):
            num_soft = int(st.number_input(t("num_soft"), 0, 10, len(saved_sec.get("Soft Skills", [])) if isinstance(saved_sec.get("Soft Skills"), list) else 1))
            soft_items = []
            for i in range(num_soft):
                item_data = saved_sec.get("Soft Skills", [])[i] if isinstance(saved_sec.get("Soft Skills"), list) and i < len(saved_sec.get("Soft Skills", [])) else {}
                c_name, c_desc = st.columns(2)
                with c_name:
                    s_name = st.text_input(t("name"), key=f"soft_name_{i}", value=item_data.get("name", ""))
                with c_desc:
                    s_desc = st.text_input(t("description"), key=f"soft_desc_{i}", value=item_data.get("description", ""))
                s_keywords = st.text_area(t("keywords"), key=f"soft_keywords_{i}", value=item_data.get("keywords", ""), height=60)
                if s_name or s_keywords:
                    soft_items.append({"name": s_name, "description": s_desc, "keywords": s_keywords})
                st.divider()
            sections_data["Soft Skills"] = soft_items

        # -------- STRENGTHS --------
        with st.expander(t("strengths")):
            num_strengths = int(st.number_input(t("num_strengths"), 0, 10, len(saved_sec.get("Strengths", [])) if isinstance(saved_sec.get("Strengths"), list) else 0))
            strength_items = []
            for i in range(num_strengths):
                item_data = saved_sec.get("Strengths", [])[i] if isinstance(saved_sec.get("Strengths", []), list) and i < len(saved_sec.get("Strengths", [])) else {}
                c_name, c_desc = st.columns(2)
                with c_name:
                    str_name = st.text_input(t("name"), key=f"strength_name_{i}", value=item_data.get("name", ""))
                with c_desc:
                    str_desc = st.text_input(t("description"), key=f"strength_desc_{i}", value=item_data.get("description", ""))
                str_keywords = st.text_area(t("keywords"), key=f"strength_keywords_{i}", value=item_data.get("keywords", ""), height=60)
                if str_name or str_keywords:
                    strength_items.append({"name": str_name, "description": str_desc, "keywords": str_keywords})
                st.divider()
            sections_data["Strengths"] = strength_items

        # -------- INTERESTS --------
        with st.expander(t("interests")):
            num_interests = int(st.number_input(t("num_interests"), 0, 10, len(saved_sec.get("Interests", [])) if isinstance(saved_sec.get("Interests", list), list) else 0))
            interest_items = []
            for i in range(num_interests):
                item_data = saved_sec.get("Interests", [])[i] if isinstance(saved_sec.get("Interests", []), list) and i < len(saved_sec.get("Interests", [])) else {}
                c_name, c_desc = st.columns(2)
                with c_name:
                    int_name = st.text_input(t("name"), key=f"interest_name_{i}", value=item_data.get("name", ""))
                with c_desc:
                    int_desc = st.text_input(t("description"), key=f"interest_desc_{i}", value=item_data.get("description", ""))
                int_keywords = st.text_area(t("keywords"), key=f"interest_keywords_{i}", value=item_data.get("keywords", ""), height=60)
                if int_name or int_keywords:
                    interest_items.append({"name": int_name, "description": int_desc, "keywords": int_keywords})
                st.divider()
            sections_data["Interests"] = interest_items

        # -------- CERTIFICATIONS --------
        with st.expander(t("certifications")):
            num_certs = int(st.number_input(t("num_certs"), 0, 10, len(saved_sec.get("Certifications", [])) if isinstance(saved_sec.get("Certifications", list), list) else 0))
            certs = []
            for i in range(num_certs):
                cert_data = saved_sec.get("Certifications", [])[i] if isinstance(saved_sec.get("Certifications", []), list) and i < len(saved_sec.get("Certifications", [])) else {}
                col_title, col_issuer, col_date = st.columns([2, 2, 1])
                with col_title:
                    title_val = st.text_input(t("name"), key=f"cert_title_{i}", value=cert_data.get("title", ""))
                with col_issuer:
                    issuer_val = st.text_input(t("issuer"), key=f"cert_issuer_{i}", value=cert_data.get("issuer", ""))
                with col_date:
                    date_val = st.text_input(t("date"), key=f"cert_date_{i}", value=cert_data.get("date", ""))

                col_i_bold, col_i_italic, col_i_size = st.columns(3)
                with col_i_bold:
                    bold_issuer = st.checkbox("Bold Issuer", key=f"cert_bold_issuer_{i}", value=cert_data.get("bold_issuer", False))
                with col_i_italic:
                    italic_issuer = st.checkbox("Italic Issuer", key=f"cert_italic_issuer_{i}", value=cert_data.get("italic_issuer", True))
                with col_i_size:
                    issuer_size = st.slider("Issuer Size (pt)", 8, 16, cert_data.get("issuer_size", 10), key=f"cert_size_issuer_{i}")

                col_url, col_label = st.columns([2, 1])
                with col_url:
                    url_val = st.text_input(t("website_url"), key=f"cert_url_{i}", value=cert_data.get("url", ""))
                with col_label:
                    label_val = st.text_input(t("link_label"), key=f"cert_label_{i}", value=cert_data.get("label", t("view_credentials")))
                summary_val = st.text_area(t("summary"), key=f"cert_summary_{i}", value=cert_data.get("summary", ""), height=60)
                if title_val or issuer_val or url_val:
                    certs.append({
                        "title": title_val, "issuer": issuer_val, "date": date_val, "url": url_val,
                        "label": label_val, "summary": summary_val,
                        "bold_issuer": bold_issuer, "italic_issuer": italic_issuer, "issuer_size": issuer_size
                    })
                st.divider()
            sections_data["Certifications"] = certs

        # -------- AWARDS --------
        with st.expander(t("awards")):
            num_awards = int(st.number_input(t("num_awards"), 0, 10, len(saved_sec.get("Awards", [])) if isinstance(saved_sec.get("Awards", list), list) else 0))
            awards = []
            for i in range(num_awards):
                award_data = saved_sec.get("Awards", [])[i] if isinstance(saved_sec.get("Awards", []), list) and i < len(saved_sec.get("Awards", [])) else {}
                col_title, col_awarder = st.columns(2)
                with col_title:
                    a_title = st.text_input(t("name"), key=f"award_title_{i}", value=award_data.get("title", ""))
                with col_awarder:
                    a_awarder = st.text_input(t("awarder"), key=f"award_awarder_{i}", value=award_data.get("awarder", ""))
                col_date, col_url = st.columns(2)
                with col_date:
                    a_date = st.text_input(t("date"), key=f"award_date_{i}", value=award_data.get("date", ""))
                with col_url:
                    a_url = st.text_input(t("website_url"), key=f"award_url_{i}", value=award_data.get("url", ""))
                if a_title or a_awarder:
                    awards.append({"title": a_title, "awarder": a_awarder, "date": a_date, "url": a_url})
                st.divider()
            sections_data["Awards"] = awards

        # -------- LANGUAGES --------
        with st.expander(t("languages")):
            num_langs = int(st.number_input(t("num_langs"), 0, 10, len(saved_sec.get("Languages", [])) if isinstance(saved_sec.get("Languages", list), list) else 0))
            langs = []
            for i in range(num_langs):
                lang_data = saved_sec.get("Languages", [])[i] if isinstance(saved_sec.get("Languages", []), list) and i < len(saved_sec.get("Languages", [])) else {}
                col_name, col_desc = st.columns(2)
                with col_name:
                    name_val = st.text_input(t("name"), key=f"lang_name_{i}", value=lang_data.get("name", ""))
                with col_desc:
                    desc_val = st.text_input(t("description"), key=f"lang_desc_{i}", value=lang_data.get("description", ""))
                if name_val:
                    langs.append({"name": name_val, "description": desc_val})
                st.divider()
            sections_data["Languages"] = langs

        # -------- EXPERIENCE --------
        with st.expander(t("experience")):
            num_exp = int(st.number_input(t("num_exp"), 0, 10, len(saved_sec.get("Experience", [])) if isinstance(saved_sec.get("Experience", list), list) else 1))
            experiences = []
            for i in range(num_exp):
                exp_data = saved_sec.get("Experience", [])[i] if isinstance(saved_sec.get("Experience", []), list) and i < len(saved_sec.get("Experience", [])) else {}
                col_company, col_title = st.columns(2)
                with col_company:
                    company = st.text_input(t("company_name"), key=f"exp_company_{i}", value=exp_data.get("company", ""))
                with col_title:
                    job_title = st.text_input(t("position_title"), key=f"exp_title_{i}", value=exp_data.get("title", ""))

                col_c_bold, col_c_italic, col_c_size = st.columns(3)
                with col_c_bold:
                    bold_company = st.checkbox("Bold Company", key=f"exp_bold_comp_{i}", value=exp_data.get("bold_company", False))
                with col_c_italic:
                    italic_company = st.checkbox("Italic Company", key=f"exp_italic_comp_{i}", value=exp_data.get("italic_company", True))
                with col_c_size:
                    company_size = st.slider("Company Size (pt)", 8, 16, exp_data.get("company_size", 10), key=f"exp_size_comp_{i}")

                col_date, col_loc = st.columns(2)
                with col_date:
                    date_range = st.text_input(t("date_range"), key=f"exp_date_{i}", value=exp_data.get("date_range", ""))
                with col_loc:
                    exp_location = st.text_input(t("location"), key=f"exp_location_{i}", value=exp_data.get("location", ""))
                col_url, col_label = st.columns([2, 1])
                with col_url:
                    exp_website = st.text_input(t("website_url"), key=f"exp_url_{i}", value=exp_data.get("website", ""))
                with col_label:
                    exp_link_label = st.text_input(t("link_label"), key=f"exp_link_label_{i}", value=exp_data.get("link_label", t("visit_website")))
                exp_summary = st.text_area(t("summary"), key=f"exp_summary_{i}", value=exp_data.get("summary", ""), height=60, placeholder=t("summary_placeholder"))
                bullets = exp_data.get("bullets", [])
                if isinstance(bullets, str): bullets = [bullets]
                bullets_input = st.text_area(t("achievements"), key=f"exp_bullets_{i}", value="\n".join(bullets), height=80)
                bullets_list = [b.strip() for b in bullets_input.split("\n") if b.strip()]
                if company or job_title or exp_summary or bullets_list:
                    experiences.append({
                        "company": company, "title": job_title, "date_range": date_range,
                        "location": exp_location, "website": exp_website, "link_label": exp_link_label,
                        "summary": exp_summary, "bullets": bullets_list,
                        "bold_company": bold_company, "italic_company": italic_company, "company_size": company_size
                    })
                st.divider()
            sections_data["Experience"] = experiences

        # -------- EDUCATION --------
        with st.expander(t("education")):
            num_edu = int(st.number_input(t("num_edu"), 0, 10, len(saved_sec.get("Education", [])) if isinstance(saved_sec.get("Education", list), list) else 1))
            educations = []
            for i in range(num_edu):
                edu_data = saved_sec.get("Education", [])[i] if isinstance(saved_sec.get("Education", []), list) and i < len(saved_sec.get("Education", [])) else {}
                col_degree, col_school = st.columns(2)
                with col_degree:
                    degree = st.text_input(t("position_title"), key=f"edu_degree_{i}", value=edu_data.get("degree", ""))
                with col_school:
                    school = st.text_input(t("school"), key=f"edu_school_{i}", value=edu_data.get("school", ""))

                col_s_bold, col_s_italic, col_s_size = st.columns(3)
                with col_s_bold:
                    bold_school = st.checkbox("Bold School", key=f"edu_bold_school_{i}", value=edu_data.get("bold_school", False))
                with col_s_italic:
                    italic_school = st.checkbox("Italic School", key=f"edu_italic_school_{i}", value=edu_data.get("italic_school", True))
                with col_s_size:
                    school_size = st.slider("School Size (pt)", 8, 16, edu_data.get("school_size", 10), key=f"edu_size_school_{i}")

                col_grad_start, col_grad_end = st.columns(2)
                with col_grad_start:
                    graduation = st.text_input(t("graduation_date"), key=f"edu_grad_{i}", value=edu_data.get("graduation", ""))
                with col_grad_end:
                    gpa = st.text_input(t("gpa"), key=f"edu_gpa_{i}", value=edu_data.get("gpa", ""))
                highlights = st.text_area(t("highlights"), key=f"edu_highlights_{i}", value=edu_data.get("highlights", ""), height=60)
                if degree or school:
                    educations.append({
                        "degree": degree, "school": school, "graduation": graduation,
                        "gpa": gpa, "highlights": highlights,
                        "bold_school": bold_school, "italic_school": italic_school, "school_size": school_size
                    })
                st.divider()
            sections_data["Education"] = educations

        # -------- PROJECTS --------
        with st.expander(t("projects")):
            num_projects = int(st.number_input(t("num_projects"), 0, 10, len(saved_sec.get("Projects", [])) if isinstance(saved_sec.get("Projects", list), list) else 0))
            projects = []
            for i in range(num_projects):
                proj_data = saved_sec.get("Projects", [])[i] if isinstance(saved_sec.get("Projects", []), list) and i < len(saved_sec.get("Projects", [])) else {}
                proj_name = st.text_input(t("project_name"), key=f"proj_name_{i}", value=proj_data.get("name", ""))
                proj_desc = st.text_area(t("project_desc"), key=f"proj_desc_{i}", value=proj_data.get("description", ""), height=60)
                proj_date = st.text_input(t("date_range"), key=f"proj_date_{i}", value=proj_data.get("date_range", ""))
                col_url, col_label = st.columns([2, 1])
                with col_url:
                    proj_website = st.text_input(t("website_url"), key=f"proj_website_{i}", value=proj_data.get("website", ""))
                with col_label:
                    proj_link_label = st.text_input(t("link_label"), key=f"proj_link_label_{i}", value=proj_data.get("link_label", t("view_project")))
                proj_summary = st.text_area(t("summary"), key=f"proj_summary_{i}", value=proj_data.get("summary", ""), height=60)
                if proj_name or proj_desc:
                    projects.append({"name": proj_name, "description": proj_desc, "date_range": proj_date, "website": proj_website, "link_label": proj_link_label, "summary": proj_summary})
                st.divider()
            sections_data["Projects"] = projects

        # -------- CUSTOM SECTIONS --------
        for custom_sec in st.session_state.custom_sections:
            sec_type = st.session_state.custom_section_types.get(custom_sec, "Generic Text")
            saved_custom_val = saved_sec.get(custom_sec, [])
            with st.expander(f"📌 {custom_sec} ({sec_type})"):
                c_val = st.text_area(f"{custom_sec} Content", value=str(saved_custom_val) if isinstance(saved_custom_val, str) else "", key=f"custom_sec_{custom_sec}", height=100)
                sections_data[custom_sec] = c_val

        cv_data.update({
            "full_name": full_name, "title": title, "email": email, "phone": phone,
            "location": location, "residency": residency, "relocation": relocation,
            "linkedin_url": linkedin_url, "summary": summary, "sections_data": sections_data,
            "custom_sections": st.session_state.custom_sections, "custom_section_types": st.session_state.custom_section_types,
            "section_visibility": st.session_state.section_visibility, "section_placement": st.session_state.section_placement,
            "section_order": st.session_state.section_order
        })
        st.session_state.cv_data = cv_data
        safe_filename = full_name.replace(' ', '_') if full_name else "My"

        # ------------------------------------------------------------------------
        # CV ANALYSIS & EXPORT OPTIONS
        # ------------------------------------------------------------------------
        st.divider()
        st.header(t("analysis_export"))

        col_score, col_ai = st.columns([1, 1])
        with col_score:
            score, suggestions = get_cv_score(cv_data)
            color = "🟢" if score >= 80 else "🟡" if score >= 60 else "🔴"
            st.metric(t("completeness_score"), f"{score}/100", f"{color}")
            with st.expander(t("improvement_suggestions")):
                for suggestion in suggestions:
                    st.write(suggestion)

        with col_ai:
            if st.button(t("btn_ai_general"), use_container_width=True):
                with st.spinner("Analyzing..."):
                    st.session_state.ai_general_text = get_cv_enhancement_suggestions(cv_data)
                    st.session_state.show_ai_suggestions = True
            if st.session_state.show_ai_suggestions and "ai_general_text" in st.session_state:
                with st.expander(t("general_ai_suggestions"), expanded=True):
                    st.info(st.session_state.ai_general_text)

        # ------------------------------------------------------------------------
        # JOB-TARGETED AI CUSTOMIZATION
        # ------------------------------------------------------------------------
        st.markdown("---")
        st.subheader(t("job_matching"))

        with st.container():
            job_desc_input = st.text_area(
                t("paste_job_desc"),
                height=140,
                placeholder="Paste full job description here...",
                key="unique_job_desc_input_box"
            )

        if st.button(t("btn_analyze_job"), use_container_width=True):
            if not job_desc_input.strip():
                st.warning("⚠️ Please paste a job description first.")
            else:
                with st.spinner("Comparing..."):
                    st.session_state.job_tailored_analysis = get_job_tailored_suggestions(cv_data, job_desc_input)
                    st.session_state.show_job_match = True

        if st.session_state.get("show_job_match", False) and "job_tailored_analysis" in st.session_state:
            with st.expander(t("tailored_recommendations"), expanded=True):
                st.markdown(st.session_state.job_tailored_analysis)

        st.markdown("---")
        st.subheader(t("export_options"))

        selected_template_key = cast(str, st.session_state.selected_template)
        rendered_html = generate_cv_html(
            cv_data, CV_TEMPLATES[selected_template_key], photo_settings,
            sidebar_width_pct=sidebar_width_pct if layout_mode == "Two Columns" else 32,
            sidebar_position=sidebar_position if layout_mode == "Two Columns" else "Right",
            layout_mode=layout_mode, primary_color=primary_color, accent_color=accent_color,
            font_family=font_family, heading_size=heading_size, body_size=body_size,
            line_height=line_height, margin_size=margin_size
        )
        pdf_bytes = HTML(string=rendered_html).write_pdf() or b""

        sub_col1, sub_col2 = st.columns(2)
        with sub_col1:
            st.download_button(t("btn_download_pdf"), data=pdf_bytes, file_name=f"{safe_filename}_CV.pdf", mime="application/pdf", use_container_width=True)
        with sub_col2:
            st.download_button(t("btn_download_json"), data=json.dumps(cv_data, indent=2), file_name=f"{safe_filename}_CV_data.json", mime="application/json", use_container_width=True)

        with st.popover(t("save_version"), use_container_width=True):
            version_input = st.text_input(t("version_tag"), value=f"{safe_filename}_{st.session_state.get('selected_template', 'default')}")
            if st.button(t("confirm_save"), use_container_width=True):
                save_version(cv_data, version_input)
                st.success("✅ Saved!")

# 2. Right Column Scrollable Viewport
with col_prev:
    with st.container(height=800, border=False):
        st.subheader(t("live_preview"))
        render_pdf_preview(pdf_bytes)

# ============================================================================
# FOOTER
# ============================================================================
st.divider()
st.caption(t("pro_tips"))