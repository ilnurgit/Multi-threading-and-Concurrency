import asyncio
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


async def main():
    task1 = asyncio.create_task(complete_difficult_task())
    task2 = asyncio.create_task(rendering_video())
    await asyncio.sleep(randint(1, 5))
    task2.cancel()
    await asyncio.sleep(randint(1, 5))
    task1.cancel()

    try:
        res = await asyncio.gather(task1, task2, return_exceptions=True)
    except asyncio.CancelledError:
        print("Задачи были отменены")
    finally:
        print(res)


if __name__ == "__main__":
    asyncio.run(main())
