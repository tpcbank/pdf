from fillpdf import fillpdfs
import os 
from datetime import datetime
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

# Register THSarabunNEW Font


today = datetime.now()
folder_name = today.strftime("%Y-%m-%d")
os.makedirs(folder_name, exist_ok=True)



data = ["01-บต.31.pdf","สวัสดีครับ","yaker","1","123/32","yaker","1","123/32","yaker","1","Yes","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","johnasdasdasdasdasdasdasdasdsadasdasdasdasdasdasdasdasdas","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","johnasdasdasdasdasdasdasdasdsadasdasdasdasdasdasdasdasdas","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","johnasdasdasdasdasdasdasdasdsadasdasdasdasdasdasdasdasdas","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32","yaker","1","123/32"]

form_fields = list(fillpdfs.get_form_fields(f"template/{data[0]}").keys())

print(form_fields)

data_dict = {}
for i in range(len(form_fields)):
    data_dict.update({form_fields[i]:data[i+1].encode('utf-8').decode('utf-8')})


fillpdfs.write_fillable_pdf(f"template/{data[0]}",f"{folder_name}/{data[0].split("pdf")[0]}{folder_name}.pdf",data_dict,True)
