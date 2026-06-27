import asyncio
import websockets

SERVER = "ws://YOUR_SERVER_IP:8765"

async def receive(ws):
    async for message in ws:
        print(f"\n{message}")

async def send(ws):
    while True:
        target = input("Send to: ")
        text = input("Message: ")

        await ws.send(f"MSG|{target}|{text}")

async def main():
    username = input("Username: ")

    async with websockets.connect(SERVER) as ws:
        await ws.send(username)

        await asyncio.gather(
            receive(ws),
            send(ws)
        )

asyncio.run(main())
