import sounddevice as sd
import soundfile as sf
import pyaudio
import wave
import sys
import glob
import random
import os
import datetime

OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'

chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 2
fs = 44100  # Record at 44100 samples per second

def record(seconds=3):
    word = input('Type word to record, and start recording: ')
    filename = f"{word}.wav"
    p = pyaudio.PyAudio()  # Create an interface to PortAudio
    print('Recording')
    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)
    frames = []  # Initialize array to store frames
    # Store data in chunks for 3 seconds
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the stream 
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()

    print(f'Finished recording {filename}')

    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

    return filename

def play(filename):
    # Extract data and sampling rate from file
    data, fs = sf.read(filename, dtype='float32')  
    sd.play(data, fs)
    status = sd.wait()  # Wait until file is done playing
    

def write(n_words=1000):
    files = glob.glob('*.wav')
    random.shuffle(files)
    for ff in files[:n_words]:
        repeat = True
        while repeat:
            play(ff)
            answer = input("Volgende (V) of herhaal (H)?")
            repeat = answer.lower().startswith('h')
    print("Gebruikte woorden:")
    print(", ".join([os.path.splitext(ff)[0] for ff in files]))

def do_type(n_words=12):
    report = open(f"logs/dictee_{'_'.join(str(datetime.datetime.now()).split()).split('.')[0]}.txt", 'w')

    files = glob.glob('*.wav')
    random.shuffle(files)
    used_words = files[:n_words]
    score = 0
    for ff in used_words:
        repeat = True
        while repeat:
            play(ff)
            answer = input("Welk woord hoorde je? (voor herhaling, schrijf H) ")
            repeat = answer.lower() == 'h'
            if not repeat:
                woord = os.path.splitext(ff)[0].replace('_', ' ')
                correct = answer == woord
                if correct:
                    score += 1
                    print(f"{OKGREEN}Proficiat!{ENDC}")
                    report.write(f"+ {woord}\n")
                else:
                    print(f"{FAIL}Fout, het juiste woord was {woord} (je schreef '{answer}'){ENDC}")
                    report.write(f"- {woord} (geschreven: {answer})\n")
    print("Gebruikte woorden:")
    print(", ".join([os.path.splitext(ff)[0].replace('_',' ') for ff in files]))
    msg = f"===== Testje afgelopen! ======\nJe score is: {score} / {len(used_words)}\n"
    print(msg)
    report.write(msg)
    report.flush()
            
def main(mode: str = 'opnemen'):
    if mode == 'opnemen':
        do_next = True
        while do_next:
            filename = record()
            play(filename)
            answer = input("Volgende? (of opnieuw) [J/n]")
            do_next = not answer.lower().startswith('n')
    elif mode == 'schrijven':
        write()
    elif mode == 'typen':
        do_type()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser("Dictee")
    parser.add_argument("mode", nargs=1,
            choices=['opnemen', 'typen', 'schrijven'],
            help="Opnemen: neem woordjes op via de microfoon; Typen: de gedicteerde woorden moeten worden ingegeven. Schrijven: de gedicteerde woorden moeten worden opgeschreven.")
    args = parser.parse_args()
    main(mode=args.mode[0].lower())