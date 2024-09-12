from fillpdf import fillpdfs
import os
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from PyPDF2 import PdfReader, PdfWriter, PdfMerger

# Register THSarabunNEW Font
pdfmetrics.registerFont(TTFont('THSarabunNEW', 'font/THSarabunNew.ttf'))

# สร้างโฟลเดอร์สำหรับเก็บไฟล์ output
today = datetime.now()
folder_name = today.strftime("%Y-%m-%d")
os.makedirs(folder_name, exist_ok=True)

# ข้อมูลที่ต้องการแทรก
data = ["02-บต.46.pdf","สวัสดีครับ","yaker","1","123/32","yaker","1","123/32","yaker","1","Yes","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","johnasdasdasdasdasdasdasdasdsadasdasdasdasdasdasdasdasdas","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","johnasdasdasdasdasdasdasdasdsadasdasdasdasdasdasdasdasdas","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","johnasdasdasdasdasdasdasdasdsadasdasdasdasdasdasdasdasdas","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32"]


# ดึงฟิลด์ฟอร์มจาก PDF
form_fields = fillpdfs.get_form_fields(f"template/{data[0]}")
form_field_keys = list(form_fields.keys())
print("Form fields:", form_field_keys)

# เตรียมข้อมูลฟอร์มที่ต้องการเติมลงไป
data_dict = {}
for i in range(len(form_field_keys)):
    data_dict[form_field_keys[i]] = data[i + 1]

# เติมข้อมูลฟอร์มลงใน PDF โดยใช้ fillpdfs
filled_pdf_path = f"{folder_name}/{data[0].split('pdf')[0]}{folder_name}.pdf"
fillpdfs.write_fillable_pdf(f"template/{data[0]}", filled_pdf_path, data_dict, flatten=False)

# สร้าง overlay ด้วยฟอนต์ THSarabunNEW
def create_overlay(output_path, form_fields, data_dict):
    c = canvas.Canvas(output_path)
    c.setFont("THSarabunNEW", 12)

    # ใช้ชื่อฟิลด์และข้อมูลเพื่อสร้างข้อความที่ต้องการ (ปรับตำแหน่ง x, y ตามฟอร์มฟิลด์)
    x_position = 100  # ตำแหน่ง x
    y_position = 750  # ตำแหน่ง y เริ่มต้น
    
    for key in form_fields:
        if key in data_dict:
            value = data_dict[key]
            c.drawString(x_position, y_position, value)
            y_position -= 20  # เลื่อนตำแหน่ง y ลงมาแต่ละบรรทัด

    c.save()

# สร้าง overlay ด้วยข้อมูลจาก data_dict
overlay_pdf_path = f"{folder_name}/overlay.pdf"
create_overlay(overlay_pdf_path, form_fields, data_dict)

# ผสม PDF ที่ถูกเติมฟอร์มแล้วกับ overlay ที่มีฟอนต์ THSarabunNEW
def merge_pdfs(input_pdf, overlay_pdf, output_pdf):
    input_reader = PdfReader(input_pdf)
    overlay_reader = PdfReader(overlay_pdf)
    pdf_writer = PdfWriter()

    for page_number in range(len(input_reader.pages)):
        input_page = input_reader.pages[page_number]
        overlay_page = overlay_reader.pages[0]  # overlay มีแค่หน้าเดียวในกรณีนี้

        input_page.merge_page(overlay_page)
        pdf_writer.add_page(input_page)

    with open(output_pdf, "wb") as output_file:
        pdf_writer.write(output_file)

# เรียกใช้ฟังก์ชัน merge_pdfs
final_pdf_path = f"{folder_name}/final_{data[0]}"
merge_pdfs(filled_pdf_path, overlay_pdf_path, final_pdf_path)

print(f"PDF ที่เสร็จสมบูรณ์อยู่ที่: {final_pdf_path}")
