import asyncio


async def prints_numbers() -> None:
    for i in range(1, 8):
        await asyncio.sleep(1)
        print(f"Number: {i}")


async def main():
    await prints_numbers()


if __name__ == "__main__":
    asyncio.run(main())
