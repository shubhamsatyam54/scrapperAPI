import json
import re
import threading
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def myntra_single_product_scrapper(url):
    service = Service()
    options = webdriver.ChromeOptions()
    options.add_argument("--proxy=http://95ce3caaf58d4e58a29dec8d5763d2fa:@proxy.crawlera.com:8011/")
    certificate_path = "zyte-proxy-ca.crt"
    options.add_argument(f'--cert-path={certificate_path}')
    options.add_argument('--ignore-certificate-errors')
    # options.add_extension("proxy_auth_plugin.zip")
    options.add_argument("--no-sandbox")
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    user_agent = ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 '
                  'Safari/537.36')
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument('--window-size=1920,1080')
    myntra_driver = webdriver.Chrome(service=service, options=options)
    myntra_driver.get(url)
    print(myntra_driver.page_source)
    try:
        product_data = {"product_URL": url}
        #html = myntra_driver.find_element(By.TAG_NAME, 'html')
        #html.send_keys(Keys.END)
        product_title_element = myntra_driver.find_elements(By.CLASS_NAME, "pdp-name")
        if len(product_title_element) > 0:
            product_title = product_title_element[0]
            product_data["title"] = product_title.text.lower().lower()
        else:
            product_data["title"] = None

        product_brand_element = myntra_driver.find_elements(By.CLASS_NAME, "pdp-title")
        if len(product_brand_element) > 0:
            product_brand = product_brand_element[0]
            product_data["brand"] = product_brand.text.lower()
        else:
            product_data["brand"] = None


        product_review_count_element = myntra_driver.find_elements(By.CLASS_NAME, "detailed-reviews-allReviews")
        if len(product_review_count_element) > 0:
            product_review_url = product_review_count_element[0].get_property("href")
            product_review_count = re.search(r"\d+", product_review_count_element[0].text.lower())
            product_data["review_Page_URL"] = product_review_url
            product_data["number_of_Reviews"] = product_review_count[0]
        else:
            product_data["review_Page_URL"] = None
            product_data["number_of_Reviews"] = None

        product_price_element = myntra_driver.find_elements(By.CLASS_NAME, "pdp-price")
        if len(product_price_element) > 0:
            product_price = product_price_element[0]
            product_data["price"] = product_price.text.lower()
        else:
            product_data["price"] = None

        product_mrp_selector = ("#mountRoot > div > div:nth-child(1) > main > div.pdp-details.common-clearfix > "
                                "div.pdp-description-container > div.pdp-price-info > div > p.pdp-discount-container "
                                "> span.pdp-mrp > s")
        product_mrp_element = myntra_driver.find_elements(By.CSS_SELECTOR, product_mrp_selector)
        if len(product_mrp_element) > 0:
            product_mrp = product_mrp_element[0]
            product_data["mrp"] = product_mrp.text.lower()
        else:
            product_data["mrp"] = None

        other_colors_full_data = []
        other_colors_container = myntra_driver.find_elements(By.CLASS_NAME, "colors-container")
        if len(other_colors_container) > 0:
            other_colors = other_colors_container[0].find_elements(By.TAG_NAME, "a")
            for color in other_colors:
                color_data = {}
                color_name = color.get_attribute("title")
                color_data["color"] = color_name.lower()
                color_link = color.get_attribute("href")
                color_data["web_Page_URL"] = color_link.lower()
                color_image_url_element = color.find_elements(By.TAG_NAME, "img")[0]
                color_image_url = color_image_url_element.get_attribute("src")
                color_data["image_url"] = color_image_url.lower()
                other_colors_full_data.append(color_data)

            product_data["other_available_colors"] = other_colors_full_data
        else:
            product_data["other_available_colors"] = None



        size_button_container = myntra_driver.find_elements(By.CLASS_NAME, "size-buttons-size-container")
        if len(size_button_container) > 0:
            size_button_sub_container = \
                size_button_container[0].find_elements(By.CLASS_NAME, "size-buttons-size-buttons")[0]

            sizes = [container.find_element(By.TAG_NAME, "p").text.lower() for container in
                     size_button_sub_container.find_elements(By.CLASS_NAME, "size-buttons-tipAndBtnContainer")]

            parsed_sizes = [{"size": size_price.split('\n')[0],
                             "price": size_price.split('\n')[1]} if '\n' in size_price else size_price for size_price in
                sizes]
            product_data["sizes"] = parsed_sizes

        else:
            product_data["sizes"] = None


    except:
        myntra_driver.quit()
        return None

    myntra_driver.quit()
    return product_data
