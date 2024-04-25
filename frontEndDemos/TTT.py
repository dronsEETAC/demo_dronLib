#tool to talk
import speech_recognition as sr
from gtts import gTTS
import os
import subprocess
import pygame as pygame

class TTT:
    def __init__(self, words):
        self.r = sr.Recognizer()
        self.words = words

    def detect(self):
        with sr.Microphone() as source:
            audio = self.r.listen(source, phrase_time_limit=5)
            try:
                # for testing purposes, we're just using the default API key
                # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
                # instead of `r.recognize_google(audio)`
                voice = self.r.recognize_google(audio, language="es-ES")
            except sr.UnknownValueError:
                voice = "?????"
            voice = voice.capitalize()
            print("has dicho ", voice)
        if voice in self.words:
            code = self.words.index(voice)
            return code, voice
        elif voice == "?????":
            return -1, None
        else:
            return -2, None
        ''' code = -1
        if voice == "?????":
            code = 0
        elif voice == "Conectar":
            code = 1
        elif voice == "Armar":
            code = 2
        elif voice == "Despegar":
            code = 3
        elif voice == "Izquierda":
            code = 4
        elif voice == "Derecha":
            code = 5
        elif voice == "Adelante":
            code = 6
        elif voice == "Atrás":
            code = 7
        elif voice == "Arriba":
            code = 8
        elif voice == "Abajo":
            code = 9
        elif voice == "Aterrizar":
            code = 10
        elif voice == "Retornar":
            code = 11'''


        #return code, voice


    def talk (self, sentence):
        tts = gTTS(text=sentence, lang='es')
        tts.save("tecsify.mp3")

        # Inicializar pygame
        pygame.init()

        # Ocultar la ventana de pygame
        pygame.display.set_mode((1, 1))

        # Reproducir el archivo de audio
        pygame.mixer.music.load("tecsify.mp3")
        pygame.mixer.music.play()

        # Esperar a que termine la reproducción
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        # Detener pygame
        pygame.quit()
        os.remove("tecsify.mp3")

