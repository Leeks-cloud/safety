import streamlit as st
from datetime import date
import streamlit as st
from datetime import date
import tempfile
from utils.pdf_generator import PDF

st.set_page_config(page_title="안전위험요소 보고", layout="centered")

st.title("📋 안전위험요소 보고서 작성")
st.markdown("현장에서 위험요소를 발견했을 때, 아래 항목을 입력하세요.")

# 날짜
report_date = st.date_input("📅 날짜", value=date.today())

# 장소
location = st.text_input("📍 장소 (설치 장소 주소 기재)")

# 위험도 선택
severity = st.radio("⚠️ 심각도", ["경계", "중간", "심각"], horizontal=True)

# 재발 가능성 선택
recurrence = st.radio("♻️ 재발 가능성", ["낮음", "보통", "높음"], horizontal=True)

# 전체 사진 업로드
st.markdown("### 📷 위험요소 전체 사진")
whole_photo = st.file_uploader("전체 사진 업로드", type=["jpg", "jpeg", "png"], key="whole")

# 근접 사진 업로드
st.markdown("### 🔍 위험요소 근접 사진")
closeup_photo = st.file_uploader("근접 사진 업로드", type=["jpg", "jpeg", "png"], key="close")

# 기타 설명
etc = st.text_area("📝 기타 사항 (상세 설명)", height=150)

# PDF 생성 버튼
generate = st.button("📄 PDF 리포트 생성")

if generate:
    if not whole_photo or not closeup_photo:
        st.warning("📸 사진을 모두 업로드해주세요.")
    else:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
            pdf = PDF()
            pdf.header_table(
                str(report_date),
                location,
                severity,
                recurrence,
                whole_photo,
                closeup_photo,
                etc
            )
            pdf.export(tmpfile.name)

        with open(tmpfile.name, "rb") as f:
            st.download_button(
                label="📥 PDF 다운로드",
                data=f,
                file_name=f"안전위험요소_{report_date}.pdf",
                mime="application/pdf"
            )
