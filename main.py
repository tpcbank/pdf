import os
import json
from datetime import datetime
from fillpdf import fillpdfs
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PyPDF2 import PdfMerger

# ฟังก์ชันเพื่อประมวลผลข้อมูลและสร้างไฟล์ PDF
def process_data():
    today = datetime.now()
    folder_name = today.strftime("%Y-%m-%d")
    timestamp = today.strftime("%H%M%S")
    os.makedirs(folder_name, exist_ok=True)

    # โหลดข้อมูลจาก data.json
    with open('data.json', 'r', encoding='utf-8') as file:
        data_list = json.load(file)

    output_pdfs = []

    # วนลูปผ่านแต่ละชุดข้อมูลใน data.json
    for idx, data in enumerate(data_list):
        template = data[0]
        form_fields = list(fillpdfs.get_form_fields(f"template/{template}").keys())

        # สร้าง dictionary สำหรับข้อมูลฟอร์ม
        data_dict = {}
        for i in range(len(form_fields)):
            data_dict[form_fields[i]] = data[i+1]

        # สร้างชื่อไฟล์ PDF ออกมา
        file_name = f"{template.split('.pdf')[0]}-{timestamp}-{idx+1}.pdf"
        output_pdf_path = os.path.join(folder_name, file_name)

        # สร้างไฟล์ PDF
        fillpdfs.write_fillable_pdf(
            f"template/{template}",
            output_pdf_path,
            data_dict,
            flatten=True
        )
        print(f"สร้างไฟล์ PDF สำเร็จ: {output_pdf_path}")
        output_pdfs.append(output_pdf_path)

    # ถ้าสร้างไฟล์ PDF มากกว่า 1 ไฟล์ ให้ทำการรวมไฟล์
    if len(output_pdfs) > 1:
        output_name_merge = f"merged_{template.split('.pdf')[0]}-{timestamp}-{idx+1}.pdf"
        merge_pdfs(folder_name, output_pdfs,output_name_merge)
    else:
        print(f"มีไฟล์เดียว: {output_pdfs[0]} ไม่จำเป็นต้องรวมไฟล์")

    return output_pdfs

# ฟังก์ชันเพื่อรวมไฟล์ PDF
def merge_pdfs(folder_name, output_pdfs, output_name):
    pdf_merger = PdfMerger()

    # เพิ่มไฟล์ PDF ที่สร้างขึ้นไปยัง PdfMerger
    for pdf in output_pdfs:
        pdf_merger.append(pdf)

    # บันทึกไฟล์ PDF ที่รวมแล้ว
    merged_pdf_path = os.path.join(folder_name, output_name)
    with open(merged_pdf_path, 'wb') as merged_pdf:
        pdf_merger.write(merged_pdf)

    print(f"สร้างไฟล์ PDF ที่รวมกันแล้ว: {merged_pdf_path}")

# ตัวจัดการเหตุการณ์สำหรับการเปลี่ยนแปลงไฟล์
class FileChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith('data.json'):
            print("ตรวจพบการเปลี่ยนแปลงใน data.json, กำลังประมวลผล...")
            process_data()

# ฟังก์ชันหลักเพื่อเริ่มการเฝ้าดูไฟล์
if __name__ == "__main__":
    event_handler = FileChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)  # เฝ้าดูในไดเรกทอรีปัจจุบัน
    observer.start()

    try:
        print("กำลังเฝ้าดูการเปลี่ยนแปลงใน data.json. กด Ctrl+C เพื่อออก.")
        while True:
            pass  # รักษาสคริปต์ให้อยู่ในสถานะทำงาน
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
