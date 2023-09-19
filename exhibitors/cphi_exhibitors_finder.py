
import requests

import pandas
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup

URL = "https://exhibitors.cphi.com/cpww23/"
# URL = "https://exhibitors.cphi.com/live/cphi/event46v2.jsp?site=46&type=company&eventid=446&map=false"

# Set up Selenium WebDriver
driver = webdriver.Chrome()
driver.get(URL)

# Wait for the results to load
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.CLASS_NAME, "cookieButton")))

driver.find_element(By.CLASS_NAME, "cookieButton").click()

wait.until(EC.presence_of_element_located((By.CLASS_NAME, "results")))


# Keep clicking 'Show more' as long as the button is there
while True: 
  try:
    # btn = wait.until(EC.presence_of_element_located((By.XPATH, '//a[text()="Show more results"]')))
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[text()="Show more results"]')))
    btn.click()
  except NoSuchElementException:
      break
  except TimeoutException:
      break
  

# Get the page source after the results are loaded
page_source = driver.page_source

# Quit the WebDriver to free up resources
driver.quit()


soup = BeautifulSoup(page_source, "html.parser")

results = soup.find(class_="exhibitors-list")

exhibitor_elements = soup.find_all("div", class_="results")

name_col = []
location_col = []
country_col = []
category_col = []

for i in exhibitor_elements: 
  title = i.find("div", class_="exhibitor__title")
  # description = i.find("div", class_="exhibitor__description")
  # company_type = i.find("div", class_="entity__spec")
  location = i.find("div", class_="exhibitor__h-place")
  country = i.find("div", class_="exhibitor__country")
  category = i.find("div", class_="entity__tags")
  # category_tags = i.find("div", class_="entity__tags").find_all("div", class_="m-tag")
  # category = ';'.join([tag.text.strip() for tag in category_tags])

  if hasattr(title, "text"):
    name_col.append(title.text.strip())
  # if hasattr(description, "text"):
  #   print(description.text.strip())
  if hasattr(location, "text"):
    location_col.append(location.text.strip())
  if hasattr(country, "text"):
    country_col.append(country.text.strip())
  if hasattr(category, "text"): 
    category_col.append(category.text.strip())

data = list(zip(name_col, location_col, country_col, category_col))

df = pandas.DataFrame(data, columns= ["Company name", "Location", "Country", "Category"])

try: 
    df.to_excel("ExhibitionData.xlsx")
except:
    print("\nSomething went wrong ! Please check code / Internet Connection")
else:
    print("\nExhibition data successfully written to Excel.")
finally:
    print("\nQuitting the program. Bye !")
