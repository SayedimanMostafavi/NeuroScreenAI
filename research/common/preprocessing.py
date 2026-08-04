import mne


class EEGPreprocessor:

    CHANNELS = [
        "EEG Fp1-LE",
        "EEG Fp2-LE",
        "EEG F3-LE",
        "EEG F4-LE",
        "EEG F7-LE",
        "EEG F8-LE",
        "EEG C3-LE",
        "EEG C4-LE",
        "EEG P3-LE",
        "EEG P4-LE",
        "EEG O1-LE",
        "EEG O2-LE",
        "EEG Fz-LE",
        "EEG Cz-LE",
        "EEG Pz-LE",
        "EEG A2-A1",
    ]

    def __init__(
        self,
        lowcut=1,
        highcut=40,
        notch=50,
    ):
        self.lowcut = lowcut
        self.highcut = highcut
        self.notch = notch

    def load(self, path):

        raw = mne.io.read_raw_edf(
            path,
            preload=True,
            verbose=False,
        )

        return raw

    def preprocess(self, raw):

        raw.filter(
            self.lowcut,
            self.highcut,
            verbose=False,
        )

        raw.notch_filter(
            self.notch,
            verbose=False,
        )

        raw.set_eeg_reference(
            "average",
            verbose=False,
        )

        raw.pick(self.CHANNELS)

        return raw

    def run(self, path):

        raw = self.load(path)

        raw = self.preprocess(raw)

        return raw
