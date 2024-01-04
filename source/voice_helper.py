import speech_recognition as sr
import pyttsx3

class voice_processer:
    def __init__(self) -> None:
        self.sr = sr.Recognizer()
    
    def listening(self):
        with sr.Microphone() as audio_source:
            audio = self.sr.listen(audio_source)
            
            text = ''
            try:
                text = self.sr.recognize_google(audio, language='zh-tw')
                
            except:
                text = None
                
            return text
        
def say(line):
    engine = pyttsx3.init()
    engine.say(line)
    engine.runAndWait()