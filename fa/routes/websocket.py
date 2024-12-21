# routes /routes/websocket.py

from fastapi import WebSocket, WebSocketDisconnect

async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Odbieranie danych z Telegrama
            command = await websocket.receive_text()
            print(f"Command received: {command}")

            if command == "ping":
                await websocket.send_text("Pong od WS")
            else:
                await websocket.send_text(f"Unknown command: {command}")
    except WebSocketDisconnect:
        print("The Websocket connection has been closed.")