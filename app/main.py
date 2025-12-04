import asyncio
import json
import os

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

from app.state import SpeakerState

NUM_SPEAKERS = int(os.getenv("NUM_SPEAKERS", 3))

state = SpeakerState(NUM_SPEAKERS)

app = FastAPI()

@app.get("/")
async def get():
    try:
        with open("app/templates/index.html", "r") as f:
            return HTMLResponse(f.read())
    except FileNotFoundError:
        return HTMLResponse("", status_code=404)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = state.get_visualization_data()

            await websocket.send_json(data)
            await asyncio.sleep(0.1)
    except WebSocketDisconnect:
        pass
    except Exception as e:
        print(f"WebSocket error: {e}")
