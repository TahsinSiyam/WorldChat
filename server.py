import asyncio
import websockets

clients = {}

async def handler(websocket):
    username = await websocket.recv()

    if username in clients:
        await websocket.send("Username already exists.")
        return

    clients[username] = websocket

    print(f"{username} connected")

    try:
        async for message in websocket:
            parts = message.split("|", 2)

            if len(parts) != 3:
                continue

            _, target, text = parts

            if target in clients:
                await clients[target].send(
                    f"{username}: {text}"
                )
            else:
                await websocket.send("User not online.")

    except websockets.ConnectionClosed:
        pass

    finally:
        print(f"{username} disconnected")
        clients.pop(username, None)

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print("Server running on port 8765")
        await asyncio.Future()

asyncio.run(main())
