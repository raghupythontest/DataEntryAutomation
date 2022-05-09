import time

from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import lxml

USER_AGENT="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36"
ACCEPT_LANGUAGE="en-US,en;q=0.9"
headers = { 'Accept-Language':USER_AGENT,
            'User-Agent':ACCEPT_LANGUAGE
          }
chrome_driver_path = "C:/Development/chromedriver"
url="https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-122.79725111914063%2C%22east%22%3A-122.06940688085938%2C%22south%22%3A37.6295134195541%2C%22north%22%3A37.92078260682894%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D"

response=requests.get(url=url,headers=headers)
zilloweb=response.text

soup=BeautifulSoup(zilloweb,"lxml")
#print(soup.prettify())
print(soup.title)

list_cards=soup.find_all(name="div",class_="list-card-info")

data=[]
for list_card in list_cards:
    try:
        price=list_card.find(class_="list-card-price").text
        address=list_card.select_one("a address").text
        property_link=list_card.select_one("a").get("href")
        data_dict={
            "price":price,
            "address":address,
            "property_link":property_link
        }
        data.append(data_dict)
    except:
        print("No data")
print(data)
# selenium google form fill
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

time.sleep(2)
driver = webdriver.Chrome(chrome_options=options,executable_path=chrome_driver_path)
driver.get("https://forms.gle/fi8sb7gZqxcTuZ1M6")
for data_dict in data:
    time.sleep(2)
    p_address = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    p_price = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    p_link = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit_button = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    p_address.send_keys(data_dict["address"])
    p_price.send_keys(data_dict["price"])
    p_link.send_keys(data_dict["property_link"])
    submit_button.click()
    time.sleep(1)
    another_response_link=driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[1]/div/div[4]/a")
    another_response_link.click()
driver.quit()


