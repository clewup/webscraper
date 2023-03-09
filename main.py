import pickle
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

CHROME_DRIVER_PATH = 'c:/WebDrivers/chromedriver.exe'

def get_data(query):
    # Set up the webdriver
    options = Options()
    driver = webdriver.Chrome(options=options, executable_path=CHROME_DRIVER_PATH)

    # Fetch Amazon
    driver.get("https://amazon.co.uk")

    # Search for the query
    search_input = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Search Amazon.co.uk"]')
    search_input.send_keys(query)
    search_button = driver.find_element(By.ID, "nav-search-submit-button")
    search_button.click()

    # Fetch the products list
    soup = BeautifulSoup(driver.page_source, "html.parser")
    products = soup.find_all("div", {"data-component-type": "s-search-result"})

    # Initialize an empty product data array
    product_data_array = []

    # Loop through and parse each listing
    for product in products:
        product_link = product.find("a", {"class": "a-link-normal"})
        driver.get("https://www.amazon.co.uk" + product_link.get("href"))

        soup = BeautifulSoup(driver.page_source, "html.parser")
        product_data = parse_data(soup)
        product_data_array.append(product_data)

    driver.quit()

    # Pickle the data
    save_data(query, product_data_array)


class Product(object):
    def __init__(self, name, image, price):
        self.name = name
        self.image = image
        self.price = price


def parse_data(soup: BeautifulSoup):
    # Parse key information
    product_name = soup.find("span", {"id": "productTitle"}).text
    product_image = soup.find("img", {"id": "landingImage"}).get("src")

    # Parse the price components and concatenate together
    product_price_symbol = soup.find("span", {"class": "a-price-symbol"}).text
    product_price_whole = soup.find("span", {"class": "a-price-whole"}).text
    product_price_fraction = soup.find("span", {"class": "a-price-fraction"}).text
    product_full_price = product_price_symbol + product_price_whole + product_price_fraction

    # Return the data as an object
    return Product(
        name=product_name.strip(),
        image=product_image,
        price=product_full_price)


def save_data(query, products: []):
    filename = query + "_" + datetime.now().strftime("%m%d%Y-%H:%M:%S") + ".pkl"
    f = open(filename, "wb")
    pickle.dump(products, f)

    f.close()


if __name__ == '__main__':
    get_data("Yubico")
