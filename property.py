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
  def __init__(self, url, postdate, upddate, usagetype, district, addreng, addrchi, bldeng, bldchi, price, remark, indate, landyr):
    self.url = url
    self.postdate = postdate
    self.upddate = upddate
    self.usagetype = usagetype
    self.district = district
    self.addreng = addreng
    self.addrchi = addrchi
    self.bldeng = bldeng
    self.bldchi = bldchi
    self.price = price
    self.remark = remark
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
  
  links = result_all.find_elements(By.XPATH, "//*[text()='樓盤詳情']")
  
  driver1 = get_driver()

  for each_link in links:
    link = each_link.get_attribute('href')
    driver1.get(link)
    print("link:",link) 
    propDiv = driver1.find_element(By.ID,"property-info")
    postdate = propDiv.find_element(By.XPATH, "//div[2]/table[1]/tbody[1]/tr[1]/td[@class='val']").get_attribute('innerHTML')
    print("postdate:",postdate) 

    upddate = propDiv.find_element(By.XPATH, "//div[2]/table[1]/tbody[1]/tr[2]/td[@class='val']").get_attribute('innerHTML')
    print("upddate:",upddate) 

    usagetype = propDiv.find_element(By.XPATH, "//div[2]/table[1]/tbody[1]/tr[3]/td[@class='val']").get_attribute('innerHTML')
    print("usagetype:",usagetype) 
    
    district = propDiv.find_element(By.XPATH, "//div[2]/table[1]/tbody[1]/tr[4]/td[@class='val']").get_attribute('innerHTML')
    print("district:",district) 

    addreng = propDiv.find_element(By.XPATH, "//div[2]/table[1]/tbody[1]/tr[5]/td[@class='val']").get_attribute('innerHTML')
    print("addreng:",addreng) 

    addrchi = propDiv.find_element(By.XPATH, "//div[2]/table[1]/tbody[1]/tr[6]/td[@class='val']").get_attribute('innerHTML')
    print("addrchi:",addrchi) 
    
    bldeng = propDiv.find_element(By.XPATH, "//div[2]/table[1]/tbody[1]/tr[7]/td[@class='val']").get_attribute('innerHTML')
    print("bldeng:",bldeng) 

    bldchi = propDiv.find_element(By.XPATH, "//div[2]/table[1]/tbody[1]/tr[8]/td[@class='val']").get_attribute('innerHTML')
    print("bldchi:",bldchi) 

    price = propDiv.find_element(By.XPATH, "//div[2]/table[1]/tbody[1]/tr[9]/td[@class='val']").get_attribute('innerHTML')
    print("price:",price) 
    
    remark = propDiv.find_element(By.XPATH, "//div[2]/table[1]/tbody[1]/tr[10]/td[@class='val']").get_attribute('innerHTML')
    print("remark:",remark) 

    indate = propDiv.find_element(By.XPATH, "//div[2]/table[1]/tbody[1]/tr[11]/td[@class='val']").get_attribute('innerHTML')
    print("indate:",indate) 

    landyr = propDiv.find_element(By.XPATH, "//div[2]/table[1]/tbody[1]/tr[12]/td[@class='val']").get_attribute('innerHTML')
    print("landyr:",landyr) 