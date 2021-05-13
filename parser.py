import sys
import re
import glob
from PyPDF2 import PdfFileReader
from rich import print
import csv

def get_number(regex, text):
    match = re.search(regex, text)
    print(match)
    if match:
        number = match.group(1).replace(".","").replace(",",".")
        try:
            return int(number)
        except ValueError:
            return ""
    else:
        return ""

data = {
    "codigo": "",
    "año": "",
    "tipo": "",
    "rate": "",
    "total": "",
    "comuna": "",
    "sector": "",
    "total": "",
    "aporte_empresas_electricas": "",
    "aporte_beneficiarios": "",
    "donacion": "",
    "aporte_particulares": "",
    "recursos_propios": "",
    "otros": "",
    "beneficiarios": "",
    "empalmes": "",
}
with open("output/output.csv", "w", newline='') as f:
    w = csv.DictWriter(f, data.keys(), delimiter='\t')
    w.writeheader()

filenames = glob.glob("pdfs/*.pdf")
# print(filenames)
for idx, filename in enumerate(filenames[1491:]):
    print(filename)
    print(f"{round(idx/len(filenames),2)}% ({idx}/{len(filenames)})")
    filename_split = filename.split("_")
    codigo = filename_split[0].split("\\")[1]
    año = filename_split[1]
    tipo = filename_split[2]
    rate = filename_split[3].split(".pdf")[0]

    with open(filename, 'rb') as f:
        pdf = PdfFileReader(f)
        # ----------- PAGINA 1 ------------
        print ("PAGINA 1")
        page = pdf.getPage(0)
        text_page_1 = page.extractText()
        print(text_page_1)

        match = re.search("COMUNA(\ |\n)DE ([\w\s]+)( - REGION (DE )?\w+)?-?(REGIONAL|NACIONAL)", text_page_1)
        if match:
            print(match)
            comuna = match.group(2)
        else:
            comuna = ""
        print("------------")
        print(comuna)
        print("------------")

        match = re.search("ENERGIA / ((.|\n)* USUARIOS)3", text_page_1)
        print(match)
        sector = match.group(1)
        print("------------")
        print(sector)
        print("------------")
        # -------- PAGINA 2 ------------
        print ("PAGINA 2")
        page = pdf.getPage(1)
        text_page_2 = page.extractText()
        print(text_page_2)

        #-----------------PAGINA 3-----------------
        print ("PÁGINA 3")
        try:
            page = pdf.getPage(2)
        except:
            continue
        text_page_3 = page.extractText()
        print(text_page_3)

        match = re.search("Medida(\d+)", text_page_3)
        match2 = re.search("Medida(\d+)", text_page_2)
        if match:
            print(match)
            beneficiarios = match.group(1)
        elif match2:
            print(match2)
            beneficiarios = match2.group(1)
        else:
            beneficiarios = ""
        print("------------")
        print(beneficiarios)
        print("------------")

        match = re.search("::TOTAL(\d+)", text_page_3)
        match2 = re.search("::TOTAL(\d+)", text_page_2)
        if match:
            print(match)
            empalmes = match.group(1)
        elif match2:
            print(match2)
            empalmes = match2.group(1)
        else:
            empalmes = ""
        print("------------")
        print(empalmes)
        print("------------")



        data = {
            "codigo": codigo,
            "año": año,
            "tipo": tipo,
            "rate": rate,
            "comuna":comuna,
            "sector": sector,
            "total": get_number("TOTAL([\d|\.]+)", text_page_2),
            "aporte_empresas_electricas": get_number("APORTE EMPRESAS ELECTRICAS([\d|\.]+)", text_page_2),
            "aporte_beneficiarios": get_number("APORTE BENEFICIARIOS([\d|\.]+)", text_page_2),
            "donacion": get_number("DONACION([\d|\.]+)", text_page_2),
            "aporte_particulares": get_number("APORTE DE PARTICULARES([\d|\.]+)", text_page_2),
            "recursos_propios": get_number("RECURSOS PROPIOS([\d|\.]+)", text_page_2),
            "otros": get_number("OTROS([\d|\.]+)", text_page_2),
            "beneficiarios":beneficiarios,
            "empalmes":empalmes

        }
        print(data)

        with open("output/output.csv", "a", newline='') as f:
            w = csv.DictWriter(f, data.keys(), delimiter='\t')
            w.writerow(data)
