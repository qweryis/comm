import os
import asyncio
import websockets

PORT = int(os.environ.get('PORT', 5000))

connected = set()

async def handler(ws, path):
    connected.add(ws)
    try:
        async for message in ws:
            print(f"Client: {message}")
            reply = f"Server echo: {message}"
            # broadcast reply back to sender
            print(reply)
            await ws.send(reply)
    finally:
        connected.remove(ws)

if __name__ == "__main__":
    print(f"Starting server on port {PORT}")
    asyncio.get_event_loop().run_until_complete(
        websockets.serve(handler, "0.0.0.0", PORT)
    )
    asyncio.get_event_loop().run_forever()
