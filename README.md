# 🚀 Advanced CV Builder Pro

A powerful, AI-enhanced CV/Resume builder with multiple templates, smart validation, and Claude AI suggestions. Perfect for job seekers and professionals looking to create standout resumes.

---

## ✨ Features

### 🎨 **4 Professional Templates**
- **Modern**: Two-column layout with contemporary styling
- **Classic**: Traditional single-column professional design
- **Minimal**: Clean, distraction-free aesthetic
- **Creative**: Modern with accent colors for tech/creative roles

### 🤖 **AI-Powered Enhancements**
- Get AI suggestions powered by Claude API to improve your CV
- Smart recommendations for keyword optimization
- Action verb suggestions for better impact
- Personalized improvement tips based on your content

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
- Version history tracking

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
- **PDF Download**: Professional PDF with formatting
- **JSON Backup**: Complete data export for backup/sharing
- **Live Preview**: Real-time preview before download
- **Version History**: Track and manage CV versions

---

## 🛠️ Installation

### Prerequisites
- Python 3.9+
- pip (Python package manager)

### Step 1: Clone or Download
```bash
# If using git
git clone https://github.com/yourusername/advanced-cv-builder.git
cd advanced-cv-builder

# Or just download the files
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Set Up Claude API Key (Optional - for AI suggestions)

#### Option A: Using Environment Variable
```bash
# On Linux/Mac
export ANTHROPIC_API_KEY='your-api-key-here'

# On Windows (Command Prompt)
set ANTHROPIC_API_KEY=your-api-key-here

# On Windows (PowerShell)
$env:ANTHROPIC_API_KEY='your-api-key-here'
```

#### Option B: Using .env File
Create a `.env` file in the same directory:
```
ANTHROPIC_API_KEY=your-api-key-here
```

#### Option C: Using Streamlit Secrets (Production)
Create `.streamlit/secrets.toml`:
```toml
ANTHROPIC_API_KEY = "your-api-key-here"
```

### Step 4: Run the Application
```bash
streamlit run advanced_cv_builder.py
```

The app will open in your browser at `http://localhost:8501`

---

## 📖 Usage Guide

### 1. **Getting Started**
- The app opens with sample placeholder text
- Fill in your **Personal Information** section first
- Required fields are marked with `*`

### 2. **Selecting a Template**
1. Go to the sidebar → **Template & Styling**
2. Choose from: Modern, Classic, Minimal, or Creative
3. Customize colors, fonts, and spacing
4. Changes apply in real-time to the preview

### 3. **Adding Content**
- Click on section expanders to add information
- For multiple entries (Experience, Education, Projects):
  - Use the number input to add more entries
  - Fill in each entry's details
  - Entries appear in order on the CV

### 4. **Profile Photo** (Optional)
1. Sidebar → **Profile Photo**
2. Check "Include Profile Photo"
3. Upload your image (JPG, PNG)
4. Choose placement: Header Left, Header Right, Left Sidebar
5. Select shape: Circular, Square, Rectangular
6. Adjust size and positioning

### 5. **Custom Sections**
1. Sidebar → **Custom Sections**
2. Enter section name (e.g., "Publications", "Volunteer Work")
3. Click "Add Section"
4. The section appears in the content editor
5. Add content and it displays on your CV

### 6. **Saving Your Profile**
1. Fill in "New Profile Name" in sidebar
2. Click "Save" button
3. Your profile is saved locally
4. Load it anytime from the dropdown

### 7. **AI Suggestions**
1. Click **"Get AI Enhancement Suggestions"** button
2. Wait for Claude API analysis
3. Review personalized recommendations
4. Apply suggestions manually

### 8. **Check CV Quality**
- View **CV Completeness Score** (0-100)
- Read improvement suggestions
- Score increases as you fill sections

### 9. **Export Your CV**
- **Download PDF**: Ready-to-send resume
- **Download JSON**: Backup your data
- **Live Preview**: See how it looks before downloading

---

## 🎯 Tips for Best Results

### ✍️ **Content Tips**
- **Summary**: Write 150-300 words, compelling professional overview
- **Experience**: Use action verbs (Led, Developed, Designed, etc.)
- **Achievements**: Quantify results (30% improvement, 5+ projects)
- **Skills**: Organize by category for clarity

### 📋 **Format Tips**
- Keep font size readable (10-11pt body text)
- Use 1.2-1.6 line height for readability
- Limit margins to 10-15mm
- Maintain consistent date formatting

### 🎨 **Design Tips**
- Use one primary color for headers
- Keep text color dark for print (black/dark gray)
- Use sidebar sparingly in two-column mode
- Test PDF preview before downloading

### 💼 **Professional Tips**
- Customize CV for each job application
- Use specific keywords from job postings
- Tailor summary to target role
- Include measurable achievements

---

