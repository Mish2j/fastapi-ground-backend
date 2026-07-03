"""
@app.websocket("/ws/telemetry")
async def tel_websocket(websocket: WebSocket):
    await websocket.accept()

    try: 
        while True:
            data = generate_telemetry()
            await websocket.send_json(data)
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        print("Client disconnected")

"""