import streamlit as st
from datetime import datetime

st.set_page_config(page_title="المنصة الوطنية للتحقق", page_icon="✅", layout="centered")

# ---------------- Strong RTL + Absher-like styling ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;600;700;800&display=swap');

:root{
  --bg:#ffffff;
 /* أخضر غامق */
  --card:#ffffff;
  --text:#0b2a24;
  --muted:#65726e;
  --border:rgba(0,0,0,0.10);
  --absher:#0b3a2e;
  --absherDark:#075544;
  --shadow: 0 18px 45px rgba(0,0,0,0.22);
}

/* Global */
html, body, [class*="css"], .stApp{
  font-family:'Tajawal', sans-serif !important;
}
.stApp{
  background: var(--bg);
}

/* Force RTL everywhere (Streamlit sometimes needs deep selectors) */
*{
  direction: rtl !important;
  text-align: right !important;
}
div, p, span, label, h1, h2, h3, h4, h5, h6, input, textarea{
  direction: rtl !important;
  text-align: right !important;
}

/* Hide Streamlit chrome */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Layout width */
.block-container{
  padding-top: 1.3rem;
  max-width: 980px;
}

/* Top title on green background */
.hero{
  margin: 0 auto 18px auto;
  width: min(920px, 100%);
  color: #eafff7;
}
.hero h1{
  margin: 0 0 6px 0;
  font-size: 1.65rem;
  font-weight: 900;
  color:#eafff7 !important;
}
.hero p{
  margin: 0;
  color: rgba(234,255,247,0.88) !important;
  font-weight: 650;
}

/* White card */
.card{
  width: min(920px, 100%);
  margin: 0 auto 16px auto;
  background: var(--card);
  border-radius: 26px;
  border: 1px solid rgba(255,255,255,0.10);
  box-shadow: var(--shadow);
  overflow: hidden;
}

/* Card header strip */
.card-head{
  background: linear-gradient(90deg, var(--absherDark), var(--absher));
  padding: 20px 22px;
}
.card-head h2{
  margin: 0;
  color:#fff !important;
  font-size: 1.35rem;
  font-weight: 900;
}

/* Card body */
.card-body{
  padding: 20px 22px 18px 22px;
}

/* Inputs row with icon */
.field{
  margin-top: 12px;
}
.field .label{
  font-weight: 900;
  color: var(--text) !important;
  margin-bottom: 6px;
}

/* Make Streamlit inputs look like Absher */
.stTextInput input{
  border-radius: 14px !important;
  padding: 12px 12px !important;
  border: 1px solid rgba(0,0,0,0.14) !important;
  background: #fff !important;
}

/* Buttons */
.stButton>button{
  background: var(--absher) !important;
  color: #fff !important;
  border: 0 !important;
  border-radius: 14px !important;
  padding: 14px 16px !important;
  font-weight: 900 !important;
  font-size: 1.05rem !important;
  width: 100% !important;
}
.stButton>button:hover{
  background: var(--absherDark) !important;
}

/* Logout as text-like button */
.logout .stButton>button{
  width: auto !important;
  padding: 10px 14px !important;
  border-radius: 12px !important;
  font-weight: 900 !important;
}

/* Service chips */
.chips{
  display:flex;
  flex-wrap:wrap;
  gap:10px;
}
.chip{
  display:inline-flex;
  align-items:center;
  gap:8px;
  padding: 9px 12px;
  border-radius: 999px;
  border: 1px solid rgba(11,107,85,0.22);
  background: rgba(11,107,85,0.08);
  color: var(--text) !important;
  font-weight: 850;
}

/* File uploader RTL fixes */
div[data-testid="stFileUploader"]{
  direction: rtl !important;
  text-align: right !important;
}
div[data-testid="stFileUploader"] section{
  direction: rtl !important;
  text-align: right !important;
}
div[data-testid="stFileUploader"] *{
  direction: rtl !important;
  text-align: right !important;
}

/* Selectbox RTL fixes */
div[data-baseweb="select"] *{
  direction: rtl !important;
  text-align: right !important;
}