## 🔧 Advanced Features

### Version History
```
Save multiple versions of your CV:
1. Fill in your CV
2. Click "Save as Version"
3. Name it (e.g., "Software Engineer - v2")
4. Access previous versions from history
```

### Backup & Restore
```
Backup your data:
1. Click "Download JSON"
2. Save the JSON file
3. Later, load it from sidebar or import manually

Restore from backup:
- Upload the JSON in new session
- All data restored
```

### Template Customization
```
Each template has preset values:
- Modern: Professional blues, two-column
- Classic: Traditional black/gray, single column
- Minimal: Elegant simplicity
- Creative: Bold colors for creatives

Modify any preset after selection!
```

---

## ❓ Troubleshooting

### Issue: "API Key Error" for AI suggestions
**Solution:**
1. Verify API key is set correctly
2. Check ANTHROPIC_API_KEY environment variable
3. Ensure API key is valid and has usage credits
4. AI suggestions are optional - app works without them

### Issue: PDF Download is Blank
**Solution:**
1. Fill in at least Personal Information section
2. Check browser console for errors
3. Try in a different browser
4. Ensure WeasyPrint library is installed

### Issue: Custom Sections Not Appearing
**Solution:**
1. Add custom section in sidebar
2. Click "Add Section" button
3. Section appears in CV Content Editor
4. Fill content in the expander

### Issue: Photo Not Showing in PDF
**Solution:**
1. Ensure image is <5MB
2. Use JPG or PNG format
3. Check photo position setting
4. Try circular shape if rectangular doesn't work

### Issue: Slow Loading
**Solution:**
1. Clear browser cache
2. Close other Streamlit apps
3. Reduce image size before upload
4. Reload the page

---

## 📦 File Structure

```
advanced-cv-builder/
├── advanced_cv_builder.py    # Main application
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── .env                       # (Create) API key configuration
└── saved_cvs/                 # (Auto-created) Profile storage
    ├── profile1.json
    ├── profile2.json
    └── ...
└── cv_versions/              # (Auto-created) Version history
    ├── profile1_timestamp.json
    └── ...
```

---

## 🚀 Deployment

### Deploy to Streamlit Cloud (Free)
1. Fork repository on GitHub
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
3. Click "New App"
4. Select your repository
5. Add `ANTHROPIC_API_KEY` in secrets
6. Deploy!

### Deploy to Heroku
```bash
# Create Procfile
echo "web: streamlit run advanced_cv_builder.py" > Procfile

# Deploy
git push heroku main
```

### Deploy to Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "advanced_cv_builder.py"]
```

---

## 🔐 Privacy & Security

- **Local Storage**: All CVs saved locally on your machine
- **No Cloud Sync**: Data doesn't leave your device unless you export
- **API Key**: Only used for optional AI suggestions
- **PDF Generation**: Processed locally, not stored
- **No Tracking**: No analytics or user tracking

---

## 🤝 Contributing

Found a bug? Have a feature suggestion? 
- Open an issue on GitHub
- Submit a pull request
- Share feedback via email

---

## 📝 License

MIT License - Feel free to use and modify!

---

## 🙏 Acknowledgments

- **Streamlit**: Amazing framework for data apps
- **Anthropic**: Claude API for AI suggestions
- **WeasyPrint**: HTML to PDF conversion
- **Font Awesome**: Icons and symbols

---

## 📞 Support

### Getting Help
1. Check **Troubleshooting** section above
2. Review **Tips for Best Results**
3. Ensure all dependencies are installed
4. Clear cache and reload

### Report Issues
- GitHub Issues: Report bugs
- Email: Support for questions
- Discussions: Community help

---

## 🎯 Roadmap

### Coming Soon 🌟
- [ ] Import CV from LinkedIn
- [ ] Parse existing PDF CVs
- [ ] ATS scoring (Applicant Tracking System)
- [ ] Cover letter generator
- [ ] Interview prep suggestions
- [ ] CV templates gallery
- [ ] Collaborative editing
- [ ] Mobile app version

---

## 💡 Pro Features

### Maximize Your CV Score
1. **Complete all sections**: Aim for 80+ score
2. **Use keywords**: Match job posting language
3. **Quantify achievements**: Numbers impress
4. **Professional summary**: Hook the reader
5. **Valid contact info**: Make it easy to reach you

### Common Mistakes to Avoid
- ❌ Generic summary with no specifics
- ❌ Spelling and grammar errors
- ❌ Inconsistent formatting
- ❌ Too long (keep to 1-2 pages)
- ❌ Missing contact information
- ❌ Outdated skills listed

---

**Ready to build your amazing CV?** 🎉

Start the app and create your professional resume today!

```bash
streamlit run advanced_cv_builder.py
```

---

*Made with ❤️ for job seekers and professionals*

Last Updated: 2024
