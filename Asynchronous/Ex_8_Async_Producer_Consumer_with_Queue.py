import asyncio
import random


async def producer(queue: asyncio.Queue) -> None:
    for i in range(5):
        await asyncio.sleep(random.uniform(0.1, 1))
        item = f"item-{i}"
        await queue.put(item)
        print(f"📦 Producer: добавил {item}")

    print("🚪 Producer: завершил работу")
    await queue.put(None)


async def consumer(queue: asyncio.Queue) -> None:
    while True:
        item = await queue.get()
        if item is None:
            queue.task_done()
            break
        print(f"⚙️ Consumer: обрабатываю {item}")
        await asyncio.sleep(random.uniform(0.5, 1.5))
        print(f"✅ Consumer: обработал {item}")
        queue.task_done()


async def main() -> None:
    queue = asyncio.Queue(maxsize=3)
    prod = asyncio.create_task(producer(queue))
    cons = asyncio.create_task(consumer(queue))

    await asyncio.gather(prod, cons)
    await queue.join()
    print("🏁 Все задачи обработаны")


if __name__ == "__main__":
    asyncio.run(main())
