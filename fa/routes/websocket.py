# routes /routes/websocket.py

from fastapi import WebSocket, WebSocketDisconnect

async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Odbieranie danych z Telegrama
            command = await websocket.receive_text()
            print(f"Odebrano polecenie: {command}")

            if command == "ping":
                await websocket.send_text("Pong od WS")
            else:
                await websocket.send_text(f"Nieznane polecenie: {command}")
    except WebSocketDisconnect:
        print("Polaczenie Websocket zostalo zamkniete.")