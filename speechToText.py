# returns a transcription of a set duration of recorded audio, using the device's default audio input device
def stt():
    import sounddevice as sd

    # ===================================================================== Get audio from mic ================================================================================
    # Sampling frequency in hz
    freq = 44100

    # Recording duration in seconds
    duration = 3
    # Start recorder with the set values of duration and sample frequency
    # and return a numpy array of the audio

    recording = sd.rec(int(duration * freq), samplerate=freq, channels=1)

    # Record audio for the set number of seconds
    sd.wait()

    import wavio as wv

    # Convert the NumPy array to audio file
    wv.write("recording.wav", recording, freq, sampwidth=2)

    # ==================================================================== Transcribe the audio ===============================================================================
    from faster_whisper import WhisperModel

    model_size = "small.en"
    model = WhisperModel(
        model_size, download_root="./Whisper", device="cpu", compute_type="int8"
    )

    segments, info = model.transcribe("./recording.wav", beam_size=5)

    text = "".join(segment.text for segment in segments)
    return text


t = stt()
print(t)
