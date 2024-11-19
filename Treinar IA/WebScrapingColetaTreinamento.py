import undetected_chromedriver as uc

from selenium import webdriver  
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager

service = Service(ChromeDriverManager().install())  

options = webdriver.ChromeOptions()

driver = uc.Chrome(options=options)

empresa = input("Digite a empresa que deseje fazer scraping: ")

quantidade_pagina = int(input("Digite a quantidade de páginas que deseja pegar: "))

dicionarioEmpresas = {
    "positivo" : "positivo-informatica",
    "habibs" : "habibs"
}

for pagina in range(quantidade_pagina):
    url = f"https://www.reclameaqui.com.br/empresa/{dicionarioEmpresas.get(empresa)}/lista-reclamacoes/?pagina={pagina + 1}"
    driver.get(url)
    
    WebDriverWait(driver, 10).until(lambda d: len(d.find_elements(By.CLASS_NAME, 'sc-1pe7b5t-1')) > 0)
    
    reclamacoes = driver.find_elements(By.CLASS_NAME, 'sc-1pe7b5t-1')
    
    for index in range(len(reclamacoes)):
        try:
            reclamacoes = driver.find_elements(By.CLASS_NAME, 'sc-1pe7b5t-1')
            reclamacao = reclamacoes[index]

            driver.execute_script("arguments[0].click();", reclamacao)
            
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'sc-lzlu7c-3')))
            
            titulo = driver.find_element(By.CLASS_NAME, 'sc-lzlu7c-3').text
            reclamacao = driver.find_element(By.CLASS_NAME, 'sc-lzlu7c-17').text.replace('\n', ' ')

            with open("teste.txt", "a") as arquivo:
                arquivo.write(f"{titulo} {reclamacao}\n---\n")
            
            driver.get(url)
            
            WebDriverWait(driver, 10).until(lambda d: len(d.find_elements(By.CLASS_NAME, 'sc-1pe7b5t-1')) > 0)
        
        except:
            driver.get(url)

driver.quit()