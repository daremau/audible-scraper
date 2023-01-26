from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

options = Options()
options.headless = True
options.add_argument('window-size=1920x1080')

website = "https://www.audible.com/search"
path = "./chromedrive.exe"

driver = webdriver.Chrome(path, options=options)
driver.get(website)
#driver.maximize_window()


#Pagination
pagination = driver.find_element(By.XPATH, '//ul[contains(@class, "pagingElements ")]')
pages = pagination.find_elements(By.TAG_NAME, 'li')
last_page = int(pages[-2].text)

book_title = []
book_author = []
book_length = []

current_page = 1
while current_page <= last_page:
  
  
  #Grab container of audible books
  #time.sleep(2)
  container = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'adbl-impression-container ')))
  #container = driver.find_element(By.CLASS_NAME, 'adbl-impression-container ')
  products = container.find_elements(By.XPATH, './/li[contains(@class, "productListItem")]')

  #Getting title, author, runtime of books
  for product in products:
    title = product.find_element(By.XPATH, './/h3[contains(@class, "bc-heading")]').text
    book_title.append(title)
    
    author = product.find_element(By.XPATH, './/li[contains(@class, "authorLabel")]').text
    book_author.append(author)
    
    length = product.find_element(By.XPATH, './/li[contains(@class, "runtimeLabel")]').text
    book_length.append(length)
    
    print(title, author, length)
  
  current_page += 1

  try:
    next_page = driver.find_element(By.XPATH, '//span[contains(@class, "nextButton ")]')
    next_page.click()
  except:
    pass

driver.quit()

df = pd.DataFrame({'title': book_title, 'author': book_author, 'runtime': book_length})
df.to_csv('books.csv', index=False)
