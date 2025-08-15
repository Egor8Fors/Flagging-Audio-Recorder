import pyaudio
import wave
import time
import threading
import sys
import argparse

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

recording = False
flags = []

def record_audio(filename):
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    frames = []
    global recording
    recording = True
    start_time = time.time()
    while recording:
        data = stream.read(CHUNK)
        frames.append(data)
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    print(f"Recording saved to {filename}")
    print("Flags:", flags)

def flag_handler():
    global recording
    start_time = time.time()
    while recording:
        input_str = input()
        if input_str.lower() == 'f':
            timestamp = time.time() - start_time
            note = input("Enter note (optional): ")
            flags.append({"time": timestamp, "note": note})
        elif input_str.lower() == 'q':
            recording = False

def main():
    parser = argparse.ArgumentParser(description="Flagging Audio Recorder")
    parser.add_argument("filename", help="Output WAV filename")
    args = parser.parse_args()

    print("Press Enter to start recording. 'f' to flag, 'q' to quit.")
    input()
    record_thread = threading.Thread(target=record_audio, args=(args.filename,))
    flag_thread = threading.Thread(target=flag_handler)
    record_thread.start()
    flag_thread.start()
    record_thread.join()

if __name__ == "__main__":
    main()
