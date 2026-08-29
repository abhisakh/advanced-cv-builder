# 🚀 Advanced CV Builder Pro v2.0

A powerful, AI-enhanced CV/Resume builder with built-in text formatting, section management, multiple templates, and Google Gemini AI suggestions. Perfect for job seekers and professionals looking to create standout resumes.

**What's New in v2.0:** ✨ Built-in text formatter | 🎛️ Section management | ⚡ Gemini AI (faster) | 🎯 7 section types

---

## ✨ Key Features

### 🎨 **4 Professional Templates**
- **Modern**: Two-column layout with contemporary styling
- **Classic**: Traditional single-column professional design
- **Minimal**: Clean, distraction-free aesthetic
- **Creative**: Modern with accent colors for tech/creative roles

### 🤖 **AI-Powered Enhancements (Gemini)**
- Get AI suggestions powered by Google Gemini API to improve your CV
- Smart recommendations for keyword optimization
- Action verb suggestions for better impact
- Personalized improvement tips based on your content
- **Faster responses and better pricing than alternatives!**

### 📝 **Built-in Text Formatting**
Format your text with markdown-like syntax (no external dependencies!):
- **Bold**: `**text**`
- *Italic*: `*text*`
- Superscript: `^text^`
- Subscript: `~text~`
- `Code`: `` `text` ``
- ~~Strikethrough~~: `~~text~~`
- __Underline__: `__text__`

### 🎛️ **Section Management (NEW!)**
Users can now:
- **Show/Hide Sections** - Control which sections appear
- **Place Sections** - Choose Sidebar or Main Column placement
- **Reorder Sections** - Custom priority ordering
- **Choose Layout Types** - 7 different section layouts:
  - Experience Layout (with bullets and dates)
  - Certification Layout (compact format)
  - Summary Layout (paragraph style)
  - Projects (with links)
  - Technical Skills (tag format)
  - Soft Skills (tag format)
  - Generic Text (flexible format)

### ✅ **Smart Validation**
- Email format validation
- Phone number verification
- URL validation for links
- Professional summary length recommendations

### 📊 **CV Quality Scoring**
- Automatic completeness score (0-100)
- Section-by-section analysis
- Actionable improvement suggestions
- Best practices guidance

### 📁 **Profile Management**
- Save multiple CV profiles locally
- Quick load and switch between profiles
- JSON backup for data portability
- Version history tracking with timestamps

### 📝 **Comprehensive Sections**
- **Personal Information**: Full details with validation
- **Technical Skills**: Categorized skills with tags
- **Soft Skills**: Professional competencies
- **Experience**: Multiple entries with achievements
- **Education**: Degrees, schools, GPA, highlights
- **Certifications**: Credentials with issuer and date
- **Languages**: Proficiency levels
- **Projects**: Portfolio showcasing with links
- **Custom Sections**: Add any sections you need
- **Social Links**: GitHub, LinkedIn, Portfolio

### 🎯 **Advanced Customization**
- **Colors**: Primary and accent color pickers
- **Typography**: 4 font options, adjustable sizes
- **Layout**: Single or two-column layouts
- **Spacing**: Customizable margins and line height
- **Photo**: Multiple placement options, shape choices

### 📥 **Export Options**
- **PDF Download**: Professional PDF with all formatting
- **JSON Backup**: Complete data export for backup/sharing
- **Live Preview**: Real-time preview before download
- **Version History**: Track and manage CV versions

---

## 🛠️ Installation

### Prerequisites
- Python 3.9+
- pip (Python package manager)

### Quick Setup (5 minutes)

#### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install streamlit==1.32.0 weasyprint==60.1 google-genai==0.3.0 python-dotenv==1.0.0 Pillow==10.1.0
```

#### Step 2: (Optional) Set Up Gemini API Key for AI Features

Get your API key:
1. Go to: https://console.cloud.google.com
2. Create a new project (if needed)
3. Enable "Generative Language API"
4. Create an API key
5. Copy your key

Set the API key:

**Option A: Using Environment Variable**
```bash
# On Linux/Mac
export GEMINI_API_KEY='your-api-key-here'

# On Windows (Command Prompt)
set GEMINI_API_KEY=your-api-key-here

