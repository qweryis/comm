import asyncio
import websockets

async def chat():
    uri = "wss://comm-s1tw.onrender.com"
    async with websockets.connect(uri) as ws:
        print("Connected to server. Type messages below (Ctrl+C to exit).")

        # Receiver coroutine: handles incoming broadcasts
        async def receive():
            try:
                async for msg in ws:
                    print(f"\n<b>Peer:</b> {msg}\nYou: ", end="", flush=True)
            except websockets.ConnectionClosed:
                print("Connection closed by server.")

        recv_task = asyncio.create_task(receive())

        # Sender loop: reads user input and sends to server
        try:
            while True:
                text = await asyncio.get_event_loop().run_in_executor(None, input, "You: ")
                if text.lower() == "exit":
                    break
                await ws.send(text)
        except (asyncio.CancelledError, KeyboardInterrupt):
            pass
        finally:
            recv_task.cancel()

if __name__ == "__main__":
    asyncio.run(chat())
