import eventlet
eventlet.monkey_patch()  # Call this before importing other modules

from flask import Flask, request, render_template
from flask_socketio import SocketIO, emit
import threading
import mss
import base64
import time
import os
import sys

app = Flask(__name__)
socketio = SocketIO(app, async_mode='eventlet')  # Specify eventlet as async_mode

clients = []

@app.route("/")
def index():
    return "Signaling server is running!"

@socketio.on("connect")
def handle_connect():
    clients.append(request.sid)
    print(f"Client connected: {request.sid}")

@socketio.on("disconnect")
def handle_disconnect():
    clients.remove(request.sid)
    print(f"Client disconnected: {request.sid}")

@socketio.on("offer")
def handle_offer(data):
    emit("offer", data, broadcast=True, include_self=False)

@socketio.on("answer")
def handle_answer(data):
    emit("answer", data, broadcast=True, include_self=False)

@socketio.on("candidate")
def handle_candidate(data):
    emit("candidate", data, broadcast=True, include_self=False)

def start_server():
    # Use eventlet to run the server
    socketio.run(app, host="0.0.0.0", port=5000, use_reloader=False, debug=False)

def main():
    print("Starting signaling server...")
    # Starting the server in a separate thread
    threading.Thread(target=start_server, daemon=True).start()  # daemon=True allows the thread to exit when the main program exits
    print("Signaling server started at: http://192.168.0.102:5000")
    
    # Keep the main program running indefinitely
    while True:
        time.sleep(1)

if __name__ == "__main__":
    # Check if we are running in Termux, and try to background the process
    if 'termux' in sys.argv:
        # Run the server as a background process (daemonize it)
        pid = os.fork()
        if pid > 0:
            sys.exit(0)  # Parent process exits
        else:
            # Child process will continue running the server
            main()
    else:
        main()
