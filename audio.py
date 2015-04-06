import pyaudio, audioop, wave, sys, os

from pyaudio import PyAudio

audioInterface = PyAudio()

#Converts to 16k FLAC Audio format
class Flac:
    path = 'Flac.exe'
    @staticmethod
    def convertFromWave(wavFilename):
        if (not wavFilename.endswith('.wav')):
            wavFileName+='.wav'
        os.system('%s -f --totally-silent %s'%(Flac.path, wavFilename))

class Microphone:

    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    WIDTH = 2
    RATE = 16000

    def __init__(self):
        self.stream = audioInterface.open(format=Microphone.FORMAT,
                    channels = Microphone.CHANNELS,
                    rate = Microphone.RATE,
                    input = True,
                    frames_per_buffer = Microphone.CHUNK)
        self.savedClips = []
        self.frames = []
        self.sampleVolume = 400
        
    def halt(self):
        self.stream.stop_stream()
        self.stream.close()
        audioInterface.terminate()

    def getCurrentData(self): #Volume, frame
        dataBlock = self.stream.read(Microphone.CHUNK)
        volume = audioop.rms(dataBlock, Microphone.WIDTH)
        return (volume,dataBlock)
        
    def getVolume(self):
        dataBlock = self.stream.read(Microphone.CHUNK)
        return audioop.rms(dataBlock, Microphone.WIDTH)

    def recordForTime(self, time = 5):
        self.frames = []
        for i in range(0, int(Microphone.RATE / Microphone.CHUNK * time)):
            data = self.stream.read(Microphone.CHUNK)
            self.frames.append(data)
            
        return self.frames
    
    def encodeAsWav(self, frames, filename = 'output.wav'):
        wf = wave.open(filename, 'wb')
        wf.setnchannels(Microphone.CHANNELS)
        wf.setsampwidth(audioInterface.get_sample_size(Microphone.FORMAT))
        wf.setframerate(Microphone.RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        return filename

    def encodeWavAsFlac(self, frames, filename = 'output.flac'):
        wavFilename = filename.replace('.flac','')+'.wav'
        Flac.convertFromWave(wavFilename)
        return filename

    def encodeAsFlac(self, frames, filename = 'output.flac'):
        wavFilename = filename.replace('.flac','') + '.wav'
        self.encodeAsWav(frames, wavFilename)
        Flac.convertFromWave(wavFilename)
        return filename

    def getSampleVolume(self, sampleTime = 5):
        self.sampleVolume = 0
        for i in range(0, int(Microphone.RATE / Microphone.CHUNK * sampleTime)):
            self.sampleVolume += self.getVolume()
        self.sampleVolume /= int(Microphone.RATE / Microphone.CHUNK * sampleTime)

    def recordPhrase(self, frames, filename = 'output.flac'):
        minimumChunkSize = 12
        if (len(frames) < minimumChunkSize):
            return 'short'
        elif (len(frames) > int(Microphone.RATE / Microphone.CHUNK * 10)):
            return 'long'
        self.encodeAsFlac(frames,filename)
        return filename
    
    def continuousListening(self, graph = None, silent = None):
        currentphrase = []
        maxsilent = 5
        isSilent = True
        timesilent = 0
        active = False
                          
        while True:
            v, dataBlock = self.getCurrentData()
            isSilent = self.sampleVolume*3 > v

            if not active:
                if not isSilent:
                    active = True
                    timesilent = 0
                    
            if active:
                if not isSilent:
                    timesilent = 0
                else:
                    timesilent += 1
                currentphrase.append(dataBlock)
                
            if timesilent > maxsilent:
                return self.recordPhrase(currentphrase)
az