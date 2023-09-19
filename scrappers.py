import json
import re
import threading
from time import sleep

import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from single import *

file = open('offline_data.json', 'r')
scrapper_data = json.load(file)
threads = {}

#
# def myntra_single_product_scrapper(url):
#     service = Service()
#     options = webdriver.ChromeOptions()
#     options.add_argument("--no-sandbox")
#     options.add_argument("--headless")
#     options.add_argument("--disable-gpu")
#     user_agent = ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 '
#                   'Safari/537.36')
#     options.add_argument(f'user-agent={user_agent}')
#     options.add_argument('--window-size=1920,1080')
#     driver = webdriver.Chrome(service=service, options=options)
#     driver.get(url)
#     try:
#         product_data = {"product_URL": url}
#         html = driver.find_element(By.TAG_NAME, 'html')
#         html.send_keys(Keys.END)
#         product_title_element = driver.find_elements(By.CLASS_NAME, "pdp-name")
#         if len(product_title_element) > 0:
#             product_title = product_title_element[0]
#             product_data["title"] = product_title.text.lower().lower()
#         else:
#             product_data["title"] = None
#
#         product_brand_element = driver.find_elements(By.CLASS_NAME, "pdp-title")
#         if len(product_brand_element) > 0:
#             product_brand = product_brand_element[0]
#             product_data["brand"] = product_brand.text.lower()
#         else:
#             product_data["brand"] = None
#
#         product_rating_selector = ("#mountRoot > div > div:nth-child(1) > main > div.pdp-details.common-clearfix > "
#                                    "div.pdp-description-container > div.pdp-price-info > div > div > div > "
#                                    "div:nth-child("
#                                    "1)")
#         product_rating_element = driver.find_elements(By.CSS_SELECTOR, product_rating_selector)
#         if len(product_rating_element) > 0:
#             product_rating = product_rating_element[0]
#             product_data["star_Rating"] = product_rating.text.lower()
#         else:
#             product_data["star_Rating"] = None
#
#         product_rating_count_selector = (
#             "#mountRoot > div > div:nth-child(1) > main > div.pdp-details.common-clearfix > "
#             "div.pdp-description-container > div.pdp-price-info > div > div > div > "
#             "div.index-ratingsCount")
#         product_rating_count_element = driver.find_elements(By.CSS_SELECTOR, product_rating_count_selector)
#         if len(product_rating_count_element) > 0:
#             product_rating_count = re.search(r"\d+", product_rating_count_element[0].text.lower())
#             product_data["number_of_Ratings"] = product_rating_count[0]
#         else:
#             product_data["number_of_Ratings"] = None
#
#         product_review_count_element = driver.find_elements(By.CLASS_NAME, "detailed-reviews-allReviews")
#         if len(product_review_count_element) > 0:
#             product_review_url = product_review_count_element[0].get_property("href")
#             product_review_count = re.search(r"\d+", product_review_count_element[0].text.lower())
#             product_data["review_Page_URL"] = product_review_url
#             product_data["number_of_Reviews"] = product_review_count[0]
#         else:
#             product_data["review_Page_URL"] = None
#             product_data["number_of_Reviews"] = None
#
#         product_price_element = driver.find_elements(By.CLASS_NAME, "pdp-price")
#         if len(product_price_element) > 0:
#             product_price = product_price_element[0]
#             product_data["price"] = product_price.text.lower()
#         else:
#             product_data["price"] = None
#
#         product_mrp_selector = ("#mountRoot > div > div:nth-child(1) > main > div.pdp-details.common-clearfix > "
#                                 "div.pdp-description-container > div.pdp-price-info > div > p.pdp-discount-container "
#                                 "> span.pdp-mrp > s")
#         product_mrp_element = driver.find_elements(By.CSS_SELECTOR, product_mrp_selector)
#         if len(product_mrp_element) > 0:
#             product_mrp = product_mrp_element[0]
#             product_data["mrp"] = product_mrp.text.lower()
#         else:
#             product_data["mrp"] = None
#
#         other_colors_full_data = []
#         other_colors_container = driver.find_elements(By.CLASS_NAME, "colors-container")
#         if len(other_colors_container) > 0:
#             other_colors = other_colors_container[0].find_elements(By.TAG_NAME, "a")
#             for color in other_colors:
#                 color_data = {}
#                 color_name = color.get_attribute("title")
#                 color_data["color"] = color_name.lower()
#                 color_link = color.get_attribute("href")
#                 color_data["web_Page_URL"] = color_link.lower()
#                 color_image_url_element = color.find_elements(By.TAG_NAME, "img")[0]
#                 color_image_url = color_image_url_element.get_attribute("src")
#                 color_data["image_url"] = color_image_url.lower()
#                 other_colors_full_data.append(color_data)
#
#             product_data["other_available_colors"] = other_colors_full_data
#         else:
#             product_data["other_available_colors"] = None
#         product_description_data = {}
#
#         product_description_element = driver.find_elements(By.CLASS_NAME, "pdp-productDescriptorsContainer")
#         if len(product_description_element) > 0:
#             product_detail_element = product_description_element[0].find_elements(By.CLASS_NAME,
#                                                                                   "pdp-product-description-content")
#             if len(product_detail_element) > 0:
#                 product_description_data["description"] = product_detail_element[0].text.lower()
#             else:
#                 product_description_data["description"] = None
#
#             product_size_fits_element = product_description_element[0].find_elements(By.CLASS_NAME, "pdp-sizeFitDesc")
#             if len(product_size_fits_element) > 0:
#                 for product_size_fit in product_size_fits_element:
#                     key = product_size_fit.find_elements(By.CLASS_NAME, "pdp-sizeFitDescTitle")[0].text.lower()
#                     value = product_size_fit.find_elements(By.CLASS_NAME, "pdp-sizeFitDescContent")[0].text.lower()
#                     product_description_data[key] = value
#
#             specifications_data = {}
#             specifications = product_description_element[0].find_elements(By.CLASS_NAME, "index-tableContainer")[
#                 0].find_elements(By.CLASS_NAME, "index-row")
#             if len(specifications) > 0:
#                 for specification in specifications:
#                     key = specification.find_elements(By.CLASS_NAME, "index-rowKey")[0].text.lower()
#                     value = specification.find_elements(By.CLASS_NAME, "index-rowValue")[0].text.lower()
#                     specifications_data[key] = value
#
#                 product_description_data["specifications"] = specifications_data
#             else:
#                 product_description_data["specifications"] = None
#
#             product_data["description"] = product_description_data
#         else:
#             product_data["description"] = None
#
#         size_button_container = driver.find_elements(By.CLASS_NAME, "size-buttons-size-container")
#         if len(size_button_container) > 0:
#             size_button_sub_container = \
#                 size_button_container[0].find_elements(By.CLASS_NAME, "size-buttons-size-buttons")[0]
#
#             sizes = [container.find_element(By.TAG_NAME, "p").text.lower() for container in
#                      size_button_sub_container.find_elements(By.CLASS_NAME, "size-buttons-tipAndBtnContainer")]
#
#             parsed_sizes = [{"size": size_price.split('\n')[0],
#                              "price": size_price.split('\n')[1]} if '\n' in size_price else size_price for size_price in
#                 sizes]
#             product_data["sizes"] = parsed_sizes
#
#         else:
#             product_data["sizes"] = None
#
#         imageboxes = driver.find_elements(By.CLASS_NAME, "image-grid-image")
#         if len(imageboxes) > 0:
#             i = 1
#             for imagebox in imageboxes:
#                 image_url = imagebox.value_of_css_property("background-image").split('"')[1]
#                 product_data[f"image_URL_{i}"] = image_url
#                 i += 1
#     except:
#         return None
#     driver.quit()
#
#     return product_data


