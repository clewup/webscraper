from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

CHROME_DRIVER_PATH = 'c:/WebDrivers/chromedriver.exe'

def get_data(url):
    browser_options = Options()

    driver = webdriver.Chrome(options=browser_options, executable_path=CHROME_DRIVER_PATH)
    driver.get(url)

    whatInput = driver.find_element(By.ID, "text-input-what")
    whatInput.send_keys("Developer")

    whereInput = driver.find_element(By.ID, "text-input-where")
    whereInput.send_keys("Leeds")

    findJobsButton = driver.find_element(By.CLASS_NAME, "yosegi-InlineWhatWhere-primaryButton")
    findJobsButton.click()

    soup = BeautifulSoup(driver.page_source, "html.parser")

    jobList = soup.find("ul", {"class": "jobsearch-ResultsList"})
    jobListings = jobList.find_all('li')

    driver.quit()

if __name__ == '__main__':
    get_data("https://uk.indeed.com")
