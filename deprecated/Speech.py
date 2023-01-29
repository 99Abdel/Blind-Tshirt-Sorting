import pocketsphinx

# Create a new recognizer object
recognizer = pocketsphinx.Decoder()

# Set the model parameters
model_path = "/path/to/model" # path to the model files
hmm = model_path + "/en-us/en-us" # path to the HMM model
lm = model_path + "/en-us/en-us.lm.bin" # path to the LM file
dictd = model_path + "/en-us/cmudict-en-us.dict" # path to the dictionary


# Set the recognizer's parameters
recognizer.set_kws("keyphrase_search", "oh mighty computer")
recognizer.set_lmfile(lm)
recognizer.set_dictfile(dictd)

# Start the microphone
microphone = pocketsphinx.AudioDevice()
microphone.open()

# Start the recognition process
in_speech_bf = False

while True:
    buf = microphone.read()
    if buf:
        # Process the audio data
        recognizer.process_raw(buf, False, False)
        if recognizer.get_in_speech() != in_speech_bf:
            in_speech_bf = recognizer.get_in_speech()
            if not in_speech_bf:
                # Recognition has stopped
                result = recognizer.get_hyp()
                if result:
                    print("You said:", result[0])

# Close the microphone
microphone.close()


