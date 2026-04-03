import json
from vosk import Model, KaldiRecognizer
import pyaudio

#model and recognizers
modelEN = Model(r"C:\\Users\\Nathaniel\\Documents\\GitHub\\Broadino_Project\\vosk-model-small-en-us-0.15")
modelES = Model(r"C:\\Users\\Nathaniel\\Documents\\GitHub\\Broadino_Project\\vosk-model-small-es-0.42")

recognizerEN = KaldiRecognizer(modelEN, 16000)
recognizerES = KaldiRecognizer(modelES, 16000)

active_rec = recognizerEN

mic = pyaudio.PyAudio()

stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input= True, frames_per_buffer=8192)
stream.start_stream()

while True:
    data = stream.read(4096, exception_on_overflow=False)
    
    if active_rec.AcceptWaveform(data):
        result_json = json.loads(active_rec.Result())
        text = result_json.get("text", "").lower()

        if not text:
            continue

        #switch to spanish if word in trigger list
        if active_rec == recognizerEN:
            spanish_triggers = ["my whore oh", "may or oh", "major oh", "measure oh", "may whore oh", "my who are oh", "mejor oh", "my oh", "man whore oh"]
            if any(trigger in text for trigger in spanish_triggers) or "mejor" in text:

                active_rec = recognizerES

                continue 

        #switch to english if word in trigger list
        elif active_rec == recognizerES:
            english_triggers = ["big oh", "beck o", "bec o más", "vega a o", "pega o", "beck", "ve", "vega", "ve o"]
            if any(trigger in text for trigger in english_triggers):

                active_rec = recognizerEN

                continue
                
        #command recognized in english
        if active_rec == recognizerEN and "big oh" in text:
            print(f"Command: {text}")

        #command recognized in spanish
        elif active_rec == recognizerES and "mejor o" in text:
            print(f"Command: {text}")

        print(f"{text}")
