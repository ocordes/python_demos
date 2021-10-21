"""
loadaudio.py

written by: Oliver Cordes 2020-06-12
changed by: Oliver Cordes 2020-06-17


This module is based on the stackoverflow article:

https://stackoverflow.com/questions/53633177/how-to-read-a-mp3-audio-file-into-a-numpy-array-save-a-numpy-array-to-mp3/53633178

It provides a simple class to read the data from a mp3 file and return a numpy array

"""

# we need these modules for mp3
try:
    import pydub 
except:
    print('WARNING: pydub module cannot be loaded! Please install pydub!')
    
# for wavfile we need this module    
import scipy.io.wavfile as wavfile

import numpy as np


class audiofile(object):
    def __init__(self, filename, format=None, normalized=False):
        """
        __init__
        
            filename:  the filename of the data file
            format:    format of the data, if none, the filename will set the format
            normilzed: if set, the data will normalized after reading
            
        the constructor initialize the audio object
        """
        self._filename = filename
        self._data = None
        self._format = self._check_format(filename, format)
        self._normalized = normalized
        
        self._data = None
        self._frame_rate = None
        
        # read the data
        if self._format == 'wav':
            self.internal_read_wav()
        elif self._format == 'mp3':
            self.internal_read_mp3()
            
        
    def _check_format(self, filename, format):
        """
        _check_format
         
          filename: the filename to check
          format  : predefined format, mp3 or wav
        
        return the correct format for the file. format has the predecence over the filename
        """
        
        if format is not None:
            return format
        
        ending = filename.split('.')[-1].lower()
        
        if ending in ['wav', 'mp3']:
            return ending
        else:
            return 'wav'
        
        
    def internal_read_wav(self):
        self._frame_rate , self._data = wavfile.read('cdda.wav')
        
        if self._normalized:
            self._data /= 2**15

        
    def internal_read_mp3(self):
        """MP3 to numpy array"""
        a = pydub.AudioSegment.from_mp3(self._filename)
        self._data  = np.array(a.get_array_of_samples(), dtype=np.float64)
        self._frame_rate = a.frame_rate
        
        if a.channels == 2:
            self._data = self._data.reshape((-1, 2))
        if self._normalized:
            self._data /= 2**15
        
        
    def read(self):
        return self._data
    
    
    @property
    def frame_rate(self):
        return self._frame_rate
    
    
    @staticmethod
    def write(data, filename, frame_rate=44100, format='wav'):
        # converting to int
        int_data = np.array(data, dtype=np.int16)
        # make it stereo
        int_data = int_data[:,np.newaxis]
        # stereo
        sdata = np.broadcast_to(int_data, (int_data.shape[0],2))
        print(sdata.shape)
        if format == 'wav':
            wavfile.write(filename, frame_rate, sdata)
