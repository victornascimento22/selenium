from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import time 

login_conexos = 'VVIANA'
senha_conexos = '25434472v'


# define o caminho para o driver do Chrome
driver = webdriver.Chrome()

driver.get('https://capital.conexos.cloud/imp021')

wait = WebDriverWait(driver,20)

# inserindo o login no input da tela de login do conexos
element_login_input = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/cnx-login/div/div/cnx-login-form/div/form/div[1]/input")))
element_login_input.send_keys(login_conexos)

# inserindo a senha no input da tela de login do conexos
element_password_input = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/cnx-login/div/div/cnx-login-form/div/form/div[2]/input")))
element_password_input.send_keys(senha_conexos)


# clicando no botão da tela do conexos
button_login= wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/cnx-login/div/div/cnx-login-form/div/form/button')))
button_login.click()

# localiza o botão para exportar o relatório
button_export = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[3]/div/div/div/div/div/form/div/div/div[1]/h4/div/a[1]/span/i')))

# define as datas iniciais e finais
start_date = datetime.date(2020, 1, 1)
end_date = datetime.date(2020, 12, 31)

# itera sobre as datas e exporta o relatório para cada uma
while start_date.year <= end_date.year and start_date.month <= end_date.month:

    last_day = datetime.date(start_date.year, start_date.month, 1)
    last_day = last_day.replace(day=28) + datetime.timedelta(days=4)
    last_day = last_day - datetime.timedelta(days=last_day.day)

    # loop until the number of records is less than 1000
    while True:
        element_date_from = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="dtaFechFinanceiroGEimp021"]')))
        element_date_from.clear()
        element_date_from.send_keys(start_date.strftime("%d/%m/%Y"))
        time.sleep(5)
        element_date_to = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="dtaFechFinanceiroLEimp021"]')))
        element_date_to.clear()
        time.sleep(5)
        element_date_to.send_keys(last_day.strftime("%d/%m/%Y"))
        time.sleep(5)
        
        button_search = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="collapseOne"]/div/div/div[2]/div/div/div/button[1]/span')))
        button_search.click()

        # wait for the search results to load
        time.sleep(20)

        # check the number of records
        element_num_records = driver.find_element(By.XPATH, '//*[@id="paginationControl"]/div/div/span/span[2]')
        num_records = int(element_num_records.text)

        # if there are more than 1000 records, adjust the end date and search again
        if num_records >= 1000:
            last_day = last_day - datetime.timedelta(days=1)
        else:
            break

    time.sleep(12)
    # click the export button
    button_export.click()

    # wait for the download to complete
    time.sleep(10)

    # update the start and end dates for the next iteration
    start_date = last_day + datetime.timedelta(days=1)
    end_date = end_date

# export any remaining days for the last month
while start_date.day <= end_date.day:
    last_day = end_date
    element_date_from = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="dtaFechFinanceiroGEimp021"]')))
    element_date_from.clear()
    element_date_from.send_keys(start_date.strftime("%d/%m/%Y"))
    time.sleep(5)
    element_date_to = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="dtaFechFinanceiroLEimp021"]')))
    element_date_to.clear()
    time.sleep(5)
    element_date_to.send_keys(last_day.strftime("%d/%m/%Y"))
    time.sleep(5)
    
    button_search = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="collapseOne"]/div/div/div[2]/div/div/div/button[1]/span')))
    
    time.sleep(10)
    button_search.click()

    # wait for the search results to load
    time.sleep(20)

    # click the export button
    button_export.click()

    # wait for the download to complete
    time.sleep(10)

    # update the start and end dates for the next iteration
    start_date = last_day + datetime.timedelta(days=1)