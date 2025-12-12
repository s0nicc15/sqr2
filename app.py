import streamlit as st
from datetime import datetime

st.set_page_config(page_title="المنصة الوطنية للتحقق", page_icon="✅", layout="centered")

# ---------- Styling (Absher-ish dark green) ----------
st.markdown("""
<style>
:root{
  --bg:#0b2a24;
  --card:#0f3a32;
  --text:#e8fff6;
  --muted:#bde6d7;
  --accent:#19b394;
  --danger:#ff5a5f;
}
.stApp { background: var(--bg); color: var(--text); }
h1,h2,h3,p,li,div { color: var(--text) !important; }
.block-container { padding-top: 2rem; }
.card{
  background: var(--card);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 16px;
  padding: 16px;
  margin-bottom: 14px;
}
.badge{
  display:inline-block;
  padding:6px 10px;
  border-radius:999px;
  font-size: 0.9rem;
  background: rgba(25,179,148,0.16);
  border: 1px solid rgba(25,179,148,0.35);
  color: var(--text);
}
.muted{ color: var(--muted) !important; }
hr{ border-color: rgba(255,255,255,0.12); }
.stButton>button{
  background: var(--accent);
  color: #062019;
  border: 0;
  border-radius: 12px;
  padding: 10px 14px;
  font-weight: 700;
}
.stTextInput>div>div>input, .stNumberInput>div>div>input, .stSelectbox>div>div>div{
  border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# ---------- Session ----------
if "page" not in st.session_state:
    st.session_state.page = "login"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "last_result" not in st.session_state:
    st.session_state.last_result = None

# ---------- Header ----------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("## مرحبًا بكم في **المنصة الوطنية للتحقق من المستندات**")
st.markdown('<span class="badge">محاكاة توضيحية (Prototype) — لا تستخدم بيانات حكومية حقيقية</span>', unsafe_allow_html=True)
st.markdown('<p class="muted">واجهة تجريبية لعرض فكرة SQR2 ضمن مسار الأمن والذكاء الاصطناعي.</p>', unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# ---------- Helpers ----------
def goto(page):
    st.session_state.page = page

def fake_verify(doc_type, filename):
    # محاكاة بسيطة حسب النوع
    if doc_type == "صك (وزارة العدل)":
        return {
            "status": "أصلي",
            "score": 0.93,
            "issuer": "وزارة العدل",
            "copies": 2,
            "usage_count": 10,
            "used_at": ["وزارة الموارد البشرية", "وزارة التجارة", "وزارة الداخلية"],
            "notes": "تم التحقق من البصمات الأمنية (محاكاة) ومطابقة النموذج المرجعي."
        }
    elif doc_type == "هوية (بطاقة)":
        return {
            "status": "مشتبه",
            "score": 0.41,
            "issuer": "الأحوال المدنية",
            "copies": None,
            "usage_count": 0,
            "used_at": [],
            "notes": "تم رصد مؤشرات تزوير/تلاعب بصري (محاكاة) — يوصى بالمراجعة والإبلاغ."
        }
    else:
        return {
            "status": "غير مؤكد",
            "score": 0.66,
            "issuer": "جهة غير محددة",
            "copies": None,
            "usage_count": 3,
            "used_at": ["جهة حكومية (محاكاة)"],
            "notes": "نتيجة أولية (محاكاة) — تحتاج عينات مرجعية أكثر لتحسين الدقة."
        }

# ---------- Pages ----------
if st.session_state.page == "login":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### تسجيل الدخول")
    st.markdown('<p class="muted">ادخلي أي رقم/اسم — الهدف عرض تجربة المستخدم فقط.</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        user = st.text_input("اسم المستخدم / رقم الهوية", placeholder="مثال: 1234567890")
    with col2:
        pin = st.text_input("رمز الدخول", placeholder="أي أرقام", type="password")

    if st.button("دخول"):
        st.session_state.logged_in = True
        goto("verify")

    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.page == "verify":
    if not st.session_state.logged_in:
        goto("login")
        st.stop()

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### رفع مستند للتحقق")
    st.markdown('<p class="muted">ارفع أي صورة (JPG/PNG/PDF صورة). سيتم عرض نتيجة محاكاة.</p>', unsafe_allow_html=True)

    doc_type = st.selectbox("نوع المستند", ["صك (وزارة العدل)", "هوية (بطاقة)", "رخصة/شهادة أخرى"])
    uploaded = st.file_uploader("ارفع صورة المستند", type=["png", "jpg", "jpeg"])

    colA, colB = st.columns([1,1])
    with colA:
        if st.button("تحقق الآن") and uploaded is not None:
            res = fake_verify(doc_type, uploaded.name)
            res["filename"] = uploaded.name
            res["time"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            st.session_state.last_result = res
            goto("result")
    with colB:
        if st.button("تسجيل خروج"):
            st.session_state.logged_in = False
            st.session_state.last_result = None
            goto("login")

    if uploaded is not None:
        st.image(uploaded, caption="معاينة المستند (محاكاة)", use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.page == "result":
    res = st.session_state.last_result
    if not res:
        goto("verify")
        st.stop()

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### نتيجة التحقق")
    st.markdown(f'<p class="muted">الملف: <b>{res["filename"]}</b> — وقت التحقق: {res["time"]}</p>', unsafe_allow_html=True)
    st.markdown("---")

    if res["status"] == "أصلي":
        st.success("✅ التحقق: المستند **أصلي ورسمي** (محاكاة)")
    elif res["status"] == "مشتبه":
        st.error("⚠️ التحقق: **مؤشرات اشتباه بالتزوير/التلاعب** (محاكاة)")
    else:
        st.warning("ℹ️ التحقق: **نتيجة غير مؤكدة** (محاكاة)")

    st.markdown(f"**الجهة المُصدِرة:** {res['issuer']}")
    if res["copies"] is not None:
        st.markdown(f"**عدد النسخ الصادرة (محاكاة):** {res['copies']}")
    st.markdown(f"**عدد مرات الاستخدام (محاكاة):** {res['usage_count']}")

    if res["used_at"]:
        st.markdown("**تم استخدامه لدى (محاكاة):**")
        for x in res["used_at"]:
            st.markdown(f"- {x}")

    st.markdown(f"**ملاحظات النظام:** {res['notes']}")
    st.markdown(f"**نسبة الثقة (محاكاة):** {int(res['score']*100)}%")

    st.markdown("---")
    st.markdown("### هل تريد الإبلاغ عن المستند المدخل؟")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("نعم، إبلاغ"):
            goto("report")
    with c2:
        if st.button("رجوع لرفع مستند"):
            goto("verify")

    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.page == "report":
    res = st.session_state.last_result

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### نموذج الإبلاغ (محاكاة)")
    reason = st.selectbox("سبب الإبلاغ", ["اشتباه تزوير", "اختلاف بيانات", "مستند منتحل", "أخرى"])
    details = st.text_area("ملاحظات إضافية", placeholder="اكتب/ي تفاصيل مختصرة...")

    if st.button("إرسال البلاغ"):
        st.success("✅ تم إرسال البلاغ (محاكاة). شكرًا لتعاونك.")
        st.markdown('<p class="muted">سيتم ربط الإبلاغ بالجهة المختصة عند اعتماد النظام ودمجه رسميًا.</p>', unsafe_allow_html=True)

    if st.button("عودة للنتيجة"):
        goto("result")
    st.markdown("</div>", unsafe_allow_html=True)
