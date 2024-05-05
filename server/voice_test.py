import pyttsx3

def initialize_engine():
    engine = pyttsx3.init()
    return engine

def list_voices(engine):
    voices = engine.getProperty('voices')
    for index, voice in enumerate(voices):
        print(f"Voice {index}: ID: {voice.id} - Name: {voice.name} - Gender: {voice.gender} - Languages: {voice.languages}")

def set_voice(engine, voice_index):
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[voice_index].id)  # Change index based on available voices

def set_speech_rate(engine, rate):
    engine.setProperty('rate', rate)  # Normal speech rate is around 200 words per minute

def set_volume(engine, volume):
    engine.setProperty('volume', volume)  # Volume can be set between 0.0 and 1.0

def speak_text(engine, text):
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    engine = initialize_engine()
    list_voices(engine)
    set_voice(engine, 0)  # Change to desired voice index
    set_speech_rate(engine, 150)  # Slower than normal
    set_volume(engine, 0.9)  # Slightly lower than maximum volume
    speak_text(engine, "Hello, this is an example of pyttsx3 with customized settings.")
