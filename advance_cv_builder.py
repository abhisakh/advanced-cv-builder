"""
Advanced CV Builder with AI Enhancement, Job Matcher, Built-in Text Formatter,
Multiple Templates & Dynamic Custom Section Types
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
# BUILT-IN TEXT FORMATTER
# ============================================================================

class TextFormatter:
    """Parses lightweight markdown syntax into standard HTML tags for PDF rendering."""

    @staticmethod
    def format_html_for_pdf(text: str) -> str:
        if not text:
            return ""

        text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

        text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)       # **bold**
        text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)                   # *italic*
        text = re.sub(r'__(.*?)__', r'<u>\1</u>', text)                     # __underline__
        text = re.sub(r'~~(.*?)~~', r'<del>\1</del>', text)                 # ~~strikethrough~~
        text = re.sub(r'\^(.*?)\^', r'<sup>\1</sup>', text)                 # ^superscript^
        text = re.sub(r'~(.*?)~', r'<sub>\1</sub>', text)                   # ~subscript~
        text = re.sub(r'`(.*?)`', r'<code>\1</code>', text)                 # `code`

        return text

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
    """Analyzes CV data against a provided job description to generate targeted recommendations."""
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
    page_title="Advanced CV Builder",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
    <style>
    /* 1. Prevent global window scrollbar */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"], .main .block-container {
        height: 100vh !important;
        overflow: hidden !important;
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
        max-width: 100% !important;
    }

    /* 2. Set horizontal column container height */
    [data-testid="stHorizontalBlock"] {
        height: calc(100vh - 2.5rem) !important;
        align-items: stretch !important;
        gap: 1.5rem !important;
    }

    /* 3. Force columns to inherit full height */
    [data-testid="stHorizontalBlock"] > [data-testid="column"] {
        height: 100% !important;
        min-height: 0 !important;
        display: flex !important;
        flex-direction: column !important;
    }

    /* 4. Target Streamlit's inner block wrappers to isolate scrolling & enable flex vertical layout */
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

        /* ADDED: Generous bottom padding so text never crops at the bottom */
        padding-bottom: 5rem !important;
        box-sizing: border-box !important;
    }

    /* 5. Custom scrollbars */
    [data-testid="stHorizontalBlock"] > [data-testid="column"] div::-webkit-scrollbar {
        width: 6px;
    }
    [data-testid="stHorizontalBlock"] > [data-testid="column"] div::-webkit-scrollbar-thumb {
        background-color: #cccccc;
        border-radius: 4px;
    }

    /* 6. Keep expander headers and content strictly contained */
    div[data-testid="stExpander"] {
        height: auto !important;
        min-height: 0 !important;
    }

    /* 7. Tighten internal vertical block spacing */
    [data-testid="stVerticalBlock"] {
        gap: 0.5rem !important;
    }

    /* 8. Bottom Column Footer CSS Rule */
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
# SIDEBAR - PROFILE & TEMPLATE MANAGEMENT
# ============================================================================

st.sidebar.title("🎯 CV Builder Pro")

with st.sidebar.expander("📁 Profile Management", expanded=True):
    saved_files = [f.replace(".json", "") for f in os.listdir(SAVED_PROFILES_DIR) if f.endswith(".json")]

    col_load, col_new = st.columns(2)

    with col_load:
        selected_profile = st.selectbox("Load Profile", ["Default"] + saved_files, key="profile_select")
        if st.button("📂 Load", use_container_width=True):
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
        new_profile_name = st.text_input("New Profile Name", placeholder="My CV")
        if st.button("💾 Save", use_container_width=True):
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
            selected_v_idx = st.selectbox("Restore Saved Version", range(len(version_names)), format_func=lambda x: version_names[x])
            if st.button("⏪ Restore Selected Version", use_container_width=True):
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

with st.sidebar.expander("🎨 Template & Styling", expanded=True):
    st.session_state.selected_template = st.selectbox("Select Template", list(CV_TEMPLATES.keys()))
    selected_tpl = cast(str, st.session_state.selected_template)
    template_config = CV_TEMPLATES[selected_tpl]

    st.divider()
    st.subheader("Customize Colors")
    col_primary, col_accent = st.columns(2)

    with col_primary:
        primary_color = st.color_picker("Primary Color", template_config["primary_color"])
    with col_accent:
        accent_color = st.color_picker("Accent Color", template_config["accent"])

    st.subheader("Typography")
    col_font, col_size = st.columns(2)

    with col_font:
        font_family = st.selectbox("Font Family", ["Helvetica", "Arial", "Georgia", "Times New Roman"])
    with col_size:
        heading_size = st.slider("Heading Size (pt)", 10, 16, 13)

    body_size = st.slider("Body Text Size (pt)", 9, 12, 10)
    line_height = st.slider("Line Height", 1.2, 1.8, 1.4, 0.1)
    margin_size = st.slider("Page Margin (mm)", 8, 20, 12)

    layout_mode = st.radio("Layout Mode", ["Two Columns", "Single Column"])

with st.sidebar.expander("🧩 Layout & Section Control", expanded=False):
    st.caption("Toggle visibility and column layout:")

    if layout_mode == "Two Columns":
        st.subheader("Column Configuration")
        sidebar_position = st.selectbox("Sidebar Position", ["Left", "Right"])
        sidebar_width_pct = st.slider("Sidebar Width (%)", 20, 50, 32)
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
    st.caption("Reorder Section Priority:")
    st.session_state.section_order = st.multiselect(
        "Section Render Order",
        options=available_sections,
        default=st.session_state.section_order
    )

# ============================================================================
# SIDEBAR - PROFILE PHOTO & FRAME OFFSETS
# ============================================================================

with st.sidebar.expander("🖼️ Profile Photo"):
    show_photo = st.checkbox("Include Profile Photo", value=False)
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

    if show_photo:
        uploaded_photo = st.file_uploader("Upload Photo", type=["jpg", "jpeg", "png"])

        col_pos, col_shape = st.columns(2)
        with col_pos:
            photo_settings["position"] = st.selectbox("Position", ["Left Sidebar", "Header Right", "Header Left"])
        with col_shape:
            photo_settings["shape"] = st.selectbox("Shape", ["Circular", "Square", "Rectangular"])

        col_w, col_h = st.columns(2)
        with col_w:
            photo_settings["width"] = st.slider("Width (px)", 80, 180, 100)
        with col_h:
            if photo_settings["shape"] == "Rectangular":
                photo_settings["height"] = st.slider("Height (px)", 80, 220, 130)
            else:
                photo_settings["height"] = photo_settings["width"]

        photo_settings["border_radius"] = "50%" if photo_settings["shape"] == "Circular" else "0px"

        st.subheader("Photo Frame Offsets")
        photo_settings["offset_x"] = st.slider("Horizontal Offset (%)", 0, 100, 50, help="Shifts image horizontally inside the frame")
        photo_settings["offset_y"] = st.slider("Vertical Offset (%)", 0, 100, 50, help="Shifts image vertically inside the frame")

        if uploaded_photo:
            photo_b64 = get_image_base64(uploaded_photo)

# ============================================================================
# SIDEBAR - CUSTOM SECTIONS WITH DROPDOWN TYPE SELECTION
# ============================================================================

with st.sidebar.expander("➕ Custom Sections"):
    new_sec_name = st.text_input("Section Name", placeholder="e.g., Publications")
    sec_type_choice = st.selectbox("Section Type", SECTION_TYPES)

    if st.button("Add Section", use_container_width=True):
        if new_sec_name and new_sec_name not in st.session_state.custom_sections:
            st.session_state.custom_sections.append(new_sec_name)
            st.session_state.custom_section_types[new_sec_name] = sec_type_choice
            st.session_state.section_visibility[new_sec_name] = True
            st.session_state.section_placement[new_sec_name] = "Main Column"
            st.session_state.section_order.append(new_sec_name)
            st.success(f"✅ Added '{new_sec_name}' as {sec_type_choice}")
            st.rerun()

    if st.session_state.custom_sections:
        st.write("**Current Custom Sections:**")
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
        link_label = exp.get("link_label") or "Visit Website"
        date_range = exp.get("date_range", "")
        loc = exp.get("location", "")
        summary = TextFormatter.format_html_for_pdf(exp.get("summary", ""))

        title_html = f'<span class="entry-title">{TextFormatter.format_html_for_pdf(title)}</span>' if title else ""
        date_html = f'<span class="entry-meta">{date_range}</span>' if date_range else ""
        company_html = f'<span class="entry-subtitle">{company}</span>' if company else ""

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
        label_str = cert.get("label") or "View Credentials"
        issuer_str = cert.get("issuer", "")
        date_str = cert.get("date", "")
        summary_str = TextFormatter.format_html_for_pdf(cert.get("summary", ""))

        title_html = f'<span class="entry-title">{title_str}</span>' if title_str else ""
        date_html = f'<span class="entry-meta">{date_str}</span>' if date_str else ""
        issuer_html = f'<div class="entry-subtitle">{issuer_str}</div>' if issuer_str else ""
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

def render_single_section(sec_name, sections_data, layout_mode="Two Columns"):
    sec_html = ""

    if sec_name == "Profiles & Links" and sections_data.get("Profiles & Links"):
        links = sections_data["Profiles & Links"]
        sec_html += '<div class="section"><h2>Profiles & Links</h2><div class="social-links">'
        if links.get("GitHub"):
            sec_html += f'<a href="{links["GitHub"]}" target="_blank"><i class="fab fa-github"></i> GitHub</a>'
        if links.get("LinkedIn"):
            sec_html += f'<a href="{links["LinkedIn"]}" target="_blank"><i class="fab fa-linkedin"></i> LinkedIn</a>'
        if links.get("Portfolio"):
            sec_html += f'<a href="{links["Portfolio"]}" target="_blank"><i class="fas fa-globe"></i> Portfolio</a>'
        sec_html += '</div></div>'

    elif sec_name == "Technical Skills" and sections_data.get("Technical Skills"):
        sec_html += '<div class="section"><h2>Technical Skills</h2>'
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
        sec_html += '<div class="section"><h2>Soft Skills</h2>'
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

    elif sec_name == "Experience" and sections_data.get("Experience"):
        sec_html += f'<div class="section"><h2>Experience</h2>{render_experience_items(sections_data["Experience"])}</div>'

    elif sec_name == "Education" and sections_data.get("Education"):
        sec_html += '<div class="section"><h2>Education</h2>'
        for edu in sections_data["Education"]:
            formatted_highlights = TextFormatter.format_html_for_pdf(edu.get("highlights", ""))
            gpa_block = f"<div class='entry-meta'>GPA: {edu.get('gpa', '')}</div>" if edu.get("gpa") else ""
            high_block = f"<p>{formatted_highlights}</p>" if formatted_highlights else ""
            sec_html += f'''
            <div class="entry">
                <div class="entry-header">
                    <span class="entry-title">{edu.get("degree", "")}</span>
                    <span class="entry-meta">{edu.get("graduation", "")}</span>
                </div>
                <div class="entry-subtitle">{edu.get("school", "")}</div>
                {gpa_block}
                {high_block}
            </div>
            '''
        sec_html += '</div>'

    elif sec_name == "Projects" and sections_data.get("Projects"):
        sec_html += '<div class="section"><h2>Projects</h2>'
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
        sec_html += f'<div class="section"><h2>Certifications</h2>{render_certification_items(sections_data["Certifications"])}</div>'

    elif sec_name == "Awards" and sections_data.get("Awards"):
        sec_html += '<div class="section"><h2>Awards</h2>'
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
        sec_html += '<div class="section"><h2>Languages</h2>'
        for lang in sections_data["Languages"]:
            name = TextFormatter.format_html_for_pdf(lang.get("name", ""))
            desc = TextFormatter.format_html_for_pdf(lang.get("description", ""))
            sec_html += f'<p><strong>{name}:</strong> {desc}</p>'
        sec_html += '</div>'

    elif sec_name in st.session_state.custom_sections and sections_data.get(sec_name):
        sec_type = st.session_state.custom_section_types.get(sec_name, "Generic Text")
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
            rendered = render_single_section(sec, cv_data.get("sections_data", {}), layout_mode=layout_mode)
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

        @page {{
            size: A4 portrait;
            margin: {margin_size}mm;
        }}

        body {{
            font-family: '{font_family}', sans-serif;
            color: #333333;
            line-height: {line_height};
            font-size: {body_size}pt;
            background: white;
        }}

        .header {{
            border-bottom: 3px solid {primary_color};
            padding-bottom: 15px;
            margin-bottom: 20px;
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 20px;
        }}

        .header-info {{ flex: 1; }}
        .header-info h1 {{
            font-size: {heading_size + 6}pt;
            color: {primary_color};
            margin-bottom: 5px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}

        .header-info .title {{
            font-size: {body_size + 2}pt;
            color: {accent_color};
            font-weight: bold;
            margin-bottom: 5px;
        }}

        .header-info .meta {{
            font-size: {body_size - 1}pt;
            color: #666;
            line-height: 1.5;
        }}

        .profile-photo {{
            width: {photo_settings['width']}px;
            height: {photo_settings['height']}px;
            object-fit: cover;
            object-position: {photo_settings['offset_x']}% {photo_settings['offset_y']}%;
            border: 2px solid {primary_color};
            border-radius: {photo_settings['border_radius']};
            flex-shrink: 0;
        }}

        .summary {{
            font-size: {body_size}pt;
            margin-bottom: 20px;
            line-height: 1.6;
            color: #333;
        }}

        .layout-container {{
            display: flex;
            flex-direction: {flex_direction};
            gap: 20px;
            width: 100%;
        }}

        .main-col {{
            width: {main_width_pct}%;
        }}

        .side-col {{
            width: {sidebar_width_pct}%;
            background-color: {template_config["sidebar_bg"]};
            padding: 12px;
            border-radius: 6px;
        }}

        .section {{
            margin-bottom: 20px;
            page-break-inside: avoid;
        }}

        .section h2 {{
            font-size: {heading_size}pt;
            color: {primary_color};
            border-bottom: 2px solid {accent_color};
            padding-bottom: 4px;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .entry {{
            margin-bottom: 12px;
        }}

        .entry-header {{
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            margin-bottom: 4px;
        }}

        .entry-title {{
            font-weight: bold;
            font-size: {body_size + 1}pt;
            color: #000;
        }}

        .entry-subtitle {{
            font-size: {body_size - 1}pt;
            color: #666;
            font-style: italic;
        }}

        .entry-meta {{
            font-size: {body_size - 1}pt;
            color: #888;
        }}

        ul {{ margin-left: 20px; margin-bottom: 8px; }}
        li {{ margin-bottom: 3px; }}

        code {{
            background: #f4f4f4;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: monospace;
        }}

        .skills-grid {{
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            margin-bottom: 10px;
        }}

        .skill-tag {{
            background-color: {accent_color}20;
            color: {primary_color};
            padding: 3px 8px;
            border-radius: 12px;
            font-size: {body_size - 1}pt;
            border: 1px solid {primary_color}40;
        }}

        .social-links {{
            display: flex;
            flex-direction: column;
            gap: 6px;
            margin-bottom: 10px;
            font-size: {body_size}pt;
        }}

        .social-links a {{
            color: {primary_color};
            text-decoration: none;
        }}
    </style>
    </head>
    <body>
        <div class="header">
            <div class="header-info">
                <h1>{full_name}</h1>
                <div class="title">{title_str}</div>
                <div class="meta">
                    {location_str} | {phone_str} | {email_str}
                    {meta_extra}
                </div>
            </div>
            {photo_html}
        </div>

        {summary_html}

        <div class="layout-container">
            <div class="main-col">
                {main_html}
            </div>
            {side_col_html}
        </div>
    </body>
    </html>
    """
    return html

