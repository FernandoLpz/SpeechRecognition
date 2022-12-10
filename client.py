import pyaudio
import asyncio
import webrtcvad
import websockets

CHANNELS = 1                                
RATE = 16000                                
FRAME_DURATION = 30                         
FORMAT = pyaudio.paInt16    
CHUNK = int(RATE * FRAME_DURATION / 1000)
INPUT_DEVICE = "UMC204HD 192k"             
SERVER = "ws://localhost:8001/"

vad = webrtcvad.Vad()
vad.set_mode(1)

class SpeechRecognitionClient:

    def __init__(self):
        self.transcript = ""
        self.audio = pyaudio.PyAudio()

        self.getAudioInterface()
        self.setStreamSettings()
        
        asyncio.run(self.startStream())

        self.stream.close()
        self.audio.terminate()


    async def startStream(self):
        async with websockets.connect(SERVER) as websocket:
            frames = b''
            try:
                while True:
                    frame = self.stream.read(CHUNK, exception_on_overflow=False)
                    if vad.is_speech(frame, RATE):
                        frames += frame
                    elif len(frames) > 1:
                        await websocket.send(frames)
                        frames = b''
                        
                        text = await websocket.recv()
                        self.transcript = f"{self.transcript} {text}" if len(text) > 1 else self.transcript
                        print(f"> {self.transcript}")

    
            except KeyboardInterrupt:
                await websocket.close()
                print(f"\nWebsocket closed.")
            except websockets.exceptions.ConnectionClosedError:
                print(f"\nWebsocket closed.")
            except Exception:
                print(f"\nWebsocket closed.")
            finally:
                print('*'*50)
                print(f"\nTranscript: \n\n{self.transcript}\n")


    def setStreamSettings(self):
        self.stream = self.audio.open(
                input_device_index=self.inputDevice, 
                format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)


    def getAudioInterface(self):
        self.inputDevice = None
        numDevices = self.audio.get_host_api_info_by_index(0)["deviceCount"]
        for index in range(numDevices):
            name = self.audio.get_device_info_by_host_api_device_index(0, index).get("name")
            if name == INPUT_DEVICE:
                self.inputDevice = index
                break
        
        if not self.inputDevice:
            raise ValueError(f"Audio device was not found under name: {INPUT_DEVICE}")


if __name__ == '__main__':
    s = SpeechRecognitionClient()