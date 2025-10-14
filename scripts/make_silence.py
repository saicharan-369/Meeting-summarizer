import wave, struct
path='sample_silence.wav'
duration_s=2
framerate=16000
nframes=duration_s*framerate
with wave.open(path,'w') as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(framerate)
    for i in range(nframes):
        w.writeframes(struct.pack('<h',0))
print('WROTE',path)