def render_pdf_preview(pdf_bytes: bytes):
    """Renders PDF pages as images to display a live visual preview in Streamlit."""
    try:
        doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")

        st.write(f"**Preview ({len(doc)} Page/s)**")

        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            pix = page.get_pixmap(dpi=120)
            img_bytes = pix.tobytes("png")

            st.image(img_bytes, caption=f"Page {page_num + 1}", use_container_width=True)

    except Exception as e:
        st.warning(f"Could not render visual preview: {e}")
        st.info("Use the download button below to view your full CV layout.")

# ============================================================================
# TWO-COLUMN SPLIT WITH INDEPENDENT SCROLL CONTAINERS
# ============================================================================

col_edit_area, col_prev = st.columns([1.2, 1])

# 1. Left Column Scrollable Viewport
with col_edit_area:
    with st.container(height=800, border=False):
        # ------------------------------------------------------------------------
        # MAIN CONTENT - PERSONAL INFORMATION
        # ------------------------------------------------------------------------
        st.title("👤 Personal Information")

        cv_data = st.session_state.cv_data

        col1, col2, col3 = st.columns(3)

        with col1:
            full_name = st.text_input("Full Name *", cv_data.get("full_name", ""), placeholder="John Doe")
            title = st.text_input("Professional Title *", cv_data.get("title", ""), placeholder="Software Engineer")
            phone = st.text_input("Phone *", cv_data.get("phone", ""), placeholder="+1 234 567 8900")
            if phone and not validate_phone(phone):
                st.warning("⚠️ Phone format may be invalid")

        with col2:
            email = st.text_input("Email *", cv_data.get("email", ""), placeholder="your@email.com")
            if email and not validate_email(email):
                st.error("❌ Invalid email format")

            location = st.text_input("Location", cv_data.get("location", ""), placeholder="City, Country")
            residency = st.text_input("Residency Status", cv_data.get("residency", ""))

        with col3:
            relocation = st.text_input("Relocation", cv_data.get("relocation", ""), placeholder="Open to relocation")
            linkedin_url = st.text_input("LinkedIn Profile", cv_data.get("linkedin_url", ""), placeholder="https://linkedin.com/in/...")

            if linkedin_url and not validate_url(linkedin_url):
                st.warning("⚠️ Invalid URL format")

        summary = st.text_area("Professional Summary (Markdown supported: **bold**, *italic*, `code`, ^sup^, ~sub~)",
                               cv_data.get("summary", ""),
                               height=100,
                               placeholder="Brief overview of your professional background and goals...")

        if summary and len(summary) < 50:
            st.warning("💡 Summary is quite short. Aim for 150-300 words for better impact.")

        # ------------------------------------------------------------------------
        # CV CONTENT SECTIONS
        # ------------------------------------------------------------------------
        st.divider()
        st.header("📝 CV Content")

        sections_data = {}
        saved_sec = cv_data.get("sections_data", {})

        # -------- PROFILES & LINKS --------
        with st.expander("🔗 Profiles & Links", expanded=True):
            col_github, col_linkedin_s, col_portfolio = st.columns(3)

            with col_github:
                github = st.text_input("GitHub", saved_sec.get("Profiles & Links", {}).get("GitHub", ""),
                                      placeholder="https://github.com/username")
            with col_linkedin_s:
                linkedin = st.text_input("LinkedIn", saved_sec.get("Profiles & Links", {}).get("LinkedIn", ""),
                                        placeholder="https://linkedin.com/in/username")
            with col_portfolio:
                portfolio = st.text_input("Portfolio/Website", saved_sec.get("Profiles & Links", {}).get("Portfolio", ""),
                                         placeholder="https://yourportfolio.com")

            sections_data["Profiles & Links"] = {
                "GitHub": github,
                "LinkedIn": linkedin,
                "Portfolio": portfolio,
            }

        # -------- TECHNICAL SKILLS --------
        with st.expander("💻 Technical Skills"):
            num_tech = int(st.number_input("Number of Technical Skill Categories/Items", 0, 10,
                                       len(saved_sec.get("Technical Skills", [])) if isinstance(saved_sec.get("Technical Skills"), list) else 1))
            tech_items = []
            for i in range(num_tech):
                st.markdown(f"**Technical Skill {i+1}**")
                item_data = saved_sec.get("Technical Skills", [])[i] if isinstance(saved_sec.get("Technical Skills"), list) and i < len(saved_sec.get("Technical Skills", [])) else {}

                c_name, c_desc = st.columns(2)
                with c_name:
                    t_name = st.text_input("Name", key=f"tech_name_{i}", value=item_data.get("name", ""))
                with c_desc:
                    t_desc = st.text_input("Description", key=f"tech_desc_{i}", value=item_data.get("description", ""))

                t_keywords = st.text_area("Keywords (comma separated or lines)", key=f"tech_keywords_{i}", value=item_data.get("keywords", ""), height=60)

                if t_name or t_keywords:
                    tech_items.append({
                        "name": t_name,
                        "description": t_desc,
                        "keywords": t_keywords
                    })
                st.divider()
            sections_data["Technical Skills"] = tech_items

        # -------- SOFT SKILLS --------
        with st.expander("🤝 Soft Skills"):
            num_soft = int(st.number_input("Number of Soft Skill Categories/Items", 0, 10,
                                       len(saved_sec.get("Soft Skills", [])) if isinstance(saved_sec.get("Soft Skills"), list) else 1))
            soft_items = []
            for i in range(num_soft):
                st.markdown(f"**Soft Skill {i+1}**")
                item_data = saved_sec.get("Soft Skills", [])[i] if isinstance(saved_sec.get("Soft Skills"), list) and i < len(saved_sec.get("Soft Skills", [])) else {}

                c_name, c_desc = st.columns(2)
                with c_name:
                    s_name = st.text_input("Name", key=f"soft_name_{i}", value=item_data.get("name", ""))
                with c_desc:
                    s_desc = st.text_input("Description", key=f"soft_desc_{i}", value=item_data.get("description", ""))

                s_keywords = st.text_area("Keywords", key=f"soft_keywords_{i}", value=item_data.get("keywords", ""), height=60)

                if s_name or s_keywords:
                    soft_items.append({
                        "name": s_name,
                        "description": s_desc,
                        "keywords": s_keywords
                    })
                st.divider()
            sections_data["Soft Skills"] = soft_items

        # -------- CERTIFICATIONS --------
        with st.expander("🏆 Certifications"):
            num_certs = int(st.number_input("Number of Certifications", 0, 10,
                                       len(saved_sec.get("Certifications", [])) if isinstance(saved_sec.get("Certifications"), list) else 0))
            certs = []
            for i in range(num_certs):
                st.markdown(f"**Certification {i+1}**")
                cert_data = saved_sec.get("Certifications", [])[i] if isinstance(saved_sec.get("Certifications"), list) and i < len(saved_sec.get("Certifications", [])) else {}

                col_title, col_issuer, col_date = st.columns([2, 2, 1])
                with col_title:
                    title_val = st.text_input("Name", key=f"cert_title_{i}", value=cert_data.get("title", ""))
                with col_issuer:
                    issuer_val = st.text_input("Issuer", key=f"cert_issuer_{i}", value=cert_data.get("issuer", ""))
                with col_date:
                    date_val = st.text_input("Date", key=f"cert_date_{i}", value=cert_data.get("date", ""), placeholder="2024")

                col_url, col_label = st.columns([2, 1])
                with col_url:
                    url_val = st.text_input("Website URL", key=f"cert_url_{i}", value=cert_data.get("url", ""), placeholder="https://...")
                with col_label:
                    label_val = st.text_input("Link Label", key=f"cert_label_{i}", value=cert_data.get("label", "View Credentials"))

                summary_val = st.text_area("Summary (Markdown supported)", key=f"cert_summary_{i}", value=cert_data.get("summary", ""), height=60)

                if title_val or issuer_val or url_val:
                    certs.append({
                        "title": title_val,
                        "issuer": issuer_val,
                        "date": date_val,
                        "url": url_val,
                        "label": label_val if label_val else "View Credentials",
                        "summary": summary_val
                    })
                st.divider()

            sections_data["Certifications"] = certs

        # -------- AWARDS --------
        with st.expander("🎖️ Awards"):
            num_awards = int(st.number_input("Number of Awards", 0, 10,
                                       len(saved_sec.get("Awards", [])) if isinstance(saved_sec.get("Awards"), list) else 0))
            awards = []
            for i in range(num_awards):
                st.markdown(f"**Award {i+1}**")
                award_data = saved_sec.get("Awards", [])[i] if isinstance(saved_sec.get("Awards"), list) and i < len(saved_sec.get("Awards", [])) else {}

                col_title, col_awarder = st.columns(2)
                with col_title:
                    a_title = st.text_input("Title", key=f"award_title_{i}", value=award_data.get("title", ""))
                with col_awarder:
                    a_awarder = st.text_input("Awarder", key=f"award_awarder_{i}", value=award_data.get("awarder", ""))

                col_date, col_url = st.columns(2)
                with col_date:
                    a_date = st.text_input("Date", key=f"award_date_{i}", value=award_data.get("date", ""), placeholder="2024")
                with col_url:
                    a_url = st.text_input("Website", key=f"award_url_{i}", value=award_data.get("url", ""), placeholder="https://...")

                if a_title or a_awarder:
                    awards.append({
                        "title": a_title,
                        "awarder": a_awarder,
                        "date": a_date,
                        "url": a_url
                    })
                st.divider()
            sections_data["Awards"] = awards

        # -------- LANGUAGES --------
        with st.expander("🌍 Languages"):
            num_langs = int(st.number_input("Number of Languages", 0, 10,
                                       len(saved_sec.get("Languages", [])) if isinstance(saved_sec.get("Languages"), list) else 0))
            langs = []
            for i in range(num_langs):
                st.markdown(f"**Language {i+1}**")
                lang_data = saved_sec.get("Languages", [])[i] if isinstance(saved_sec.get("Languages"), list) and i < len(saved_sec.get("Languages", [])) else {}

                col_name, col_desc = st.columns(2)
                with col_name:
                    name_val = st.text_input(f"Name", key=f"lang_name_{i}", value=lang_data.get("name", ""))
                with col_desc:
                    desc_val = st.text_input(f"Description", key=f"lang_desc_{i}", value=lang_data.get("description", ""), placeholder="Native / Fluent")

                if name_val:
                    langs.append({"name": name_val, "description": desc_val})
                st.divider()

            sections_data["Languages"] = langs

        # -------- EXPERIENCE --------
        with st.expander("💼 Work Experience"):
            num_exp = int(st.number_input("Number of Experience Entries", 0, 10,
                                     len(saved_sec.get("Experience", [])) if isinstance(saved_sec.get("Experience"), list) else 1))
            experiences = []

            for i in range(num_exp):
                st.subheader(f"Position {i+1}")
                exp_data = saved_sec.get("Experience", [])[i] if isinstance(saved_sec.get("Experience"), list) and i < len(saved_sec.get("Experience", [])) else {}

                col_company, col_title = st.columns(2)
                with col_company:
                    company = st.text_input("Company Name", key=f"exp_company_{i}", value=exp_data.get("company", ""))
                with col_title:
                    job_title = st.text_input("Position / Job Title", key=f"exp_title_{i}", value=exp_data.get("title", ""))

                col_date, col_loc = st.columns(2)
                with col_date:
                    date_range = st.text_input("Date Range", key=f"exp_date_{i}", value=exp_data.get("date_range", ""), placeholder="Jan 2020 - Present")
                with col_loc:
                    exp_location = st.text_input("Location", key=f"exp_location_{i}", value=exp_data.get("location", ""), placeholder="New York, NY")

                col_url, col_label = st.columns([2, 1])
                with col_url:
                    exp_website = st.text_input("Website URL", key=f"exp_url_{i}", value=exp_data.get("website", ""), placeholder="https://company.com")
                with col_label:
                    exp_link_label = st.text_input("Link Label", key=f"exp_link_label_{i}", value=exp_data.get("link_label", "Visit Website"))

                exp_summary = st.text_area("Summary (Markdown supported)", key=f"exp_summary_{i}", value=exp_data.get("summary", ""), height=60, placeholder="Brief overview of the role...")

                bullets = exp_data.get("bullets", [])
                if isinstance(bullets, str):
                    bullets = [bullets]

                bullets_text = "\n".join(bullets)
                bullets_input = st.text_area("Key Achievements / Bullets (Markdown supported)", key=f"exp_bullets_{i}", value=bullets_text, height=80)
                bullets_list = [b.strip() for b in bullets_input.split("\n") if b.strip()]

                if company or job_title or exp_summary or bullets_list:
                    experiences.append({
                        "company": company,
                        "title": job_title,
                        "date_range": date_range,
                        "location": exp_location,
                        "website": exp_website,
                        "link_label": exp_link_label if exp_link_label else "Visit Website",
                        "summary": exp_summary,
                        "bullets": bullets_list
                    })

                st.divider()

            sections_data["Experience"] = experiences

        # -------- EDUCATION --------
        with st.expander("🎓 Education"):
            num_edu = int(st.number_input("Number of Education Entries", 0, 10,
                                     len(saved_sec.get("Education", [])) if isinstance(saved_sec.get("Education"), list) else 1))
            educations = []

            for i in range(num_edu):
                st.subheader(f"Education {i+1}")
                edu_data = saved_sec.get("Education", [])[i] if isinstance(saved_sec.get("Education"), list) and i < len(saved_sec.get("Education", [])) else {}

                col_degree, col_school = st.columns(2)
                with col_degree:
                    degree = st.text_input("Degree", key=f"edu_degree_{i}", value=edu_data.get("degree", ""))
                with col_school:
                    school = st.text_input("School/University", key=f"edu_school_{i}", value=edu_data.get("school", ""))

                col_grad_start, col_grad_end = st.columns(2)
                with col_grad_start:
                    graduation = st.text_input("Graduation Date", key=f"edu_grad_{i}", value=edu_data.get("graduation", ""),
                                               placeholder="2023")
                with col_grad_end:
                    gpa = st.text_input("GPA (optional)", key=f"edu_gpa_{i}", value=edu_data.get("gpa", ""),
                                       placeholder="3.8/4.0")

                highlights = st.text_area("Highlights/Details (Markdown supported)", key=f"edu_highlights_{i}",
                                         value=edu_data.get("highlights", ""), height=60)

                if degree or school:
                    educations.append({
                        "degree": degree,
                        "school": school,
                        "graduation": graduation,
                        "gpa": gpa,
                        "highlights": highlights
                    })

                st.divider()

            sections_data["Education"] = educations

        # -------- PROJECTS --------
        with st.expander("🚀 Projects"):
            num_projects = int(st.number_input("Number of Projects", 0, 10,
                                          len(saved_sec.get("Projects", [])) if isinstance(saved_sec.get("Projects"), list) else 0))
            projects = []

            for i in range(num_projects):
                st.subheader(f"Project {i+1}")
                proj_data = saved_sec.get("Projects", [])[i] if isinstance(saved_sec.get("Projects", []), list) and i < len(saved_sec.get("Projects", [])) else {}

                proj_name = st.text_input("Name", key=f"proj_name_{i}", value=proj_data.get("name", ""))
                proj_desc = st.text_area("Description (Markdown supported)", key=f"proj_desc_{i}", value=proj_data.get("description", ""), height=60)
                proj_date = st.text_input("Date or Date Range", key=f"proj_date_{i}", value=proj_data.get("date_range", ""), placeholder="Jan 2023 - Mar 2023")

                col_url, col_label = st.columns([2, 1])
                with col_url:
                    proj_website = st.text_input("Website URL", key=f"proj_website_{i}", value=proj_data.get("website", ""), placeholder="https://...")
                with col_label:
                    proj_link_label = st.text_input("Link Label", key=f"proj_link_label_{i}", value=proj_data.get("link_label", "View Project"))

                proj_summary = st.text_area("Summary", key=f"proj_summary_{i}", value=proj_data.get("summary", ""), height=60)

                if proj_name or proj_desc:
                    projects.append({
                        "name": proj_name,
                        "description": proj_desc,
                        "date_range": proj_date,
                        "website": proj_website,
                        "link_label": proj_link_label if proj_link_label else "View Project",
                        "summary": proj_summary
                    })

                st.divider()

            sections_data["Projects"] = projects

        # -------- CUSTOM SECTIONS DATA INPUT --------
        for custom_sec in st.session_state.custom_sections:
            sec_type = st.session_state.custom_section_types.get(custom_sec, "Generic Text")
            saved_custom_val = saved_sec.get(custom_sec, [])

            with st.expander(f"📌 {custom_sec} ({sec_type})"):
                if sec_type == "Experience Layout":
                    c_num = int(st.number_input(f"Number of Entries for {custom_sec}", 0, 10, len(saved_custom_val) if isinstance(saved_custom_val, list) else 1, key=f"num_{custom_sec}"))
                    c_items = []
                    for i in range(c_num):
                        st.subheader(f"Entry {i+1}")
                        c_data = saved_custom_val[i] if isinstance(saved_custom_val, list) and i < len(saved_custom_val) else {}

                        col_c1, col_c2 = st.columns(2)
                        with col_c1:
                            c_comp = st.text_input("Organization / Company", key=f"{custom_sec}_comp_{i}", value=c_data.get("company", ""))
                        with col_c2:
                            c_title = st.text_input("Role / Title", key=f"{custom_sec}_title_{i}", value=c_data.get("title", ""))

                        col_d, col_l = st.columns(2)
                        with col_d:
                            c_date = st.text_input("Date Range", key=f"{custom_sec}_date_{i}", value=c_data.get("date_range", ""))
                        with col_l:
                            c_loc = st.text_input("Location", key=f"{custom_sec}_loc_{i}", value=c_data.get("location", ""))

                        col_u, col_lbl = st.columns([2, 1])
                        with col_u:
                            c_url = st.text_input("Website URL", key=f"{custom_sec}_url_{i}", value=c_data.get("website", ""))
                        with col_lbl:
                            c_link_label = st.text_input("Link Label", key=f"{custom_sec}_link_label_{i}", value=c_data.get("link_label", "Visit Website"))

                        c_summ = st.text_area("Summary", key=f"{custom_sec}_summary_{i}", value=c_data.get("summary", ""), height=60)

                        c_bullets = c_data.get("bullets", [])
                        if isinstance(c_bullets, str): c_bullets = [c_bullets]
                        c_b_input = st.text_area("Key Points / Bullets (One per line)", key=f"{custom_sec}_bullets_{i}", value="\n".join(c_bullets), height=80)
                        c_b_list = [b.strip() for b in c_b_input.split("\n") if b.strip()]

                        if c_comp or c_title or c_summ or c_b_list:
                            c_items.append({
                                "company": c_comp, "title": c_title, "date_range": c_date,
                                "location": c_loc, "website": c_url, "link_label": c_link_label if c_link_label else "Visit Website",
                                "summary": c_summ, "bullets": c_b_list
                            })
                        st.divider()
                    sections_data[custom_sec] = c_items

                elif sec_type == "Certification Layout":
                    c_num = int(st.number_input(f"Number of Certifications/Items for {custom_sec}", 0, 10, len(saved_custom_val) if isinstance(saved_custom_val, list) else 1, key=f"num_cert_{custom_sec}"))
                    c_items = []
                    for i in range(c_num):
                        st.markdown(f"**Item {i+1}**")
                        c_data = saved_custom_val[i] if isinstance(saved_custom_val, list) and i < len(saved_custom_val) else {}

                        col_t, col_iss, col_d = st.columns([2, 2, 1])
                        with col_t:
                            c_title = st.text_input("Title / Name", key=f"{custom_sec}_ctitle_{i}", value=c_data.get("title", ""))
                        with col_iss:
                            c_issuer = st.text_input("Issuer / Organization", key=f"{custom_sec}_cissuer_{i}", value=c_data.get("issuer", ""))
                        with col_d:
                            c_date = st.text_input("Date", key=f"{custom_sec}_cdate_{i}", value=c_data.get("date", ""))

                        col_u, col_l = st.columns([2, 1])
                        with col_u:
                            c_url = st.text_input("URL", key=f"{custom_sec}_curl_{i}", value=c_data.get("url", ""))
                        with col_l:
                            c_label = st.text_input("Label", key=f"{custom_sec}_clabel_{i}", value=c_data.get("label", "View Link"))

                        c_summ = st.text_area("Summary", key=f"{custom_sec}_csumm_{i}", value=c_data.get("summary", ""), height=60)

                        if c_title or c_issuer or c_url:
                            c_items.append({
                                "title": c_title, "issuer": c_issuer, "date": c_date,
                                "url": c_url, "label": c_label if c_label else "View Link", "summary": c_summ
                            })
                        st.divider()
                    sections_data[custom_sec] = c_items

                elif sec_type == "Projects":
                    c_num = int(st.number_input(f"Number of Projects for {custom_sec}", 0, 10, len(saved_custom_val) if isinstance(saved_custom_val, list) else 1, key=f"num_proj_{custom_sec}"))
                    c_items = []
                    for i in range(c_num):
                        st.markdown(f"**Project {i+1}**")
                        c_data = saved_custom_val[i] if isinstance(saved_custom_val, list) and i < len(saved_custom_val) else {}

                        c_name = st.text_input("Name", key=f"{custom_sec}_pname_{i}", value=c_data.get("name", ""))
                        c_desc = st.text_area("Description (Markdown supported)", key=f"{custom_sec}_pdesc_{i}", value=c_data.get("description", ""), height=60)
                        c_date = st.text_input("Date or Date Range", key=f"{custom_sec}_pdate_{i}", value=c_data.get("date_range", ""))

                        col_u, col_l = st.columns([2, 1])
                        with col_u:
                            c_url = st.text_input("Website URL", key=f"{custom_sec}_purl_{i}", value=c_data.get("website", ""))
                        with col_l:
                            c_label = st.text_input("Link Label", key=f"{custom_sec}_plabel_{i}", value=c_data.get("link_label", "View Project"))

                        c_summ = st.text_area("Summary", key=f"{custom_sec}_psum_{i}", value=c_data.get("summary", ""), height=60)

                        if c_name or c_desc:
                            c_items.append({
                                "name": c_name, "description": c_desc, "date_range": c_date,
                                "website": c_url, "link_label": c_label if c_label else "View Project", "summary": c_summ
                            })
                        st.divider()
                    sections_data[custom_sec] = c_items

                elif sec_type == "Summary Layout":
                    c_val = st.text_area(f"{custom_sec} Summary Text (Markdown supported)",
                                         value=str(saved_custom_val) if isinstance(saved_custom_val, str) else "",
                                         key=f"custom_sec_summary_{custom_sec}", height=120)
                    sections_data[custom_sec] = c_val

                else: # Generic Text
                    c_val = st.text_area(f"{custom_sec} Content (Markdown supported)",
                                         value=str(saved_custom_val) if isinstance(saved_custom_val, str) else "",
                                         key=f"custom_sec_input_{custom_sec}", height=100)
                    sections_data[custom_sec] = c_val

        cv_data.update({
            "full_name": full_name,
            "title": title,
            "email": email,
            "phone": phone,
            "location": location,
            "residency": residency,
            "relocation": relocation,
            "linkedin_url": linkedin_url,
            "summary": summary,
            "sections_data": sections_data,
            "custom_sections": st.session_state.custom_sections,
            "custom_section_types": st.session_state.custom_section_types,
            "section_visibility": st.session_state.section_visibility,
            "section_placement": st.session_state.section_placement,
            "section_order": st.session_state.section_order
        })
        st.session_state.cv_data = cv_data

        safe_filename = full_name.replace(' ', '_') if full_name else "My"

        # ------------------------------------------------------------------------
        # CV ANALYSIS & EXPORT OPTIONS
        # ------------------------------------------------------------------------
        st.divider()
        st.header("📊 CV Analysis & Export Options")

        col_score, col_ai = st.columns([1, 1])

        with col_score:
            score, suggestions = get_cv_score(cv_data)

            if score >= 80:
                color = "🟢"
            elif score >= 60:
                color = "🟡"
            else:
                color = "🔴"

            st.metric("CV Completeness Score", f"{score}/100", f"{color}")

            with st.expander("📋 Improvement Suggestions"):
                for suggestion in suggestions:
                    st.write(suggestion)

        with col_ai:
            if st.button("✨ Get General AI Suggestions", use_container_width=True):
                with st.spinner("Analyzing your CV..."):
                    st.session_state.ai_general_text = get_cv_enhancement_suggestions(cv_data)
                    st.session_state.show_ai_suggestions = True

            if st.session_state.show_ai_suggestions and "ai_general_text" in st.session_state:
                with st.expander("🤖 General AI Suggestions", expanded=True):
                    st.info(st.session_state.ai_general_text)

        # ------------------------------------------------------------------------
        # JOB-TARGETED AI CUSTOMIZATION
        # ------------------------------------------------------------------------
        st.markdown("---")
        st.subheader("🎯 Target Job Matching & Customization")

        # Added a unique key so Streamlit remembers what you type
        with st.container():
            job_desc_input = st.text_area(
                "Paste Job Description / Requirements",
                height=140,
                placeholder="Paste the full job posting here to analyze ATS keyword match and get tailored bullet recommendations...",
                key="unique_job_desc_input_box"
            )

        if st.button("🎯 Analyze & Match Job Description", use_container_width=True):
            if not job_desc_input.strip():
                st.warning("⚠️ Please paste a job description first.")
            else:
                with st.spinner("Comparing CV with job posting..."):
                    st.session_state.job_tailored_analysis = get_job_tailored_suggestions(cv_data, job_desc_input)
                    st.session_state.show_job_match = True

        if st.session_state.get("show_job_match", False) and "job_tailored_analysis" in st.session_state:
            with st.expander("📌 Tailored Job Recommendations", expanded=True):
                st.markdown(st.session_state.job_tailored_analysis)

        st.markdown("---")
        st.subheader("⚙️ Export Options")

        # Generate PDF bytes dynamically for the download buttons
        selected_template_key = cast(str, st.session_state.selected_template)
        rendered_html = generate_cv_html(
            cv_data,
            CV_TEMPLATES[selected_template_key],
            photo_settings,
            sidebar_width_pct=sidebar_width_pct if layout_mode == "Two Columns" else 32,
            sidebar_position=sidebar_position if layout_mode == "Two Columns" else "Right",
            layout_mode=layout_mode,
            primary_color=primary_color,
            accent_color=accent_color,
            font_family=font_family,
            heading_size=heading_size,
            body_size=body_size,
            line_height=line_height,
            margin_size=margin_size
        )
        pdf_bytes = HTML(string=rendered_html).write_pdf() or b""

        sub_col1, sub_col2 = st.columns(2)
        with sub_col1:
            st.download_button(
                "📥 Download PDF",
                data=pdf_bytes,
                file_name=f"{safe_filename}_CV.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        with sub_col2:
            st.download_button(
                "💾 Download JSON",
                data=json.dumps(cv_data, indent=2),
                file_name=f"{safe_filename}_CV_data.json",
                mime="application/json",
                use_container_width=True
            )

        with st.popover("📝 Save Version", use_container_width=True):
            version_input = st.text_input("Version Tag", value=f"{safe_filename}_{st.session_state.get('selected_template', 'default')}")
            if st.button("Confirm Save", use_container_width=True):
                save_version(cv_data, version_input)
                st.success(f"✅ Saved!")
        # ---> PLACE LEFT COLUMN SPACER HERE <---
        # for _ in range(5):
        #     st.markdown("<br>", unsafe_allow_html=True)
# 2. Right Column Scrollable Viewport
with col_prev:
    with st.container(height=800, border=False):
        st.subheader("👀 Live Preview")
        render_pdf_preview(pdf_bytes)
    # ---> PLACE RIGHT COLUMN SPACER HERE <---
    # for _ in range(5):
    #     st.markdown("<br>", unsafe_allow_html=True)
# ============================================================================
# FOOTER
# ============================================================================

st.divider()
st.caption("💡 Pro Tips: Fill all fields with *, keep summary 150-300 words, use action verbs in experience bullets, maintain consistent formatting")