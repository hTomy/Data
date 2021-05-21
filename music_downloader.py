from selenium import webdriver
import subprocess
import os
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup

FNULL = open(os.devnull, 'w')

chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options=chrome_options)

driver.get("http://radioas.fm/muzika.php?cat=hitlist")
time.sleep(2)
soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.quit()

lista = soup.find('div',{'class': 'ht__list'})
list_elems = lista.findAll('div', {'class': 'ht__item'})

songs = []

for i in range(len(list_elems)):
    title = list_elems[i].find('h4', {'class': 'listview__title ht__item-tit'})
    title = title.encode_contents().decode("utf-8").replace('<span>', '- ').replace('</span>', '').replace('&amp;', '&').replace('/', '')
    yt_link = list_elems[i].find('a', {'class': 'ht__item-link'})['href']

    songs.append({'title': title, 'link': yt_link})

status = 0

for song in songs:
    print(f'\rDownloaded: {status}/{len(songs)}', end='\r')
    if song['title'] + '.mp3' not in os.listdir('music'):
        subprocess.call(f'''downloader/youtube-dl --extract-audio --audio-format mp3 -o "music/{song['title']}.%(ext)s" {song['link']}' ''', stdout=FNULL, stderr=FNULL)
        time.sleep(5)
    status += 1



