from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import csv
import time
  
text = input("Enter search query: ").replace(" ", "+")
# ts stores the time in seconds
ts = time.time()
browser = webdriver.Firefox()
browser.get("https://www.google.com/search?tbs=lf:1,lf_ui:14&tbm=lcl&q="+text)
delay = 3 # seconds
try:
    business = []
    businessData = [[]]
    data = []
    header = ["Business Name", "Address", "Phone"]
    x = 0
    stop = 0
    while stop == 0:
        try:
            WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'rl_full-list')))
            for business in browser.find_elements(By.CLASS_NAME, "VkpGBb"):
                try:
                    business.find_element(By.CLASS_NAME, "BSaJxc")
                except NoSuchElementException:
                    print("FOUND BUSINESS WITHOUT WEBSITE")
                    businessName = business.text.splitlines()[0]
                    addrphone = business.text.splitlines()[3].split(" · ")
                    if len(addrphone) == 1:
                        address = addrphone[0]
                        businessPhone = "No Phone"
                    elif len(addrphone) == 3:
                        businessPhone = addrphone[2].replace("-", "")
                        address = addrphone[1]
                    else:
                        businessPhone = addrphone[1].replace("-", "")
                        address = addrphone[0]
                    businessData.append([])
                    businessData[x].append(businessName)
                    businessData[x].append(address)
                    businessData[x].append(businessPhone)
                    x = x + 1
        except NoSuchElementException:
            print("ERROR?")
            stop = 1
        try:
            if browser.find_element(By.ID, 'pnnext'):
                browser.get(browser.find_element(By.ID, 'pnnext').get_attribute('href'))
                print("next page")
        except NoSuchElementException:
            print("Page Ended")
            stop = 1
    
    with open(str(ts)+'.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        # write the header
        writer.writerow(header)
        # write the data
        for data in businessData:
            writer.writerow(data)
        browser.quit()
except TimeoutException:
    print("YAS")