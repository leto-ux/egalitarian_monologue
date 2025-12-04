import os
import sys
import threading

import uvicorn

sys.path.append(os.getcwd())

from app.diarization import run_diarization_loop
from app.main import app, state


def main():
    diart_thread = threading.Thread(
        target=run_diarization_loop, 
        args=(state, None),
        daemon=True
    )
    diart_thread.start()
    
    try:
        print("localhost:8000")
        uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
    except KeyboardInterrupt:
        print("stopppinngggeddded")

if __name__ == "__main__":
    main()
