
import requests

import pandas
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup

URL = "https://exhibitors.figlobal.com/hifi23/"
# URL = "https://exhibitors.figlobal.com/live/figlobal/event46.jsp?site=47&type=company&eventid=463&map=false&name=&SugType_val=&RecordId_val="


# Set up Selenium WebDriver
driver = webdriver.Chrome()
driver.get(URL)
action = ActionChains(driver)

driver.maximize_window()

# Wait for the results to load
wait = WebDriverWait(driver, 8)

wait.until(EC.presence_of_element_located((By.CLASS_NAME, "exhibitor")))

cookie_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "cookieButton")))

cookie_button.click()

# chat_minimize = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.purechat-super-minimize-link-button")))
chat_open = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.purechat-start-chat")))

time.sleep(1)
chat_open.click()

# driver._switch_to.default_content
driver.switch_to.window(driver.window_handles[0])



# chat_span = driver.find_element((By.CSS_SELECTOR, "span.purechat-widget-title-link"))
# driver.execute_script("arguments[0].style.visibility='hidden', chat_span")


# Keep clicking 'Show more' as long as the button is there
while True: 
  try:
    # show_more_btn = wait.until(EC.presence_of_element_located((By.XPATH, '//a[text()="Show more results"]')))
    # show_more_btn = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.paging a.button.button-secondary')))
    show_more_btn = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div.main > div.wrapper-centered > div > div.span8.results > div.paging > a')))
    # driver.execute_script("arguments[0].style.display = 'block';", show_more_btn)
    # driver.execute_script("arguments[0].style.opacity = '1';", show_more_btn)
    # driver.execute_script("arguments[0].style.pointerEvents = 'auto';", show_more_btn)
    # driver.execute_script("arguments[0].style.zIndex = 9999;", show_more_btn)

    # Switch to Iframe and close the chat box
    # wait.until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "button.purechat-super-minimize-link-button"))).click()
    # wait.until(EC.element_to_be_clickable((By.XPATH,"//button[@id='gorgias-chat-messenger-button']"))).click()

    # total_height = int(driver.execute_script("return document.body.scrollHeight"))
    # for i in range(1, total_height, 5):
    #   driver.execute_script("window.scrollTo(0, {});".format(i))

    driver.execute_script("arguments[0].scrollIntoView();", show_more_btn)
    # driver.execute_script("arguments[0].active = true;", show_more_btn)

    driver.refresh()
    button = driver.find_element(By.CSS_SELECTOR, 'body > div.main > div.wrapper-centered > div > div.span8.results > div.paging > a')
    button.click()

    time.sleep(1)

    show_more_btn.click()
    # show_more_btn.send_keys(Keys.ENTER)
    # driver.execute_script("arguments[0].click();", show_more_btn)
    action.move_to_element(show_more_btn).pause(1).click(show_more_btn).perform()

    # action.move_to_element(show_more_btn).context_click().move_by_offset(-3, 0).click().perform()


    # button_location = show_more_btn.location
    # button_size = show_more_btn.size
    # x_coord = button_location['x'] + button_size['width'] / 2
    # y_coord = button_location['y'] + button_size['height'] / 2

    # driver.execute_script(f"window.scrollTo({x_coord}, {y_coord});")
    # driver.execute_script("document.elementFromPoint(arguments[0], arguments[1]).click();", x_coord, y_coord)


    # show_more_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[text()="Show more results"]')))
    # show_more_btn.click()
  except NoSuchElementException:
      break
  except TimeoutException:
      break


# Get the page source after the results are loaded
page_source = driver.page_source

# Quit the WebDriver to free up resources
driver.quit()


soup = BeautifulSoup(page_source, "html.parser")

results = soup.find(class_="results-wrapper")

exhibitor_elements = soup.find_all("div", class_="exhibitor")

name_col = []
location_col = []
country_col = []

for i in exhibitor_elements: 
  h4_element = i.find("h4")
  title = h4_element.contents[-1]
  # description = i.find("div", class_="exhibitor__description")
  # company_type = i.find("div", class_="entity__spec")
  location = i.find("span", class_="stand")
  country = i.find("span", class_="country")

  if hasattr(title, "text"):
    name_col.append(title.text.strip())
    # print(title.text.strip())
  # if hasattr(description, "text"):
  #   print(description.text.strip())
  if hasattr(location, "text"):
    location_col.append(location.text.strip())
    # print(location.text.strip())
  if hasattr(country, "text"):
    country_col.append(country.text.strip())
    # print(country.text.strip())

  print()

data = list(zip(name_col, location_col, country_col))

df = pandas.DataFrame(data, columns= ["Company name", "Location", "Country"])

try: 
    df.to_excel("fi_exhibitors_data.xlsx")
except:
    print("\nSomething went wrong ! Please check code / Internet Connection")
else:
    print("\nExhibition data successfully written to Excel.")
finally:
    print("\nQuitting the program. Bye !")
