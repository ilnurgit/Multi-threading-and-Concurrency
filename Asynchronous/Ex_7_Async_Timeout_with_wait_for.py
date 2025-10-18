import asyncio
from contextlib import suppress
from random import randint


async def complete_difficult_task() -> None:
    i = 0

    try:
        while True:
            print(f"Я работаю уже {i} секунд!")
            await asyncio.sleep(1)
            i += 1
    except asyncio.CancelledError:
        print("⚠️ Сложная задача была отменена")
        raise


async def rendering_video() -> None:
    i = 0
    try:
        while i < 100:
            print(f"⏳ Рендеринг видео: {i}%")
            await asyncio.sleep(1)
            i += 10
        print("✅ Рендеринг видео завершен")
    except asyncio.CancelledError:
        print("⚠️ Рендеринг был отменен")
        raise


async def await_with_timeout(task: asyncio.Task, timeout: float, name: str) -> None:
    try:
        await asyncio.wait_for(task, timeout=timeout)
        print(f"✅ {name}: завершилась")
    except asyncio.CancelledError:
        print(f"⚠️ {name}: задача была отменена")
    except asyncio.TimeoutError:
        print(f"⏰ {name}: истёк таймаут — отменяю")
        task.cancel()
        with suppress(asyncio.CancelledError):
            await task


async def main():
    task1 = asyncio.create_task(complete_difficult_task())
    task2 = asyncio.create_task(rendering_video())

    await asyncio.sleep(randint(1, 5))
    task2.cancel()
    await asyncio.sleep(randint(1, 5))
    task1.cancel()

    await await_with_timeout(task1, 3, "Heavy Task")
    await await_with_timeout(task2, 3, "Rendering Video")


if __name__ == "__main__":
    asyncio.run(main())
