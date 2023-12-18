from multiprocessing import Process
import time
import requests
from sys import argv

start_time = time.time()
all_time = 0
urls = argv[1::]


def time_calc(func):
    def wrapper(*args, **kwargs):
        all_time = time.time()
        func(*args, **kwargs)
        print(f'{time.time() - all_time:.2f} seconds')
    return wrapper


def download(url):
    res = requests.get(url)
    file_name = url.split('/')
    with open(f'multiproc/{file_name[-1]}', 'wb') as f:
        f.write(res.content)
    print(f'{time.time()-start_time:.2f} seconds | all')


@time_calc
def main_mp(urls):
    processes = []

    for url in urls:
        process = Process(target=download, args=(url, ))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()


if __name__ == '__main__':
    main_mp(urls)