# On Windows (PowerShell)
$env:GEMINI_API_KEY='your-api-key-here'
```

**Option B: Using .env File** (Recommended)
Create a `.env` file in your project directory:
```
GEMINI_API_KEY=your-api-key-here
```

**Option C: Using Streamlit Secrets** (Production)
Create `.streamlit/secrets.toml`:
```toml
GEMINI_API_KEY = "your-api-key-here"
```

#### Step 3: Run the Application
```bash
streamlit run advance_cv_builder.py
```

The app will open in your browser at `http://localhost:8501`

**Note:** The app works without an API key - AI features just won't be available.

---

## 📖 Usage Guide

### 1. **Getting Started**
- The app opens with the sidebar and main content area
- Fill in your **Personal Information** section first
- Required fields are marked with `*`

### 2. **Creating Your CV**

#### Basic Information
- Full Name, Professional Title
- Email, Phone, Location
- Professional Summary (150-300 words recommended)
- Links: LinkedIn, GitHub, Portfolio

#### Adding Sections
Click on section expanders to add:
- Technical Skills (one per line)
- Soft Skills (one per line)
- Work Experience (multiple entries)
- Education (multiple entries)
- Projects (with links)
- Certifications (multiple entries)
- Languages (with proficiency levels)
- Custom Sections (unlimited!)

#### Using Text Formatting
Add emphasis with markdown-like syntax:
```
**Bold achievement:** Led team of 5
*Italic concept*: Machine learning expertise
`Code`: FastAPI and TensorFlow
Version: Python^3^.11+
Formula: H~2~O
Old: ~~outdated skill~~
Important: __underline this__
```

### 3. **Managing Sections** (NEW!)

#### Show/Hide Sections
- Toggle visibility for each section
- Create focused CVs for specific roles
- Hide irrelevant sections

#### Change Section Placement
- Move sections to Sidebar or Main Column
- Optimize for readability
- Different layouts per template

#### Reorder Sections
- Drag sections to reorder
- Put key content first
- Optimize for ATS scanning

#### Choose Section Types
- Experience Layout - for job descriptions
- Certification Layout - for credentials
- Summary Layout - for paragraphs
- Projects - for portfolio items
- And 3 more specialized types

### 4. **Selecting a Template**
1. Go to the sidebar → **Template & Styling**
2. Choose from: Modern, Classic, Minimal, or Creative
3. Customize colors, fonts, and spacing
4. Changes apply in real-time to the preview

### 5. **Profile Photo** (Optional)
1. Sidebar → **Profile Photo**
2. Check "Include Profile Photo"
3. Upload your image (JPG, PNG)
4. Choose placement: Header Left, Header Right, Left Sidebar
5. Select shape: Circular, Square, Rectangular
6. Adjust size and positioning

### 6. **Saving Your Profile**
1. Fill in "New Profile Name" in sidebar
2. Click "Save" button
3. Your profile is saved locally
4. Load anytime from the dropdown

### 7. **AI Suggestions** (Optional)
1. Click **"✨ Get AI Enhancement Suggestions"** button
2. Wait for Gemini API analysis
3. Review personalized recommendations
4. Apply suggestions manually

### 8. **Check CV Quality**
- View **CV Completeness Score** (0-100)
- Read improvement suggestions
- Score increases as you fill sections
- Aim for 80+ score

### 9. **Export Your CV**
- **Download PDF**: Ready-to-send resume
- **Download JSON**: Backup your data
- **Live Preview**: See exactly how it looks before downloading
- **Save Version**: Keep track of iterations

---

## 💡 Tips for Best Results

### ✍️ **Content Tips**
- **Summary**: Write 150-300 words, compelling professional overview
- **Experience**: Use action verbs (Led, Developed, Designed, Implemented)
- **Achievements**: Quantify results (30% improvement, 5+ projects, $2M budget)
- **Skills**: Organize by category for clarity
- **Formatting**: Use **bold** for key achievements, *italic* for concepts

### 📋 **Format Tips**
- Keep font size readable (10-11pt body text)
- Use 1.2-1.6 line height for readability
- Limit margins to 10-15mm
- Maintain consistent date formatting
- Use formatting sparingly (~10-15% of text)

