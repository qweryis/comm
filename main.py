import os
import asyncio
import websockets

PORT = int(os.environ.get('PORT', 5000))
connected = set()

async def handler(ws, path):
    connected.add(ws)
    try:
        async for message in ws:
            print(f"Received: {message}")
            reply = f"Server broadcast: {message}"
            # Prepare tasks for all other clients
            targets = [client for client in connected if client != ws]
            if targets:
                await asyncio.gather(*(client.send(reply) for client in targets))
    except websockets.ConnectionClosed:
        pass
    finally:
        connected.remove(ws)

if __name__ == "__main__":
    print(f"Starting server on port {PORT}")
    start_server = websockets.serve(handler, "0.0.0.0", PORT)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


