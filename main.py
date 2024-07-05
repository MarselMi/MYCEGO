'''
Всем привет, это моя первая работа с изображениями и Yandex.диском, на все потратил ~ 5-6 часов
'''
import os
from pathlib import Path
from urllib.parse import urlencode
import requests
import zipfile
from PIL import Image


public_key = 'https://disk.yandex.ru/d/V47MEP5hZ3U1kg'
final_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?' + urlencode(dict(public_key=public_key))
response = requests.get(final_url)
download_link = response.json()['href']
response = requests.get(download_link, stream=True)

with open('file.zip', 'wb') as f:
    '''Записываем архив с Яндекс.диска в текущую директорию'''
    response.raw.decode_content = True
    f.write(response.content)


with zipfile.ZipFile("file.zip", "r") as zf:
    '''Извлекаем архив'''
    zf.extractall()

# директория в которой будет проводиться поиск по папкам
search_dir = Path(__file__).resolve().parent / 'Для тестового/'


def convert_images_to_tiff(input_folder_list: list[str]):
    with open('Result.tif', 'wb'):
        '''Создаю/перезаписываю файл Result.tif'''
        pass

    merged_image = Image.new(
        mode="RGB",
        size=(4000, 4800)  # задаю макс размеры, были другие варианты, но оставил так
    )  # создаю экземпляр обьекта который будут принимать картинки

    index_x = 0
    index_y = 0

    for folder in input_folder_list:
        '''цикл для прохождения по списку папок'''
        path_files = search_dir / folder
        images = os.listdir(path_files)

        for image in images:
            '''Цикл для обьединения картинок внутри папки'''
            if index_x < 4000:
                img = Image.open(search_dir / folder / image)
                merged_image.paste(img, (index_x, index_y))
                index_x += img.size[0]
            else:
                '''переход на новую строку, чтобы не было накладок на фотографии'''
                index_x = 0
                img = Image.open(search_dir / folder / image)
                index_y += img.size[1]
                merged_image.paste(img, (index_x, index_y))
                index_x += img.size[0]

    merged_image.save('Result.tif', 'TIFF')


convert_images_to_tiff(
    [
        '1388_2_Наклейки 3-D_1',
        '1388_6_Наклейки 3-D_2',
        '1388_12_Наклейки 3-D_3',
        '1369_12_Наклейки 3-D_3'
    ]
)  # вызов функции со списком папок

