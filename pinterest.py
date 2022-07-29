from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import random
import concurrent.futures
from selenium.webdriver.chrome.service import Service
from fastapi import FastAPI
import pandas as pd

app = FastAPI()

def get_free_proxies():
    url = "https://free-proxy-list.net/"
    soup = BeautifulSoup(requests.get(url).content, 'html.parser')
    # to store proxies
    proxies = []
    for row in soup.find("table", attrs={"class": "table-striped"}).find_all("tr")[1:]:
        tds = row.find_all("td")
        try:
            ip = tds[0].text.strip()
            port = tds[1].text.strip()
            proxies.append(str(ip) + ":" + str(port))
        except IndexError:
            continue
    return proxies


checkurl ='http://httpbin.org/ip'
workingProxy = []
trimProxies = []
links = []


def extract(proxy):
        try:
            requests.get(checkurl,proxies={'http':proxy,'https':proxy},timeout=3)
            workingProxy.append(proxy)
        except:
            pass
        return proxy


@app.get('/get-image-link')
def get_image_link(searchTitle : str = None):
    proxies = get_free_proxies()
    # random.shuffle(proxies)

    for ip in range(0,20):
        trimProxies.append(proxies[ip])
    
    with concurrent.futures.ThreadPoolExecutor() as exector:
        exector.map(extract,trimProxies)
    counter = random.randrange(0,len(workingProxy))
    proxy = workingProxy[counter]
    print(proxy)

    webdriver.DesiredCapabilities.CHROME['proxy']={
        "httpProxy":proxy,
        "ftpProxy":proxy,
        "sslProxy":proxy,
    
        "proxyType":"MANUAL",   
    }
    webdriver.DesiredCapabilities.CHROME['acceptSslCerts']=True
    option=webdriver.ChromeOptions()
    option.add_experimental_option("excludeSwitches",["enable-logging"])
    service = Service("C:\Program Files (x86)\chromedriver.exe")
    driver=webdriver.Chrome(service=service,options=option)

    pinterestUrl = f'https://in.pinterest.com/search/pins/?q={searchTitle}'
    # pinterestUrl = f'https://in.pinterest.com/'
    # pinterestUrl = f'https://www.flipkart.com/search?q={searchTitle}'
    driver.get(pinterestUrl)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    for link in soup.findAll('img'):
        if link.get('src').endswith('.jpg'):
            links.append(link.get('src'))
    driver.quit() 
    df = pd.DataFrame({'imageUrl':links})
    if searchTitle != '' and searchTitle !=None:
        return df.to_json()
    return {'Data':'Not Found'}


