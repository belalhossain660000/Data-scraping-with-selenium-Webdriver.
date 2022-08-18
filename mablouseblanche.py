from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import csv
import time

f = open('urls.txt', 'r')
urls = f.readlines()
urls = list(set([url.replace("\n", '') for url in urls]))
print(len(urls))
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.maximize_window()

for link in urls:
    driver.get(link)
    get_dr_link = driver.find_elements("xpath", "//div[@class='noSlotThisWeek']//h2//a")
    for dlink in get_dr_link:
        dlink_f = dlink.get_attribute('href')
        f = open('dr_list.txt', 'a', encoding='utf-8')
        f.write(str(dlink_f)+"\n")
        f.close()
    time.sleep(1)

counter = 0
for dr_details in urls:
    driver.get(dr_details)
    name = driver.find_element("xpath", "//h1").text
    image_url = driver.find_element("xpath", "//figure//img").get_attribute('src')
    full_address = driver.find_element("xpath", "//h6[text()='Adresse principale']/parent::li").text.replace('Adresse principale', '').replace('\n', ' ')
    zip_code = ""
    c = full_address.split()
    for elem in c:
        if elem.isdigit():
            if len(elem) > 3:
                zip_code += elem
    try:
        siren = driver.find_element("xpath", "//i[@class='icon-user-md']/parent::li").text.replace("n° SIREN :", "").replace(" ", '').replace(",", '')
    except:
        siren = "null"
    try:
        finess = driver.find_element("xpath", "//i[@class='icon-hospital']/parent::li").text.replace("n° FINESS :", "").replace(" ", '').replace(",", '')
    except:
        finess = "null"
    find_phone_number = driver.find_element("xpath", "//a[@class='nav-link']")
    try:
        adeli1 = driver.find_element("xpath", "//h6[text()='Informations Légales']/parent::li").text.split()
        adeli = adeli1[-1]
    except:
        adeli = "null"
    find_phone_number.click()
    time.sleep(1)
    phone_number = driver.find_element("xpath", "//i[@class='icon-phone']/parent::li//a[@class='link']").text
    try:
        mail = driver.find_element("xpath", "//i[@class='icon-mail-4']").text
    except:
        mail = "null"
    try:
        fax = (driver.find_element("xpath", "//i[@class='icon-print']/parent::li").text.replace("n° Fax :","")).replace(" ",'').replace(",",'')
    except:
        fax = "null"
    job = ""
    counter += 1
    if counter <= 201:
        job += ("Infirmier".upper())
        job += ("Medecin_generaliste".upper())
    details_list = [dr_details.replace("\n",''), name, job, image_url, full_address, zip_code, phone_number, adeli, mail, siren, finess, fax]
    print(details_list)
    print(counter)
    f = open('details_list.csv', 'a',newline='', encoding='utf-8')
    writer = csv.writer(f)
    writer.writerow(details_list)
    f.write(str(details_list) + "\n")
    f.close()
driver.close()
