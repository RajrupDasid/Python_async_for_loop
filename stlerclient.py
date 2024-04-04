import asyncio
import httpx


async def fake_file_data():
    yield b"Hello, "
    await asyncio.sleep(1)  # fake lag
    yield b"world"
    yield b""


async def main():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://127.0.0.1:5000",
            data=fake_file_data()
        )
        data = response.read()
        print("Got response", data.hex())


if __name__ == '__main__':
    asyncio.run(main())
