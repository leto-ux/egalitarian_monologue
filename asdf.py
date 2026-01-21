import asyncio
import os

from dotenv import load_dotenv
from speechmatics.rt import Microphone
from speechmatics.voice import (AgentServerMessageType, VoiceAgentClient,
                                VoiceAgentConfigPreset)

load_dotenv()

async def main():
    client = VoiceAgentClient(
        api_key=os.getenv("SPEECHMATICS_API_KEY"),
        config=VoiceAgentConfigPreset.load("adaptive")
    )

    @client.on(AgentServerMessageType.ADD_SEGMENT)
    def on_segment(message):
        for segment in message.get("segments", []):
            print(f"[{segment.get('speaker_id', 'S1')}]: {segment.get('text', '')}")

    @client.on(AgentServerMessageType.END_OF_TURN)
    def on_turn_end(message):
        print("[END OF TURN]")

    mic = Microphone(sample_rate=16000, chunk_size=320)
    mic.start()

    try:
        await client.connect()
        print("Voice agent ready. Speak now...")

        while True:
            await client.send_audio(await mic.read(320))
    finally:
        mic.stop()
        await client.disconnect()

asyncio.run(main())
