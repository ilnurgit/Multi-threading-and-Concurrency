import asyncio


async def print_text() -> None:
    await asyncio.sleep(2)
    print("Python Exercises!")


async def main() -> None:
    await print_text()


if __name__ == "__main__":
    asyncio.run(main())
