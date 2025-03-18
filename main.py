import time
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
chrome_options.debugger_address = "127.0.0.1:9222"  

chromedriver_path = "/usr/bin/chromedriver"

driver = webdriver.Chrome(service=Service(chromedriver_path), options=chrome_options)

df = pd.read_csv("offers-import.csv", sep=";")
data = []

for sku in df["product-id"]:
    try:
        driver.get("https://www.leroymerlin.pt/")
        time.sleep(random.uniform(3, 5))

        wait = WebDriverWait(driver, 10)

        try:
            search_bar = wait.until(EC.visibility_of_element_located((By.ID, "search-autocomplete__input--a11y-skip-link")))
            search_bar.send_keys(sku)
            search_bar.send_keys(Keys.RETURN)
            time.sleep(random.uniform(2, 4))
        except Exception as e:
            print(f"Erro ao encontrar a barra de pesquisa: {e}")
            continue

        url = driver.current_url

        try:
            price = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "m-price__line"))).text
        except:
            price = "Preço não encontrado"

        try:
          name = wait.until(
          EC.visibility_of_element_located((By.CLASS_NAME, "l-product-detail-presentation__title"))).text
        except:
          name = "Nome não encontrado"

        try:
            seller = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "m-3p-seller__seller-link"))).text
        except:
            seller = "Vendedor não encontrado"

        data.append({"product-id": sku, "url": url, "price": price, "name": name, "seller": seller})

    except Exception as e:
        print(f"Erro ao processar o SKU {sku}: {e}")

    time.sleep(random.uniform(2, 5))

driver.quit()

output_df = pd.DataFrame(data)
output_df.to_csv("offers-output.csv", index=False, header=not df.empty)

print("Finalizado")
