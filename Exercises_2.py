import requests
import threading

files_to_download = [
    {
        "url": "https://en.wikipedia.org/wiki/British_logistics_in_the_Normandy_campaign",
        "filename": "wfile1",
    },
    {
        "url": "https://en.wikipedia.org/wiki/Graph_(abstract_data_type)",
        "filename": "Graph_abstract_data_type",
    },
    {"url": "https://example.com/", "filename": "example"},
]


def save_file(url: str, filename: str) -> None:
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    print(f"\n{filename} downloaded successfully.")


threads = []

for file in files_to_download:
    thread = threading.Thread(target=save_file, args=(file["url"], file["filename"]))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()