### 🎨 **Design Tips**
- Use one primary color for headers
- Keep text color dark for print (black/dark gray)
- Use sidebar strategically (don't overload)
- Test PDF preview before downloading
- Choose template that matches your industry

### 💼 **Professional Tips**
- Customize CV for each job application
- Use specific keywords from job postings
- Tailor summary to target role
- Include measurable achievements
- Create role-specific versions (keep multiple profiles)

### 🤖 **AI Tips**
- Use AI suggestions to inspire improvements
- Add keywords recommended by Gemini
- Try action verb suggestions
- Iterate based on feedback
- Keep your best version saved

---

## 🔧 Advanced Features

### Version History
```
Save multiple versions of your CV:
1. Fill in your CV content
2. Click "Save as Version"
3. Name it (e.g., "Software Engineer - v2")
4. Access previous versions from history
```

### Backup & Restore
```
Backup your data:
1. Click "Download JSON"
2. Save the JSON file to safe location
3. Later, load it from sidebar

Restore from backup:
- Upload the JSON in new session
- All data is restored
- Perfect for syncing between devices
```

### Template Customization
```
Each template has preset values:
- Modern: Professional blues, two-column
- Classic: Traditional black/gray, single column
- Minimal: Elegant simplicity, minimal colors
- Creative: Bold colors for creative roles

All presets are customizable after selection!
```

### Multiple CVs
```
Create different versions for different roles:
1. Tech-focused CV (hide soft skills)
2. Management CV (emphasize leadership)
3. Startup CV (highlight projects)
4. Academic CV (emphasize education)
```

---

## 📊 Feature Comparison: v1.0 vs v2.0

| Feature | v1.0 | v2.0 | What Changed |
|---------|------|------|-------------|
| **Text Formatter** | Separate file | Built-in | Simpler, no external files |
| **AI Model** | Claude API | Gemini 2.5 | 2-3x faster, better pricing |
| **Section Control** | None | Full control | Users manage sections |
| **Section Types** | Basic | 7 types | More flexible layouts |
| **Speed** | Good | Excellent | Faster AI responses |
| **Code Size** | 1200 lines | 1523 lines | More features |
| **Dependencies** | 6 | 6 | Same, but better |

---

## ❓ Troubleshooting

### Issue: "Gemini API key error"
**Solution:**
1. Verify API key is set correctly
2. Check `GEMINI_API_KEY` environment variable
3. Ensure API key is valid and has quota
4. App works without key - AI features just won't work
5. Check you enabled "Generative Language API" in GCP

### Issue: "Text formatting not showing"
**Solution:**
1. Check syntax: `**text**` not `* text *`
2. No extra spaces before/after format markers
3. Try downloading PDF again
4. Check live preview first

### Issue: "PDF Download is Blank or Looks Wrong"
**Solution:**
1. Fill in at least Personal Information section
2. Check browser console for errors
3. Use live preview before downloading
4. Try in a different browser
5. Reduce image size if using photo

### Issue: "Custom Sections Not Appearing"
**Solution:**
1. Add custom section in sidebar
2. Click "Add Section" button
3. Section appears in CV Content Editor
4. Fill content in the expander

### Issue: "Photo Not Showing in PDF"
**Solution:**
1. Ensure image is <5MB
2. Use JPG or PNG format
3. Check photo position setting
4. Try circular shape
5. Check image file is valid

### Issue: "App Running Slowly"
**Solution:**
1. Clear browser cache
2. Close other Streamlit apps
3. Reduce image size before upload
4. Restart the app
5. Use a modern browser

### Issue: "Can't Save Profile"
**Solution:**
1. Check file permissions in directory
2. Ensure `saved_cvs/` directory exists
3. Try different profile name
4. Check available disk space
5. Restart the app

---

## 📦 File Structure

```
your-cv-builder/
├── advance_cv_builder.py          # Main application (1523 lines)
├── requirements.txt               # Python dependencies (UPDATED)
├── env.example                    # Configuration template (UPDATED)
├── README.md                      # This file (UPDATED)
├── QUICKSTART.md                  # 5-minute setup guide
├── UPDATED_QUICKSTART.md          # For v2.0 features
├── COMPLETE_SETUP_GUIDE.md        # Complete reference
├── UPDATE_ANALYSIS.md             # What changed in v2.0
├── EVERYTHING_SUMMARY.md          # Master overview
│
├── .env                           # (Create) Your API key
├── .streamlit/secrets.toml        # (Optional) For production
│
├── saved_cvs/                     # (Auto-created) Profile storage
│   ├── profile1.json
│   ├── profile2.json
│   └── ...
│
└── cv_versions/                   # (Auto-created) Version history
    ├── profile1_20240829_120000.json
    └── ...
```

---

## 🚀 Deployment

### Deploy to Streamlit Cloud (Recommended - Free)
1. Push repository to GitHub
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
3. Click "New App"
4. Select your repository
5. Add `GEMINI_API_KEY` in "Secrets"
6. Click "Deploy"
7. Auto-deploys on GitHub push

### Deploy to Your Own Server
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variable
export GEMINI_API_KEY='your-key'

# Run with Streamlit
streamlit run advance_cv_builder.py

# Or run with systemd/supervisord for production
```

### Deploy with Docker
```bash
# Create Dockerfile
docker build -t cv-builder .

# Run container
docker run -p 8501:8501 \
  -e GEMINI_API_KEY='your-key' \
  cv-builder

# Or use docker-compose
docker-compose up
```

---

## 🔐 Privacy & Security

- **Local Storage**: All CVs saved locally on your machine
- **No Cloud Sync**: Data doesn't leave your device unless you export
- **API Key**: Only used for optional AI suggestions
- **PDF Generation**: Processed locally, not stored anywhere
- **No Tracking**: No analytics, user tracking, or telemetry
- **Data Export**: You can export all data anytime
- **Open Source**: Full code transparency

---

## 📞 Support & Help

### Getting Help
1. Check **Troubleshooting** section above
2. Review **Tips for Best Results**
3. Read **UPDATED_QUICKSTART.md** for v2.0 features
4. Check **UPDATE_ANALYSIS.md** for technical details
5. Read code comments in `advance_cv_builder.py`

### Report Issues
- Found a bug? Open an issue on GitHub
- Have a feature request? Submit a pull request
- General questions? Check the documentation

---

## 🎯 Roadmap

### Coming Soon 🌟
- [ ] Import CV from LinkedIn profile
- [ ] Parse existing PDF resumes
- [ ] ATS scoring (Applicant Tracking System)
- [ ] Cover letter generator
- [ ] Interview prep suggestions
- [ ] Extended CV templates gallery
- [ ] Collaborative editing (share CVs)
- [ ] Mobile app version

---

## 💡 Pro Features

### Maximize Your CV Score
1. **Complete all sections** - Aim for 80+ score
2. **Use keywords** - Match job posting language
3. **Quantify achievements** - Numbers impress
4. **Professional summary** - Hook the reader
5. **Valid contact info** - Easy to reach you
6. **Use formatting** - **Bold** achievements, `code` for tools

### Common Mistakes to Avoid
- ❌ Generic summary with no specifics
- ❌ Spelling and grammar errors
- ❌ Inconsistent formatting or dates
- ❌ Too long (keep to 1-2 pages)
- ❌ Missing or invalid contact information
- ❌ Outdated skills listed
- ❌ Over-formatting (looks unprofessional)

### What Gemini AI Looks For
- Relevant keywords for your role
- Action verbs in achievement statements
- Quantified results and metrics
- Consistent formatting
- Clear professional narrative
- Specific skills and tools

---

## 📊 Technical Details

### Technology Stack
- **Frontend**: Streamlit (Python web framework)
- **PDF Generation**: WeasyPrint (HTML to PDF)
- **AI**: Google Gemini 2.5 Flash API
- **Text Formatting**: Built-in (no external library)
- **Storage**: Local JSON files
- **Configuration**: Python-dotenv

### System Requirements
- Python 3.9+
- 50MB disk space (plus space for exports)
- Modern web browser
- Internet connection (for Gemini API)

### Performance
- PDF generation: 1-2 seconds
- AI suggestions: 3-5 seconds
- Text formatting: < 100ms
- File operations: < 500ms

---

## 🤝 Contributing

Found a bug? Want to contribute?
- Fork the repository
- Create a feature branch
- Submit a pull request
- Share feedback or suggestions

---

## 📝 License

MIT License - Feel free to use, modify, and distribute!

---

## 🙏 Acknowledgments

- **Streamlit** - Amazing framework for data applications
- **Google Gemini** - Fast and affordable AI API
- **WeasyPrint** - Excellent HTML to PDF conversion
- **Python Community** - Great open-source libraries

---

## 🎉 Get Started Now!

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app
streamlit run advance_cv_builder.py

# 3. Build your professional CV
# 4. Get AI suggestions
# 5. Export and apply for jobs!
```

**Made with ❤️ for job seekers and professionals**

---

*Advanced CV Builder Pro v2.0*  
*Built-in text formatting | Gemini AI | Section management | Production-ready*  
*Last Updated: 2024*
