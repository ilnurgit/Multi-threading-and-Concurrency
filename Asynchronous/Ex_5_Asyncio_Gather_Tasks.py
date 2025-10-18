import asyncio
import time


async def task1():
    print("Task-1 started")
    await asyncio.sleep(4)
    print("Task-1 completed")


async def task2():
    print("Task-2 started")
    await asyncio.sleep(1)
    print("Task-2 completed")


async def task3():
    print("Task-3 started\n")
    await asyncio.sleep(2)
    print("Task-3 completed")


async def main():
    start_time = time.perf_counter()
    await asyncio.gather(task1(), task2(), task3())
    elapsed_time = time.perf_counter() - start_time
    print(f"\nAll tasks completed in {elapsed_time:.2f} seconds")


if __name__ == "__main__":
    asyncio.run(main())
