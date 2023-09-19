import json
import re
import threading
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


service = Service()
options = webdriver.ChromeOptions()
#options.add_argument("--proxy=http://rxagjoeb:ce9jutub96sj@185.199.229.156:7492/")
options.add_extension("proxy_auth_plugin.zip")
options.add_argument("--no-sandbox")
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
user_agent = ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 '
              'Safari/537.36')
options.add_argument(f'user-agent={user_agent}')
options.add_argument('--window-size=1920,1080')
myntra_driver = webdriver.Chrome(service=service, options=options)

myntra_driver.get("https://www.myntra.com/")
print(myntra_driver.page_source)
myntra_driver.quit()