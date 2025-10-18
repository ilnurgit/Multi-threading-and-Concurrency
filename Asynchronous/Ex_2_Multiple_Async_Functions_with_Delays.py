import asyncio


async def print_name_1s() -> None:
    await asyncio.sleep(1)
    print(f"Function name: {print_name_1s.__name__}")


async def print_name_2s() -> None:
    await asyncio.sleep(2)
    print(f"Function name: {print_name_2s.__name__}")


async def print_name_3s() -> None:
    await asyncio.sleep(3)
    print(f"Function name: {print_name_3s.__name__}")


async def main() -> None:
    tasks = [print_name_1s(), print_name_2s(), print_name_3s()]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
