from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import base64, cv2
from closed_loop import ClosedLoopAgent

app = FastAPI()
agent = ClosedLoopAgent("scenarios/neurodoom_room.cfg")

@app.get("/")
async def index():
    with open("../frontend/index.html") as f:
        return HTMLResponse(f.read())

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    while True:
        frame, spikes, action = agent.step()
        # encode frame as base64
        _, jpg = cv2.imencode(".jpg", frame)
        frame_b64 = base64.b64encode(jpg).decode("utf-8")
        await ws.send_json({
            "frame": frame_b64,
            "spikes": spikes.tolist(),
            "action": action
        })
