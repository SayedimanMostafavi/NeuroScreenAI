import numpy as np

from scipy.signal import coherence


class ConnectivityExtractor:

    def __init__(self, sfreq=256):

        self.sfreq = sfreq

        self.bands = {

            "delta": (1,4),

            "theta": (4,8),

            "alpha": (8,13),

            "beta": (13,30),

        }

    def compute(self, window):

        n_channels = window.shape[0]

        matrices = {}

        for band_name, band in self.bands.items():

            matrix = np.zeros((n_channels,n_channels))

            for i in range(n_channels):

                for j in range(i+1,n_channels):

                    f,cxy = coherence(

                        window[i],

                        window[j],

                        fs=self.sfreq,

                        nperseg=512,

                    )

                    idx = (f>=band[0]) & (f<band[1])

                    value = np.mean(cxy[idx])

                    matrix[i,j]=value

                    matrix[j,i]=value

            matrices[band_name]=matrix

        return matrices
