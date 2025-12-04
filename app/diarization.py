import threading
import traceback
import typing

import omegaconf
import torch
from diart import SpeakerDiarization
from diart.inference import StreamingInference
from diart.sources import MicrophoneAudioSource

from app.state import SpeakerState

torch.serialization.add_safe_globals([
    omegaconf.listconfig.ListConfig,
    omegaconf.dictconfig.DictConfig,
    omegaconf.base.ContainerMetadata,
    typing.Any,
    list,
    dict
])

class DiartObserver:
    def __init__(self, state: SpeakerState):
        self.state = state

    def on_next(self, value):
        try:
            if isinstance(value, tuple):
                prediction = value[0]
            else:
                prediction = value
            
            if prediction is not None:
                self.state.update(prediction)
        except Exception as e:
            print(f"Error in observer: {e}")

    def on_error(self, error):
        print(f"Diart stream error: {error}")

    def on_completed(self):
        print("Diart stream completed")

def run_diarization_loop(state: SpeakerState, stop_event: threading.Event):
    try:
        pipeline = SpeakerDiarization()
        mic = MicrophoneAudioSource()
        
        inference = StreamingInference(pipeline, mic, do_plot=False)
        
        observer = DiartObserver(state)
        inference.attach_observers(observer)
        
        print("Diart int working")
        
        inference()
        
    except KeyboardInterrupt:
        print("stoppingegdsfgdsfa")
    except Exception as e:
        print("error")
        traceback.print_exc()
