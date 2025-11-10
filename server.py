from flask import Flask, request, jsonify
import random

app = Flask(__name__)

# { "1234": {"relay_ip": "wss://...", "players": 1, "max_players": 2} }
rooms: dict[str, dict] = {}

@app.route("/")
def index():
    return "FishNet Master Server is running!"

@app.route("/create", methods=["POST"])
def create_room():
    data = request.get_json(silent=True) or {}
    relay_ip = data.get("relay_ip")
    if not relay_ip:
        return jsonify({"ok": False, "error": "Missing relay_ip"}), 400

    for _ in range(100):
        room_id = f"{random.randint(0, 9999):04d}"
        if room_id not in rooms:
            rooms[room_id] = {
                "relay_ip": relay_ip,
                "players": 0,
                "max_players": 2
            }
            print(f"🟢 Created room {room_id} ({relay_ip})")
            return jsonify({"ok": True, "room_id": room_id})

    return jsonify({"ok": False, "error": "Room ID space exhausted"}), 503


@app.route("/join/<room_id>", methods=["GET"])
def join_room(room_id: str):
    room = rooms.get(room_id)
    if not room:
        return jsonify({"ok": False, "error": "Room not found"}), 404

    if room["players"] >= room["max_players"]:
        return jsonify({"ok": False, "error": "Room full"}), 403

    room["players"] += 1
    print(f"👤 Player joined {room_id} ({room['players']}/{room['max_players']})")
    return jsonify({
        "ok": True,
        "relay_ip": room["relay_ip"],
        "players": room["players"]
    })


@app.route("/leave/<room_id>", methods=["POST"])
def leave_room(room_id: str):
    room = rooms.get(room_id)
    if not room:
        return jsonify({"ok": False, "error": "Room not found"}), 404

    room["players"] = max(0, room["players"] - 1)
    print(f"👋 Player left {room_id} ({room['players']}/{room['max_players']})")

    if room["players"] == 0:
        del rooms[room_id]
        print(f"🗑️ Deleted empty room {room_id}")

    return jsonify({"ok": True, "players": room["players"]})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
