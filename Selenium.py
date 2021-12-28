import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

YOUTUBE_TRENDING_URL = 'https://www.youtube.com/results?search_query=hong+kong+chill+club'

def  get_driver():
  chrome_options = Options()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')
  chrome_options.add_argument('--headless')
  driver = webdriver.Chrome(options=chrome_options)
  return driver

def get_videos(driver):
  VIDEO_DIV_TAG = 'ytd-video-renderer'
  driver.get(YOUTUBE_TRENDING_URL)
  driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
  videos = driver.find_elements(By.TAG_NAME, VIDEO_DIV_TAG)
  return videos


class Video_D:
  def __init__(self, title, url, thumbnail_url, channel):
    self.title = title
    self.url = url
    self.thumbnail_url = thumbnail_url
    self.channel = channel

def get_video_data(video):

  title_tag = video.find_element(By.ID, 'video-title')
  
  title = title_tag.text
  url = title_tag.get_attribute('href')
  thumbnail_tag = video.find_element(By.TAG_NAME, 'img')
  thumbnail_url = thumbnail_tag.get_attribute('src')

  #channel_div = video.find_element(By.TAG_NAME,  'ytd-video-meta-block').find_element(By.TAG_NAME, 'tp-yt-paper-tooltip').find_element(By.ID, 'tooltip')

  channel_div = video.find_element(By.ID, 'channel-info').find_element(By.XPATH, "//yt-formatted-string[1]/a")
  channel_name = channel_div.get_attribute('innerHTML')

  return Video_D(title,url,thumbnail_url,channel_name)


if __name__ == "__main__":
  print('Fetching the page')
  driver = get_driver()
  driver.get(YOUTUBE_TRENDING_URL)

  print('Get Video DIV')

  TAG ='ytd-video-name-render' 
  video_divs = driver.find_elements(By.TAG_NAME, TAG)
  
  videos = get_videos(driver)
  
  video_data_list = []
   
  for video_data_itm in videos:
    video_data = get_video_data(video_data_itm)
    print('Video Title:',video_data.title)
    print('Video URL:',video_data.url)
    print('Video Thumbnail URL:', video_data.thumbnail_url)
    print('Video Channel Name:', video_data.channel)
    video_data_list.append([video_data.title, video_data.url, video_data.thumbnail_url, video_data.channel])

print('Data List',video_data_list)

print('Save data to CSV')
video_df = pd.DataFrame(video_data_list,columns=['Title','URL','Thumbnail URL','Channel Name'])
print(video_df)
video_df.to_csv('trending.csv')