import time
from requests import options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd
from fastapi import FastAPI

app = FastAPI()

@app.get('/get-data')
def get_image_link(searchTitle : str =None):
    option=webdriver.ChromeOptions()
    option.add_experimental_option("excludeSwitches",["enable-logging"])
    service = Service("C:\Program Files (x86)\chromedriver.exe")
    driver=webdriver.Chrome(service=service,options=option)
    products=[] #List to store name of the product
    prices=[] #List to store price of the product
    # ratings=[] #List to store rating of the product
    image=[]
    driver.get(f"https://www.flipkart.com/search?q={searchTitle}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off")
    # driver.get(f"https://www.flipkart.com/search?q=laptops&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off")
    # time.sleep(10) 
    content = driver.page_source
    soup = BeautifulSoup(content,"html.parser")
    if searchTitle != '' and searchTitle !=None:
        for a in soup.findAll('div', attrs={'class':['_2kHMtA','_1xHGtK _373qXS']}):
            if len(image) <= 15:
                split=a.find('img').get('src')
                img = split.split('?')[0]
                name=a.find('div', attrs={'class':['_4rR01T','_2WkVRV']})
                price=a.find('div', attrs={'class':['_30jeq3 _1_WHN1','_30jeq3']})
            # rating=a.find('div', attrs={'class':'_3LWZlK'})
            
                image.append(img)
                products.append(name.text)
                prices.append(price.text)
            else:
                break
            # ratings.append(rating.text)

        df = pd.DataFrame({'Image link':[image],'Product Name':[products],'Price':[prices]})
        driver.close()
        return df
    else:
      driver.close()
      return {"Data":"Not Found"}
