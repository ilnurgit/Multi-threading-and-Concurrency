import asyncio
from aiohttp import ClientSession
import time

URLS = [
    "https://example.com/",  # простой HTML
    "http://example.com/",  # HTTP-вариант (для проверки перенаправлений)
    "https://www.python.org/",  # официальный сайт Python
    "https://www.wikipedia.org/",  # страница с множеством языков
    "https://www.w3schools.com/",  # учебный HTML-ресурс
    "https://jsonplaceholder.typicode.com/todos/1",  # пример API, возвращает JSON
    "https://httpbin.org/get",  # JSON с информацией о запросе
    "https://httpbin.org/image/png",  # бинарный контент (PNG)
    "https://httpstat.us/500",  # имитация ошибки сервера 500
    "https://httpstat.us/200",  # успешный статус 200
]


async def fetch_data_from_url(url: str, session: ClientSession) -> None:
    try:
        async with session.get(url, timeout=10) as response:
            print(f"[{url}] Status: {response.status}")
            html = await response.text(encoding="UTF-8")
            save_file(url, html)
    except Exception as e:
        print(f"[{url}] Error: {e}")


def save_file(url: str, html: str) -> None:
    file_name = url.split("/")[2] + ".html"
    with open(file_name, "w", encoding="UTF-8") as file:
        file.write(html)
    print(f"[+] Saved: {file_name}")


async def main(urls: list[str]) -> None:
    start = time.perf_counter()
    async with ClientSession() as session:
        tasks = [asyncio.create_task(fetch_data_from_url(url, session)) for url in urls]
        await asyncio.gather(*tasks)
    print(f"Время выполнения программы заняло {time.perf_counter() - start:.3f} секунд")


if __name__ == "__main__":
    asyncio.run(main(URLS))
