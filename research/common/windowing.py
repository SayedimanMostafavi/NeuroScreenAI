import numpy as np


class WindowGenerator:

    def __init__(

        self,

        sfreq=256,

        window_sec=4,

        overlap=0.5,

    ):

        self.sfreq = sfreq

        self.window_size = int(window_sec * sfreq)

        self.step = int(self.window_size * (1 - overlap))

    def generate(self, raw):

        data = raw.get_data()

        windows = []

        for start in range(

            0,

            data.shape[1] - self.window_size + 1,

            self.step,

        ):

            stop = start + self.window_size

            windows.append(

                data[:, start:stop]

            )

        return np.asarray(

            windows,

            dtype=np.float32,

        )
