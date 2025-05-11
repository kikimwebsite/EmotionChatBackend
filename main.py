import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from starlette_graphene3 import GraphQLApp
from schema import schema
from emotion import run_and_display_nonzero_emotions
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  #replace "https://yourdomain.com"
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to EmotionChat!"}

app.add_route("/graphql", GraphQLApp(schema=schema))

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            try:
                data = await asyncio.wait_for(websocket.receive_text(), timeout=210)
                
                if len(data) > 1000:
                    await websocket.send_json({"error": "Input data exceeds 1000 characters. Please send smaller text."})
                    logger.warning("Client sent input exceeding 1000 characters. Rejecting request.")
                    continue

                try:
                    emotion_results = run_and_display_nonzero_emotions(data)
                except Exception as e:
                    logger.error(f"Error processing emotions: {e}")
                    await websocket.send_json({"error": "Failed to process emotions."})
                    continue

                await websocket.send_json({
                    "text": data,
                    "emotions": [
                        {"label": label, "score": score} for label, score in emotion_results
                    ]
                })
            except asyncio.TimeoutError:
                logger.info("WebSocket connection timed out due to inactivity.")
                await websocket.close(code=1001)
    except WebSocketDisconnect:
        print("WebSocket disconnected.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        await websocket.close(code=1006)


