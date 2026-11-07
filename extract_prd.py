import pdfplumber, sys
sys.stdout.reconfigure(encoding='utf-8')
pdf = pdfplumber.open('Portfolio Website PRD \u2014 Edison, Data Analyst.pdf')
for i, p in enumerate(pdf.pages):
    t = p.extract_text()
    if t:
        print(f'--- PAGE {i+1} ---')
        print(t)
