st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;600;700;800&display=swap');

/* ===== GLOBAL RTL FORCE ===== */
html, body, [class*="css"], .stApp, .main, .block-container {
  font-family: 'Tajawal', sans-serif !important;
  direction: rtl !important;
  text-align: right !important;
}

/* force RTL on EVERYTHING */
* {
  direction: rtl !important;
  text-align: right !important;
}

/* background */
.stApp {
  background: #f4f7f6;
  color: #0b1f19;
}

/* columns fix */
div[data-testid="column"] {
  direction: rtl !important;
}

/* cards */
.card {
  background: #ffffff;
  border-radius: 18px;
  border: 1px solid rgba(0,0,0,0.08);
  padding: 16px;
  margin-bottom: 14px;
}

/* top bar */
.topbar {
  background: linear-gradient(90deg, #0b6b55 0%, #0f8a6b 100%);
  border-radius: 18px;
  padding: 18px;
  color: #ffffff;
  margin-bottom: 14px;
}
.topbar h1, .topbar p {
  color: #ffffff !important;
}

/* buttons */
.stButton > button {
  background: #0b6b55 !important;
  color: #ffffff !important;
  border-radius: 14px !important;
  font-weight: 800 !important;
}
.stButton > button:hover {
  background: #0f8a6b !important;
}

/* inputs */
.stTextInput input,
.stTextArea textarea,
div[data-baseweb="select"] {
  direction: rtl !important;
  text-align: right !important;
  border-radius: 14px !important;
}

/* selectbox text */
div[data-baseweb="select"] * {
  direction: rtl !important;
  text-align: right !important;
}

/* file uploader */
div[data-testid="stFileUploader"],
div[data-testid="stFileUploader"] * {
  direction: rtl !important;
  text-align: right !important;
}

/* alerts */
div[role="alert"] {
  direction: rtl !important;
  text-align: right !important;
}

/* markdown + lists */
ul, li {
  direction: rtl !important;
  text-align: right !important;
}

/* labels */
label {
  font-weight: 700 !important;
  direction: rtl !important;
  text-align: right !important;
}

/* hide streamlit chrome */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)
