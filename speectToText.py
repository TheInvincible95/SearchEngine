from faster_whisper import WhisperModel
import sounddevice as sd
import wavio as wv


# returns a transcription of a set duration of recorded audio, using the device's default audio input device
def stt():

    # ===================================================================== Get audio from mic ================================================================================
    # Sampling frequency in hz
    freq = 44100

    # Recording duration in seconds
    duration = 3

    # Start recorder with the set values of duration and sample frequency
    # and return a numpy array of the audio
    recording = sd.rec(int(duration * freq),
                       samplerate=freq, channels=2)

    # Record audio for the set number of seconds
    sd.wait()

    # Convert the NumPy array to audio file
    wv.write("recording.wav", recording, freq, sampwidth=2)

    # ==================================================================== Transcribe the audio ===============================================================================

    model_size = "small.en"
    model = WhisperModel(model_size, download_root="./Whisper", device="cpu")

    segments, info = model.transcribe(
        "./recording.wav", beam_size=5)

    print("Detected language '%s' with probability %f" %
          (info.language, info.language_probability))

    for segment in segments:
        print("[%.2fs -> %.2fs] %s" %
              (segment.start, segment.end, segment.text))

    return segments[0].text


text = stt()
print(text)
