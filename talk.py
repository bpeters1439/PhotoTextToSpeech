#import pyttsx3
#engine = pyttsx3.init()
#engine.say("fuck you")
#engine.runAndWait()

import pyttsx3
engine = pyttsx3.init() # object creation

""" RATE"""
rate = engine.getProperty('rate')   # getting details of current speaking rate
print (rate)                        #printing current voice rate
engine.setProperty('rate', 200)     # setting up new voice rate


"""VOLUME"""
volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
print (volume)                          #printing current volume level
engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1

"""TEST INPUT CHANGE"""
print("Type 1 for English and 2 for Spanish.")
language = input()
print("What should I say?")
phrase:str = input()

"""VOICE"""
voices = engine.getProperty('voices')       #getting details of current voice

if language == "1":
#engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
    engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female
    engine.say(phrase)
    engine.runAndWait()
    engine.stop()

elif language == "2": 
    es_voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-MX_SABINA_11.0"
    engine.setProperty('voice', es_voice_id)
    engine.say(phrase)
    engine.runAndWait()
    engine.stop()

else:
    print("Error not an option")
    engine.say("Error not an option")
    engine.runAndWait()
    engine.stop()

#engine.say("How are you doing?")
#engine.runAndWait()
#engine.stop()