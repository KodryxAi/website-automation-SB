import requests

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Website Automation Agent",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS styling
st.markdown("""
<style>
    .main { padding-top: 2rem; }

    .header-container {
        background: linear-gradient(135deg, #00c6ff 0%, #0072ff 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }

    .header-title {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }

    .header-subtitle {
        color: rgba(255,255,255,0.9);
        font-size: 1.2rem;
        font-weight: 300;
    }

    .upload-section {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.08);
        margin-bottom: 2rem;
        border: 1px solid #e0e6ed;
    }

    .stButton > button {
        background: linear-gradient(135deg, #00c6ff 0%, #0072ff 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 25px;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 198, 255, 0.4);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 198, 255, 0.6);
    }

    .loader-container {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #ffeaa7 0%, #fab1a0 100%);
        border-radius: 15px;
        margin: 2rem 0;
    }

    .loader-text {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2d3436;
        margin-top: 1rem;
    }

    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background: linear-gradient(135deg, #2d3436 0%, #636e72 100%);
        color: white;
        text-align: center;
        padding: 1rem;
        font-weight: 500;
        z-index: 999;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Session state
if 'submitted_url' not in st.session_state:
    st.session_state.submitted_url = ""
if 'automation_started' not in st.session_state:
    st.session_state.automation_started = False
if 'automation_complete' not in st.session_state:
    st.session_state.automation_complete = False
if 'n8n_results' not in st.session_state:
    st.session_state.n8n_results = []

# Header
st.markdown("""
<div class="header-container">
    <div class="header-title">🌐 Website Automation Agent</div>
    <div class="header-subtitle">Paste your website URL and let the agent do the work</div>
</div>
""", unsafe_allow_html=True)

# Main section
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    website_url = st.text_input("🔗 Enter Website URL", placeholder="https://example.com")
    st.markdown('</div>', unsafe_allow_html=True)

    if website_url:
        st.session_state.submitted_url = website_url
        if st.button("🤖 Automate Now"):
            st.session_state.automation_started = True
            st.session_state.automation_complete = False
            st.session_state.n8n_results = []
            
            # Show loading immediately
            with st.spinner('🔄 Processing your website...'):
                webhook_url = "https://ekshith06.app.n8n.cloud/webhook/streamlit"
                try:
                    response = requests.post(webhook_url, data={"url": website_url})
                    if response.status_code == 200:
                        try:
                            st.session_state.n8n_results.append(response.json())
                        except:
                            st.session_state.n8n_results.append({
                                "error": "Failed to parse JSON response",
                                "raw": response.text
                            })
                    else:
                        st.session_state.n8n_results.append({
                            "error": f"Request failed with status code {response.status_code}"
                        })
                except Exception as e:
                    st.session_state.n8n_results.append({"error": str(e)})
                
                st.session_state.automation_complete = True
                st.rerun()

    # Show results after loading completes
    if st.session_state.get('automation_complete', False):
        st.success("🎉 Automation completed successfully!")

        if st.button("🔄 Start New Automation"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    elif not website_url:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; color: #6c757d;">
            <div style="font-size: 3rem;">🌍</div>
            <div style="font-size: 1.2rem;">Paste a website URL to get started</div>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    Built by Kodryx AI ✨
</div>
""", unsafe_allow_html=True)

# Spacer for footer
st.markdown('<div style="height: 80px;"></div>', unsafe_allow_html=True)
