import pdfplumber, sys
sys.stdout.reconfigure(encoding='utf-8')
pdf = pdfplumber.open('Edison_Data_Analyst_Resume (2).pdf')
for i, p in enumerate(pdf.pages):
    t = p.extract_text()
    if t:
        print(f'--- PAGE {i+1} ---')
        print(t)
