import asyncio
import threading
import os

from dotenv import load_dotenv
from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO

# Speechmatics imports
# from speechmatics.rt import Microphone
# from speechmatics.voice import (AgentServerMessageType, VoiceAgentClient,
                                # VoiceAgentConfigPreset)

# --- For mock tests --- #
import random
MOCK_SPEAKERS = [ "S1", "S2", "S3", "S4" ]
# --- --- ------ --- --- #


load_dotenv()

app = Flask( __name__, static_folder='static' )

# Can use async_mode='eventlet' or 'threading' for compatibility
socketio = SocketIO( app, cors_allowed_origins="*", async_mode='threading' )

# Global dictionary for statistics
stats = {}

@app.route( '/' )
def index():
    return send_from_directory( 'static', 'index.html' )

def update_and_emit( speaker_id ):
    """Helps update data and send it to frontend"""
    if speaker_id not in stats:
        stats[ speaker_id ] = 0
    stats[ speaker_id ] += 1

    # Send data to all connected clients
    socketio.emit( 'stats_update', stats )

# async def speechmatics_task():
#     """Main Speechmatics asynchronous loop"""
#     client = VoiceAgentClient(
#         api_key=os.getenv("SPEECHMATICS_API_KEY"),
#         config=VoiceAgentConfigPreset.load("adaptive")
#     )
#
#     @client.on(AgentServerMessageType.ADD_SEGMENT)
#     def on_segment(message):
#         for segment in message.get("segments", []):
#             speaker_id = segment.get( 'speaker_id', 'S1' )
#             text = segment.get( 'text', '' )
#             print( f"[{ speaker_id }]: { text }" )
#
#             # Send info to socket
#             update_and_emit( speaker_id )
#
#     @client.on(AgentServerMessageType.END_OF_TURN)
#     def on_turn_end(message):
#         print("[END OF TURN]")
#
#     mic = Microphone(sample_rate=16000, chunk_size=320)
#     mic.start()
#
#     try:
#         await client.connect()
#         print("Voice agent ready. Speak now...")
#
#         while True:
#             audio_chunk = await mic.read( 320 )
#             await client.send_audio( audio_chunk )
#             # Small pause
#             await asyncio.sleep( 0 )
#     except Exception as e:
#         print( f"Błąd synchronizacji: {e}" )
#
#     finally:
#         mic.stop()
#         await client.disconnect()
#
def mock_speechmatics_simulation():
    """Mock function since Mr. Rustyman didnt share his api key"""
    print( "MOCK SIMULATION" )

    while True:
        # Who will talk?
        speaker = random.choices( MOCK_SPEAKERS, weights=[40, 30, 20, 10] )[0]

        # Simulation talking 2-5s
        burst_length = random.randint( 2, 5 )

        for _ in range( burst_length ):
            update_and_emit( speaker )
            print( f"Simulation: {speaker} is talking")
            socketio.sleep( 0.1 )

        socketio.sleep( random.uniform( 0.5, 1.5 ) )


# def start_async_loop():
#     """Starts asyncio loop in another thread"""
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop( loop )
#     loop.run_until_complete( speechmatics_task() )

if __name__ == '__main__':
    # Start thread with microphone and Speechmatics
    # sm_thread = threading.Thread( target=start_async_loop, daemon=True )
    sm_thread = threading.Thread( target=mock_speechmatics_simulation, daemon=True )  # mock sim

    sm_thread.start()

    # Start Flask server ( SocketIO )
    socketio.run( app, host='0.0.0.0', port=5000, debug=False, allow_unsafe_werkzeug=True )

























