from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import urllib.parse
import re

PROPERTY_TRENDING_URL = 'https://property.hk/property_search.php?bldg='+urllib.parse.quote("永利中心", safe='')+'&prop=P&pt=A&loc=&dt=&saleType=1&greenform=&fh=&parking='

PROPERTY_TXN_TRENDING_URL = 'https://property.hk/tran.php?dt=&bldg='+urllib.parse.quote("永利中心", safe='')+'&year&prop=P&saleType=3&loc='

def  get_driver():
  chrome_options = Options()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')
  chrome_options.add_argument('--headless')
  driver = webdriver.Chrome(options=chrome_options)
  return driver

class propSalesClass:
  def __init__(self, url, postdate, upddate, floor, price):
    self.url = url
    self.postdate = postdate
    self.upddate = upddate
    self.floor = floor
    self.price = price


class propTxnClass:
  def __init__(self, url, postdate, ref_num, docdate, addr, price):
    self.url = url
    self.postdate = postdate
    self.ref_num = ref_num
    self.docdate = docdate
    self.addr = addr
    self.price = price


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

  print ("For Sales")
  
  for each_link in links:
    link = each_link.get_attribute('href')
    driver1.get(link)
    print("link:",link) 
    propDiv = driver1.find_element(By.ID,"property-info")
    postdateTxt = propDiv.find_element(By.XPATH, "//*[text()='更新日期']")
    postdate = postdateTxt.find_element(By.XPATH, "..").find_element(By.CLASS_NAME,"val").get_attribute('innerHTML')
    print("更新日期:",postdate) 

    upddateTxt = propDiv.find_element(By.XPATH, "//*[text()='刊登日期']")
    upddate = upddateTxt.find_element(By.XPATH, "..").find_element(By.CLASS_NAME,"val").get_attribute('innerHTML')
    print("刊登日期:",upddate) 

    try:
      floorTxt = propDiv.find_element(By.XPATH, "//*[text()='層數及單位']")
      floor = floorTxt.find_element(By.XPATH, "..").find_element(By.CLASS_NAME,"val").get_attribute('innerHTML')
      print("層數及單位:",floor)
    except NoSuchElementException:
      print("層數及單位:Not Found")

    priceTxt = propDiv.find_element(By.XPATH, "//*[text()='售價 ']")
    price = priceTxt.find_element(By.XPATH, "..").find_element(By.CLASS_NAME,"val").get_attribute('innerHTML')
    price = re.split('<span', price,1)
    print("售價(萬):",price[0]) 
    
print ("Transaction History")
driver2 = get_driver()
driver2.get(PROPERTY_TXN_TRENDING_URL)
propTxnDiv = driver2.find_element(By.ID,"proplist")

TxnLinks = propTxnDiv.find_elements(By.XPATH, "//*[text()='詳情']")

driver3 = get_driver()

for each_txn_link in TxnLinks:
  txn_link = each_txn_link.get_attribute('href')
  #print("Txn Link:",txn_link) 

  driver3.get(txn_link)
  propTxnDetailDiv = driver3.find_element(By.CLASS_NAME,"col-xs-12")
  postdateTxt = propTxnDetailDiv.find_element(By.XPATH, "//*[text()='登記日期']")
  postdate = postdateTxt.find_element(By.XPATH, "..").find_element(By.CLASS_NAME,"col-xs-9").get_attribute('innerHTML')
  print("登記日期:",postdate) 

  refNumTxt = propTxnDetailDiv.find_element(By.XPATH, "//*[text()='登記編號']")
  refNum = refNumTxt.find_element(By.XPATH, "..").find_element(By.CLASS_NAME,"col-xs-9").get_attribute('innerHTML')
  print("登記編號:",refNum) 

  docdateTxt = propTxnDetailDiv.find_element(By.XPATH, "//*[text()='文件日期']")
  docdate = docdateTxt.find_element(By.XPATH, "..").find_element(By.CLASS_NAME,"col-xs-9").get_attribute('innerHTML')
  print("文件日期:",docdate) 

  addrTxt = propTxnDetailDiv.find_element(By.XPATH, "//*[text()='地址']")
  addr = docdateTxt.find_element(By.XPATH, "..").find_element(By.CLASS_NAME,"col-xs-9").get_attribute('innerHTML')
  print("地址:",addr)

  priceTxt = propTxnDetailDiv.find_element(By.XPATH, "//*[text()='售價']")
  price = priceTxt.find_element(By.XPATH, "..").find_element(By.CLASS_NAME,"col-xs-9").get_attribute('innerHTML')
  price = re.split('<a', price,1)
  price = re.split(' ', price[0],1)
  print("售價（百萬）:",price[0])

  




