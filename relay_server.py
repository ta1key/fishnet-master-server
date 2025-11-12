import asyncio
import websockets
import os
import json

PORT = int(os.environ.get("PORT", 10000))
rooms = {}  # room_id -> set of websockets

async def handler(ws):
    room_id = None
    try:
        while True:
            msg = await ws.recv()

            # --- 🧠 FishNetの通信は「バイナリ」 ---
            # バイナリならそのまま中継
            if isinstance(msg, bytes):
                if room_id and room_id in rooms:
                    for client in rooms[room_id]:
                        if client != ws:
                            await client.send(msg)
                continue

            # --- 🧠 JSONコマンド（joinなど）はテキスト ---
            try:
                data = json.loads(msg)
            except:
                data = None

            if data and data.get("cmd") == "join":
                room_id = data["room"]
                if room_id not in rooms:
                    rooms[room_id] = set()
                rooms[room_id].add(ws)
                print(f"🟢 Client joined room {room_id}")
                continue

    except Exception as e:
        print(f"⚠️ Error: {e}")
    finally:
        # クライアント切断時
        if room_id and room_id in rooms:
            rooms[room_id].discard(ws)
            if not rooms[room_id]:
                del rooms[room_id]
        print(f"🔴 Client disconnected from room {room_id}")

async def main():
    async with websockets.serve(handler, "0.0.0.0", PORT):
        print(f"🚀 Relay server running on port {PORT}")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())