def myntra_image_scrapp(label=None, max_pages=15, request_id=None):
    print("started")
    service = Service()
    options = webdriver.ChromeOptions()
    #options.add_argument("--proxy=http://rxagjoeb:ce9jutub96sj@185.199.229.156:7492/")
    options.add_extension("proxy_auth_plugin.zip")
    options.add_argument("--no-sandbox")
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    options.add_argument(f'user-agent={user_agent}')
    # Run Chrome in headless mode
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://www.myntra.com/")
    search_bar = driver.find_element(By.CLASS_NAME, "desktop-searchBar")
    search_bar.send_keys(label)
    search_bar.send_keys(Keys.ENTER)
    max_no_of_pages = max_pages
    counter = 0
    for p in range(max_no_of_pages):
        scrapper_data[request_id]["scrapping_page"] = p + 1
        no_product_boxs = driver.find_elements(By.CLASS_NAME, "product-base")
        print(f"page : {p + 1} - products : {len(no_product_boxs)}")
        for i in range(1, len(no_product_boxs) + 1):
            counter+=1
            print(counter)
            product_data = {}
            selector = f"#desktopSearchResults > div.search-searchProductsContainer.row-base > section > ul > li:nth-child({i}) > a"
            product_url = driver.find_element(By.CSS_SELECTOR, selector).get_attribute("href")
            product_data["product_URL"] = product_url
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[1])
            driver.get(product_url)
            html = driver.find_element(By.TAG_NAME, 'html')
            html.send_keys(Keys.END)
            sleep(2)
            product_title_element = driver.find_elements(By.CLASS_NAME, "pdp-name")
            if len(product_title_element) > 0:
                product_title = product_title_element[0]
                product_data["title"] = product_title.text.lower().lower()
            else:
                product_data["title"] = None

            product_brand_element = driver.find_elements(By.CLASS_NAME, "pdp-title")
            if len(product_brand_element) > 0:
                product_brand = product_brand_element[0]
                product_data["brand"] = product_brand.text.lower()
            else:
                product_data["brand"] = None

            product_rating_selector = "#mountRoot > div > div:nth-child(1) > main > div.pdp-details.common-clearfix > div.pdp-description-container > div.pdp-price-info > div > div > div > div:nth-child(1)"
            product_rating_element = driver.find_elements(By.CSS_SELECTOR, product_rating_selector)
            if len(product_rating_element) > 0:
                product_rating = product_rating_element[0]
                product_data["star_Rating"] = product_rating.text.lower()
            else:
                product_data["star_Rating"] = None

            product_rating_count_selector = "#mountRoot > div > div:nth-child(1) > main > div.pdp-details.common-clearfix > div.pdp-description-container > div.pdp-price-info > div > div > div > div.index-ratingsCount"
            product_rating_count_element = driver.find_elements(By.CSS_SELECTOR, product_rating_count_selector)
            if len(product_rating_count_element) > 0:
                product_rating_count = re.search(r"\d+", product_rating_count_element[0].text.lower())
                product_data["number_of_Ratings"] = product_rating_count[0]
            else:
                product_data["number_of_Ratings"] = None

            product_review_count_element = driver.find_elements(By.CLASS_NAME, "detailed-reviews-allReviews")
            if len(product_review_count_element) > 0:
                product_review_url = product_review_count_element[0].get_property("href")
                product_review_count = re.search(r"\d+", product_review_count_element[0].text.lower())
                product_data["review_Page_URL"] = product_review_url
                product_data["number_of_Reviews"] = product_review_count[0]
            else:
                product_data["review_Page_URL"] = None
                product_data["number_of_Reviews"] = None

            product_price_element = driver.find_elements(By.CLASS_NAME, "pdp-price")
            if len(product_price_element) > 0:
                product_price = product_price_element[0]
                product_data["price"] = product_price.text.lower()
            else:
                product_data["price"] = None

            product_mrp_selector = "#mountRoot > div > div:nth-child(1) > main > div.pdp-details.common-clearfix > div.pdp-description-container > div.pdp-price-info > div > p.pdp-discount-container > span.pdp-mrp > s"
            product_mrp_element = driver.find_elements(By.CSS_SELECTOR, product_mrp_selector)
            if len(product_mrp_element) > 0:
                product_mrp = product_mrp_element[0]
                product_data["mrp"] = product_mrp.text.lower()
            else:
                product_data["mrp"] = None

            other_colors_full_data = []
            other_colors_container = driver.find_elements(By.CLASS_NAME, "colors-container")
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
            product_description_data = {}

            product_description_element = driver.find_elements(By.CLASS_NAME, "pdp-productDescriptorsContainer")
            if len(product_description_element) > 0:
                product_detail_element = product_description_element[0].find_elements(By.CLASS_NAME,
                                                                                      "pdp-product-description-content")
                if len(product_detail_element) > 0:
                    product_description_data["description"] = product_detail_element[0].text.lower()
                else:
                    product_description_data["description"] = None

                product_size_fits_element = product_description_element[0].find_elements(By.CLASS_NAME,
                                                                                         "pdp-sizeFitDesc")
                if len(product_size_fits_element) > 0:
                    for product_size_fit in product_size_fits_element:
                        key = product_size_fit.find_elements(By.CLASS_NAME, "pdp-sizeFitDescTitle")[0].text.lower()
                        value = product_size_fit.find_elements(By.CLASS_NAME, "pdp-sizeFitDescContent")[0].text.lower()
                        product_description_data[key] = value

                specifications_data = {}
                specifications = product_description_element[0].find_elements(By.CLASS_NAME, "index-tableContainer")[
                    0].find_elements(By.CLASS_NAME, "index-row")
                if len(specifications) > 0:
                    for specification in specifications:
                        key = specification.find_elements(By.CLASS_NAME, "index-rowKey")[0].text.lower()
                        value = specification.find_elements(By.CLASS_NAME, "index-rowValue")[0].text.lower()
                        specifications_data[key] = value

                    product_description_data["specifications"] = specifications_data
                else:
                    product_description_data["specifications"] = None

                product_data["description"] = product_description_data
            else:
                product_data["description"] = None

            size_button_container = driver.find_elements(By.CLASS_NAME, "size-buttons-size-container")
            if len(size_button_container) > 0:
                size_button_sub_container = \
                    size_button_container[0].find_elements(By.CLASS_NAME, "size-buttons-size-buttons")[0]

                sizes = [container.find_element(By.TAG_NAME, "p").text.lower() for container in
                         size_button_sub_container.find_elements(By.CLASS_NAME, "size-buttons-tipAndBtnContainer")]

                parsed_sizes = [{"size": size_price.split('\n')[0],
                                 "price": size_price.split('\n')[1]} if '\n' in size_price else size_price for
                    size_price in sizes]
                product_data["sizes"] = parsed_sizes

            else:
                product_data["sizes"] = None

            imageboxes = driver.find_elements(By.CLASS_NAME, "image-grid-image")
            if len(imageboxes) > 0:
                i = 1
                for imagebox in imageboxes:
                    image_url = imagebox.value_of_css_property("background-image").split('"')[1]
                    product_data[f"image_URL_{i}"] = image_url
                    i += 1

            scrapper_data[request_id]["data"].append(product_data)

            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            if counter % 10 == 0:
                send_page = counter // 10
                url = f"http://localhost:8000/scrapper/{request_id}/senddata?page={send_page}"
                requests.get(url)
        scrapper_data[request_id]["scraped_pages"] = p + 1
        with open('offline_data.json', 'w') as file:
            json.dump(scrapper_data, file, indent=4)
        next_btn = driver.find_elements(By.CSS_SELECTOR,
                                        "#desktopSearchResults > div.search-searchProductsContainer.row-base > section > div.results-showMoreContainer > ul > li.pagination-next > a")

        if len(next_btn) == 0:
            break
        else:
            next_btn[0].send_keys(Keys.ENTER)
        sleep(5)

    if counter % 10 != 0:
        send_page = (counter // 10) + 1
        url = f"http://localhost:8000/scrapper/{request_id}/senddata?page={send_page}"
        requests.get(url)
    driver.quit()


def start_scrapp(label, max_pages, request_id, website):
    scrapper_data[request_id] = {'data': [], 'website': website, 'label': label, 'scraped_pages': 0,
        'scrapping_page': 0, 'max_pages': max_pages}

    if website.lower() == "myntra":
        task = threading.Thread(target=myntra_image_scrapp, args=(label, max_pages, request_id,))
        threads[request_id] = task
        task.start()

    return request_id


def start_single_page_scrapper(website, url):
    if website.lower() == "myntra":
        data = myntra_single_product_scrapper(url)
        return data
    return None
