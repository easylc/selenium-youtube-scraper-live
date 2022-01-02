from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import urllib.parse

PROPERTY_TRENDING_URL = 'https://property.hk/property_search.php?bldg='+urllib.parse.quote("永利中心", safe='')+'&prop=P&pt=A&loc=&dt=&saleType=1&greenform=&fh=&parking='

def  get_driver():
  chrome_options = Options()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')
  chrome_options.add_argument('--headless')
  driver = webdriver.Chrome(options=chrome_options)
  return driver

class trxnClass:
  def __init__(self, url, postdate, upddate, usagetype, district, addreng, addrchi, bldeng, bldchi, unit, price, indate, landyr):
    self.url = url
    self.postdate = postdate
    self.upddate = upddate
    self.usagetype = usagetype
    self.district = district
    self.addreng = addreng
    self.addrchi = addrchi
    self.bldeng = bldeng
    self.bldchi = bldchi
    self.unit = unit
    self.price = price
    self.indate = indate
    self.landyr = landyr


if __name__ == "__main__":
  print('Fetching the page - Property')
  driver = get_driver()
  driver.get(PROPERTY_TRENDING_URL)
  stypeElement = driver.find_element(By.ID,"stypetab3")
  stypeElement.click()
  
  #typeElement = driver.find_element(By.ID,"tusageP")
  #typeElement.click()
  #print('Usage:',typeElement.get_attribute('innerHTML'))
  #inputElement = driver.find_element(By.ID,"b")
  #inputElement.submit()

  searchDiv = driver.find_element(By.CLASS_NAME,"searchqueryitem")
  #print('Search:',searchDiv.get_attribute('innerHTML'))
  resultDiv = driver.find_element(By.CLASS_NAME,"searchresult")
  #print('Result:',resultDiv.get_attribute('innerHTML'))

  result_all = driver.find_element(By.NAME,"printForm")
  #print('Result:',result_all.get_attribute('innerHTML'))
  results = result_all.find_elements(By.XPATH, "//span[@class='saleprice']")
  #print('Details:',len(results))
  
  links = result_all.find_elements(By.XPATH, "//*[text()='樓盤詳情']").get_attribute('href')
  
  for each_link in links:
    driver.get(each_link)
    propDiv = driver.find_element(By.ID,"property-info")
    val = propDiv.find_element(By.XPATH, "//div[2]/table[1]/tbody[1]/tr[1]/td[@class='val']")
    print("val",val) 
