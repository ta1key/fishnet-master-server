import asyncio
import websockets
import json
import os

PORT = int(os.environ.get("PORT", 10000))

clients = {}  # room_id -> [websockets]

async def handler(websocket):
    room_id = None
    try:
        async for msg in websocket:
            data = json.loads(msg)
            cmd = data.get("cmd")

            if cmd == "join":
                room_id = data["room"]
                if room_id not in clients:
                    clients[room_id] = []
                clients[room_id].append(websocket)
                print(f"✅ Joined room: {room_id}")
                continue

            # broadcast to others
            if room_id and room_id in clients:
                for ws in clients[room_id]:
                    if ws != websocket:
                        await ws.send(msg)

    except Exception as e:
        print("Error:", e)
    finally:
        if room_id and room_id in clients:
            clients[room_id].remove(websocket)
            if not clients[room_id]:
                del clients[room_id]
        print(f"❌ Disconnected from {room_id}")

async def main():
    async with websockets.serve(handler, "0.0.0.0", PORT):
        print("🚀 Relay server running on port " + PORT)
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
