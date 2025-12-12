import streamlit as st
from datetime import datetime

st.set_page_config(page_title="المنصة الوطنية للتحقق", page_icon="✅", layout="centered")

# ---------------- RTL + Absher-like clean login ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;600;700;800&display=swap');

:root{
  --bg:#ffffff;
  --card:#ffffff;
  --text:#1b1f1e;
  --muted:#6a7772;
  --border:rgba(0,0,0,0.10);
  --absher:#0b6b55;
  --absherDark:#075544;
  --shadow: 0 18px 40px rgba(0,0,0,0.08);
}

html, body, [class*="css"]{
  font-family:'Tajawal', sans-serif !important;
  direction: rtl !important;
  text-align: right !important;
}

.stApp{ background: var(--bg); color: var(--text); }
.block-container{ padding-top: 1.4rem; max-width: 980px; }

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Top header */
.header{
  border-radius: 18px;
  padding: 18px 18px;
  border: 1px solid var(--border);
  background: #fff;
  box-shadow: 0 12px 28px rgba(0,0,0,0.05);
  margin-bottom: 16px;
}
.header h1{ margin:0; font-size: 1.45rem; font-weight:800; color: var(--absher) !important; }
.header p{ margin:6px 0 0 0; color: var(--muted) !important; font-weight:600; }

/* Login card */
.login-wrap{
  display:flex;
  justify-content:center;
}
.login-card{
  width: min(640px, 100%);
  background: #fff;
  border: 1px solid var(--border);
  border-radius: 26px;
  box-shadow: var(--shadow);
  overflow:hidden;
}
.login-top{
  background: linear-gradient(90deg, var(--absherDark), var(--absher));
  padding: 20px 22px;
}
.login-top h2{
  margin:0;
  color:#fff !important;
  font-size: 1.35rem;
  font-weight: 800;
}
.login-body{
  padding: 20px 22px 22px 22px;
}
.label{
  font-weight:800;
  margin: 10px 0 6px 0;
  color: var(--text) !important;
}

/* Inputs nicer */
.stTextInput input{
  border-radius: 14px !important;
  padding: 12px 12px !important;
}

/* Buttons */
.stButton>button{
  width: 100%;
  background: var(--absher);
  color:#fff;
  border:0;
  border-radius: 14px;
  padding: 14px 16px;
  font-weight: 900;
  font-size: 1.05rem;
}
.stButton>button:hover{ background: var(--absherDark); }

/* Services card */
.service-card{
  width: min(860px, 100%);
  margin: 18px auto 0 auto;
  background: #fff;
  border: 1px solid var(--border);
  border-radius: 22px;
  box-shadow: 0 12px 28px rgba(0,0,0,0.04);
  padding: 16px 18px;
}
.service-title{
  font-weight: 900;
  color: var(--absher) !important;
  font-size: 1.05rem;
  margin-bottom: 10px;
}
.badges{ display:flex; flex-wrap:wrap; gap:10px; }
.badge{
  padding: 8px 12px;
  border-radius: 999px;
  border: 1px solid rgba(11,107,85,0.20);
  background: rgba(11,107,85,0.08);
  font-weight: 800;
  color: var(--text) !important;
}

/* File uploader align RTL */
div[data-testid="stFileUploader"] section { direction: rtl; }

/* Result cards */
.card{
  background:#fff;
  border:1px solid var(--border);
  border-radius: 18px;
  padding: 16px 18px;
  box-shadow: 0 12px 28px rgba(0,0,0,0.04);
  margin-bottom: 14px;
}
.muted{ color: var(--muted) !important; }
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

# ---------------- Header (ONLY place to mention) ----------------
st.markdown("""
<div class="header">
  <h1>المنصة الوطنية للتحقق من المستندات</h1>
  <p>محاكاة توضيحية (Prototype) — لا تستخدم بيانات حكومية حقيقية</p>
  <p>واجهة تجريبية لعرض فكرة SQR2 ضمن مسار الأمن والذكاء الاصطناعي.</p>
</div>
""", unsafe_allow_html=True)

# ---------------- Pages ----------------
if st.session_state.page == "login":
    st.markdown('<div class="login-wrap"><div class="login-card">', unsafe_allow_html=True)
    st.markdown('<div class="login-top"><h2>تسجيل الدخول</h2></div>', unsafe_allow_html=True)
    st.markdown('<div class="login-body">', unsafe_allow_html=True)

    st.markdown('<div class="label">اسم المستخدم أو رقم الهوية</div>', unsafe_allow_html=True)
    user = st.text_input("", placeholder="اسم المستخدم أو رقم الهوية", label_visibility="collapsed")

    st.markdown('<div class="label">رمز الدخول</div>', unsafe_allow_html=True)
    pin = st.text_input("", placeholder="رمز الدخول", type="password", label_visibility="collapsed")

    if st.button("تسجيل الدخول"):
        st.session_state.logged_in = True
        goto("verify")

    st.markdown('</div></div></div>', unsafe_allow_html=True)

    # service section UNDER the login (not beside)
    st.markdown("""
    <div class="service-card">
      <div class="service-title">عن الخدمة</div>
      <div class="badges">
        <div class="badge">🔒 تعزيز موثوقية المستندات</div>
        <div class="badge">⚡ تحقق فوري خلال ثوانٍ</div>
        <div class="badge">🤖 تحليل بصمة أمنية بالذكاء الاصطناعي</div>
        <div class="badge">🔗 تكامل عبر واجهات آمنة</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

elif st.session_state.page == "verify":
    if not st.session_state.logged_in:
        goto("login")
        st.stop()

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### رفع مستند للتحقق")

    c1, c2 = st.columns([1.2, 0.8])
    with c1:
        doc_type = st.selectbox("نوع المستند", ["صك (وزارة العدل)", "هوية وطنية", "رخصة/شهادة أخرى"])
    with c2:
        if st.button("تسجيل خروج"):
            st.session_state.logged_in = False
            st.session_state.last_result = None
            goto("login")

    # شلنا مثال الرقم المرجعي بالكامل
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
    c1, c2 = st.columns(2)
    with c1:
        if st.button("إبلاغ عن المستند"):
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
            st.success("✅ تم إرسال البلاغ")
    with c2:
        if st.button("عودة"):
            goto("result")
    st.markdown("</div>", unsafe_allow_html=True)
