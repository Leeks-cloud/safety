from fpdf import FPDF
from PIL import Image, ExifTags
import tempfile

class PDF(FPDF):
    def __init__(self):
        super().__init__()
        # 나눔고딕 폰트 등록 (한글 사용 가능하도록)
        self.add_font("Nanum", "", "NanumGothic.ttf", uni=True)
        self.set_font("Nanum", "", 12)  # 기본 폰트 설정
        self.add_page()  # PDF 첫 페이지 생성

    def header_table(self, date, location, severity, recurrence, whole_img, close_img, desc_text):
        self.set_fill_color(255, 230, 230)
        self.set_font("Nanum", "", 16)

        # 제목 행
        self.cell(0, 14, "안전위험요소 사진", border=1, ln=True, align="C", fill=True)

        self.set_font("Nanum", "", 12)

        # 1행: 날짜 / 날짜값 / 심각도 / 값
        self.cell(30, 10, "날짜", border=1, align="C", fill=True)
        self.cell(80, 10, date, border=1, align="C")
        self.cell(30, 10, "심각도", border=1, align="C", fill=True)
        self.cell(50, 10, severity, border=1, align="C", ln=True)

        # 2행: 장소 / 장소값 / 재발가능성 / 값
        self.cell(30, 10, "장소", border=1, align="C", fill=True)
        self.cell(80, 10, location, border=1, align="C")
        self.cell(30, 10, "재발가능성", border=1, align="C", fill=True)
        self.cell(50, 10, recurrence, border=1, align="C", ln=True)

        # 3행: 전체사진
        self._add_image_row("전체사진", whole_img)

        # 4행: 상세사진
        self._add_image_row("상세사진", close_img)

        # 5행: 상세설명
        self._add_text_row("상세설명", desc_text)

    def _add_image_row(self, label, image_file):
        row_height = 80
        cell_label_w = 30
        cell_img_w = 160

        # 현재 위치 기억
        x = self.get_x()
        y = self.get_y()

        # 셀 먼저 그림
        self.set_fill_color(255, 230, 230)
        self.cell(cell_label_w, row_height, label, border=1, align="C", fill=True)
        self.cell(cell_img_w, row_height, "", border=1)
        self.ln(row_height)

        if image_file:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_img:
                image_file.seek(0)
                tmp_img.write(image_file.read())
                img_path = tmp_img.name

            # 이미지 열기 + EXIF 회전 보정
            img = Image.open(img_path)
            img = self._correct_image_orientation(img)
            img_w, img_h = img.size

            # ✅ 이미지 여백 설정
            padding = 5
            max_img_w = cell_img_w - 2 * padding
            max_img_h = row_height - 2 * padding

            ratio = min(max_img_w / img_w, max_img_h / img_h)
            new_w = img_w * ratio
            new_h = img_h * ratio

            img_x = x + cell_label_w + (cell_img_w - new_w) / 2
            img_y = y + (row_height - new_h) / 2

            # ✅ 회전 적용된 이미지를 임시 파일로 다시 저장
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as rotated_tmp:
                img.save(rotated_tmp.name)
                rotated_path = rotated_tmp.name

            # 이미지 삽입
            self.image(rotated_path, x=img_x, y=img_y, w=new_w, h=new_h)

    def _correct_image_orientation(self, image):
        try:
            exif = image._getexif()
            if exif:
                for tag, value in exif.items():
                    key = ExifTags.TAGS.get(tag, tag)
                    if key == "Orientation":
                        if value == 3:
                            image = image.rotate(180, expand=True)
                        elif value == 6:
                            image = image.rotate(270, expand=True)
                        elif value == 8:
                            image = image.rotate(90, expand=True)
                        break
        except Exception as e:
            print("EXIF 회전 처리 오류:", e)
        return image

    def _add_text_row(self, label, text):
        label_w = 30
        text_w = 160
        row_height = 50

        # 셀 생성
        self.set_fill_color(255, 230, 230)
        self.cell(label_w, row_height, label, border=1, align="C", fill=True)

        y = self.get_y()
        self.multi_cell(text_w, row_height, text or "(작성 내용 없음)", border=1, align="L")

        self.set_y(y + row_height)

    def export(self, output_path):
        self.output(output_path)
