import streamlit as st
from datetime import datetime

st.set_page_config(page_title="المنصة الوطنية للتحقق", page_icon="✅", layout="wide")

# ---------------- RTL + Absher-like UI ----------------
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

# ---------------- Header (ONLY place we mention prototype) ----------------
st.markdown("""
<div class="topbar">
  <h1>المنصة الوطنية للتحقق من المستندات</h1>
  <p>محاكاة توضيحية (Prototype) — لا تستخدم بيانات حكومية حقيقية</p>
  <p>واجهة تجريبية لعرض فكرة SAQR2 ضمن مسار الأمن والذكاء الاصطناعي.</p>
</div>
""", unsafe_allow_html=True)

# ---------------- Pages ----------------
if st.session_state.page == "login":
    colL, colR = st.columns([1, 1.2])

    with colR:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### تسجيل الدخول")
        user = st.text_input("اسم المستخدم / رقم الهوية", placeholder="أدخل رقم الهوية أو اسم المستخدم")
        pin = st.text_input("رمز الدخول", type="password", placeholder="••••••")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("دخول"):
                st.session_state.logged_in = True
                goto("verify")
        with c2:
            st.markdown('<p class="muted" style="margin-top:10px;">نسيت رمز الدخول؟</p>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with colL:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### عن الخدمة")
        st.markdown("""
- التحقق الفوري من المستندات عبر تحليل البصمات الأمنية.
- تقليل التزوير الرقمي والورقي ورفع موثوقية الهوية.
- ربط موحّد يدعم تكامل الجهات الحكومية عبر واجهات آمنة.
        """)
        st.markdown('<div class="badge">🔒 أمن عالي</div> &nbsp; <div class="badge">⚡ سرعة تحقق</div> &nbsp; <div class="badge">🤖 ذكاء اصطناعي</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.page == "verify":
    if not st.session_state.logged_in:
        goto("login")
        st.stop()

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### رفع مستند للتحقق")

    cA, cB, cC = st.columns([1.1, 1.1, 0.8])
    with cA:
        doc_type = st.selectbox("نوع المستند", ["صك (وزارة العدل)", "هوية وطنية", "رخصة/شهادة أخرى"])
    with cB:
        ref_no = st.text_input("رقم مرجعي (اختياري)", placeholder="مثال: 12345")
    with cC:
        if st.button("تسجيل خروج"):
            st.session_state.logged_in = False
            st.session_state.last_result = None
            goto("login")

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
            res["ref_no"] = ref_no
            st.session_state.last_result = res
            goto("result")
    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.page == "result":
    res = st.session_state.last_result
    if not res:
        goto("verify")
        st.stop()

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### نتيجة التحقق")

    st.markdown(f'<p class="muted">نوع المستند: <b>{res["doc_type"]}</b> &nbsp;|&nbsp; الملف: <b>{res["filename"]}</b> &nbsp;|&nbsp; وقت التحقق: {res["time"]}</p>', unsafe_allow_html=True)

    if res["status"] == "أصلي":
        st.success("✅ التحقق: المستند أصلي ورسمي")
    elif res["status"] == "مشتبه":
        st.error("⚠️ التحقق: توجد مؤشرات اشتباه بالتزوير/التلاعب")
    else:
        st.warning("ℹ️ التحقق: نتيجة غير مؤكدة")

    st.markdown("—")
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

    st.markdown("---")
    st.markdown("### هل تريد الإبلاغ عن المستند؟")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("إبلاغ"):
            goto("report")
    with c2:
        if st.button("رجوع"):
            goto("verify")
    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.page == "report":
    res = st.session_state.last_result
    if not res:
        goto("verify")
        st.stop()

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### نموذج الإبلاغ")
    reason = st.selectbox("سبب الإبلاغ", ["اشتباه تزوير", "اختلاف بيانات", "مستند منتحل", "أخرى"])
    details = st.text_area("ملاحظات إضافية", placeholder="اكتب التفاصيل باختصار...")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("إرسال البلاغ"):
            st.success("✅ تم إرسال البلاغ شكرا لتعاونك")
    with c2:
        if st.button("عودة"):
            goto("result")

    st.markdown("</div>", unsafe_allow_html=True)
