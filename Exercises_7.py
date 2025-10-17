import time
from typing import Iterable, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def make_session(
    total_retries: int = 3,  # Количество повторов
    backoff_factor: float = 0.3,  # Коэффициент задержки между попытками
    pool_connections: int = 50,  # Cколько пулов кэшировать (грубо — «сколько хостов держать открытыми»)
    pool_maxsize: int = 50,  # Cколько одновременных соединений в каждом пуле (на хост)
    status_forcelist: tuple[int, ...] = (429, 500, 502, 503, 504),
    # Список HTTP-кодов, при которых разрешено повторять запрос
) -> requests.Session:
    """
    Создаём Session с пулом соединений и политикой повторов (retry).
    """
    session = requests.Session()

    # Создаем повторы на случай ошибок сетей, таймаутов и обрывов соединений
    retry = Retry(
        total=total_retries,
        read=total_retries,
        connect=total_retries,
        status=total_retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
        allowed_methods=frozenset(
            ["HEAD", "GET", "OPTIONS"]
        ),  # Методы, для которых допускаются повторы
        raise_on_status=False,  # При ошибочных кодах возвращаем ответ, не бросаем исключение.
    )

    # Создаем адаптер, чтобы можно было использовать retry
    adapter = HTTPAdapter(
        max_retries=retry,
        pool_connections=pool_connections,
        pool_maxsize=pool_maxsize,
    )

    # Все URL с этими префиксами пойдут через наш адаптер (а значит — с ретраями и пулом)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    # Задаём дефолтный заголовок для всех запросов этой сессии
    session.headers.update(
        {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
        }
    )
    return session


def fetch(session: requests.Session, url: str, timeout: float = 10.0) -> dict[str, Any]:
    """
    Выполняет GET-запрос и возвращает компактный отчёт.
    Не бросает исключений наружу — все ошибки попадают в поле 'error'.
    """
    started = time.perf_counter()  # Начинаем замер времени. Возвращает текущее значение высокоточного счётчика времени (в секундах, с плавающей точкой)
    try:
        resp = session.get(url, timeout=timeout)
        elapsed = time.perf_counter() - started  # Закончили замер времени
        return {
            "url": url,
            "status": resp.status_code,
            "bytes": len(resp.content),
            "elapsed_sec": round(elapsed, 3),
            "error": None if resp.ok else f"HTTP {resp.status_code}",
        }
    except requests.RequestException as e:
        elapsed = time.perf_counter() - started
        return {
            "url": url,
            "status": None,
            "bytes": 0,
            "elapsed_sec": round(elapsed, 3),
            "error": str(e),
        }


def fetch_concurrently(
    urls: Iterable[str], max_workers: int = 20
) -> list[dict[str, Any]]:
    """
    Запускает конкурентные запросы.
    Возвращает список словарей-результатов (порядок — как придут ответы).
    """
    session = make_session()

    try:
        results: list[dict[str, Any]] = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(fetch, session, url): url for url in urls}
            for fut in as_completed(futures):
                results.append(fut.result())
        return results
    finally:
        session.close()


if __name__ == "__main__":
    test_urls = [
        "https://httpbin.org/get",
        "https://example.com/",
        "https://httpbin.org/status/200",
        "https://httpbin.org/delay/2",  # искусственная задержка
        "https://httpbin.org/status/503",  # сработают ретраи
    ]

    print("Запускаю конкурентные запросы... \n")
    results = fetch_concurrently(test_urls, max_workers=10)

    title = f"{'STATUS':>6} | {'ERROR':>10} | {'BYTES':>7} | {'TIME(s)':>7} | URL"
    print(title)
    print("-" * 2 * len(title))
    for r in results:
        status = r["status"] if r["status"] is not None else "--"
        error = str(r.get("error", "--"))
        print(
            f"{status:>6} | {error:>10} | {r['bytes']:>7} | {r['elapsed_sec']:>7.3f} | {r['url']}"
        )
