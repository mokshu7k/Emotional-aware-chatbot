import sounddevice as sd
import soundfile as sf
import queue, sys, uuid, datetime
from pathlib import Path

# ------------ parameters you might want to tweak -------------
SAMPLERATE  = 44100          # Hz
CHANNELS    = 2              # 1 = mono, 2 = stereo …
SUBTYPE     = 'PCM_16'       # 16‑bit WAV
OUT_DIR     = Path("recordings")  # where files go
# --------------------------------------------------------------

# Ensure the output directory exists
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Build a unique file name: e.g. recordings/20250702_201530_f3a9e0a2.wav
timestamp   = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
random_stub = uuid.uuid4().hex[:8]           # 8‑char random string
FILENAME    = OUT_DIR / f"{timestamp}_{random_stub}.wav"

q = queue.Queue()

def audio_callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(indata.copy())

print(f"🎙️  Recording…  Press Ctrl+C to stop (saving to {FILENAME})")

try:
    with sf.SoundFile(FILENAME, mode='w',
                      samplerate=SAMPLERATE,
                      channels=CHANNELS,
                      subtype=SUBTYPE) as wav_file, \
         sd.InputStream(samplerate=SAMPLERATE,
                        channels=CHANNELS,
                        callback=audio_callback):
        while True:
            wav_file.write(q.get())

except KeyboardInterrupt:
    print(f"\n🛑  Stopped — saved to: {FILENAME}")

except Exception as e:
    print("Error:", e)
