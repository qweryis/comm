import os
import asyncio
import websockets

PORT = int(os.environ.get('PORT', 5000))
connected = set()

async def handler(ws, path):
    # Register new client
    connected.add(ws)
    try:
        async for message in ws:
            print(f"Received from a client: {message}")
            reply = f"Server broadcast: {message}"
            # Send to every connected client except the sender
            targets = [client for client in connected if client != ws]
            if targets:
                await asyncio.wait([client.send(reply) for client in targets])
    except websockets.ConnectionClosed:
        pass
    finally:
        # Unregister client
        connected.remove(ws)

if __name__ == "__main__":
    print(f"Starting server on port {PORT}")
    start_server = websockets.serve(handler, "0.0.0.0", PORT)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

