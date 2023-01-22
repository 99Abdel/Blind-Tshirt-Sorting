import speech_recognition as sr

def recognise_speech():
    # initialize recognizer class (for recognizing the speech)
    r = sr.Recognizer()
    frase = ""
    # Reading Microphone as source
    # listening the speech and store in audio_text variable
    with sr.Microphone() as source:
        print("Talk")
        audio_text = r.listen(source)
        print("Time over, thanks")

        # recoginize_() method will throw a request error if the API is unreachable, hence using exception handling
        try:
            # using google speech recognition
            frase = r.recognize_google(audio_text, language='en-US')
            print("Text: " + frase)
        except:
            print("Sorry, I did not get that")

    return frase