/* Alerts RTL */
div[role="alert"]{
  direction: rtl !important;
  text-align: right !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------- Session ----------------
if "page" not in st.session_state:
    st.session_state.page = "login"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "last_result" not in st.session_state:
    st.session_state.last_result = None

def goto(page: str):
    st.session_state.page = page

def fake_verify(doc_type: str, filename: str):
    if doc_type == "صك (وزارة العدل)":
        return {
            "status": "أصلي",
            "score": 0.93,
            "issuer": "وزارة العدل",
            "copies": 2,
            "usage_count": 10,
            "used_at": ["وزارة الموارد البشرية", "وزارة التجارة", "وزارة الداخلية"],
            "notes": "تمت مطابقة البصمة الأمنية مع النموذج المرجعي."
        }
    if doc_type == "هوية وطنية":
        return {
            "status": "مشتبه",
            "score": 0.41,
            "issuer": "الأحوال المدنية",
            "copies": None,
            "usage_count": 0,
            "used_at": [],
            "notes": "تم رصد مؤشرات تلاعب بصري تتطلب مراجعة."
        }
    return {
        "status": "غير مؤكد",
        "score": 0.66,
        "issuer": "جهة غير محددة",
        "copies": None,
        "usage_count": 3,
        "used_at": ["جهة حكومية"],
        "notes": "نتيجة أولية قابلة للتحسين عند توسيع النماذج المرجعية."
    }

# ---------------- Hero (green background) ----------------
st.markdown("""
<div class="hero">
  <h1>المنصة الوطنية للتحقق من المستندات</h1>
  <p>محاكاة توضيحية (Prototype) — لا تستخدم بيانات حكومية حقيقية</p>
  <p>واجهة تجريبية لعرض فكرة SQR2 ضمن مسار الأمن والذكاء الاصطناعي.</p>
</div>
""", unsafe_allow_html=True)

# ---------------- Pages ----------------
if st.session_state.page == "login":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-head"><h2>تسجيل الدخول</h2></div>', unsafe_allow_html=True)
    st.markdown('<div class="card-body">', unsafe_allow_html=True)

    st.markdown('<div class="field"><div class="label">👤 اسم المستخدم أو رقم الهوية</div></div>', unsafe_allow_html=True)
    user = st.text_input("", placeholder="اسم المستخدم أو رقم الهوية", label_visibility="collapsed")

    st.markdown('<div class="field"><div class="label">🔒 رمز الدخول</div></div>', unsafe_allow_html=True)
    pin = st.text_input("", placeholder="رمز الدخول", type="password", label_visibility="collapsed")

    st.markdown('<div style="margin-top:14px;"></div>', unsafe_allow_html=True)
    if st.button("تسجيل الدخول"):
        st.session_state.logged_in = True
        goto("verify")

    st.markdown('<div style="margin-top:16px;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="chips">', unsafe_allow_html=True)
    st.markdown('<div class="chip">🔒 تعزيز موثوقية المستندات</div>', unsafe_allow_html=True)
    st.markdown('<div class="chip">⚡ تحقق فوري خلال ثوانٍ</div>', unsafe_allow_html=True)
    st.markdown('<div class="chip">🤖 تحليل بصمة أمنية</div>', unsafe_allow_html=True)
    st.markdown('<div class="chip">🔗 تكامل عبر واجهات آمنة</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div></div>', unsafe_allow_html=True)

elif st.session_state.page == "verify":
    if not st.session_state.logged_in:
        goto("login")
        st.stop()

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-head"><h2>رفع مستند للتحقق</h2></div>', unsafe_allow_html=True)
    st.markdown('<div class="card-body">', unsafe_allow_html=True)

    doc_type = st.selectbox("نوع المستند", ["صك (وزارة العدل)", "هوية وطنية", "رخصة/شهادة أخرى"])

    uploaded = st.file_uploader("ارفع صورة المستند", type=["png", "jpg", "jpeg"])

    if uploaded is not None:
        st.image(uploaded, caption="معاينة المستند", use_container_width=True)

    if st.button("تحقق الآن"):
        if uploaded is None:
            st.warning("فضلاً ارفع صورة للمستند أولاً.")
        else:
            res = fake_verify(doc_type, uploaded.name)
            res["filename"] = uploaded.name
            res["time"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            res["doc_type"] = doc_type
            st.session_state.last_result = res
            goto("result")

    # logout under (as requested)
    st.markdown('<div style="margin-top:14px;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="logout">', unsafe_allow_html=True)
    if st.button("تسجيل خروج"):
        st.session_state.logged_in = False
        st.session_state.last_result = None
        goto("login")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div></div>', unsafe_allow_html=True)

elif st.session_state.page == "result":
    res = st.session_state.last_result
    if not res:
        goto("verify")
        st.stop()

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-head"><h2>نتيجة التحقق</h2></div>', unsafe_allow_html=True)
    st.markdown('<div class="card-body">', unsafe_allow_html=True)

    st.markdown(f'<p style="color:var(--muted); font-weight:700; margin-top:0;">نوع المستند: <b>{res["doc_type"]}</b> | الملف: <b>{res["filename"]}</b> | وقت التحقق: {res["time"]}</p>', unsafe_allow_html=True)

    if res["status"] == "أصلي":
        st.success("✅ التحقق: المستند أصلي ورسمي")
    elif res["status"] == "مشتبه":
        st.error("⚠️ التحقق: توجد مؤشرات اشتباه بالتزوير/التلاعب")
    else:
        st.warning("ℹ️ التحقق: نتيجة غير مؤكدة")

    st.markdown(f"**الجهة المُصدِرة:** {res['issuer']}")
    if res.get("copies") is not None:
        st.markdown(f"**عدد النسخ الصادرة:** {res['copies']}")
    st.markdown(f"**عدد مرات الاستخدام:** {res['usage_count']}")

    if res.get("used_at"):
        st.markdown("**تم استخدامه لدى:**")
        for x in res["used_at"]:
            st.markdown(f"- {x}")

    st.markdown(f"**ملاحظات النظام:** {res['notes']}")
    st.markdown(f"**نسبة الثقة:** {int(res['score']*100)}%")

    st.markdown('<div style="margin-top:14px;"></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("إبلاغ عن المستند"):
            goto("report")
    with c2:
        if st.button("رجوع"):
            goto("verify")

    st.markdown('</div></div>', unsafe_allow_html=True)

elif st.session_state.page == "report":
    res = st.session_state.last_result
    if not res:
        goto("verify")
        st.stop()

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-head"><h2>نموذج الإبلاغ</h2></div>', unsafe_allow_html=True)
    st.markdown('<div class="card-body">', unsafe_allow_html=True)

    reason = st.selectbox("سبب الإبلاغ", ["اشتباه تزوير", "اختلاف بيانات", "مستند منتحل", "أخرى"])
    details = st.text_area("ملاحظات إضافية", placeholder="اكتب التفاصيل باختصار...")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("إرسال البلاغ"):
            st.success("✅ تم إرسال البلاغ")
    with c2:
        if st.button("عودة"):
            goto("result")

    st.markdown('</div></div>', unsafe_allow_html=True)
