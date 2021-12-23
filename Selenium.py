from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

YOUTUBE_TRENDING_URL = 'https://youtube.com/feed/trending'

def  get_driver():
  chrome_options = Options()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')
  chrome_options.add_argument('--headless')
  driver = webdriver.Chrome(options=chrome_options)
  return driver

if __name__ == "__main__":
  print('Fetching the page')
  driver = get_driver()
  driver.get(YOUTUBE_TRENDING_URL)

  print('Get Video DIV')

  TAG ='ytd-video-name-render' 
  video_divs = driver.find_elements(By.TAG_NAME, TAG)
  
  print(f'Found {len(video_divs)} videos')
  print('Page Title',driver.title)