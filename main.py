# import os
# import asyncio
# import websockets

# # <b>Port configuration</b>
# PORT = int(os.environ.get("PORT", 5000))

# # <b>Buffers of undelivered messages per client ID</b>
# message_buffers: dict[str, list[str]] = {}

# # <b>Active WebSockets per client ID</b>
# active_clients: dict[str, websockets.WebSocketServerProtocol] = {}

# async def handler(ws: websockets.WebSocketServerProtocol, path: str):
#     # Derive a unique client_id (e.g., "/alice" → "alice")
#     client_id = path.lstrip("/")

#     # Ensure a buffer exists for this client
#     if client_id not in message_buffers:
#         message_buffers[client_id] = []

#     # Register this WebSocket as active
#     active_clients[client_id] = ws

#     # <b>Flush pending messages</b>
#     for msg in message_buffers[client_id]:
#         await ws.send(msg)
#     message_buffers[client_id].clear()

#     try:
#         async for message in ws:
#             broadcast = f"Server broadcast: {message}"

#             # 1) <b>Buffer for every client</b>
#             for buf in message_buffers.values():
#                 buf.append(broadcast)

#             # 2) <b>Immediately send</b> to connected clients (excluding sender)
#             for cid, client_ws in list(active_clients.items()):
#                 if cid != client_id and not client_ws.closed:
#                     try:
#                         await client_ws.send(broadcast)
#                     except websockets.ConnectionClosed:
#                         # Clean up closed connections
#                         active_clients.pop(cid, None)

#     finally:
#         # On disconnect, remove from active_clients
#         active_clients.pop(client_id, None)

# if __name__ == "__main__":
#     print(f"Starting server on port {PORT}")
#     start_server = websockets.serve(handler, "0.0.0.0", PORT)
#     asyncio.get_event_loop().run_until_complete(start_server)
#     asyncio.get_event_loop().run_forever()

from twisted.internet import reactor, protocol
from twisted.mail import imap4, maildir
from mailbox import Maildir

# Ensure the Maildir directory exists (string path)
mailbox_path = 'mailbox'
Maildir(mailbox_path, create=True)

class MaildirIMAPServer(imap4.IMAP4Server):
    def __init__(self, userMailbox, *args, **kwargs):
        self.users = {'user': 'password'}
        # Pass just the path (string); default factory=None
        self.mailbox = maildir.MaildirMailbox(userMailbox)
        super().__init__(*args, **kwargs)

    def authenticateUser(self, identity, password, context):
        if self.users.get(identity) == password:
            return self.mailbox
        raise imap4.MailboxError("Authentication failed")

class IMAPFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return MaildirIMAPServer(mailbox_path)

if __name__ == '__main__':
    reactor.listenTCP(1430, IMAPFactory())
    print("**IMAP server running on port 1430**")
    reactor.run()





