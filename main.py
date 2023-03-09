from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

CHROME_DRIVER_PATH = 'c:/WebDrivers/chromedriver.exe'

def get_data():
    # Set up the webdriver
    options = Options()
    driver = webdriver.Chrome(options=options, executable_path=CHROME_DRIVER_PATH)

    # Fetch Indeed
    driver.get("https://uk.indeed.com")

    # Fetch 'Developer' listings in the UK
    whatInput = driver.find_element(By.ID, "text-input-what")
    whatInput.send_keys("Developer")
    whereInput = driver.find_element(By.ID, "text-input-where")
    whereInput.send_keys("United Kingdom")
    findJobsButton = driver.find_element(By.CLASS_NAME, "yosegi-InlineWhatWhere-primaryButton")
    findJobsButton.click()

    # Parse and print the results
    soup = BeautifulSoup(driver.page_source, "html.parser")
    listings = soup.find_all("table", {"class": "jobCard_mainContent"})
    parse_data(listings)

    driver.quit()


def parse_data(listings):
    for listing in listings:
        title = listing.find("a", {"role": "button"})
        title_text = title.text

        salary = listing.find("div", {"class": "salary-snippet-container"})
        salary_text = "Not Stated"

        if salary:
            salary_text = salary.text

        f = open("salaryinfo.txt", "a+")
        f.write("\n" + title_text + ": " + salary_text)
        f.close()


if __name__ == '__main__':
    get_data()
