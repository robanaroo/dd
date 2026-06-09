import streamlit as st
from cryptography.fernet import Fernet

# 1. إعدادات الصفحة، العنوان، والأيقونة
st.set_page_config(
    page_title="تشفير END - TO - END", 
    page_icon="🔐", 
    layout="centered"
)

# 2. إضافة صورة معبرة عن العمل (تشفير وبيانات)
image_url = "https://images.unsplash.com/photo-1563986768609-322da13575f3?auto=format&fit=crop&w=800&q=80"
st.image(image_url, use_container_width=True)

# 3. العناوين الرئيسية للتطبيق
st.title("🔐 تطبيق محاكاة: تشفير END - TO - END")
st.subheader("قناة اتصال آمنة ومباشرة بين ربانا ونجلاء")
st.write("هذا التطبيق يشرح عملياً كيف يتم تشفير الرسائل من الطرف المرسل وفك تشفيرها فقط عند الطرف المستقبل، دون أن يتمكن أي طرف ثالث من قراءتها.")

# 4. توليد أو استرجاع مفتاح التشفير المشترك (مخزن في ذاكرة الجلسة)
if 'secret_key' not in st.session_state:
    st.session_state.secret_key = Fernet.generate_key()

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# إنشاء كائن التشفير
fernet = Fernet(st.session_state.secret_key)

# صندوق جانبي لإظهار مفتاح التشفير (للتوضيح العملي فقط)
with st.sidebar:
    st.header("🔑 إدارة المفاتيح")
    st.info("هذا هو المفتاح السري المشترك بين ربانا ونجلاء لتشفير وفك تشفير الرسائل:")
    st.code(st.session_state.secret_key.decode(), language="text")
    
    # زر لإعادة ضبط المحادثة
    if st.button("🗑️ مسح المحادثة وتغيير المفتاح"):
        del st.session_state.secret_key
        del st.session_state.chat_history
        st.rerun()

# 5. منطقة إرسال الرسائل (تحديد المرسل والمستقبل)
st.write("---")
st.markdown("### 💬 إرسال رسالة جديدة")

# اختيار من يرسل الرسالة ومن يستقبلها
sender = st.radio("اختر الطرف الذي يريد إرسال الرسالة الآن:", ("ربانا", "نجلاء"), horizontal=True)
receiver = "نجلاء" if sender == "ربانا" else "ربانا"

# حقل إدخال النص
user_message = st.text_input(f"الرسالة من [{sender}] إلى [{receiver}]:", key="msg_input")

if st.button("تشفير وإرسال الرسالة 🚀"):
    if user_message.strip() != "":
        # عملية التشفير العملي (تحويل النص إلى بايتس ثم تشفيره)
        encrypted_bytes = fernet.encrypt(user_message.encode())
        
        # حفظ البيانات في تاريخ المحادثة
        st.session_state.chat_history.append({
            "sender": sender,
            "receiver": receiver,
            "original_text": user_message,
            "encrypted_text": encrypted_bytes.decode()
        })
        st.rerun()
    else:
        st.warning("الرجاء كتابة نص الرسالة أولاً!")

# 6. عرض النتائج (المنظور الآمن ضد منظور المخترق)
st.write("---")
tab1, tab2 = st.tabs(["📥 منظور المستخدمين (ربانا ونجلاء)", "🕵️‍♂️ منظور المتصنت أو المخترق (البيانات المارة بالشبكة)"])

with tab1:
    st.markdown("#### 💬 شاشة المحادثة بعد فك التشفير التلقائي")
    if not st.session_state.chat_history:
        st.caption("لا توجد رسائل متبادلة حالياً.")
    else:
        for msg in st.session_state.chat_history:
            # محاكاة فك التشفير عند الطرف الآخر
            decrypted_msg = fernet.decrypt(msg["encrypted_text"].encode()).decode()
            
            if msg["sender"] == "ربانا":
                st.markdown(f"**👩‍💼 ربانا** ⬅️ **👩‍💻 نجلاء:** {decrypted_msg}")
            else:
                st.markdown(f"**👩‍💻 نجلاء** ⬅️ **👩‍💼 ربانا:** {decrypted_msg}")

with tab2:
    st.markdown("#### 📡 حزم البيانات المشفرة داخل السيرفر / الشبكة")
    st.error("إذا حاول أي شخص اعتراض المحادثة في منتصف الطريق، فلن يرى الأسماء ولا النصوص، بل سيرى هذا التشفير المعقد فقط:")
    if not st.session_state.chat_history:
        st.caption("الشبكة فارغة، لا توجد بيانات مارة.")
    else:
        for msg in st.session_state.chat_history:
            st.code(f"From: [SECRET] -> To: [SECRET]\nData: {msg['encrypted_text']}", language="text")
