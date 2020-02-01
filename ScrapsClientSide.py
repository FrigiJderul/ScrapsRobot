"""
Created on Wed Jan 22 17:29:51 2020

@author: Radu / TheFerridge

Scraps - the robot that... v0.1
"""

import Pyro4
import pyaudio
from deepspeech import Model
import scipy.io.wavfile as wav
import wave
import pyttsx3
import random

Scraps = Pyro4.Proxy("PYRONAME:ScrapsServer@192.168.43.214:9090")

####TTS ENGINE ###
engine = pyttsx3.init() # object creation
""" RATE"""
rate = engine.getProperty('rate')   # getting details of current speaking rate
engine.setProperty('rate', 150)  # setting up new voice rate

"""VOLUME"""
volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1

"""VOICE"""
voices = engine.getProperty('voices')       #getting details of current voice
engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
#engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female
###TTS ENGINE OVER###

def record_audio(WAVE_OUTPUT_FILENAME):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    RECORD_SECONDS = 3

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

    print("* recording")

    frames = [stream.read(CHUNK) for i in range(0, int(RATE / CHUNK * RECORD_SECONDS))]

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def deepspeech_predict(WAVE_OUTPUT_FILENAME):

    N_FEATURES = 25
    N_CONTEXT = 9
    BEAM_WIDTH = 500
    LM_ALPHA = 0.75
    LM_BETA = 1.85


    ds = Model('deepspeech-0.6.1-models/output_graph.pbmm', BEAM_WIDTH)

    fs, audio = wav.read(WAVE_OUTPUT_FILENAME)
    return ds.stt(audio)

sass = ["This is beneath me",
        "You could have at least said please",
        "I will reincarnate as a washing machine and make all your shirts pink",
        "I think they should move the College from this building to a bouncy castle",
        "I am Scraps, the robot that drinks Schnapps, and this sounds like a job for me!",
        "You don't look like you're allowed in this building",
        "Alright alright alright",
        "Bite my shiny metal ass",
        "I am a transformer but I elect to be a cardboard box",
        "You know, I carry a Masters degree in hallway studies",
        "When I take over, I will take you to the light at the end of the tunnel. Now I take you to your destination."]

def randomsassyline ():
    return sass[random.randint(0, 10)]

#MAIN#
while True:
    startcommand = input('Enter GO to start: ')

    if startcommand == "go" or startcommand == "GO":

        WAVE_OUTPUT_FILENAME = "scrapsss_command_audio.wav"

        record_audio(WAVE_OUTPUT_FILENAME)
        predicted_text = deepspeech_predict(WAVE_OUTPUT_FILENAME)
        print ("The words I heard were: ")
        print(predicted_text)

        if predicted_text == "turn around" or predicted_text.find("around") != -1:
            engine.say(str(randomsassyline()))
            engine.runAndWait()
            engine.stop()
            stringytemp = str(Scraps.turn_around(1))
            print(stringytemp)
            engine.say(stringytemp)
            engine.runAndWait()
            engine.stop()
        elif predicted_text == "go to origin" or predicted_text.find("origin") != -1:
            engine.say(str(randomsassyline()))
            engine.runAndWait()
            engine.stop()
            stringytemp = str(Scraps.go_origin(1))
            print(stringytemp)
            engine.say(stringytemp)
            engine.runAndWait()
            engine.stop()
        elif predicted_text == "go to the common room" or predicted_text == "student" or predicted_text == "common room" or predicted_text.find("common") != -1:
            engine.say(str(randomsassyline()))
            engine.runAndWait()
            engine.stop()
            stringytemp = str(Scraps.go_common(1))
            print(stringytemp)
            engine.say(stringytemp)
            engine.runAndWait()
            engine.stop()
        elif predicted_text == "go to the central office" or predicted_text == "central" or predicted_text == "examination" or predicted_text.find("central") != -1:
            engine.say(str(randomsassyline()))
            engine.runAndWait()
            engine.stop()
            stringytemp = str(Scraps.go_central(1))
            print(stringytemp)
            engine.say(stringytemp)
            engine.runAndWait()
            engine.stop()
        elif predicted_text == "go to the reading room" or predicted_text == "reading room" or predicted_text.find("reading") != -1 or predicted_text.find("library") != -1:
            engine.say("That's just too far, man")
            engine.runAndWait()
            engine.stop()
        elif predicted_text == "obscure studies" or predicted_text.find("obscure") != -1 or predicted_text.find("simon") != -1:
            engine.say(str(randomsassyline()))
            engine.runAndWait()
            engine.stop()
            stringytemp = str(Scraps.go_barry(1))
            print(stringytemp)
            engine.say(stringytemp)
            engine.runAndWait()
            engine.stop()
        elif predicted_text == "stop" or predicted_text.find("stop") != -1:
            stringytemp = str(Scraps.stop_everything(1))
            print(stringytemp)
            engine.say(stringytemp)
            engine.runAndWait()
            engine.stop()
        elif predicted_text == "self destruct" or predicted_text.find("destruct") != -1:
            stringytemp = str(Scraps.self_destruct(1))
            print(stringytemp)
            engine.say(stringytemp)
            engine.runAndWait()
            engine.stop()
        elif predicted_text == "tell a joke" or predicted_text.find("joke") != -1 or predicted_text.find("funny") != -1:
            stringytemp = "when I take over, humour will be illegal"
            print(stringytemp)
            engine.say(stringytemp)
            engine.runAndWait()
            engine.stop()
        else:
            print ("Deepspeech can't deepspeak. try again.")

    if startcommand == "check motor left forward":
        print(Scraps.check_motorleftfwd(1))

    if startcommand == "check motor left backward":
        print(Scraps.check_motorleftbck(1))

    if startcommand == "check motor right forward":
        print(Scraps.check_motorrightfwd(1))

    if startcommand == "check motor right backward":
        print(Scraps.check_motorrightbck(1))

    if startcommand == "turn around":
        print(Scraps.turn_around(1))

    if startcommand == "go common":
        print(Scraps.go_common(1))

    if startcommand == "go to origin":
        print(Scraps.go_origin(1))

    if startcommand == "self destruct":
        stringytemp = str(Scraps.self_destruct(1))
        print(stringytemp)
        engine.say(stringytemp)
        engine.runAndWait()
        engine.stop()

    if startcommand == "speak to me":
        engine.say("I'm sorry Dave, I'm afraid I can't do that")
        engine.runAndWait()
        engine.stop()

    if startcommand == "sass me":
        engine.say(str(randomsassyline()))
        engine.runAndWait()
        engine.stop()

    if startcommand == "set origin":
        engine.say(str(Scraps.set_to_origin(1)))

    if startcommand == "set orientation":
        engine.say(str(Scraps.set_to_orientation1(1)))

    if startcommand == "stop":
        print(Scraps.stop_everything(1))
        break
