import time
import asyncio
import aiohttp
from sys import argv

start_time = time.time()
all_time = 0
urls = argv[1::]


async def download(url):
    global all_time
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as res:
            content = await res.read()
            filename = url.split('/')
            with open(f'async_folder/{filename[-1]}', 'wb') as f:
                f.write(content)
                print(f'{time.time() - start_time:.2f} seconds')
                all_time += time.time() - start_time
                if url != urls[-1]:
                    print(f'{all_time:.2f} seconds | all')


async def main():
    tasks = []
    for url in urls:
        task = asyncio.ensure_future(download(url))
        tasks.append(task)
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
