# -*- coding: utf-8 -*-
"""
Author: Fernando Lopez 
Description: This script contains the definition of the websocket client.
"""

import asyncio
import argparse
import websockets
import numpy as np

import torch
from transformers import AutoModelForCTC, AutoProcessor
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor

SERVER = "localhost"
PORT = 8001

# You can add or replace more models here
ENGLIISH_MODEL = "facebook/wav2vec2-large-960h-lv60-self"
SPANISH_MODEL = "jonatasgrosman/wav2vec2-large-xlsr-53-spanish"

class SpeechRecognitionServer:
    def __init__(self, language: str):
        if language not in ("EN", "ES"):
            raise ValueError(f"Language: '{language}', not supported.")
        
        if language == "EN":
            self.model = AutoModelForCTC.from_pretrained(ENGLIISH_MODEL)
            self.processor = AutoProcessor.from_pretrained(ENGLIISH_MODEL)
        elif language == "ES":
            self.model = Wav2Vec2ForCTC.from_pretrained(SPANISH_MODEL)
            self.processor = Wav2Vec2Processor.from_pretrained(SPANISH_MODEL)
        
        print(f"Server up.")
        
        run = websockets.serve(self.speechRecognition, SERVER, PORT)
        asyncio.get_event_loop().run_until_complete(run)
        asyncio.get_event_loop().run_forever()
        

    async def speechRecognition(self, websocket):
        print(f"-> Client connection stablished.")
        try:
            while True:
                message = await websocket.recv()
                float64_buffer = np.frombuffer(message, dtype=np.int16) / 32767
                
                if len(float64_buffer) > 1:
                    inputs = self.processor(torch.tensor(float64_buffer), sampling_rate=16_000, return_tensors="pt", padding=True)
                    with torch.no_grad():
                        logits = self.model(inputs.input_values, attention_mask=inputs.attention_mask).logits

                    predicted_ids = torch.argmax(logits, dim=-1)
                    transcription = self.processor.batch_decode(predicted_ids)[0]

                    await websocket.send(transcription.lower())
                else:
                    await websocket.send("")
        
        except KeyboardInterrupt:
            await websocket.close()
            print(f"\nServer finalized.")
        except websockets.exceptions.ConnectionClosedOK:
            print(f"<- Client connection finalized.")
        except websockets.exceptions.ConnectionClosedError:
            print(f"\nWebsocket closed.")
        except Exception:
            print(f"Server down.")

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--language", help = "Set language")
    args = parser.parse_args()

    s = SpeechRecognitionServer(language=args.language)
