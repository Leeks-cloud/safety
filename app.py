import streamlit as st
from datetime import date
import tempfile
from utils.pdf_generator import PDF

st.set_page_config(page_title="안전위험요소 보고", layout="centered")

st.title("📋 안전위험요소")

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

# 선택 항목 리스트
options = [
    "이동용 사다리로 추락 위험이 높은 경우", 
    "주정차가 불가능한 도로 및 터널에 설치된 경우", 
    "안전난간이 없는 지붕 위 설치된 경우", 
    "감염병으로 출입이 불가능한 지역", 
    "기타 위험국소"
]

# 선택항목을 선택할 때 사용되는 selectbox 위젯
selected_option = st.selectbox("선택 항목", options)

# 선택에 따라 추가 정보 표시 및 내용 수집
additional_info = f"선택항목: {selected_option}\n"  # 선택 항목 추가
auto_description = ""  # 자동으로 추가되는 설명 초기화

# 🔑 선택 옵션에 따라 조건 처리
if selected_option == "이동용 사다리로 추락 위험이 높은 경우":
    st.write("사다리 유형 선택")
    
    ladder_type = st.radio("사다리 유형을 선택하세요:", ["A자형 사다리", "비 A자형 사다리"])
    additional_info += f"사다리 유형: {ladder_type}\n"

    if ladder_type == "A자형 사다리":
        st.write("✔️ 안전장구류 체크리스트")
        safety_gear = ["안전모", "안전화", "안전대", "안전고리", "보호장갑"]
        checked_items = []
        columns = st.columns(len(safety_gear))

        for idx, item in enumerate(safety_gear):
            with columns[idx]:
                if st.checkbox(item, value=True, key=f"safety_{idx}"):
                    checked_items.append(item)
        
        if checked_items:
            auto_description += "A형 사다리를 이용하여 안전에 유의하여 검사 진행\n안전장구류 착용 확인: " + ", ".join(checked_items) + "\n설명추가 : "
        else:
            auto_description += "안전장구류 착용 확인: 없음 -> ⚠️안전장구류 필수 착용 요망\n"

    else:  # 비 A자형 사다리일 경우
        warning_message = "⚠️ 현재 비 A자형 사다리 사용 중 - A자형 사다리로 변경 후 검사 요망!\n"
        auto_description += warning_message

elif selected_option == "주정차가 불가능한 도로 및 터널에 설치된 경우":
    st.write("🛤️ 우회로 확인")
    
    detour_option = st.radio("우회로 존재 여부를 선택하세요:", ["우회로 있음", "우회로 없음"])
    additional_info += f"우회로 여부: {detour_option}\n"

    if detour_option == "우회로 있음":
        auto_description += "다른 우회로: 있음 -> 우회로를 통해 도보로 이동 후 검사 진행\n"
    else:
        auto_description += "다른 우회로: 없음 -> 안테나가 잘 보이는 위치에서 OTA측정 진행\n"

    st.write("✔️ 안전장구류 체크리스트")
    safety_gear = ["안전모", "안전화", "안전대", "안전고리", "보호장갑"]
    checked_items = []
    columns = st.columns(len(safety_gear))

    for idx, item in enumerate(safety_gear):
        with columns[idx]:
            if st.checkbox(item, value=True, key=f"safety_{idx}_detour"):
                checked_items.append(item)
    
    if checked_items:
        auto_description += "안전장구류 착용 확인: " + ", ".join(checked_items) + "\n설명추가 : "
    else:
        auto_description += "안전장구류 착용 확인: 없음 -> ⚠️안전장구류 필수 착용 요망\n"

elif selected_option == "안전난간이 없는 지붕 위 설치된 경우":
    st.write("📡 식별 가능 여부 확인")
    
    identify_option = st.radio("식별 가능 여부를 선택하세요:", ["식별 가능", "식별 불가능"])
    additional_info += f"식별 가능 여부: {identify_option}\n"

    if identify_option == "식별 가능":
        auto_description += "식별 가능: 식별 가능한 대조검사 진행 후 OTA검사 시행\n"
    else:
        auto_description += "식별 불가능: OTA 검사 시행 후 입회자에게 정보를 요구하여 대조검사 시행\n"

    st.write("✔️ 안전장구류 체크리스트")
    safety_gear = ["안전모", "안전화", "안전대", "안전고리", "보호장갑"]
    checked_items = []
    columns = st.columns(len(safety_gear))

    for idx, item in enumerate(safety_gear):
        with columns[idx]:
            if st.checkbox(item, value=True, key=f"safety_{idx}_roof"):
                checked_items.append(item)
    
    if checked_items:
        auto_description += "안전장구류 착용 확인: " + ", ".join(checked_items) + "\n설명추가 : "
    else:
        auto_description += "안전장구류 착용 확인: 없음 -> ⚠️안전장구류 필수 착용 요망\n"

elif selected_option == "감염병으로 출입이 불가능한 지역":
    auto_description = "⚠️검사 연기 후 감염 위험요소 해소 후 재검사 시행 예정\n"

elif selected_option == "기타 위험국소":
    auto_description = "상세설명 : "

# 기타 설명 입력창에 자동으로 메시지를 삽입
etc = st.text_area("📝추가설명", value=auto_description, height=150)

if etc:
    etc = etc.replace('\n', '\n')

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
                additional_info + etc
            )
            pdf.export(tmpfile.name)

        with open(tmpfile.name, "rb") as f:
            st.download_button(
                label="📥 PDF 다운로드",
                data=f,
                file_name=f"안전위험요소_{report_date}.pdf",
                mime="application/pdf"
            )
