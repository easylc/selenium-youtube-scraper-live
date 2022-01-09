from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import urllib.parse
import re
import pandas as pd

PROPERTY_TRENDING_URL = 'https://property.hk/property_search.php?bldg='+urllib.parse.quote("永利中心", safe='')+'&prop=P&pt=A&loc=&dt=&saleType=1&greenform=&fh=&parking='

PROPERTY_TXN_TRENDING_URL = 'https://property.hk/tran.php?dt=&bldg='+urllib.parse.quote("永利中心", safe='')+'&year&prop=P&saleType=3&loc='

sales_data_list = []
trxns_data_list = []

def  get_driver():
  chrome_options = Options()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')
  chrome_options.add_argument('--headless')
  driver = webdriver.Chrome(options=chrome_options)
  return driver

def  get_mb_driver():
  chrome_options = Options()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')
  chrome_options.add_argument('--headless')
  chrome_options.add_argument('--user-agent="Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"')
  driver = webdriver.Chrome(options=chrome_options)
  return driver

if __name__ == "__main__":
  print('Fetching the page - Property')
  driver = get_driver()
  driver.get(PROPERTY_TRENDING_URL)
  stypeElement = driver.find_element(By.ID,"stypetab3")
  stypeElement.click()

  searchDiv = driver.find_element(By.CLASS_NAME,"searchqueryitem")
  resultDiv = driver.find_element(By.CLASS_NAME,"searchresult")
  result_all = driver.find_element(By.NAME,"printForm")
  results = result_all.find_elements(By.XPATH, "//span[@class='saleprice']") 
  links = result_all.find_elements(By.XPATH, "//*[text()='樓盤詳情']")
  
  driver1 = get_driver()

  print ("== Part(1)  Print Sales ==")
  
  i = 1
  for each_link in links:
    link = each_link.get_attribute('href')
    driver1.get(link)
    
    propDiv = driver1.find_element(By.ID,"property-info")
    postdateTxt = propDiv.find_element(By.XPATH, "//*[text()='更新日期']")
    postdate = postdateTxt.find_element(By.XPATH, "..").find_element(By.CLASS_NAME,"val").get_attribute('innerHTML')
    print(i,".更新日期:",postdate) 

    upddateTxt = propDiv.find_element(By.XPATH, "//*[text()='刊登日期']")
    upddate = upddateTxt.find_element(By.XPATH, "..").find_element(By.CLASS_NAME,"val").get_attribute('innerHTML')
    print(i,".刊登日期:",upddate) 

    try:
      floorTxt = propDiv.find_element(By.XPATH, "//*[text()='層數及單位']")
      floor = floorTxt.find_element(By.XPATH, "..").find_element(By.CLASS_NAME,"val").get_attribute('innerHTML')
      print(i,".層數及單位:",floor)
    except NoSuchElementException:
      floor = 'NA'
      print(i,".層數及單位:Not Found")

    priceTxt = propDiv.find_element(By.XPATH, "//*[text()='售價 ']")
    price = priceTxt.find_element(By.XPATH, "..").find_element(By.CLASS_NAME,"val").get_attribute('innerHTML')
    price = re.split('<span', price,1) 
    price = price[0][1:]
    price = int(price)*10000
    price = "${:,.2f}".format(price)
    print(i,".售價(萬):",price)
    
    sales_data_list.append(['永利中心','P',link,postdate,upddate,floor,price])
    i=i+1


print ("== Part(2)  Print Transaction History(20) ==")
j=1
driver2 = get_driver()
driver2.get(PROPERTY_TXN_TRENDING_URL)
propTxnDiv = driver2.find_element(By.ID,"proplist")

TxnLinks = propTxnDiv.find_elements(By.XPATH, "//*[text()='詳情']")

driver3 = get_driver()

for each_txn_link in TxnLinks:
  txn_link = each_txn_link.get_attribute('href')
  
  driver3.get(txn_link)
  propTxnDetailDiv = driver3.find_element(By.CLASS_NAME,"col-xs-12")
  postdateTxt = propTxnDetailDiv.find_element(By.XPATH, "//*[text()='登記日期']")
  postdate = postdateTxt.find_element(By.XPATH, "..").find_element(By.CLASS_NAME,"col-xs-9").get_attribute('innerHTML')
  print(j,".登記日期:",postdate) 

  refNumTxt = propTxnDetailDiv.find_element(By.XPATH, "//*[text()='登記編號']")
  refNum = refNumTxt.find_element(By.XPATH, "..").find_element(By.CLASS_NAME,"col-xs-9").get_attribute('innerHTML')
  print(j,".登記編號:",refNum) 

  docdateTxt = propTxnDetailDiv.find_element(By.XPATH, "//*[text()='文件日期']")
  docdate = docdateTxt.find_element(By.XPATH, "..").find_element(By.CLASS_NAME,"col-xs-9").get_attribute('innerHTML')
  print(j,".文件日期:",docdate) 

  addrTxt = propTxnDetailDiv.find_element(By.XPATH, "//*[text()='地址']")
  addr = addrTxt.find_element(By.XPATH, "..").find_element(By.CLASS_NAME,"col-xs-9").get_attribute('innerHTML')
  print(j,".地址:",addr)

  priceTxt = propTxnDetailDiv.find_element(By.XPATH, "//*[text()='售價']")
  price = priceTxt.find_element(By.XPATH, "..").find_element(By.CLASS_NAME,"col-xs-9").get_attribute('innerHTML')
  price = re.split('<a', price,1)
  price = re.split(' ', price[0],1)
  price = float(price[0])*1000000
  price = "${:,.2f}".format(price)
  print(j,".售價（萬）:",price)
  
  trxns_data_list.append(['永利中心','P',link,postdate,refNum,docdate,addr,price])
  j=j+1

print ("== Part(3)  Export CSV ==")
sales_df = pd.DataFrame(sales_data_list,columns=['keyword','type','url','postdate','upddate','floor','price'],index=None)
print(sales_df)
sales_df.to_csv('sales_trending.csv')

trxns_df = pd.DataFrame(trxns_data_list,columns=['keyword','type','url','postdate','refNum','docdate','address','price'],index=None)
print(trxns_df)
trxns_df.to_csv('trxns_trending.csv')

print ("== End ==")

driver.close()
driver.quit()

driver1.close()
driver1.quit()

driver2.close()
driver2.quit()

driver3.close()
driver3.quit()