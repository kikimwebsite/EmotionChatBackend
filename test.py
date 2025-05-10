import asyncio
import websockets
import json

async def test_websocket():
    uri = "ws://localhost:8000/ws"
    async with websockets.connect(uri) as websocket:

        input_text = "I’m leaving for college tomorrow. I’m excited for the new adventure but sad to leave my family behind."
        await websocket.send(input_text)


        response = await websocket.recv()
        data = json.loads(response)
        print(f"Input Text: {data['text']}")
        print("Emotions:")
        for emotion in data['emotions']:
            label = emotion['label']
            score = emotion['score']
            print(f"- {label.capitalize()}: {score:.2f}")

asyncio.run(test_websocket())