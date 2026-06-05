#! python 
import requests
from bs4 import BeautifulSoup
import fake_useragent 
from tqdm import tqdm

ua = fake_useragent.FakeUserAgent().random
header = {'user-agent' : ua}
image_number = 0
page = 1
url = 'https://zastavok.net/'

for storage in range(5):

    responce = requests.get(f"{url}/{page}", headers=header)

    if responce.status_code!=200 : 
        print("Error")

    soupe = BeautifulSoup(responce.text, 'lxml')

    block = soupe.find('div', class_ = 'block-photo')
    all_image = block.find_all('div', class_ = 'short_full')
    for image in tqdm(all_image, desc='Скачиваю картинки'): 
        image_link = image.find('a').get('href')
        download_storage = requests.get(f'{url}/{image_link}')
        if download_storage.status_code != 200 : print(download_storage.status_code)
        download_soup = BeautifulSoup(download_storage.text, 'lxml')
        download_block = download_soup.find('div', class_ = 'image_data').find('div', class_ = 'block_down')
        result_link = download_block.find('a').get('href')

        image_bytes = requests.get(f'{url}/{result_link}').content
        with open(f'image/{image_number}.jpg', 'wb') as file:
            file.write(image_bytes)
        image_number += 1
        print(f'Image {image_number}.jpg successfull downloading !')
    page += 1