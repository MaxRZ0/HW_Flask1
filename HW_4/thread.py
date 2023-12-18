"""Написать программу, которая скачивает изображения с заданных URL-адресов и сохраняет их на диск. Каждое изображение
должно сохраняться в отдельном файле, название которого соответствует названию изображения в URL-адресе.
Например, URL-адрес: https://example/images/image1.jpg -> файл на диске: image1.jpg
— Программа должна использовать многопоточный, многопроцессорный и асинхронный подходы.
— Программа должна иметь возможность задавать список URL-адресов через аргументы командной строки.
— Программа должна выводить в консоль информацию о времени скачивания каждого изображения и
общем времени выполнения программы."""

import threading
import time
import requests
from sys import argv

start_time = time.time()
all_time = 0
urls = argv[1::]


def download(url):
    global all_time
    res = requests.get(url)
    file_name = url.split('/')
    with open(f'thread/{file_name[-1]}', 'wb') as f:
        f.write(res.content)
    print(f'{time.time() - start_time:.2f} seconds')
    all_time += time.time() - start_time


threads = []

for url in urls:
    thread = threading.Thread(target=download, args=[url])
    threads.append(thread)
    thread.start()
    if url == urls[-1]:
        check = True

for thread in threads:
    thread.join()

if check:
    print(f'{all_time:.2f} seconds | all')
