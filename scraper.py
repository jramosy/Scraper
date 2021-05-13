from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import sys
import glob
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException

chrome_options = webdriver.ChromeOptions()
prefs = {'download.default_directory' : 'C:\\Users\\josef\\OneDrive\\Escritorio\\scraper\\pdfs'}
chrome_options.add_experimental_option('prefs', prefs)


with open("ultimo_codigo.txt", "r") as f:
    ultimo_codigo = f.read()       
codigos = []
flag = 0
with open("input/codigos.csv", "r") as f:
    for line in f:
        codigo = line.replace("\n","")
        if ultimo_codigo != "":
            if codigo == ultimo_codigo and flag == 0:
                flag = 1
        else:
            flag = 1
        if flag:
            codigos.append(codigo)

driver = webdriver.Chrome('chromedriver.exe', options=chrome_options)
for codigo_idx, codigo in enumerate(codigos):
    with open("ultimo_codigo.txt", "w") as f:
        f.write(codigo)
    driver.get('https://bip.ministeriodesarrollosocial.gob.cl/bip2-consulta/app/parent-flow;jsessionid=C773C62FB576AD3FB6BF3C5883FB83CC?execution=e1s2');
    cajita = WebDriverWait(driver, 5000).until(EC.presence_of_element_located((By.XPATH, '/html/body/form/div[3]/div/div/table[1]/tbody/tr[2]/td[2]/input')))
    cajita.clear()
    cajita.send_keys(codigo[:-2])
    boton = driver.find_element(By.XPATH, '/html/body/form/div[3]/div/div/div[2]/div/div/button[2]')
    boton.click()
    WebDriverWait(driver, 5000).until(EC.presence_of_element_located((By.XPATH, '/html/body/form/div[3]/div/div[1]/div/div/div[1]/div[4]/span[3]/span')))
    paginas = driver.find_elements(By.XPATH, '/html/body/form/div[3]/div/div[1]/div/div/div[1]/div[4]/span[3]/span')
    for idx, pagina in enumerate(paginas):
        pagina.click()
        WebDriverWait(driver, 5000).until(EC.presence_of_element_located((By.XPATH, f'/html/body/form/div[3]/div/div[1]/div/div/div[1]/div[4]/span[3]/span[{idx+1}][contains(@class, "ui-state-active")]')))
        trs = driver.find_elements(By.XPATH, '/html/body/form/div[3]/div/div[1]/div/div/div[1]/div[2]/table/tbody/tr')
        for tr in trs:
            link = tr.find_element(By.XPATH, 'td[2]/a')
            año = tr.find_element(By.XPATH, 'td[3]').text
            etapa_actual = tr.find_element(By.XPATH, 'td[2]').text.split("-")[-1]
            rate = tr.find_element(By.XPATH, 'td[8]').text
            existing_filename = glob.glob(f'pdfs\\{codigo}_{año}_{etapa_actual}_{rate}.pdf')
            if len(existing_filename) != 0:
                print("Existing Filename:", existing_filename)
            if int(año) >= 2005 and len(existing_filename) == 0:
                link.click()
                try:
                    boton2 = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form/div[3]/div/div[2]/div[2]/div[2]/button[1]')))
                    boton2.click()
                    while True:
                        filenames = glob.glob("pdfs/Ficha_IDI*.PDF")
                        if filenames:
                            new_filename = f'pdfs\\{codigo}_{año}_{etapa_actual}_{rate}.pdf'
                            os.rename(filenames[0], new_filename)
                            print(f"{round(codigo_idx/len(codigos)*100,1)}% ({codigo_idx}/{len(codigos)})", new_filename)
                            break
                except WebDriverException:
                    boton3 = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[2]/button')
                    boton3.click()
                    time.sleep(1)
                    continue

